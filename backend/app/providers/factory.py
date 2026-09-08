"""Resolve STT / summarizer / judge implementations by catalog id."""

from __future__ import annotations

import os
from typing import Any

from app.providers.groq_judge import GroqJudge
from app.providers.groq_stt import GroqSTT
from app.providers.groq_summarize import GroqSummarizer
from app.providers.local_stt import LocalFasterWhisperSTT
from app.providers.mocks import MockJudge, MockSTT, MockSummarizer


def use_mocks() -> bool:
    """Prefer mocks in tests or when FORCE_MOCK_PROVIDERS=1 / no API key."""
    if os.getenv("FORCE_MOCK_PROVIDERS", "").lower() in {"1", "true", "yes"}:
        return True
    if os.getenv("PYTEST_CURRENT_TEST"):
        return True
    return False


def get_stt(agent_id: str) -> Any:
    if use_mocks() or agent_id.startswith("mock"):
        return MockSTT()
    if agent_id == "local-faster-whisper":
        return LocalFasterWhisperSTT()
    if agent_id in {"groq-whisper-large-v3-turbo", "groq-whisper-large-v3"}:
        if not os.getenv("GROQ_API_KEY"):
            return MockSTT()
        return GroqSTT(agent_id)
    raise ValueError(f"Unknown transcription agent: {agent_id}")


def get_summarizer() -> Any:
    if use_mocks() or not os.getenv("GROQ_API_KEY"):
        return MockSummarizer()
    return GroqSummarizer()


def get_judge(agent_id: str) -> Any:
    if use_mocks() or agent_id.startswith("mock"):
        return MockJudge()
    if agent_id in {
        "groq-llama-3.3-70b-versatile",
        "groq-llama-4-scout",
        "groq-gpt-oss-20b",
    }:
        if not os.getenv("GROQ_API_KEY"):
            return MockJudge()
        return GroqJudge(agent_id)
    raise ValueError(f"Unknown judge agent: {agent_id}")
