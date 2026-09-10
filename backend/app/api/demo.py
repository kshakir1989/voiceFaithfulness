"""Learner-facing demo session clear (runs, scores, uploads — keep preloads)."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response

from app.domain.session import get_or_set_session_id
from app.domain.store import store

router = APIRouter(tags=["demo"])


@router.delete("/demo/session")
def clear_demo_session(request: Request, response: Response) -> dict:
    """Clear pipeline runs, scores, and ephemeral uploads; preloaded demos remain."""
    sid = get_or_set_session_id(request, response)
    store.clear_demo_session(sid)
    return {"ok": True, "cleared": ["runs", "scores", "uploads"]}
