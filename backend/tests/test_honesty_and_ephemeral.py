"""Honesty mode + blocked demo recording + ephemeral uploads."""

from pathlib import Path

from app.providers.catalog import DEFAULT_JUDGE_ID, DEFAULT_TRANSCRIPTION_ID

PRELOAD_WAV = Path(__file__).resolve().parents[2] / "data" / "preloaded" / "preload-01.wav"


def test_health_reports_stub_mode(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["providers_mode"] == "stub"


def test_blocked_demo_listed_and_fails_run(client):
    recs = client.get("/api/recordings").json()["recordings"]
    blocked = next(r for r in recs if r["id"] == "preload-blocked")
    assert blocked["all_ages_eligible"] is False
    assert "Blocked" in blocked["title"]
    r = client.post(
        "/api/runs",
        json={
            "recording_id": "preload-blocked",
            "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
            "judge_agent_id": DEFAULT_JUDGE_ID,
        },
    )
    assert r.status_code == 403
    assert r.json()["detail"]["code"] == "all_ages_blocked"
    dash = client.get("/api/metrics/dashboard").json()
    assert dash["completed_count"] == 0


def test_upload_is_session_scoped_and_clearable(client):
    files = {"file": ("session-chat.wav", PRELOAD_WAV.read_bytes(), "audio/wav")}
    up = client.post("/api/recordings/upload", files=files, data={"title": "Session chat"})
    assert up.status_code == 201, up.text
    rid = up.json()["id"]
    listed = client.get("/api/recordings").json()["recordings"]
    assert any(r["id"] == rid for r in listed)
    assert any(r.get("ephemeral") for r in listed if r["id"] == rid)
    cleared = client.delete("/api/recordings/session")
    assert cleared.status_code == 200
    listed2 = client.get("/api/recordings").json()["recordings"]
    assert not any(r["id"] == rid for r in listed2)
    # Preloads remain
    assert any(r["id"] == "preload-01" for r in listed2)


def test_stubbed_flag_after_mock_score(client):
    assert (
        client.post(
            "/api/runs",
            json={
                "recording_id": "preload-01",
                "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
                "judge_agent_id": DEFAULT_JUDGE_ID,
            },
        ).status_code
        == 201
    )
    dash = client.get("/api/metrics/dashboard").json()
    assert dash["providers_mode"] == "stub"
    assert dash["scores_are_stubbed"] is True
