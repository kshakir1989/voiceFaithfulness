---
description: "Scan recent Cursor agent transcripts, write a dream proposal, and auto-apply learnings-bound candidates"
---

# Dream (propose + auto-apply learnings)

Consolidate recent agent session history into durable memory for **this Spec Kit
app** (the project root that contains `.specify/`).

This command **reads** transcripts and existing Spec Kit memory. It **writes**:

1. `.specify/memory/dreams/<run>/sources.md` and `proposal.md` (always kept as the audit trail)
2. Auto-appends all eligible `learnings`-bound candidates into `.specify/memory/learnings.md`
3. Auto-promotes **portable** process learnings into the workspace shared kit
   `agent-kit/LEARNINGS.md` (see **Shared agent-kit promotion** below)
4. `dreams/<run>/apply.md` recording what was auto-applied (app + kit)

It MUST NOT edit `constitution.md`, application source, or catalog/product data.
It MUST NOT copy product-specific facts into `agent-kit/`.

Downstream: `__SPECKIT_COMMAND_DREAM_APPLY__` is only for rare re-apply /
manual subset overrides — normal dreams auto-apply in this command.

## User Input

```text
$ARGUMENTS
```

Optional arguments (any subset):

- `run=<id>` — kebab-case run folder name. Default: `dream-YYYYMMDD-HHMM` (local time).
- `since=<days>` — only consider transcripts modified in the last N days (default `14`).
- `limit=<n>` — max transcript files to open (default `12`, hard cap `25`).
- `focus=<text>` — bias extraction toward a topic.
- `app=<name>` — filter sessions to this app. Default: the basename of the Spec Kit
  project root (e.g. `SourcedValue`, `voiceFaithfulness`, `ummahHomes`).
- `dry_run=true` — write proposal + sources only; skip auto-apply (exception path).

## Path safety

Before any mkdir/read/write:

1. Resolve the project root (the Spec Kit app root containing `.specify/`).
2. Refuse if `.specify`, `.specify/memory`, or `.specify/memory/dreams` exists as a symlink or resolves outside the project root.
3. Normalize `run` like assess/bug slugs: lowercase kebab-case; only `a-z`, `0-9`, `-`; reject empty/unsafe values.
4. Set `DREAM_DIR = .specify/memory/dreams/<run>`. Never overwrite an existing `proposal.md` without asking (interactive) or picking a new run id (automated).

## Transcript source (Cursor)

Locate agent transcripts for this workspace:

1. Prefer
   `~/.cursor/projects/<cursor-project-id>/agent-transcripts/**/*.jsonl`
   where `<cursor-project-id>` matches the open workspace (for the freshusa-apps
   monorepo checkout that is typically `Users-khalilshakir-workspace`).
2. If that path is missing, search `~/.cursor/projects/*/agent-transcripts/` for
   the project whose path maps to this repo; if still ambiguous, **stop** and
   report the candidates in `proposal.md` — do not guess across unrelated projects.
3. Each transcript is JSONL. Lines are events with `role` (`user` / `assistant`)
   and message text. Prefer user corrections, explicit preferences, repeated
   failures, and durable project facts. Prefer summarizing over dumping tool
   payloads. Skip empty or pure tool-trace noise.

**Scope filter:** Prefer sessions that mention this app’s folder name
(`apps/<app>`), product name, or constitution/spec work for this app. If a
session is clearly another app only, skip it and list it under **Skipped** in
`sources.md`.

## What to extract

Produce candidate memory items. Each item MUST have:

| Field | Meaning |
|-------|---------|
| `kind` | `preference` \| `mistake` \| `project-fact` \| `process` |
| `summary` | One sentence, actionable for a future agent |
| `evidence` | Short quote or paraphrase + transcript uuid (no secrets) |
| `suggests` | `learnings` (default) \| `constitution` (rare — propose text only, never auto-apply) |
| `confidence` | `high` \| `medium` \| `low` |

**Do not extract:** one-off task status, transient file paths, secrets, or
invented product facts. Never launder guesses into memory.

**Deduplicate** against existing `.specify/memory/constitution.md` and
`.specify/memory/learnings.md`. Mark overlaps as `already-covered` and omit
from auto-apply.

## Fail-closed

Stop and write a short `proposal.md` explaining why, with **no candidate
accept list** and **no learnings edit**, when:

- No readable transcripts in range
- Parse failure on all candidates
- Nothing durable enough at `medium`+ confidence
- Focus filter yields zero relevant sessions

Never invent session content to fill a proposal.

## Auto-apply rules (default)

Unless `dry_run=true`, after writing `proposal.md`:

1. Auto-accept every candidate that is `suggests: learnings` and confidence
   `high` or `medium` (skip `low`, `already-covered`, and rejected).
2. Skip any `suggests: constitution` — list under **Skipped (constitution)** in
   `apply.md`; never write `constitution.md`.
3. Ensure `.specify/memory/learnings.md` exists (create with the standard header
   if missing).
4. Append a dated section for this run with one bullet per auto-accepted item.
5. Run **Shared agent-kit promotion** for portable subset.
6. Write `DREAM_DIR/apply.md` with `Mode: auto-approved` (include kit paths).
7. Set proposal status to **auto-applied**.

## Shared agent-kit promotion

Resolve kit root (first match):

1. `$AGENT_KIT` if it contains `PROMPT.md`
2. Git toplevel `agent-kit/` if that directory contains `PROMPT.md`
3. `$PAYDAY_AGENT_KIT` if it contains `PROMPT.md`

If none exist, note **kit skipped (missing)** in `apply.md` and continue (do not fail the dream).

For each auto-accepted candidate that is `kind: preference|process|mistake`
(or process-shaped `project-fact` that generalizes):

1. Rewrite `summary` to remove app/brand names, private paths, secrets, URLs,
   catalogs, and one-off task status. If rewrite is impossible, skip.
2. Deduplicate against existing `agent-kit/LEARNINGS.md`.
3. Append under:

   ```markdown
   ## Dream promote — <ISO date> — <run>

   - <portable summary> _(kind, confidence)_
   ```

4. Follow `agent-kit/skills/qa-dream-promote/SKILL.md` when present.
5. **Never** auto-edit `agent-kit/PROMPT.md` hard rules. List any suggested
   PROMPT deltas under **Proposed PROMPT deltas** in `apply.md` for owner review.

## Execution

1. Resolve `run`, `since`, `limit`, `focus`, `app`, `dry_run`. Create `DREAM_DIR`.
2. List transcript files by mtime; take up to `limit` within `since`.
3. Read and skim each selected file (targeted search for corrections /
   preferences / app keywords — do not load megabyte tool dumps wholesale).
4. Draft candidates; dedupe against current memory files.
5. Write `DREAM_DIR/sources.md` — files considered, skipped, and why.
6. Write `DREAM_DIR/proposal.md` using the template below.
7. Unless `dry_run=true`, auto-apply per **Auto-apply rules** (app learnings +
   kit promotion) and write `apply.md`.
8. Tell the owner the dream folder path, that app learnings were updated, and
   whether portable bullets were promoted to `agent-kit/LEARNINGS.md`
   (or that dry_run / missing kit skipped apply).

## proposal.md template

```markdown
# Dream proposal — <run>

- Date: <ISO date>
- App: <app name>
- Window: last <since> days, limit <n>
- Focus: <focus or none>
- Status: **auto-applied** | **proposal only (dry_run)** | **fail-closed (nothing applied)**

## Summary

<2–4 sentences: what patterns showed up>

## Candidates

### 1. <short title>
- kind: …
- confidence: …
- suggests: learnings | constitution
- summary: …
- evidence: … (transcript <uuid>)

### 2. …

## Already covered

- …

## Rejected / low confidence

- …

## Apply

Learnings-bound medium+ candidates are **auto-applied** to
`.specify/memory/learnings.md` unless this run is `dry_run` or fail-closed.
Portable process bullets are also promoted to `agent-kit/LEARNINGS.md` when
the kit is present. See `apply.md`. Constitution-bound items and PROMPT hard
rules are never auto-written.
```

## sources.md template

```markdown
# Dream sources — <run>

| Transcript | mtime | Used? | Notes |
|------------|-------|-------|-------|
| <uuid> | … | yes/no | … |
```
