"""SQLite schema for recordings, runs, stages, and score artifacts."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parents[3] / "data" / "voicefaithfulness.db"

# Keep DDL here so connect() can bootstrap a fresh local DB.
SCHEMA = """
CREATE TABLE IF NOT EXISTS recordings (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  source_type TEXT NOT NULL,
  audio_path TEXT NOT NULL,
  duration_seconds REAL,
  all_ages_eligible INTEGER NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
  id TEXT PRIMARY KEY,
  recording_id TEXT NOT NULL,
  transcription_agent_id TEXT NOT NULL,
  judge_agent_id TEXT NOT NULL,
  summarizer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  error_message TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (recording_id) REFERENCES recordings(id)
);

CREATE TABLE IF NOT EXISTS pipeline_stages (
  run_id TEXT NOT NULL,
  name TEXT NOT NULL,
  status TEXT NOT NULL,
  started_at TEXT,
  finished_at TEXT,
  detail TEXT,
  PRIMARY KEY (run_id, name),
  FOREIGN KEY (run_id) REFERENCES pipeline_runs(id)
);

CREATE TABLE IF NOT EXISTS transcripts (
  run_id TEXT PRIMARY KEY,
  text TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  FOREIGN KEY (run_id) REFERENCES pipeline_runs(id)
);

CREATE TABLE IF NOT EXISTS summaries (
  run_id TEXT PRIMARY KEY,
  text TEXT NOT NULL,
  summarizer_id TEXT NOT NULL,
  FOREIGN KEY (run_id) REFERENCES pipeline_runs(id)
);

CREATE TABLE IF NOT EXISTS faithfulness_scores (
  run_id TEXT PRIMARY KEY,
  recording_id TEXT NOT NULL,
  value REAL NOT NULL,
  judge_agent_id TEXT NOT NULL,
  rationale TEXT,
  FOREIGN KEY (run_id) REFERENCES pipeline_runs(id)
);
"""


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    """Open DB and ensure tables exist."""
    path = db_path or DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
