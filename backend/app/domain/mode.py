"""Provider mode: stub (mocks) vs live (Groq key + not forced mock)."""

from __future__ import annotations

import os

from app.providers.factory import use_mocks


def providers_mode() -> str:
    """Return 'stub' or 'live' for learner-facing honesty about scores."""
    if use_mocks():
        return "stub"
    if not (os.getenv("GROQ_API_KEY") or "").strip():
        return "stub"
    return "live"
