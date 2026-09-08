# Research: LLM Judge Faithfulness Dashboard

**Feature**: `001-llm-judge-dashboard`  
**Date**: 2026-09-08

## 1. Backend framework

**Decision**: FastAPI + Uvicorn on Python 3.12.

**Rationale**: Async-friendly for long pipeline runs; OpenAPI for `contracts/api.md`; easy pytest; matches constitution Python stack.

**Alternatives considered**: Flask (more sync boilerplate); Django (heavier than needed for one SPA demo).

## 2. SPA framework

**Decision**: Vite + React + TypeScript single page (no multi-route product IA).

**Rationale**: Strong Playwright ecosystem; charts and drop-downs are straightforward; keeps elegant component structure for Figma implementation.

**Alternatives considered**: Vue; plain HTML + Alpine (charts and test selectors get messier); Next.js (multi-route bias, unnecessary for SPA).

## 3. Transcription agents (drop-down catalog)

**Decision** — learner-visible free-tier options:

| ID | Label | Backend |
|----|-------|---------|
| `groq-whisper-large-v3-turbo` | Groq Whisper Large v3 Turbo | Groq Audio Transcriptions API |
| `groq-whisper-large-v3` | Groq Whisper Large v3 | Groq Audio Transcriptions API |
| `local-faster-whisper` | Local Faster-Whisper (PyTorch) | On-device `faster-whisper` |

**Default**: `groq-whisper-large-v3-turbo`.

**Rationale**: Groq free tier includes Whisper with documented RPM/RPD caps (~20 RPM, ~2000 RPD) and no credit card for free tier. Local Faster-Whisper satisfies Free-Tier First when cloud limits hit and uses PyTorch as constitution expects.

**Alternatives considered**: OpenAI Whisper paid API; AssemblyAI free trial only; HF Inference (less predictable free STT for long audio).

## 4. Summarizer (fixed, no drop-down)

**Decision**: `groq-llama-3.1-8b-instant` via Groq Chat Completions (product-configured).

**Rationale**: Highest free-tier headroom among Groq text models; enough for short summaries; keeps UI uncluttered (FR-017).

**Alternatives considered**: Gemini free tier (second vendor/key); Llama 70B for summary (wastes stronger quota better reserved for judge).

## 5. Judge agents (drop-down catalog, slightly stronger)

**Decision** — learner-visible free-tier options:

| ID | Label | Backend model |
|----|-------|---------------|
| `groq-llama-3.3-70b-versatile` | Groq Llama 3.3 70B | `llama-3.3-70b-versatile` |
| `groq-llama-4-scout` | Groq Llama 4 Scout | `meta-llama/llama-4-scout-17b-16e-instruct` |
| `groq-gpt-oss-20b` | Groq GPT-OSS 20B | `openai/gpt-oss-20b` |

**Default**: `groq-llama-3.3-70b-versatile`.

**Rationale**: Clearly stronger than the 8B summarizer; all on Groq free tier so one API key; judge prompt returns a single 0–100 faithfulness integer with brief rationale stored but not required on dashboard.

**Alternatives considered**: OpenAI/Anthropic free credits (paid path risk); using 8B as judge (weakens “slightly stronger” lesson).

## 6. Provider limits & failures

**Decision**: Map HTTP 429 / provider rate-limit errors to user-visible free-tier messages; do not invent transcripts or scores; allow switching agents (spec Stories 2–3, 7).

**Rationale**: Constitution Free-Tier First + FR-012.

## 7. Storage

**Decision**: SQLite for recordings metadata, pipeline runs, stage status, agent IDs, scores; files on disk for audio.

**Rationale**: Zero hosted cost; pandas can read scores for aggregate/export later; simple backups.

**Alternatives considered**: JSON-only files (race conditions under concurrent writes); Postgres (paid/hosting).

## 8. Aggregate metric

**Decision**: Arithmetic mean of completed faithfulness scores only (pandas or pure Python); display with ordinary rounding; empty state “No scores yet”.

**Rationale**: Spec FR-009 / SC-002.

## 9. Charts

**Decision**: At least two views — per-recording faithfulness bars; overall/aggregate highlight (and optional simple run-order trend if it stays minimal). Library chosen at implement (Recharts or Chart.js).

**Rationale**: Spec FR-018/019, Elegant UI — few views, numbers remain primary.

## 10. Acceptance tests

**Decision**: Gherkin under `features/` + Playwright driving UI; API/pipeline scenarios via Playwright request fixtures or pytest+httpx marked as backend acceptance; mocks for Groq in CI; optional live smoke when `GROQ_API_KEY` present.

**Rationale**: Constitution VIII; free CI without burning quota.

## 11. Preloaded audio

**Decision**: Ship ~10 all-ages ~3-minute clips generated or licensed for demo; metadata JSON lists title, duration, `all_ages: true`. Generation method locked in tasks (TTS script) — content review before commit.

**Rationale**: Spec FR-002 / SC-003.

## 12. All-ages local uploads

**Decision**: v1 heuristic gate (duration bounds + optional lightweight text check after transcript / block list); if uncertain, block scoring with clear message (spec assumption).

**Rationale**: Honest policy without paid moderation APIs.
