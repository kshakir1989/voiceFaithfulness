from app.providers.catalog import DEFAULT_JUDGE_ID, DEFAULT_TRANSCRIPTION_ID


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_transcription_catalog(client):
    r = client.get("/api/agents/transcription")
    assert r.status_code == 200
    body = r.json()
    assert body["default_id"] == DEFAULT_TRANSCRIPTION_ID
    assert len(body["agents"]) >= 5


def test_judge_catalog(client):
    r = client.get("/api/agents/judge")
    assert r.status_code == 200
    body = r.json()
    assert body["default_id"] == DEFAULT_JUDGE_ID


def test_dashboard_empty(client):
    r = client.get("/api/metrics/dashboard")
    assert r.status_code == 200
    body = r.json()
    assert body["overall_percentage"] is None
    assert body["completed_count"] == 0
    assert len(body["graph_views"]) >= 2


def test_teaching_messages(client):
    r = client.get("/api/teaching/messages")
    assert r.status_code == 200
    concepts = {m["concept"] for m in r.json()["messages"]}
    assert concepts == {"ingest", "transcript", "summary", "judge", "aggregate"}
