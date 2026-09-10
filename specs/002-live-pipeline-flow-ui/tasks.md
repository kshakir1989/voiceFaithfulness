# Tasks: Live Pipeline Learning Flow

**Input**: Design documents from `specs/002-live-pipeline-flow-ui/`

**Prerequisites**: plan.md, spec.md (Approved), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included — constitution TDD; Gherkin (docs) + Playwright e2e + pytest.

**Organization**: Evolve existing app under `apps/voiceFaithfulness/`. Paths relative to that app root unless noted.

**Git**: Work on `voiceFaithfulness/v1.1`; push in chunks; do not commit to `main`.

**UI gate**: `contracts/ui-design.md` **approved** 2026-09-09 via owner waiver (node URLs TBD).

**Owner notes (2026-09-09)**:
- After stories are proven and updated, add **section comments** across Python (and touched SPA modules) so the owner can review what each part does and learn Python usage in this app — see Phase 8.
- Do **not** start implementation until the owner says **go implement** (or `/speckit-implement`).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no incomplete deps)
- **[Story]**: `US1`…`US7` matching `spec.md`
- Exact file paths on every task

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Env keys and docs for new providers; no greenfield scaffold

- [x] T001 [P] Extend `backend/.env.example` with `DEEPGRAM_API_KEY=` and `ASSEMBLYAI_API_KEY=` (keep `GROQ_API_KEY`)
- [x] T002 [P] Update `README.md` for live vs stub, five STT agents, history, layout toggle, demo reset (point at `specs/002-live-pipeline-flow-ui/quickstart.md`)
- [x] T003 [P] Add Gherkin stubs under `features/` for 002 stories (live honesty, agent-owns-summary, rationale, history, highlight, layout, reset)

**Checkpoint**: Docs/env describe 002; features exist as living docs

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Catalog, summary ownership, demo clear API — before story UI polish

**⚠️ CRITICAL**: Complete before claiming US delivery

- [x] T004 Expand transcription catalog to five agents + `owns_summary` / `provider` fields in `backend/app/providers/catalog.py` per `research.md` §2
- [x] T005 [P] Add `power_tier` + `highlight` on judge catalog in `backend/app/providers/catalog.py` per `research.md` §4
- [x] T006 Change runner so summary is owned by `transcription_agent_id` (amend fixed `SUMMARIZER_ID` usage) in `backend/app/domain/runner.py` + factory helpers in `backend/app/providers/factory.py`
- [x] T007 [P] Add Deepgram STT adapter stub/HTTP in `backend/app/providers/deepgram_stt.py` (unavailable without key)
- [x] T008 [P] Add AssemblyAI STT (+ summary when free-path allows) in `backend/app/providers/assemblyai_stt.py` (unavailable without key)
- [x] T009 Wire per-agent summarization (attached summarizer behind agent ID) in `backend/app/providers/` so each transcription agent returns transcript then summary
- [x] T010 Implement `DELETE /api/demo/session` (clear runs, scores, uploads; keep preloads) in `backend/app/api/` and register in `backend/app/main.py`
- [x] T011 [P] Ensure `GET /api/runs` returns newest-first history with transcript, summary, score+rationale per `contracts/api.md`
- [x] T012 [P] Extend agent list JSON responses in `backend/app/api/agents.py` for new catalog fields
- [x] T013 Align score payload to always include `rationale` key (null ok) in `backend/app/domain/runner.py` / API serialization

**Checkpoint**: Catalog returns 5 STT + highlighted judges; POST run attributes summary to STT agent; DELETE demo session works under mocks

---

## Phase 2b: UI/UX Foundation

- [x] T014 Figma frames for VF-FLOW-* — **waived** 2026-09-09 (owner); draw later when quota returns
- [x] T015 Set `Review: approved` in `specs/002-live-pipeline-flow-ui/contracts/ui-design.md` — done via waiver
- [x] T016 [P] Reuse/extend `frontend/src/theme.ts` tokens for flow layout (no new purple/AI-slop look; keep 001 direction)

---

## Phase 3: User Story 1 — Live (non-stub) pipeline pass (P1) 🎯 MVP

**Goal**: Live honesty + successful live/stub-aware end-to-end score

**Independent Test**: Live mode banner when keys; stub banner when forced; run completes with transcript/summary/score/overall

### Tests

- [x] T017 [P] [US1] Pytest for `providers_mode` / stub honesty on health + dashboard in `backend/tests/`
- [x] T018 [P] [US1] Playwright: stub banner visible under mocks; score path still works in `frontend/e2e/`

### Implementation

- [x] T019 [US1] Harden live provider path (unset `FORCE_MOCK_PROVIDERS` + Groq key) in factory/mode modules under `backend/app/`
- [x] T020 [US1] Keep SPA stub/live banners accurate in `frontend/src/App.tsx`
- [x] T021 [US1] Pass US1 tests

**Checkpoint**: SC-001 / SC-006 direction met under mocks; live smoke documented in README

---

## Phase 4: User Story 2 — Transcription agent owns transcript + summary (P1)

**Goal**: Switching STT agents changes attributed transcript/summary

### Tests

- [x] T022 [P] [US2] Pytest: summary `agent_id` / run attribution matches transcription agent in `backend/tests/test_stt_selection.py` (extend) or new `test_summary_ownership.py`
- [x] T023 [P] [US2] Playwright: two runs with different STT show distinct attribution in UI

### Implementation

- [x] T024 [US2] SPA shows which transcription agent produced transcript and summary in `frontend/src/App.tsx`
- [x] T025 [US2] Disable unavailable STT options from catalog `available: false`
- [x] T026 [US2] Pass US2 tests

**Checkpoint**: FR-003/004 visible

---

## Phase 5: User Story 3 — Score rationale reveal (P1)

**Goal**: Hover + accessible reveal of rationale on summary

### Tests

- [x] T027 [P] [US3] Pytest run payload includes rationale under mocks in `backend/tests/`
- [x] T028 [P] [US3] Playwright: open “Why this score?” / hover target shows rationale (`data-testid` vf-rationale*)

### Implementation

- [x] T029 [US3] Extend frontend `Run` type + render rationale reveal in `frontend/src/App.tsx` (hover + keyboard/button)
- [x] T030 [US3] Honest empty state when rationale null
- [x] T031 [US3] Pass US3 tests

**Checkpoint**: SC-003

---

## Phase 6: User Story 4 — Session history (P2)

**Goal**: Multi-run history for comparison

### Tests

- [x] T032 [P] [US4] Pytest `GET /runs` ordering and fields in `backend/tests/`
- [x] T033 [P] [US4] Playwright: two completed runs appear in history list

### Implementation

- [x] T034 [US4] Fetch/render session history panel in `frontend/src/App.tsx` (or `frontend/src/components/HistoryPanel.tsx`)
- [x] T035 [US4] Allow inspecting past summary/score from a history row
- [x] T036 [US4] Pass US4 tests

**Checkpoint**: SC-002

---

## Phase 7: User Story 5 — Judge highlight (P2)

**Goal**: Stronger judges visually highlighted; any judge selectable

### Tests

- [x] T037 [P] [US5] Pytest judge catalog returns `highlight` / `power_tier` in `backend/tests/`
- [x] T038 [P] [US5] Playwright: highlighted option distinguishable; non-highlighted still runnable

### Implementation

- [x] T039 [US5] Render highlight affordance in judge `<select>` / labels in `frontend/src/App.tsx`
- [x] T040 [US5] Pass US5 tests

---

## Phase 8: User Story 6 — Desktop LTR / mobile vertical + toggle (P2)

**Goal**: Explicit view mode toggle

### Tests

- [x] T041 [P] [US6] Playwright: toggle desktop vs mobile changes layout `data-view-mode`; critical controls remain

### Implementation

- [x] T042 [US6] Implement `desktop` | `mobile` layout + sessionStorage persistence in `frontend/src/App.tsx` (CSS/modules as needed)
- [x] T043 [US6] Pass US6 tests

**Checkpoint**: SC-004

---

## Phase 9: User Story 7 — Demo reset (P3)

**Goal**: Clear runs/scores/uploads; keep preloads

### Tests

- [x] T044 [P] [US7] Pytest `DELETE /demo/session` clears store + uploads, preloads remain in `backend/tests/`
- [x] T045 [P] [US7] Playwright: clear control empties history/overall; preloads still in picker

### Implementation

- [x] T046 [US7] SPA “Clear demo data” control calling demo session delete in `frontend/src/App.tsx`
- [x] T047 [US7] Pass US7 tests

**Checkpoint**: SC-005

---

## Phase 10: Polish + educational comments

**Purpose**: Full suite green; teaching comments for owner Python review

- [x] T048 Run full `FORCE_MOCK_PROVIDERS=1 pytest` + `npm run test:e2e`; fix regressions
- [x] T049 [P] Update `specs/002-live-pipeline-flow-ui/checklists/` or quickstart if APIs drifted
- [ ] T050 After T048 green: add clear **section comments** (module/class/function section headers explaining purpose and how Python is used) across touched backend modules under `backend/app/` — especially `domain/`, `providers/`, `api/`, `policy/` — without changing behavior
- [ ] T051 [P] Add brief section comments on new/changed frontend flow modules in `frontend/src/` for the same learning goal
- [ ] T052 Prefer filling Figma node URLs in `contracts/ui-design.md` when MCP quota returns (non-blocking)

**Checkpoint**: Feature proven under mocks; owner can read commented Python as a tour of the app

---

## Dependencies (story order)

- Phase 2 → US1 → US2 → US3 → US4 → US5 → US6 → US7 → Phase 10
- US5 may parallel US4 after Phase 2 if needed
- T050–T051 **only after** behavior proven (T048)

## Parallel examples

- T007 ∥ T008; T017 ∥ T018; T027 ∥ T028; T032 ∥ T033

## Implementation strategy

1. Foundation (catalog, summary ownership, demo delete, runs list)
2. US1–US3 MVP teaching path (live honesty, ownership, rationale)
3. US4–US7 comparison + layout + reset
4. Comment pass for learning review
5. Push `voiceFaithfulness/v1.1` in chunks per story checkpoint
