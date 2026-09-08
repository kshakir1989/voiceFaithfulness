# Tasks: LLM Judge Faithfulness Dashboard

**Input**: Design documents from `specs/001-llm-judge-dashboard/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included — constitution **VIII. TDD** + Gherkin/Playwright for UI and backend.

**Organization**: Greenfield under `apps/voiceFaithfulness`. Paths below are relative to `apps/voiceFaithfulness/` unless noted.

**Note**: Do **not** start implementation until the owner says **go implement** (or `/speckit-implement`). UI story tasks that touch styled SPA screens are **blocked** until `specs/001-llm-judge-dashboard/contracts/ui-design.md` has `Review: approved` and node URLs (Figma MCP rate-limited this session — file exists: https://www.figma.com/design/KzdHLMsPOiKVCTKhznVeHI).

**Git**: Work on branch `voiceFaithfulness/v1`; do not commit to `main`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no incomplete deps)
- **[Story]**: User story label (`US1`…`US7`)
- Exact file paths required on every task

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Scaffold backend, frontend, data dirs, and test runners

- [x] T001 Create backend package layout `backend/app/{main.py,api/,domain/,providers/,policy/,db/}` and `backend/tests/` per `specs/001-llm-judge-dashboard/plan.md`
- [x] T002 [P] Add `backend/requirements.txt` (or `pyproject.toml`) with FastAPI, uvicorn, httpx, pandas, pytest, pytest-asyncio, and note `faster-whisper`/torch as optional extra for local STT
- [x] T003 [P] Add `backend/.env.example` with `GROQ_API_KEY=` and document in `README.md`
- [x] T004 [P] Scaffold Vite + React + TypeScript app in `frontend/` with `package.json` scripts `dev`, `build`, `preview`
- [x] T005 [P] Create `data/preloaded/`, `data/uploads/`, and gitignore uploads in `.gitignore`
- [x] T006 [P] Add Playwright + Gherkin scaffolding (`playwright.config.ts`, `features/`, `features/steps/`) and `npm` script `test:e2e` from app root or `frontend/` as chosen in README
- [x] T007 Write root `README.md` with start commands matching `specs/001-llm-judge-dashboard/quickstart.md`

**Checkpoint**: Empty API boots; empty SPA loads; pytest/playwright commands exist

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared domain, DB, provider interfaces, agent catalogs — no full UI polish yet

**⚠️ CRITICAL**: Complete before user-story delivery. Prefer failing tests first (TDD).

- [x] T008 Define SQLite schema/models for Recording, PipelineRun, PipelineStage, artifacts, FaithfulnessScore in `backend/app/db/` aligned to `specs/001-llm-judge-dashboard/data-model.md`
- [x] T009 [P] Implement aggregate mean helper (completed scores only; null when empty) in `backend/app/domain/aggregate.py` with pytest in `backend/tests/test_aggregate.py`
- [x] T010 [P] Implement pipeline stage state machine helpers in `backend/app/domain/pipeline.py` with pytest in `backend/tests/test_pipeline.py`
- [x] T011 [P] Define provider protocols/adapters stubs (STT, summarize, judge) in `backend/app/providers/` per `specs/001-llm-judge-dashboard/research.md`
- [x] T012 [P] Implement agent catalogs (transcription + judge IDs/labels/defaults) in `backend/app/providers/catalog.py`
- [x] T013 [P] Implement all-ages policy gate stub in `backend/app/policy/all_ages.py` with pytest in `backend/tests/test_all_ages.py`
- [x] T014 Wire FastAPI app factory and health route in `backend/app/main.py`
- [x] T015 [P] Add teaching message static catalog JSON or module in `backend/app/domain/teaching.py`
- [x] T016 Seed `data/preloaded/manifest.json` listing ~10 all-ages ~3-minute recording placeholders (titles + paths; audio files may be stubbed until media task)
- [x] T017 Add mocked Groq HTTP fixtures for CI in `backend/tests/conftest.py`

**Checkpoint**: Domain tests green; catalogs return research.md IDs; DB migrates/creates

---

## Phase 2b: UI/UX Foundation (Figma gate)

**Purpose**: Visual contract before styled SPA implementation

- [x] T018 Complete Figma frames for spa-empty / spa-ready / spa-running / spa-complete / spa-error (desktop + mobile) in file `KzdHLMsPOiKVCTKhznVeHI` — **waived** 2026-09-08 (MCP rate limit); draw frames later when quota returns
- [x] T019 Record Figma file + node URLs and set `Review: approved` in `specs/001-llm-judge-dashboard/contracts/ui-design.md` — approved via owner waiver; node URLs remain TBD
- [x] T020 [P] Map design tokens from Figma into `frontend/src/theme.ts` (only after T019)

**Note:** T019 approved 2026-09-08 via owner waiver (Figma MCP rate-limited; node URLs still TBD). Styled UI may proceed using ui-design.md direction + ui-behavior. Prefer filling node URLs later.

---

## Phase 3: User Story 1 — Score a preloaded recording end-to-end (P1) 🎯 MVP core

**Goal**: Pick preloaded recording, select agents, run pipeline, see score + overall %

**Independent Test**: Select preloaded + both agents → run → stages complete → per-recording % and overall % update

### Tests

- [x] T021 [P] [US1] Add failing Gherkin scenarios for preloaded happy path in `features/pipeline.feature`
- [x] T022 [P] [US1] Add failing API/pytest contract tests for `POST /runs` and `GET /metrics/dashboard` in `backend/tests/test_api_runs.py` from `specs/001-llm-judge-dashboard/contracts/api.md`

### Implementation

- [x] T023 [US1] Implement `GET /recordings` listing preloaded items in `backend/app/api/recordings.py`
- [x] T024 [US1] Implement `GET /agents/transcription` and `GET /agents/judge` in `backend/app/api/agents.py`
- [x] T025 [US1] Implement async pipeline runner (ingest→transcript→summary→judge→aggregate) in `backend/app/domain/runner.py` using mocked providers in tests
- [x] T026 [US1] Implement `POST /runs`, `GET /runs/{id}`, `GET /runs` in `backend/app/api/runs.py` (single active run enforcement)
- [x] T027 [US1] Implement `GET /metrics/dashboard` in `backend/app/api/metrics.py`
- [x] T028 [US1] Implement Groq Whisper STT adapter for turbo/v3 IDs in `backend/app/providers/groq_stt.py`
- [x] T029 [US1] Implement fixed summarizer `groq-llama-3.1-8b-instant` in `backend/app/providers/groq_summarize.py`
- [x] T030 [US1] Implement Groq judge adapters for 70B/Scout/GPT-OSS IDs returning 0–100 in `backend/app/providers/groq_judge.py`
- [x] T031 [US1] Implement local Faster-Whisper adapter `local-faster-whisper` in `backend/app/providers/local_stt.py` (optional skip if torch missing, with clear unavailable flag)
- [x] T032 [US1] Generate or add first all-ages ~3-minute preloaded audio set under `data/preloaded/` and wire manifest (content review before commit)
- [x] T033 [US1] After T019: build minimal SPA wiring for picker, agent selects, run, stages, overall in `frontend/src/` per `contracts/ui-behavior.md` + approved Figma
- [x] T034 [US1] Bind Playwright e2e in `frontend/e2e/us1.spec.ts` (mirrors `features/*.feature`; playwright-bdd deferred due to version clash) + pytest

**Checkpoint**: US1 independent test green with mocks; live Groq optional smoke

---

## Phase 4: User Story 2 — Choose free-tier transcription agent (P1)

**Goal**: Drop-down drives transcript stage; recorded on run; limits surfaced

**Independent Test**: Change STT agent from default → run uses selected id; unavailable/limit messaging works

### Tests

- [ ] T035 [P] [US2] Add Gherkin for STT drop-down selection + recorded agent in `features/pipeline.feature`
- [ ] T036 [P] [US2] Add pytest asserting run stores `transcription_agent_id` and mock STT receives that id in `backend/tests/test_stt_selection.py`

### Implementation

- [ ] T037 [US2] Enforce required `transcription_agent_id` before start; map rate limits to `rate_limited` errors in `backend/app/api/runs.py` / providers
- [ ] T038 [US2] After T019: ensure STT `<select>` uses catalog + shows selected agent on completed row in `frontend/src/`
- [ ] T039 [US2] Pass US2 Gherkin + pytest

**Checkpoint**: US2 independent test green

---

## Phase 5: User Story 3 — Choose free-tier judge agent (P1)

**Goal**: Separate judge drop-down; slightly stronger catalog; recorded on run

**Independent Test**: Change judge → score stage uses selected id; limit messaging works

### Tests

- [ ] T040 [P] [US3] Add Gherkin for judge drop-down in `features/pipeline.feature`
- [ ] T041 [P] [US3] Add pytest for `judge_agent_id` wiring in `backend/tests/test_judge_selection.py`

### Implementation

- [ ] T042 [US3] Enforce required `judge_agent_id`; judge provider dispatch by catalog id in `backend/app/domain/runner.py`
- [ ] T043 [US3] After T019: judge `<select>` + display on score rows in `frontend/src/`
- [ ] T044 [US3] Pass US3 Gherkin + pytest

**Checkpoint**: US1–US3 form MVP pipeline with both agent pickers

---

## Phase 6: User Story 4 — Add a local recording (P1)

**Goal**: Local upload path; all-ages block; contributes to aggregate when accepted

**Independent Test**: Upload accepted audio → scoreable; blocked upload shows message and no score

### Tests

- [ ] T045 [P] [US4] Add Gherkin for upload accept/block in `features/pipeline.feature`
- [ ] T046 [P] [US4] Add pytest for `POST /recordings/upload` codes in `backend/tests/test_upload.py`

### Implementation

- [ ] T047 [US4] Implement multipart upload to `data/uploads/` + recording row in `backend/app/api/recordings.py`
- [ ] T048 [US4] Hook all-ages policy (reject → `all_ages_blocked`) in `backend/app/policy/all_ages.py`
- [ ] T049 [US4] After T019: upload control + error banner in `frontend/src/`
- [ ] T050 [US4] Pass US4 Gherkin + pytest

**Checkpoint**: Local + preloaded both feed dashboard

---

## Phase 7: User Story 5 — Teach-in-UI (P2)

**Goal**: Short messages for ingest/transcript/summary/judge/aggregate during use

**Independent Test**: One successful run shows teaching for all five concepts without covering primary metrics

### Tests

- [ ] T051 [P] [US5] Add Gherkin for teaching region visibility in `features/dashboard.feature`
- [ ] T052 [P] [US5] Add pytest for `GET /teaching/messages` in `backend/tests/test_teaching.py`

### Implementation

- [ ] T053 [US5] Implement `GET /teaching/messages` in `backend/app/api/teaching.py`
- [ ] T054 [US5] After T019: teaching region bound to stage events in `frontend/src/` per ui-behavior
- [ ] T055 [US5] Pass US5 Gherkin

**Checkpoint**: SC-005 covered

---

## Phase 8: User Story 6 — Dashboard metrics + graph views (P2)

**Goal**: Elegant score list + overall %; ≥2 selectable graph views consistent with numbers

**Independent Test**: ≥2 scores → list + overall mean; switch graphs; empty state when none

### Tests

- [ ] T056 [P] [US6] Add Gherkin for overall mean, empty state, graph selector in `features/dashboard.feature`
- [ ] T057 [P] [US6] Add pytest for dashboard payload `graph_views` + mean rounding in `backend/tests/test_metrics.py`

### Implementation

- [ ] T058 [US6] Ensure metrics endpoint returns graph view catalog + scores with agent ids in `backend/app/api/metrics.py`
- [ ] T059 [US6] After T019: add Recharts (or Chart.js) views `per_recording_bars` and `overall_aggregate` in `frontend/src/components/graphs/`
- [ ] T060 [US6] Mobile-width layout pass matching Figma in `frontend/src/`
- [ ] T061 [US6] Pass US6 Gherkin + pytest

**Checkpoint**: SC-002, SC-006, SC-009 covered

---

## Phase 9: User Story 7 — Graceful free-tier limits and failures (P3)

**Goal**: Explicit messages; no fabricated scores; single-run lock

**Independent Test**: Mock 429 → message + aggregate unchanged; second run blocked while running

### Tests

- [ ] T062 [P] [US7] Add Gherkin for rate limit and run-in-progress in `features/pipeline.feature`
- [ ] T063 [P] [US7] Add pytest for 429 mapping and 409 `run_in_progress` in `backend/tests/test_errors.py`

### Implementation

- [ ] T064 [US7] Map provider failures to API error codes in `backend/app/providers/` + `api/runs.py`
- [ ] T065 [US7] After T019: error banner states in `frontend/src/` per spa-error Figma
- [ ] T066 [US7] Pass US7 Gherkin + pytest

**Checkpoint**: SC-004 covered

---

## Phase 10: Polish & Cross-Cutting

- [ ] T067 [P] Align `spec-architecture.mmd` / `.html` with new backend/frontend/test artifacts and re-render `spec-architecture.png`
- [ ] T068 [P] Verify quickstart paths in `specs/001-llm-judge-dashboard/quickstart.md` against real scripts
- [ ] T069 Run full `pytest` + `npm run test:e2e` and fix regressions
- [ ] T070 Owner review: confirm all-ages preloaded content; no secrets committed

---

## Dependencies & Story Order

```text
Phase 1 Setup → Phase 2 Foundational → Phase 2b Figma (T018–T019)
     ↓
US1 (needs agents APIs) → US2 → US3  } P1 MVP pipeline
     ↓
US4 local upload
     ↓
US5 teaching → US6 graphs/dashboard polish → US7 errors
     ↓
Polish
```

- **UI styled work** (T033, T038, T043, T049, T054, T059–T060, T065) depends on **T019**
- Backend-only tasks can proceed while Figma is unfinished

## Parallel Opportunities

- Within Phase 1: T002–T006
- Within Phase 2: T009–T013, T015
- Per story: Gherkin + pytest pairs marked [P] before implementation
- US5 teaching API vs US6 metrics graphs after US1–US4 backend solid

## MVP Scope (suggested)

1. Complete Phase 1–2  
2. T018–T019 Figma approval (or defer UI and ship API+pytest MVP)  
3. US1 + US2 + US3 (T021–T044) as first demoable slice  
4. Then US4 → US5 → US6 → US7  

## Task Count Summary

| Area | Tasks |
|------|-------|
| Phase 1 Setup | T001–T007 (7) |
| Phase 2 Foundational | T008–T017 (10) |
| Phase 2b Figma | T018–T020 (3) |
| US1 | T021–T034 (14) |
| US2 | T035–T039 (5) |
| US3 | T040–T044 (5) |
| US4 | T045–T050 (6) |
| US5 | T051–T055 (5) |
| US6 | T056–T061 (6) |
| US7 | T062–T066 (5) |
| Polish | T067–T070 (4) |
| **Total** | **70** |
