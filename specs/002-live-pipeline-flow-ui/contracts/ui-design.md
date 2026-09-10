# UI Design Contract: Live Pipeline Learning Flow

**Feature**: `002-live-pipeline-flow-ui`  
**Date**: 2026-09-09  
**Functional contract**: [ui-behavior.md](./ui-behavior.md)  
**Visual source of truth**: Figma **design file** (not FigJam)

## Figma file

| Field | Value |
|-------|-------|
| Design file URL | TBD |
| File name | voiceFaithfulness — live pipeline flow (v1.1) |

## Review

| Field | Value |
|-------|-------|
| Status | approved |
| Reviewed by | Owner |
| Date | 2026-09-09 |

**Gate:** Owner approved UI implementation on 2026-09-09 despite missing Figma node URLs (same waiver pattern as 001). Visual direction: reuse 001 theme tokens; ui-behavior.md is the interaction contract for flow layout, history, rationale reveal, and demo reset. Prefer filling node URLs later when Figma/MCP quota allows; do not re-block story UI on TBD nodes.

## Frame matrix

| Screen ID | Story | Surface | Frame name | Node URL | States |
|-----------|-------|---------|------------|----------|--------|
| VF-FLOW-DESKTOP | US6 | web | Desktop LTR pipeline flow | TBD | default, with-history, stub-banner |
| VF-FLOW-MOBILE | US6 | web | Mobile vertical pipeline flow | TBD | default |
| VF-RATIONALE | US3 | web | Summary + rationale reveal | TBD | hover/open, empty-rationale |
| VF-HISTORY | US4 | web | Session history comparison | TBD | multi-run |
| VF-RESET | US7 | web | Clear demo data confirm | TBD | confirm |

### testID convention

Map each `Screen ID` to a stable `testID` prefix for Gherkin/Playwright/Detox (e.g. `browse`, `listing-detail`).

| Screen ID | testID prefix |
|-----------|---------------|
| VF-FLOW-DESKTOP | vf-flow-desktop |
| VF-FLOW-MOBILE | vf-flow-mobile |
| VF-RATIONALE | vf-rationale |
| VF-HISTORY | vf-history |
| VF-RESET | vf-demo-reset |

## Design tokens

Reuse 001 SPA theme where possible; refine from Figma when frames land.

| Token | Value | Usage |
|-------|-------|-------|
| color.primary | TBD (reuse 001) | CTAs, links |
| color.background | TBD (reuse 001) | Page background |
| color.surface | TBD | Panels |
| color.text | TBD (reuse 001) | Body text |
| color.textMuted | TBD (reuse 001) | Secondary text |
| font.family | TBD (reuse 001) | Brand typography |
| spacing.unit | TBD (reuse 001) | Base spacing |

## Out of scope (frames)

- Separate mobile native apps
- Concurrent side-by-side compare canvas
- Admin / settings pages

## Links

- Functional UI: [ui-behavior.md](./ui-behavior.md)
- Spec: [../spec.md](../spec.md)
