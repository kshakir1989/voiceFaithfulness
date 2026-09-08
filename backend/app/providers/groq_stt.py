"""Groq Whisper STT (turbo / v3)."""

from __future__ import annotations

import os
from pathlib import Path

import httpx

from app.providers.errors import ProviderError, RateLimitedError

# Model id per catalog entry.
GROQ_STT_MODELS = {
    "groq-whisper-large-v3-turbo": "whisper-large-v3-turbo",
    "groq-whisper-large-v3": "whisper-large-v3",
}


class GroqSTT:
    def __init__(self, agent_id: str, api_key: str | None = None) -> None:
        self.agent_id = agent_id
        self.model = GROQ_STT_MODELS[agent_id]
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")

    async def transcribe(self, audio_path: str) -> str:
        if not self.api_key:
            raise ProviderError("provider_error", "GROQ_API_KEY is not set.")
        path = Path(audio_path)
        if not path.is_file():
            raise ProviderError("invalid_audio", f"Audio not found: {audio_path}")
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=120.0) as client:
            with path.open("rb") as f:
                files = {"file": (path.name, f, "audio/wav")}
                data = {"model": self.model, "response_format": "json"}
                resp = await client.post(url, headers=headers, files=files, data=data)
        if resp.status_code == 429:
            raise RateLimitedError()
        if resp.status_code >= 400:
            raise ProviderError("provider_error", f"Groq STT failed: {resp.status_code}")
        text = (resp.json().get("text") or "").strip()
        if not text:
            raise ProviderError("provider_error", "Empty transcript from Groq STT.")
        return text
