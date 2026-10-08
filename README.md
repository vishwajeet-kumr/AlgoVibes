# 🛡️ ContractShield AI

> **"Know What You're Signing"**

AI-powered contract risk analysis platform that helps startups, freelancers, and non-lawyers identify hidden legal risks in NDAs and contracts.

**Team:** AlgoVibes (4 members) · **Hackathon:** CodeFiesta — 24-Hour Hackathon @ GIT Jaipur

## 🏗️ Architecture

```
frontend/    → Next.js 14 + Tailwind CSS + TypeScript
backend/     → FastAPI (Python) + Gemini AI
```

### Agentic Pipeline: **PLAN → ACT → VERIFY → REPORT**

1. **INPUT** — Upload PDF/DOCX with metadata
2. **PLAN** — AI determines analysis strategy
3. **ACT** — Clause segmentation → Risk pattern matching → Scoring
4. **VERIFY** — Ground flags to source text, validate severity
5. **REPORT** — Interactive risk dashboard

---

## 🚀 Quick Start

### Backend

```bash
cd backend
source ../venv/bin/activate
cp .env.example .env  # Add your GOOGLE_API_KEY
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

- **Frontend:** <http://localhost:3000>
- **API Docs:** <http://localhost:8000/docs>
- **Health Check:** <http://localhost:8000/api/v1/health>

--

## 📁 Project Structure

```
AlgoVibes/
├── frontend/                   # Next.js 14 app
│   ├── app/
│   │   ├── page.tsx           # Landing / Upload page
│   │   ├── analyze/[id]/      # Risk report dashboard
│   │   └── clause-library/    # Clause library browser
│   ├── components/            # React components
│   ├── lib/
│   │   ├── types.ts           # TypeScript types (mirrors backend)
│   │   ├── api.ts             # API client
│   │   └── utils.ts           # Utility functions
│   └── .env.local             # Frontend env vars
│
├── backend/                    # FastAPI app
│   ├── main.py                # Entry point + API routes
│   ├── config.py              # Centralized configuration
│   ├── agents/                # Agentic pipeline
│   │   ├── orchestrator.py    # Main loop controller
│   │   ├── planner.py         # PLAN phase
│   │   ├── analyzer.py        # ACT phase
│   │   └── verifier.py        # VERIFY phase
│   ├── tools/                 # Deterministic tools
│   │   ├── document_parser.py # PDF/DOCX extraction
│   │   ├── clause_segmenter.py# Clause boundary detection
│   │   ├── risk_matcher.py    # Risk pattern matching
│   │   └── score_calculator.py# Risk score computation
│   ├── models/                # Data models
│   │   ├── schemas.py         # Pydantic request/response models
│   │   └── enums.py           # Domain enumerations
│   ├── knowledge/             # Knowledge base
│   │   ├── risk_patterns.json # 50+ regex risk patterns
│   │   ├── clause_library.json# Risky vs safe examples
│   │   └── jurisdiction_rules.json
│   ├── prompts/               # LLM prompt templates
│   └── requirements.txt       # Python dependencies
│
├── data/sample_contracts/     # Test contracts for demo
├── artifacts/                 # PRD and project docs
└── .env.example               # Environment template
```

---

## 🛠️ Tech Stack

| Layer | Technology |
| ------- | ----------- |
| Frontend | Next.js 14, Tailwind CSS, TypeScript |
| Backend | FastAPI, Python 3.11+ |
| LLM | Google Gemini 1.5 Flash / Pro |
| Document Parsing | PyMuPDF, python-docx |
| Data Models | Pydantic v2 |

---

## 📊 Build Phases

- [x] **Phase 1** — Foundation & Scaffolding
- [ ] **Phase 2** — Document Parsing & Clause Segmentation
- [ ] **Phase 3** — Risk Detection & Scoring Engine
- [ ] **Phase 4** — Agentic Pipeline (Plan→Act→Verify→Report)
- [ ] **Phase 5** — Upload Page UI
- [ ] **Phase 6** — Risk Report Dashboard UI
- [ ] **Phase 7** — Polish, Integration & Demo Prep
