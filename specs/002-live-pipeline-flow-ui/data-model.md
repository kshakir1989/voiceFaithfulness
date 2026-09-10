# Data Model: Live Pipeline Learning Flow

**Feature**: `002-live-pipeline-flow-ui`  
**Date**: 2026-09-09  
**Extends**: `001-llm-judge-dashboard` data model

## Entities (deltas)

### TranscriptionAgent (catalog)

| Field | Type | Rules |
|-------|------|-------|
| id | string | Stable catalog ID (see research.md §2) |
| label | string | Drop-down label |
| kind | `transcription` | Fixed |
| provider | string | `groq` \| `local` \| `deepgram` \| `assemblyai` |
| available | boolean | False if key missing / known disabled |
| owns_summary | boolean | Always true for this feature |
| summary_backend | string \| null | Internal summarizer id/provider; not a third drop-down |

### JudgeAgent (catalog)

| Field | Type | Rules |
|-------|------|-------|
| id | string | Stable catalog ID |
| label | string | Drop-down label |
| kind | `judge` | Fixed |
| provider | string | e.g. `groq` |
| available | boolean | |
| power_tier | integer | Higher = more powerful; used for highlight |
| highlight | boolean | Derived or stored; UI emphasis when true |

### PipelineRun

| Field | Type | Rules |
|-------|------|-------|
| id | string (UUID) | Required |
| recording_id | string | FK |
| transcription_agent_id | string | Required; owns transcript + summary |
| judge_agent_id | string | Required |
| summarizer_id | string \| null | **Deprecated for product-fixed use**; may mirror transcription agent summary backend for audit |
| status | enum | `pending` \| `running` \| `completed` \| `failed` |
| error_message / error_code | string \| null | Honest failures |
| created_at / updated_at | datetime | Required |

### Transcript Artifact

| Field | Type | Rules |
|-------|------|-------|
| run_id | string | 1:1 |
| text | string | Non-empty on success |
| agent_id | string | MUST equal `transcription_agent_id` |

### Summary Artifact

| Field | Type | Rules |
|-------|------|-------|
| run_id | string | 1:1 |
| text | string | Non-empty on success |
| agent_id | string | MUST equal `transcription_agent_id` (owns summary) |

### FaithfulnessScore

| Field | Type | Rules |
|-------|------|-------|
| run_id | string | 1:1 |
| recording_id | string | Denormalized |
| value | number | 0–100 |
| judge_agent_id | string | Match run |
| rationale | string \| null | **Required to surface in UI when present** |

### SessionHistory

Logical view: ordered list of `PipelineRun` snapshots for the current demo session (in-memory primary). Cleared by demo reset.

### ViewMode (client)

| Field | Type | Rules |
|-------|------|-------|
| mode | enum | `desktop` \| `mobile` |
| persistence | session | `sessionStorage` for the browser tab |

### DemoSessionReset

Action (not a stored entity): clears runs, scores, ephemeral uploads; retains preloaded recordings.

## Validation rules

1. Pipeline order unchanged: ingest → transcript → summary → judge → aggregate.
2. Summary failure (empty) → fail run before judge; no score row.
3. Only completed scores enter overall mean.
4. Reset must not delete preloaded audio or manifest entries.
5. Unavailable agents cannot start a run.

## State transitions

Unchanged from 001 for stages; add UI states: `history_visible`, `rationale_revealed`, `view_mode`, `demo_cleared`.
