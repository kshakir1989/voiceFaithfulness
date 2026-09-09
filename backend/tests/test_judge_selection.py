"""US3: selected judge agent is stored and used for scoring."""

from __future__ import annotations

import pytest

from app.domain.runner import execute_run
from app.providers.catalog import DEFAULT_TRANSCRIPTION_ID, JUDGE_AGENTS
from app.providers.mocks import MockJudge

ALT_JUDGE = "groq-llama-4-scout"


def test_run_stores_selected_judge_agent(client):
    assert ALT_JUDGE != JUDGE_AGENTS[0]["id"]
    body = {
        "recording_id": "preload-01",
        "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
        "judge_agent_id": ALT_JUDGE,
    }
    r = client.post("/api/runs", json=body)
    assert r.status_code == 201, r.text
    run = r.json()
    assert run["judge_agent_id"] == ALT_JUDGE
    assert run["score"]["judge_agent_id"] == ALT_JUDGE
    assert run["status"] == "completed"


@pytest.mark.asyncio
async def test_mock_judge_receives_selected_agent_id():
    judge = MockJudge(agent_id=ALT_JUDGE)
    recording = {
        "id": "preload-01",
        "title": "Test",
        "audio_path": "data/preloaded/preload-01.wav",
        "all_ages_eligible": True,
    }
    run = await execute_run(
        recording=recording,
        transcription_agent_id=DEFAULT_TRANSCRIPTION_ID,
        judge_agent_id=ALT_JUDGE,
        judge=judge,
    )
    assert run["judge_agent_id"] == ALT_JUDGE
    assert judge.agent_ids == [ALT_JUDGE]


def test_unknown_judge_agent_rejected(client):
    r = client.post(
        "/api/runs",
        json={
            "recording_id": "preload-01",
            "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
            "judge_agent_id": "not-a-real-judge",
        },
    )
    assert r.status_code == 400
    assert r.json()["detail"]["code"] == "unknown_judge_agent"


def test_dashboard_score_includes_judge_agent(client):
    body = {
        "recording_id": "preload-03",
        "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
        "judge_agent_id": ALT_JUDGE,
    }
    assert client.post("/api/runs", json=body).status_code == 201
    dash = client.get("/api/metrics/dashboard").json()
    assert dash["scores"][0]["judge_agent_id"] == ALT_JUDGE
