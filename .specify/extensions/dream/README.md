# Dreaming Extension (monorepo template)

Canonical Spec Kit extension for **dreaming**: session-transcript consolidation
into `.specify/memory/`.

Install into an app (from that app’s root):

```bash
specify extension add --dev ../../templates/speckit-extensions/dream --force
# nested clone at apps/<name> — adjust relative path if needed:
# specify extension add --dev /Users/khalilshakir/workspace/templates/speckit-extensions/dream --force
```

Then ensure:

```text
.specify/memory/learnings.md
.specify/memory/dreams/README.md
```

exist (create empty learnings header if missing).

## Behavior

- `/speckit.dream.propose` — write `dreams/<run>/` audit docs **and** auto-apply
  medium+ learnings-bound candidates to `learnings.md`
- Also promote **portable** process learnings to workspace
  `agent-kit/LEARNINGS.md` (company-agnostic; no product facts). See
  `agent-kit/README.md` and `agent-kit/skills/qa-dream-promote`.
- `/speckit.dream.apply` — optional override / re-apply / post-`dry_run` (same
  kit promotion rules)
- **Never** auto-edit `constitution.md` or `agent-kit/PROMPT.md` hard rules

See command markdown under `commands/` for full rules.
