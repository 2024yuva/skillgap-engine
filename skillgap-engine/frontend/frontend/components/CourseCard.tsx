"use client";

import { type CourseRecommendation } from "@/lib/api";

const LEVEL_COLORS: Record<string, string> = {
  beginner:     "bg-emerald-50 text-emerald-700 border-emerald-200",
  intermediate: "bg-blue-50 text-blue-700 border-blue-200",
  advanced:     "bg-violet-50 text-violet-700 border-violet-200",
};

export default function CourseCard({ rec, rank }: { rec: CourseRecommendation; rank: number }) {
  const levelKey = (rec.course.level ?? "").toLowerCase();
  const levelClass = LEVEL_COLORS[levelKey] ?? "bg-slate-50 text-slate-600 border-slate-200";
  const impactPct = Math.min(Math.round(rec.impact_score * 100), 100);

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-col gap-3 hover:border-violet-300 transition-colors">
      {/* Rank + title */}
      <div className="flex items-start gap-3">
        <div className="w-7 h-7 rounded-full bg-violet-100 text-violet-700 text-xs font-bold flex items-center justify-center shrink-0">
          {rank}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-slate-800 leading-snug">{rec.course.title}</p>
          {rec.course.provider && (
            <p className="text-xs text-slate-500 mt-0.5">{rec.course.provider}</p>
          )}
        </div>
      </div>

      {/* Badges */}
      <div className="flex flex-wrap gap-1.5">
        {rec.course.level && (
          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border capitalize ${levelClass}`}>
            {rec.course.level}
          </span>
        )}
        {rec.course.duration && (
          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full border bg-slate-50 text-slate-600 border-slate-200">
            {rec.course.duration}
          </span>
        )}
        <span className="text-[10px] font-medium px-2 py-0.5 rounded-full border bg-slate-50 text-slate-600 border-slate-200">
          {rec.gaps_addressed_count} gap{rec.gaps_addressed_count !== 1 ? "s" : ""} addressed
        </span>
      </div>

      {/* Impact bar */}
      <div>
        <div className="flex justify-between text-[10px] text-slate-500 mb-1">
          <span>Gap closure impact</span>
          <span className="font-semibold text-violet-700">{impactPct}%</span>
        </div>
        <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div
            className="h-full bg-violet-500 rounded-full transition-all"
            style={{ width: `${impactPct}%` }}
          />
        </div>
      </div>

      {/* Explanation */}
      {rec.explanation && (
        <p className="text-xs text-slate-500 leading-relaxed line-clamp-2">{rec.explanation}</p>
      )}

      {/* Link */}
      {rec.course.source_url && (
        <a
          href={rec.course.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs font-semibold text-violet-600 hover:text-violet-800 hover:underline transition-colors mt-auto"
        >
          View course →
        </a>
      )}
    </div>
  );
}
