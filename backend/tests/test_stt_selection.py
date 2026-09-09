"""US2: selected transcription agent is stored and used for STT."""

from __future__ import annotations

import pytest

from app.domain.runner import execute_run
from app.providers.catalog import DEFAULT_JUDGE_ID, TRANSCRIPTION_AGENTS
from app.providers.errors import RateLimitedError
from app.providers.mocks import MockSTT

ALT_STT = "groq-whisper-large-v3"


def test_run_stores_selected_transcription_agent(client):
    assert ALT_STT != TRANSCRIPTION_AGENTS[0]["id"]
    body = {
        "recording_id": "preload-01",
        "transcription_agent_id": ALT_STT,
        "judge_agent_id": DEFAULT_JUDGE_ID,
    }
    r = client.post("/api/runs", json=body)
    assert r.status_code == 201, r.text
    run = r.json()
    assert run["transcription_agent_id"] == ALT_STT
    assert run["status"] == "completed"


@pytest.mark.asyncio
async def test_mock_stt_receives_selected_agent_id():
    stt = MockSTT(agent_id=ALT_STT)
    recording = {
        "id": "preload-01",
        "title": "Test",
        "audio_path": "data/preloaded/preload-01.wav",
        "all_ages_eligible": True,
    }
    run = await execute_run(
        recording=recording,
        transcription_agent_id=ALT_STT,
        judge_agent_id=DEFAULT_JUDGE_ID,
        stt=stt,
    )
    assert run["transcription_agent_id"] == ALT_STT
    assert stt.agent_ids == [ALT_STT]
    assert stt.calls


def test_unknown_transcription_agent_rejected(client):
    r = client.post(
        "/api/runs",
        json={
            "recording_id": "preload-01",
            "transcription_agent_id": "not-a-real-stt",
            "judge_agent_id": DEFAULT_JUDGE_ID,
        },
    )
    assert r.status_code == 400
    assert r.json()["detail"]["code"] == "unknown_transcription_agent"


@pytest.mark.asyncio
async def test_rate_limited_stt_marks_run_failed():
    class LimitedSTT:
        async def transcribe(self, audio_path: str) -> str:
            raise RateLimitedError("Free-tier STT limit reached.")

    recording = {
        "id": "preload-01",
        "title": "Test",
        "audio_path": "data/preloaded/preload-01.wav",
        "all_ages_eligible": True,
    }
    run = await execute_run(
        recording=recording,
        transcription_agent_id=ALT_STT,
        judge_agent_id=DEFAULT_JUDGE_ID,
        stt=LimitedSTT(),
    )
    assert run["status"] == "failed"
    assert run["error_code"] == "rate_limited"
    assert "limit" in (run["error_message"] or "").lower()


def test_rate_limited_maps_to_429(client, monkeypatch):
    async def boom(**kwargs):
        from app.providers.errors import RateLimitedError

        raise RateLimitedError("Free-tier rate limit reached.")

    monkeypatch.setattr("app.api.runs.execute_run", boom)
    r = client.post(
        "/api/runs",
        json={
            "recording_id": "preload-01",
            "transcription_agent_id": ALT_STT,
            "judge_agent_id": DEFAULT_JUDGE_ID,
        },
    )
    assert r.status_code == 429
    assert r.json()["detail"]["code"] == "rate_limited"
