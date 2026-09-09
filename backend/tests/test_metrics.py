"""US6: dashboard metrics payload + mean rounding."""

from app.domain.aggregate import overall_percentage, round_display
from app.providers.catalog import DEFAULT_JUDGE_ID, DEFAULT_TRANSCRIPTION_ID


def test_empty_dashboard_null_overall(client):
    dash = client.get("/api/metrics/dashboard").json()
    assert dash["completed_count"] == 0
    assert dash["overall_percentage"] is None
    assert dash["scores"] == []
    ids = [g["id"] for g in dash["graph_views"]]
    assert ids == ["per_recording_bars", "overall_aggregate"]


def test_graph_views_and_mean_rounding(client):
    for rid, value_note in (("preload-01", None), ("preload-02", None)):
        r = client.post(
            "/api/runs",
            json={
                "recording_id": rid,
                "transcription_agent_id": DEFAULT_TRANSCRIPTION_ID,
                "judge_agent_id": DEFAULT_JUDGE_ID,
            },
        )
        assert r.status_code == 201, r.text

    dash = client.get("/api/metrics/dashboard").json()
    assert dash["completed_count"] == 2
    # Mock judge returns 88.0; mean of two is 88.0
    assert dash["overall_percentage"] == 88.0
    assert len(dash["scores"]) == 2
    for s in dash["scores"]:
        assert "transcription_agent_id" in s
        assert "judge_agent_id" in s
        assert "value" in s


def test_round_display_helper():
    assert round_display(None) is None
    assert round_display(87.56) == 87.6
    assert overall_percentage([]) is None
    assert overall_percentage([90.0, 80.0]) == 85.0
