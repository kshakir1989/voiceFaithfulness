"""In-memory provider doubles for CI (no Groq network calls)."""

from __future__ import annotations


class MockSTT:
    def __init__(
        self,
        text: str = "Hello, this is an all-ages conversation about learning.",
        *,
        agent_id: str | None = None,
    ) -> None:
        self.text = text
        self.agent_id = agent_id
        self.calls: list[str] = []
        self.agent_ids: list[str] = []

    async def transcribe(self, audio_path: str) -> str:
        self.calls.append(audio_path)
        if self.agent_id is not None:
            self.agent_ids.append(self.agent_id)
        return self.text


class MockSummarizer:
    def __init__(self, text: str = "A short summary of learning.") -> None:
        self.text = text

    async def summarize(self, transcript: str) -> str:
        return self.text


class MockJudge:
    def __init__(self, value: float = 88.0, *, agent_id: str | None = None) -> None:
        self.value = value
        self.agent_id = agent_id
        self.agent_ids: list[str] = []

    async def score(self, transcript: str, summary: str) -> tuple[float, str | None]:
        if self.agent_id is not None:
            self.agent_ids.append(self.agent_id)
        return self.value, "Mock rationale"
