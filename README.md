# voiceFaithfulness

Single-page learning demo: audio → transcript (chosen free-tier STT) → summary → LLM-as-judge faithfulness score → dashboard aggregate.

**Branch:** `voiceFaithfulness/v1`  
**Spec:** `specs/001-llm-judge-dashboard/`

## Prerequisites

- Python 3.12+
- Node 20+
- Optional: `GROQ_API_KEY` (see `backend/.env.example`)

## Backend

```bash
cd apps/voiceFaithfulness/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health: `GET http://127.0.0.1:8000/api/health`

## Frontend

```bash
cd apps/voiceFaithfulness/frontend
npm install
npm run dev
```

SPA: http://127.0.0.1:5173 (proxies `/api` → backend)

**UI note:** Figma contract approved (MCP waiver); polish frames/node URLs when quota returns.

## Tests

```bash
cd apps/voiceFaithfulness/backend && source .venv/bin/activate && FORCE_MOCK_PROVIDERS=1 pytest
cd apps/voiceFaithfulness/frontend && npm run test:e2e
```

Gherkin in `features/*.feature` is living documentation. Executable UI coverage is Playwright in `frontend/e2e/`. Without `GROQ_API_KEY` (or with `FORCE_MOCK_PROVIDERS=1`), providers use mocks.

## Preloaded audio

Titles + paths: `data/preloaded/manifest.json`. Short silent `.wav` placeholders are committed for pipeline tests; replace with real ~3-minute all-ages clips before demos.