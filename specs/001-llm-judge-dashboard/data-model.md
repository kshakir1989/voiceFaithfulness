# Data Model: LLM Judge Faithfulness Dashboard

**Feature**: `001-llm-judge-dashboard`  
**Date**: 2026-09-08

## Entities

### Recording

| Field | Type | Rules |
|-------|------|-------|
| id | string (UUID) | Required, stable |
| title | string | Required, learner-visible |
| source_type | enum: `preloaded` \| `local` | Required |
| audio_path | string | Required; relative path under `data/` |
| duration_seconds | number | Optional; ~180 for preloaded |
| all_ages_eligible | boolean | Required; must be true to score |
| created_at | datetime | Required |

**Notes**: Preloaded rows seeded from metadata JSON. Local uploads create a row after file accept.

### TranscriptionAgent / JudgeAgent (catalog, not user-authored)

| Field | Type | Rules |
|-------|------|-------|
| id | string | Stable catalog ID (see research.md) |
| label | string | Drop-down label |
| kind | enum: `transcription` \| `judge` | Required |
| provider | string | e.g. `groq`, `local` |
| available | boolean | False when known disabled/limit |

### PipelineRun

| Field | Type | Rules |
|-------|------|-------|
| id | string (UUID) | Required |
| recording_id | string | FK → Recording |
| transcription_agent_id | string | Required before start |
| judge_agent_id | string | Required before start |
| summarizer_id | string | Fixed product config |
| status | enum: `pending` \| `running` \| `completed` \| `failed` | Required |
| error_message | string \| null | Set on failure / limit |
| created_at / updated_at | datetime | Required |

### PipelineStage

| Field | Type | Rules |
|-------|------|-------|
| run_id | string | FK → PipelineRun |
| name | enum: `ingest` \| `transcript` \| `summary` \| `judge` \| `aggregate` | Required |
| status | enum: `pending` \| `running` \| `completed` \| `failed` | Required |
| started_at / finished_at | datetime \| null | Optional |
| detail | string \| null | Optional teaching/debug snippet |

### Transcript Artifact

| Field | Type | Rules |
|-------|------|-------|
| run_id | string | FK, 1:1 |
| text | string | Non-empty on success |
| agent_id | string | Must match run.transcription_agent_id |

### Summary Artifact

| Field | Type | Rules |
|-------|------|-------|
| run_id | string | FK, 1:1 |
| text | string | Non-empty on success |
| summarizer_id | string | Product-configured |

### FaithfulnessScore

| Field | Type | Rules |
|-------|------|-------|
| run_id | string | FK, 1:1 |
| recording_id | string | Denormalized for dashboard |
| value | number | 0–100 inclusive |
| judge_agent_id | string | Must match run.judge_agent_id |
| rationale | string \| null | Optional; not required on UI |

### DashboardAggregate

Computed, not stored as source of truth:

- `overall_percentage` = mean(`FaithfulnessScore.value` for completed runs) or null if none
- `completed_count` = N

### TeachingMessage

| Field | Type | Rules |
|-------|------|-------|
| id | string | Stable |
| concept | enum: ingest, transcript, summary, judge, aggregate | Required |
| body | string | Short plain language |

Static catalog served to SPA; may be stage-triggered.

### DashboardGraphView

| Field | Type | Rules |
|-------|------|-------|
| id | enum: `per_recording_bars` \| `overall_aggregate` | Required |
| label | string | Selector label |

## Relationships

```text
Recording 1─* PipelineRun
PipelineRun 1─* PipelineStage
PipelineRun 1─0..1 Transcript, Summary, FaithfulnessScore
FaithfulnessScore *─→ DashboardAggregate (computed)
```

## State transitions (PipelineRun)

```text
pending → running → completed
                 ↘ failed
```

- Only one `running` run globally in v1.
- Score contributes to aggregate **only** on `completed` with FaithfulnessScore present.
- Partial stages never update aggregate.

## Validation rules

- Cannot start run without recording + transcription_agent_id + judge_agent_id.
- Cannot score if `all_ages_eligible` is false.
- Reject empty/corrupt/unsupported audio before `running`.
- Empty summary → fail before judge.
- Faithfulness value outside 0–100 → fail (do not clamp silently into fake success without recording error).
