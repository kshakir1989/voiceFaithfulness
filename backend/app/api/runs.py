"""Start/list pipeline runs (sync completion for mock-speed demos)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

from app.domain.pipeline import can_start_run
from app.domain.recordings import find_recording
from app.domain.runner import execute_run
from app.domain.session import get_or_set_session_id
from app.domain.store import store
from app.providers.catalog import find_judge_agent, find_transcription_agent
from app.providers.errors import ProviderError

router = APIRouter(tags=["runs"])

_HTTP_BY_CODE = {
    "run_in_progress": 409,
    "rate_limited": 429,
    "all_ages_blocked": 403,
    "not_found": 404,
}


def _load_recording(recording_id: str, session_id: str | None) -> dict:
    rec = find_recording(recording_id, session_id)
    if not rec:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Recording not found."})
    return rec


def _require_agents(transcription_agent_id: str, judge_agent_id: str) -> None:
    if not can_start_run(
        transcription_agent_id=transcription_agent_id,
        judge_agent_id=judge_agent_id,
    ):
        raise HTTPException(
            status_code=400,
            detail={"code": "missing_agents", "message": "Select both agents."},
        )
    stt = find_transcription_agent(transcription_agent_id)
    if stt is None:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "unknown_transcription_agent",
                "message": f"Unknown transcription agent: {transcription_agent_id}",
            },
        )
    if not stt.get("available", True):
        raise HTTPException(
            status_code=400,
            detail={
                "code": "transcription_unavailable",
                "message": f"{stt['label']} is unavailable. Choose another transcription agent.",
            },
        )
    judge = find_judge_agent(judge_agent_id)
    if judge is None:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "unknown_judge_agent",
                "message": f"Unknown judge agent: {judge_agent_id}",
            },
        )
    if not judge.get("available", True):
        raise HTTPException(
            status_code=400,
            detail={
                "code": "judge_unavailable",
                "message": f"{judge['label']} is unavailable. Choose another judge agent.",
            },
        )


def _raise_provider(exc: ProviderError) -> None:
    status = _HTTP_BY_CODE.get(exc.code, 400)
    raise HTTPException(status_code=status, detail={"code": exc.code, "message": exc.message}) from exc


class StartRunBody(BaseModel):
    recording_id: str
    transcription_agent_id: str = Field(min_length=1)
    judge_agent_id: str = Field(min_length=1)


@router.post("/runs", status_code=201)
async def start_run(body: StartRunBody, request: Request, response: Response) -> dict:
    sid = get_or_set_session_id(request, response)
    if store.active_run_id is not None:
        raise HTTPException(
            status_code=409,
            detail={"code": "run_in_progress", "message": "Another pipeline run is active."},
        )
    _require_agents(body.transcription_agent_id, body.judge_agent_id)
    recording = _load_recording(body.recording_id, sid)
    if not recording.get("all_ages_eligible", True):
        msg = (
            "This demo recording is labeled as blocked bad data and cannot be scored."
            if recording.get("demo_fail")
            else "Recording is not all-ages eligible."
        )
        raise HTTPException(
            status_code=403,
            detail={"code": "all_ages_blocked", "message": msg},
        )
    try:
        run = await execute_run(
            recording=recording,
            transcription_agent_id=body.transcription_agent_id,
            judge_agent_id=body.judge_agent_id,
        )
    except ProviderError as exc:
        _raise_provider(exc)
    assert run is not None
    # Mid-run rate limits are recorded on the run; surface as 429 for the SPA banner.
    if run.get("status") == "failed" and run.get("error_code") == "rate_limited":
        raise HTTPException(
            status_code=429,
            detail={
                "code": "rate_limited",
                "message": run.get("error_message") or "Free-tier rate limit reached.",
                "run": run,
            },
        )
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
