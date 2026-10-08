"""
ContractShield AI — FastAPI Application Entry Point

This is the main application file that defines all API routes.
Route handlers are thin — they delegate to the agentic pipeline
(agents/orchestrator.py) for actual processing.

Run with:
    uvicorn main:app --reload --port 8000
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# Ensure backend directory is in sys.path so imports resolve from any CWD
_backend_dir = str(Path(__file__).resolve().parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models.enums import (
    ContractType,
    Industry,
    Jurisdiction,
    UserRole,
)
from models.schemas import (
    AnalyzeRequest,
    AnalysisResponse,
    ChatRequest,
    ChatResponse,
    HealthResponse,
)


# ═══════════════════════════════════════════════════════════════════
# APP INITIALIZATION
# ═══════════════════════════════════════════════════════════════════

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered contract risk analysis platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for completed analyses (sufficient for hackathon demo)
analyses_store: dict[str, AnalysisResponse] = {}


# ═══════════════════════════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════════════════════════


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
    )


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_contract(
    document: UploadFile = File(..., description="Contract file (PDF or DOCX)"),
    contract_type: ContractType = Form(...),
    parties: str = Form(..., description='JSON array of party names, e.g. ["Acme Corp", "StartupX"]'),
    jurisdiction: Jurisdiction = Form(...),
    user_role: UserRole | None = Form(None),
    industry: Industry | None = Form(None),
):
    """
    Upload and analyze a contract for legal risks.

    Accepts a PDF or DOCX file with metadata, runs the full agentic
    analysis pipeline (Plan → Act → Verify → Report), and returns
    a comprehensive risk report.
    """
    import json

    # ── Validate file type ───────────────────────────────
    if not document.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    file_ext = document.filename.rsplit(".", 1)[-1].lower() if "." in document.filename else ""
    if file_ext not in ("pdf", "docx"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{file_ext}. Only PDF and DOCX are supported.",
        )

    # ── Validate file size ───────────────────────────────
    file_bytes = await document.read()
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB.",
        )

    # ── Parse parties JSON ───────────────────────────────
    try:
        parties_list = json.loads(parties)
        if not isinstance(parties_list, list) or len(parties_list) < 2:
            raise ValueError("At least 2 parties required.")
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid parties format. Expected JSON array with ≥2 names. Error: {e}",
        )

    # ── Build request model ──────────────────────────────
    request = AnalyzeRequest(
        contract_type=contract_type,
        parties=parties_list,
        jurisdiction=jurisdiction,
        user_role=user_role,
        industry=industry,
    )

    # ── Run the agentic analysis pipeline ────────────────
    start_time = time.time()

    try:
        from agents.orchestrator import run_analysis

        result = await run_analysis(
            file_bytes=file_bytes,
            filename=document.filename,
            request=request,
        )
    except NotImplementedError:
        # During Phase 1, the pipeline isn't built yet.
        # Return a helpful message instead of crashing.
        raise HTTPException(
            status_code=501,
            detail=(
                "Analysis pipeline not yet implemented. "
                "This endpoint is wired up and ready — "
                "the pipeline will be built in Phases 2–4."
            ),
        )

    # ── Store result and return ──────────────────────────
    result.processing_time_ms = (time.time() - start_time) * 1000
    analyses_store[result.analysis_id] = result

    return result


@app.get("/api/v1/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    """Retrieve a previously computed analysis by ID."""
    if analysis_id not in analyses_store:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return analyses_store[analysis_id]


@app.get("/api/v1/clause-library")
async def get_clause_library(
    category: str | None = None,
    contract_type: str | None = None,
    severity: str | None = None,
    search: str | None = None,
):
    """
    Browse the clause library.

    Supports filtering by category, contract type, severity, and full-text search.
    Will be populated with data in Phase 3.
    """
    # Placeholder — will load from knowledge/clause_library.json in Phase 3
    return {
        "status": "placeholder",
        "message": "Clause library will be populated in Phase 3.",
        "filters": {
            "category": category,
            "contract_type": contract_type,
            "severity": severity,
            "search": search,
        },
        "clauses": [],
    }


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_contract(request: ChatRequest):
    """
    Ask follow-up questions about an analyzed contract.

    Requires a valid analysis_id from a previous analysis.
    Will be implemented as a stretch goal.
    """
    if request.analysis_id not in analyses_store:
        raise HTTPException(status_code=404, detail="Analysis not found. Analyze a contract first.")

    # Placeholder — will be implemented as a stretch goal
    return ChatResponse(
        analysis_id=request.analysis_id,
        question=request.question,
        answer="Chat feature will be implemented as a stretch goal. The analysis data is available for querying.",
        sources=[],
    )


# ═══════════════════════════════════════════════════════════════════
# STARTUP / SHUTDOWN EVENTS
# ═══════════════════════════════════════════════════════════════════


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"🛡️  {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 API docs:   http://localhost:{settings.BACKEND_PORT}/docs")
    print(f"🌐 Frontend:   {settings.FRONTEND_URL}")
    print(f"🤖 LLM model:  {settings.LLM_MODEL}")
    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "your_gemini_api_key_here":
        print("⚠️  WARNING: GOOGLE_API_KEY not set! LLM features will not work.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
