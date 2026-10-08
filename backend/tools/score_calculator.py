"""
ContractShield AI — Score Calculator (Stub)

Computes the weighted composite risk score using:
  Score = min(100, Σ(Wi × Si × Ci) / N × 100)

Where:
  Wi = Category weight
  Si = Severity multiplier
  Ci = Confidence score
  N  = Normalization factor

Will be implemented in Phase 3.
"""

from models.schemas import RiskFlag, RiskSummary, RiskBreakdown
from models.enums import RiskBand


def calculate_risk_score(
    flags: list[RiskFlag],
    total_clauses: int,
) -> RiskSummary:
    """
    Calculate the overall risk score and summary from flagged risks.

    Args:
        flags: List of detected risk flags with severity and confidence.
        total_clauses: Total number of clauses analyzed.

    Returns:
        RiskSummary with overall score, band, label, and breakdown.
    """
    raise NotImplementedError("Score calculator will be implemented in Phase 3.")
