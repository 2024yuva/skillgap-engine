"use client";

import { useEffect, useState, useMemo, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import CompetencyBar from "@/components/CompetencyBar";
import CourseCard from "@/components/CourseCard";
import ReadinessGauge from "@/components/ReadinessGauge";
import CategoryRadar from "@/components/CategoryRadar";
import {
  api,
  type GapAnalysisResult,
  type CourseRecommendationResult,
  type CompetencyGap,
} from "@/lib/api";

type Tab = "gaps" | "courses" | "chart";

export default function DashboardPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-slate-50">
          <Navbar />
          <div className="flex items-center justify-center h-[60vh]">
            <div className="text-center">
              <div className="animate-spin text-4xl mb-4">⟳</div>
              <p className="text-slate-500 text-sm">Loading dashboard…</p>
            </div>
          </div>
        </div>
      }
    >
      <DashboardContent />
    </Suspense>
  );
}

function DashboardContent() {
  const params = useSearchParams();
  const router = useRouter();

  const userId = Number(params.get("user") ?? 1);
  const roleId = Number(params.get("role") ?? 1);

  const [gapResult, setGapResult] = useState<GapAnalysisResult | null>(null);
  const [recResult, setRecResult] = useState<CourseRecommendationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>("gaps");
  const [categoryFilter, setCategoryFilter] = useState<string>("All");
  const [showAllGaps, setShowAllGaps] = useState(false);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([
      api.analysis.gaps(userId, roleId),
      api.analysis.recommendations(userId, roleId),
    ])
      .then(([g, r]) => {
        setGapResult(g);
        setRecResult(r);
      })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
      .finally(() => setLoading(false));
  }, [userId, roleId]);

  // Category filter options
  const categories = useMemo(() => {
    if (!gapResult) return [];
    const cats = Array.from(new Set(gapResult.gaps.map((g) => g.category)));
    return ["All", ...cats.sort()];
  }, [gapResult]);

  const filteredGaps: CompetencyGap[] = useMemo(() => {
    if (!gapResult) return [];
    const filtered =
      categoryFilter === "All"
        ? gapResult.gaps
        : gapResult.gaps.filter((g) => g.category === categoryFilter);
    return showAllGaps ? filtered : filtered.slice(0, 8);
  }, [gapResult, categoryFilter, showAllGaps]);

  const totalFiltered = useMemo(() => {
    if (!gapResult) return 0;
    return categoryFilter === "All"
      ? gapResult.gaps.length
      : gapResult.gaps.filter((g) => g.category === categoryFilter).length;
  }, [gapResult, categoryFilter]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="flex items-center justify-center h-[60vh]">
          <div className="text-center">
            <div className="animate-spin text-4xl mb-4">⟳</div>
            <p className="text-slate-500 text-sm">Running gap analysis…</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="max-w-2xl mx-auto px-6 py-16">
          <div className="rounded-xl bg-red-50 border border-red-200 p-6">
            <h2 className="text-red-700 font-semibold mb-2">Analysis failed</h2>
            <p className="text-red-600 text-sm">{error}</p>
            <button
              onClick={() => router.push("/")}
              className="mt-4 text-sm text-violet-600 hover:underline"
            >
              ← Back to profile
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!gapResult) return null;

  const topGap = gapResult.gaps.find((g) => g.gap > 0);

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-start justify-between mb-6 flex-wrap gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <button
                onClick={() => router.push("/")}
                className="text-xs text-slate-400 hover:text-slate-600"
              >
                ← Profile
              </button>
            </div>
            <h1 className="text-xl font-bold text-slate-800">
              {gapResult.user_name}
              <span className="text-slate-400 font-normal mx-2">→</span>
              {gapResult.role_name}
            </h1>
            <p className="text-sm text-slate-500 mt-0.5">
              Competency gap analysis &amp; course recommendations
            </p>
          </div>

          {/* Stats strip */}
          <div className="flex gap-3 flex-wrap">
            <StatPill label="Total Competencies" value={gapResult.gaps.length} color="slate" />
            <StatPill label="Strong Match" value={gapResult.strong_match_count ?? gapResult.covered_count} color="emerald" />
            <StatPill label="Need Work" value={gapResult.gap_count} color="red" />
            <StatPill
              label="Top Gap"
              value={topGap?.competency_name ?? "None"}
              color="orange"
              small
            />
          </div>
        </div>

        {/* Two-column layout */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar: gauge + radar */}
          <aside className="lg:col-span-1 space-y-4">
            <div className="rounded-xl bg-white border border-slate-200 p-5 shadow-sm flex flex-col items-center">
              <ReadinessGauge
                score={gapResult.readiness_score}
                coveredCount={gapResult.covered_count}
                gapCount={gapResult.gap_count}
              />
            </div>

            <div className="rounded-xl bg-white border border-slate-200 p-5 shadow-sm">
              <CategoryRadar gaps={gapResult.gaps} />
            </div>

            {/* Priority legend — replaced with status guide */}
            <div className="rounded-xl bg-white border border-slate-200 p-4 shadow-sm">
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
                Competency Status
              </p>
              <div className="space-y-1.5 text-xs">
                {[
                  { color: "bg-emerald-500", label: "Strong Match" },
                  { color: "bg-blue-500",    label: "Related / Transferable" },
                  { color: "bg-yellow-400",  label: "Needs Verification" },
                  { color: "bg-orange-400",  label: "Needs Development" },
                  { color: "bg-slate-400",   label: "Missing Evidence" },
                ].map(({ color, label }) => (
                  <div key={label} className="flex items-center gap-2">
                    <div className={`w-2.5 h-2.5 rounded-sm ${color}`} />
                    <span className="text-slate-600">{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </aside>

          {/* Main content */}
          <div className="lg:col-span-3 space-y-4">
            {/* Tab bar */}
            <div className="flex gap-1 bg-white border border-slate-200 rounded-lg p-1 shadow-sm w-fit">
              {(["gaps", "courses", "chart"] as Tab[]).map((t) => (
                <button
                  key={t}
                  onClick={() => setTab(t)}
                  className={`text-sm px-4 py-1.5 rounded-md font-medium transition-colors capitalize ${
                    tab === t
                      ? "bg-violet-600 text-white shadow-sm"
                      : "text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {t === "gaps"
                    ? `Competency Profile (${gapResult.gaps.length})`
                    : t === "courses"
                    ? `Course Recommendations (${recResult?.recommendations.length ?? 0})`
                    : "Category Overview"}
                </button>
              ))}
            </div>

            {/* Gaps tab */}
            {tab === "gaps" && (
              <div>
                {/* Category filter */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {categories.map((cat) => (
                    <button
                      key={cat}
                      onClick={() => {
                        setCategoryFilter(cat);
                        setShowAllGaps(false);
                      }}
                      className={`text-xs px-3 py-1 rounded-full border font-medium transition-colors ${
                        categoryFilter === cat
                          ? "bg-violet-600 text-white border-violet-600"
                          : "bg-white text-slate-600 border-slate-200 hover:border-violet-300"
                      }`}
                    >
                      {cat}
                    </button>
                  ))}
                </div>

                <div className="space-y-3">
                  {filteredGaps.map((g) => (
                    <CompetencyBar key={g.competency_id} gap={g} />
                  ))}
                </div>

                {totalFiltered > filteredGaps.length && (
                  <button
                    onClick={() => setShowAllGaps(true)}
                    className="mt-4 text-sm text-violet-600 hover:underline"
                  >
                    Show all {totalFiltered} competencies ↓
                  </button>
                )}

                {filteredGaps.length === 0 && (
                  <p className="text-sm text-slate-400 text-center py-8">
                    No competencies in this category.
                  </p>
                )}
              </div>
            )}

            {/* Courses tab */}
            {tab === "courses" && (
              <div>
                {recResult && recResult.recommendations.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {recResult.recommendations.map((rec, i) => (
                      <CourseCard key={rec.course.id} rec={rec} rank={i + 1} />
                    ))}
                  </div>
                ) : (
                  <div className="rounded-xl bg-white border border-slate-200 p-8 text-center text-slate-400 text-sm shadow-sm">
                    No course recommendations found for the current gap profile.
                  </div>
                )}
              </div>
            )}

            {/* Chart tab */}
            {tab === "chart" && (
              <div className="rounded-xl bg-white border border-slate-200 p-6 shadow-sm">
                <GapBarChart gaps={gapResult.gaps} />
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function StatPill({
  label,
  value,
  color,
  small,
}: {
  label: string;
  value: number | string;
  color: "slate" | "red" | "emerald" | "orange";
  small?: boolean;
}) {
  const colorMap = {
    slate:   "bg-slate-100 text-slate-700",
    red:     "bg-red-100 text-red-700",
    emerald: "bg-emerald-100 text-emerald-700",
    orange:  "bg-orange-100 text-orange-700",
  };
  return (
    <div className={`rounded-lg px-3 py-2 ${colorMap[color]}`}>
      <p className="text-xs font-medium opacity-70">{label}</p>
      <p className={`font-bold truncate max-w-[140px] ${small ? "text-sm" : "text-lg"}`}>
        {value}
      </p>
    </div>
  );
}

function GapBarChart({ gaps }: { gaps: CompetencyGap[] }) {
  const {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    Cell,
  } = require("recharts");

  const data = gaps.map((g) => ({
    name:
      g.competency_name.length > 18
        ? g.competency_name.slice(0, 16) + "…"
        : g.competency_name,
    Current: g.current_level,
    Gap: g.gap,
    Required: g.required_level,
  }));

  return (
    <div>
      <p className="text-sm font-semibold text-slate-700 mb-4">
        Current vs Required Levels — All Competencies
      </p>
      <ResponsiveContainer width="100%" height={340}>
        <BarChart data={data} margin={{ top: 4, right: 8, left: -10, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 10, fill: "#64748b" }}
            angle={-40}
            textAnchor="end"
            interval={0}
          />
          <YAxis domain={[0, 5]} tick={{ fontSize: 11, fill: "#64748b" }} />
          <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }} />
          <Legend
            wrapperStyle={{ fontSize: 12, paddingTop: 12 }}
            verticalAlign="top"
          />
          <Bar dataKey="Current" stackId="a" fill="#3b82f6" radius={[0, 0, 0, 0]} />
          <Bar dataKey="Gap" stackId="a" fill="#fca5a5" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-xs text-slate-400 mt-2 text-center">
        Blue = current level · Red = remaining gap to required
      </p>
    </div>
  );
}
