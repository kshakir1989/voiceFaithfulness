"""List preloaded (and later local) recordings from the on-disk manifest."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(tags=["recordings"])

# apps/voiceFaithfulness/data/preloaded/manifest.json
MANIFEST = Path(__file__).resolve().parents[3] / "data" / "preloaded" / "manifest.json"


@router.get("/recordings")
def list_recordings() -> dict:
    if not MANIFEST.exists():
        return {"recordings": []}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"recordings": data.get("recordings", [])}
