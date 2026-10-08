"""ContractShield AI — Models Package"""

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
    SEVERITY_MULTIPLIERS,
    CATEGORY_WEIGHTS,
    RISK_BAND_THRESHOLDS,
)

from .schemas import (
    AnalyzeRequest,
    ChatRequest,
    Clause,
    RiskFlag,
    SafeClause,
    AnalysisPlan,
    VerificationResult,
    DocumentInfo,
    RiskBreakdown,
    RiskSummary,
    AnalysisResponse,
    ChatResponse,
    HealthResponse,
)

__all__ = [
    # Enums
    "AnalysisStatus",
    "ContractType",
    "Industry",
    "Jurisdiction",
    "RiskBand",
    "RiskCategory",
    "SegmentationStrategy",
    "Severity",
    "UserRole",
    # Constants
    "SEVERITY_MULTIPLIERS",
    "CATEGORY_WEIGHTS",
    "RISK_BAND_THRESHOLDS",
    # Schemas
    "AnalyzeRequest",
    "ChatRequest",
    "Clause",
    "RiskFlag",
    "SafeClause",
    "AnalysisPlan",
    "VerificationResult",
    "DocumentInfo",
    "RiskBreakdown",
    "RiskSummary",
    "AnalysisResponse",
    "ChatResponse",
    "HealthResponse",
]
