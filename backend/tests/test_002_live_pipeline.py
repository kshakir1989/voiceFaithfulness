"""002: catalog size, summary ownership, demo reset, rationale."""

from __future__ import annotations

import pytest

from app.domain.runner import execute_run
from app.domain.store import store
from app.providers.catalog import DEFAULT_JUDGE_ID, DEFAULT_TRANSCRIPTION_ID
from app.providers.mocks import MockJudge, MockSTT, MockSummarizer


def test_transcription_catalog_has_five_and_owns_summary(client):
    r = client.get("/api/agents/transcription")
    assert r.status_code == 200
    body = r.json()
    assert len(body["agents"]) == 5
    assert all(a.get("owns_summary") is True for a in body["agents"])


def test_judge_catalog_highlights_stronger(client):
    r = client.get("/api/agents/judge")
    assert r.status_code == 200
    body = r.json()
    highlighted = [a for a in body["agents"] if a.get("highlight")]
    assert len(highlighted) >= 1
    assert all("power_tier" in a for a in body["agents"])


@pytest.mark.asyncio
async def test_summary_owned_by_transcription_agent():
    recording = {
        "id": "rec-1",
        "title": "Demo",
        "audio_path": "missing.wav",
        "all_ages_eligible": True,
    }
    run = await execute_run(
        recording=recording,
        transcription_agent_id=DEFAULT_TRANSCRIPTION_ID,
        judge_agent_id=DEFAULT_JUDGE_ID,
        stt=MockSTT(agent_id=DEFAULT_TRANSCRIPTION_ID),
        summarizer=MockSummarizer(agent_id=DEFAULT_TRANSCRIPTION_ID),
        judge=MockJudge(),
    )
    assert run["status"] == "completed"
    assert run["summary_owner_agent_id"] == DEFAULT_TRANSCRIPTION_ID
    assert DEFAULT_TRANSCRIPTION_ID in (run["summary"] or "")
    assert run["score"]["rationale"]


def test_list_runs_history(client):
    # seed via store after a mock run is awkward through API without preload; use store
    store.runs["r1"] = {
        "id": "r1",
        "recording_id": "x",
        "transcription_agent_id": "a",
        "judge_agent_id": "b",
        "status": "completed",
        "created_at": "2026-09-09T12:00:00+00:00",
        "stages": [],
        "transcript": "t",
        "summary": "s",
        "score": {"value": 90, "judge_agent_id": "b", "rationale": "ok"},
    }
    r = client.get("/api/runs")
    assert r.status_code == 200
    assert any(x["id"] == "r1" for x in r.json()["runs"])


def test_demo_session_clear(client):
    store.scores.append({"recording_id": "x", "value": 80, "title": "t"})
    store.runs["r1"] = {
        "id": "r1",
        "created_at": "2026-09-09T12:00:00+00:00",
        "status": "completed",
    }
    r = client.delete("/api/demo/session")
    assert r.status_code == 200
    assert r.json()["ok"] is True
    assert store.list_scores() == []
    assert store.list_runs() == []
