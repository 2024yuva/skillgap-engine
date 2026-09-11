"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type CourseRecommendationResult, type CourseRecommendation } from "@/lib/api";
import { getSession, getSelectedRole } from "@/lib/session";
import { BookOpen, ExternalLink, Zap, TrendingUp, ArrowRight } from "lucide-react";

const LEVEL_COLORS: Record<string, string> = {
  beginner:     "bg-emerald-50 text-emerald-700 border-emerald-200",
  intermediate: "bg-blue-50 text-blue-700 border-blue-200",
  advanced:     "bg-violet-50 text-violet-700 border-violet-200",
};

const PROVIDER_COLORS: Record<string, string> = {
  "NPTEL":    "bg-orange-50 text-orange-700",
  "Coursera": "bg-blue-50 text-blue-700",
  "Kaggle":   "bg-sky-50 text-sky-700",
  "Udemy":    "bg-red-50 text-red-700",
  "Swayam":   "bg-teal-50 text-teal-700",
  "Educative":"bg-emerald-50 text-emerald-700",
  "GitHub":   "bg-slate-100 text-slate-700",
  "iGOT":     "bg-indigo-50 text-indigo-700",
  "MathWorks":"bg-rose-50 text-rose-700",
  "IASRI":    "bg-amber-50 text-amber-700",
};

export default function CoursesPage() {
  const router = useRouter();
  const [result, setResult] = useState<CourseRecommendationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState<"all" | "top">("top");

  useEffect(() => {
    const session = getSession();
    const role = getSelectedRole();
    if (!session) { router.replace("/"); return; }
    if (!role) { router.replace("/role"); return; }

    api.analysis.recommendations(session.id, role.id, 12)
      .then(setResult)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [router]);

  const recs = result?.recommendations ?? [];
  const displayed = filter === "top" ? recs.slice(0, 6) : recs;

  if (loading) return (
    <AppShell>
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-sm text-slate-500">Finding best courses for your gaps...</p>
        </div>
      </div>
    </AppShell>
  );

  if (error) return (
    <AppShell>
      <div className="max-w-lg mx-auto px-6 py-16 text-center">
        <p className="text-red-600 text-sm">{error}</p>
        <button onClick={() => router.push("/role")} className="mt-4 text-indigo-600 text-sm hover:underline">
          Select a role first
        </button>
      </div>
    </AppShell>
  );

  return (
    <AppShell>
      <div className="max-w-5xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-7">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Top Recommended Courses</h1>
            <p className="text-sm text-slate-500 mt-1">
              Courses ranked by how much of your weighted competency gap they close.
            </p>
          </div>

          {/* Filter tabs */}
          <div className="flex gap-1 bg-slate-100 rounded-xl p-1">
            {(["top", "all"] as const).map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  filter === f ? "bg-white text-indigo-700 shadow-sm" : "text-slate-500 hover:text-slate-700"
                }`}
              >
                {f === "top" ? "Top Picks" : `All (${recs.length})`}
              </button>
            ))}
          </div>
        </div>

        {recs.length === 0 ? (
          <div className="text-center py-16 text-slate-400">
            <BookOpen size={36} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm">No courses found for your current gap profile.</p>
            <button onClick={() => router.push("/analysis")} className="mt-3 text-indigo-600 text-sm hover:underline">
              Update your analysis
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {displayed.map((rec, i) => (
              <CourseRow key={rec.course.id} rec={rec} rank={i + 1} />
            ))}
          </div>
        )}

        {filter === "top" && recs.length > 6 && (
          <button
            onClick={() => setFilter("all")}
            className="mt-5 text-sm text-indigo-600 hover:underline font-medium"
          >
            Show all {recs.length} courses
          </button>
        )}

        {/* Learning path CTA */}
        {recs.length > 0 && (
          <div className="mt-8 p-5 bg-gradient-to-r from-indigo-50 to-violet-50 border border-indigo-200 rounded-2xl flex items-center justify-between gap-4">
            <div>
              <p className="text-sm font-bold text-indigo-900">Build your personalised learning path</p>
              <p className="text-xs text-indigo-600 mt-0.5">
                These courses ordered into a recommended sequence.
              </p>
            </div>
            <button
              onClick={() => router.push("/learning")}
              className="shrink-0 flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-all"
            >
              Learning Path
              <ArrowRight size={13} />
            </button>
          </div>
        )}
      </div>
    </AppShell>
  );
}

// ---------------------------------------------------------------------------
// Course row
// ---------------------------------------------------------------------------
function CourseRow({ rec, rank }: { rec: CourseRecommendation; rank: number }) {
  const { course, impact_score, gaps_addressed, explanation } = rec;

  const impactLabel = impact_score >= 1.0 ? "High" : impact_score >= 0.5 ? "Medium" : "Low";
  const impactColor = impact_score >= 1.0
    ? "bg-violet-100 text-violet-700 border-violet-200"
    : impact_score >= 0.5
    ? "bg-blue-100 text-blue-700 border-blue-200"
    : "bg-slate-100 text-slate-600 border-slate-200";

  const gapClosurePct = Math.min(Math.round(impact_score * 50), 99);
  const providerColor = PROVIDER_COLORS[course.provider ?? ""] ?? "bg-slate-100 text-slate-700";

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow p-5">
      <div className="flex items-start gap-4">
        {/* Rank */}
        <div className="w-8 h-8 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-xs font-bold text-indigo-600 shrink-0">
          #{rank}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3 mb-2">
            <h3 className="text-sm font-bold text-slate-800 leading-snug">{course.title}</h3>
            <div className="flex items-center gap-2 shrink-0">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${impactColor}`}>
                {impactLabel} Impact
              </span>
              <span className="text-xs font-mono text-slate-400">{impact_score.toFixed(3)}</span>
            </div>
          </div>

          {/* Meta chips */}
          <div className="flex flex-wrap items-center gap-1.5 mb-3">
            {course.provider && (
              <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${providerColor}`}>
                {course.provider}
              </span>
            )}
            {course.duration && (
              <span className="text-[10px] text-slate-500 bg-slate-50 border border-slate-200 px-2 py-0.5 rounded">
                {course.duration}
              </span>
            )}
            {course.level && (
              <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border capitalize ${LEVEL_COLORS[course.level] ?? "bg-slate-50 text-slate-600 border-slate-200"}`}>
                {course.level}
              </span>
            )}
          </div>

          {/* Explanation */}
          <p className="text-xs text-slate-600 leading-relaxed mb-3">{explanation}</p>

          {/* Gap closure bar */}
          <div className="mb-3">
            <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
              <span className="font-medium">Est. gap closure</span>
              <span className="font-bold text-indigo-600">{gapClosurePct}%</span>
            </div>
            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full transition-all"
                style={{ width: `${gapClosurePct}%` }}
              />
            </div>
          </div>

          {/* Competency chips */}
          {gaps_addressed.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-3">
              {gaps_addressed.map(name => (
                <span key={name} className="text-[10px] bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded-full font-medium">
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
              className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:underline font-medium"
            >
              View on {course.source}
              <ExternalLink size={11} />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
