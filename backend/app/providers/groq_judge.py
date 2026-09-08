"""Groq chat judges returning faithfulness 0–100."""

from __future__ import annotations

import os
import re

import httpx

from app.providers.errors import ProviderError, RateLimitedError

JUDGE_MODELS = {
    "groq-llama-3.3-70b-versatile": "llama-3.3-70b-versatile",
    "groq-llama-4-scout": "meta-llama/llama-4-scout-17b-16e-instruct",
    "groq-gpt-oss-20b": "openai/gpt-oss-20b",
}


class GroqJudge:
    def __init__(self, agent_id: str, api_key: str | None = None) -> None:
        self.agent_id = agent_id
        self.model = JUDGE_MODELS[agent_id]
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")

    async def score(self, transcript: str, summary: str) -> tuple[float, str | None]:
        if not self.api_key:
            raise ProviderError("provider_error", "GROQ_API_KEY is not set.")
        prompt = (
            "You are an LLM-as-judge. Score how faithful the SUMMARY is to the TRANSCRIPT "
            "on a scale from 0 to 100 (integer). Reply with one line: SCORE=<n> then a short reason.\n\n"
            f"TRANSCRIPT:\n{transcript}\n\nSUMMARY:\n{summary}\n"
        )
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
        }
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(url, headers=headers, json=body)
        if resp.status_code == 429:
            raise RateLimitedError()
        if resp.status_code >= 400:
            raise ProviderError("provider_error", f"Groq judge failed: {resp.status_code}")
        text = (
            resp.json()
            .get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        match = re.search(r"SCORE\s*=\s*(\d{1,3})", text, re.I)
        if not match:
            # Fallback: first integer 0-100 in the reply
            match = re.search(r"\b(\d{1,3})\b", text)
        if not match:
            raise ProviderError("provider_error", "Judge did not return a score.")
        value = float(match.group(1))
        if value < 0 or value > 100:
            raise ProviderError("provider_error", "Judge score out of range.")
        return value, text
