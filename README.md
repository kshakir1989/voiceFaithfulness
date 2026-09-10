# voiceFaithfulness

Single-page learning demo: audio → transcript (chosen free-tier STT) → summary → LLM-as-judge faithfulness score → dashboard aggregate.

**Branch:** `voiceFaithfulness/v1.1`  
**Specs:** `specs/001-llm-judge-dashboard/` · `specs/002-live-pipeline-flow-ui/`

## Prerequisites

- Python 3.9+ (3.12+ preferred)
- Node 20+
- Optional keys in `backend/.env` (from `.env.example`): `GROQ_API_KEY`, `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY`. Without keys, set `FORCE_MOCK_PROVIDERS=1` for stub STT/summary/judge.

## Run locally

You need **two processes**. The UI is the Vite app on **5173**; the API on **8000** has no SPA at `/` (opening `http://127.0.0.1:8000/` shows a hint, not the dashboard).

### 1. One-time setup

```bash
# Backend
cd apps/voiceFaithfulness/backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # optional: add GROQ_API_KEY=

# Frontend
cd ../frontend
npm install
```

### 2. Start the API (terminal A)

```bash
cd apps/voiceFaithfulness/backend
source .venv/bin/activate
# Optional mocks (recommended until you have a Groq key):
export FORCE_MOCK_PROVIDERS=1
uvicorn app.main:app --reload --port 8000
```

Check: http://127.0.0.1:8000/api/health → `{"status":"ok"}`

### 3. Start the SPA (terminal B)

```bash
cd apps/voiceFaithfulness/frontend
npm run dev
```

### 4. Open the app

**http://127.0.0.1:5173/**

Vite proxies `/api` → `http://127.0.0.1:8000`. Do **not** use port 8000 as the app URL.

### First-run checklist

1. Confirm stub/live banner; ~10 preloaded recordings (+ blocked demo).
2. Confirm up to **5** transcription agents; stronger judges marked with ★.
3. Preview audio; run pipeline → transcript + summary (owned by STT agent).
4. Open **Why this score?** for rationale; use Desktop/Mobile layout toggle.
5. Run again with another agent; compare in **Session history**.
6. **Clear demo data** resets runs/scores/uploads; preloads remain.

## Tests

```bash
cd apps/voiceFaithfulness/backend && source .venv/bin/activate && FORCE_MOCK_PROVIDERS=1 pytest
cd apps/voiceFaithfulness/frontend && npm run test:e2e
```

Gherkin in `features/*.feature` is living documentation. Executable UI coverage is Playwright in `frontend/e2e/`. Without `GROQ_API_KEY` (or with `FORCE_MOCK_PROVIDERS=1`), providers use mocks — the SPA shows **Stub mode** and marks dashboard percentages as stubbed.

**Uploads:** stored only for the browser session (`vf_session` cookie) under `data/uploads/sessions/` and cleared on tab close / `DELETE /api/recordings/session`. Preloaded demos (including the labeled **[Blocked demo]** failure sample) always remain in the picker.

## Preloaded audio

Titles + paths: `data/preloaded/manifest.json`. All-ages spoken demos (~3 minutes each) are generated with macOS TTS via:

```bash
cd apps/voiceFaithfulness
python3 scripts/generate-preloaded-audio.py
```

The picker also includes a labeled **[Blocked demo]** item that always fails the all-ages gate. Uploads remain session-only.
