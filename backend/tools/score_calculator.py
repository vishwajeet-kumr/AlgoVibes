"""
ContractShield AI — Score Calculator

Computes the weighted composite risk score using:
  Score = min(100, Σ(Wi × Si × Ci) / N × 100)

Where:
  Wi = Category weight
  Si = Severity multiplier
  Ci = Confidence score
  N  = Normalization factor (total_clauses × max_possible_weight)
"""

from models.schemas import RiskFlag, RiskSummary, RiskBreakdown
from models.enums import (
    RiskBand,
    RiskCategory,
    Severity,
    SEVERITY_MULTIPLIERS,
    CATEGORY_WEIGHTS,
    RISK_BAND_THRESHOLDS,
)


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
    if not flags or total_clauses == 0:
        return RiskSummary(
            overall_score=0,
            risk_band=RiskBand.LOW,
            risk_label="🟢 Low Risk — Safe to sign with minor review",
            total_clauses_analyzed=total_clauses,
            total_risks_found=0,
            risk_breakdown=RiskBreakdown(),
        )

    # ── Count breakdown by severity ──────────────────────
    breakdown = RiskBreakdown(
        critical=sum(1 for f in flags if f.severity == Severity.CRITICAL),
        high=sum(1 for f in flags if f.severity == Severity.HIGH),
        medium=sum(1 for f in flags if f.severity == Severity.MEDIUM),
        low=sum(1 for f in flags if f.severity == Severity.LOW),
        info=sum(1 for f in flags if f.severity == Severity.INFO),
    )

    # ── Calculate weighted score ─────────────────────────
    # Score = min(100, Σ(Wi × Si × Ci) / N × 100)
    weighted_sum = 0.0
    for flag in flags:
        # Get category weight (default to MISCELLANEOUS weight)
        category = flag.risk_category or RiskCategory.MISCELLANEOUS
        wi = CATEGORY_WEIGHTS.get(category, 0.4)

        # Get severity multiplier
        si = SEVERITY_MULTIPLIERS.get(flag.severity, 1.0)

        # Confidence
        ci = flag.confidence

        weighted_sum += wi * si * ci

        # Store contribution on the flag
        flag.risk_score_contribution = round(wi * si * ci, 3)

    # Normalization: divide by total clauses × max possible weight per clause
    # Max weight per clause = max_category_weight (1.0) × max_severity (4.0) × max_confidence (1.0) = 4.0
    max_weight_per_clause = 4.0
    normalization_factor = total_clauses * max_weight_per_clause

    raw_score = (weighted_sum / normalization_factor) * 100
    overall_score = int(min(100, max(0, round(raw_score))))

    # ── Determine risk band and label ────────────────────
    risk_band = RiskBand.LOW
    risk_label = "🟢 Low Risk — Safe to sign with minor review"

    for low, high, band, label in RISK_BAND_THRESHOLDS:
        if low <= overall_score <= high:
            risk_band = band
            risk_label = label
            break

    return RiskSummary(
        overall_score=overall_score,
        risk_band=risk_band,
        risk_label=risk_label,
        total_clauses_analyzed=total_clauses,
        total_risks_found=len(flags),
        risk_breakdown=breakdown,
    )
