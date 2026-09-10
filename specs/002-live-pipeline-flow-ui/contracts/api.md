# API Contract: Live pipeline learning flow (deltas on 001)

**Feature**: `002-live-pipeline-flow-ui`  
**Date**: 2026-09-09  
**Base URL**: `http://localhost:8000/api` (dev)  
**Supersedes / extends**: `001-llm-judge-dashboard/contracts/api.md`

All responses JSON. Errors: `{ "detail": { "code": string, "message": string } }` (FastAPI style) or equivalent documented error object.

## Agents

### `GET /agents/transcription`

```json
{
  "agents": [
    {
      "id": "groq-whisper-large-v3-turbo",
      "label": "Groq Whisper Large v3 Turbo",
      "available": true,
      "owns_summary": true,
      "provider": "groq"
    }
  ],
  "default_id": "groq-whisper-large-v3-turbo"
}
```

Catalog MUST include up to five free-tier agents per research.md (Groq×2, local Faster-Whisper, Deepgram Nova-3, AssemblyAI Universal). Unavailable agents set `available: false`.

### `GET /agents/judge`

```json
{
  "agents": [
    {
      "id": "groq-llama-3.3-70b-versatile",
      "label": "Groq Llama 3.3 70B",
      "available": true,
      "power_tier": 3,
      "highlight": true,
      "provider": "groq"
    }
  ],
  "default_id": "groq-llama-3.3-70b-versatile"
}
```

`highlight: true` when the agent is a more powerful model (see research power_tier rules). Selection of non-highlighted judges remains allowed.

## Runs

### `POST /runs`

Body unchanged:

```json
{
  "recording_id": "…",
  "transcription_agent_id": "…",
  "judge_agent_id": "…"
}
```

On completed:

```json
{
  "id": "…",
  "recording_id": "…",
  "transcription_agent_id": "…",
  "judge_agent_id": "…",
  "status": "completed",
  "stages": [{ "name": "transcript", "status": "completed" }],
  "transcript": "…",
  "summary": "…",
  "score": {
    "value": 88,
    "judge_agent_id": "…",
    "rationale": "SCORE=88 …"
  }
}
```

`score.rationale` MAY be null; MUST NOT be invented. Summary text is owned by `transcription_agent_id`.

### `GET /runs`

Newest-first history for session/demo store:

```json
{
  "runs": [
    {
      "id": "…",
      "recording_id": "…",
      "transcription_agent_id": "…",
      "judge_agent_id": "…",
      "status": "completed",
      "transcript": "…",
      "summary": "…",
      "score": { "value": 88, "judge_agent_id": "…", "rationale": "…" },
      "created_at": "…"
    }
  ]
}
```

### `GET /runs/{id}`

Same run shape as POST response.

## Demo reset

### `DELETE /demo/session`

Clears session runs, scores, and ephemeral uploads. Preloaded recordings remain.

```json
{ "ok": true, "cleared": ["runs", "scores", "uploads"] }
```

May be implemented as an extension of `DELETE /recordings/session` plus run/score clear — document the chosen single entry point in implement tasks; SPA calls one clear action.

## Metrics

### `GET /metrics/dashboard`

Unchanged meaning; `scores` rows SHOULD include `run_id`. Continue `providers_mode` and `scores_are_stubbed` honesty fields from 001.

## Health

### `GET /health`

Include `providers_mode`: `stub` \| `live`.
