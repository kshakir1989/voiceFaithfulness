<!--
Sync Impact Report
- Version change: 1.2.1 → 1.2.2
- Modified: XII + Development Workflow — push feature branch in small chunks
- Notes: monorepo AGENTS.md establishes the same rule for all apps
-->

# voiceFaithfulness Constitution

## Core Principles

### I. Ask First
Agents MUST ask the owner before running commands, making edits, creating
commits, or deploying. Agents MUST NOT implement application behavior unless
the owner explicitly says to implement it (or replies **go** after
Teach-Along for that step). Rationale: owner-driven delivery; protects review
and Cursor budget.

### II. Spec First
User-facing behavior MUST be documented in a Spec Kit feature spec under
`specs/` before or with the change that implements it. Agents MUST NOT add
or change user-facing behavior without a matching spec. Automated tests for
that behavior MUST land with the implementation using the locked test stack
in Product Constraints. Rationale: the spec is what we can review and run.

### III. One App
Agents MUST work only in `apps/voiceFaithfulness` unless the owner names
another app. Agents MUST NOT share secrets, catalogs, or product data with
sibling apps. Rationale: each app in freshusa-apps is a separate product.

### IV. Teach-Along (NON-NEGOTIABLE)
Before each non-trivial step (commands, edits, commits, deploys, or
multi-file design), agents MUST pause and teach in plain language:
(1) what will change, (2) why this option over named alternatives, (3) how
the component fits voiceFaithfulness. Agents MUST NOT run tools or write
files for that step until the owner replies **go**, asks a follow-up, or
explicitly skips Teach-Along for that step. Rationale: this app is also a
learning vehicle; Ask First is permission, Teach-Along is understanding.

### V. Faithfulness Pipeline (NON-NEGOTIABLE)
Every scored recording MUST follow this ordered pipeline and no other:
(1) ingest audio (local upload or preloaded picker), (2) produce a full
transcript via a free-tier transcription agent, (3) produce a summary of
that transcript via a free-tier summarizer, (4) score summary faithfulness
to the transcript on a 0–100 scale via a slightly stronger free-tier judge
model (LLM-as-judge), (5) contribute that score to the overall aggregate
percentage shown on the dashboard. Agents MUST NOT judge faithfulness
directly against raw audio when a transcript exists, invent scores, or skip
stages. Rationale: the transcript is the text bridge; the judge measures
summary fidelity to that bridge, which is the pedagogical core of the app.

### VI. All-Ages Content (NON-NEGOTIABLE)
All preloaded conversations, demo audio, transcripts, summaries, and
in-product teaching copy MUST be acceptable for all ages. Agents MUST NOT
add adult, violent, hateful, or otherwise restricted material. Owner-
supplied local uploads that violate this policy MUST be rejected or blocked
from scoring with a clear UI message. Rationale: educational demo usable
without content warnings.

### VII. Free-Tier First
v1 MUST prefer free-tier (or local/no-cost) transcription, summarization,
and judge models. Agents MUST NOT add paid APIs, paid hosting, custom
domains, analytics vendors, or paid model tiers unless the owner unlocks
them. When a free-tier limit is hit, the app MUST degrade gracefully with
an explicit user-visible message rather than silently failing. Rationale:
keep the learning project runnable without a bill.

### VIII. Test-Driven Development (NON-NEGOTIABLE)
All application development MUST follow TDD: write a failing test first,
implement the minimum to pass, then refactor. UI capabilities and backend
pipeline/API capabilities MUST both have automated coverage under the
locked Gherkin + Playwright stack. Agents MUST NOT ship behavior with no
automated coverage under that stack. Rationale: pipeline and dashboard
regressions must stay reviewable as stages grow.

### IX. Figma First UI (NON-NEGOTIABLE)
Agents MUST NOT implement user-facing screens or styled UI components until
approved frames exist in a Figma **design file** and matching entries exist
in `contracts/ui-design.md` with `Review: approved`. FigJam is process
only; design files are the visual source of truth. Rationale: single-page
dashboard needs a reviewable visual contract before code.

### X. Teach-in-UI
The single-page web app MUST surface short, plain-language messages that
explain concepts and process stages (ingest → transcript → summary →
judge → aggregate) as the user works. Agents MUST NOT ship a metrics-only
dashboard with no educational messaging. Rationale: the product teaches
LLM-as-judge while it runs it.

### XI. Elegant UI (NON-NEGOTIABLE)
The single-page web app MUST be designed with an elegant, minimalistic aesthetic. 
Agents MUST NOT ship a dashboard with a cluttered, busy, or overly complex UI. 
The UI must be simple and clean, with a focus on the learning.
The UI must be responsive and mobile-friendly.
Rationale: the product is a learning tool that displays the kind of work I have done in the past 
A clean, simple UI helps the user focus on learning.
Source possible layout examples from https://www.awwwards.com/

### XII. Git Branches (NON-NEGOTIABLE)
Agents MUST create a dedicated git branch when (1) this app is initiated or
(2) a new implementation is added. Agents MUST NOT commit that work onto
`main`. Agents MUST land reviewable work as **small commits** and **push the
feature branch in chunks** (logical slices), not one mega-commit or a bulk
dump mixed with other apps. After the implementation is deployed (or otherwise
shipped and ready to land), the branch MUST be merged into `main` via pull
request. Branch naming SHOULD use `voiceFaithfulness/<track>` (e.g.
`voiceFaithfulness/v1`). Rationale: matches monorepo AGENTS.md; keeps shipped
`main` separate from in-progress learning demos and keeps reviews tractable.

## Product Constraints

- Product name: voiceFaithfulness.
- App path: `/Users/khalilshakir/workspace/apps/voiceFaithfulness` in the
  `freshusa-apps` monorepo.
- Spec Kit is required. Extensions `bug` and `assess` MUST remain installed.
- **Product shape**: single-page web app with recording picker (local +
  preloaded), pipeline status, per-recording faithfulness scores, overall
  aggregate percentage, and educational messages.
- **Preloaded audio**: approximately 10 AI-generated voice recordings,
  about 3 minutes each, all-ages topics only.
- **Stack (locked for v1)**:
  - **Backend / data**: Python; PyTorch and pandas for scoring support and
    metrics aggregation as justified in plan/spec.
  - **Web UI**: single-page application (concrete framework chosen in plan).
  - **Acceptance tests**: Gherkin feature files + Playwright (UI and
    backend/API capabilities).
- **UI contracts**: functional behavior in feature specs / Gherkin; visual
  contract in `contracts/ui-design.md` (Figma file URL + node URLs);
  scaffold from monorepo `templates/spec-ui-design/` after `/speckit-plan`.
- **Providers**: concrete free-tier STT, summarizer, and judge model IDs
  MUST be locked in the feature plan; constitution requires free-tier
  preference but does not invent vendor names.
- TODO(PROVIDERS): Locked in `specs/001-llm-judge-dashboard/research.md` (Groq Whisper + local Faster-Whisper; Groq Llama 8B summarizer; Groq 70B/Scout/GPT-OSS judges).

## Development Workflow

- Feature work lives under `specs/`. Assess artifacts (when used) live
  under `.specify/assessments/<slug>/`.
- After `/speckit-plan`, complete the **UI/UX foundation phase** before
  story UI: Figma frames → node URLs in `ui-design.md` → owner
  `Review: approved` → then UI implementation tasks.
- Agents MUST keep `spec-architecture.png` aligned with Spec Kit
  artifacts. When files or dependencies change, update
  `spec-architecture.mmd` and `spec-architecture.html`, then run
  `node render-spec-architecture.mjs` from `apps/voiceFaithfulness`
  (unset sandbox `PLAYWRIGHT_BROWSERS_PATH` if Chromium fails to launch).
- Run installs and tests from `apps/voiceFaithfulness`.
- Prefer small commits scoped to this app only; commit only when the owner
  asks. When landing work, **push `voiceFaithfulness/<track>` in chunks**
  (docs → scaffold → story increments) and open/update a PR into `main`.
  Do not push unrelated monorepo apps in the same chunk.

## Governance

This constitution supersedes conflicting informal practice for
voiceFaithfulness. Amendments MUST update this file, bump
**Version** (MAJOR for incompatible principle changes, MINOR for new
principles/sections, PATCH for clarifications), set **Last Amended** to
the amendment date (ISO YYYY-MM-DD), and record a Sync Impact Report HTML
comment at the top. PRs and agent work MUST be reviewable against these
principles. Complexity beyond the single-page free-tier demo MUST be
justified in the feature plan or rejected.

**Version**: 1.2.2 | **Ratified**: 2026-09-08 | **Last Amended**: 2026-09-08
