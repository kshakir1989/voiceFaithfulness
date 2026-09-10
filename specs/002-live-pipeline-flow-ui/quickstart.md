# Quickstart: Live pipeline learning flow (post-implement)

**Feature**: `002-live-pipeline-flow-ui`  
**Date**: 2026-09-09  
**Contracts**: [api.md](./contracts/api.md), [ui-behavior.md](./contracts/ui-behavior.md)  
**Data**: [data-model.md](./data-model.md)  
**App README**: [../../README.md](../../README.md)

## Prerequisites

- Python 3.9+ / 3.12+, Node 20+
- Backend venv + deps; frontend `npm install`
- Live demo: `GROQ_API_KEY` (and optionally `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY`) in `backend/.env`
- Stub demo: `FORCE_MOCK_PROVIDERS=1`
- Branch: `voiceFaithfulness/v1.1`

## Start

```bash
# Terminal A — API
cd apps/voiceFaithfulness/backend
source .venv/bin/activate
# Live:
# unset FORCE_MOCK_PROVIDERS
# Stub:
export FORCE_MOCK_PROVIDERS=1
uvicorn app.main:app --reload --port 8000

# Terminal B — SPA
cd apps/voiceFaithfulness/frontend
npm run dev
```

Open **http://127.0.0.1:5173/**

## Manual happy path (002)

1. Confirm stub vs live banner matches env.
2. Open transcription catalog — up to five agents; unavailable ones disabled.
3. Preview audio; pick STT + judge (note highlighted stronger judges); run pipeline.
4. See transcript + summary attributed to the transcription agent; score value.
5. Hover / open “Why this score?” on summary → rationale (or honest empty).
6. Change agents; run again; open session history and compare summaries/scores.
7. Toggle Desktop vs Mobile view — LTR vs vertical; controls remain usable.
8. Clear demo data — history/scores/uploads gone; preloads remain; overall empty.
9. Optional: run with Deepgram/AssemblyAI when keys present.

## Acceptance tests

```bash
cd apps/voiceFaithfulness/backend && source .venv/bin/activate && FORCE_MOCK_PROVIDERS=1 pytest
cd apps/voiceFaithfulness/frontend && npm run test:e2e
```

## Plan validation (this phase)

Owner reviews `plan.md` + `research.md` (STT roster) + contracts. After **approve**, complete Figma/`ui-design.md` gate, then `/speckit-tasks`.
