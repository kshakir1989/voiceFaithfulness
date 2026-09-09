"""Dev-only helpers for deterministic e2e isolation."""

from __future__ import annotations

import os

from fastapi import APIRouter, HTTPException

from app.domain.store import store

router = APIRouter(tags=["dev"])


def _reset_allowed() -> bool:
    # Learning/demo app: allow unless explicitly disabled (e.g. a future hosted deploy).
    if os.getenv("DISABLE_DEV_RESET", "").lower() in {"1", "true", "yes"}:
        return False
    return True


@router.post("/dev/reset")
def reset_store() -> dict:
    if not _reset_allowed():
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Not available."})
    store.reset()
    return {"ok": True}
