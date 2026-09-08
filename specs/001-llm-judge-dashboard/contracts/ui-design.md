# UI Design Contract: LLM Judge Faithfulness Dashboard

**Feature**: `001-llm-judge-dashboard`  
**Date**: 2026-09-08  
**Functional contract**: [ui-behavior.md](./ui-behavior.md)  
**Visual source of truth**: Figma **design file** (not FigJam)  
**Inspiration**: Elegant/minimal references may be sourced from https://www.awwwards.com/ (inspiration only — Figma frames remain the pixel spec)

## Figma file

| Field | Value |
|-------|-------|
| Design file URL | https://www.figma.com/design/KzdHLMsPOiKVCTKhznVeHI |
| File name | voiceFaithfulness — Faithfulness Dashboard |
| File key | `KzdHLMsPOiKVCTKhznVeHI` |

## Review

| Field | Value |
|-------|-------|
| Status | approved |
| Reviewed by | Owner |
| Date | 2026-09-08 |

**Gate:** Owner approved UI implementation on 2026-09-08 despite missing Figma node URLs, because **Figma MCP Starter rate limits** blocked frame generation. Visual direction in this file (teal accent, cool mist background, brand-first SPA regions in ui-behavior) is the interim pixel guidance. Prefer filling node URLs later when MCP quota returns; do not re-block backend/UI work on TBD nodes.

**Session note (2026-09-08):** File created at URL above. Frames not auto-drawn (MCP limit). Owner waiver unlocks story UI tasks.

## Frame matrix

| Screen ID | Story | Surface | Frame name | Node URL | States |
|-----------|-------|---------|------------|----------|--------|
| spa-empty | 1,6 | web | SPA — empty / no scores | TBD | default, mobile |
| spa-ready | 1–3 | web | SPA — recording + agents selected | TBD | default, mobile |
| spa-running | 1,5 | web | SPA — pipeline running + teaching | TBD | transcript, summary, judge |
| spa-complete | 1,6 | web | SPA — scores + overall + graph | TBD | bars view, overall view |
| spa-error | 7 | web | SPA — rate limit / policy error | TBD | rate_limited, all_ages_blocked |

### testID convention

| Screen ID | testID prefix |
|-----------|---------------|
| spa-* | `vf` (e.g. `vf-recording-picker`, `vf-agent-stt`, `vf-agent-judge`, `vf-run`, `vf-stages`, `vf-overall`, `vf-scores`, `vf-graph`, `vf-teach`, `vf-error`) |

## Design direction (for manual or later MCP fill)

Avoid purple gradients, cream+terracotta defaults, and broadsheet layouts.

| Token | Proposed value | Usage |
|-------|----------------|-------|
| color.primary / accent | `#0F6B5C` (deep teal) | Run CTA |
| color.background | `#E8EEF2` (cool mist) | Page atmosphere |
| color.surface | `#F7FAFC` | Interactive panels if needed |
| color.text | `#1A242E` | Body / brand |
| color.textMuted | `#5A6A7A` | Teaching secondary |
| color.danger | `#9B2C2C` | Error banner |
| font.family | Prefer expressive display + clean body (not Inter-only in final; Inter OK as interim) | Brand + UI |
| spacing.unit | 8 | Base |
| Brand | **voiceFaithfulness** as hero-level identity on first viewport | Constitution XI |

## Layout regions to draw (from ui-behavior)

1. Brand / title (hero-level product name)  
2. Ingest: preloaded picker + local upload  
3. Agents: STT drop-down + judge drop-down  
4. Run control  
5. Pipeline stage status  
6. Teaching message region  
7. Score list + overall %  
8. Graph view selector (≥2 views)

## Out of scope (frames)

- Multi-page marketing site  
- Account / settings screens  
- Summarizer picker UI  

## Links

- Functional UI: [ui-behavior.md](./ui-behavior.md)
- API: [api.md](./api.md)
