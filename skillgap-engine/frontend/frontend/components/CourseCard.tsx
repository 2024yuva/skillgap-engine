"use client";

import { impactBadge, impactBadgeColor } from "@/lib/utils";
import type { CourseRecommendation } from "@/lib/api";

interface Props {
  rec: CourseRecommendation;
  rank: number;
}

const LEVEL_COLORS: Record<string, string> = {
  beginner:     "bg-emerald-100 text-emerald-700",
  intermediate: "bg-blue-100 text-blue-700",
  advanced:     "bg-violet-100 text-violet-700",
};

export default function CourseCard({ rec, rank }: Props) {
  const { course, impact_score, gaps_addressed, explanation } = rec;

  return (
    <div className="rounded-xl bg-white border border-slate-200 p-5 shadow-sm hover:shadow-md transition-shadow">
      {/* Rank + impact badge */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-bold text-slate-400">#{rank}</span>
        <div className="flex items-center gap-2">
          <span
            className={`text-xs font-semibold px-2 py-0.5 rounded-full ${impactBadgeColor(
              impact_score
            )}`}
          >
            {impactBadge(impact_score)}
          </span>
          <span className="text-xs text-slate-500 font-mono">
            {impact_score.toFixed(3)}
          </span>
        </div>
      </div>

      {/* Title + meta */}
      <h3 className="text-sm font-semibold text-slate-800 leading-snug mb-1">
        {course.title}
      </h3>
      <div className="flex flex-wrap gap-1.5 mb-3">
        {course.provider && (
          <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded">
            {course.provider}
          </span>
        )}
        {course.duration && (
          <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded">
            {course.duration}
          </span>
        )}
        {course.level && (
          <span
            className={`text-xs px-2 py-0.5 rounded capitalize ${
              LEVEL_COLORS[course.level] ?? "bg-slate-100 text-slate-600"
            }`}
          >
            {course.level}
          </span>
        )}
      </div>

      {/* Explanation */}
      <p className="text-xs text-slate-600 leading-relaxed mb-3">{explanation}</p>

      {/* Gaps addressed chips */}
      {gaps_addressed.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {gaps_addressed.map((name) => (
            <span
              key={name}
              className="text-xs bg-violet-50 text-violet-700 border border-violet-200 px-2 py-0.5 rounded-full"
            >
              {name}
            </span>
          ))}
        </div>
      )}

      {/* Source link */}
      {course.source_url && (
        <a
          href={course.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-3 inline-flex items-center text-xs text-violet-600 hover:underline"
        >
          View on {course.source ?? "source"} →
        </a>
      )}
    </div>
  );
}
