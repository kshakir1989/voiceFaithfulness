# Quickstart: Validate faithfulness dashboard (post-implement)

**Feature**: `001-llm-judge-dashboard`  
**Date**: 2026-09-08  
**Contracts**: [api.md](./contracts/api.md), [ui-behavior.md](./contracts/ui-behavior.md)  
**Data**: [data-model.md](./data-model.md)

## Prerequisites

- Python 3.12+, Node 20+
- From `apps/voiceFaithfulness`: backend deps + frontend deps installed (see app README once created)
- Optional: `GROQ_API_KEY` for live Groq STT/summary/judge; without it, use mocked provider tests + `local-faster-whisper` where enabled
- Branch: work on `voiceFaithfulness/v1` (not `main`)

## Start (expected after implement)

```bash
cd apps/voiceFaithfulness/backend && uvicorn app.main:app --reload --port 8000
cd apps/voiceFaithfulness/frontend && npm run dev
```

Open the SPA URL printed by Vite (proxied to API).

## Manual happy path

1. Confirm ~10 preloaded recordings in the picker.
2. Select transcription agent (default Groq Whisper Turbo OK) and judge agent (default Llama 3.3 70B OK).
3. Run pipeline; watch stages transcript → summary → judge.
4. Confirm per-recording % and overall %; confirm both agent IDs visible for the run.
5. Switch graph views; values match the numeric list.
6. Confirm teaching messages appear for the five concepts.

## Acceptance tests

```bash
cd apps/voiceFaithfulness
# Backend unit/API (mocked providers)
pytest
# UI + API Gherkin/Playwright
npm run test:e2e
```

Expected: P1 scenarios in `features/*.feature` pass (picker, both agent drop-downs, run, scores, aggregate mean).

## Limit / failure check

- Force mock 429 → UI shows rate-limit message; overall % unchanged.
- Start second run while first running → blocked with clear message.

## Do not

- Implement UI before `contracts/ui-design.md` is `Review: approved` with Figma node URLs.
- Commit onto `main`; merge via PR after deploy/ship.
