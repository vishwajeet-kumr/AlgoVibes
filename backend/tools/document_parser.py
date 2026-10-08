"""
ContractShield AI — Document Parser (Stub)

Handles PDF and DOCX text extraction.
Uses PyMuPDF (fitz) for PDFs and python-docx for DOCX files.

Will be implemented in Phase 2.
"""

from dataclasses import dataclass


@dataclass
class ParsedDocument:
    """Result of parsing an uploaded document."""
    raw_text: str
    pages: int
    word_count: int
    filename: str


async def parse_document(file_bytes: bytes, filename: str) -> ParsedDocument:
    """
    Extract text content from a PDF or DOCX file.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename: Original filename (used to determine file type).

    Returns:
        ParsedDocument with extracted text and metadata.

    Raises:
        ValueError: If file type is unsupported or file is corrupted.
    """
    raise NotImplementedError("Document parser will be implemented in Phase 2.")
