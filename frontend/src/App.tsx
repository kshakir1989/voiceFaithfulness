/**
 * SPA: editorial learning flow — audio → transcript → summary → judge → aggregate.
 * Desktop: forced 5-column LTR stage board. Mobile: stacked stages.
 */
import { useCallback, useEffect, useMemo, useState, type CSSProperties, type ReactNode } from "react";
import { theme } from "./theme";
import { DashboardGraphs, type GraphViewId } from "./components/graphs/DashboardGraphs";

type Agent = {
  id: string;
  label: string;
  available: boolean;
  highlight?: boolean;
  owns_summary?: boolean;
  power_tier?: number;
};
type Recording = {
  id: string;
  title: string;
  source_type: string;
  duration_seconds?: number | null;
  all_ages_eligible: boolean;
  audio_url?: string;
  demo_fail?: boolean;
  ephemeral?: boolean;
};
type Stage = { name: string; status: string };
type RunScore = { value: number; judge_agent_id: string; rationale?: string | null };
type Run = {
  id: string;
  status: string;
  stages: Stage[];
  transcript?: string | null;
  summary?: string | null;
  score?: RunScore | null;
  error_message?: string | null;
  error_code?: string | null;
  transcription_agent_id: string;
  judge_agent_id: string;
  summary_owner_agent_id?: string;
  created_at?: string;
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
  graph_views?: Array<{ id: GraphViewId; label: string }>;
  providers_mode?: "stub" | "live";
  scores_are_stubbed?: boolean;
};

type TeachMsg = { id: string; concept: string; body: string };
type ViewMode = "desktop" | "mobile";

const emptyDash: Dashboard = { overall_percentage: null, completed_count: 0, scores: [] };
const PIPELINE_TEACH = ["transcript", "summary", "judge", "aggregate"] as const;
const VIEW_KEY = "vf_view_mode";

function initialViewMode(): ViewMode {
  try {
    const stored = sessionStorage.getItem(VIEW_KEY);
    if (stored === "desktop" || stored === "mobile") return stored;
  } catch {
    /* ignore */
  }
  if (typeof window !== "undefined" && window.matchMedia("(max-width: 900px)").matches) {
    return "mobile";
  }
  return "desktop";
}

function StageCard({
  num,
  title,
  children,
  testId,
}: {
  num: string;
  title: string;
  children: ReactNode;
  testId: string;
}) {
  return (
    <article data-testid={testId} className="vf-stage">
      <div className="vf-stage-num">{num}</div>
      <h2>{title}</h2>
      {children}
    </article>
  );
}

export default function App() {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [sttAgents, setSttAgents] = useState<Agent[]>([]);
  const [judgeAgents, setJudgeAgents] = useState<Agent[]>([]);
  const [recordingId, setRecordingId] = useState("");
  const [sttId, setSttId] = useState("");
  const [judgeId, setJudgeId] = useState("");
  const [run, setRun] = useState<Run | null>(null);
  const [history, setHistory] = useState<Run[]>([]);
  const [dash, setDash] = useState<Dashboard>(emptyDash);
  const [error, setError] = useState<string | null>(null);
  const [errorCode, setErrorCode] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [teach, setTeach] = useState<string>("");
  const [teachConcept, setTeachConcept] = useState<string>("");
  const [teachByConcept, setTeachByConcept] = useState<Record<string, string>>({});
  const [teachSeen, setTeachSeen] = useState<string[]>([]);
  const [graphView, setGraphView] = useState<GraphViewId>("per_recording_bars");
  const [providersMode, setProvidersMode] = useState<"stub" | "live">("stub");
  const [liveNotice, setLiveNotice] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>(initialViewMode);
  const [rationaleOpen, setRationaleOpen] = useState(false);

  const showTeach = useCallback(
    (concept: string, catalog?: Record<string, string>) => {
      const map = catalog ?? teachByConcept;
      const body = map[concept];
      if (!body) return;
      setTeach(body);
      setTeachConcept(concept);
      setTeachSeen((prev) => (prev.includes(concept) ? prev : [...prev, concept]));
    },
    [teachByConcept],
  );

  const presentPipelineTeaching = useCallback(async (catalog: Record<string, string>) => {
    for (const concept of PIPELINE_TEACH) {
      const body = catalog[concept];
      if (!body) continue;
      setTeach(body);
      setTeachConcept(concept);
      setTeachSeen((prev) => (prev.includes(concept) ? prev : [...prev, concept]));
      await new Promise((r) => setTimeout(r, 120));
    }
  }, []);

  const selected = useMemo(
    () => recordings.find((r) => r.id === recordingId) ?? null,
    [recordings, recordingId],
  );
  const previewUrl = selected?.audio_url ?? "";

  const setView = (mode: ViewMode) => {
    setViewMode(mode);
    try {
      sessionStorage.setItem(VIEW_KEY, mode);
    } catch {
      /* ignore */
    }
  };

  const refreshRecordings = useCallback(async (preferId?: string) => {
    const r = await fetch("/api/recordings", { credentials: "include" });
    if (!r.ok) return;
    const body = await r.json();
    const list: Recording[] = body.recordings ?? [];
    setRecordings(list);
    setRecordingId((cur) => {
      if (preferId) return preferId;
      if (cur && list.some((x) => x.id === cur)) return cur;
      const firstOk = list.find((x) => x.all_ages_eligible)?.id;
      return firstOk || list[0]?.id || "";
    });
  }, []);

  const refreshDash = useCallback(async () => {
    const r = await fetch("/api/metrics/dashboard", { credentials: "include" });
    if (!r.ok) return;
    const body = (await r.json()) as Dashboard;
    setDash(body);
    if (body.providers_mode === "live") setProvidersMode("live");
    else if (body.providers_mode === "stub") setProvidersMode("stub");
  }, []);

  const refreshHistory = useCallback(async () => {
    const r = await fetch("/api/runs", { credentials: "include" });
    if (!r.ok) return;
    const body = await r.json();
    setHistory((body.runs ?? []) as Run[]);
  }, []);

  useEffect(() => {
    const clearUploads = () => {
      void fetch("/api/recordings/session", {
        method: "DELETE",
        credentials: "include",
        keepalive: true,
      });
    };
    window.addEventListener("pagehide", clearUploads);
    return () => window.removeEventListener("pagehide", clearUploads);
  }, []);

  useEffect(() => {
    void (async () => {
      const [stt, judge, teaching, health] = await Promise.all([
        fetch("/api/agents/transcription", { credentials: "include" }).then((r) => r.json()),
        fetch("/api/agents/judge", { credentials: "include" }).then((r) => r.json()),
        fetch("/api/teaching/messages", { credentials: "include" }).then((r) => r.json()),
        fetch("/api/health", { credentials: "include" }).then((r) => r.json()),
      ]);
      setSttAgents(stt.agents ?? []);
      setJudgeAgents(judge.agents ?? []);
      setSttId(stt.default_id ?? "");
      setJudgeId(judge.default_id ?? "");
      const mode = health.providers_mode === "live" ? "live" : "stub";
      setProvidersMode(mode);
      if (mode === "live") {
        setLiveNotice("Live providers are active — scores come from real STT/summary/judge calls.");
      }
      const map: Record<string, string> = {};
      for (const m of (teaching.messages ?? []) as TeachMsg[]) {
        map[m.concept] = m.body;
      }
      setTeachByConcept(map);
      const ingestBody = map.ingest ?? "";
      setTeach(ingestBody);
      setTeachConcept("ingest");
      setTeachSeen(ingestBody ? ["ingest"] : []);
      await refreshRecordings();
      await refreshDash();
      await refreshHistory();
    })();
  }, [refreshDash, refreshHistory, refreshRecordings]);

  async function onUpload(file: File | null) {
    if (!file) return;
    setError(null);
    setErrorCode(null);
    const form = new FormData();
    form.append("file", file);
    form.append("title", file.name.replace(/\.[^.]+$/, "") || "Local recording");
    const r = await fetch("/api/recordings/upload", {
      method: "POST",
      body: form,
      credentials: "include",
    });
    const body = await r.json();
    if (!r.ok) {
      const detail = body?.detail;
      const msg = (typeof detail === "object" && detail?.message) || "Upload failed";
      setError(typeof msg === "string" ? msg : JSON.stringify(msg));
      setErrorCode(typeof detail === "object" ? detail?.code ?? null : null);
      return;
    }
    await refreshRecordings(body.id);
    showTeach("ingest");
  }

  async function onRun() {
    setError(null);
    setErrorCode(null);
    setBusy(true);
    setRationaleOpen(false);
    showTeach("transcript");
    try {
      const r = await fetch("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          recording_id: recordingId,
          transcription_agent_id: sttId,
          judge_agent_id: judgeId,
        }),
      });
      const body = await r.json();
      if (!r.ok) {
        const detail = body?.detail;
        const code = typeof detail === "object" ? detail?.code : null;
        const msg =
          (typeof detail === "object" && detail?.message) || body?.message || "Run failed";
        setError(typeof msg === "string" ? msg : JSON.stringify(msg));
        setErrorCode(typeof code === "string" ? code : null);
        if (typeof detail === "object" && detail?.run) setRun(detail.run);
        else setRun(null);
        await refreshDash();
        await refreshHistory();
      } else if (body.status === "failed") {
        setRun(body);
        setError(body.error_message || body.error_code || "Run failed");
        setErrorCode(body.error_code || "provider_error");
        await refreshDash();
        await refreshHistory();
      } else {
        setRun(body);
        await presentPipelineTeaching(teachByConcept);
        await refreshDash();
        await refreshHistory();
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Network error");
      setErrorCode("network_error");
    } finally {
      setBusy(false);
    }
  }

  async function onClearDemo() {
    if (!window.confirm("Clear session runs, scores, and uploads? Preloaded demos stay.")) return;
    setError(null);
    const r = await fetch("/api/demo/session", { method: "DELETE", credentials: "include" });
    if (!r.ok) {
      setError("Could not clear demo data");
      return;
    }
    setRun(null);
    setHistory([]);
    setRationaleOpen(false);
    await refreshRecordings();
    await refreshDash();
    await refreshHistory();
  }

  const canRun = Boolean(recordingId && sttId && judgeId) && !busy;
  const graphViews = dash.graph_views?.length
    ? dash.graph_views
    : [
        { id: "per_recording_bars" as const, label: "Per-recording scores" },
        { id: "overall_aggregate" as const, label: "Overall aggregate" },
      ];
  const rationale = run?.score?.rationale ?? null;
  const stageStatus = (name: string) => run?.stages.find((s) => s.name === name)?.status;

  const shellStyle: CSSProperties = {
    width: "100%",
    maxWidth: viewMode === "desktop" ? 1280 : 640,
    margin: "0 auto",
    padding: `max(${theme.space * 2}px, env(safe-area-inset-top)) max(${theme.space * 2}px, env(safe-area-inset-right)) max(${theme.space * 3}px, env(safe-area-inset-bottom)) max(${theme.space * 2}px, env(safe-area-inset-left))`,
    color: theme.color.text,
    fontFamily: theme.font.body,
    minHeight: "100vh",
  };

  const controlsStyle: CSSProperties =
    viewMode === "desktop"
      ? {
          display: "grid",
          gridTemplateColumns: "1.2fr 1fr 1fr auto",
          gap: theme.space * 1.5,
          alignItems: "end",
          marginBottom: theme.space * 2,
          padding: theme.space * 1.5,
          background: theme.color.surfaceRaised,
          border: `1px solid ${theme.color.line}`,
        }
      : {
          display: "grid",
          gap: theme.space * 1.25,
          marginBottom: theme.space * 2,
          padding: theme.space * 1.5,
          background: theme.color.surfaceRaised,
          border: `1px solid ${theme.color.line}`,
        };

  return (
    <main data-testid="vf-shell" data-view-mode={viewMode} style={shellStyle}>
      <header
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: theme.space,
          alignItems: "baseline",
          justifyContent: "space-between",
          marginBottom: theme.space * 2,
          borderBottom: `1px solid ${theme.color.line}`,
          paddingBottom: theme.space * 1.5,
        }}
      >
        <div>
          <p
            style={{
              margin: 0,
              fontFamily: theme.font.mono,
              fontSize: "0.7rem",
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: theme.color.textMuted,
            }}
          >
            LLM-as-judge lesson
          </p>
          <h1
            style={{
              fontFamily: theme.font.display,
              fontSize: "clamp(2rem, 4vw, 2.75rem)",
              fontWeight: 600,
              margin: "0.15rem 0 0",
              letterSpacing: "-0.02em",
              color: theme.color.ink,
            }}
          >
            voiceFaithfulness
          </h1>
        </div>
        <div data-testid="vf-view-toggle" role="group" aria-label="Layout view">
          <button
            type="button"
            data-testid="vf-view-desktop"
            aria-pressed={viewMode === "desktop"}
            onClick={() => setView("desktop")}
            style={{ marginRight: 6 }}
          >
            Desktop · LTR
          </button>
          <button
            type="button"
            data-testid="vf-view-mobile"
            aria-pressed={viewMode === "mobile"}
            onClick={() => setView("mobile")}
          >
            Mobile · stack
          </button>
        </div>
      </header>

      <p
        data-testid="vf-providers-mode"
        role="status"
        style={{
          marginTop: 0,
          padding: `${theme.space}px ${theme.space * 1.5}px`,
          background: providersMode === "stub" ? theme.color.dangerSoft : theme.color.primarySoft,
          borderLeft: `3px solid ${providersMode === "stub" ? theme.color.danger : theme.color.primary}`,
        }}
      >
        {providersMode === "stub"
          ? "Stub mode: scores and transcripts are demo placeholders (mocks), not real audio analysis. Set GROQ_API_KEY and unset FORCE_MOCK_PROVIDERS for live data."
          : "Live mode: providers are active. Scores reflect real STT → summary → judge calls."}
      </p>

      {liveNotice && providersMode === "live" ? (
        <p data-testid="vf-live-notice" role="status" style={{ color: theme.color.primary }}>
          {liveNotice}
        </p>
      ) : null}

      {dash.scores_are_stubbed ? (
        <p data-testid="vf-stub-scores" role="status" style={{ color: theme.color.danger }}>
          Dashboard percentages are stubbed (mock judge). They are not faithfulness of your audio.
        </p>
      ) : null}

      <p style={{ color: theme.color.textMuted, marginTop: 0 }} data-testid="vf-teach" data-concept={teachConcept}>
        {teach}
      </p>
      <p
        data-testid="vf-teach-log"
        style={{
          color: theme.color.textMuted,
          fontSize: "0.8rem",
          marginTop: 0,
          fontFamily: theme.font.mono,
        }}
        aria-live="polite"
      >
        Concepts: {teachSeen.join(" · ") || "none yet"}
      </p>

      <section style={controlsStyle} data-testid="vf-controls">
        <label style={{ display: "block" }}>
          Recording
          <select
            data-testid="vf-recording-picker"
            value={recordingId}
            onChange={(e) => setRecordingId(e.target.value)}
            style={{ display: "block", width: "100%", marginTop: 4, padding: 6 }}
          >
            {recordings.map((rec) => (
              <option key={rec.id} value={rec.id}>
                {rec.title}
                {rec.ephemeral ? " · session upload" : ""}
              </option>
            ))}
          </select>
        </label>

        <label style={{ display: "block" }}>
          Transcription agent
          <select
            data-testid="vf-agent-stt"
            value={sttId}
            onChange={(e) => setSttId(e.target.value)}
            style={{ display: "block", width: "100%", marginTop: 4, padding: 6 }}
          >
            {sttAgents.map((a) => (
              <option key={a.id} value={a.id} disabled={!a.available}>
                {a.label}
                {!a.available ? " (unavailable)" : ""}
              </option>
            ))}
          </select>
        </label>

        <label style={{ display: "block" }}>
          Judge agent
          <select
            data-testid="vf-agent-judge"
            value={judgeId}
            onChange={(e) => setJudgeId(e.target.value)}
            style={{ display: "block", width: "100%", marginTop: 4, padding: 6 }}
          >
            {judgeAgents.map((a) => (
              <option key={a.id} value={a.id} disabled={!a.available}>
                {a.highlight ? "★ " : ""}
                {a.label}
                {a.highlight ? " (stronger)" : ""}
                {!a.available ? " (unavailable)" : ""}
              </option>
            ))}
          </select>
        </label>

        <div style={{ display: "flex", flexWrap: "wrap", gap: theme.space, alignItems: "center" }}>
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
              opacity: canRun ? 1 : 0.5,
            }}
          >
            {busy ? "Running…" : "Run pipeline"}
          </button>
          <button
            data-testid="vf-demo-reset"
            type="button"
            onClick={() => void onClearDemo()}
            style={{
              background: "transparent",
              border: `1px solid ${theme.color.line}`,
              padding: `${theme.space}px ${theme.space * 1.5}px`,
            }}
          >
            Clear demo
          </button>
        </div>
      </section>

      {previewUrl ? (
        <div style={{ marginBottom: theme.space * 2 }}>
          <div
            style={{
              fontFamily: theme.font.mono,
              fontSize: "0.7rem",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              color: theme.color.textMuted,
              marginBottom: 4,
            }}
          >
            Preview
          </div>
          <audio data-testid="vf-audio-preview" controls src={previewUrl} style={{ width: "100%" }}>
            Your browser does not support audio.
          </audio>
          <label style={{ display: "block", marginTop: theme.space, fontSize: "0.9rem" }}>
            Add local recording
            <input
              data-testid="vf-upload"
              type="file"
              accept="audio/*"
              style={{ display: "block", marginTop: 4 }}
              onChange={(e) => void onUpload(e.target.files?.[0] ?? null)}
            />
          </label>
        </div>
      ) : null}

      {error && (
        <p
          data-testid="vf-error"
          data-error-code={errorCode ?? undefined}
          style={{
            color: theme.color.danger,
            background: theme.color.dangerSoft,
            borderLeft: `3px solid ${theme.color.danger}`,
            padding: theme.space,
          }}
          role="alert"
        >
          {errorCode ? `[${errorCode}] ` : ""}
          {error}
        </p>
      )}

      <p
        style={{
          fontFamily: theme.font.mono,
          fontSize: "0.7rem",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          color: theme.color.textMuted,
          marginBottom: theme.space,
        }}
      >
        Pipeline · {viewMode === "desktop" ? "left → right" : "stacked"}
      </p>

      <div data-testid="vf-flow" data-layout={viewMode}>
        <StageCard num="01" title="Source" testId="vf-stage-source">
          <p style={{ margin: 0, fontSize: "0.85rem", color: theme.color.textMuted }}>
            {selected?.title ?? "Choose a recording"}
          </p>
          <p style={{ margin: 0, fontFamily: theme.font.mono, fontSize: "0.75rem" }}>
            ingest: {stageStatus("ingest") ?? "idle"}
          </p>
        </StageCard>

        <StageCard num="02" title="Transcript" testId="vf-stage-transcript">
          <p style={{ margin: 0, fontSize: "0.75rem", color: theme.color.textMuted }} data-testid="vf-transcript-owner">
            {run ? `Agent: ${run.transcription_agent_id}` : "Awaiting run"}
          </p>
          <pre data-testid="vf-transcript" className="vf-stage-body">
            {run?.transcript || "—"}
          </pre>
          <p style={{ margin: 0, fontFamily: theme.font.mono, fontSize: "0.75rem" }}>
            {stageStatus("transcript") ?? "idle"}
          </p>
        </StageCard>

        <StageCard num="03" title="Summary" testId="vf-stage-summary">
          <p style={{ margin: 0, fontSize: "0.75rem", color: theme.color.textMuted }} data-testid="vf-summary-owner">
            {run
              ? `Agent: ${run.summary_owner_agent_id || run.transcription_agent_id}`
              : "Owned by transcription agent"}
          </p>
          <div data-testid="vf-rationale">
            <pre
              data-testid="vf-summary"
              className="vf-stage-body"
              title={rationale || "No rationale yet"}
              onMouseEnter={() => rationale && setRationaleOpen(true)}
            >
              {run?.summary || "—"}
            </pre>
            <button
              type="button"
              data-testid="vf-rationale-toggle"
              onClick={() => setRationaleOpen((o) => !o)}
              style={{
                marginTop: 4,
                border: "none",
                background: "transparent",
                color: theme.color.primary,
                padding: 0,
                textDecoration: "underline",
                fontSize: "0.85rem",
              }}
            >
              Why this score?
            </button>
            {rationaleOpen ? (
              <pre data-testid="vf-rationale-text" className="vf-stage-body" style={{ marginTop: 6 }}>
                {rationale || "No rationale available for this run."}
              </pre>
            ) : null}
          </div>
          <p style={{ margin: 0, fontFamily: theme.font.mono, fontSize: "0.75rem" }}>
            {stageStatus("summary") ?? "idle"}
          </p>
        </StageCard>

        <StageCard num="04" title="Judge" testId="vf-stage-judge">
          {run?.score ? (
            <p data-testid="vf-run-score" style={{ margin: 0, fontFamily: theme.font.display, fontSize: "1.75rem" }}>
              {run.score.value}
              <span style={{ fontSize: "0.9rem", color: theme.color.textMuted }}> / 100</span>
            </p>
          ) : (
            <p style={{ margin: 0, color: theme.color.textMuted }}>—</p>
          )}
          <p style={{ margin: 0, fontSize: "0.75rem", color: theme.color.textMuted }}>
            judge: <span data-testid="vf-run-judge">{run?.judge_agent_id ?? "—"}</span>
            <br />
            STT: <span data-testid="vf-run-stt">{run?.transcription_agent_id ?? "—"}</span>
          </p>
          <ul data-testid="vf-stages" style={{ margin: 0, paddingLeft: "1.1rem", fontSize: "0.8rem" }}>
            {(run?.stages ?? []).map((s) => (
              <li key={s.name}>
                {s.name}: {s.status}
              </li>
            ))}
          </ul>
        </StageCard>

        <StageCard num="05" title="Overall" testId="vf-overall">
          <p style={{ margin: 0, fontFamily: theme.font.display, fontSize: "1.75rem" }}>
            {dash.overall_percentage == null ? "—" : `${dash.overall_percentage}%`}
          </p>
          <p style={{ margin: 0, fontSize: "0.85rem", color: theme.color.textMuted }}>
            {dash.overall_percentage == null
              ? "No scores yet"
              : `${dash.completed_count} completed judgement${dash.completed_count === 1 ? "" : "s"}`}
          </p>
        </StageCard>
      </div>

      <section data-testid="vf-history" style={{ marginTop: theme.space * 3, marginBottom: theme.space * 2 }}>
        <h2 style={{ fontFamily: theme.font.display, fontSize: "1.25rem", marginBottom: theme.space }}>
          Session history
        </h2>
        {history.length === 0 ? (
          <p data-testid="vf-history-empty" style={{ color: theme.color.textMuted }}>
            No runs yet
          </p>
        ) : (
          <ol style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {history.map((h, i) => (
              <li
                key={h.id}
                data-testid="vf-history-row"
                style={{
                  borderTop: `1px solid ${theme.color.line}`,
                  padding: `${theme.space}px 0`,
                  display: "grid",
                  gridTemplateColumns: viewMode === "desktop" ? "3rem 1fr" : "2.5rem 1fr",
                  gap: theme.space,
                }}
              >
                <span style={{ fontFamily: theme.font.mono, color: theme.color.textMuted }}>
                  {String(i + 1).padStart(2, "0")}
                </span>
                <button
                  type="button"
                  onClick={() => {
                    setRun(h);
                    setRationaleOpen(false);
                  }}
                  style={{
                    background: "transparent",
                    border: "none",
                    padding: 0,
                    color: theme.color.primary,
                    textAlign: "left",
                    fontFamily: "inherit",
                  }}
                >
                  {h.status} — STT {h.transcription_agent_id}; judge {h.judge_agent_id}
                  {h.score ? ` — ${h.score.value}%` : ""}
                  {h.summary ? (
                    <span style={{ display: "block", color: theme.color.textMuted, fontSize: "0.85rem" }}>
                      {h.summary.slice(0, 140)}
                      {h.summary.length > 140 ? "…" : ""}
                    </span>
                  ) : null}
                </button>
              </li>
            ))}
          </ol>
        )}
      </section>

      <DashboardGraphs
        views={graphViews}
        selected={graphView}
        onSelect={setGraphView}
        scores={dash.scores}
        overallPercentage={dash.overall_percentage}
        completedCount={dash.completed_count}
      />

      <section data-testid="vf-scores" style={{ marginTop: theme.space * 2 }}>
        <h2 style={{ fontFamily: theme.font.display, fontSize: "1.25rem" }}>Scores</h2>
        <ul>
          {dash.scores.map((s) => (
            <li key={s.run_id ?? s.recording_id} data-testid="vf-score-row">
              {s.title}: {s.value}% — STT: {s.transcription_agent_id}; judge: {s.judge_agent_id}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
