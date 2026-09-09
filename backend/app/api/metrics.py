"""Dashboard aggregate payload (mean of completed scores + graph view ids)."""

from fastapi import APIRouter

from app.domain.aggregate import overall_percentage, round_display
from app.domain.mode import providers_mode
from app.domain.store import store

router = APIRouter(tags=["metrics"])


@router.get("/metrics/dashboard")
def dashboard() -> dict:
    scores = store.list_scores()
    values = [float(s["value"]) for s in scores]
    overall = round_display(overall_percentage(values))
    mode = providers_mode()
    return {
        "overall_percentage": overall,
        "completed_count": len(values),
        "scores": scores,
        "graph_views": [
            {"id": "per_recording_bars", "label": "Per-recording scores"},
            {"id": "overall_aggregate", "label": "Overall aggregate"},
        ],
        "providers_mode": mode,
        "scores_are_stubbed": mode == "stub" and len(values) > 0,
    }
