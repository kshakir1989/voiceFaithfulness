"""In-memory provider doubles for CI (no Groq network calls)."""

from __future__ import annotations


class MockSTT:
    def __init__(
        self,
        text: str | None = None,
        *,
        agent_id: str | None = None,
    ) -> None:
        self.agent_id = agent_id
        self.text = text or (
            f"[{agent_id}] Hello, this is an all-ages conversation about learning."
            if agent_id
            else "Hello, this is an all-ages conversation about learning."
        )
        self.calls: list[str] = []
        self.agent_ids: list[str] = []

    async def transcribe(self, audio_path: str) -> str:
        self.calls.append(audio_path)
        if self.agent_id is not None:
            self.agent_ids.append(self.agent_id)
        return self.text


class MockSummarizer:
    def __init__(self, text: str | None = None, *, agent_id: str | None = None) -> None:
        self.agent_id = agent_id
        self.text = text or (
            f"Summary from {agent_id}: a short summary of learning."
            if agent_id
            else "A short summary of learning."
        )

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
        return self.value, "Mock rationale: summary stays faithful to the transcript."
