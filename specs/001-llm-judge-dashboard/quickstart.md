# Quickstart: Validate faithfulness dashboard (post-implement)

**Feature**: `001-llm-judge-dashboard`  
**Date**: 2026-09-09  
**Contracts**: [api.md](./contracts/api.md), [ui-behavior.md](./contracts/ui-behavior.md)  
**Data**: [data-model.md](./data-model.md)  
**App README**: [../../README.md](../../README.md) (authoritative local start)

## Prerequisites

- Python 3.9+ (3.12+ preferred), Node 20+
- Backend venv + `pip install -r requirements.txt`; frontend `npm install` (see app README)
- Optional: `GROQ_API_KEY` in `backend/.env`; otherwise `FORCE_MOCK_PROVIDERS=1` (stub scores)
- Branch: `voiceFaithfulness/v1` (not `main`)

## Start

```bash
# Terminal A — API
cd apps/voiceFaithfulness/backend
source .venv/bin/activate
export FORCE_MOCK_PROVIDERS=1
uvicorn app.main:app --reload --port 8000

# Terminal B — SPA
cd apps/voiceFaithfulness/frontend
npm run dev
```

Open **http://127.0.0.1:5173/** (not `:8000`). Health: `GET http://127.0.0.1:8000/api/health`.

## Manual happy path

1. Confirm stub-mode banner; ~10 all-ages preloads + labeled **[Blocked demo]** item.
2. Preview audio; select STT + judge; run pipeline.
3. Confirm stages, transcript + summary panels, score, overall %, teaching concepts log.
4. Switch graph views; values match the numeric list.
5. Optional: upload a local file (session-only); try blocked demo → clear error, no score.

## Acceptance tests

```bash
cd apps/voiceFaithfulness/backend
source .venv/bin/activate
FORCE_MOCK_PROVIDERS=1 pytest

cd ../frontend
npm run test:e2e
```

Or from app root: `npm run test:e2e` (delegates to frontend).

## Limit / failure check

- Stub 429 (or Playwright route) → rate-limit banner; overall % unchanged.
- Run-in-progress → `run_in_progress` banner.
- Blocked demo / all-ages → 403 message; no fabricated score.

## Do not

- Commit secrets (`.env` with real keys).
- Commit onto `main`; push `voiceFaithfulness/v1` and merge via PR after ship/review.
