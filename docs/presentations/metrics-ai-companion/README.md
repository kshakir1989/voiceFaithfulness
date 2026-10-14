# metricsDashboard AI companion — slide presentation

Screenshot-backed deck for Spec Kit **003-ai-companion** (Option C, local).

## Open

```bash
open apps/voiceFaithfulness/docs/presentations/metrics-ai-companion/index.html
```

Arrow keys / Space to advance.

## Slides (PNG)

| File | Content |
|------|---------|
| `01-ops-console.png` | Ops console + Companion toggle |
| `02-companion-drawer.png` | Right drawer open |
| `03-fixture-answer.png` | Fixture-grounded 62.4% answer |
| `04-refusal.png` | Live/invent refusal |
| `05-architecture.png` | Archify map |

## Recapture

Companion API on `:8088`, then from metricsDashboard:

```bash
cd apps/metricsDashboard
node scripts/capture-companion-presentation.mjs
```

Writes into this folder (cross-app asset store named by owner).
