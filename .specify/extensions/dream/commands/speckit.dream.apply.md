---
description: "Re-apply or manually subset a dream proposal into learnings.md (normal dreams auto-apply from propose)"
---

# Dream apply (override / re-apply)

Normal dreaming **auto-applies** learnings from `__SPECKIT_COMMAND_DREAM_PROPOSE__`.
Use this command only to:

- Re-apply after a `dry_run` propose
- Apply a **subset** the owner names explicitly
- Re-run apply after editing `proposal.md` by hand

## Hard rules

- MUST NOT edit `.specify/memory/constitution.md`. If a candidate `suggests:
  constitution`, record it under **Skipped (constitution)** in `apply.md`.
- MUST NOT invent new items that are not in `proposal.md`.
- MUST NOT apply `low` confidence items unless the owner explicitly names them
  in `accept=`.
- Redact secrets if any slipped into the proposal.
- Prefer leaving existing auto-apply history intact: if `apply.md` exists,
  append a new dated section rather than destroying prior apply records.

## User Input

```text
$ARGUMENTS
```

Required:

- `run=<id>` — which `.specify/memory/dreams/<run>/` to apply from.

Accept selection (one of):

- `accept=1,3,4` — 1-based candidate numbers from `proposal.md`
- `accept=all` — all `learnings`-bound candidates with `high` or `medium`
  confidence (still skips constitution-bound)

If `run` or accept selection is missing in interactive mode, ask once and wait.
In automated mode, stop and report what was missing.

## Path safety

Same as `__SPECKIT_COMMAND_DREAM_PROPOSE__`: refuse symlinked `.specify` ancestors;
keep all writes inside the project root under `.specify/memory/`.

Prerequisites:

- `DREAM_DIR/proposal.md` must exist.

## Execution

1. Read `proposal.md`. Parse numbered candidates.
2. Resolve the accept set. Drop invalid numbers; report them.
3. Ensure `.specify/memory/learnings.md` exists. If missing, create it with a
   short header using **this app’s display name**:

   ```markdown
   # <App> — Learnings

   Soft patterns from dreaming (auto-applied unless dry_run). Not constitution.
   Agents SHOULD prefer these when they do not conflict with constitution.md.
   ```

4. Append a dated section (skip bullets already present verbatim from this run
   if re-applying):

   ```markdown
   ## Dream <run> — <ISO date>

   - <approved summary> _(kind, confidence; source dream <run> #n)_
   ```

5. Append or write `DREAM_DIR/apply.md` recording mode (`manual-override` or
   `re-apply`), what was accepted/skipped, and the learnings path touched.
6. Update proposal status line to **auto-applied** or **manually applied** as
   appropriate.
7. Do **not** commit unless the owner asked to commit.

## apply.md template

```markdown
# Dream apply — <run>

- Date: <ISO date>
- Mode: auto-approved | manual-override | re-apply
- Accepted: <list>
- Skipped (constitution): <list>
- Skipped (other): <list>
- Updated: .specify/memory/learnings.md
```
