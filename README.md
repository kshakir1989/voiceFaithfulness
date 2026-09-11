# voiceFaithfulness

Single-page learning demo: audio → transcript (chosen free-tier STT) → summary → LLM-as-judge faithfulness score → dashboard aggregate.

**UI:** Vite + React + Tailwind + shadcn (teal / cool mist tokens). Pipeline uses a stepper; overall score uses a circular gauge.

**Specs:** `specs/001-llm-judge-dashboard/` · `specs/002-live-pipeline-flow-ui/`

Paths below are from **this repo root** (`voiceFaithfulness/`). If you are in the freshusa-apps index, that root is `apps/voiceFaithfulness/`.

## Prerequisites

- Python 3.9+ (3.12+ preferred)
- Node 20+
- Optional keys in `backend/.env` (copy from `.env.example`): `GROQ_API_KEY`, `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY`
- Without keys (or for a quick demo), use `FORCE_MOCK_PROVIDERS=1` for stub STT / summary / judge

## Run locally

You need **two processes**:

| Process | Port | Role |
|---------|------|------|
| FastAPI (`uvicorn`) | **8000** | API only — `/` is a hint page, not the app |
| Vite (`npm run dev`) | **5173** | SPA — **open this URL** |

Vite proxies `/api` → `http://127.0.0.1:8000`.

### 1. One-time setup

```bash
# From voiceFaithfulness repo root

# Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # optional: add GROQ_API_KEY=

# Frontend
cd ../frontend
npm install
```

If `source .venv/bin/activate` fails with “no such file”, the venv was never created — re-run `python3 -m venv .venv` in `backend/`.

If `uvicorn: command not found`, the venv is not active (or packages were not installed). Activate it, then `pip install -r requirements.txt`.

### 2. Start the API (terminal A)

```bash
cd backend
source .venv/bin/activate
export FORCE_MOCK_PROVIDERS=1      # recommended until you have a Groq key
uvicorn app.main:app --reload --port 8000
```

Health check: http://127.0.0.1:8000/api/health → `{"status":"ok"}`

### 3. Start the SPA (terminal B)

```bash
cd frontend
npm run dev
```

### 4. Open the app

**http://127.0.0.1:5173/**

Do **not** use port 8000 as the app URL.

### First-run checklist

1. Confirm **Stub mode** / **Live mode** alert; ~10 preloaded recordings (+ blocked demo).
2. Confirm up to **5** transcription agents; stronger judges marked with ★.
3. Preview audio; **Run pipeline** → pipeline **stepper**, transcript + summary (owned by STT agent).
4. Overall card shows a **circular % gauge** when scores exist; open **Why this score?** for rationale.
5. Use Desktop / Mobile layout toggle; run again and compare in **Session history**.
6. **Clear demo data** resets runs / scores / uploads; preloads remain.

## Tests

```bash
cd backend && source .venv/bin/activate && FORCE_MOCK_PROVIDERS=1 pytest
cd frontend && npm run test:e2e
```

Gherkin in `features/*.feature` is living documentation. Executable UI coverage is Playwright in `frontend/e2e/`. Without `GROQ_API_KEY` (or with `FORCE_MOCK_PROVIDERS=1`), providers use mocks — the SPA shows **Stub mode** and marks dashboard percentages as stubbed.

**Uploads:** stored only for the browser session (`vf_session` cookie) under `data/uploads/sessions/` and cleared on tab close / `DELETE /api/recordings/session`. Preloaded demos (including the labeled **[Blocked demo]** failure sample) always remain in the picker.

## Preloaded audio

Titles + paths: `data/preloaded/manifest.json`. All-ages spoken demos (~3 minutes each) are generated with macOS TTS via:

```bash
# From voiceFaithfulness repo root
python3 scripts/generate-preloaded-audio.py
```

The picker also includes a labeled **[Blocked demo]** item that always fails the all-ages gate. Uploads remain session-only.
