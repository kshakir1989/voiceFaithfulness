# voiceFaithfulness

Single-page learning demo: audio → transcript (chosen free-tier STT) → summary → LLM-as-judge faithfulness score → dashboard aggregate.

**Current implementation branch:** `voiceFaithfulness_1.1` (branch from `main`; land via PR into `main`)  
**UI baseline on `main`:** editorial SPA matching the [portfolio walkthrough](https://www.khalil-shakir.com/videos/voice-faithfulness.mp4) (5-stage LTR board, Desktop · LTR / Mobile · stack)  
**Specs:** `specs/001-llm-judge-dashboard/` · `specs/002-live-pipeline-flow-ui/`

Paths below are from **this repo root**. In the freshusa-apps index that is `apps/voiceFaithfulness/`.

---

## Prerequisites

- Python 3.9+ (3.12+ preferred)
- Node 20+
- Optional keys in `backend/.env` (from `.env.example`): `GROQ_API_KEY`, `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY`
- Without keys (or for a quick demo): `FORCE_MOCK_PROVIDERS=1` for stub STT / summary / judge

---

## Spec Kit workflow — implementing a new update

Use this whenever you add or change product behavior (not for typo-only docs). Agents follow Teach-Along and chunk = commit + push on the implementation branch (`voiceFaithfulness_1.1` or a newer track). Do **not** push feature work straight to `main`.

### 0. Branch

```bash
git checkout main && git pull
git checkout voiceFaithfulness_1.1   # or: git checkout -b voiceFaithfulness_<version>
```

Keep the working tree clean between chunks. Never commit `backend/.env` or `plan.md`.

### 1. Assess (when the change is ambiguous or large)

Prefer assess before specify when the constitution / overlay says so:

`/speckit-assess-intake` → research → define → shape → decide → **go** verdict  

Artifacts (when used): `.specify/assessments/<slug>/`.

### 2. Specify → plan → tasks

| Step | Command / artifact | Notes |
|------|-------------------|--------|
| Specify | `/speckit-specify` | Feature under `specs/<###-slug>/` |
| Clarify | `/speckit-clarify` if needed | |
| Plan | `/speckit-plan` | Produces plan + contracts (incl. `ui-behavior.md`) |
| Tasks | `/speckit-tasks` | Story breakdown |

Constitution: `.specify/memory/constitution.md`. Gherkin living docs: `features/*.feature`.

### 3. UI / UX foundation (before story UI code)

After plan has `contracts/ui-behavior.md`:

1. Scaffold `contracts/ui-design.md` (from freshusa-apps `templates/spec-ui-design/` if needed).
2. **Figma gate:** design file frames + node URLs in `ui-design.md`; owner sets `Review: approved` (or records a waiver).
3. PRs that touch UI cite Figma **node URL**s when frames exist.

FigJam = process only. Design file = visual source of truth.

### 4. When to use UI MCP (implementation)

Only **after** the Figma gate (or explicit waiver). Free tier only unless the owner opts in. Config: `.cursor/mcp.json`; 21st key in `~/.cursor/mcp.env` (`API_KEY_21ST`). Skill: `speckit-ui-mcp`.

| Order | Tool | Use for | Free-tier stop |
|-------|------|---------|----------------|
| 1 | **Figma MCP** | Draw / sync frames; `get_design_context` for design→code | Rate-limit → skip sync; note in PR; do not block domain/tests |
| 2 | **shadcn MCP** | Primitives (button, alert, card, select, …) adapted to VF tokens + `data-testid`s | Private / paid registries |
| 3 | **21st MCP** | Catalog **search / inspiration**; ≤ **2 installs/day** for polish blocks | 3rd install same day; `generate` / AI credits; membership-only code |

Do **not** call 21st `generate` or burn paid retrieval on free-only sessions. If a cap hits, stop and tell the owner:

```text
Free-tier max reached for <tool>: <what failed>. Need your OK before paid/credits, or continue without that install/generate.
```

Preserve editorial tokens, brand-first layout, and existing test IDs. Prefer shadcn primitives before 21st blocks.

### 5. Implement (stories)

- Backend + API from `backend/`; SPA from `frontend/`.
- Spec first for user-facing behavior.
- After each reviewable chunk: **commit + `git push`** on the implementation branch.

### 6. Architecture / Archify documentation (required when structure changes)

When Spec Kit artifacts, providers, UI surfaces, or dependencies change, keep architecture docs in sync **in the same update** (or the next immediate chunk)—do not leave diagrams stale.

**In-repo Spec Kit diagram (always):**

| File | Role |
|------|------|
| `spec-architecture.mmd` | Mermaid source — edit this |
| `spec-architecture.html` | HTML preview used to render the PNG |
| `spec-architecture.png` | Committed diagram agents/PRs must keep current |
| `render-spec-architecture.mjs` | Regenerates the PNG |

```bash
# From voiceFaithfulness repo root
# 1) Edit spec-architecture.mmd (+ Mermaid block in spec-architecture.html)
# 2) Render:
node render-spec-architecture.mjs
```

If Chromium fails under a sandbox, unset `PLAYWRIGHT_BROWSERS_PATH` and retry. Playwright may resolve from this app or a sibling install (see script comments).

**Archify (portfolio / guided architecture map):**

- Source of truth for the interactive Archify map used on [khalil-shakir.com](https://khalil-shakir.com) (voiceFaithfulness work entry) lives with the product docs / export used for portfolio (`docs/archify/` when present, or the Archify HTML exported for the personal site).
- After architecture changes that affect the lesson path (learner → SPA → API → STT / summary / judge → metrics, providers, Spec Kit / Playwright):
  1. Update the in-repo `spec-architecture.*` as above.
  2. **Refresh the Archify HTML** so guided views still match the product.
  3. If the portfolio should show the new map, sync the Archify asset into the personal site (`apps/khalil-shakir.com/public/archify/…`) in a **separate** personal-site session/PR—do not edit that repo in the same voiceFaithfulness session.

### 7. Verify

```bash
cd backend && source .venv/bin/activate && FORCE_MOCK_PROVIDERS=1 pytest
cd frontend && npm run test:e2e
```

### 8. Ship

Open a PR from `voiceFaithfulness_1.1` (or your track) into **`main`**. Merge when ready. Optionally re-record the portfolio walkthrough (`frontend/scripts/record-portfolio-walkthrough.mjs`) after major UI changes.

---

## Run locally

You need **two processes**:

| Process | Port | Role |
|---------|------|------|
| FastAPI (`uvicorn`) | **8000** | API only — `/` is a hint page, not the app |
| Vite (`npm run dev`) | **5173** | SPA — **open this URL** |

Vite proxies `/api` → `http://127.0.0.1:8000`.

### 1. One-time setup

```bash
# From voiceFaithfulness repo root

cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # optional: add GROQ_API_KEY=

cd ../frontend
npm install
```

If `source .venv/bin/activate` fails, create the venv first. If `uvicorn: command not found`, activate the venv and reinstall requirements.

### 2. Start the API (terminal A)

```bash
cd backend
source .venv/bin/activate
export FORCE_MOCK_PROVIDERS=1      # recommended until you have a Groq key
uvicorn app.main:app --reload --port 8000
```

Health: http://127.0.0.1:8000/api/health → `{"status":"ok"}`

### 3. Start the SPA (terminal B)

```bash
cd frontend
npm run dev
```

### 4. Open the app

**http://127.0.0.1:5173/** — do **not** use port 8000 as the app URL.

### First-run checklist

1. Confirm stub/live mode; ~10 preloaded recordings (+ blocked demo).
2. Confirm Desktop · LTR shows five stage columns; Mobile · stack stacks them.
3. Preview audio; **Run pipeline** → stage board + detail panel.
4. Open judge rationale / why-improve when a score exists; check graphs.
5. Run again with another agent; compare history / graph views.
6. **Clear demo** resets runs / scores / uploads; preloads remain.

---

## Tests

```bash
cd backend && source .venv/bin/activate && FORCE_MOCK_PROVIDERS=1 pytest
cd frontend && npm run test:e2e
cd frontend && npm run test:coverage
cd frontend && npm run test:qaiq
```

`test:coverage` runs the same Playwright e2e suite with Chromium V8 coverage via Monocart (report-only). Open `frontend/coverage/index.html` or `frontend/coverage/lcov.info`. Filtered to `src/`.

`test:qaiq` is Playwright suite hygiene (QAIQ, report-only). A high score means tests are well-*written*, not that the product is well-*tested*. Cursor MCP `qaiq` is in `~/.cursor/mcp.json`. From repo root: `npm run test:qaiq`.

Gherkin in `features/*.feature` is living documentation. Executable UI coverage is Playwright in `frontend/e2e/`. Without `GROQ_API_KEY` (or with `FORCE_MOCK_PROVIDERS=1`), providers use mocks — the SPA shows **Stub mode** and marks dashboard percentages as stubbed.

**Uploads:** session-only (`vf_session` cookie) under `data/uploads/sessions/`; cleared on tab close / `DELETE /api/recordings/session`. Preloaded demos (including **[Blocked demo]**) always remain in the picker.

---

## Preloaded audio

Titles + paths: `data/preloaded/manifest.json`. All-ages spoken demos (~3 minutes each) via macOS TTS:

```bash
# From voiceFaithfulness repo root
python3 scripts/generate-preloaded-audio.py
```
