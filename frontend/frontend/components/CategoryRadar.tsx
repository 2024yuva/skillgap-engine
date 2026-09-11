"use client";

import { useMemo } from "react";
import { type CompetencyGap } from "@/lib/api";

// Aggregate average gap per category for display
function aggregateByCategory(gaps: CompetencyGap[]) {
  const map: Record<string, { totalGap: number; count: number }> = {};
  for (const g of gaps) {
    if (!map[g.category]) map[g.category] = { totalGap: 0, count: 0 };
    map[g.category].totalGap += g.gap;
    map[g.category].count += 1;
  }
  return Object.entries(map).map(([cat, { totalGap, count }]) => ({
    category: cat,
    avgGap: totalGap / count,
    count,
  })).sort((a, b) => b.avgGap - a.avgGap);
}

export default function CategoryRadar({ gaps }: { gaps: CompetencyGap[] }) {
  const categories = useMemo(() => aggregateByCategory(gaps), [gaps]);

  if (categories.length === 0) return null;

  return (
    <div>
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
        Gap by Category
      </p>
      <div className="space-y-2.5">
        {categories.map(({ category, avgGap, count }) => {
          const pct = (avgGap / 5) * 100;
          const barColor =
            avgGap >= 2.5 ? "bg-red-400"
            : avgGap >= 1.5 ? "bg-orange-400"
            : avgGap >= 0.5 ? "bg-yellow-400"
            : "bg-emerald-400";

          return (
            <div key={category}>
              <div className="flex justify-between text-[10px] text-slate-500 mb-1">
                <span className="font-medium text-slate-700 truncate max-w-[130px]">{category}</span>
                <span>{avgGap.toFixed(1)} avg · {count}</span>
              </div>
              <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${barColor}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
