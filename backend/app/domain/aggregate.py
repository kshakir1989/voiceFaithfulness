"""Overall % = arithmetic mean of completed faithfulness scores only."""

from __future__ import annotations

from statistics import fmean


def overall_percentage(scores: list[float]) -> float | None:
    """None when empty so the UI can show a neutral empty state (not a fake 0%)."""
    if not scores:
        return None
    return fmean(scores)


def round_display(value: float | None, digits: int = 1) -> float | None:
    """Ordinary display rounding for the dashboard."""
    if value is None:
        return None
    return round(value, digits)
