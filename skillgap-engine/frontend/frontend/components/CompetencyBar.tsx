"use client";

import { type CompetencyGap } from "@/lib/api";
import { CheckCircle2, GitMerge, HelpCircle, TrendingUp, AlertCircle } from "lucide-react";

function levelLabel(level: number): string {
  return ["No Evidence", "Awareness", "Basic", "Intermediate", "Advanced", "Expert"][level] ?? String(level);
}

// Map status to left-border colour
function statusBorderColor(status: CompetencyGap["status"]): string {
  switch (status) {
    case "strong_match":        return "border-l-emerald-500";
    case "related":             return "border-l-blue-500";
    case "needs_verification":  return "border-l-yellow-500";
    case "needs_development":   return "border-l-orange-500";
    case "missing":             return "border-l-slate-400";
    default:                    return "border-l-slate-300";
  }
}

function statusBadge(status: CompetencyGap["status"], label: string) {
  const map: Record<CompetencyGap["status"], string> = {
    strong_match:       "bg-emerald-50 text-emerald-700 border-emerald-200",
    related:            "bg-blue-50 text-blue-700 border-blue-200",
    needs_verification: "bg-yellow-50 text-yellow-700 border-yellow-200",
    needs_development:  "bg-orange-50 text-orange-700 border-orange-200",
    missing:            "bg-slate-100 text-slate-500 border-slate-200",
  };
  return (
    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${map[status]}`}>
      {label}
    </span>
  );
}

export default function CompetencyBar({ gap }: { gap: CompetencyGap }) {
  const currentPct = (gap.current_level / 5) * 100;
  const gapPct = Math.max((gap.required_level - gap.current_level) / 5 * 100, 0);
  const requiredPct = (gap.required_level / 5) * 100;

  return (
    <div className={`bg-white border border-l-4 border-slate-200 ${statusBorderColor(gap.status)} rounded-xl p-4 shadow-sm`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="min-w-0">
          <p className="text-sm font-semibold text-slate-800 leading-snug truncate">
            {gap.competency_name}
          </p>
          <span className="text-[10px] text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full font-medium">
            {gap.category}
          </span>
        </div>
        <div className="shrink-0">
          {statusBadge(gap.status, gap.status_label)}
        </div>
      </div>

      {/* Stacked progress bar */}
      <div className="relative h-2 rounded-full bg-slate-100 overflow-hidden mb-2">
        <div className="absolute inset-y-0 left-0 bg-indigo-500 rounded-l-full" style={{ width: `${currentPct}%` }} />
        {gapPct > 0 && (
          <div className="absolute inset-y-0 bg-red-200" style={{ left: `${currentPct}%`, width: `${gapPct}%` }} />
        )}
        <div className="absolute inset-y-0 w-0.5 bg-slate-600" style={{ left: `${requiredPct}%` }} />
      </div>

      <div className="flex justify-between text-[10px] text-slate-400">
        <span>
          Your level: <span className="font-semibold text-slate-600">{levelLabel(gap.current_level)}</span>
        </span>
        <span>
          Required: <span className="font-semibold text-slate-600">{levelLabel(gap.required_level)}</span>
        </span>
      </div>

      {/* Evidence source if present */}
      {gap.evidence_source && (
        <p className="text-[10px] text-slate-400 italic mt-1 truncate">
          Evidence: {gap.evidence_source}
        </p>
      )}
    </div>
  );
}
