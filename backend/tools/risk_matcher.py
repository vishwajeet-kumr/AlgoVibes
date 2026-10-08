"""
ContractShield AI — Risk Matcher

Dual-layer risk detection:
  1. Deterministic: Regex pattern matching against 50+ risk patterns
  2. Contextual: LLM-based nuanced risk analysis via Gemini
"""

import json
import re
from pathlib import Path

from models.schemas import Clause, RiskFlag
from models.enums import RiskCategory, Severity


def _load_risk_patterns() -> dict:
    """Load risk patterns from the knowledge base."""
    patterns_path = Path(__file__).resolve().parent.parent / "knowledge" / "risk_patterns.json"
    with open(patterns_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("patterns", {})


def _load_jurisdiction_rules(jurisdiction: str) -> dict:
    """Load jurisdiction-specific rules."""
    rules_path = Path(__file__).resolve().parent.parent / "knowledge" / "jurisdiction_rules.json"
    with open(rules_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("jurisdictions", {}).get(jurisdiction, {})


def _regex_match_clause(clause: Clause, patterns: dict) -> list[dict]:
    """Run regex patterns against a single clause and return matches."""
    matches = []

    for category_name, category_patterns in patterns.items():
        for pattern_info in category_patterns:
            regex = pattern_info["regex"]
            try:
                match = re.search(regex, clause.clause_text, re.IGNORECASE | re.DOTALL)
            except re.error:
                continue

            if match:
                matches.append({
                    "category": category_name,
                    "pattern_id": pattern_info["id"],
                    "severity": pattern_info["severity"],
                    "risk_type": pattern_info["risk_type"],
                    "description": pattern_info["description"],
                    "matched_text": match.group(0)[:200],  # Limit matched text length
                })

    return matches


async def _llm_analyze_clause(
    clause: Clause,
    jurisdiction: str,
    contract_type: str,
    user_role: str | None,
    jurisdiction_rules: dict,
) -> list[dict]:
    """Use Gemini to analyze a clause for risks."""
    from config import settings

    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "your_gemini_api_key_here":
        return []

    try:
        from google import genai
    except ImportError:
        return []

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    # Load analysis prompt template
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "analysis.txt"
    prompt_template = prompt_path.read_text(encoding="utf-8")

    role_str = user_role if user_role else "the reviewing party"
    parties_str = "the contracting parties"

    # Add jurisdiction context
    jurisdiction_notes = ""
    if jurisdiction_rules and "notes" in jurisdiction_rules:
        notes = jurisdiction_rules["notes"]
        jurisdiction_notes = "\n".join(f"- {k}: {v}" for k, v in notes.items())

    prompt = prompt_template.format(
        contract_type=contract_type,
        jurisdiction=jurisdiction,
        user_role=role_str,
        clause_title=clause.clause_title,
        clause_text=clause.clause_text[:3000],  # Limit text length
        parties=parties_str,
    )

    if jurisdiction_notes:
        prompt += f"\n\nJurisdiction-specific rules to consider:\n{jurisdiction_notes}"

    try:
        response = client.models.generate_content(
            model=settings.LLM_MODEL,
            contents=prompt,
            config={
                "temperature": 0.1,
                "max_output_tokens": 2048,
            },
        )

        response_text = response.text.strip()
        # Strip markdown code fences
        if response_text.startswith("```"):
            response_text = re.sub(r"^```(?:json)?\s*\n?", "", response_text)
            response_text = re.sub(r"\n?```\s*$", "", response_text)

        risks = json.loads(response_text)
        return risks if isinstance(risks, list) else []

    except Exception:
        return []


async def match_risks(
    clauses: list[Clause],
    jurisdiction: str,
    contract_type: str,
    user_role: str | None = None,
) -> list[RiskFlag]:
    """
    Detect risks in extracted clauses using regex + LLM analysis.

    Args:
        clauses: List of segmented clauses from the contract.
        jurisdiction: Legal jurisdiction for context-aware analysis.
        contract_type: Type of contract being analyzed.
        user_role: Which party the user represents (for perspective).

    Returns:
        List of RiskFlag objects for each detected risk.
    """
    patterns = _load_risk_patterns()
    jurisdiction_rules = _load_jurisdiction_rules(jurisdiction)
    all_flags: list[RiskFlag] = []

    for clause in clauses:
        # ── Layer 1: Regex pattern matching ──────────────────
        regex_matches = _regex_match_clause(clause, patterns)

        # Track which risk types we've already found via regex
        found_risk_types = set()

        for match_info in regex_matches:
            try:
                severity = Severity(match_info["severity"])
            except ValueError:
                severity = Severity.MEDIUM

            try:
                category = RiskCategory(match_info["category"])
            except ValueError:
                category = clause.clause_category or RiskCategory.MISCELLANEOUS

            # Generate jurisdiction note if applicable
            jurisdiction_note = None
            if jurisdiction_rules and "notes" in jurisdiction_rules:
                for key, note in jurisdiction_rules["notes"].items():
                    if key.lower() in match_info["category"].lower() or key.lower() in match_info["risk_type"].lower():
                        jurisdiction_note = note
                        break

            flag = RiskFlag(
                clause_id=clause.clause_id,
                clause_title=clause.clause_title,
                clause_text=clause.clause_text[:500],
                risk_type=match_info["risk_type"],
                severity=severity,
                confidence=0.75,  # Regex matches get moderate confidence
                explanation=match_info["description"],
                problematic_language=match_info["matched_text"],
                suggested_alternative=f"Consider adding protections against: {match_info['description'].lower()}",
                jurisdiction_note=jurisdiction_note,
                risk_category=category,
            )

            all_flags.append(flag)
            found_risk_types.add(match_info["risk_type"])

        # ── Layer 2: LLM contextual analysis ─────────────────
        # Only run LLM on clauses where regex found something interesting,
        # or on clauses that seem important (by category)
        should_run_llm = (
            len(regex_matches) > 0 or
            clause.clause_category in [
                RiskCategory.LIABILITY,
                RiskCategory.INDEMNIFICATION,
                RiskCategory.IP_OWNERSHIP,
                RiskCategory.NON_COMPETE,
                RiskCategory.TERMINATION,
            ]
        )

        if should_run_llm:
            llm_risks = await _llm_analyze_clause(
                clause, jurisdiction, contract_type, user_role, jurisdiction_rules
            )

            for risk in llm_risks:
                risk_type = risk.get("risk_type", "unknown")

                # Skip if regex already caught this
                if risk_type in found_risk_types:
                    continue

                try:
                    severity = Severity(risk.get("severity", "medium"))
                except ValueError:
                    severity = Severity.MEDIUM

                confidence = min(1.0, max(0.0, float(risk.get("confidence", 0.7))))

                flag = RiskFlag(
                    clause_id=clause.clause_id,
                    clause_title=clause.clause_title,
                    clause_text=clause.clause_text[:500],
                    risk_type=risk_type,
                    severity=severity,
                    confidence=confidence,
                    explanation=risk.get("explanation", "Risk detected by AI analysis"),
                    problematic_language=risk.get("problematic_language", ""),
                    suggested_alternative=risk.get("suggested_alternative", "Consult with legal counsel"),
                    jurisdiction_note=risk.get("jurisdiction_note"),
                    risk_category=clause.clause_category or RiskCategory.MISCELLANEOUS,
                )

                all_flags.append(flag)

    return all_flags
