"""
ContractShield AI — Planner Agent

PLAN phase: Identifies contract type, selects jurisdiction rules,
chooses segmentation strategy, and determines analysis modules.
"""

from models.schemas import AnalysisPlan, AnalyzeRequest
from models.enums import SegmentationStrategy


# Keywords that suggest structured documents (numbered sections, articles, etc.)
STRUCTURED_KEYWORDS = [
    r"\bSection\s+\d",
    r"\bArticle\s+[IVX\d]",
    r"\b\d+\.\d+",
    r"\bClause\s+\d",
]


async def create_analysis_plan(
    raw_text: str,
    request: AnalyzeRequest,
) -> AnalysisPlan:
    """
    Create an analysis plan based on the document content and metadata.

    Returns an AnalysisPlan specifying:
      - Detected contract type
      - Segmentation strategy (regex / llm / hybrid)
      - Jurisdiction ruleset to apply
      - Which analysis modules to run
      - Estimated number of clauses
    """
    import re

    # ── Detect document structure ────────────────────────
    structured_count = 0
    for pattern in STRUCTURED_KEYWORDS:
        matches = re.findall(pattern, raw_text, re.IGNORECASE)
        structured_count += len(matches)

    # Decide segmentation strategy based on structure
    word_count = len(raw_text.split())
    if structured_count >= 5:
        strategy = SegmentationStrategy.REGEX
    elif structured_count >= 2:
        strategy = SegmentationStrategy.HYBRID
    else:
        strategy = SegmentationStrategy.HYBRID  # Default to hybrid

    # ── Estimate clauses ─────────────────────────────────
    # Rough heuristic: 1 clause per ~200 words for structured docs
    estimated_clauses = max(3, min(50, word_count // 200))

    # ── Determine analysis modules ───────────────────────
    modules = [
        "document_parser",
        "clause_segmenter",
        "risk_matcher",
        "score_calculator",
    ]

    # Contract-type-specific modules
    contract_type_str = request.contract_type.value
    if contract_type_str in ("nda", "employment"):
        modules.append("non_compete_analyzer")
        modules.append("confidentiality_analyzer")
    if contract_type_str in ("service_agreement", "freelance", "vendor"):
        modules.append("liability_analyzer")
        modules.append("ip_analyzer")

    return AnalysisPlan(
        contract_type_detected=contract_type_str,
        segmentation_strategy=strategy,
        jurisdiction_ruleset=request.jurisdiction.value,
        analysis_modules=modules,
        estimated_clauses=estimated_clauses,
    )
