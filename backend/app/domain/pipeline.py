"""Ordered pipeline stages: ingest → transcript → summary → judge → aggregate."""

from __future__ import annotations

from enum import Enum


class StageName(str, Enum):
    INGEST = "ingest"
    TRANSCRIPT = "transcript"
    SUMMARY = "summary"
    JUDGE = "judge"
    AGGREGATE = "aggregate"


class StageStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


STAGE_ORDER: tuple[StageName, ...] = (
    StageName.INGEST,
    StageName.TRANSCRIPT,
    StageName.SUMMARY,
    StageName.JUDGE,
    StageName.AGGREGATE,
)


def initial_stages() -> dict[str, str]:
    """All stages start pending when a run is created."""
    return {s.value: StageStatus.PENDING.value for s in STAGE_ORDER}


def advance(stages: dict[str, str], stage: StageName, status: StageStatus) -> dict[str, str]:
    """Return a copy with one stage updated (immutable-style)."""
    next_stages = dict(stages)
    next_stages[stage.value] = status.value
    return next_stages


def can_start_run(*, transcription_agent_id: str | None, judge_agent_id: str | None) -> bool:
    """Both drop-downs must be selected before transcription starts."""
    return bool(transcription_agent_id and judge_agent_id)
