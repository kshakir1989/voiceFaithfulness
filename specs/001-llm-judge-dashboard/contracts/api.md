# API Contract: Faithfulness pipeline & dashboard

**Feature**: `001-llm-judge-dashboard`  
**Date**: 2026-09-08  
**Base URL**: `http://localhost:<port>/api` (dev)

All responses JSON. Errors: `{ "error": { "code": string, "message": string } }` with appropriate HTTP status.

## Agents

### `GET /agents/transcription`

Returns free-tier transcription catalog for the drop-down.

```json
{
  "agents": [
    { "id": "groq-whisper-large-v3-turbo", "label": "Groq Whisper Large v3 Turbo", "available": true }
  ],
  "default_id": "groq-whisper-large-v3-turbo"
}
```

### `GET /agents/judge`

Same shape for judge catalog; `default_id`: `groq-llama-3.3-70b-versatile`.

## Recordings

### `GET /recordings`

Lists preloaded + accepted local recordings.

```json
{
  "recordings": [
    {
      "id": "…",
      "title": "…",
      "source_type": "preloaded",
      "duration_seconds": 180,
      "all_ages_eligible": true,
      "audio_url": "/api/recordings/{id}/audio"
    }
  ]
}
```

### `GET /recordings/{id}/audio`

Streams (or serves) the recording audio for in-page preview.  
**200**: audio bytes with appropriate `Content-Type` (`audio/wav`, `audio/mpeg`, etc.).  
**404**: unknown id.

### `POST /recordings/upload`

Multipart audio upload.  
**201**: recording object.  
**400**: unsupported/corrupt/empty.  
**403**: all-ages policy block (`code`: `all_ages_blocked`).

## Pipeline runs

### `POST /runs`

Body:

```json
{
  "recording_id": "…",
  "transcription_agent_id": "…",
  "judge_agent_id": "…"
}
```

**201**: run object with stages all `pending` then server starts async work → `running`.  
**409**: another run already `running` (`code`: `run_in_progress`).  
**400**: missing agents / ineligible recording.

### `GET /runs/{id}`

```json
{
  "id": "…",
  "recording_id": "…",
  "transcription_agent_id": "…",
  "judge_agent_id": "…",
  "status": "running",
  "error_message": null,
  "stages": [
    { "name": "transcript", "status": "running" }
  ],
  "transcript": null,
  "summary": null,
  "score": null
}
```

On completed: `transcript`, `summary` text; `score: { "value": 0-100, "judge_agent_id": "…" }`.

### `GET /runs`

Optional history list (newest first) for dashboard rows.

## Metrics

### `GET /metrics/dashboard`

```json
{
  "overall_percentage": 87.5,
  "completed_count": 4,
  "scores": [
    {
      "recording_id": "…",
      "title": "…",
      "value": 90,
      "transcription_agent_id": "…",
      "judge_agent_id": "…",
      "run_id": "…"
    }
  ],
  "graph_views": [
    { "id": "per_recording_bars", "label": "Per-recording scores" },
    { "id": "overall_aggregate", "label": "Overall aggregate" }
  ]
}
```

`overall_percentage` is `null` when `completed_count` is 0.

## Teaching

### `GET /teaching/messages`

```json
{
  "messages": [
    { "id": "teach-transcript", "concept": "transcript", "body": "…" }
  ]
}
```

## Limit / provider errors

When Groq returns rate limit or local STT fails: fail active stage + run with `error.code` in `{ "rate_limited", "provider_error", "invalid_audio", "all_ages_blocked", "empty_summary" }` and human `message`.
