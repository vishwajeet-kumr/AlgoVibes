"""
ContractShield AI — Enums

All enumeration types used across the application.
These enums define the valid values for contract types, severities,
jurisdictions, risk categories, and other domain concepts.
"""

from enum import Enum


class ContractType(str, Enum):
    """Supported contract types for analysis."""
    NDA = "nda"
    SERVICE_AGREEMENT = "service_agreement"
    FREELANCE = "freelance"
    EMPLOYMENT = "employment"
    LEASE = "lease"
    VENDOR = "vendor"


class Jurisdiction(str, Enum):
    """Supported jurisdictions with region-specific legal rules."""
    INDIA = "india"
    US_CALIFORNIA = "us-california"
    US_DELAWARE = "us-delaware"
    US_NEWYORK = "us-newyork"
    UK = "uk"
    EU = "eu"


class Severity(str, Enum):
    """Risk severity levels, ordered from most to least severe."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RiskBand(str, Enum):
    """Overall risk classification bands based on composite score."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    """Categories of legal risk for clause classification."""
    LIABILITY = "liability"
    INDEMNIFICATION = "indemnification"
    IP_OWNERSHIP = "ip_ownership"
    NON_COMPETE = "non_compete"
    TERM_RENEWAL = "term_renewal"
    CONFIDENTIALITY = "confidentiality"
    TERMINATION = "termination"
    DISPUTE_RESOLUTION = "dispute_resolution"
    GOVERNING_LAW = "governing_law"
    DATA_PRIVACY = "data_privacy"
    PENALTY_DAMAGES = "penalty_damages"
    MISCELLANEOUS = "miscellaneous"


class UserRole(str, Enum):
    """Which contracting party the user represents."""
    PARTY_A = "party_a"
    PARTY_B = "party_b"


class Industry(str, Enum):
    """Industry context for analysis tuning."""
    TECH = "tech"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    REAL_ESTATE = "real_estate"
    GENERAL = "general"


class SegmentationStrategy(str, Enum):
    """How to segment the document into clauses."""
    REGEX = "regex"
    LLM = "llm"
    HYBRID = "hybrid"


class AnalysisStatus(str, Enum):
    """Status of a contract analysis job."""
    PENDING = "pending"
    PARSING = "parsing"
    PLANNING = "planning"
    ANALYZING = "analyzing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


# ── Severity Multipliers (used in risk score calculation) ────────

SEVERITY_MULTIPLIERS: dict[Severity, float] = {
    Severity.CRITICAL: 4.0,
    Severity.HIGH: 3.0,
    Severity.MEDIUM: 2.0,
    Severity.LOW: 1.0,
    Severity.INFO: 0.5,
}

# ── Category Weights (used in risk score calculation) ────────────

CATEGORY_WEIGHTS: dict[RiskCategory, float] = {
    RiskCategory.LIABILITY: 1.0,
    RiskCategory.INDEMNIFICATION: 0.95,
    RiskCategory.IP_OWNERSHIP: 0.90,
    RiskCategory.NON_COMPETE: 0.85,
    RiskCategory.TERM_RENEWAL: 0.80,
    RiskCategory.CONFIDENTIALITY: 0.75,
    RiskCategory.TERMINATION: 0.70,
    RiskCategory.DATA_PRIVACY: 0.65,
    RiskCategory.DISPUTE_RESOLUTION: 0.60,
    RiskCategory.GOVERNING_LAW: 0.50,
    RiskCategory.PENALTY_DAMAGES: 0.65,
    RiskCategory.MISCELLANEOUS: 0.40,
}

# ── Risk Band Thresholds ────────────────────────────────────────

RISK_BAND_THRESHOLDS: list[tuple[int, int, RiskBand, str]] = [
    (0, 25, RiskBand.LOW, "🟢 Low Risk — Safe to sign with minor review"),
    (26, 50, RiskBand.MEDIUM, "🟡 Medium Risk — Review flagged clauses before signing"),
    (51, 75, RiskBand.HIGH, "🟠 High Risk — Negotiate changes before signing"),
    (76, 100, RiskBand.CRITICAL, "🔴 Critical Risk — Do NOT sign without legal counsel"),
]
