"""
ContractShield AI — Pydantic Schemas

All request/response models for the API and internal data structures.
These schemas define the contracts between frontend ↔ backend and
between internal pipeline stages.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .enums import (
    AnalysisStatus,
    ContractType,
    Industry,
    Jurisdiction,
    RiskBand,
    RiskCategory,
    SegmentationStrategy,
    Severity,
    UserRole,
)


# ═══════════════════════════════════════════════════════════════════
# REQUEST SCHEMAS
# ═══════════════════════════════════════════════════════════════════


class AnalyzeRequest(BaseModel):
    """Metadata submitted alongside the uploaded document."""
    contract_type: ContractType
    parties: list[str] = Field(..., min_length=2, max_length=10)
    jurisdiction: Jurisdiction
    user_role: Optional[UserRole] = None
    industry: Optional[Industry] = None


class ChatRequest(BaseModel):
    """Follow-up question about an analyzed contract."""
    analysis_id: str
    question: str = Field(..., min_length=1, max_length=2000)


# ═══════════════════════════════════════════════════════════════════
# INTERNAL PIPELINE SCHEMAS (used between agent phases)
# ═══════════════════════════════════════════════════════════════════


class Clause(BaseModel):
    """A single extracted clause from the document."""
    clause_id: str
    clause_title: str
    clause_text: str
    clause_category: Optional[RiskCategory] = None
    start_page: Optional[int] = None
    end_page: Optional[int] = None


class RiskFlag(BaseModel):
    """A single flagged risk within a clause."""
    clause_id: str
    clause_title: str
    clause_text: str
    risk_type: str
    severity: Severity
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str
    problematic_language: str
    suggested_alternative: str
    jurisdiction_note: Optional[str] = None
    risk_category: Optional[RiskCategory] = None
    risk_score_contribution: Optional[float] = None


class SafeClause(BaseModel):
    """A clause determined to be safe / standard."""
    clause_id: str
    clause_title: str
    status: str = "safe"
    note: str


class AnalysisPlan(BaseModel):
    """Output of the PLAN phase — the agent's analysis strategy."""
    contract_type_detected: str
    segmentation_strategy: SegmentationStrategy
    jurisdiction_ruleset: str
    analysis_modules: list[str]
    estimated_clauses: int


class VerificationResult(BaseModel):
    """Output of the VERIFY phase — quality checks."""
    all_flags_grounded: bool
    jurisdiction_rules_applied: bool
    segmentation_quality: str  # "high" | "medium" | "low"
    hallucination_check_passed: bool
    removed_flags: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════
# RESPONSE SCHEMAS
# ═══════════════════════════════════════════════════════════════════


class DocumentInfo(BaseModel):
    """Metadata extracted from the uploaded document."""
    filename: str
    pages: int
    word_count: int
    detected_contract_type: str
    detected_parties: list[str]


class RiskBreakdown(BaseModel):
    """Count of flagged risks by severity level."""
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    info: int = 0


class RiskSummary(BaseModel):
    """Top-level risk summary for the analyzed contract."""
    overall_score: int = Field(..., ge=0, le=100)
    risk_band: RiskBand
    risk_label: str
    total_clauses_analyzed: int
    total_risks_found: int
    risk_breakdown: RiskBreakdown


class AnalysisResponse(BaseModel):
    """Full analysis response returned by POST /api/v1/analyze."""
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: AnalysisStatus
    processing_time_ms: float
    document_info: DocumentInfo
    risk_summary: RiskSummary
    flags: list[RiskFlag]
    safe_clauses: list[SafeClause]
    verification: VerificationResult
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatResponse(BaseModel):
    """Response to a follow-up chat question."""
    analysis_id: str
    question: str
    answer: str
    sources: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
