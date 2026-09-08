"""Free-tier agent catalogs shown in the SPA drop-downs."""

from __future__ import annotations

from typing import Any

# Fixed summarizer — not learner-selectable in v1 (FR-017).
SUMMARIZER_ID = "groq-llama-3.1-8b-instant"

TRANSCRIPTION_AGENTS: list[dict[str, Any]] = [
    {
        "id": "groq-whisper-large-v3-turbo",
        "label": "Groq Whisper Large v3 Turbo",
        "available": True,
    },
    {
        "id": "groq-whisper-large-v3",
        "label": "Groq Whisper Large v3",
        "available": True,
    },
    {
        "id": "local-faster-whisper",
        "label": "Local Faster-Whisper (PyTorch)",
        "available": True,
    },
]

# Slightly stronger than the 8B summarizer for the LLM-as-judge lesson.
JUDGE_AGENTS: list[dict[str, Any]] = [
    {
        "id": "groq-llama-3.3-70b-versatile",
        "label": "Groq Llama 3.3 70B",
        "available": True,
    },
    {
        "id": "groq-llama-4-scout",
        "label": "Groq Llama 4 Scout",
        "available": True,
    },
    {
        "id": "groq-gpt-oss-20b",
        "label": "Groq GPT-OSS 20B",
        "available": True,
    },
]

DEFAULT_TRANSCRIPTION_ID = "groq-whisper-large-v3-turbo"
DEFAULT_JUDGE_ID = "groq-llama-3.3-70b-versatile"


def transcription_catalog() -> dict[str, Any]:
    return {"agents": TRANSCRIPTION_AGENTS, "default_id": DEFAULT_TRANSCRIPTION_ID}


def judge_catalog() -> dict[str, Any]:
    return {"agents": JUDGE_AGENTS, "default_id": DEFAULT_JUDGE_ID}
