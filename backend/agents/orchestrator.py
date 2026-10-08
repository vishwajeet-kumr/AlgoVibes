"""
ContractShield AI — Agentic Orchestrator

Main agentic loop controller that coordinates:
  PLAN → ACT → VERIFY → REPORT

This module wires together all pipeline stages:
  1. INPUT  — Parse document, extract raw text
  2. PLAN   — Decide analysis strategy
  3. ACT    — Segment clauses → match risks → score
  4. VERIFY — Ground flags, check hallucinations, validate severity
  5. REPORT — Assemble final AnalysisResponse
"""

import traceback
from datetime import datetime

from models.schemas import (
    AnalyzeRequest,
    AnalysisResponse,
    DocumentInfo,
)
from models.enums import AnalysisStatus

from tools.document_parser import parse_document
from tools.score_calculator import calculate_risk_score
from agents.planner import create_analysis_plan
from agents.analyzer import run_risk_analysis
from agents.verifier import verify_risk_flags


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
    try:
        # ═══════════════════════════════════════════════════
        # Phase 1: INPUT — Parse document
        # ═══════════════════════════════════════════════════
        parsed_doc = await parse_document(file_bytes, filename)

        # ═══════════════════════════════════════════════════
        # Phase 2: PLAN — Decide analysis strategy
        # ═══════════════════════════════════════════════════
        plan = await create_analysis_plan(parsed_doc.raw_text, request)

        # ═══════════════════════════════════════════════════
        # Phase 3: ACT — Segment, match risks, identify safe
        # ═══════════════════════════════════════════════════
        request_metadata = {
            "contract_type": request.contract_type.value,
            "jurisdiction": request.jurisdiction.value,
            "user_role": request.user_role.value if request.user_role else None,
        }

        clauses, flags, safe_clauses = await run_risk_analysis(
            raw_text=parsed_doc.raw_text,
            plan=plan,
            request_metadata=request_metadata,
        )

        # ═══════════════════════════════════════════════════
        # Phase 4: VERIFY — Validate flags
        # ═══════════════════════════════════════════════════
        verified_flags, verification = await verify_risk_flags(
            raw_text=parsed_doc.raw_text,
            flags=flags,
            jurisdiction=request.jurisdiction.value,
        )

        # ═══════════════════════════════════════════════════
        # Phase 5: REPORT — Calculate score and assemble
        # ═══════════════════════════════════════════════════
        total_clauses = len(clauses)
        risk_summary = calculate_risk_score(verified_flags, total_clauses)

        # Build document info
        document_info = DocumentInfo(
            filename=filename,
            pages=parsed_doc.pages,
            word_count=parsed_doc.word_count,
            detected_contract_type=plan.contract_type_detected,
            detected_parties=request.parties,
        )

        # Assemble final response
        response = AnalysisResponse(
            status=AnalysisStatus.COMPLETED,
            processing_time_ms=0,  # Will be set by the route handler
            document_info=document_info,
            risk_summary=risk_summary,
            flags=verified_flags,
            safe_clauses=safe_clauses,
            verification=verification,
        )

        return response

    except ValueError as e:
        # Document parsing errors
        raise ValueError(str(e))

    except Exception as e:
        # Log the full traceback for debugging
        traceback.print_exc()
        raise RuntimeError(f"Analysis pipeline failed: {str(e)}")
