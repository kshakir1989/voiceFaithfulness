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

export type ScorePoint = {
  recording_id: string;
  title: string;
  value: number;
};

type Props = {
  scores: ScorePoint[];
};

export function PerRecordingBars({ scores }: Props) {
  const data = scores.map((s) => ({
    name: s.title.length > 18 ? `${s.title.slice(0, 16)}…` : s.title,
    value: s.value,
  }));

  if (data.length === 0) {
    return <p data-testid="vf-graph-empty">No scores yet</p>;
  }

  return (
    <div data-testid="vf-graph-per-recording" style={{ width: "100%", height: 220 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
          <CartesianGrid stroke={theme.color.line} strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{ fill: theme.color.textMuted, fontSize: 11 }} />
          <YAxis domain={[0, 100]} tick={{ fill: theme.color.textMuted, fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="value" fill={theme.color.primary} name="Score" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
