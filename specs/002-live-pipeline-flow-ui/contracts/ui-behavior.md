# UI Behavior Contract: Live pipeline learning flow

**Feature**: `002-live-pipeline-flow-ui`  
**Date**: 2026-09-09  
**Audience**: Web (desktop + mobile browsers)  
**Visual contract**: [ui-design.md](./ui-design.md)  
**Data**: [../data-model.md](../data-model.md)  
**API**: [api.md](./api.md)  
**IA**: Single page at `/`

## Non-goals

- Concurrent side-by-side pipeline runs  
- Separate summarizer drop-down  
- Accounts / cross-session durable history  
- Invented scores or rationales  
- Production deploy / App Store  

## Surfaces (additive to 001)

| Surface | Depth |
|---------|--------|
| Stub/live honesty | Keep banners; must match provider mode |
| Agents | Transcription (≤5) + Judge with highlight affordance |
| Pipeline results | Transcript + summary + score |
| Rationale reveal | Hover on summary (pointer) + accessible “Why this score?” |
| Session history | Multi-run list; inspect past summaries/scores |
| View mode | Explicit Desktop / Mobile toggle |
| Demo reset | Clear runs/scores/uploads; keep preloads |
| Overall + graphs | Retain 001 behavior |

## Layout

| Mode | Contract |
|------|----------|
| Desktop | Primary pipeline information reads **left → right** |
| Mobile | Primary pipeline information stacks **vertically** |
| Toggle | Always available; overrides default derived from viewport; persist in sessionStorage |

## Interaction rules

1. Run remains sequential; disable start while a run is active.
2. After each completed/failed run, refresh history and dashboard.
3. Hover/reveal shows rationale when present; honest empty state otherwise.
4. Highlighted judges are visually distinct; non-highlighted remain selectable.
5. Clear demo data confirms intent (lightweight confirm OK); then empty overall + empty history; preloads remain.
6. Teaching messages for five concepts remain available.

## Accessibility

- Rationale MUST be reachable without hover-only (keyboard/focus or button).
- View mode toggle labeled and announced.
- Stub/live banners use `role="status"`.
