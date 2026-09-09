"""US4: audio preview URL and stream."""

from __future__ import annotations


def test_list_includes_audio_url(client):
    recs = client.get("/api/recordings").json()["recordings"]
    assert recs
    assert recs[0]["audio_url"] == f"/api/recordings/{recs[0]['id']}/audio"


def test_get_audio_stream(client):
    rid = client.get("/api/recordings").json()["recordings"][0]["id"]
    r = client.get(f"/api/recordings/{rid}/audio")
    assert r.status_code == 200
    assert len(r.content) > 0
    assert "audio" in (r.headers.get("content-type") or "") or r.headers.get("content-type")


def test_get_audio_missing_404(client):
    r = client.get("/api/recordings/does-not-exist/audio")
    assert r.status_code == 404
