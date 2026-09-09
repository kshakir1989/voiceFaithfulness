# voiceFaithfulness

Single-page learning demo: audio → transcript (chosen free-tier STT) → summary → LLM-as-judge faithfulness score → dashboard aggregate.

**Branch:** `voiceFaithfulness/v1`  
**Spec:** `specs/001-llm-judge-dashboard/`

## Prerequisites

- Python 3.9+ (3.12+ preferred)
- Node 20+
- Optional: `GROQ_API_KEY` in `backend/.env` (copy from `backend/.env.example`). Without a key, set `FORCE_MOCK_PROVIDERS=1` for mock STT/summary/judge.

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

1. Confirm ~10 preloaded recordings in the picker.
2. Use **Preview** to listen before running.
3. Leave or change STT + judge agents; click **Run pipeline**.
4. Confirm stages complete, then **Transcript**, **Summary**, score, and overall %.

**UI note:** Figma contract approved (MCP waiver); polish frames/node URLs when quota returns.

## Tests

```bash
cd apps/voiceFaithfulness/backend && source .venv/bin/activate && FORCE_MOCK_PROVIDERS=1 pytest
cd apps/voiceFaithfulness/frontend && npm run test:e2e
```

Gherkin in `features/*.feature` is living documentation. Executable UI coverage is Playwright in `frontend/e2e/`. Without `GROQ_API_KEY` (or with `FORCE_MOCK_PROVIDERS=1`), providers use mocks — the SPA shows **Stub mode** and marks dashboard percentages as stubbed.

**Uploads:** stored only for the browser session (`vf_session` cookie) under `data/uploads/sessions/` and cleared on tab close / `DELETE /api/recordings/session`. Preloaded demos (including the labeled **[Blocked demo]** failure sample) always remain in the picker.

## Preloaded audio

Titles + paths: `data/preloaded/manifest.json`. Short silent `.wav` placeholders are committed for pipeline tests; replace with real ~3-minute all-ages clips before demos.
