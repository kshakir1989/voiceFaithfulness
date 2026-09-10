# UI Design Contract: [FEATURE NAME]

**Feature**: `[###-feature-name]`  
**Date**: [DATE]  
**Functional contract**: [ui-behavior.md](./ui-behavior.md)  
**Visual source of truth**: Figma **design file** (not FigJam)

## Figma file

| Field | Value |
|-------|-------|
| Design file URL | TBD |
| File name | TBD |

## Review

| Field | Value |
|-------|-------|
| Status | draft |
| Reviewed by | |
| Date | |

**Gate:** Story UI implementation MUST NOT start until `Status: approved` and every in-scope frame has a node URL.

## Frame matrix

| Screen ID | Story | Surface | Frame name | Node URL | States |
|-----------|-------|---------|------------|----------|--------|
| | | web / iOS / Android | | TBD | default |

### testID convention

Map each `Screen ID` to a stable `testID` prefix for Gherkin/Playwright/Detox (e.g. `browse`, `listing-detail`).

| Screen ID | testID prefix |
|-----------|---------------|
| | |

## Design tokens

Fill from Figma variables or manual table; consumed by `src/ui/theme.ts` at implement time.

| Token | Value | Usage |
|-------|-------|-------|
| color.primary | TBD | CTAs, links |
| color.background | TBD | Page background |
| color.surface | TBD | Cards, panels |
| color.text | TBD | Body text |
| color.textMuted | TBD | Secondary text |
| font.family | TBD | System or brand |
| font.size.body | TBD | Body |
| font.size.heading | TBD | Titles |
| spacing.unit | TBD | Base spacing (e.g. 8) |
| radius.card | TBD | Listing cards |

## Out of scope (frames)

- [List screens explicitly excluded from this increment]

## Links

- Functional UI: [ui-behavior.md](./ui-behavior.md)
- Testing: [testing.md](./testing.md)
