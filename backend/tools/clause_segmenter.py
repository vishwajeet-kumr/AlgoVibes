"""
ContractShield AI — Clause Segmenter (Stub)

Segments contract text into individual clauses using:
  - Regex-based approach for well-structured documents
  - LLM-based approach for unstructured/prose-heavy documents
  - Hybrid approach combining both

Will be implemented in Phase 2.
"""

from models.schemas import Clause
from models.enums import SegmentationStrategy


async def segment_clauses(
    raw_text: str,
    strategy: SegmentationStrategy,
    contract_type: str,
    jurisdiction: str,
) -> list[Clause]:
    """
    Segment a contract's raw text into individual clauses.

    Args:
        raw_text: The full text of the contract.
        strategy: Which segmentation approach to use.
        contract_type: Type of contract (for LLM context).
        jurisdiction: Jurisdiction (for LLM context).

    Returns:
        List of Clause objects, each representing a distinct clause.
    """
    raise NotImplementedError("Clause segmenter will be implemented in Phase 2.")
