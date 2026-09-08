"""Start/list pipeline runs (sync completion for mock-speed demos)."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.domain.pipeline import can_start_run
from app.domain.runner import execute_run
from app.domain.store import store
from app.providers.errors import ProviderError

router = APIRouter(tags=["runs"])

MANIFEST = Path(__file__).resolve().parents[3] / "data" / "preloaded" / "manifest.json"


def _load_recording(recording_id: str) -> dict:
    if not MANIFEST.exists():
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "No recordings."})
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for rec in data.get("recordings", []):
        if rec["id"] == recording_id:
            return rec
    raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Recording not found."})


class StartRunBody(BaseModel):
    recording_id: str
    transcription_agent_id: str = Field(min_length=1)
    judge_agent_id: str = Field(min_length=1)


@router.post("/runs", status_code=201)
async def start_run(body: StartRunBody) -> dict:
    if store.active_run_id is not None:
        raise HTTPException(
            status_code=409,
            detail={"code": "run_in_progress", "message": "Another pipeline run is active."},
        )
    if not can_start_run(
        transcription_agent_id=body.transcription_agent_id,
        judge_agent_id=body.judge_agent_id,
    ):
        raise HTTPException(
            status_code=400,
            detail={"code": "missing_agents", "message": "Select both agents."},
        )
    recording = _load_recording(body.recording_id)
    if not recording.get("all_ages_eligible", True):
        raise HTTPException(
            status_code=403,
            detail={"code": "all_ages_blocked", "message": "Recording is not all-ages eligible."},
        )
    try:
        run = await execute_run(
            recording=recording,
            transcription_agent_id=body.transcription_agent_id,
            judge_agent_id=body.judge_agent_id,
        )
    except ProviderError as exc:
        if exc.code == "run_in_progress":
            raise HTTPException(status_code=409, detail={"code": exc.code, "message": exc.message}) from exc
        raise HTTPException(status_code=400, detail={"code": exc.code, "message": exc.message}) from exc
    assert run is not None
    return run


@router.get("/runs")
def list_runs() -> dict:
    return {"runs": store.list_runs()}


@router.get("/runs/{run_id}")
def get_run(run_id: str) -> dict:
    run = store.snapshot_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Run not found."})
    return run
