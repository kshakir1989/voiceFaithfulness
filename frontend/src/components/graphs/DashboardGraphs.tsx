import { PerRecordingBars, type ScorePoint } from "./PerRecordingBars";
import { OverallAggregate } from "./OverallAggregate";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export type GraphViewId = "per_recording_bars" | "overall_aggregate";

type GraphView = { id: GraphViewId; label: string };

type Props = {
  views: GraphView[];
  selected: GraphViewId;
  onSelect: (id: GraphViewId) => void;
  scores: ScorePoint[];
  overallPercentage: number | null;
  completedCount: number;
};

const selectClass =
  "mt-1 flex h-9 w-full max-w-sm rounded-lg border border-input bg-card px-2.5 text-sm outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50";

export function DashboardGraphs({
  views,
  selected,
  onSelect,
  scores,
  overallPercentage,
  completedCount,
}: Props) {
  return (
    <Card data-testid="vf-graphs" className="mb-4" size="sm">
      <CardHeader>
        <CardTitle>Graphs</CardTitle>
      </CardHeader>
      <CardContent>
        <label className="mb-3 block text-sm font-medium">
          View
          <select
            data-testid="vf-graph-selector"
            value={selected}
            onChange={(e) => onSelect(e.target.value as GraphViewId)}
            className={selectClass}
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
        ) : (
          <OverallAggregate overallPercentage={overallPercentage} completedCount={completedCount} />
        )}
      </CardContent>
    </Card>
  );
}
