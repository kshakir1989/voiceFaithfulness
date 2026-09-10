"""AssemblyAI Universal STT (+ optional LeMUR/summary when configured)."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import httpx

from app.providers.errors import ProviderError, RateLimitedError


class AssemblyAISTT:
    """Upload → poll transcript. Summary is still produced by attached summarizer in factory."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY", "")
        self.agent_id = "assemblyai-universal"
        self.base = "https://api.assemblyai.com/v2"

    def _headers(self) -> dict[str, str]:
        return {"authorization": self.api_key}

    async def transcribe(self, audio_path: str) -> str:
        if not self.api_key:
            raise ProviderError("provider_error", "ASSEMBLYAI_API_KEY is not set.")
        path = Path(audio_path)
        if not path.is_file():
            raise ProviderError("invalid_audio", f"Audio not found: {audio_path}")
        async with httpx.AsyncClient(timeout=120.0) as client:
            up = await client.post(
                f"{self.base}/upload",
                headers=self._headers(),
                content=path.read_bytes(),
            )
            if up.status_code == 429:
                raise RateLimitedError()
            if up.status_code >= 400:
                raise ProviderError("provider_error", f"AssemblyAI upload failed: {up.status_code}")
            upload_url = up.json().get("upload_url")
            if not upload_url:
                raise ProviderError("provider_error", "AssemblyAI upload missing URL.")
            create = await client.post(
                f"{self.base}/transcript",
                headers={**self._headers(), "content-type": "application/json"},
                json={"audio_url": upload_url},
            )
            if create.status_code == 429:
                raise RateLimitedError()
            if create.status_code >= 400:
                raise ProviderError(
                    "provider_error", f"AssemblyAI transcript create failed: {create.status_code}"
                )
            tid = create.json().get("id")
            if not tid:
                raise ProviderError("provider_error", "AssemblyAI missing transcript id.")
            for _ in range(60):
                poll = await client.get(f"{self.base}/transcript/{tid}", headers=self._headers())
                if poll.status_code == 429:
                    raise RateLimitedError()
                if poll.status_code >= 400:
                    raise ProviderError(
                        "provider_error", f"AssemblyAI poll failed: {poll.status_code}"
                    )
                body = poll.json()
                status = body.get("status")
                if status == "completed":
                    text = (body.get("text") or "").strip()
                    if not text:
                        raise ProviderError("provider_error", "AssemblyAI empty transcript.")
                    return text
                if status == "error":
                    raise ProviderError(
                        "provider_error", body.get("error") or "AssemblyAI transcript error."
                    )
                await asyncio.sleep(1.0)
        raise ProviderError("provider_error", "AssemblyAI transcript timed out.")
