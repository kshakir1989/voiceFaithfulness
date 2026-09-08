"""Execute ingest → transcript → summary → judge → aggregate for one run."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.domain.pipeline import STAGE_ORDER, StageName, StageStatus, RunStatus, initial_stages
from app.domain.store import RunStore, store
from app.providers.catalog import SUMMARIZER_ID
from app.providers.errors import ProviderError
from app.providers.factory import get_judge, get_stt, get_summarizer

APP_ROOT = Path(__file__).resolve().parents[3]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stage_list(stages: dict[str, str]) -> list[dict[str, str]]:
    return [{"name": name.value, "status": stages[name.value]} for name in STAGE_ORDER]


def resolve_audio_path(audio_path: str) -> Path:
    path = Path(audio_path)
    if path.is_file():
        return path
    candidate = APP_ROOT / audio_path
    if candidate.is_file():
        return candidate
    return path


async def execute_run(
    *,
    recording: dict[str, Any],
    transcription_agent_id: str,
    judge_agent_id: str,
    run_store: RunStore | None = None,
    stt: Any | None = None,
    summarizer: Any | None = None,
    judge: Any | None = None,
) -> dict[str, Any]:
    """Create and fully execute a pipeline run; returns the final run snapshot."""
    rs = run_store or store
    run_id = str(uuid4())
    created = _now()
    stages = initial_stages()
    run: dict[str, Any] = {
        "id": run_id,
        "recording_id": recording["id"],
        "recording_title": recording.get("title", recording["id"]),
        "transcription_agent_id": transcription_agent_id,
        "judge_agent_id": judge_agent_id,
        "summarizer_id": SUMMARIZER_ID,
        "status": RunStatus.RUNNING.value,
        "error_message": None,
        "error_code": None,
        "created_at": created,
        "updated_at": created,
        "stages": _stage_list(stages),
        "transcript": None,
        "summary": None,
        "score": None,
    }

    with rs._lock:
        if rs.active_run_id is not None:
            raise ProviderError("run_in_progress", "Another pipeline run is active.")
        rs.active_run_id = run_id
        rs.runs[run_id] = run

    def persist() -> None:
        run["updated_at"] = _now()
        run["stages"] = _stage_list(stages)
        with rs._lock:
            rs.runs[run_id] = dict(run)

    def set_stage(name: StageName, status: StageStatus) -> None:
        stages[name.value] = status.value
        persist()

    stt_impl = stt or get_stt(transcription_agent_id)
    sum_impl = summarizer or get_summarizer()
    judge_impl = judge or get_judge(judge_agent_id)

    try:
        # ingest
        set_stage(StageName.INGEST, StageStatus.RUNNING)
        audio = resolve_audio_path(recording["audio_path"])
        if not audio.is_file():
            # Allow mock path when using MockSTT without real files.
            if stt is None and hasattr(stt_impl, "calls"):
                audio = Path(recording["audio_path"])
            else:
                raise ProviderError("invalid_audio", f"Audio not found: {recording['audio_path']}")
        set_stage(StageName.INGEST, StageStatus.COMPLETED)

        # transcript
        set_stage(StageName.TRANSCRIPT, StageStatus.RUNNING)
        transcript = await stt_impl.transcribe(str(audio))
        if not (transcript or "").strip():
            raise ProviderError("provider_error", "Empty transcript.")
        run["transcript"] = transcript
        set_stage(StageName.TRANSCRIPT, StageStatus.COMPLETED)

        # summary
        set_stage(StageName.SUMMARY, StageStatus.RUNNING)
        summary = await sum_impl.summarize(transcript)
        if not (summary or "").strip():
            raise ProviderError("empty_summary", "Empty summary.")
        run["summary"] = summary
        set_stage(StageName.SUMMARY, StageStatus.COMPLETED)

        # judge
        set_stage(StageName.JUDGE, StageStatus.RUNNING)
        value, rationale = await judge_impl.score(transcript, summary)
        if value < 0 or value > 100:
            raise ProviderError("provider_error", "Score out of range.")
        run["score"] = {
            "value": float(value),
            "judge_agent_id": judge_agent_id,
            "rationale": rationale,
        }
        set_stage(StageName.JUDGE, StageStatus.COMPLETED)

        # aggregate contribution
        set_stage(StageName.AGGREGATE, StageStatus.RUNNING)
        score_row = {
            "recording_id": recording["id"],
            "title": recording.get("title", recording["id"]),
            "value": float(value),
            "transcription_agent_id": transcription_agent_id,
            "judge_agent_id": judge_agent_id,
            "run_id": run_id,
        }
        with rs._lock:
            rs.scores.append(score_row)
        set_stage(StageName.AGGREGATE, StageStatus.COMPLETED)

        run["status"] = RunStatus.COMPLETED.value
        persist()
    except ProviderError as exc:
        run["status"] = RunStatus.FAILED.value
        run["error_code"] = exc.code
        run["error_message"] = exc.message
        # Mark current running stage failed
        for name in STAGE_ORDER:
            if stages[name.value] == StageStatus.RUNNING.value:
                stages[name.value] = StageStatus.FAILED.value
                break
        persist()
    finally:
        with rs._lock:
            if rs.active_run_id == run_id:
                rs.active_run_id = None

    return rs.snapshot_run(run_id) or run
