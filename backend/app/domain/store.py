"""In-memory run/score store (swap for SQLite persistence later)."""

from __future__ import annotations

from copy import deepcopy
from threading import Lock
from typing import Any


class RunStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self.active_run_id: str | None = None
        self.runs: dict[str, dict[str, Any]] = {}
        self.scores: list[dict[str, Any]] = []

    def reset(self) -> None:
        with self._lock:
            self.active_run_id = None
            self.runs.clear()
            self.scores.clear()

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
