"""Fixed free-tier summarizer: llama-3.1-8b-instant."""

from __future__ import annotations

import os

import httpx

from app.providers.catalog import SUMMARIZER_ID
from app.providers.errors import ProviderError, RateLimitedError

MODEL = "llama-3.1-8b-instant"


class GroqSummarizer:
    def __init__(self, api_key: str | None = None, for_agent_id: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        # Product model used under the hood; ownership is for_agent_id (transcription agent).
        self.summarizer_id = for_agent_id or SUMMARIZER_ID
        self.for_agent_id = for_agent_id

    async def summarize(self, transcript: str) -> str:
        if not self.api_key:
            raise ProviderError("provider_error", "GROQ_API_KEY is not set.")
        prompt = (
            "Summarize the following transcript in 2-4 short sentences for all ages. "
            "Reply with the summary only.\n\n"
            f"{transcript}"
        )
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=headers, json=body)
        if resp.status_code == 429:
            raise RateLimitedError()
        if resp.status_code >= 400:
            raise ProviderError("provider_error", f"Groq summarize failed: {resp.status_code}")
        text = (
            resp.json()
            .get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        if not text:
            raise ProviderError("empty_summary", "Summarizer returned empty text.")
        return text
