# UI Behavior Contract: Faithfulness dashboard SPA

**Feature**: `001-llm-judge-dashboard`  
**Date**: 2026-09-08  
**Audience**: Web (desktop + mobile browsers)  
**Visual contract**: [ui-design.md](./ui-design.md)  
**Data**: [../data-model.md](../data-model.md)  
**API**: [api.md](./api.md)  
**IA**: Single page at `/` (no multi-route product navigation)

## Non-goals (v1)

- User accounts, ads, analytics, paid APIs  
- Summarizer drop-down  
- Multi-page router  
- Invented scores or silent failures  
- Cluttered multi-widget dashboard  

## Surfaces

| Surface | Depth |
|---------|--------|
| Web SPA | Full: picker, agent drop-downs, run controls, stage status, teaching messages, score list, overall %, graph selector |

## Layout regions (logical)

| Region | Contract |
|--------|----------|
| Brand / title | Product name visible as primary identity (Elegant UI / portfolio-quality) |
| Ingest | Preloaded picker + local upload control |
| Agents | Transcription drop-down + Judge drop-down (required before Run) |
| Run | Start control; disabled while another run is active or agents missing |
| Pipeline status | Per-stage pending/running/completed/failed |
| Teaching | Short messages for ingest → transcript → summary → judge → aggregate |
| Scores | List of completed scores with agent IDs visible |
| Overall | Overall % or “No scores yet” |
| Graphs | Selector for ≥2 views; charts consistent with numbers |

## Flows

### Select preloaded + agents + run (P1)

| Step | Contract |
|------|----------|
| Picker | Shows ~10 all-ages preloaded titles |
| Agents | Both drop-downs populated from API; defaults selectable/changeable |
| Run | Starts only with recording + both agents |
| Progress | Stages update live (poll or push) |
| Done | Per-recording % and overall % update; agents shown for the run |

### Choose agents (P1)

| Element | Contract |
|---------|----------|
| Transcription list | Free-tier labels only; unavailable options explained |
| Judge list | Free-tier stronger-tier labels; same failure UX |
| Limit | Clear message; allow switching agent |

### Local upload (P1)

| Result | Contract |
|--------|----------|
| Accept | Appears in selectable list |
| Policy block | Clear message; no score |
| Bad file | Clear message; pipeline not started |

### Teaching (P2)

| Trigger | Contract |
|---------|----------|
| Stage start/complete | Matching concept message visible without covering primary metrics |
| Overall | Explains mean-of-completed-scores idea |

### Graphs (P2)

| Element | Contract |
|---------|----------|
| Selector | At least `per_recording_bars` and `overall_aggregate` |
| Consistency | Chart values match listed scores / overall |
| Empty | Neutral empty state |

### Errors (P3)

| Case | Contract |
|------|----------|
| Rate limit / provider | Explicit message; no fake score added |
| Run in progress | Block or message; single active run |

## Accessibility / responsive

- Critical controls usable at mobile width without horizontal scroll of primary actions  
- Drop-downs and Run reachable without hover-only affordances  

## Test hooks (for Gherkin)

Stable `data-testid` (or role+name) for: recording picker, transcription select, judge select, run button, stage list, overall metric, score list, graph selector, teaching region, error banner.
