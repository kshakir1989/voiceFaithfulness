import { cn } from "@/lib/utils";

interface CircularProgressProps {
  value: number;
  renderLabel?: (progress: number) => number | string;
  size?: number;
  strokeWidth?: number;
  circleStrokeWidth?: number;
  progressStrokeWidth?: number;
  shape?: "square" | "round";
  className?: string;
  progressClassName?: string;
  labelClassName?: string;
  showLabel?: boolean;
}

export function CircularProgress({
  value,
  renderLabel,
  className,
  progressClassName,
  labelClassName,
  showLabel,
  shape = "round",
  size = 100,
  strokeWidth,
  circleStrokeWidth = 10,
  progressStrokeWidth = 10,
}: CircularProgressProps) {
  const clamped = Math.min(100, Math.max(0, value));
  const radius = size / 2 - 10;
  const circumference = Math.ceil(Math.PI * radius * 2);
  const percentage = Math.ceil(circumference * ((100 - clamped) / 100));

  const viewBox = `-${size * 0.125} -${size * 0.125} ${size * 1.25} ${size * 1.25}`;

  return (
    <div className="relative inline-flex">
      <svg
        className="relative"
        height={size}
        style={{ transform: "rotate(-90deg)" }}
        version="1.1"
        viewBox={viewBox}
        width={size}
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden={!showLabel}
      >
        <circle
          className={cn("stroke-primary/25", className)}
          cx={size / 2}
          cy={size / 2}
          fill="transparent"
          r={radius}
          strokeDasharray={circumference}
          strokeDashoffset="0"
          strokeWidth={strokeWidth ?? circleStrokeWidth}
        />
        <circle
          className={cn("stroke-primary", progressClassName)}
          cx={size / 2}
          cy={size / 2}
          fill="transparent"
          r={radius}
          strokeDasharray={circumference}
          strokeDashoffset={percentage}
          strokeLinecap={shape}
          strokeWidth={strokeWidth ?? progressStrokeWidth}
        />
      </svg>
      {showLabel ? (
        <div
          className={cn(
            "absolute inset-0 flex items-center justify-center text-md",
            labelClassName,
          )}
        >
          {renderLabel ? renderLabel(clamped) : clamped}
        </div>
      ) : null}
    </div>
  );
}
