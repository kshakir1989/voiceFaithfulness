# Concept: Live pipeline learning flow

- **Slug**: live-pipeline-flow-ui
- **Created**: 2026-09-09
- **Recommended option**: Option B — Full teaching flow on v1.1

## Options

### Option A — Do nothing / keep stub demo as-is
- **Sketch**: Leave the app on stub providers and the current single-column UI. Learners keep hearing sample audio and seeing placeholder transcript/summary/score. Teaching happens via banners and outside explanation rather than a trustworthy end-to-end run.
- **Appetite**: small (decision only)
- **Trade-offs**: Wins: zero build cost, no provider-key or rate-limit risk. Sacrifices: fails the problem statement—owner cannot demo the LLM-as-judge lesson with real agent outputs, comparison, or score explainability.
- **Rabbit holes**: None for build; opportunity cost if demos stay unconvincing.

### Option B — Full teaching flow on v1.1
- **Sketch**: Continue on the v1.1 track so a learner can run live (non-stub) free-tier agents end to end: pick audio → choose a transcription agent that produces both transcript and summary → choose any judge (with stronger/more powerful models highlighted) → see score plus rationale on summary hover → retain multi-run session history for comparison → see overall aggregate → clear scores/runs/uploads while keeping preloaded demos → view the lesson as a left-to-right desktop flow or vertical mobile flow with an explicit layout toggle. Stub vs live honesty stays visible.
- **Appetite**: medium (weeks for live providers, history, rationale UX, layout modes, and demo reset—not a greenfield rewrite)
- **Trade-offs**: Wins: matches goals and success metrics (live pass, agent comparison, explainability, layout, reset). Sacrifices: more free-tier call volume and rate-limit exposure; amending the prior fixed-summarizer stance; layout toggle + history add UI complexity. Risks: “top five STT” catalog may be uneven (some STT-only); rationale quality varies by judge text.
- **Rabbit holes**: Wiring five STT vendors with keys and rate limits; treating “transcription agent owns summary” as a second product inside one agent; overbuilding layered rationale parsing beyond hover tooltip; perfect desktop/mobile preview toggle vs responsive-only; expanding reset into full product “workspace” management.

### Option C — Smallest unlock: live + rationale + history only
- **Sketch**: Turn on live providers, show score rationale (tooltip), and list prior runs in-session, but keep the fixed summarizer, keep the current vertical layout (no desktop LTR / toggle), and keep a thinner agent catalog (existing Groq/local options rather than five STT providers). Demo reset stays a simple clear of runs/scores (uploads optional).
- **Appetite**: small (days to ~1–2 weeks)
- **Trade-offs**: Wins: faster path to “not stub-only” and basic explainability. Sacrifices: weaker match to “different summaries by different agents,” flow UI goals, and top-five STT scope; comparison story remains incomplete.
- **Rabbit holes**: Temptation to bolt on layout/toggle and summarizer ownership mid-slice until it becomes Option B without an appetite check.

## Recommendation

**Option B — Full teaching flow on v1.1.** It is the only option that covers the owner’s stated goals together: live non-stub outputs, transcription agent owning transcript+summary, multi-run history, judge highlight, rationale on summary hover, overall aggregate, demo reset (keep preloads), and desktop/mobile presentation modes. Option C is the shrink path if appetite must cut; Option A fails the problem.

Keep concept-level only: no stack, schema, or task breakdown here.

## Out of Scope (for the recommended option)

- Side-by-side concurrent pipeline runs
- Production deploy, multi-user accounts, cross-session persistence beyond the demo
- Inventing scores/rationales on provider failure
- General-purpose transcription/evaluation platform ambitions
- App Store / external publish
- Deep structured-rationale productization beyond what hover/layers need for teaching (parse quality is specify-time)
- Vendor legal/branding deep-dive in assess (catalog named in specify/plan)

## Assumptions to Validate

- Owner can supply keys (or accepted free-tier access) for the target STT/summary/judge providers used in demos.
- “Top five free STT” can be researched and narrowed to a demoable set where each selected agent can produce (or be paired to produce) a summary as part of the transcription-agent role.
- “More powerful model” for judge highlight can be expressed as a simple catalog attribute without dynamic pairing logic.
- Hover tooltip for rationale is enough for SC-level explainability in v1.1; richer layered views can follow.
- Amending FR-017 so the transcription agent owns summary is accepted in the next specify pass on the v1.1 track.
- Session-scoped history + clear runs/scores/uploads (retain preloads) is enough for repeatable demos without durable DB work.
- Explicit desktop/mobile layout toggle is desired even when the viewport already suggests one mode.
