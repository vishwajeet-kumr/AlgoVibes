# 🛡️ ContractShield AI — AGENTS.md
> Coding instructions for AI agents (Antigravity, Claude, Cursor, Copilot, etc.)  
> Read this file BEFORE writing any code in this repository.

---

## 🎯 Project Overview

**ContractShield AI** is a hackathon project by team AlgoVibes for CodeFiesta (24-hour hackathon at GIT Jaipur).  
It's an AI-powered contract risk analyzer: upload a PDF/DOCX → get clause-level risk flags + a 0–100 risk score.

**Always read `ACTIVE_CONTEXT.md` first** — it has the exact current state of what's built vs what's pending.

---

## 🏗️ Architecture

```
frontend/    → Next.js 16 + Tailwind CSS v4 + TypeScript (App Router)
backend/     → FastAPI (Python 3.11+) + Google Gemini AI
venv/        → Python virtualenv (at repo ROOT, not inside backend/)
```

**Agentic Pipeline:** `INPUT → PLAN → ACT → VERIFY → REPORT`

---

## 🧠 Backend Rules

### 1. Python & FastAPI
- Python 3.11+. Use type hints everywhere. Use `async def` for all route handlers and agent functions.
- FastAPI patterns: all routes live in `backend/main.py`. Route handlers are **thin** — delegate to `agents/orchestrator.py`.
- Config: always import `from config import settings` — never hardcode values.
- NEVER add a bare `except:` — always catch specific exceptions.

### 2. Pydantic Models
- All request/response models are in `backend/models/schemas.py`.
- All enums + constants are in `backend/models/enums.py`.
- **Do not change schema field names** — the frontend `lib/types.ts` is a 1:1 mirror.
- When adding new fields, add them as `Optional` with defaults to avoid breaking existing API consumers.

### 3. LLM / Gemini Integration
- Use the `google-genai` package (`import google.generativeai as genai` OR the newer `google-genai` SDK).
- **Primary model:** `settings.LLM_MODEL` (default: `gemini-1.5-flash`) — for analysis.
- **Verification model:** `settings.VERIFICATION_MODEL` (default: `gemini-1.5-pro`) — for verification only.
- Temperature: `settings.LLM_TEMPERATURE` (0.1 — low, for deterministic output).
- All LLM calls must handle `json.JSONDecodeError` — Gemini sometimes wraps JSON in markdown code fences.
- Strip markdown fences before parsing: `text.strip().removeprefix("```json").removesuffix("```").strip()`

### 4. Prompt Templates
- Prompts are in `backend/prompts/*.txt` as string templates with `{variable}` placeholders.
- Load with: `Path("prompts/analysis.txt").read_text()` then `.format(**kwargs)`.
- **Never** embed multi-line prompts inline in Python code — always use the `.txt` files.

### 5. Tools (backend/tools/)
Each tool is a standalone async function. Implement in this order:
1. `document_parser.py` → `parse_document(file_bytes, filename) -> ParsedDocument`
2. `clause_segmenter.py` → `segment_clauses(raw_text, strategy, contract_type, jurisdiction) -> list[Clause]`
3. `risk_matcher.py` → `match_risks(clauses, jurisdiction, contract_type, user_role) -> list[RiskFlag]`
4. `score_calculator.py` → `calculate_risk_score(flags, total_clauses) -> RiskSummary`

**Replace `raise NotImplementedError` — do not keep stubs.**

### 6. Agents (backend/agents/)
Implement in this order (after all tools work):
1. `planner.py` → calls no tools, just LLM to detect contract type + choose strategy
2. `analyzer.py` → calls document_parser → clause_segmenter → risk_matcher → score_calculator
3. `verifier.py` → calls Gemini with verification prompt to QA the flags
4. `orchestrator.py` → wires: planner → analyzer → verifier → assembles `AnalysisResponse`

### 7. Knowledge Files
- `backend/knowledge/risk_patterns.json` — Use this structure:
  ```json
  {
    "patterns": {
      "liability": [{"pattern": "regex here", "description": "..."}],
      "indemnification": [...]
    }
  }
  ```
- `backend/knowledge/jurisdiction_rules.json` — Rules per jurisdiction string (e.g., `"india"`, `"us-california"`)
- `backend/knowledge/clause_library.json` — Risky vs safe examples per `RiskCategory`

### 8. Error Handling
- Tool failures → raise `ValueError` with descriptive message
- LLM failures → retry once, then raise
- In `main.py`, catch all errors with proper `HTTPException(status_code=..., detail=...)`
- Log with `print()` for hackathon (no logging setup needed)

### 9. Running the Backend
```bash
source venv/bin/activate          # venv is at REPO ROOT
cd backend
uvicorn main:app --reload --port 8000
```

---

## 🎨 Frontend Rules

### 1. Framework
- **Next.js 16** with App Router (`app/` directory). 
- **READ `frontend/AGENTS.md`** before touching any Next.js code — this version has breaking changes from what you know.
- TypeScript strictly. No `any` types. All types come from `frontend/lib/types.ts`.

### 2. Styling
- **Tailwind CSS v4** — syntax differs from v3. Use `@import "tailwindcss"` not `@tailwind base/components/utilities`.
- Design tokens are in `frontend/app/globals.css`. Use CSS variables: `var(--color-accent)`, `var(--card-bg)`, etc.
- **Dark theme only.** Background `#0a0a0a`. Cards `#1a1a2e`.
- Glassmorphism cards: `backdrop-blur-sm` + `bg-[#1a1a2e]` + `border border-[rgba(255,255,255,0.08)]`
- No shadcn/ui installed yet — build components from scratch with Tailwind.

### 3. API Calls
- **Always use `frontend/lib/api.ts`** — never call `fetch` directly in components.
- Available functions: `checkHealth()`, `analyzeContract()`, `getAnalysis()`, `getClauseLibrary()`, `chatWithContract()`
- `ApiError` class is exported from `api.ts` — use it for typed error handling.

### 4. Types
- All types are in `frontend/lib/types.ts` — mirrors `backend/models/schemas.py` exactly.
- Key types: `AnalysisResponse`, `RiskFlag`, `SafeClause`, `RiskSummary`, `DocumentInfo`
- Enums are string unions (e.g., `type Severity = "critical" | "high" | "medium" | "low" | "info"`)
- Constants/configs: `SEVERITY_CONFIG`, `RISK_BAND_CONFIG`, `CONTRACT_TYPE_OPTIONS`, `JURISDICTION_OPTIONS`
- Utility functions: `cn()`, `formatFileSize()`, `formatDuration()`, `formatRiskScore()`, `formatRelativeTime()`

### 5. Pages
| Route | File | Current State |
|-------|------|---------------|
| `/` | `app/page.tsx` | Scaffold — replace with real upload UI (Phase 5) |
| `/analyze/[id]` | `app/analyze/[id]/page.tsx` | Stub — replace with dashboard (Phase 6) |
| `/clause-library` | `app/clause-library/page.tsx` | Stub — stretch goal (Phase 7) |

### 6. Components
- Place all reusable components in `frontend/components/` (e.g., `components/FileUpload.tsx`)
- `components/ui/` is empty — start here for base UI elements
- Components should be `'use client'` only when they need browser APIs or event handlers

### 7. Running the Frontend
```bash
cd frontend
npm run dev
# http://localhost:3000
```

---

## 🔐 Environment Variables

### Backend (`backend/.env`)
```env
GOOGLE_API_KEY=<real-key-from-root-.env>
LLM_MODEL=gemini-1.5-flash
VERIFICATION_MODEL=gemini-1.5-pro
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
MAX_FILE_SIZE_MB=10
MAX_PAGES=50
DEBUG=true
DATABASE_URL=sqlite:///./contractshield.db
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

> ⚠️ Both files are gitignored. Create them manually on each machine.

---

## 🚫 Things NOT To Do

1. **Don't change Pydantic schema field names** — breaks frontend type sync
2. **Don't use ChromaDB or sentence-transformers** — decided to skip for MVP (pure regex + LLM)
3. **Don't use LangChain or LangGraph** — custom orchestrator only
4. **Don't add database ORM** — in-memory `analyses_store` dict is sufficient for hackathon
5. **Don't add authentication** — out of scope
6. **Don't use `google.generativeai` if `google-genai` API differs** — check the installed SDK
7. **Don't install new npm packages without checking** — keep bundle lean
8. **Don't add shadcn/ui** without first doing `npx shadcn@latest init`
9. **Don't `cd` into `backend/` to activate venv** — venv is at repo root
10. **Don't add `print()` inside loops** — will spam console during clause processing

---

## 📐 Risk Score Formula

```
Score = min(100, Σ(Wi × Si × Ci) / N × 100)

Where:
  Wi = CATEGORY_WEIGHTS[flag.risk_category]    # from enums.py (0.40 to 1.0)
  Si = SEVERITY_MULTIPLIERS[flag.severity]     # from enums.py (0.5 to 4.0)  
  Ci = flag.confidence                         # float 0.0 to 1.0
  N  = total_clauses_analyzed                  # normalization factor
```

Risk bands (from `enums.py`):
- 0–25 → `LOW` 🟢
- 26–50 → `MEDIUM` 🟡
- 51–75 → `HIGH` 🟠
- 76–100 → `CRITICAL` 🔴

---

## 📦 Key Dependencies

### Python (backend)
```
fastapi>=0.115.0          # Web framework
uvicorn[standard]>=0.30.0 # ASGI server
python-multipart>=0.0.12  # File upload support
PyMuPDF>=1.25.0           # PDF parsing (import as fitz)
pdfplumber>=0.11.0        # PDF fallback
python-docx>=1.1.0        # DOCX parsing
google-genai>=1.0.0       # Gemini LLM
pydantic>=2.10.0          # Data validation
pydantic-settings>=2.5.0  # Config from .env
python-dotenv>=1.0.0      # .env loader
aiofiles>=24.0.0          # Async file I/O
```

### JavaScript (frontend)
```
next: 16.3.8
react: 19.2.8
react-dom: 19.2.8
clsx: ^2.1.1             # Conditional classnames
tailwind-merge: ^3.7.0   # Tailwind class deduplication
tailwindcss: ^4          # CSS framework
typescript: ^5
```

---

## 🧪 Testing

No formal test framework set up. For hackathon:
1. Test backend: hit `http://localhost:8000/docs` (Swagger UI)
2. Test parsing: upload a sample PDF via Swagger
3. Test frontend: open `http://localhost:3000`
4. Sample contracts go in `data/sample_contracts/` (currently empty)

---

## 📄 Key Files Quick Reference

| File | Purpose |
|------|---------|
| `ACTIVE_CONTEXT.md` | Current build state + next steps |
| `artifacts/PRD-ContractShield-AI-1.0.md` | Full product requirements |
| `artifacts/build_plan.md` | Phase-by-phase build order |
| `backend/main.py` | All API routes |
| `backend/config.py` | All config (import `settings`) |
| `backend/models/schemas.py` | All Pydantic models |
| `backend/models/enums.py` | All enums + score constants |
| `backend/prompts/analysis.txt` | LLM prompt for risk analysis |
| `backend/prompts/segmentation.txt` | LLM prompt for clause segmentation |
| `backend/prompts/verification.txt` | LLM prompt for verification QA |
| `frontend/lib/types.ts` | All TypeScript types |
| `frontend/lib/api.ts` | All API functions |
| `frontend/lib/utils.ts` | Helper utilities |
| `frontend/app/globals.css` | Design tokens |
