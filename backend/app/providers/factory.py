"""
Resolve STT / summarizer / judge implementations by catalog id.

Python note: this module is a small factory. Callers pass an agent id string;
we return an object that implements the async methods used by the pipeline
(`transcribe`, `summarize`, `score`). `use_mocks()` keeps CI and local demos
off the network when FORCE_MOCK_PROVIDERS=1 or when pytest is running.
"""

from __future__ import annotations

import os
from typing import Any

from app.providers.assemblyai_stt import AssemblyAISTT
from app.providers.deepgram_stt import DeepgramSTT
from app.providers.groq_judge import GroqJudge
from app.providers.groq_stt import GroqSTT
from app.providers.groq_summarize import GroqSummarizer
from app.providers.local_stt import LocalFasterWhisperSTT
from app.providers.mocks import MockJudge, MockSTT, MockSummarizer


def use_mocks() -> bool:
    """Prefer mocks in tests or when FORCE_MOCK_PROVIDERS=1."""
    if os.getenv("FORCE_MOCK_PROVIDERS", "").lower() in {"1", "true", "yes"}:
        return True
    if os.getenv("PYTEST_CURRENT_TEST"):
        return True
    return False


def get_stt(agent_id: str) -> Any:
    """Return a speech-to-text provider for the selected catalog id."""
    if use_mocks() or agent_id.startswith("mock"):
        return MockSTT(agent_id=agent_id)
    if agent_id == "local-faster-whisper":
        return LocalFasterWhisperSTT()
    if agent_id in {"groq-whisper-large-v3-turbo", "groq-whisper-large-v3"}:
        if not os.getenv("GROQ_API_KEY"):
            return MockSTT(agent_id=agent_id)
        return GroqSTT(agent_id)
    if agent_id == "deepgram-nova-3":
        if not os.getenv("DEEPGRAM_API_KEY"):
            raise ValueError("Deepgram agent unavailable without DEEPGRAM_API_KEY")
        return DeepgramSTT()
    if agent_id == "assemblyai-universal":
        if not os.getenv("ASSEMBLYAI_API_KEY"):
            raise ValueError("AssemblyAI agent unavailable without ASSEMBLYAI_API_KEY")
        return AssemblyAISTT()
    raise ValueError(f"Unknown transcription agent: {agent_id}")


def get_summarizer(transcription_agent_id: str | None = None) -> Any:
    """
    Summarizer attached to the selected transcription agent.

    Spec 002: the STT agent owns the summary artifact; we may still call a
    Groq chat model under the hood, but attribution stays on transcription_agent_id.
    """
    if use_mocks() or not os.getenv("GROQ_API_KEY"):
        return MockSummarizer(agent_id=transcription_agent_id)
    return GroqSummarizer(for_agent_id=transcription_agent_id)


def get_judge(agent_id: str) -> Any:
    """Return an LLM-as-judge that scores summary faithfulness 0–100."""
    if use_mocks() or agent_id.startswith("mock"):
        return MockJudge(agent_id=agent_id)
    if agent_id in {
        "groq-llama-3.3-70b-versatile",
        "groq-llama-4-scout",
        "groq-gpt-oss-20b",
    }:
        if not os.getenv("GROQ_API_KEY"):
            return MockJudge(agent_id=agent_id)
        return GroqJudge(agent_id)
    raise ValueError(f"Unknown judge agent: {agent_id}")
