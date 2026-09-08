"""US1 API contract: start run → completed score → dashboard mean."""

from app.providers.catalog import DEFAULT_JUDGE_ID, DEFAULT_TRANSCRIPTION_ID


def test_post_run_completes_with_mocks(client):
    body = {
        "recording_id": "preload-01",
        "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
        "judge_agent_id": DEFAULT_JUDGE_ID,
    }
    r = client.post("/api/runs", json=body)
    assert r.status_code == 201, r.text
    run = r.json()
    assert run["status"] == "completed"
    assert run["transcription_agent_id"] == DEFAULT_TRANSCRIPTION_ID
    assert run["judge_agent_id"] == DEFAULT_JUDGE_ID
    assert run["transcript"]
    assert run["summary"]
    assert run["score"]["value"] == 88.0
    stages = {s["name"]: s["status"] for s in run["stages"]}
    assert stages["transcript"] == "completed"
    assert stages["judge"] == "completed"
    assert stages["aggregate"] == "completed"


def test_dashboard_updates_after_run(client):
    body = {
        "recording_id": "preload-02",
        "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
        "judge_agent_id": DEFAULT_JUDGE_ID,
    }
    assert client.post("/api/runs", json=body).status_code == 201
    dash = client.get("/api/metrics/dashboard").json()
    assert dash["completed_count"] == 1
    assert dash["overall_percentage"] == 88.0
    assert dash["scores"][0]["recording_id"] == "preload-02"
    assert dash["scores"][0]["transcription_agent_id"] == DEFAULT_TRANSCRIPTION_ID


def test_two_runs_mean(client):
    for rid in ("preload-01", "preload-02"):
        r = client.post(
            "/api/runs",
            json={
                "recording_id": rid,
                "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
                "judge_agent_id": DEFAULT_JUDGE_ID,
            },
        )
        assert r.status_code == 201
    dash = client.get("/api/metrics/dashboard").json()
    assert dash["completed_count"] == 2
    assert dash["overall_percentage"] == 88.0


def test_missing_recording_404(client):
    r = client.post(
        "/api/runs",
        json={
            "recording_id": "missing",
            "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
            "judge_agent_id": DEFAULT_JUDGE_ID,
        },
    )
    assert r.status_code == 404
