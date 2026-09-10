"""In-memory run/score store + session-scoped ephemeral uploads."""

from __future__ import annotations

import shutil
from copy import deepcopy
from pathlib import Path
from threading import Lock
from typing import Any

# apps/voiceFaithfulness/data/uploads/sessions
_APP_ROOT = Path(__file__).resolve().parents[3]
SESSIONS_DIR = _APP_ROOT / "data" / "uploads" / "sessions"


class RunStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self.active_run_id: str | None = None
        self.runs: dict[str, dict[str, Any]] = {}
        self.scores: list[dict[str, Any]] = []
        self.local_by_session: dict[str, list[dict[str, Any]]] = {}

    def reset(self) -> None:
        with self._lock:
            self.active_run_id = None
            self.runs.clear()
            self.scores.clear()
            self.local_by_session.clear()
        if SESSIONS_DIR.is_dir():
            shutil.rmtree(SESSIONS_DIR, ignore_errors=True)

    def clear_demo_session(self, session_id: str | None = None) -> None:
        """Clear runs/scores and uploads (optionally one session); keep preloaded files."""
        with self._lock:
            self.active_run_id = None
            self.runs.clear()
            self.scores.clear()
            if session_id:
                self.local_by_session.pop(session_id, None)
                session_dir = SESSIONS_DIR / session_id
                if session_dir.is_dir():
                    shutil.rmtree(session_dir, ignore_errors=True)
            else:
                self.local_by_session.clear()
                if SESSIONS_DIR.is_dir():
                    shutil.rmtree(SESSIONS_DIR, ignore_errors=True)

    def add_local_recording(self, session_id: str, rec: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            self.local_by_session.setdefault(session_id, []).append(dict(rec))
            return deepcopy(rec)

    def list_local_recordings(self, session_id: str | None) -> list[dict[str, Any]]:
        if not session_id:
            return []
        with self._lock:
            return deepcopy(self.local_by_session.get(session_id, []))

    def snapshot_run(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            run = self.runs.get(run_id)
            return deepcopy(run) if run else None

    def list_runs(self) -> list[dict[str, Any]]:
        with self._lock:
            return [deepcopy(r) for r in sorted(self.runs.values(), key=lambda r: r["created_at"], reverse=True)]

    def list_scores(self) -> list[dict[str, Any]]:
        with self._lock:
            return deepcopy(self.scores)


store = RunStore()
