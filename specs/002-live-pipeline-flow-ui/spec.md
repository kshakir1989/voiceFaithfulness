# Feature Specification: Live Pipeline Learning Flow

**Feature Branch**: `voiceFaithfulness/v1.1`

**Created**: 2026-09-09

**Status**: Approved

**Input**: Assess handoff `live-pipeline-flow-ui` Option B — Full teaching flow on v1.1: learners need trustworthy non-stub pipeline outputs; transcription agents that own transcript and summary; comparable re-runs with session history; judge score with rationale on summary hover; overall aggregate; desktop left-to-right / mobile vertical layout with explicit toggle; demo reset that clears runs/scores/uploads while retaining preloaded recordings. Amends 001 FR-017 (fixed summarizer).

**Assessment**: `.specify/assessments/live-pipeline-flow-ui/decision.md` (verdict: go)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete a live (non-stub) pipeline pass (Priority: P1)

A learner opens the app with live providers available, picks a preloaded or uploaded all-ages recording, chooses a transcription agent and a judge agent, runs the pipeline, and sees real transcript text, summary text, a faithfulness score, and an updated overall percentage—without mistaking stub placeholders for analysis of their audio.

**Why this priority**: Without a trustworthy end-to-end pass, the teaching product fails its purpose.

**Independent Test**: With live providers configured, run one recording end to end; confirm stub/live honesty signals match live mode; confirm transcript, summary, score, and overall update.

**Acceptance Scenarios**:

1. **Given** live providers are active, **When** I open the app, **Then** I see a clear live-mode signal (not stub-mode placeholders for pipeline truth).
2. **Given** I selected a recording, transcription agent, and judge agent, **When** I complete a successful run, **Then** I see transcript text, summary text, a 0–100 score for that run, and an overall percentage that includes it.
3. **Given** providers are stubbed, **When** I view scores or transcripts, **Then** I see an explicit stub warning so I do not treat them as real audio analysis.

---

### User Story 2 - Transcription agent owns transcript and summary (Priority: P1)

A learner selects a free-tier transcription agent from the catalog. That agent produces both the transcript and the summary for the run. Switching agents and re-running yields different transcript and/or summary text when agents differ, so the learner can compare quality.

**Why this priority**: Comparison of agent quality for both transcript and summary is a core learning goal; amends the prior fixed-summarizer rule.

**Independent Test**: Run the same recording with two different transcription agents; confirm each run records the selected agent and shows that agent’s transcript and summary.

**Acceptance Scenarios**:

1. **Given** the transcription-agent catalog is available, **When** I open it, **Then** I see multiple free-tier options (target: up to five when available).
2. **Given** I selected transcription agent A, **When** the pipeline completes, **Then** the transcript and summary for that run are attributed to agent A.
3. **Given** I re-run the same recording with transcription agent B, **When** both runs complete, **Then** I can tell which transcript and summary came from which agent.

---

### User Story 3 - Understand why a score was given (Priority: P1)

After a successful judge stage, a learner sees the faithfulness score and can inspect the judge’s rationale by interacting with the summary (hover on desktop-capable pointers), so they can explain the score in plain language.

**Why this priority**: A number without reason does not teach LLM-as-judge.

**Independent Test**: Complete one successful run; locate the score; reveal rationale via summary hover (or equivalent accessible reveal); confirm rationale text is present.

**Acceptance Scenarios**:

1. **Given** a completed run with a score, **When** I view the run result, **Then** I see the numeric faithfulness score for that instance.
2. **Given** a completed run with a rationale, **When** I hover (or otherwise reveal) over the summary, **Then** I see the judge rationale for that score.
3. **Given** a completed run where rationale is missing, **When** I reveal the summary explanation, **Then** I see an honest empty/unavailable state—not an invented reason.

---

### User Story 4 - Compare runs via session history (Priority: P2)

A learner re-runs the pipeline with different transcription and/or judge combinations in one session and reviews a multi-run history to compare summaries and scores. They do not need concurrent side-by-side runs.

**Why this priority**: Comparison is required for the teaching goal but depends on Stories 1–2 working first.

**Independent Test**: Complete at least two successful runs with different agent choices; open session history; confirm both runs appear with agents, summaries (or links to them), and scores.

**Acceptance Scenarios**:

1. **Given** I completed two runs with different agent combinations, **When** I open session history, **Then** I see both runs listed with their agents and scores.
2. **Given** session history has multiple summaries, **When** I inspect past runs, **Then** I can view the different summaries produced across those runs.
3. **Given** only one run exists, **When** I open history, **Then** I see that single run without fabricated extras.

---

### User Story 5 - Choose any judge with stronger models highlighted (Priority: P2)

A learner may select any listed free-tier judge agent. Judges that are more powerful models are visually highlighted relative to the transcription agent that produced the summary being judged, reinforcing the “stronger judge” lesson without blocking weaker choices.

**Why this priority**: Highlighting teaches the intended pattern; free choice preserves exploration.

**Independent Test**: Open the judge drop-down; confirm any available judge can be selected; confirm stronger/more powerful judges are visually distinguished.

**Acceptance Scenarios**:

1. **Given** the judge catalog is open, **When** I review options, **Then** I can select any available judge agent.
2. **Given** the catalog marks some judges as more powerful, **When** I view the list, **Then** those options are highlighted relative to others / relative to the transcription-agent context.
3. **Given** I selected a non-highlighted judge, **When** I run the pipeline, **Then** that judge is still used for scoring (highlight is guidance, not a hard block).

---

### User Story 6 - Read the lesson in a flow layout (Priority: P2)

A learner views pipeline information in a left-to-right flow on desktop presentation and a vertical flow on mobile presentation, and can explicitly switch between desktop and mobile view modes.

**Why this priority**: Improves teaching clarity; not required for a minimal live score, hence P2.

**Independent Test**: Toggle desktop vs mobile view; confirm LTR vs vertical arrangement of the main pipeline information without losing access to transcript, summary, score, or overall.

**Acceptance Scenarios**:

1. **Given** desktop view is selected, **When** I view the pipeline results, **Then** primary stages/information read left to right.
2. **Given** mobile view is selected, **When** I view the pipeline results, **Then** primary stages/information stack vertically.
3. **Given** either view, **When** I switch modes, **Then** I still can access transcript, summary, score, and overall aggregate.

---

### User Story 7 - Reset demo data for a clean walkthrough (Priority: P3)

After demonstrating the app, an operator clears session pipeline data (runs, scores, and uploads) while preloaded demo recordings remain, so the next walkthrough starts clean.

**Why this priority**: Demo hygiene; not required for the first successful live lesson.

**Independent Test**: Accumulate runs and an upload; trigger clear; confirm history/scores/uploads are gone and preloaded recordings remain selectable.

**Acceptance Scenarios**:

1. **Given** session runs, scores, and at least one upload exist, **When** I clear demo data, **Then** runs and scores are removed and uploads are removed.
2. **Given** I cleared demo data, **When** I open the recording picker, **Then** preloaded demo recordings are still available.
3. **Given** I cleared demo data, **When** I view overall percentage, **Then** it reflects no completed scores (empty state), not a stale average.

---

### Edge Cases

- What happens if live providers are unavailable or keys are missing? → Stay in stub mode with explicit honesty banners; do not present stub outputs as live analysis.
- What happens on free-tier rate limits or provider failure? → Fail the run with a clear message; do not invent transcript, summary, score, or rationale.
- What happens if summary is empty after transcription? → Fail the run before judging; no score added to overall.
- What happens if two runs are requested while one is active? → Block the second start with a clear in-progress message (sequential runs only).
- What happens if history is empty? → Show a neutral empty state.
- What happens on blocked / non-all-ages recordings? → Do not score; show the existing all-ages block message.
- What happens if rationale text is unstructured? → Show the available rationale text in the reveal/tooltip; do not invent structured criteria.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support a live (non-stub) end-to-end pipeline for eligible recordings when providers are configured, producing transcript, summary, faithfulness score, and aggregate contribution.
- **FR-002**: System MUST clearly signal stub vs live mode so learners cannot confuse placeholder outputs with live analysis.
- **FR-003**: System MUST present a catalog of free-tier transcription agents (target up to five when available) and require an explicit selection before a run starts.
- **FR-004**: The selected transcription agent MUST produce both the transcript and the summary for that run (amends 001 FR-017 fixed product summarizer).
- **FR-005**: System MUST present a catalog of free-tier judge agents and allow selection of any available judge for a run.
- **FR-006**: System MUST visually highlight judge options that are more powerful models relative to the transcription-agent context, without preventing selection of non-highlighted judges.
- **FR-007**: For each completed run, the system MUST display transcript text, summary text, and faithfulness score 0–100.
- **FR-008**: For each completed run with a rationale, the system MUST make that rationale revealable from the summary (hover on pointer devices, with an accessible equivalent).
- **FR-009**: System MUST retain multi-run history within the session so learners can compare agent combinations, summaries, and scores after sequential re-runs.
- **FR-010**: System MUST NOT require concurrent side-by-side pipeline execution; comparison is via sequential runs plus history.
- **FR-011**: System MUST show an overall aggregate across completed judgements in the session (mean of completed scores; empty state when none).
- **FR-012**: System MUST provide an explicit desktop vs mobile view control: desktop presents primary pipeline information left-to-right; mobile presents it vertically.
- **FR-013**: System MUST provide a clear-demo-data action that removes session runs, scores, and uploads while retaining preloaded demo recordings.
- **FR-014**: System MUST NOT invent scores, transcripts, summaries, or rationales on failure or rate limit.
- **FR-015**: System MUST continue to enforce all-ages eligibility before scoring (blocked demos remain unscored with a clear message).
- **FR-016**: Each run MUST record which transcription agent and which judge agent were used.
- **FR-017**: Existing teaching messages for ingest → transcript → summary → judge → aggregate MUST remain available during use.
- **FR-018**: Provider catalog specifics (exact vendor roster, keys, rate-limit mapping) MUST be decided in planning without blocking this specification’s user-facing behavior.

### Key Entities

- **Transcription Agent**: Free-tier selectable option that produces transcript and summary for a run; identified by a learner-visible name.
- **Judge Agent**: Free-tier selectable option that scores summary faithfulness vs transcript; may be marked as a more powerful model for highlighting.
- **Pipeline Run**: One sequential attempt through ingest → transcript → summary → judge → aggregate contribution; completed or failed; stores agents used, texts, score, and optional rationale.
- **Session History**: In-session list of pipeline runs available for comparison until cleared or session ends.
- **Faithfulness Score**: Numeric 0–100 for one completed run, with optional rationale text from the judge.
- **Overall Aggregate**: Mean of completed session scores; null/empty when none.
- **View Mode**: Explicit learner choice between desktop (left-to-right) and mobile (vertical) presentation of primary pipeline information.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: With live providers configured, a learner can complete one guided end-to-end pass (recording → transcript → summary → score → overall) in a single session without treating stub data as live analysis.
- **SC-002**: In one session, a learner can complete at least two runs with different transcription agents and at least two runs with different judge agents and identify them in session history.
- **SC-003**: After one successful run, a learner can point to displayed rationale (via summary reveal) and explain the score in plain language.
- **SC-004**: A learner can switch between desktop and mobile view modes and still access transcript, summary, score, and overall without losing critical controls.
- **SC-005**: After clear-demo-data, session runs/scores/uploads are gone, preloaded recordings remain, and overall shows empty state.
- **SC-006**: Stub vs live mode is unambiguous whenever pipeline outputs are shown.
- **SC-007**: Failed or rate-limited runs never add invented scores to the overall percentage.

## Assumptions

- Work continues on the `voiceFaithfulness/v1.1` implementation track as an evolution of `001-llm-judge-dashboard`, not a greenfield app.
- Exact top-five free STT vendor roster and how each produces summaries is resolved during `/speckit-plan` research (behavior here requires “transcription agent owns summary,” not specific brands).
- “More powerful model” for judge highlighting is expressible as a catalog attribute decided in plan.
- Hover tooltip (plus accessible equivalent) is sufficient for v1.1 rationale; richer layered criteria UI may follow later.
- Session-scoped history (no durable multi-user accounts) is enough for demos.
- Owner can supply provider credentials needed for live demos when available; otherwise stub honesty remains mandatory.
- Concurrent side-by-side runs, production deploy, and App Store publish remain out of scope.
