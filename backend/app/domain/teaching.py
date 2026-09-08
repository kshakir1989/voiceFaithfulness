"""Static teaching messages for ingest → transcript → summary → judge → aggregate."""

from __future__ import annotations

MESSAGES = [
    {
        "id": "teach-ingest",
        "concept": "ingest",
        "body": "Ingest means choosing audio so the pipeline has a recording to study.",
    },
    {
        "id": "teach-transcript",
        "concept": "transcript",
        "body": "Speech-to-text writes the full conversation so later steps work on text, not raw audio.",
    },
    {
        "id": "teach-summary",
        "concept": "summary",
        "body": "A shorter summary is written from the transcript only.",
    },
    {
        "id": "teach-judge",
        "concept": "judge",
        "body": "An LLM-as-judge scores how faithful that summary is to the transcript (0–100).",
    },
    {
        "id": "teach-aggregate",
        "concept": "aggregate",
        "body": "The overall percentage is the average of completed recording scores.",
    },
]
