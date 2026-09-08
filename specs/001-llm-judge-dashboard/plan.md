# Implementation Plan: LLM Judge Faithfulness Dashboard

**Branch**: `voiceFaithfulness/v1` | **Date**: 2026-09-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-llm-judge-dashboard/spec.md`

**Note**: Design-only. No application code until the owner runs `/speckit-tasks` → `/speckit-implement` (and Figma approval for UI).

## Summary

Build a single-page learning demo under `apps/voiceFaithfulness` that runs an ordered LLM-as-judge pipeline: ingest audio → transcript (learner-selected free-tier STT) → summary (fixed free-tier summarizer) → faithfulness 0–100 (learner-selected slightly stronger free-tier judge) → update per-recording and overall mean scores on an elegant dashboard with teaching messages, selectable graph views, Gherkin+Playwright acceptance tests for UI and backend, and graceful free-tier limit handling.

## Technical Context

**Language/Version**: Python 3.12 (backend/pipeline); TypeScript 5.x (SPA frontend)

**Primary Dependencies**: FastAPI + Uvicorn; pandas; PyTorch + `faster-whisper` (local STT option); `httpx` for Groq API; Vite + React for SPA; chart library TBD in tasks (minimal: e.g. Chart.js or Recharts); Playwright + Gherkin (`playwright-bdd` or equivalent); pytest for backend unit/API tests

**Storage**: Local SQLite (pipeline runs, scores, agent selections) + on-disk audio under `data/preloaded/` and `data/uploads/`; no hosted DB

**Testing**: Gherkin features for UI + API/pipeline; Playwright against local SPA+API; pytest for domain/aggregate and provider adapters (mocked HTTP)

**Target Platform**: Local web (desktop + mobile viewports); deploy later only if owner unlocks free hosting

**Project Type**: Monorepo app — Python API + SPA under `apps/voiceFaithfulness`

**Performance Goals**: One ~3-minute recording completes end-to-end within a single guided session on free-tier limits; SPA remains usable on mobile-width viewport

**Constraints**: Free-tier first (Groq free + local Whisper); all-ages content; no accounts; Figma-first UI; Teach-Along; branch `voiceFaithfulness/v1` until deploy then PR to `main`

**Scale/Scope**: ~10 preloaded 3-minute recordings; one SPA; two agent drop-downs; two+ graph views; single active pipeline run

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| I. Ask First | PASS | Owner said **go plan**; no implement |
| II. Spec First | PASS | Spec + checklist green |
| III. One App | PASS | Only `apps/voiceFaithfulness` |
| IV. Teach-Along | PASS | Pause before next non-trivial step |
| V. Faithfulness Pipeline | PASS | Ordered stages locked in research/data-model |
| VI. All-Ages | PASS | Preloaded + upload policy in contracts |
| VII. Free-Tier First | PASS | Groq free + local Whisper; graceful limits |
| VIII. TDD / Gherkin+Playwright | PASS | Planned in structure + quickstart |
| IX. Figma First | PASS | `ui-design.md` scaffolded; no UI code until approved |
| X. Teach-in-UI | PASS | Teaching messages in ui-behavior |
| XI. Elegant UI | PASS | Minimal SPA + few graph views |
| XII. Git Branches | PASS | Track `voiceFaithfulness/v1` |

**Post-design re-check**: PASS — contracts add API + UI behavior only; no paid vendors; providers are free-tier/local.

## Project Structure

### Documentation (this feature)

```text
specs/001-llm-judge-dashboard/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── api.md
│   ├── ui-behavior.md
│   └── ui-design.md          # scaffold; Review pending
└── tasks.md                  # later: /speckit-tasks
```

### Source Code (planned)

```text
apps/voiceFaithfulness/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── api/                    # routes: recordings, agents, runs, metrics
│   │   ├── domain/                 # aggregate mean, pipeline state machine
│   │   ├── providers/              # STT / summarize / judge adapters
│   │   ├── policy/                 # all-ages gate
│   │   └── db/                     # SQLite models/repos
│   ├── tests/                      # pytest
│   ├── pyproject.toml / requirements.txt
│   └── .env.example                # GROQ_API_KEY
├── frontend/
│   ├── src/                        # Vite React SPA
│   ├── package.json
│   └── ...
├── data/
│   ├── preloaded/                  # ~10 all-ages audio + metadata JSON
│   └── uploads/                    # local uploads (gitignored)
├── features/                       # Gherkin
│   ├── dashboard.feature
│   ├── pipeline.feature
│   └── steps/
├── playwright.config.ts
└── README.md
```

**Structure Decision**: Split API and SPA for clear Playwright targeting and Python pipeline ownership. Rejected monolith Jinja-only UI — charts, drop-downs, and teach-in-UI need a maintainable SPA while staying one page.

## Complexity Tracking

> No constitution violations requiring justification.
