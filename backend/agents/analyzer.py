"""
ContractShield AI — Analyzer Agent

ACT phase: Segments clauses, runs risk pattern matching (regex + LLM),
and identifies safe clauses.
"""

from models.schemas import AnalysisPlan, Clause, RiskFlag, SafeClause
from tools.clause_segmenter import segment_clauses
from tools.risk_matcher import match_risks


async def run_risk_analysis(
    raw_text: str,
    plan: AnalysisPlan,
    request_metadata: dict,
) -> tuple[list[Clause], list[RiskFlag], list[SafeClause]]:
    """
    Analyze clauses for legal risks.

    Args:
        raw_text: Full document text.
        plan: Analysis plan from the planner agent.
        request_metadata: Dict with contract_type, jurisdiction, user_role.

    Returns:
        A tuple of (clauses, flagged_risks, safe_clauses).
    """
    # ── Step 1: Segment clauses ──────────────────────────
    clauses = await segment_clauses(
        raw_text=raw_text,
        strategy=plan.segmentation_strategy,
        contract_type=plan.contract_type_detected,
        jurisdiction=plan.jurisdiction_ruleset,
    )

    if not clauses:
        return [], [], []

    # ── Step 2: Run risk matching on all clauses ─────────
    flags = await match_risks(
        clauses=clauses,
        jurisdiction=request_metadata.get("jurisdiction", "india"),
        contract_type=request_metadata.get("contract_type", "nda"),
        user_role=request_metadata.get("user_role"),
    )

    # ── Step 3: Identify safe clauses ────────────────────
    flagged_clause_ids = {flag.clause_id for flag in flags}

    safe_clauses = []
    for clause in clauses:
        if clause.clause_id not in flagged_clause_ids:
            safe_clauses.append(SafeClause(
                clause_id=clause.clause_id,
                clause_title=clause.clause_title,
                status="safe",
                note=f"No risks detected in this clause. Standard {clause.clause_category.value if clause.clause_category else 'general'} language.",
            ))

    return clauses, flags, safe_clauses
