"""
ContractShield AI — Clause Segmenter

Segments contract text into individual clauses using:
  - Regex-based approach for well-structured documents
  - LLM-based approach for unstructured/prose-heavy documents
  - Hybrid approach combining both
"""

import json
import re
from pathlib import Path

from models.schemas import Clause
from models.enums import SegmentationStrategy, RiskCategory


# Regex patterns for clause boundaries
CLAUSE_PATTERNS = [
    # "Section 1.", "Section 1.1", "SECTION 1"
    r"(?:^|\n)\s*(?:SECTION|Section)\s+(\d+(?:\.\d+)*)\s*[.:\-—]?\s*(.*?)(?=\n)",
    # "Article I.", "ARTICLE 1"
    r"(?:^|\n)\s*(?:ARTICLE|Article)\s+([IVXLCDM]+|\d+)\s*[.:\-—]?\s*(.*?)(?=\n)",
    # "1.", "1.1", "1.1.1" at start of line
    r"(?:^|\n)\s*(\d+(?:\.\d+)*)\s*[.)\-]\s+(.*?)(?=\n)",
    # "A.", "B.", "(a)", "(b)" at start of line for sub-sections
    r"(?:^|\n)\s*(?:\(?([A-Z]|[a-z])\)?)\s*[.)]\s+(.*?)(?=\n)",
]

# Category keywords for auto-classification
CATEGORY_KEYWORDS: dict[str, RiskCategory] = {
    "definition": RiskCategory.MISCELLANEOUS,
    "confiden": RiskCategory.CONFIDENTIALITY,
    "non-disclosure": RiskCategory.CONFIDENTIALITY,
    "nondisclosure": RiskCategory.CONFIDENTIALITY,
    "secret": RiskCategory.CONFIDENTIALITY,
    "liabil": RiskCategory.LIABILITY,
    "indemn": RiskCategory.INDEMNIFICATION,
    "hold harmless": RiskCategory.INDEMNIFICATION,
    "intellectual property": RiskCategory.IP_OWNERSHIP,
    "copyright": RiskCategory.IP_OWNERSHIP,
    "patent": RiskCategory.IP_OWNERSHIP,
    "trademark": RiskCategory.IP_OWNERSHIP,
    "work for hire": RiskCategory.IP_OWNERSHIP,
    "work-for-hire": RiskCategory.IP_OWNERSHIP,
    "non-compete": RiskCategory.NON_COMPETE,
    "noncompete": RiskCategory.NON_COMPETE,
    "non-solicit": RiskCategory.NON_COMPETE,
    "restrictive covenant": RiskCategory.NON_COMPETE,
    "term": RiskCategory.TERM_RENEWAL,
    "duration": RiskCategory.TERM_RENEWAL,
    "renewal": RiskCategory.TERM_RENEWAL,
    "expir": RiskCategory.TERM_RENEWAL,
    "terminat": RiskCategory.TERMINATION,
    "cancel": RiskCategory.TERMINATION,
    "dispute": RiskCategory.DISPUTE_RESOLUTION,
    "arbitrat": RiskCategory.DISPUTE_RESOLUTION,
    "mediat": RiskCategory.DISPUTE_RESOLUTION,
    "governing law": RiskCategory.GOVERNING_LAW,
    "jurisdiction": RiskCategory.GOVERNING_LAW,
    "applicable law": RiskCategory.GOVERNING_LAW,
    "choice of law": RiskCategory.GOVERNING_LAW,
    "data": RiskCategory.DATA_PRIVACY,
    "privacy": RiskCategory.DATA_PRIVACY,
    "personal information": RiskCategory.DATA_PRIVACY,
    "gdpr": RiskCategory.DATA_PRIVACY,
    "penalty": RiskCategory.PENALTY_DAMAGES,
    "liquidated damage": RiskCategory.PENALTY_DAMAGES,
    "late fee": RiskCategory.PENALTY_DAMAGES,
    "damage": RiskCategory.PENALTY_DAMAGES,
}


def _detect_category(title: str, text: str) -> RiskCategory | None:
    """Detect the risk category based on clause title and text keywords."""
    combined = (title + " " + text).lower()
    for keyword, category in CATEGORY_KEYWORDS.items():
        if keyword in combined:
            return category
    return RiskCategory.MISCELLANEOUS


def _segment_by_regex(raw_text: str) -> list[dict]:
    """Segment using regex patterns for structured documents."""
    segments = []

    # Try each pattern and collect matches with positions
    all_matches = []
    for pattern in CLAUSE_PATTERNS:
        for match in re.finditer(pattern, raw_text):
            start = match.start()
            section_id = match.group(1) if match.group(1) else ""
            title = match.group(2).strip() if match.group(2) else ""
            all_matches.append((start, section_id, title))

    if not all_matches:
        return []

    # Sort by position in document
    all_matches.sort(key=lambda x: x[0])

    # Extract text between matches
    for i, (start, section_id, title) in enumerate(all_matches):
        # Get text until next match or end of document
        end = all_matches[i + 1][0] if i + 1 < len(all_matches) else len(raw_text)
        clause_text = raw_text[start:end].strip()

        if len(clause_text.split()) < 5:  # Skip very short fragments
            continue

        clause_id = f"section_{section_id}" if section_id else f"clause_{i + 1}"
        if not title:
            # Use first line as title
            first_line = clause_text.split("\n")[0].strip()
            title = first_line[:80] if len(first_line) > 80 else first_line

        segments.append({
            "clause_id": clause_id,
            "clause_title": title,
            "clause_text": clause_text,
        })

    return segments


def _segment_by_paragraphs(raw_text: str) -> list[dict]:
    """
    Fallback segmentation: split by double newlines (paragraph-based).
    Used when regex doesn't find enough structure.
    """
    paragraphs = re.split(r"\n\s*\n", raw_text)
    segments = []

    clause_num = 0
    for para in paragraphs:
        para = para.strip()
        if len(para.split()) < 10:  # Skip very short paragraphs
            continue

        clause_num += 1
        # Try to extract a title from the first line
        lines = para.split("\n")
        first_line = lines[0].strip()

        # If first line is short enough, treat it as a title
        if len(first_line.split()) <= 8 and len(lines) > 1:
            title = first_line
            text = para
        else:
            title = f"Clause {clause_num}"
            text = para

        segments.append({
            "clause_id": f"clause_{clause_num}",
            "clause_title": title,
            "clause_text": text,
        })

    return segments


async def _segment_by_llm(
    raw_text: str,
    contract_type: str,
    jurisdiction: str,
) -> list[dict]:
    """Segment using Gemini LLM for unstructured documents."""
    from config import settings

    try:
        from google import genai
    except ImportError:
        raise RuntimeError("google-genai is required for LLM segmentation.")

    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "your_gemini_api_key_here":
        raise ValueError("GOOGLE_API_KEY not configured. Cannot use LLM segmentation.")

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    # Load prompt template
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "segmentation.txt"
    prompt_template = prompt_path.read_text(encoding="utf-8")

    # Truncate text to avoid token limits (roughly 100K chars ≈ 30K tokens)
    truncated_text = raw_text[:100000]

    prompt = prompt_template.format(
        document_text=truncated_text,
        contract_type=contract_type,
        jurisdiction=jurisdiction,
    )

    response = client.models.generate_content(
        model=settings.LLM_MODEL,
        contents=prompt,
        config={
            "temperature": 0.1,
            "max_output_tokens": settings.LLM_MAX_OUTPUT_TOKENS,
        },
    )

    # Parse JSON response
    response_text = response.text.strip()
    # Strip markdown code fences if present
    if response_text.startswith("```"):
        response_text = re.sub(r"^```(?:json)?\s*\n?", "", response_text)
        response_text = re.sub(r"\n?```\s*$", "", response_text)

    try:
        clauses_data = json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON array from response
        json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
        if json_match:
            clauses_data = json.loads(json_match.group())
        else:
            return []

    return clauses_data if isinstance(clauses_data, list) else []


async def segment_clauses(
    raw_text: str,
    strategy: SegmentationStrategy,
    contract_type: str,
    jurisdiction: str,
) -> list[Clause]:
    """
    Segment a contract's raw text into individual clauses.

    Args:
        raw_text: The full text of the contract.
        strategy: Which segmentation approach to use.
        contract_type: Type of contract (for LLM context).
        jurisdiction: Jurisdiction (for LLM context).

    Returns:
        List of Clause objects, each representing a distinct clause.
    """
    segments = []

    if strategy == SegmentationStrategy.REGEX:
        segments = _segment_by_regex(raw_text)
        if len(segments) < 3:
            segments = _segment_by_paragraphs(raw_text)

    elif strategy == SegmentationStrategy.LLM:
        try:
            segments = await _segment_by_llm(raw_text, contract_type, jurisdiction)
        except Exception:
            # Fall back to regex + paragraph if LLM fails
            segments = _segment_by_regex(raw_text)
            if len(segments) < 3:
                segments = _segment_by_paragraphs(raw_text)

    elif strategy == SegmentationStrategy.HYBRID:
        # Try regex first
        segments = _segment_by_regex(raw_text)
        if len(segments) < 3:
            # Fall back to LLM
            try:
                segments = await _segment_by_llm(raw_text, contract_type, jurisdiction)
            except Exception:
                segments = _segment_by_paragraphs(raw_text)

    # Convert to Clause objects
    clauses = []
    for seg in segments:
        clause_id = seg.get("clause_id", f"clause_{len(clauses) + 1}")
        clause_title = seg.get("clause_title", f"Clause {len(clauses) + 1}")
        clause_text = seg.get("clause_text", "")

        if not clause_text or len(clause_text.split()) < 5:
            continue

        category_str = seg.get("clause_category", "")
        try:
            category = RiskCategory(category_str) if category_str else _detect_category(clause_title, clause_text)
        except ValueError:
            category = _detect_category(clause_title, clause_text)

        clauses.append(Clause(
            clause_id=clause_id,
            clause_title=clause_title,
            clause_text=clause_text,
            clause_category=category,
        ))

    return clauses
