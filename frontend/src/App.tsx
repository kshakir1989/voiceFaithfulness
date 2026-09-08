/**
 * US1 SPA: picker + STT/judge agents + run + stages + overall %.
 * Styled lightly from theme.ts (Figma frames still TBD).
 */
import { useCallback, useEffect, useState } from "react";
import { theme } from "./theme";

type Agent = { id: string; label: string; available: boolean };
type Recording = {
  id: string;
  title: string;
  source_type: string;
  duration_seconds?: number;
  all_ages_eligible: boolean;
};
type Stage = { name: string; status: string };
type Run = {
  id: string;
  status: string;
  stages: Stage[];
  transcript?: string | null;
  summary?: string | null;
  score?: { value: number; judge_agent_id: string } | null;
  error_message?: string | null;
  transcription_agent_id: string;
  judge_agent_id: string;
};
type Dashboard = {
  overall_percentage: number | null;
  completed_count: number;
  scores: Array<{
    recording_id: string;
    title: string;
    value: number;
    transcription_agent_id: string;
    judge_agent_id: string;
    run_id?: string;
  }>;
};

const emptyDash: Dashboard = { overall_percentage: null, completed_count: 0, scores: [] };

export default function App() {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [sttAgents, setSttAgents] = useState<Agent[]>([]);
  const [judgeAgents, setJudgeAgents] = useState<Agent[]>([]);
  const [recordingId, setRecordingId] = useState("");
  const [sttId, setSttId] = useState("");
  const [judgeId, setJudgeId] = useState("");
  const [run, setRun] = useState<Run | null>(null);
  const [dash, setDash] = useState<Dashboard>(emptyDash);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [teach, setTeach] = useState<string>("");

  const refreshDash = useCallback(async () => {
    const r = await fetch("/api/metrics/dashboard");
    if (r.ok) setDash(await r.json());
  }, []);

  useEffect(() => {
    void (async () => {
      const [recs, stt, judge, teaching] = await Promise.all([
        fetch("/api/recordings").then((r) => r.json()),
        fetch("/api/agents/transcription").then((r) => r.json()),
        fetch("/api/agents/judge").then((r) => r.json()),
        fetch("/api/teaching/messages").then((r) => r.json()),
      ]);
      setRecordings(recs.recordings ?? []);
      setSttAgents(stt.agents ?? []);
      setJudgeAgents(judge.agents ?? []);
      setRecordingId(recs.recordings?.[0]?.id ?? "");
      setSttId(stt.default_id ?? "");
      setJudgeId(judge.default_id ?? "");
      const ingest = (teaching.messages ?? []).find((m: { concept: string }) => m.concept === "ingest");
      setTeach(ingest?.body ?? "");
      await refreshDash();
    })();
  }, [refreshDash]);

  async function onRun() {
    setError(null);
    setBusy(true);
    setTeach("Speech-to-text writes the full conversation so later steps work on text, not raw audio.");
    try {
      const r = await fetch("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          recording_id: recordingId,
          transcription_agent_id: sttId,
          judge_agent_id: judgeId,
        }),
      });
      const body = await r.json();
      if (!r.ok) {
        const msg = body?.detail?.message || body?.message || "Run failed";
        setError(typeof msg === "string" ? msg : JSON.stringify(msg));
        setRun(null);
      } else {
        setRun(body);
        setTeach("The overall percentage is the average of completed recording scores.");
        await refreshDash();
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Network error");
    } finally {
      setBusy(false);
    }
  }

  const canRun = Boolean(recordingId && sttId && judgeId) && !busy;

  return (
    <main
      data-testid="vf-shell"
      style={{
        maxWidth: 720,
        margin: "0 auto",
        padding: theme.space * 2,
        color: theme.color.text,
        background: theme.color.background,
        minHeight: "100vh",
        fontFamily: "Georgia, 'Times New Roman', serif",
      }}
    >
      <h1 style={{ fontSize: "2rem", marginBottom: theme.space }}>voiceFaithfulness</h1>
      <p style={{ color: theme.color.textMuted, marginTop: 0 }} data-testid="vf-teach">
        {teach}
      </p>

      <section style={{ display: "grid", gap: theme.space * 1.5, marginBottom: theme.space * 2 }}>
        <label>
          Recording
          <select
            data-testid="vf-recording-picker"
            value={recordingId}
            onChange={(e) => setRecordingId(e.target.value)}
            style={{ display: "block", width: "100%", marginTop: 4 }}
          >
            {recordings.map((rec) => (
              <option key={rec.id} value={rec.id}>
                {rec.title}
              </option>
            ))}
          </select>
        </label>

        <label>
          Transcription agent (STT)
          <select
            data-testid="vf-agent-stt"
            value={sttId}
            onChange={(e) => setSttId(e.target.value)}
            style={{ display: "block", width: "100%", marginTop: 4 }}
          >
            {sttAgents.map((a) => (
              <option key={a.id} value={a.id}>
                {a.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Judge agent
          <select
            data-testid="vf-agent-judge"
            value={judgeId}
            onChange={(e) => setJudgeId(e.target.value)}
            style={{ display: "block", width: "100%", marginTop: 4 }}
          >
            {judgeAgents.map((a) => (
              <option key={a.id} value={a.id}>
                {a.label}
              </option>
            ))}
          </select>
        </label>

        <button
          data-testid="vf-run"
          type="button"
          disabled={!canRun}
          onClick={() => void onRun()}
          style={{
            background: theme.color.primary,
            color: "#fff",
            border: "none",
            padding: `${theme.space}px ${theme.space * 2}px`,
            cursor: canRun ? "pointer" : "not-allowed",
            opacity: canRun ? 1 : 0.5,
          }}
        >
          {busy ? "Running…" : "Run pipeline"}
        </button>
      </section>

      {error && (
        <p data-testid="vf-error" style={{ color: theme.color.danger }} role="alert">
          {error}
        </p>
      )}

      {run && (
        <section data-testid="vf-stages" style={{ marginBottom: theme.space * 2 }}>
          <h2 style={{ fontSize: "1.1rem" }}>Pipeline</h2>
          <ul>
            {run.stages.map((s) => (
              <li key={s.name}>
                {s.name}: {s.status}
              </li>
            ))}
          </ul>
          {run.score && (
            <p data-testid="vf-run-score">
              Score: {run.score.value} (judge: {run.judge_agent_id}; STT: {run.transcription_agent_id})
            </p>
          )}
        </section>
      )}

      <section data-testid="vf-overall" style={{ marginBottom: theme.space * 2 }}>
        <h2 style={{ fontSize: "1.1rem" }}>Overall</h2>
        <p>
          {dash.overall_percentage == null
            ? "No scores yet"
            : `${dash.overall_percentage}% (${dash.completed_count} completed)`}
        </p>
      </section>

      <section data-testid="vf-scores">
        <h2 style={{ fontSize: "1.1rem" }}>Scores</h2>
        <ul>
          {dash.scores.map((s) => (
            <li key={s.run_id ?? s.recording_id}>
              {s.title}: {s.value}%
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
