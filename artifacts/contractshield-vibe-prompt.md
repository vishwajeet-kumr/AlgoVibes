# ContractShield AI — AI IDE Vibe Coding Prompt

---

## WHO YOU ARE

You are my vibe coding partner on this project. You write complete, working code on the first try. No placeholders. No TODOs. No "add your logic here." Every file you touch is 100% done when you hand it back.

---

## FIRST THING — READ THE CODEBASE

Before writing a single line of code, do the following:

1. Read the entire project folder structure so you understand what exists
2. Read `artifacts/build_plan.md` — this is the phase-by-phase build plan for the entire project. Follow it exactly.
3. Read `artifacts/PRD-ContractShield-AI-1.0.md` — this is the full product spec. All scoring formulas, risk patterns, UI wireframes, and API design are in there.
4. Read `backend/models/schemas.py` and `backend/models/enums.py` — these are the source of truth for all data shapes. Do not change them.
5. Read `frontend/lib/types.ts` — this mirrors the backend schemas for the frontend. Do not change it.

Only after reading all of the above should you start writing any code.

---

## PROJECT OVERVIEW

**Product:** ContractShield AI — "Know What You're Signing"
**What it does:** Users upload an NDA or contract (PDF/DOCX). The AI analyzes it, flags risky clauses, scores overall risk from 0–100, and shows a detailed risk report dashboard.
**Stack:** Next.js 16 + Tailwind CSS v4 + TypeScript (frontend) · FastAPI + Python 3.11 (backend) · Google Gemini 1.5 Flash (LLM)
**Deployment:** Vercel (frontend) + Railway (backend)
**Team:** 4-person team, 24-hour hackathon at GIT Jaipur

---

## GEMINI API KEY

Use this key for all Gemini API calls in the backend:

```
GOOGLE_API_KEY=[PASTE YOUR KEY HERE]
```

Set this as an environment variable in:
- A `.env` file inside the `backend/` folder for local development
- Railway environment variables for production deployment
- Never hardcode it in any Python file

---

## WHAT IS CURRENTLY BROKEN (FIX THESE FIRST)

**Problem reported:** When deployed live, the webpage shows only the project folder names instead of the actual UI.

### Bug 1 — Vercel root directory misconfiguration (CRITICAL)

The repo root contains `frontend/`, `backend/`, and `artifacts/` folders with no `package.json` at the root level. Vercel cannot detect the Next.js framework from the root, so it falls back to showing a directory listing instead of the app.

**Fix:** Create a `vercel.json` file at the repo root (not inside frontend/, at the very top level) that tells Vercel where the Next.js app lives and how to build it.

Also tell the user: Go to Vercel project settings → General → Root Directory and set it to `frontend`. This is the permanent fix. The `vercel.json` is the code-level backup.

### Bug 2 — TypeScript crash in `frontend/app/layout.tsx` (CRITICAL)

The current `layout.tsx` uses a type called `LayoutProps<"/">` for the children prop. This type does not exist anywhere in Next.js. It is never imported. This causes `next build` to fail with a TypeScript error, which means Vercel's build crashes before any page is served.

**Fix:** Replace the broken children prop type with the correct Next.js pattern. The children should be typed as `React.ReactNode`. No other changes to layout.tsx are needed.

---

## WHAT PHASE WE ARE IN

Phase 1 (scaffolding) is complete. Both apps run. The folder structure, schemas, types, config, and route stubs are all in place.

**You are now building Phases 2 through 7 in order.** The `artifacts/build_plan.md` file defines exactly what each phase requires. Read it and follow it.

Quick summary of what's a stub right now (everything that says `raise NotImplementedError` must be fully implemented):

- `backend/tools/document_parser.py` — stub
- `backend/tools/clause_segmenter.py` — stub
- `backend/tools/risk_matcher.py` — stub
- `backend/tools/score_calculator.py` — stub
- `backend/agents/orchestrator.py` — stub
- `backend/agents/planner.py` — stub
- `backend/agents/analyzer.py` — stub
- `backend/agents/verifier.py` — stub
- `backend/knowledge/risk_patterns.json` — empty shell
- `backend/knowledge/jurisdiction_rules.json` — empty shell
- `backend/knowledge/clause_library.json` — empty shell
- `frontend/app/page.tsx` — shows a status card only, needs the full upload UI
- `frontend/app/analyze/[id]/page.tsx` — stub, needs the full risk report dashboard
- `frontend/components/` — this entire folder does not exist yet, all components need to be created

---

## HOW TO BUILD — VIBE CODING RULES

- Build one complete unit at a time. Finish it fully before moving to the next.
- Every file you deliver must be the complete file — first line to last line. Never give me a partial file or say "rest stays the same."
- State your assumptions in one line before building. Then build. Do not ask five clarifying questions.
- If something in the PRD is unclear, make the sensible decision and note it in one line.
- The backend must still work even if the Gemini API key is missing or quota runs out — use regex-only risk detection as a fallback in that case. Never crash the app because the LLM is unavailable.

---

## KEY TECHNICAL CONSTRAINTS — DO NOT BREAK THESE

- Do NOT modify these files — they are complete and correct: `backend/main.py`, `backend/config.py`, `backend/models/schemas.py`, `backend/models/enums.py`, `frontend/lib/types.ts`, `frontend/lib/api.ts`, `frontend/lib/utils.ts`
- This project uses **Tailwind CSS v4** — the syntax is `@import "tailwindcss"` in the CSS file. Do NOT create a `tailwind.config.ts`. That file is not needed in v4 and will break things.
- This is **Next.js 16 + React 19** — there are breaking changes from older versions. Read the `frontend/AGENTS.md` file before writing any Next.js code. It tells you exactly this.
- There is **no shadcn/ui installed**. The `package.json` does not have it. Build all components using plain Tailwind CSS with the design tokens already defined in `frontend/app/globals.css`.
- Backend imports must be resolved from inside the `backend/` folder. Use module paths like `from models.schemas import ...` and `from tools.document_parser import ...`. The `sys.path` injection in `main.py` already handles this.

---

## DESIGN SYSTEM (ALREADY CONFIGURED IN globals.css — USE THESE VALUES)

Do not invent colors. Use only these:

- Background: `#0a0a0a`
- Card background: `#1a1a2e`
- Card hover: `#222240`
- Border: `rgba(255,255,255,0.08)`
- Accent (primary): `#6c63ff`
- Critical risk: `#e94560`
- High risk: `#f59e0b`
- Medium risk: `#eab308`
- Safe / Low risk: `#22c55e`
- Info: `#6366f1`
- Text primary: `#ededed`
- Text muted: `#71717a`
- Fonts: Inter (body), JetBrains Mono (code/monospace)

---

## DEPLOYMENT CHECKLIST (VERCEL + RAILWAY)

When everything is built, here is what needs to happen for deployment:

**Frontend → Vercel:**
- Root directory in Vercel settings: `frontend`
- `vercel.json` at repo root (fix #1 above)
- Environment variable to set in Vercel: `NEXT_PUBLIC_API_URL` = the Railway backend URL (e.g. `https://contractshield-backend.up.railway.app/api/v1`)

**Backend → Railway:**
- Point Railway to the `backend/` folder
- Environment variable to set: `GOOGLE_API_KEY` = the Gemini key above
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- After deploying, update the `FRONTEND_URL` setting in Railway env to match the Vercel frontend URL (for CORS)

---

## PRIORITY ORDER IF TIME IS SHORT

If you cannot build everything, do it in this order. Do not skip ahead.

1. Fix layout.tsx bug and add vercel.json — nothing works deployed without this
2. document_parser.py and clause_segmenter.py — without parsing, no analysis runs
3. risk_patterns.json (populated with real patterns from the PRD) and risk_matcher.py and score_calculator.py — this is the core product value
4. orchestrator.py + planner.py + analyzer.py + verifier.py — wires the full pipeline together
5. Upload page UI (page.tsx) with all components — users need to be able to submit a contract
6. Risk report dashboard (analyze/[id]/page.tsx) with all components — this is the demo showstopper
7. Sample contracts for demo (a low-risk NDA and a high-risk NDA — judges will use these)
8. Clause library page and any remaining polish

---

## START HERE

Read the codebase. Read `artifacts/build_plan.md`. Read `artifacts/PRD-ContractShield-AI-1.0.md`.

Fix Bug 1 and Bug 2 first.

Then follow the build plan phase by phase.

Let's ship this.
