"""
ContractShield AI — Agentic Orchestrator (Stub)

Main agentic loop controller that coordinates:
  PLAN → ACT → VERIFY → REPORT

This module will be fully implemented in Phase 4.
"""

from models.schemas import AnalyzeRequest, AnalysisResponse


async def run_analysis(
    file_bytes: bytes,
    filename: str,
    request: AnalyzeRequest,
) -> AnalysisResponse:
    """
    Run the full agentic analysis pipeline on an uploaded contract.

    Args:
        file_bytes: Raw bytes of the uploaded PDF/DOCX file.
        filename: Original filename of the uploaded document.
        request: Metadata about the contract (type, parties, jurisdiction, etc.)

    Returns:
        AnalysisResponse with risk flags, score, and verification results.

    Phases:
        1. INPUT  — Parse document, extract raw text
        2. PLAN   — Decide analysis strategy (segmentation, modules, rules)
        3. ACT    — Segment clauses → match risks → score
        4. VERIFY — Ground flags, check hallucinations, validate severity
        5. REPORT — Assemble final response
    """
    raise NotImplementedError(
        "Orchestrator will be implemented in Phase 4. "
        "Phases 2 & 3 (parsing, risk engine) must be built first."
    )
