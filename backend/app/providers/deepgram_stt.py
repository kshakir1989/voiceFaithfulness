"""Deepgram Nova-3 pre-recorded transcription (free-path credit / API key)."""

from __future__ import annotations

import os
from pathlib import Path

import httpx

from app.providers.errors import ProviderError, RateLimitedError


class DeepgramSTT:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("DEEPGRAM_API_KEY", "")
        self.agent_id = "deepgram-nova-3"

    async def transcribe(self, audio_path: str) -> str:
        if not self.api_key:
            raise ProviderError("provider_error", "DEEPGRAM_API_KEY is not set.")
        path = Path(audio_path)
        if not path.is_file():
            raise ProviderError("invalid_audio", f"Audio not found: {audio_path}")
        url = "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true"
        headers = {"Authorization": f"Token {self.api_key}", "Content-Type": "audio/wav"}
        data = path.read_bytes()
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, headers=headers, content=data)
        if resp.status_code == 429:
            raise RateLimitedError()
        if resp.status_code >= 400:
            raise ProviderError("provider_error", f"Deepgram STT failed: {resp.status_code}")
        try:
            alt = resp.json()["results"]["channels"][0]["alternatives"][0]
            text = (alt.get("transcript") or "").strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("provider_error", "Deepgram returned unexpected JSON.") from exc
        if not text:
            raise ProviderError("provider_error", "Deepgram produced an empty transcript.")
        return text
