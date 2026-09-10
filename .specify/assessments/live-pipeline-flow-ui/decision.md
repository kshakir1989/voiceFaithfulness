# Decision: Live pipeline learning flow (v1.1)

- **Slug**: live-pipeline-flow-ui
- **Decided**: 2026-09-09
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md | owner confirmation of Option B

## Scorecard

| Criterion | Rating | Justification |
|-----------|--------|---------------|
| Problem validity | strong | Stub-only demo blocks the teaching purpose; owner demand is concrete and current. — [problem.md, intake.md] |
| Evidence strength | adequate | Repo evidence for stub/live, missing rationale UI, fixed summarizer, single-run UI; owner clarifications closed most gaps. External “top five STT” roster still TBD at specify/plan. — [research.md, problem.md] |
| Value vs. inaction | strong | Doing nothing leaves an unconvincing demo; Option B unblocks the lesson. — [problem.md Cost of Inaction] |
| Feasibility / appetite | adequate | Option B is medium appetite on existing v1 SPA/API; Option C is explicit shrink path. Owner chose B. — [concept.md] |
| Strategic fit | strong | Continuation on voiceFaithfulness v1.1; aligns with LLM-as-judge teaching SPA. — [intake.md, problem.md] |
| Risk posture | adequate | Rate limits, multi-vendor STT, FR-017 amend, layout toggle named; mitigated by honest failures, session-only history, tooltip-first rationale. — [concept.md rabbit holes] |

## Verdict & Rationale

**go.** Problem is real, evidence is adequate (repo + owner clarifications), Option B is shaped and owner-confirmed, and value beats inaction. Remaining open items (exact STT roster, judge “power” attribute, rationale parse depth) belong in `/speckit-specify` and plan research—not blockers for assess.

## If needs-clarification

*(Not active.)*

## If go — Handoff to `/speckit-specify`

- **Problem**: Learners can hear sample audio but cannot walk the full LLM-as-judge lesson with trustworthy agent outputs, comparison, score explainability, and overall aggregation on the v1.1 track.
- **Chosen approach**: Option B — Full teaching flow on v1.1 (live free-tier agents; transcription agent owns transcript+summary; any judge with stronger models highlighted; rationale on summary hover; multi-run session history; overall aggregate; clear scores/runs/uploads retaining preloads; desktop LTR / mobile vertical with layout toggle; stub/live honesty).
- **In scope**: Live non-stub pipeline; top free-tier STT catalog (target five, named in plan); agent comparison via sequential re-runs + history; score + rationale UX; overall %; demo reset (runs/scores/uploads only); responsive flow presentation with explicit view toggle; amend FR-017 so transcription agent owns summary.
- **Out of scope**: Concurrent side-by-side runs; production deploy / multi-user / cross-session persistence; fake scores on failure; general STT platform; App Store publish; deep structured-rationale productization beyond teaching needs.
- **Success metrics**: Live end-to-end pass; ≥2 STT and ≥2 judge comparisons in one session via history; explain score from displayed rationale; desktop + mobile layouts via toggle; demo reset keeping preloads; clear stub vs live signaling.
- **Carried-forward open questions**: Exact top-five STT roster and summary capability per agent; catalog attribute for “more powerful” judge highlight; how much rationale structuring beyond raw tooltip text; provider keys available for demos.
