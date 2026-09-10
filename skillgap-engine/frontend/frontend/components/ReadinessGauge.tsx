"use client";

import {
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
  ResponsiveContainer,
} from "recharts";

interface Props {
  score: number; // 0-100
  coveredCount: number;
  gapCount: number;
}

export default function ReadinessGauge({ score, coveredCount, gapCount }: Props) {
  const data = [{ value: score }];

  const color =
    score >= 75 ? "#10b981" : score >= 50 ? "#3b82f6" : score >= 25 ? "#f97316" : "#ef4444";

  return (
    <div className="flex flex-col items-center">
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">
        Readiness Score
      </p>
      <p className="text-xs text-slate-400 mb-3">(secondary metric)</p>

      <div className="relative w-36 h-36">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart
            cx="50%"
            cy="50%"
            innerRadius="70%"
            outerRadius="100%"
            barSize={12}
            data={data}
            startAngle={90}
            endAngle={-270}
          >
            <PolarAngleAxis
              type="number"
              domain={[0, 100]}
              angleAxisId={0}
              tick={false}
            />
            <RadialBar
              background={{ fill: "#e2e8f0" }}
              dataKey="value"
              fill={color}
              cornerRadius={6}
              angleAxisId={0}
            />
          </RadialBarChart>
        </ResponsiveContainer>

        {/* Centre text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold" style={{ color }}>
            {score}%
          </span>
        </div>
      </div>

      <div className="flex gap-4 mt-3 text-xs">
        <span className="text-emerald-600 font-medium">✓ {coveredCount} met</span>
        <span className="text-red-500 font-medium">✗ {gapCount} gaps</span>
      </div>
    </div>
  );
}
