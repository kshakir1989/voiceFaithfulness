"""Dashboard aggregate payload (mean of completed scores + graph view ids)."""

from fastapi import APIRouter

from app.domain.aggregate import overall_percentage, round_display
from app.domain.store import store

router = APIRouter(tags=["metrics"])


@router.get("/metrics/dashboard")
def dashboard() -> dict:
    scores = store.list_scores()
    values = [float(s["value"]) for s in scores]
    overall = round_display(overall_percentage(values))
    return {
        "overall_percentage": overall,  # null => "No scores yet" in UI
        "completed_count": len(values),
        "scores": scores,
        "graph_views": [
            {"id": "per_recording_bars", "label": "Per-recording scores"},
            {"id": "overall_aggregate", "label": "Overall aggregate"},
        ],
    }
