/**
 * SPA: picker + upload + preview + STT/judge + run + transcript/summary +
 * rationale + history + layout toggle + demo reset (002 live pipeline flow).
 */
import { useCallback, useEffect, useMemo, useState } from "react";
import { DashboardGraphs, type GraphViewId } from "./components/graphs/DashboardGraphs";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CircularProgress } from "@/components/ui/circular-progress";
import {
  Stepper,
  StepperDescription,
  StepperIndicator,
  StepperItem,
  StepperSeparator,
  StepperTitle,
  StepperTrigger,
} from "@/components/ui/stepper";

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

const selectClass =
  "mt-1 flex h-9 w-full rounded-lg border border-input bg-card px-2.5 text-sm outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50";

const panelClass =
  "max-h-40 overflow-auto whitespace-pre-wrap rounded-lg bg-muted/60 p-3 font-mono text-sm";

function initialViewMode(): ViewMode {
  try {
    const stored = sessionStorage.getItem(VIEW_KEY);
    if (stored === "desktop" || stored === "mobile") return stored;
  } catch {
    /* ignore */
  }
  if (typeof window !== "undefined" && window.matchMedia("(max-width: 720px)").matches) {
    return "mobile";
  }
  return "desktop";
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

  const pipelineActiveStep = useMemo(() => {
    if (!run?.stages.length) return 1;
    const idx = run.stages.findIndex((s) => {
      const st = s.status.toLowerCase();
      return st !== "completed" && st !== "done" && st !== "success";
    });
    if (idx === -1) return run.stages.length;
    return idx + 1;
  }, [run?.stages]);

  return (
    <main
      data-testid="vf-shell"
      data-view-mode={viewMode}
      className={`mx-auto box-border min-h-svh w-full bg-background px-[max(1rem,env(safe-area-inset-right))] pt-[max(1rem,env(safe-area-inset-top))] pb-[max(1rem,env(safe-area-inset-bottom))] pl-[max(1rem,env(safe-area-inset-left))] text-foreground ${viewMode === "desktop" ? "max-w-[1100px]" : "max-w-[720px]"}`}
    >
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <h1 className="m-0 font-[Georgia,'Times_New_Roman',serif] text-3xl font-normal tracking-tight">
          voiceFaithfulness
        </h1>
        <div data-testid="vf-view-toggle" role="group" aria-label="Layout view" className="flex gap-2">
          <Button
            type="button"
            data-testid="vf-view-desktop"
            variant={viewMode === "desktop" ? "default" : "outline"}
            size="sm"
            aria-pressed={viewMode === "desktop"}
            onClick={() => setView("desktop")}
          >
            Desktop
          </Button>
          <Button
            type="button"
            data-testid="vf-view-mobile"
            variant={viewMode === "mobile" ? "default" : "outline"}
            size="sm"
            aria-pressed={viewMode === "mobile"}
            onClick={() => setView("mobile")}
          >
            Mobile
          </Button>
        </div>
      </div>

      <Alert
        data-testid="vf-providers-mode"
        role="status"
        variant={providersMode === "stub" ? "destructive" : "default"}
        className="mb-3"
      >
        <AlertTitle className="flex items-center gap-2">
          {providersMode === "stub" ? "Stub mode" : "Live mode"}
          <Badge variant={providersMode === "stub" ? "destructive" : "default"}>
            {providersMode}
          </Badge>
        </AlertTitle>
        <AlertDescription>
          {providersMode === "stub"
            ? "Scores and transcripts are demo placeholders (mocks), not real audio analysis. Set GROQ_API_KEY and unset FORCE_MOCK_PROVIDERS for live data."
            : "Providers are active. Scores reflect real STT → summary → judge calls."}
        </AlertDescription>
      </Alert>

      {liveNotice && providersMode === "live" ? (
        <Alert data-testid="vf-live-notice" role="status" className="mb-3">
          <AlertDescription>{liveNotice}</AlertDescription>
        </Alert>
      ) : null}

      {dash.scores_are_stubbed ? (
        <Alert data-testid="vf-stub-scores" role="status" variant="destructive" className="mb-3">
          <AlertDescription>
            Dashboard percentages are stubbed (mock judge). They are not faithfulness of your audio.
          </AlertDescription>
        </Alert>
      ) : null}

      <Card className="mb-4" size="sm">
        <CardHeader>
          <CardTitle className="text-muted-foreground">Teaching</CardTitle>
          <CardDescription data-testid="vf-teach" data-concept={teachConcept}>
            {teach}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p data-testid="vf-teach-log" className="m-0 text-xs text-muted-foreground" aria-live="polite">
            Concepts covered: {teachSeen.join(", ") || "none yet"}
          </p>
        </CardContent>
      </Card>

      <Card className="mb-4">
        <CardHeader>
          <CardTitle>Run setup</CardTitle>
          <CardDescription>Pick a recording and agents, then run the pipeline.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-3">
          <label className="text-sm font-medium">
            Recording
            <select
              data-testid="vf-recording-picker"
              value={recordingId}
              onChange={(e) => setRecordingId(e.target.value)}
              className={selectClass}
            >
              {recordings.map((rec) => (
                <option key={rec.id} value={rec.id}>
                  {rec.title}
                  {rec.ephemeral ? " · session upload" : ""}
                </option>
              ))}
            </select>
          </label>

          {previewUrl ? (
            <div>
              <div className="mb-1 text-sm font-medium">Preview</div>
              <audio data-testid="vf-audio-preview" controls src={previewUrl} className="w-full">
                Your browser does not support audio.
              </audio>
            </div>
          ) : null}

          <label className="text-sm font-medium">
            Add local recording
            <input
              data-testid="vf-upload"
              type="file"
              accept="audio/*"
              className="mt-1 block w-full text-sm"
              onChange={(e) => void onUpload(e.target.files?.[0] ?? null)}
            />
          </label>
          <p className="m-0 text-xs text-muted-foreground">
            Uploads stay in this browser session only. Preloaded demos are permanent.
          </p>

          <label className="text-sm font-medium">
            Transcription agent (owns transcript + summary)
            <select
              data-testid="vf-agent-stt"
              value={sttId}
              onChange={(e) => setSttId(e.target.value)}
              className={selectClass}
            >
              {sttAgents.map((a) => (
                <option key={a.id} value={a.id} disabled={!a.available}>
                  {a.label}
                  {!a.available ? " (unavailable)" : ""}
                </option>
              ))}
            </select>
          </label>

          <label className="text-sm font-medium">
            Judge agent
            <select
              data-testid="vf-agent-judge"
              value={judgeId}
              onChange={(e) => setJudgeId(e.target.value)}
              className={selectClass}
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

          <div className="flex flex-wrap gap-2">
            <Button data-testid="vf-run" type="button" disabled={!canRun} onClick={() => void onRun()}>
              {busy ? "Running…" : "Run pipeline"}
            </Button>
            <Button
              data-testid="vf-demo-reset"
              type="button"
              variant="outline"
              onClick={() => void onClearDemo()}
            >
              Clear demo data
            </Button>
          </div>
        </CardContent>
      </Card>

      {error ? (
        <Alert data-testid="vf-error" data-error-code={errorCode ?? undefined} variant="destructive" className="mb-4">
          <AlertTitle>Run error</AlertTitle>
          <AlertDescription>
            {errorCode ? `[${errorCode}] ` : ""}
            {error}
          </AlertDescription>
        </Alert>
      ) : null}

      <div
        data-testid="vf-flow"
        className={`mb-4 grid gap-3 ${viewMode === "desktop" ? "grid-cols-[repeat(auto-fit,minmax(200px,1fr))]" : ""}`}
      >
        {run ? (
          <Card data-testid="vf-stages" size="sm">
            <CardHeader>
              <CardTitle>Pipeline</CardTitle>
            </CardHeader>
            <CardContent>
              <Stepper
                value={pipelineActiveStep}
                orientation={viewMode === "desktop" ? "horizontal" : "vertical"}
                className="mb-3 w-full"
              >
                {run.stages.map((s, i) => {
                  const step = i + 1;
                  const st = s.status.toLowerCase();
                  const completed =
                    st === "completed" || st === "done" || st === "success" || step < pipelineActiveStep;
                  const loading =
                    busy &&
                    step === pipelineActiveStep &&
                    (st === "running" || st === "in_progress" || st === "pending" || busy);
                  return (
                    <StepperItem
                      key={s.name}
                      step={step}
                      completed={completed}
                      loading={loading}
                      className="relative flex-1 items-start"
                    >
                      <StepperTrigger className="w-full flex-col items-start gap-2 rounded-none">
                        <StepperIndicator />
                        <div className="space-y-0.5 px-0.5 text-left">
                          <StepperTitle className="capitalize">{s.name}</StepperTitle>
                          <StepperDescription>{s.status}</StepperDescription>
                        </div>
                      </StepperTrigger>
                      {step < run.stages.length ? (
                        <StepperSeparator className="absolute top-3 right-0 left-[calc(50%+0.85rem)] m-0 group-data-[orientation=horizontal]/stepper:w-[calc(100%-1.75rem)] group-data-[orientation=horizontal]/stepper:flex-none" />
                      ) : null}
                    </StepperItem>
                  );
                })}
              </Stepper>
              {run.score ? (
                <p data-testid="vf-run-score" className="mt-2 flex flex-wrap items-center gap-2">
                  Score: <Badge>{run.score.value}</Badge>
                  <span className="text-muted-foreground">
                    (judge: <span data-testid="vf-run-judge">{run.judge_agent_id}</span>; STT:{" "}
                    <span data-testid="vf-run-stt">{run.transcription_agent_id}</span>)
                  </span>
                </p>
              ) : null}
            </CardContent>
          </Card>
        ) : null}

        {run?.transcript ? (
          <Card size="sm">
            <CardHeader>
              <CardTitle>Transcript</CardTitle>
              <CardDescription data-testid="vf-transcript-owner">
                From agent: {run.transcription_agent_id}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <pre data-testid="vf-transcript" className={panelClass}>
                {run.transcript}
              </pre>
            </CardContent>
          </Card>
        ) : null}

        {run?.summary ? (
          <Card data-testid="vf-rationale" size="sm">
            <CardHeader>
              <CardTitle>Summary</CardTitle>
              <CardDescription data-testid="vf-summary-owner">
                From agent: {run.summary_owner_agent_id || run.transcription_agent_id}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <pre
                data-testid="vf-summary"
                title={rationale || "No rationale yet"}
                onMouseEnter={() => rationale && setRationaleOpen(true)}
                className={panelClass}
              >
                {run.summary}
              </pre>
              <Accordion
                type="single"
                collapsible
                className="mt-2"
                value={rationaleOpen ? "why" : ""}
                onValueChange={(v) => setRationaleOpen(v === "why")}
              >
                <AccordionItem value="why">
                  <AccordionTrigger data-testid="vf-rationale-toggle">Why this score?</AccordionTrigger>
                  <AccordionContent>
                    <pre data-testid="vf-rationale-text" className={panelClass}>
                      {rationale || "No rationale available for this run."}
                    </pre>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </CardContent>
          </Card>
        ) : null}

        <Card data-testid="vf-overall" size="sm">
          <CardHeader>
            <CardTitle>Overall</CardTitle>
            <CardDescription>Session aggregate faithfulness</CardDescription>
          </CardHeader>
          <CardContent>
            {dash.overall_percentage == null ? (
              <p className="m-0 text-muted-foreground">No scores yet</p>
            ) : (
              <div className="flex flex-wrap items-center gap-4">
                <CircularProgress
                  value={dash.overall_percentage}
                  showLabel
                  size={112}
                  strokeWidth={10}
                  className="stroke-primary/20"
                  progressClassName="stroke-primary"
                  labelClassName="text-lg font-semibold text-primary"
                  renderLabel={(v) => `${v}%`}
                />
                <Badge variant="secondary">{dash.completed_count} completed</Badge>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Card data-testid="vf-history" className="mb-4" size="sm">
        <CardHeader>
          <CardTitle>Session history</CardTitle>
        </CardHeader>
        <CardContent>
          {history.length === 0 ? (
            <p data-testid="vf-history-empty" className="m-0 text-muted-foreground">
              No runs yet
            </p>
          ) : (
            <ul className="m-0 list-none space-y-2 p-0">
              {history.map((h) => (
                <li key={h.id} data-testid="vf-history-row">
                  <Button
                    type="button"
                    variant="link"
                    className="h-auto p-0 text-left whitespace-normal"
                    onClick={() => {
                      setRun(h);
                      setRationaleOpen(false);
                    }}
                  >
                    {h.status} — STT {h.transcription_agent_id}; judge {h.judge_agent_id}
                    {h.score ? ` — ${h.score.value}%` : ""}
                  </Button>
                  {h.summary ? (
                    <div className="text-xs text-muted-foreground">
                      Summary: {h.summary.slice(0, 120)}
                      {h.summary.length > 120 ? "…" : ""}
                    </div>
                  ) : null}
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      <DashboardGraphs
        views={graphViews}
        selected={graphView}
        onSelect={setGraphView}
        scores={dash.scores}
        overallPercentage={dash.overall_percentage}
        completedCount={dash.completed_count}
      />

      <Card data-testid="vf-scores" size="sm" className="mt-4">
        <CardHeader>
          <CardTitle>Scores</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="m-0 list-disc space-y-1 pl-5">
            {dash.scores.map((s) => (
              <li key={s.run_id ?? s.recording_id} data-testid="vf-score-row">
                {s.title}: {s.value}% — STT: {s.transcription_agent_id}; judge: {s.judge_agent_id}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </main>
  );
}
