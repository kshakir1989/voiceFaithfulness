import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import { theme } from "../../theme";

type Props = {
  overallPercentage: number | null;
  completedCount: number;
};

/** Armory-style SLA ring: one hero % instead of a redundant single bar. */
export function OverallAggregate({ overallPercentage, completedCount }: Props) {
  if (overallPercentage == null || completedCount === 0) {
    return <p data-testid="vf-graph-empty">No scores yet</p>;
  }

  const clamped = Math.max(0, Math.min(100, overallPercentage));
  const data = [
    { name: "score", value: clamped },
    { name: "rest", value: Math.max(0, 100 - clamped) },
  ];

  return (
    <div data-testid="vf-graph-overall" style={{ width: "100%", height: 240, position: "relative" }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            cx="50%"
            cy="50%"
            innerRadius="68%"
            outerRadius="88%"
            startAngle={90}
            endAngle={-270}
            stroke="none"
            isAnimationActive={false}
          >
            <Cell fill={theme.color.primary} />
            <Cell fill={theme.color.line} />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            fontFamily: theme.font.display,
            fontSize: "2.25rem",
            fontWeight: 600,
            color: theme.color.ink,
            lineHeight: 1,
          }}
        >
          {overallPercentage}%
        </div>
        <div style={{ color: theme.color.textMuted, fontSize: "0.85rem", marginTop: 6 }}>
          Mean of {completedCount} score{completedCount === 1 ? "" : "s"}
        </div>
      </div>
    </div>
  );
}
