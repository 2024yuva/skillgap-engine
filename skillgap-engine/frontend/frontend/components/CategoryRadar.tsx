"use client";

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import type { CompetencyGap } from "@/lib/api";

interface Props {
  gaps: CompetencyGap[];
}

export default function CategoryRadar({ gaps }: Props) {
  // Aggregate current and required by category
  const byCategory: Record<string, { current: number[]; required: number[] }> = {};

  for (const g of gaps) {
    if (!byCategory[g.category]) {
      byCategory[g.category] = { current: [], required: [] };
    }
    byCategory[g.category].current.push(g.current_level);
    byCategory[g.category].required.push(g.required_level);
  }

  const avg = (arr: number[]) =>
    arr.length ? Math.round((arr.reduce((a, b) => a + b, 0) / arr.length) * 10) / 10 : 0;

  const data = Object.entries(byCategory).map(([cat, v]) => ({
    category: cat,
    current: avg(v.current),
    required: avg(v.required),
  }));

  if (data.length === 0) return null;

  return (
    <div>
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
        Competency by Category
      </p>
      <ResponsiveContainer width="100%" height={260}>
        <RadarChart data={data} margin={{ top: 10, right: 20, bottom: 10, left: 20 }}>
          <PolarGrid stroke="#e2e8f0" />
          <PolarAngleAxis
            dataKey="category"
            tick={{ fontSize: 11, fill: "#64748b" }}
          />
          <Radar
            name="Required"
            dataKey="required"
            stroke="#8b5cf6"
            fill="#8b5cf6"
            fillOpacity={0.12}
            strokeWidth={2}
          />
          <Radar
            name="Current"
            dataKey="current"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.25}
            strokeWidth={2}
          />
          <Tooltip
            contentStyle={{ fontSize: 12, borderRadius: 8, border: "1px solid #e2e8f0" }}
          />
          <Legend iconSize={10} wrapperStyle={{ fontSize: 12 }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
