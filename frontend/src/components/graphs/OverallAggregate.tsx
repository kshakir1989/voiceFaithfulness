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

type Props = {
  overallPercentage: number | null;
  completedCount: number;
};

export function OverallAggregate({ overallPercentage, completedCount }: Props) {
  if (overallPercentage == null || completedCount === 0) {
    return <p data-testid="vf-graph-empty">No scores yet</p>;
  }

  const data = [{ name: "Overall", value: overallPercentage }];

  return (
    <div data-testid="vf-graph-overall" style={{ width: "100%", height: 220 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
          <CartesianGrid stroke={theme.color.line} strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{ fill: theme.color.textMuted, fontSize: 11 }} />
          <YAxis domain={[0, 100]} tick={{ fill: theme.color.textMuted, fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="value" fill={theme.color.primary} name="Overall %" />
        </BarChart>
      </ResponsiveContainer>
      <p style={{ color: theme.color.textMuted, fontSize: "0.9rem" }}>
        Mean of {completedCount} completed score{completedCount === 1 ? "" : "s"}: {overallPercentage}%
      </p>
    </div>
  );
}
