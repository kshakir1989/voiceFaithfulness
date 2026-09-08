"""Provider protocols: STT → summarize → judge score."""

from __future__ import annotations

from typing import Protocol


class SpeechToText(Protocol):
    async def transcribe(self, audio_path: str) -> str: ...


class Summarizer(Protocol):
    async def summarize(self, transcript: str) -> str: ...


class Judge(Protocol):
    async def score(self, transcript: str, summary: str) -> tuple[float, str | None]:
        """Return faithfulness 0–100 and optional short rationale."""
