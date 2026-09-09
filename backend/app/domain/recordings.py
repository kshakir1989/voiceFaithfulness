"""Resolve preloaded + session-scoped local recordings for list/run/preview."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.domain.store import store

APP_ROOT = Path(__file__).resolve().parents[3]
MANIFEST = APP_ROOT / "data" / "preloaded" / "manifest.json"
UPLOADS_DIR = APP_ROOT / "data" / "uploads"
SESSIONS_DIR = UPLOADS_DIR / "sessions"


def _public(rec: dict[str, Any]) -> dict[str, Any]:
    blocked = not bool(rec.get("all_ages_eligible", True))
    title = rec.get("title", rec["id"])
    return {
        "id": rec["id"],
        "title": title,
        "source_type": rec.get("source_type", "preloaded"),
        "duration_seconds": rec.get("duration_seconds"),
        "all_ages_eligible": not blocked,
        "demo_fail": bool(rec.get("demo_fail", blocked and rec.get("source_type") == "preloaded")),
        "ephemeral": rec.get("source_type") == "local",
        "audio_url": f"/api/recordings/{rec['id']}/audio",
    }


def _preloaded() -> list[dict[str, Any]]:
    if not MANIFEST.exists():
        return []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return list(data.get("recordings", []))


def list_recordings(session_id: str | None = None) -> list[dict[str, Any]]:
    items = [_public(r) for r in _preloaded()]
    items.extend(_public(r) for r in store.list_local_recordings(session_id))
    return items


def find_recording(recording_id: str, session_id: str | None = None) -> dict[str, Any] | None:
    for rec in _preloaded():
        if rec["id"] == recording_id:
            return dict(rec)
    for rec in store.list_local_recordings(session_id):
        if rec["id"] == recording_id:
            return dict(rec)
    return None


def resolve_audio_file(recording: dict[str, Any]) -> Path | None:
    path = recording.get("audio_path")
    if not path:
        return None
    p = Path(path)
    if p.is_file():
        return p
    candidate = APP_ROOT / path
    if candidate.is_file():
        return candidate
    return None


def session_upload_dir(session_id: str) -> Path:
    path = SESSIONS_DIR / session_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def purge_session_uploads(session_id: str) -> int:
    """Remove in-memory rows and on-disk session directory."""
    import shutil

    with store._lock:
        store.local_by_session.pop(session_id, None)
    session_dir = SESSIONS_DIR / session_id
    if session_dir.is_dir():
        shutil.rmtree(session_dir, ignore_errors=True)
        return 1
    return 0
