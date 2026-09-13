import { useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { theme } from "../../theme";
import type { ScorePoint } from "./PerRecordingBars";

type GroupBy = "stt" | "judge";

type Props = {
  scores: ScorePoint[];
};

function shortLabel(id: string): string {
  if (id.length <= 22) return id;
  return `${id.slice(0, 20)}…`;
}

function averageBy(scores: ScorePoint[], key: "transcription_agent_id" | "judge_agent_id") {
  const buckets = new Map<string, { sum: number; n: number }>();
  for (const s of scores) {
    const id = s[key] || "unknown";
    const cur = buckets.get(id) ?? { sum: 0, n: 0 };
    cur.sum += s.value;
    cur.n += 1;
    buckets.set(id, cur);
  }
  return [...buckets.entries()].map(([id, { sum, n }]) => ({
    name: shortLabel(id),
    full: id,
    value: Math.round((sum / n) * 10) / 10,
    runs: n,
  }));
}

/** Compare mean scores by transcription agent or judge (teaching: does agent choice move the needle?). */
export function AgentCompare({ scores }: Props) {
  const [groupBy, setGroupBy] = useState<GroupBy>("stt");

  const data = useMemo(
    () =>
      averageBy(scores, groupBy === "stt" ? "transcription_agent_id" : "judge_agent_id"),
    [scores, groupBy],
  );

  if (scores.length === 0) {
    return <p data-testid="vf-graph-empty">No scores yet</p>;
  }

  return (
    <div data-testid="vf-graph-agent-compare">
      <div
        role="group"
        aria-label="Group agent comparison"
        style={{ display: "flex", gap: 8, marginBottom: theme.space }}
      >
        <button
          type="button"
          data-testid="vf-graph-group-stt"
          aria-pressed={groupBy === "stt"}
          onClick={() => setGroupBy("stt")}
          style={{
            border: `1px solid ${theme.color.line}`,
            background: groupBy === "stt" ? theme.color.primary : "transparent",
            color: groupBy === "stt" ? "#fff" : theme.color.text,
            padding: "4px 10px",
          }}
        >
          By STT agent
        </button>
        <button
          type="button"
          data-testid="vf-graph-group-judge"
          aria-pressed={groupBy === "judge"}
          onClick={() => setGroupBy("judge")}
          style={{
            border: `1px solid ${theme.color.line}`,
            background: groupBy === "judge" ? theme.color.primary : "transparent",
            color: groupBy === "judge" ? "#fff" : theme.color.text,
            padding: "4px 10px",
          }}
        >
          By judge agent
        </button>
      </div>
      <div style={{ width: "100%", height: 220 }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
            <CartesianGrid stroke={theme.color.line} strokeDasharray="3 3" />
            <XAxis dataKey="name" tick={{ fill: theme.color.textMuted, fontSize: 10 }} />
            <YAxis domain={[0, 100]} tick={{ fill: theme.color.textMuted, fontSize: 11 }} />
            <Tooltip
              formatter={(value) => [`${value}%`, "Mean score"]}
              labelFormatter={(_, payload) => {
                const full = payload?.[0]?.payload?.full;
                return typeof full === "string" ? full : "";
              }}
            />
            <Bar dataKey="value" fill={theme.color.primary} name="Mean score" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
