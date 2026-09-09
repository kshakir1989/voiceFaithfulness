# Feature Specification: LLM Judge Faithfulness Dashboard

**Feature Branch**: `voiceFaithfulness/v1`

**Created**: 2026-09-08

**Status**: Draft

**Input**: User description: "Single-page web app that illustrates LLM-as-judge: user selects ~3-minute all-ages voice recordings (local upload or ~10 preloaded), system transcribes with a chosen free-tier agent (from a drop-down list), summarizes the transcript, then a slightly stronger free-tier judge model chosen from a second drop-down list scores summary faithfulness 0–100; each scored recording updates an overall percentage on a dashboard with educational in-UI messages; UI and backend covered by automated acceptance tests."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Score a preloaded recording end-to-end (Priority: P1)

A learner opens the single-page app, picks one preloaded all-ages conversation from a picker, chooses a free-tier transcription agent and a free-tier judge agent from their drop-downs, runs the faithfulness pipeline, and sees stage progress plus a 0–100 faithfulness score for that recording and an updated overall percentage on the dashboard.

**Why this priority**: Without a complete pipeline and visible score, the product does not demonstrate LLM-as-judge.

**Independent Test**: Open the app, select a preloaded recording, select transcription and judge agents from their drop-downs, start scoring, wait until complete, confirm transcript/summary/score stages finished, per-recording score shown, overall percentage updated.

**Acceptance Scenarios**:

1. **Given** the app is open and preloaded recordings are available, **When** I open the picker, **Then** I see approximately 10 all-ages conversations I can choose from.
2. **Given** I selected a preloaded recording, a transcription agent, and a judge agent from their drop-downs, **When** I start the pipeline, **Then** I see clear progress through transcript → summary → faithfulness score.
3. **Given** the pipeline completes successfully, **When** I view the dashboard, **Then** I see that recording’s faithfulness percentage (0–100) and an overall percentage that includes it.

---

### User Story 2 - Choose a free-tier transcription agent (Priority: P1)

Before transcription runs, a learner opens a drop-down of available free-tier transcription agents, selects one, and that choice is used for the transcript stage of the current pipeline run.

**Why this priority**: Agent choice is part of the learning demo—learners must see that different free-tier transcribers can be selected, not a hidden fixed backend.

**Independent Test**: Open the transcription-agent drop-down, confirm more than one free-tier option when available, select a different option than the default, run the pipeline, confirm the run records/uses the selected agent for transcription.

**Acceptance Scenarios**:

1. **Given** the app is open and ready to score a recording, **When** I open the transcription-agent drop-down, **Then** I see a list of free-tier transcription agents I can choose from.
2. **Given** I selected a transcription agent from the drop-down, **When** I start the pipeline, **Then** the transcript stage uses that selected agent (not a different silent default).
3. **Given** a transcription agent is unavailable or at a free-tier limit, **When** I try to use it, **Then** I see a clear message and can choose another listed agent when one remains available.

---

### User Story 3 - Choose a free-tier judge agent (Priority: P1)

Before judging runs, a learner opens a drop-down of available free-tier judge agents (slightly stronger than the transcription tier where the catalog allows), selects one, and that choice is used for the faithfulness-scoring stage of the current pipeline run.

**Why this priority**: Choosing the judge makes LLM-as-judge visible and comparable; a hidden fixed judge hides the lesson.

**Independent Test**: Open the judge-agent drop-down, confirm free-tier judge options, select a non-default option, complete a run, confirm the run records/uses the selected judge for the 0–100 score.

**Acceptance Scenarios**:

1. **Given** the app is open and ready to score a recording, **When** I open the judge-agent drop-down, **Then** I see a list of free-tier judge agents I can choose from.
2. **Given** I selected a judge agent from the drop-down, **When** the judge stage runs, **Then** faithfulness scoring uses that selected agent (not a different silent default).
3. **Given** a judge agent is unavailable or at a free-tier limit, **When** I try to use it, **Then** I see a clear message and can choose another listed judge when one remains available.

---

### User Story 4 - Add a local recording (Priority: P1)

A learner adds an audio file from their device (or picks a preloaded one), can listen to the selected recording before running the pipeline, runs the same pipeline, then sees the transcript and its summary alongside the faithfulness score—or receives a clear block if the material is not all-ages acceptable.

**Why this priority**: Local add is a required ingest path alongside the picker; preview and post-run text make the LLM-as-judge lesson concrete (what was heard → what was written → what was judged).

**Independent Test**: Preview-play a selected recording; upload a valid all-ages sample, complete scoring, confirm transcript and summary are visible and the score appears on the dashboard. Upload or flag a disallowed sample and confirm scoring is blocked with a clear message.

**Acceptance Scenarios**:

1. **Given** I am on the app, **When** I choose to add a local audio file that is accepted, **Then** the recording appears as selectable/runnable in the same flow as preloaded items.
2. **Given** a local recording is accepted, **When** the pipeline completes, **Then** its score contributes to the overall percentage.
3. **Given** a local recording fails the all-ages policy, **When** I try to score it, **Then** scoring is blocked and I see a clear message explaining why.
4. **Given** I have selected a recording (preloaded or local), **When** I use the preview control, **Then** I can listen to that audio before starting the pipeline.
5. **Given** a pipeline run has produced a transcript, **When** I view the completed (or in-progress after transcript) run, **Then** I see a readable visual representation of the transcript text.
6. **Given** a pipeline run has produced a summary, **When** I view the completed run, **Then** I see the summary text displayed so I can compare it to the transcript and the faithfulness score.

---

### User Story 5 - Learn the LLM-as-judge process in the UI (Priority: P2)

As the learner works, the page shows short plain-language messages explaining what each stage means (ingest, transcript, summary, judge, aggregate) so the dashboard teaches the concept while it runs.

**Why this priority**: Constitution requires Teach-in-UI; metrics alone are insufficient.

**Independent Test**: Walk through one scoring run and confirm educational messages appear for each major stage without cluttering the primary metrics.

**Acceptance Scenarios**:

1. **Given** I start a pipeline run, **When** each stage begins or completes, **Then** I see a short explanation of that stage’s role in LLM-as-judge.
2. **Given** I view the overall percentage, **When** educational copy is shown, **Then** it explains that the overall value is built from individual recording scores.

---

### User Story 6 - View dashboard metrics clearly (Priority: P2)

A learner sees a clean, elegant, responsive single-page dashboard listing scored recordings with individual percentages and the overall aggregate, without a cluttered layout. The learner can switch among a small set of graph views to see the same metrics more visually.

**Why this priority**: The dashboard is the product surface and must stay readable on desktop and mobile; optional charts reinforce learning without replacing the primary numbers.

**Independent Test**: Score at least two recordings; confirm both rows and the overall percentage are visible and usable on a narrow viewport; switch graph views and confirm each view reflects the same scored data.

**Acceptance Scenarios**:

1. **Given** at least one recording has been scored, **When** I view the dashboard, **Then** I see each scored recording with its faithfulness percentage and the overall percentage.
2. **Given** I am on a mobile-sized viewport, **When** I view the dashboard, **Then** primary metrics and actions remain readable and usable without horizontal clutter.
3. **Given** at least two recordings have been scored, **When** I open the graph-view selector, **Then** I can choose among the available visual views (at least: per-recording scores bar view, and overall/aggregate view).
4. **Given** I selected a graph view, **When** the chart renders, **Then** it shows values consistent with the listed per-recording scores and overall percentage (no contradictory numbers).
5. **Given** no recordings have been scored yet, **When** I view graph options, **Then** I see an empty/neutral chart state (not fabricated data).

---

### User Story 7 - Graceful free-tier limits and failures (Priority: P3)

When a free-tier limit or stage failure occurs, the learner sees an explicit message and the app does not invent scores or silently fail.

**Why this priority**: Free-tier first requires honest degradation for a learning demo.

**Independent Test**: Simulate or trigger a stage failure / limit; confirm a user-visible message and no fabricated faithfulness percentage for that run.

**Acceptance Scenarios**:

1. **Given** transcription, summarization, or judging cannot complete, **When** the failure is detected, **Then** I see an explicit message and that run does not add a fake score to the overall percentage.
2. **Given** a free-tier limit is hit, **When** I attempt a new run, **Then** I am told clearly that the limit was reached.

---

### Edge Cases

- What happens when the overall percentage has zero scored recordings? → Show an empty/neutral overall state (e.g. “No scores yet”), not a fake 0% that implies a judged failure.
- What happens if the user starts a second run while one is in progress? → Only one active pipeline run at a time; the UI blocks or queues with a clear message.
- What happens if a preloaded recording’s pipeline partially completes? → No partial contribution to overall percentage until a final 0–100 score exists.
- What happens if uploaded audio is empty, corrupt, or unsupported? → Reject with a clear message; do not start the judge pipeline.
- What happens if the summary is empty but transcript exists? → Fail the run with a message; do not ask the judge for a score.
- What happens if no transcription agent is selected? → Pipeline MUST NOT start until the learner selects an agent from the drop-down (or confirms the shown default selection).
- What happens if no judge agent is selected? → Pipeline MUST NOT start until the learner selects a judge from the drop-down (or confirms the shown default selection).
- What happens if the only listed transcription agents are all at free-tier limit? → Show an explicit limit message; do not invent a transcript.
- What happens if the only listed judge agents are all at free-tier limit? → Show an explicit limit message; do not invent a faithfulness score.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST present a single-page experience for selecting recordings, choosing transcription and judge agents, running the pipeline, viewing scores, and reading educational messages.
- **FR-002**: System MUST provide a picker of approximately 10 preloaded all-ages voice conversations, each about 3 minutes long.
- **FR-003**: Users MUST be able to add a recording from a local file for scoring.
- **FR-004**: System MUST present a drop-down list of free-tier transcription agents and MUST require an explicit selected transcription agent before the pipeline starts.
- **FR-005**: System MUST present a separate drop-down list of free-tier judge agents (slightly stronger tier than transcription where the catalog allows) and MUST require an explicit selected judge agent before the pipeline starts.
- **FR-006**: For every scored recording, the system MUST run this ordered pipeline only: ingest → full transcript (via the selected free-tier transcription agent) → summary of transcript → faithfulness score 0–100 of summary vs transcript (via the selected free-tier judge agent) → contribute to overall aggregate.
- **FR-007**: System MUST NOT judge faithfulness against raw audio when a transcript exists, invent scores, or skip pipeline stages.
- **FR-008**: System MUST display each completed recording’s faithfulness percentage and an overall percentage derived from completed scores only.
- **FR-009**: Overall percentage MUST be the arithmetic mean of all completed recording faithfulness scores (equal weight per completed recording).
- **FR-010**: System MUST show short plain-language teaching messages for ingest, transcript, summary, judge, and aggregate concepts during use.
- **FR-011**: System MUST enforce all-ages policy for preloaded content and MUST block scoring of local uploads that fail the policy, with a clear UI message.
- **FR-012**: When free-tier limits or stage errors occur, the system MUST show an explicit user-visible message and MUST NOT add a fabricated score to the overall percentage.
- **FR-013**: UI MUST follow an elegant, minimal, responsive layout focused on learning (not a cluttered metrics wall).
- **FR-014**: Automated acceptance tests MUST cover UI capabilities and backend/pipeline capabilities for the behaviors in this spec.
- **FR-015**: System MUST allow the user to see pipeline stage status for the active or last run (at least: pending, running, completed, failed per stage).
- **FR-016**: Each completed or failed pipeline run MUST record which transcription agent and which judge agent were selected for that run so the learner can see which agents produced the transcript and the score.
- **FR-017**: v1 summarization MUST use a free-tier summarizer configured by the product (not a third learner-facing drop-down), unless a later amendment adds one.
- **FR-018**: System MUST let the learner select among a small set of dashboard graph views (at least two: per-recording faithfulness scores, and overall/aggregate) without hiding the numeric list/overall percentage.
- **FR-019**: Selected graph views MUST display values consistent with completed faithfulness scores and the overall aggregate; empty state MUST NOT invent data.
- **FR-020**: System MUST let the learner listen to the currently selected recording (preloaded or accepted local) via an in-page audio preview before starting the pipeline.
- **FR-021**: After the transcript stage succeeds, the system MUST display a readable visual representation of the transcript text (scrollable text panel; waveform optional, not required in v1).
- **FR-022**: After the summary stage succeeds, the system MUST display the summary text so the learner can see what the judge compared to the transcript.

### Key Entities

- **Recording**: A voice conversation available for scoring (preloaded or local); metadata includes title/label, source type, duration target (~3 minutes for preloaded), and all-ages eligibility.
- **Transcription Agent**: A free-tier transcription option shown in its drop-down; identified by a learner-visible name; used only for the transcript stage of a run.
- **Judge Agent**: A free-tier (slightly stronger) judging option shown in its drop-down; identified by a learner-visible name; used only for the faithfulness-scoring stage of a run.
- **Transcript**: Full text produced from a recording by the selected transcription agent; source of truth for later summary and judge steps.
- **Summary**: Condensed text derived from the transcript only (via the product-configured free-tier summarizer in v1).
- **Faithfulness Score**: Integer or numeric percentage 0–100 judging how faithful the summary is to the transcript, produced by the selected judge agent.
- **Pipeline Run**: One attempt to process a recording through all stages with selected transcription and judge agents; ends completed or failed; only completed runs with a score affect the aggregate.
- **Dashboard Aggregate**: Overall percentage computed from completed faithfulness scores.
- **Dashboard Graph View**: A learner-selectable visual presentation of completed scores and/or the overall aggregate (e.g. per-recording bar view, overall/aggregate view); always consistent with the numeric dashboard.
- **Teaching Message**: Short educational copy tied to a pipeline concept or stage.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new learner can select a preloaded recording, choose transcription and judge agents from their drop-downs, and obtain a visible faithfulness percentage within one guided session without leaving the single page.
- **SC-002**: After scoring N completed recordings (N ≥ 2), the displayed overall percentage equals the mean of those N scores (within ordinary rounding).
- **SC-003**: 100% of preloaded demo conversations shipped with the product are all-ages appropriate.
- **SC-004**: When a pipeline stage fails or a free-tier limit is hit, users see an explicit message in 100% of such cases and no fabricated score is added.
- **SC-005**: Educational messages for all five concepts (ingest, transcript, summary, judge, aggregate) appear at least once during a successful end-to-end run.
- **SC-006**: Primary dashboard tasks (pick/run, choose transcription agent, choose judge agent, see per-recording score, see overall percentage, switch graph views) remain completable on a mobile-width viewport without horizontal scrolling of critical controls.
- **SC-007**: Automated acceptance coverage includes both UI flows and backend/pipeline behaviors described in P1 user stories before the feature is considered done.
- **SC-008**: For a completed run, the learner can identify which transcription agent and which judge agent were used for that run.
- **SC-009**: With at least two completed scores, the learner can switch graph views and each view remains numerically consistent with the listed scores and overall percentage.
- **SC-010**: Before starting a run, the learner can play the selected recording in-page; after a successful run, both the transcript text and the summary text are visible on the same page.

## Assumptions

- v1 is a learning/demo product: no user accounts or multi-tenant auth.
- “Approximately 10” preloaded recordings means 8–12 items is acceptable if labeled clearly.
- Aggregate uses equal-weighted arithmetic mean of completed scores only; failed runs do not count.
- Faithfulness is judged against the transcript, not the raw audio, once transcription succeeds.
- Free-tier transcription agents, a product-configured free-tier summarizer, and free-tier judge agents (drop-down options; slightly stronger tier) will be named in the implementation plan (constitution TODO(PROVIDERS)); this spec requires visible transcription and judge drop-downs, free-tier preference, and graceful limit handling, not specific vendor brands in the product requirements.
- v1 may show sensible defaults selected in both agent drop-downs, but the learner MUST still be able to change each before starting the run.
- v1 does **not** expose a summarizer drop-down (summarizer is fixed/configured); add only via a later spec amendment if desired.
- v1 graph views stay minimal: at least per-recording faithfulness bars and an overall/aggregate view; additional chart types only if they stay elegant and do not clutter the single page.
- Visual design will be approved in Figma and recorded in `contracts/ui-design.md` before UI implementation (constitution IX / XI).
- Stack choices (Python backend, Gherkin + Playwright acceptance tests, etc.) are governed by the app constitution and plan, not restated as product requirements here.
- Local uploads that cannot be policy-checked automatically may be blocked pending review rather than scored; the user still receives a clear message.
