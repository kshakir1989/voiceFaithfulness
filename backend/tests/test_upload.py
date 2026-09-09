"""US4: multipart upload accept / all-ages block / bad file."""

from __future__ import annotations

from pathlib import Path

from app.providers.catalog import DEFAULT_JUDGE_ID, DEFAULT_TRANSCRIPTION_ID

PRELOAD_WAV = Path(__file__).resolve().parents[2] / "data" / "preloaded" / "preload-01.wav"


def test_upload_accepts_wav(client):
    assert PRELOAD_WAV.is_file()
    files = {"file": ("friendly-chat.wav", PRELOAD_WAV.read_bytes(), "audio/wav")}
    data = {"title": "Friendly chat"}
    r = client.post("/api/recordings/upload", files=files, data=data)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["source_type"] == "local"
    assert body["all_ages_eligible"] is True
    assert body["audio_url"].endswith("/audio")
    listed = client.get("/api/recordings").json()["recordings"]
    assert any(x["id"] == body["id"] for x in listed)


def test_upload_then_run(client):
    files = {"file": ("sample.wav", PRELOAD_WAV.read_bytes(), "audio/wav")}
    up = client.post("/api/recordings/upload", files=files, data={"title": "Sample"}).json()
    r = client.post(
        "/api/runs",
        json={
            "recording_id": up["id"],
            "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
            "judge_agent_id": DEFAULT_JUDGE_ID,
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["status"] == "completed"


def test_upload_all_ages_blocked(client):
    files = {"file": ("bad.wav", PRELOAD_WAV.read_bytes(), "audio/wav")}
    r = client.post(
        "/api/recordings/upload",
        files=files,
        data={"title": "Contains adult content"},
    )
    assert r.status_code == 403
    assert r.json()["detail"]["code"] == "all_ages_blocked"


def test_upload_empty_rejected(client):
    files = {"file": ("empty.wav", b"", "audio/wav")}
    r = client.post("/api/recordings/upload", files=files)
    assert r.status_code == 400
    assert r.json()["detail"]["code"] == "invalid_audio"
