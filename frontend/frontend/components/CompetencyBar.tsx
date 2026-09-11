"use client";

import { type CompetencyGap } from "@/lib/api";

function priorityColor(score: number): string {
  if (score >= 0.5) return "bg-red-500";
  if (score >= 0.3) return "bg-orange-400";
  if (score >= 0.1) return "bg-yellow-400";
  return "bg-emerald-400";
}

function levelLabel(level: number): string {
  return ["No Evidence", "Awareness", "Basic", "Intermediate", "Advanced", "Expert"][level] ?? String(level);
}

export default function CompetencyBar({ gap }: { gap: CompetencyGap }) {
  const hasgap = gap.gap > 0;
  const currentPct = (gap.current_level / 5) * 100;
  const gapPct = (gap.gap / 5) * 100;
  const dotColor = priorityColor(gap.priority_score);

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-2 min-w-0">
          <div className={`w-2 h-2 rounded-full shrink-0 ${dotColor}`} />
          <p className="text-sm font-semibold text-slate-800 leading-snug truncate">
            {gap.competency_name}
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className="text-[10px] font-medium text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">
            {gap.category}
          </span>
          {hasgap ? (
            <span className="text-[10px] font-bold text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full">
              Gap: {gap.gap}
            </span>
          ) : (
            <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
              ✓ Met
            </span>
          )}
        </div>
      </div>

      {/* Stacked progress bar */}
      <div className="flex h-2 rounded-full overflow-hidden bg-slate-100 mb-2">
        <div
          className="bg-blue-500 transition-all"
          style={{ width: `${currentPct}%` }}
        />
        {hasgap && (
          <div
            className="bg-red-300 transition-all"
            style={{ width: `${gapPct}%` }}
          />
        )}
      </div>

      <div className="flex justify-between text-[10px] text-slate-400">
        <span>
          Current: <span className="font-semibold text-slate-600">{levelLabel(gap.current_level)}</span>
        </span>
        <span>
          Required: <span className="font-semibold text-slate-600">{levelLabel(gap.required_level)}</span>
        </span>
        <span>
          Priority: <span className="font-semibold text-slate-600">{gap.priority_score.toFixed(2)}</span>
        </span>
      </div>
    </div>
  );
}
