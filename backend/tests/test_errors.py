"""US7: rate limit and run-in-progress API errors; no fabricated scores."""

from __future__ import annotations

import pytest

from app.domain.store import store
from app.providers.catalog import DEFAULT_JUDGE_ID, DEFAULT_TRANSCRIPTION_ID
from app.providers.errors import RateLimitedError


def _body(recording_id: str = "preload-01") -> dict:
    return {
        "recording_id": recording_id,
        "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
        "judge_agent_id": DEFAULT_JUDGE_ID,
    }


def test_run_in_progress_returns_409(client):
    store.active_run_id = "fake-active"
    r = client.post("/api/runs", json=_body())
    assert r.status_code == 409
    assert r.json()["detail"]["code"] == "run_in_progress"
    dash = client.get("/api/metrics/dashboard").json()
    assert dash["completed_count"] == 0


def test_rate_limited_returns_429_and_no_score(client, monkeypatch):
    async def boom(**kwargs):
        raise RateLimitedError("Free-tier rate limit reached. Try another agent or wait.")

    monkeypatch.setattr("app.api.runs.execute_run", boom)
    before = client.get("/api/metrics/dashboard").json()["completed_count"]
    r = client.post("/api/runs", json=_body())
    assert r.status_code == 429
    detail = r.json()["detail"]
    assert detail["code"] == "rate_limited"
    assert "limit" in detail["message"].lower()
    after = client.get("/api/metrics/dashboard").json()
    assert after["completed_count"] == before


@pytest.mark.asyncio
async def test_mid_run_rate_limit_does_not_aggregate():
    from app.domain.runner import execute_run

    class LimitedSTT:
        async def transcribe(self, audio_path: str) -> str:
            raise RateLimitedError()

    before = len(store.list_scores())
    run = await execute_run(
        recording={
            "id": "preload-01",
            "title": "Test",
            "audio_path": "data/preloaded/preload-01.wav",
            "all_ages_eligible": True,
        },
        transcription_agent_id=DEFAULT_TRANSCRIPTION_ID,
        judge_agent_id=DEFAULT_JUDGE_ID,
        stt=LimitedSTT(),
    )
    assert run["status"] == "failed"
    assert run["error_code"] == "rate_limited"
    assert len(store.list_scores()) == before
