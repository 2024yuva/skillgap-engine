"use client";

import { LEVEL_LABELS, gapColor } from "@/lib/utils";
import type { CompetencyGap } from "@/lib/api";

interface Props {
  gap: CompetencyGap;
  maxLevel?: number;
}

const LEVEL_COLORS = [
  "bg-slate-200",    // 0
  "bg-amber-400",    // 1
  "bg-orange-400",   // 2
  "bg-blue-500",     // 3
  "bg-violet-500",   // 4
  "bg-emerald-500",  // 5
];

export default function CompetencyBar({ gap, maxLevel = 5 }: Props) {
  const currentPct = (gap.current_level / maxLevel) * 100;
  const requiredPct = (gap.required_level / maxLevel) * 100;
  const gapPct = Math.max(requiredPct - currentPct, 0);

  const priorityClass =
    gap.priority_score >= 0.5
      ? "border-l-red-500"
      : gap.priority_score >= 0.3
      ? "border-l-orange-400"
      : gap.priority_score >= 0.1
      ? "border-l-yellow-400"
      : "border-l-emerald-400";

  return (
    <div className={`rounded-lg bg-white border border-slate-200 border-l-4 ${priorityClass} p-4 shadow-sm`}>
      {/* Header */}
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="text-sm font-semibold text-slate-800">{gap.competency_name}</p>
          <span className="text-xs text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
            {gap.category}
          </span>
        </div>
        <div className="text-right shrink-0">
          <span className={`text-sm font-bold ${gapColor(gap.gap)}`}>
            {gap.gap === 0 ? "✓ Met" : `Gap: ${gap.gap}`}
          </span>
          <p className="text-xs text-slate-400 mt-0.5">
            priority {gap.priority_score.toFixed(3)}
          </p>
        </div>
      </div>

      {/* Stacked bar */}
      <div className="relative h-4 rounded-full bg-slate-100 overflow-hidden">
        {/* Current level fill */}
        <div
          className={`absolute left-0 top-0 h-full rounded-l-full transition-all ${
            LEVEL_COLORS[gap.current_level] ?? "bg-slate-300"
          }`}
          style={{ width: `${currentPct}%` }}
        />
        {/* Gap portion */}
        {gapPct > 0 && (
          <div
            className="absolute top-0 h-full bg-red-200"
            style={{ left: `${currentPct}%`, width: `${gapPct}%` }}
          />
        )}
        {/* Required marker */}
        <div
          className="absolute top-0 h-full w-0.5 bg-slate-600"
          style={{ left: `${requiredPct}%` }}
          title={`Required: ${gap.required_level}`}
        />
      </div>

      {/* Legend */}
      <div className="flex justify-between mt-1.5 text-xs text-slate-500">
        <span>
          Current: <strong>{LEVEL_LABELS[gap.current_level]}</strong>
          {gap.evidence_source && (
            <span className="ml-1 text-slate-400 italic">({gap.evidence_source})</span>
          )}
        </span>
        <span>
          Required: <strong>{LEVEL_LABELS[gap.required_level]}</strong>
        </span>
      </div>
    </div>
  );
}
