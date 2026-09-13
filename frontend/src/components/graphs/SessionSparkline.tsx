import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { theme } from "../../theme";
import type { ScorePoint } from "./PerRecordingBars";

type Props = {
  scores: ScorePoint[];
};

/** Session “growth vector”: scores in run order as a sparkline. */
export function SessionSparkline({ scores }: Props) {
  if (scores.length === 0) {
    return <p data-testid="vf-graph-empty">No scores yet</p>;
  }

  const data = scores.map((s, i) => ({
    run: i + 1,
    value: s.value,
    title: s.title,
  }));

  return (
    <div data-testid="vf-graph-sparkline" style={{ width: "100%", height: 220 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 8 }}>
          <CartesianGrid stroke={theme.color.line} strokeDasharray="3 3" />
          <XAxis
            dataKey="run"
            tick={{ fill: theme.color.textMuted, fontSize: 11 }}
            label={{ value: "Run #", position: "insideBottom", offset: -2, fill: theme.color.textMuted }}
          />
          <YAxis domain={[0, 100]} tick={{ fill: theme.color.textMuted, fontSize: 11 }} />
          <Tooltip
            formatter={(value) => [`${value}%`, "Score"]}
            labelFormatter={(run, payload) => {
              const title = payload?.[0]?.payload?.title;
              return title ? `Run ${run} · ${title}` : `Run ${run}`;
            }}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke={theme.color.primary}
            strokeWidth={2}
            dot={{ r: 4, fill: theme.color.primary }}
            name="Score"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
