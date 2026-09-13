import { PerRecordingBars, type ScorePoint } from "./PerRecordingBars";
import { OverallAggregate } from "./OverallAggregate";
import { AgentCompare } from "./AgentCompare";
import { SessionSparkline } from "./SessionSparkline";
import { theme } from "../../theme";

export type GraphViewId =
  | "per_recording_bars"
  | "overall_aggregate"
  | "agent_compare"
  | "session_sparkline";

type GraphView = { id: GraphViewId; label: string };

type Props = {
  views: GraphView[];
  selected: GraphViewId;
  onSelect: (id: GraphViewId) => void;
  scores: ScorePoint[];
  overallPercentage: number | null;
  completedCount: number;
};

export function DashboardGraphs({
  views,
  selected,
  onSelect,
  scores,
  overallPercentage,
  completedCount,
}: Props) {
  return (
    <section data-testid="vf-graphs" style={{ marginBottom: theme.space * 2 }}>
      <h2 style={{ fontFamily: theme.font.display, fontSize: "1.25rem" }}>Graphs</h2>
      <label style={{ display: "block", marginBottom: theme.space }}>
        View
        <select
          data-testid="vf-graph-selector"
          value={selected}
          onChange={(e) => onSelect(e.target.value as GraphViewId)}
          style={{ display: "block", width: "100%", maxWidth: 360, marginTop: 4 }}
        >
          {views.map((v) => (
            <option key={v.id} value={v.id}>
              {v.label}
            </option>
          ))}
        </select>
      </label>
      {selected === "per_recording_bars" ? (
        <PerRecordingBars scores={scores} />
      ) : selected === "overall_aggregate" ? (
        <OverallAggregate overallPercentage={overallPercentage} completedCount={completedCount} />
      ) : selected === "agent_compare" ? (
        <AgentCompare scores={scores} />
      ) : (
        <SessionSparkline scores={scores} />
      )}
    </section>
  );
}
