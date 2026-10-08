# 🛡️ ContractShield AI — Active Context
>
> **Last Updated:** 2026-10-08 · **Switching to:** Laptop 2  
> **Team:** AlgoVibes (4 members) · **Event:** CodeFiesta 24-Hour Hackathon @ GIT Jaipur

--

## 🎯 Project Summary

**ContractShield AI** — An AI-powered contract risk analysis platform.  
Tagline: **"Know What You're Signing"**

Users upload PDFs or DOCX contracts → AI segments clauses → flags legal risks with severity, explanations, and safer alternatives → displays an interactive risk dashboard.

**Hackathon Track:** #1 — Legal NDA & Contract Risk Flagging Agent (Agentic AI + GenAI)

---

## 🗂️ Repository Structure

```
AlgoVibes/                          ← Git repo root
├── ACTIVE_CONTEXT.md               ← This file
├── AGENTS.md                       ← Agent coding instructions
├── README.md                       ← Project overview & quick start
├── .env                            ← Root env (HAS real GOOGLE_API_KEY)
├── .gitignore                      ← Ignores: venv/, node_modules/, .env, .next/, *.db
│
├── backend/                        ← FastAPI (Python) app
│   ├── main.py                     ← Entry point + all API routes (COMPLETE)
│   ├── config.py                   ← Pydantic-settings config (COMPLETE)
│   ├── requirements.txt            ← Python deps (COMPLETE)
│   ├── .env                        ← Backend env (GOOGLE_API_KEY = placeholder "your_gemini_api_key_here")
│   ├── agents/
│   │   ├── __init__.py             ← Package init
│   │   ├── orchestrator.py         ← STUB — raises NotImplementedError
│   │   ├── planner.py              ← STUB — raises NotImplementedError
│   │   ├── analyzer.py             ← STUB — raises NotImplementedError
│   │   └── verifier.py             ← STUB — raises NotImplementedError
│   ├── tools/
│   │   ├── __init__.py             ← Exports all tools
│   │   ├── document_parser.py      ← STUB — raises NotImplementedError
│   │   ├── clause_segmenter.py     ← STUB — raises NotImplementedError
│   │   ├── risk_matcher.py         ← STUB — raises NotImplementedError
│   │   └── score_calculator.py     ← STUB — raises NotImplementedError
│   ├── models/
│   │   ├── __init__.py             ← Full re-exports (COMPLETE)
│   │   ├── schemas.py              ← All Pydantic models (COMPLETE)
│   │   └── enums.py                ← All enums + constants (COMPLETE)
│   ├── prompts/
│   │   ├── analysis.txt            ← LLM prompt template for risk analysis (COMPLETE)
│   │   ├── segmentation.txt        ← LLM prompt template for clause segmentation (COMPLETE)
│   │   └── verification.txt        ← LLM prompt template for verification QA (COMPLETE)
│   └── knowledge/
│       ├── clause_library.json     ← EMPTY SHELL — to be populated in Phase 3
│       ├── risk_patterns.json      ← EMPTY SHELL — to be populated in Phase 3
│       └── jurisdiction_rules.json ← EMPTY SHELL — to be populated in Phase 3
│
├── frontend/                       ← Next.js 16 app
│   ├── package.json                ← deps: next@16.3.8, react@19, tailwind@4 (COMPLETE)
│   ├── .env.local                  ← NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
│   ├── app/
│   │   ├── layout.tsx              ← Root layout, Inter + JetBrains Mono fonts (COMPLETE)
│   │   ├── globals.css             ← Design tokens, CSS vars, dark theme (COMPLETE)
│   │   ├── page.tsx                ← SCAFFOLD — Static landing card, Phase 1 status
│   │   ├── analyze/[id]/page.tsx   ← STUB — "Coming in Phase 6" placeholder
│   │   └── clause-library/page.tsx ← STUB — "Coming in Phase 7" placeholder
│   ├── components/ui/              ← EMPTY — no UI components built yet
│   └── lib/
│       ├── types.ts                ← Full TypeScript types (mirrors backend, COMPLETE)
│       ├── api.ts                  ← Full API client with all 5 functions (COMPLETE)
│       └── utils.ts                ← Helper utils: cn, formatFileSize, formatDuration, etc. (COMPLETE)
│
├── data/
│   └── sample_contracts/           ← EMPTY — no test contracts yet
├── docs/                           ← EMPTY
└── artifacts/
    ├── PRD-ContractShield-AI-1.0.md ← Full product requirements document
    ├── build_plan.md                ← Phased build plan (Phases 1–7)
    ├── contractshield-vibe-prompt.md← Vibe coding prompt
    └── Updates.txt                  ← Brief notes log
```

---

## ✅ What Is COMPLETED (Phase 1 — Done)

### Backend

| Item | File | Status |
| ------ | ------ | -------- |
| FastAPI app with CORS | `backend/main.py` | ✅ Working |
| All 5 API routes wired | `main.py` | ✅ Wired (stubs return 501) |
| Pydantic config (pydantic-settings) | `backend/config.py` | ✅ Working |
| All Pydantic schemas | `backend/models/schemas.py` | ✅ Complete |
| All enums + score constants | `backend/models/enums.py` | ✅ Complete |
| In-memory analyses store | `main.py` line 67 | ✅ Ready |
| 3 LLM prompt templates | `backend/prompts/` | ✅ Complete |
| Requirements file | `backend/requirements.txt` | ✅ Complete |
| venv created | `venv/` at root | ✅ Exists |

### Frontend

| Item | File | Status |
| ------ | ------ | -------- |
| Next.js 16 + Tailwind v4 + TypeScript | `frontend/` | ✅ Working |
| Root layout with Google Fonts | `frontend/app/layout.tsx` | ✅ Complete |
| Design system CSS tokens | `frontend/app/globals.css` | ✅ Complete |
| Full TypeScript types (mirrors backend) | `frontend/lib/types.ts` | ✅ Complete |
| Full API client (5 functions) | `frontend/lib/api.ts` | ✅ Complete |
| Utility functions | `frontend/lib/utils.ts` | ✅ Complete |
| node_modules installed | `frontend/node_modules/` | ✅ Present |
| Route stubs (analyze, clause-lib) | `frontend/app/*/page.tsx` | ✅ Navigable |

### Git

| Commit | Message |
| -------- | --------- |
| `9f7d059` | added prompt 1 ← **HEAD** |
| `7d4aeda` | added .env.example |
| `8c574b7` | added build plan in github ← origin/main |
| `d2e4e67` | deleted .env.example and made .env |
| `277c67b` | Phase 1- First commit |
| `3698adb` | Initial commit |

> **Note:** Local is 2 commits ahead of `origin/main`. Push before switching machines!

---

## ⚠️ CRITICAL: Environment Variables

### Root `.env` (NOT committed — gitignored)

```
GOOGLE_API_KEY=AQ.Ab8RN6IZsBkjGYCZCZKRN1AnOHhOg1gFC6oOdx5rZHJyNHRjvA
LLM_MODEL=gemini-1.5-flash
VERIFICATION_MODEL=gemini-1.5-pro
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
MAX_FILE_SIZE_MB=10
MAX_PAGES=50
DEBUG=true
DATABASE_URL=sqlite:///./contractshield.db
```

### `backend/.env` (NOT committed — gitignored)

```
GOOGLE_API_KEY=your_gemini_api_key_here   ← ⚠️ STILL A PLACEHOLDER! Copy key from root .env
LLM_MODEL=gemini-1.5-flash
VERIFICATION_MODEL=gemini-1.5-pro
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
MAX_FILE_SIZE_MB=10
MAX_PAGES=50
DEBUG=true
DATABASE_URL=sqlite:///./contractshield.db
```

### `frontend/.env.local` (NOT committed — gitignored)

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 🔴 What Is PENDING (Phases 2–7)

### Phase 2 — Document Parsing & Clause Segmentation
>
> **Files to implement:** `backend/tools/document_parser.py`, `backend/tools/clause_segmenter.py`

- [ ] `parse_document()` in `document_parser.py` — PDF via PyMuPDF/pdfplumber, DOCX via python-docx
- [ ] `segment_clauses()` in `clause_segmenter.py` — Regex-based + LLM fallback via Gemini
- [ ] Returns `ParsedDocument` and `list[Clause]` objects (schemas already defined)

### Phase 3 — Risk Detection & Scoring Engine
>
> **Files to implement:** `backend/tools/risk_matcher.py`, `backend/tools/score_calculator.py`, `backend/knowledge/*.json`

- [ ] Populate `knowledge/risk_patterns.json` with 50+ regex patterns across 9 risk categories
- [ ] Populate `knowledge/jurisdiction_rules.json` for India, US-CA, US-DE, US-NY, UK, EU
- [ ] Populate `knowledge/clause_library.json` with risky vs safe examples
- [ ] `match_risks()` in `risk_matcher.py` — dual-layer: regex + Gemini LLM contextual analysis
- [ ] `calculate_risk_score()` in `score_calculator.py` — formula: `min(100, Σ(Wi × Si × Ci) / N × 100)`

### Phase 4 — Agentic Pipeline (Plan → Act → Verify → Report)
>
> **Files to implement:** all 4 agents

- [ ] `create_analysis_plan()` in `agents/planner.py`
- [ ] `run_risk_analysis()` in `agents/analyzer.py`
- [ ] `verify_risk_flags()` in `agents/verifier.py`
- [ ] `run_analysis()` in `agents/orchestrator.py` — MAIN loop: wires Phases 2+3+4 together
- [ ] When complete, `POST /api/v1/analyze` returns full `AnalysisResponse` (currently 501)

### Phase 5 — Frontend Upload Page UI
>
> **File:** `frontend/app/page.tsx` (replace scaffold), new components in `frontend/components/`

- [ ] Hero section + drag-and-drop file upload zone
- [ ] Metadata form: contract type dropdown, parties input, jurisdiction selector, user role toggle
- [ ] Animated progress tracker (Plan → Parse → Analyze → Verify → Report)
- [ ] `FileUpload` component
- [ ] `MetadataForm` component
- [ ] `ProgressTracker` component
- [ ] File validation: PDF/DOCX only, 10MB max

### Phase 6 — Frontend Risk Report Dashboard
>
> **File:** `frontend/app/analyze/[id]/page.tsx` (replace stub), new components

- [ ] Animated risk score gauge (0–100 with color bands)
- [ ] Risk summary header (band, breakdown by severity)
- [ ] `RiskFlagCard` — expandable cards with severity badge, problematic text, explanation, suggestion
- [ ] `SafeClauseCard` — green-styled safe clause cards
- [ ] Full dashboard layout assembling all components
- [ ] Fetch analysis by ID from `GET /api/v1/analysis/{id}`

### Phase 7 — Polish, Integration & Demo Prep

- [ ] Sample test contracts in `data/sample_contracts/` (Good NDA ~15 score, Risky NDA ~68, Terrible SA ~89)
- [ ] Error handling: file too large, empty PDF, API timeouts
- [ ] UI polish: micro-animations, hover effects, loading states
- [ ] Clause Library page at `/clause-library` (stretch)
- [ ] PDF export (stretch)
- [ ] Deploy: Vercel (frontend) + Railway/Render (backend)
- [ ] End-to-end integration test

---

## 🚀 How to Run on Laptop 2

### Prerequisites

```bash
# 1. Clone or pull latest
git clone <repo-url> AlgoVibes  # OR git pull

# 2. Create backend .env (NOT in git — copy manually or recreate)
cp AlgoVibes/.env AlgoVibes/backend/.env
# IMPORTANT: The root .env has the real API key. backend/.env still has placeholder.

# 3. Backend setup
cd AlgoVibes
python3 -m venv venv                   # Create virtualenv (venv/ is gitignored)
source venv/bin/activate               # Activate
pip install -r backend/requirements.txt  # Install deps

# 4. Frontend setup
cd frontend
npm install                            # Recreate node_modules (gitignored)

# 5. Create frontend .env.local (NOT in git)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
```

### Run Backend

```bash
cd /path/to/AlgoVibes
source venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000
# → Health check: http://localhost:8000/api/v1/health
# → API docs:     http://localhost:8000/docs
```

### Run Frontend

```bash
cd /path/to/AlgoVibes/frontend
npm run dev
# → http://localhost:3000
```

---

## 🏗️ Tech Stack

| Layer | Technology | Version |
| ------- | ----------- | --------- |
| Frontend framework | Next.js | 16.3.8 |
| Frontend language | TypeScript | ^5 |
| CSS | Tailwind CSS | ^4 |
| Backend framework | FastAPI | >=0.115.0 |
| Backend language | Python | 3.11+ |
| LLM — primary | Google Gemini 1.5 Flash | via `google-genai>=1.0.0` |
| LLM — verification | Google Gemini 1.5 Pro | via `google-genai>=1.0.0` |
| PDF parsing | PyMuPDF + pdfplumber | >=1.25.0 / >=0.11.0 |
| DOCX parsing | python-docx | >=1.1.0 |
| Data validation | Pydantic v2 | >=2.10.0 |
| Config | pydantic-settings | >=2.5.0 |

---

## 📡 API Endpoints (Current State)

| Method | Route | Status | Notes |
| -------- | ------- | -------- | ------- |
| GET | `/api/v1/health` | ✅ **Working** | Returns 200 + version |
| POST | `/api/v1/analyze` | ⚠️ **501 Not Implemented** | Route wired, pipeline is stubs |
| GET | `/api/v1/analysis/{id}` | ⚠️ **Works if ID exists** | In-memory only, no persistence |
| GET | `/api/v1/clause-library` | ⚠️ **Placeholder** | Returns empty array |
| POST | `/api/v1/chat` | ⚠️ **Placeholder** | Returns canned answer |

---

## 🔑 Key Design Decisions

| Decision | Choice | Reason |
| ---------- | -------- | -------- |
| LLM | Gemini 1.5 Flash (analysis) + 1.5 Pro (verify) | Free tier, fast, Google API |
| Agent Framework | Custom Python orchestrator (no LangChain/LangGraph) | Simpler, faster to build |
| Embeddings/Vector DB | **Skip for MVP** — pure regex + LLM | Faster to implement |
| Frontend | Next.js 16 App Router | Better demo than Streamlit |
| Persistence | In-memory dict `analyses_store` | Sufficient for hackathon demo |
| Document Parsing | PyMuPDF (primary) + python-docx | Both already in requirements |

---

## 🎨 Design System

- **Background:** `#0a0a0a` (near-black)
- **Card background:** `#1a1a2e` (dark navy)
- **Accent:** `#6c63ff` (purple)
- **Critical:** `#e94560` (red-pink)
- **High:** `#f59e0b` (amber)
- **Medium:** `#eab308` (yellow)
- **Safe/Low:** `#22c55e` (green)
- **Info:** `#6366f1` (indigo)
- **Fonts:** Inter (UI) + JetBrains Mono (code)
- **Style:** Glassmorphism cards, dark theme, micro-animations

---

## 📌 Exact Next Steps (Pick Up From Here)

**The immediately next task is Phase 2 — implement backend document parsing.**

### Step 1 — Fix the API key in `backend/.env`

```bash
# The backend/.env still has "your_gemini_api_key_here"
# Copy the real key from root .env into backend/.env
```

### Step 2 — Implement `backend/tools/document_parser.py`

Replace the `raise NotImplementedError` with:

- PDF: use `fitz` (PyMuPDF) to extract text page by page
- DOCX: use `python_docx` to iterate paragraphs
- Return `ParsedDocument(raw_text, pages, word_count, filename)`

### Step 3 — Implement `backend/tools/clause_segmenter.py`

- Regex path: split on numbered sections (`1.`, `2.`, `Section 1.`, `ARTICLE I.`)
- LLM path: call Gemini with `prompts/segmentation.txt` template
- Hybrid: try regex first, fall back to LLM if < 3 clauses found
- Return `list[Clause]`

### Step 4 — Populate `backend/knowledge/risk_patterns.json`

50+ regex patterns organized by `RiskCategory` enum values

### Step 5 — Implement `backend/tools/risk_matcher.py`

- Layer 1: match each clause text against risk_patterns.json regexes
- Layer 2: for matched/uncertain clauses, call Gemini with `prompts/analysis.txt`
- Return `list[RiskFlag]`

### Step 6 — Implement `backend/tools/score_calculator.py`

```
Score = min(100, Σ(Wi × Si × Ci) / N × 100)
Wi = CATEGORY_WEIGHTS[flag.risk_category]  # from enums.py
Si = SEVERITY_MULTIPLIERS[flag.severity]   # from enums.py
Ci = flag.confidence
N  = total_clauses
```

### Step 7 — Wire up agents (Phase 4)

1. `planner.py` → detect contract type, pick strategy
2. `analyzer.py` → call parser → segmenter → risk_matcher → score_calculator
3. `verifier.py` → call Gemini with `prompts/verification.txt`
4. `orchestrator.py` → call planner → analyzer → verifier → assemble `AnalysisResponse`

### Step 8 — Frontend Upload Page (Phase 5)

Replace `frontend/app/page.tsx` with real upload UI

---

## ⚡ Important Notes for Laptop 2

1. **`.env` files are NOT in git** — you must recreate them manually (values above)
2. **`venv/` is NOT in git** — run `python3 -m venv venv && pip install -r backend/requirements.txt`
3. **`node_modules/` is NOT in git** — run `npm install` in `frontend/`
4. **`frontend/components/ui/` is EMPTY** — no shadcn components installed yet
5. **`data/sample_contracts/` is EMPTY** — no test PDFs yet
6. **Local HEAD is 2 commits ahead of origin** — push or pull accordingly
7. **The `backend/.env` GOOGLE_API_KEY is still a placeholder** — use key from root `.env`
8. **`POST /api/v1/analyze` returns 501** — this is expected until Phase 4 is done
9. The venv is at **repo root** (`AlgoVibes/venv/`), not inside `backend/`
10. Use `google-genai` (not `google.generativeai`) — that's what's in requirements.txt
