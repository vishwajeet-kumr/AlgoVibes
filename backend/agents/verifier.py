"""
ContractShield AI — Verifier Agent (Stub)

VERIFY phase: Validates risk flags against source text,
checks for hallucinated references, validates severity calibration,
and ensures jurisdiction rules were properly applied.

Will be implemented in Phase 4.
"""

from models.schemas import RiskFlag, VerificationResult


async def verify_risk_flags(
    raw_text: str,
    flags: list[RiskFlag],
    jurisdiction: str,
) -> tuple[list[RiskFlag], VerificationResult]:
    """
    Verify and validate risk flags against the original document.

    Returns:
        A tuple of (validated_flags, verification_result).
        Flags that fail verification are removed from the list.
    """
    raise NotImplementedError("Verifier will be implemented in Phase 4.")
