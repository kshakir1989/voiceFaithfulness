"""All-ages gate for titles/transcripts and basic upload checks."""

from __future__ import annotations

# Expand later; keep free (no paid moderation API).
BLOCKED_SUBSTRINGS = (
    "explicit violence",
    "adult content",
)


def is_all_ages_eligible(*, title: str = "", transcript: str = "") -> bool:
    hay = f"{title}\n{transcript}".lower()
    return not any(b in hay for b in BLOCKED_SUBSTRINGS)


def validate_audio_meta(*, size_bytes: int, content_type: str | None) -> tuple[bool, str | None]:
    """Reject empty or obviously non-audio uploads before the pipeline starts."""
    if size_bytes <= 0:
        return False, "Audio file is empty."
    if content_type and not (
        content_type.startswith("audio/") or content_type in {"application/octet-stream"}
    ):
        return False, "Unsupported audio type."
    return True, None
