"""In-memory provider doubles for CI (no Groq network calls)."""

from __future__ import annotations


class MockSTT:
    def __init__(self, text: str = "Hello, this is an all-ages conversation about learning.") -> None:
        self.text = text
        self.calls: list[str] = []

    async def transcribe(self, audio_path: str) -> str:
        self.calls.append(audio_path)
        return self.text


class MockSummarizer:
    def __init__(self, text: str = "A short summary of learning.") -> None:
        self.text = text

    async def summarize(self, transcript: str) -> str:
        return self.text


class MockJudge:
    def __init__(self, value: float = 88.0) -> None:
        self.value = value

    async def score(self, transcript: str, summary: str) -> tuple[float, str | None]:
        return self.value, "Mock rationale"
