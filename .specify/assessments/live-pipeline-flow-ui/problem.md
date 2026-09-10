# Problem Definition: Live pipeline learning flow

- **Slug**: live-pipeline-flow-ui
- **Created**: 2026-09-09
- **Inputs used**: intake.md | research.md

## Problem Statement

A learner using voiceFaithfulness today can listen to sample audio but cannot reliably walk through the full LLM-as-judge lesson with trustworthy, agent-produced outputs. Stubbed transcript, summary, and score data hide how transcription agents, summarization, and judging differ in quality, why a faithfulness score was assigned, and how individual runs roll up into an overall result—so the app fails its core teaching purpose on the v1.1 continuation track.

## Affected Users & Stakeholders

- **Users — Learner / demo operator**: runs the single-page app to understand audio → transcript → summary → judge → aggregate; needs to compare agent choices, inspect outputs, and trust that scores reflect real pipeline behavior (not placeholders). — [source: intake.md, research.md]
- **Users — Owner (self-demo)**: validates the product before wider demos; currently blocked from demonstrating the full workflow end to end. — [source: intake.md]
- **Stakeholders — Owner (Khalil)**: decides v1.1 scope, provider keys, and when live (non-stub) behavior is acceptable for demos. — [source: intake.md]
- **Stakeholders — Future reviewers / learners**: depend on honest stub-vs-live signaling and repeatable demo sessions. — [source: research.md (stub/live mode, scores_are_stubbed)]

## Goals

- Enable a learner to complete one full pipeline pass on real audio with non-stub agent outputs from the agreed free-tier transcription catalog (top five providers in scope). — [source: intake.md]
- Make transcript and summary from the selected transcription agent visible and understandable as distinct pipeline artifacts. — [source: intake.md, research.md]
- Allow comparison across agent choices by re-running the pipeline per agent combination and retaining session history (not only the latest run). — [source: intake.md, research.md]
- Surface faithfulness scores with enough explanation that a learner can articulate *why* a score was given, not only the numeric value. — [source: intake.md, research.md (rationale exists backend-side but not in UI)]
- Show per-run scores alongside an overall aggregate across completed judgements in the session. — [source: intake.md]
- Present the full lesson in a readable flow: horizontal on desktop, vertical on mobile, with an explicit way to switch between those presentation modes. — [source: intake.md, research.md]
- Support demo hygiene: after functions have been shown, the operator can clear accumulated session data to reset for the next walkthrough. — [source: intake.md]
- Visually distinguish stronger judge options relative to the transcription agent that produced the summary being judged. — [source: research.md (owner clarification)]

## Non-Goals

- Replacing voiceFaithfulness with a general-purpose transcription or evaluation platform.
- Side-by-side concurrent pipeline runs (comparison is via sequential re-runs with retained history). — [source: intake.md, research.md]
- Production deployment, multi-user accounts, or persistent cross-session history beyond what the demo needs.
- Inventing faithfulness scores or rationales when providers fail or rate-limit (honest failure remains required). — [source: research.md, spec FR on no fake scores]
- Resolving all provider-vendor branding or legal terms in this assessment (catalog details belong in specify/plan).
- App Store / external publish requirements (local demo remains the frame).

## Success Metrics

- **End-to-end learning pass (qualitative)**: owner can run one preloaded or uploaded recording through live providers, see transcript and summary, receive a judge score with rationale, and see the overall aggregate update—without mistaking stub data for real analysis. (baseline: audio preview only; stub placeholders for pipeline outputs) — [source: intake.md, research.md]
- **Agent comparison (qualitative)**: owner can re-run with at least two different transcription-agent choices and at least two judge choices in one session and review retained history to compare output quality. (baseline: single run snapshot in UI) — [source: intake.md, research.md]
- **Score explainability (qualitative)**: owner can point to displayed rationale (raw and structured layers) and explain the score in plain language after one successful run. (baseline: score value only; rationale not shown) — [source: research.md]
- **Layout usability (qualitative)**: owner can complete primary tasks in desktop flow layout and mobile vertical layout using the view toggle without losing access to transcript, summary, score, or aggregate. (baseline: single-column vertical layout only) — [source: intake.md, research.md]
- **Demo reset (qualitative)**: owner can clear session run/score history and repeat a clean demo. (baseline: partial reset via upload session delete / dev reset; no unified “clear demo data” UX stated) — [source: intake.md]
- **Stub honesty (binary)**: when providers are stubbed, the UI clearly signals stubbed scores/transcripts; when live, it signals live mode. (baseline: banners exist but learner still experiences stub as “only hearing sample text”) — [source: research.md]

## Cost of Inaction

voiceFaithfulness remains a partial demo: audio works but the LLM-as-judge lesson stays abstract. The owner cannot credibly show how agent choice affects transcript and summary quality, why faithfulness scores differ, or how aggregation works—blocking v1.1’s purpose as a teaching SPA and forcing ad-hoc explanation outside the product.

## Open Questions

- [NEEDS CLARIFICATION: Exact roster of the “top five free STT providers” and which also produce summaries vs transcript-only.]
  - Research the top 5 free STT providers and which also produce summaries. 
- [NEEDS CLARIFICATION: How “stronger judge” is defined relative to a given transcription agent for highlighting (catalog tier, model size, fixed ordering, or dynamic per pairing).]
  - The stronger judge is a more powerful model. 
- [NEEDS CLARIFICATION: How layered rationale (raw, criteria, bullets) is derived when the judge returns unstructured text only.]
  - The rationale should be displayed in a tooltip when the user hovers over the summary.
- [NEEDS CLARIFICATION: Whether amending spec FR-017 (fixed summarizer) to “transcription agent owns summary” is accepted as part of v1.1 or needs a separate spec amendment gate.]
  - The summarizer is the agent that produces the summary is accepted as part of v1.1
- [NEEDS CLARIFICATION: Scope of “remove data” — scores/runs only, uploads too, or full dev reset equivalent exposed in the UI.]
  - The scope of “remove data” is the scores/runs and uploads only.
  - Only the current demo recordings should be retained on reset. 
  - Rational: This is to ensure that the demo is repeatable and the user can see the full flow of the pipeline.