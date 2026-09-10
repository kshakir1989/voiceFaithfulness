"""Free-tier agent catalogs shown in the SPA drop-downs (002: five STT, judge tiers)."""

from __future__ import annotations

import os
from typing import Any

# Default attached summarizer model when an STT agent has no native summary API.
# The *transcription agent* owns the summary artifact (amends 001 FR-017).
ATTACHED_SUMMARIZER_MODEL = "groq-llama-3.1-8b-instant"
# Back-compat alias for older imports/tests.
SUMMARIZER_ID = ATTACHED_SUMMARIZER_MODEL

TRANSCRIPTION_AGENTS: list[dict[str, Any]] = [
    {
        "id": "groq-whisper-large-v3-turbo",
        "label": "Groq Whisper Large v3 Turbo",
        "provider": "groq",
        "owns_summary": True,
        "summary_backend": ATTACHED_SUMMARIZER_MODEL,
        "available": True,
    },
    {
        "id": "groq-whisper-large-v3",
        "label": "Groq Whisper Large v3",
        "provider": "groq",
        "owns_summary": True,
        "summary_backend": ATTACHED_SUMMARIZER_MODEL,
        "available": True,
    },
    {
        "id": "local-faster-whisper",
        "label": "Local Faster-Whisper (PyTorch)",
        "provider": "local",
        "owns_summary": True,
        "summary_backend": ATTACHED_SUMMARIZER_MODEL,
        "available": True,
    },
    {
        "id": "deepgram-nova-3",
        "label": "Deepgram Nova-3",
        "provider": "deepgram",
        "owns_summary": True,
        "summary_backend": ATTACHED_SUMMARIZER_MODEL,
        "available": True,
    },
    {
        "id": "assemblyai-universal",
        "label": "AssemblyAI Universal",
        "provider": "assemblyai",
        "owns_summary": True,
        "summary_backend": "assemblyai-or-attached",
        "available": True,
    },
]

JUDGE_AGENTS: list[dict[str, Any]] = [
    {
        "id": "groq-gpt-oss-20b",
        "label": "Groq GPT-OSS 20B",
        "provider": "groq",
        "power_tier": 1,
        "available": True,
    },
    {
        "id": "groq-llama-4-scout",
        "label": "Groq Llama 4 Scout",
        "provider": "groq",
        "power_tier": 2,
        "available": True,
    },
    {
        "id": "groq-llama-3.3-70b-versatile",
        "label": "Groq Llama 3.3 70B",
        "provider": "groq",
        "power_tier": 3,
        "available": True,
    },
]

DEFAULT_TRANSCRIPTION_ID = "groq-whisper-large-v3-turbo"
DEFAULT_JUDGE_ID = "groq-llama-3.3-70b-versatile"
# Judges at or above this tier get highlight: true in the catalog response.
HIGHLIGHT_MIN_POWER_TIER = 2


def _key(name: str) -> bool:
    return bool((os.getenv(name) or "").strip())


def _use_mocks() -> bool:
    if os.getenv("FORCE_MOCK_PROVIDERS", "").lower() in {"1", "true", "yes"}:
        return True
    if os.getenv("PYTEST_CURRENT_TEST"):
        return True
    return False


def _transcription_available(agent: dict[str, Any]) -> bool:
    if _use_mocks():
        return True
    provider = agent.get("provider")
    # Groq + local stay selectable; factory falls back to mocks when GROQ_API_KEY is missing.
    if provider in {"groq", "local"}:
        return True
    if provider == "deepgram":
        return _key("DEEPGRAM_API_KEY")
    if provider == "assemblyai":
        return _key("ASSEMBLYAI_API_KEY")
    return False


def _judge_available(_agent: dict[str, Any]) -> bool:
    # Always selectable; factory uses MockJudge without GROQ_API_KEY / under FORCE_MOCK.
    return True


def transcription_catalog() -> dict[str, Any]:
    agents = []
    for raw in TRANSCRIPTION_AGENTS:
        agent = dict(raw)
        agent["available"] = _transcription_available(raw)
        agent["owns_summary"] = True
        agents.append(agent)
    return {"agents": agents, "default_id": DEFAULT_TRANSCRIPTION_ID}


def judge_catalog() -> dict[str, Any]:
    agents = []
    for raw in JUDGE_AGENTS:
        agent = dict(raw)
        tier = int(agent.get("power_tier", 0))
        agent["available"] = _judge_available(raw)
        agent["highlight"] = tier >= HIGHLIGHT_MIN_POWER_TIER
        agents.append(agent)
    return {"agents": agents, "default_id": DEFAULT_JUDGE_ID}


def find_transcription_agent(agent_id: str) -> dict[str, Any] | None:
    for agent in transcription_catalog()["agents"]:
        if agent["id"] == agent_id:
            return agent
    return None


def find_judge_agent(agent_id: str) -> dict[str, Any] | None:
    for agent in judge_catalog()["agents"]:
        if agent["id"] == agent_id:
            return agent
    return None
