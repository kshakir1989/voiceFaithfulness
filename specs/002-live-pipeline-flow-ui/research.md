# Research: Live Pipeline Learning Flow

**Feature**: `002-live-pipeline-flow-ui`  
**Date**: 2026-09-09  
**Spec**: [spec.md](./spec.md)

## 1. Scope relative to 001

**Decision**: Evolve the existing FastAPI + Vite/React SPA on branch `voiceFaithfulness/v1.1`. Do not rewrite the app.

**Rationale**: Spec Assumptions; medium appetite Option B; most pipeline plumbing exists (stub/live, STT/judge catalogs, transcript/summary panels, aggregate).

**Alternatives considered**: Greenfield rewrite (rejected — cost); amend only 001 docs without a new feature folder (rejected — Spec Kit feature track needs `002`).

## 2. Top five free-tier STT agents (learner catalog)

**Decision** — five learner-visible transcription agents. Each agent **owns** transcript + summary for the run (amends 001 FR-017). STT-only vendors attach a free-tier summarizer behind the same agent ID (facade).

| # | ID | Label | STT backend | Summary ownership |
|---|----|-------|-------------|-------------------|
| 1 | `groq-whisper-large-v3-turbo` | Groq Whisper Large v3 Turbo | Groq Audio Transcriptions | Groq chat summarizer attached to this agent ID |
| 2 | `groq-whisper-large-v3` | Groq Whisper Large v3 | Groq Audio Transcriptions | Same pattern (may use distinct summary model/prompt per agent for quality variance) |
| 3 | `local-faster-whisper` | Local Faster-Whisper | On-device `faster-whisper` | Attached free-tier summarizer when key present; otherwise fail honestly in live mode / mock in stub |
| 4 | `deepgram-nova-3` | Deepgram Nova-3 | Deepgram pre-recorded STT (signup credit) | Attached free-tier summarizer (Groq or Deepgram LLM if available under free path) |
| 5 | `assemblyai-universal` | AssemblyAI Universal | AssemblyAI STT (signup credit) | Prefer AssemblyAI summary/LeMUR when free-path allows; else attached free-tier summarizer |

**Default**: keep `groq-whisper-large-v3-turbo`.

**Rationale**: Matches “top five free STT” ask. Groq = true no-card free tier; Deepgram (~$200 credit) and AssemblyAI (~$50 credit) are widely cited free-path Whisper-class hosts; local Whisper satisfies Free-Tier First offline. AssemblyAI is the only one of the five with a strong native “summary in product” story; others use an attached summarizer so the **agent still owns** both artifacts in the UI and run record.

**Alternatives considered**: OpenAI Whisper paid API only (weaker free story); HF Inference-only catalog (less predictable for ~3‑min clips); five Groq Whisper variants only (fails multi-vendor comparison lesson).

**Keys**: `GROQ_API_KEY` (required for Groq live + attached summaries); `DEEPGRAM_API_KEY`; `ASSEMBLYAI_API_KEY`. Missing vendor key → that agent `available: false` with clear message. Stub mode remains when forced or no live path.

## 3. Summary ownership (FR-017 amend)

**Decision**: Drop product-fixed `SUMMARIZER_ID` as the sole summarizer. Persist `summary.agent_id` (or `transcription_agent_id`) on the summary artifact. UI shows one transcription drop-down; no separate summarizer drop-down unless a later feature adds one.

**Rationale**: Spec FR-004 / assess Option B.

**Alternatives considered**: Keep fixed summarizer + only vary STT (rejected — owner clarified transcription agent produces summary); third drop-down for summarizer (rejected — out of Option B sketch).

## 4. Judge highlight (“more powerful”)

**Decision**: Catalog field `power_tier`: integer (higher = more powerful). UI highlights judges with `power_tier` above a threshold (e.g. ≥ the default strong judge, or absolute `power_tier >= 2`). Any available judge remains selectable.

**Suggested tiers**:

| ID | power_tier |
|----|------------|
| `groq-gpt-oss-20b` | 1 |
| `groq-llama-4-scout` | 2 |
| `groq-llama-3.3-70b-versatile` | 3 |

**Rationale**: Spec FR-006; simple attribute without dynamic pairing math.

**Alternatives considered**: Dynamic “stronger than STT” pairing (complex); hide weak judges (blocks exploration).

## 5. Rationale UX

**Decision**: Backend already returns `score.rationale`. SPA reveals it on summary hover (desktop) plus an accessible control (e.g. focusable “Why this score?”). Raw text first; optional light formatting if the judge returns `SCORE=` lines — no requirement for full criteria parsing in v1.1.

**Rationale**: Spec FR-008 / SC-003; problem.md tooltip clarification.

**Alternatives considered**: Always-visible rationale panel only (clutters flow); structured rubric parser (rabbit hole).

## 6. Session history

**Decision**: Use existing `GET /runs` (or extend) to list session runs newest-first; SPA keeps a history panel fed from API after each run and on load. In-memory store is enough for demo (no durable cross-session DB requirement for this feature). Optionally persist runs to SQLite later without changing the contract shape.

**Rationale**: Spec FR-009; store already has `list_runs`.

**Alternatives considered**: Client-only history (lost on refresh mid-demo); full SQLite-first rewrite (scope creep).

## 7. Demo reset

**Decision**: New authenticated-by-session endpoint e.g. `DELETE /api/demo/session` (or extend recordings session delete) that clears: in-memory runs, scores, ephemeral uploads; **does not** delete preloaded recordings/manifest. Expose a clear control in the SPA.

**Rationale**: Spec FR-013 / Story 7.

**Alternatives considered**: Reuse only `POST /api/dev/reset` (too broad / dev-only); clear scores only (leaves uploads confusing).

## 8. Layout: desktop LTR / mobile vertical + toggle

**Decision**: CSS layout modes `desktop-flow` (horizontal stage/result columns) vs `mobile-stack` (vertical). Explicit toggle overrides auto viewport detection; default follows viewport width. Persist mode in `sessionStorage` for the tab.

**Rationale**: Spec FR-012; explicit toggle required even when viewport already implies a mode.

**Alternatives considered**: Responsive-only without toggle (fails FR-012); separate mobile app (out of scope).

## 9. API contract deltas vs 001

**Decision**: Document additive changes in `contracts/api.md`: rationale on score; summary attributed to transcription agent; runs list for history; demo session clear; agent catalog fields `power_tier` / availability; optional `providers_mode` already present.

**Rationale**: Keep OpenAPI-aligned contract as source of truth for implement + tests.

## 10. Testing

**Decision**: Extend Gherkin (docs) + Playwright e2e + pytest. Mock Deepgram/AssemblyAI/Groq in CI; live smoke optional when keys present. Cover: live/stub banners, summary attribution, rationale reveal, history after two runs, judge highlight, layout toggle, demo clear.

**Rationale**: Constitution TDD / Gherkin+Playwright.

## 11. UI design gate

**Decision**: Refresh `contracts/ui-design.md` for 002 (or copy template into 002 contracts) and require Figma frames for flow layout + history + rationale reveal before story UI implementation. Owner may waive MCP quota as before — document in ui-design.md.

**Rationale**: Constitution Figma First; README workflow.
