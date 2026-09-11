"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type GapAnalysisResult, type CompetencyGap } from "@/lib/api";
import { getSession, getSelectedRole } from "@/lib/session";
import { AlertTriangle, TrendingDown, CheckCircle2, Info } from "lucide-react";

const LEVEL_LABELS = ["No Evidence", "Awareness", "Basic", "Intermediate", "Advanced", "Expert"];
const MAX_LEVEL = 5;

export default function AnalysisPage() {
  const router = useRouter();
  const [result, setResult] = useState<GapAnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    const session = getSession();
    const role = getSelectedRole();
    if (!session) { router.replace("/"); return; }
    if (!role) { router.replace("/role"); return; }

    api.analysis.gaps(session.id, role.id)
      .then(setResult)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [router]);

  const categories = useMemo(() => {
    if (!result) return [];
    const cats = Array.from(new Set(result.gaps.map(g => g.category)));
    return ["All", ...cats.sort()];
  }, [result]);

  const filtered = useMemo(() => {
    if (!result) return [];
    const f = categoryFilter === "All" ? result.gaps : result.gaps.filter(g => g.category === categoryFilter);
    return showAll ? f : f.slice(0, 8);
  }, [result, categoryFilter, showAll]);

  const totalFiltered = useMemo(() => {
    if (!result) return 0;
    return categoryFilter === "All" ? result.gaps.length : result.gaps.filter(g => g.category === categoryFilter).length;
  }, [result, categoryFilter]);

  if (loading) return (
    <AppShell>
      <div className="flex items-center justify-center h-full min-h-96">
        <div className="text-center">
          <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-sm text-slate-500">Running competency gap analysis...</p>
        </div>
      </div>
    </AppShell>
  );

  if (error) return (
    <AppShell>
      <div className="max-w-lg mx-auto px-6 py-16 text-center">
        <AlertTriangle size={32} className="text-red-400 mx-auto mb-3" />
        <p className="text-red-600 text-sm font-medium">{error}</p>
        <button onClick={() => router.push("/role")} className="mt-4 text-indigo-600 text-sm hover:underline">
          Select a role first
        </button>
      </div>
    </AppShell>
  );

  if (!result) return null;

  const highPriority = result.gaps.filter(g => g.priority_score >= 0.3 && g.gap > 0);

  return (
    <AppShell>
      <div className="max-w-5xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Your Competency Profile</h1>
            <p className="text-sm text-slate-500 mt-1">
              {result.user_name} &nbsp;&#8594;&nbsp; <span className="font-semibold text-indigo-600">{result.role_name}</span>
            </p>
          </div>

          {/* Summary stats */}
          <div className="flex gap-3 flex-wrap">
            <StatCard icon={<TrendingDown size={14} />} label="Gaps" value={result.gap_count} color="red" />
            <StatCard icon={<CheckCircle2 size={14} />} label="Met" value={result.covered_count} color="emerald" />
            <StatCard icon={<AlertTriangle size={14} />} label="High Priority" value={highPriority.length} color="orange" />
          </div>
        </div>

        {/* Two column layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: summary + readiness */}
          <div className="lg:col-span-1 space-y-4">
            {/* Readiness score */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-4">
                Readiness Score <span className="text-slate-300 normal-case font-normal">(secondary)</span>
              </p>
              <ReadinessRing score={result.readiness_score} />
            </div>

            {/* Priority Legend */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5">
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Priority Guide</p>
              <div className="space-y-2 text-xs">
                {[
                  { color: "bg-red-500", label: "Critical gap", range: "Priority >= 0.5" },
                  { color: "bg-orange-400", label: "High gap", range: "Priority 0.3-0.5" },
                  { color: "bg-yellow-400", label: "Medium gap", range: "Priority 0.1-0.3" },
                  { color: "bg-emerald-400", label: "Met or minor", range: "Priority < 0.1" },
                ].map(({ color, label, range }) => (
                  <div key={label} className="flex items-center gap-2.5">
                    <div className={`w-2.5 h-2.5 rounded-sm shrink-0 ${color}`} />
                    <div>
                      <p className="text-slate-700 font-medium">{label}</p>
                      <p className="text-slate-400">{range}</p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-3 pt-3 border-t border-slate-100">
                <p className="text-xs text-slate-400">
                  Priority = (gap / 5) &times; importance
                </p>
              </div>
            </div>

            {/* High priority callout */}
            {highPriority.length > 0 && (
              <div className="bg-red-50 border border-red-200 rounded-2xl p-4">
                <div className="flex items-start gap-2">
                  <AlertTriangle size={14} className="text-red-500 mt-0.5 shrink-0" />
                  <p className="text-xs text-red-700 font-medium">
                    You have <strong>{highPriority.length} high-priority skill gap{highPriority.length > 1 ? "s" : ""}</strong> to reach your target role.
                  </p>
                </div>
                <div className="mt-2 space-y-1">
                  {highPriority.slice(0, 3).map(g => (
                    <p key={g.competency_id} className="text-xs text-red-600 pl-4">
                      {g.competency_name}
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right: competency bars */}
          <div className="lg:col-span-2 space-y-4">
            {/* Category filter */}
            <div className="flex flex-wrap gap-2">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => { setCategoryFilter(cat); setShowAll(false); }}
                  className={`text-xs px-3 py-1.5 rounded-full border font-semibold transition-all ${
                    categoryFilter === cat
                      ? "bg-indigo-600 text-white border-indigo-600"
                      : "bg-white text-slate-600 border-slate-200 hover:border-indigo-300"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* Legend */}
            <div className="flex items-center gap-4 text-xs text-slate-500">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-sm bg-indigo-500" />
                Your Level
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-sm bg-red-200" />
                Gap
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-0.5 h-3 bg-slate-700" />
                Required Level
              </div>
            </div>

            {/* Bars */}
            <div className="space-y-3">
              {filtered.map(g => <CompetencyRow key={g.competency_id} gap={g} />)}
            </div>

            {totalFiltered > filtered.length && (
              <button
                onClick={() => setShowAll(true)}
                className="text-sm text-indigo-600 hover:underline font-medium"
              >
                Show all {totalFiltered} competencies
              </button>
            )}

            {filtered.length === 0 && (
              <p className="text-sm text-slate-400 text-center py-8">No competencies in this category.</p>
            )}

            {/* Go to courses CTA */}
            <div className="mt-4 p-4 bg-indigo-50 border border-indigo-200 rounded-2xl flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-semibold text-indigo-900">Ready for course recommendations?</p>
                <p className="text-xs text-indigo-600 mt-0.5">
                  Courses ranked by how much of your remaining gap they close.
                </p>
              </div>
              <button
                onClick={() => router.push("/courses")}
                className="shrink-0 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-all"
              >
                View Courses
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}

// ---------------------------------------------------------------------------
// Competency row component
// ---------------------------------------------------------------------------
function CompetencyRow({ gap }: { gap: CompetencyGap }) {
  const currentPct = (gap.current_level / MAX_LEVEL) * 100;
  const requiredPct = (gap.required_level / MAX_LEVEL) * 100;
  const gapPct = Math.max(requiredPct - currentPct, 0);

  const priorityColor =
    gap.priority_score >= 0.5 ? "border-l-red-500" :
    gap.priority_score >= 0.3 ? "border-l-orange-400" :
    gap.priority_score >= 0.1 ? "border-l-yellow-400" :
    "border-l-emerald-400";

  const gapTextColor =
    gap.gap === 0 ? "text-emerald-600" :
    gap.gap <= 1 ? "text-yellow-600" :
    gap.gap <= 2 ? "text-orange-600" : "text-red-600";

  return (
    <div className={`bg-white rounded-xl border border-slate-200 border-l-4 ${priorityColor} p-4 shadow-sm`}>
      <div className="flex items-start justify-between gap-3 mb-2.5">
        <div>
          <p className="text-sm font-semibold text-slate-800">{gap.competency_name}</p>
          <span className="text-[10px] text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full font-medium">
            {gap.category}
          </span>
        </div>
        <div className="text-right shrink-0">
          <span className={`text-sm font-bold ${gapTextColor}`}>
            {gap.gap === 0 ? "Met" : `Gap: ${gap.gap}`}
          </span>
          <p className="text-[10px] text-slate-400 mt-0.5">priority {gap.priority_score.toFixed(3)}</p>
        </div>
      </div>

      {/* Stacked progress bar */}
      <div className="relative h-3.5 rounded-full bg-slate-100 overflow-hidden">
        <div
          className="absolute inset-y-0 left-0 rounded-l-full bg-indigo-500"
          style={{ width: `${currentPct}%` }}
        />
        {gapPct > 0 && (
          <div
            className="absolute inset-y-0 bg-red-200"
            style={{ left: `${currentPct}%`, width: `${gapPct}%` }}
          />
        )}
        {/* Required marker */}
        <div
          className="absolute inset-y-0 w-0.5 bg-slate-700"
          style={{ left: `${requiredPct}%` }}
          title={`Required: ${gap.required_level}`}
        />
      </div>

      <div className="flex justify-between mt-2 text-xs text-slate-500">
        <span>
          Your Level: <strong className="text-slate-700">{LEVEL_LABELS[gap.current_level]}</strong>
          {gap.evidence_source && (
            <span className="text-slate-400 italic ml-1">({gap.evidence_source})</span>
          )}
        </span>
        <span>
          Required: <strong className="text-slate-700">{LEVEL_LABELS[gap.required_level]}</strong>
        </span>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Readiness ring
// ---------------------------------------------------------------------------
function ReadinessRing({ score }: { score: number }) {
  const color = score >= 75 ? "#10b981" : score >= 50 ? "#6366f1" : score >= 25 ? "#f97316" : "#ef4444";
  const r = 44;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-28 h-28">
        <svg width="112" height="112" viewBox="0 0 112 112" className="-rotate-90">
          <circle cx="56" cy="56" r={r} fill="none" stroke="#e2e8f0" strokeWidth="10" />
          <circle
            cx="56" cy="56" r={r} fill="none"
            stroke={color} strokeWidth="10"
            strokeDasharray={`${dash} ${circ}`}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold" style={{ color }}>{score}%</span>
        </div>
      </div>
      <p className="text-xs text-slate-400 text-center mt-2 leading-snug">
        Weighted competency readiness
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Stat card
// ---------------------------------------------------------------------------
function StatCard({ icon, label, value, color }: {
  icon: React.ReactNode; label: string; value: number;
  color: "red" | "emerald" | "orange";
}) {
  const colorMap = {
    red: "bg-red-50 text-red-700 border-red-200",
    emerald: "bg-emerald-50 text-emerald-700 border-emerald-200",
    orange: "bg-orange-50 text-orange-700 border-orange-200",
  };
  return (
    <div className={`flex items-center gap-2 px-3 py-2 rounded-xl border text-sm ${colorMap[color]}`}>
      {icon}
      <div>
        <p className="text-xs opacity-70">{label}</p>
        <p className="font-bold text-base leading-none">{value}</p>
      </div>
    </div>
  );
}
