# Spec UI design scaffold

Figma-first UI/UX gate for Spec Kit features and all freshusa-apps products.

## When to use

After `/speckit-plan` produces `contracts/ui-behavior.md` (functional UI contract), scaffold `contracts/ui-design.md` from this template. Complete the **UI/UX foundation phase** before any story UI implementation.

## Gate rules

1. **Figma design file** (not FigJam) holds pixel frames for each screen.
2. Record the file URL and per-frame **node URLs** in `contracts/ui-design.md`.
3. Owner sets `Review: approved` in ui-design.md before Expo/UI code for those screens.
4. PRs that touch UI cite the Figma node URL for each changed screen.
5. **FigJam** = process only; **design files** = visual source of truth.

## Install into a feature

From monorepo root:

```bash
mkdir -p apps/<app>/specs/<feature>/contracts
cp templates/spec-ui-design/ui-design-template.md \
  apps/<app>/specs/<feature>/contracts/ui-design.md
```

Or let `/speckit-plan` copy the template during Phase 1 design.

## Figma MCP (agents)

- Load Figma MCP when drawing mockups or syncing frames.
- **Design → code:** `get_design_context` on a node URL; adapt to the app stack (do not paste Figma CSS as RN).
- **Code → design:** `use_figma` / `generate_figma_design`; `search_design_system` first if a library exists.
- **Rate limit:** If Figma MCP returns rate-limit, skip Figma sync for that session; do not block domain/tests work. Note “Figma sync skipped (MCP limit)” in PR notes.

## Reference

`$Value` documents App Store + screenshot specifics in `apps/value/store/release-flow.md`. All apps share the same **Figma-first gate**; app-specific release steps stay in each app’s store/release docs.

## Files

| File | Purpose |
|------|---------|
| `ui-design-template.md` | Copy to `specs/<feature>/contracts/ui-design.md` |
