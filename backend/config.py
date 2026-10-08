"""
ContractShield AI — Application Configuration

Centralized config using pydantic-settings for type-safe
environment variable loading. All other modules import from here.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # ── App ──────────────────────────────────────────────
    APP_NAME: str = "ContractShield AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:3000"

    # ── File Upload Limits ───────────────────────────────
    MAX_FILE_SIZE_MB: int = 10
    MAX_PAGES: int = 50

    # ── LLM / GenAI ─────────────────────────────────────
    GOOGLE_API_KEY: str = ""
    LLM_MODEL: str = "gemini-1.5-flash"
    VERIFICATION_MODEL: str = "gemini-1.5-pro"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_OUTPUT_TOKENS: int = 4096
    LLM_TOP_P: float = 0.95

    # ── Embeddings (Phase 3) ─────────────────────────────
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    SIMILARITY_THRESHOLD: float = 0.78

    # ── Database ─────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./contractshield.db"

    model_config = {
        "env_file": [".env", str(Path(__file__).resolve().parent / ".env")],
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


# Singleton instance — import this everywhere
settings = Settings()
