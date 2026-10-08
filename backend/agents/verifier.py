"""
ContractShield AI — Verifier Agent

VERIFY phase: Validates risk flags against source text,
checks for hallucinated references, validates severity calibration,
and ensures jurisdiction rules were properly applied.
"""

import json
import re
from pathlib import Path

from models.schemas import RiskFlag, VerificationResult


async def verify_risk_flags(
    raw_text: str,
    flags: list[RiskFlag],
    jurisdiction: str,
) -> tuple[list[RiskFlag], VerificationResult]:
    """
    Verify and validate risk flags against the original document.

    Returns:
        A tuple of (validated_flags, verification_result).
        Flags that fail verification are removed from the list.
    """
    if not flags:
        return [], VerificationResult(
            all_flags_grounded=True,
            jurisdiction_rules_applied=True,
            segmentation_quality="high",
            hallucination_check_passed=True,
            removed_flags=[],
            notes="No flags to verify.",
        )

    validated_flags = []
    removed_flag_ids = []
    all_grounded = True

    for flag in flags:
        # ── Check 1: Is the problematic language actually in the document? ──
        grounded = True
        if flag.problematic_language:
            # Clean and check if the problematic text exists in the document
            clean_problematic = flag.problematic_language.strip().lower()
            clean_document = raw_text.lower()

            # Check for exact or near-exact match
            if clean_problematic and len(clean_problematic) > 10:
                # For longer text, check substring match
                if clean_problematic not in clean_document:
                    # Try with some fuzzy matching (first 50 chars)
                    partial = clean_problematic[:50]
                    if partial not in clean_document:
                        grounded = False
                        all_grounded = False

        # ── Check 2: Severity validation ─────────────────────
        # Very low confidence flags with high severity are suspicious
        severity_valid = True
        if flag.confidence < 0.3 and flag.severity.value in ("critical", "high"):
            severity_valid = False

        # ── Check 3: Duplicate detection ─────────────────────
        is_duplicate = False
        for existing_flag in validated_flags:
            if (existing_flag.clause_id == flag.clause_id and
                existing_flag.risk_type == flag.risk_type):
                is_duplicate = True
                break

        # ── Decision: keep or remove ─────────────────────────
        if not grounded or not severity_valid or is_duplicate:
            reason = []
            if not grounded:
                reason.append("problematic language not found in document")
            if not severity_valid:
                reason.append("low confidence with high severity")
            if is_duplicate:
                reason.append("duplicate flag")
            removed_flag_ids.append(f"{flag.clause_id}:{flag.risk_type} — {', '.join(reason)}")
        else:
            validated_flags.append(flag)

    # ── Check jurisdiction rules were considered ─────────
    jurisdiction_applied = any(f.jurisdiction_note for f in validated_flags)

    # ── Determine segmentation quality ───────────────────
    total_flags = len(flags)
    removed_count = len(removed_flag_ids)
    if removed_count == 0:
        seg_quality = "high"
    elif removed_count / max(total_flags, 1) < 0.2:
        seg_quality = "high"
    elif removed_count / max(total_flags, 1) < 0.5:
        seg_quality = "medium"
    else:
        seg_quality = "low"

    # ── Optional: LLM verification for high-value flags ──
    # Try to use Gemini for additional verification of critical flags
    llm_verified = await _llm_verify_critical_flags(raw_text, validated_flags, jurisdiction)

    verification = VerificationResult(
        all_flags_grounded=all_grounded,
        jurisdiction_rules_applied=jurisdiction_applied,
        segmentation_quality=seg_quality,
        hallucination_check_passed=(removed_count / max(total_flags, 1)) < 0.3,
        removed_flags=removed_flag_ids,
        notes=f"Verified {len(validated_flags)} flags. Removed {removed_count} flags. {llm_verified}",
    )

    return validated_flags, verification


async def _llm_verify_critical_flags(
    raw_text: str,
    flags: list[RiskFlag],
    jurisdiction: str,
) -> str:
    """Use LLM to verify critical/high severity flags."""
    from config import settings

    critical_flags = [f for f in flags if f.severity.value in ("critical", "high")]
    if not critical_flags or not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "your_gemini_api_key_here":
        return ""

    try:
        from google import genai

        client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        # Load verification prompt
        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "verification.txt"
        prompt_template = prompt_path.read_text(encoding="utf-8")

        # Prepare flags JSON (limit to top 10 critical/high flags)
        flags_data = []
        for i, f in enumerate(critical_flags[:10]):
            flags_data.append({
                "index": i,
                "clause_title": f.clause_title,
                "risk_type": f.risk_type,
                "severity": f.severity.value,
                "explanation": f.explanation,
                "problematic_language": f.problematic_language[:200],
            })

        prompt = prompt_template.format(
            document_text=raw_text[:50000],  # Limit document length
            risk_flags_json=json.dumps(flags_data, indent=2),
            jurisdiction=jurisdiction,
        )

        response = client.models.generate_content(
            model=settings.VERIFICATION_MODEL,
            contents=prompt,
            config={
                "temperature": 0.1,
                "max_output_tokens": 2048,
            },
        )

        response_text = response.text.strip()
        # Strip code fences
        if response_text.startswith("```"):
            response_text = re.sub(r"^```(?:json)?\s*\n?", "", response_text)
            response_text = re.sub(r"\n?```\s*$", "", response_text)

        try:
            verification_data = json.loads(response_text)
            quality = verification_data.get("overall_quality", "unknown")
            return f"LLM verification quality: {quality}."
        except json.JSONDecodeError:
            return "LLM verification completed."

    except Exception:
        return ""
