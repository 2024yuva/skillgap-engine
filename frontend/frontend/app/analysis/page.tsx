"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import {
  api,
  type GapAnalysisResult,
  type CompetencyGap,
} from "@/lib/api";
import { getSession, getSelectedRole } from "@/lib/session";
import {
  CheckCircle2,
  GitMerge,
  HelpCircle,
  TrendingUp,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  BookOpen,
  ClipboardCheck,
  Info,
  Loader2,
  ArrowRight,
  ExternalLink,
} from "lucide-react";

// ─── Status config ──────────────────────────────────────────────────────────
type Status = CompetencyGap["status"];

const STATUS_CONFIG: Record<
  Status,
  {
    icon: React.ComponentType<{ size?: number; className?: string }>;
    label: string;
    color: string;        // Tailwind text colour
    bg: string;           // Tailwind bg colour for badge
    border: string;       // Tailwind left-border colour
    ring: string;         // card ring
  }
> = {
  strong_match: {
    icon: CheckCircle2,
    label: "Strong Match",
    color: "text-emerald-700",
    bg: "bg-emerald-100",
    border: "border-l-emerald-500",
    ring: "border-emerald-200",
  },
  related: {
    icon: GitMerge,
    label: "Related / Transferable",
    color: "text-blue-700",
    bg: "bg-blue-100",
    border: "border-l-blue-500",
    ring: "border-blue-200",
  },
  needs_verification: {
    icon: HelpCircle,
    label: "Needs Verification",
    color: "text-yellow-700",
    bg: "bg-yellow-100",
    border: "border-l-yellow-500",
    ring: "border-yellow-200",
  },
  needs_development: {
    icon: TrendingUp,
    label: "Needs Development",
    color: "text-orange-700",
    bg: "bg-orange-100",
    border: "border-l-orange-500",
    ring: "border-orange-200",
  },
  missing: {
    icon: AlertCircle,
    label: "Missing Evidence",
    color: "text-slate-500",
    bg: "bg-slate-100",
    border: "border-l-slate-400",
    ring: "border-slate-200",
  },
};

const STATUS_ORDER: Status[] = [
  "strong_match",
  "related",
  "needs_verification",
  "needs_development",
  "missing",
];

// ─── Helpers ────────────────────────────────────────────────────────────────

function groupByStatus(gaps: CompetencyGap[]) {
  const groups: Record<Status, CompetencyGap[]> = {
    strong_match: [],
    related: [],
    needs_verification: [],
    needs_development: [],
    missing: [],
  };
  for (const g of gaps) {
    groups[g.status].push(g);
  }
  return groups;
}

function evidenceLinks(skillName: string) {
  const query = encodeURIComponent(`${skillName} course project`);
  return [
    { label: "Learn", url: `https://www.youtube.com/results?search_query=${query}` },
    { label: "NPTEL", url: `https://nptel.ac.in/courses?search=${encodeURIComponent(skillName)}` },
    { label: "Show project", url: `https://github.com/search?q=${encodeURIComponent(skillName)}&type=repositories` },
  ];
}

export default function AnalysisPage() {
  const router = useRouter();
  const [result, setResult] = useState<GapAnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState<Status | "all">("all");
  const [expandedIds, setExpandedIds] = useState<Set<number>>(new Set());

  useEffect(() => {
    const session = getSession();
    const role = getSelectedRole();
    if (!session) { router.replace("/"); return; }
    if (!role) { router.replace("/role"); return; }

    api.analysis.gaps(session.id, role.id)
      .then(setResult)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [router]);

  const groups = useMemo(() => result ? groupByStatus(result.gaps) : null, [result]);

  const visibleGaps = useMemo(() => {
    if (!result || !groups) return [];
    if (activeSection === "all") return result.gaps;
    return groups[activeSection] ?? [];
  }, [result, groups, activeSection]);

  function toggleExpand(id: number) {
    setExpandedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  // ── Loading ────────────────────────────────────────────────────────────
  if (loading) return (
    <AppShell>
      <div className="flex items-center justify-center h-full min-h-96">
        <div className="text-center">
          <Loader2 size={32} className="text-indigo-500 animate-spin mx-auto mb-4" />
          <p className="text-sm text-slate-500">Analysing your competencies…</p>
        </div>
      </div>
    </AppShell>
  );

  if (error) return (
    <AppShell>
      <div className="max-w-lg mx-auto px-6 py-16 text-center">
        <AlertCircle size={32} className="text-red-400 mx-auto mb-3" />
        <p className="text-red-600 text-sm font-medium">{error}</p>
        <button onClick={() => router.push("/role")} className="mt-4 text-indigo-600 text-sm hover:underline">
          Select a role first
        </button>
      </div>
    </AppShell>
  );

  if (!result || !groups) return null;

  const { strong_match_count, related_count, needs_verification_count, needs_development_count, missing_count } = result;

  // Next steps list
  const nextSteps: { label: string; desc: string }[] = [];
  if (needs_verification_count > 0)
    nextSteps.push({ label: "Verify your skills", desc: `${needs_verification_count} competency${needs_verification_count > 1 ? "ies" : ""} need a quick assessment` });
  if (groups.needs_verification.some(g => g.competency_id === 4))
    nextSteps.push({ label: "Take the DSA Assessment", desc: "Demonstrate your Data Structures & Algorithms proficiency" });
  if (needs_development_count > 0)
    nextSteps.push({ label: "Build your development plan", desc: `${needs_development_count} competency${needs_development_count > 1 ? "ies" : ""} need focused improvement` });
  if (missing_count > 0)
    nextSteps.push({ label: "Explore missing skills", desc: "Find resources for skills not yet on your profile" });
  nextSteps.push({ label: "View course recommendations", desc: "Courses ranked to close your most important gaps first" });

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">

        {/* ── Hero header ─────────────────────────────────────────────────── */}
        <div className="bg-linear-to-br from-indigo-50 to-blue-50 rounded-2xl border border-indigo-100 p-6">
          <p className="text-xs font-semibold text-indigo-500 uppercase tracking-widest mb-1">
            Your Path to
          </p>
          <h1 className="text-2xl font-bold text-slate-900 mb-1">
            {result.role_name}
          </h1>
          <p className="text-sm text-slate-500 mb-5">
            {result.user_name} &nbsp;·&nbsp; {result.gaps.length} competencies analysed
          </p>

          {/* Summary cards */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            {(
              [
                ["strong_match", strong_match_count],
                ["related", related_count],
                ["needs_verification", needs_verification_count],
                ["needs_development", needs_development_count],
                ["missing", missing_count],
              ] as [Status, number][]
            ).map(([s, count]) => {
              const cfg = STATUS_CONFIG[s];
              const Icon = cfg.icon;
              const isActive = activeSection === s;
              return (
                <button
                  key={s}
                  onClick={() => setActiveSection(isActive ? "all" : s)}
                  className={`rounded-xl p-3 border text-left transition-all ${isActive
                    ? `${cfg.bg} ${cfg.ring} border-2`
                    : "bg-white border-slate-200 hover:border-indigo-200"
                    }`}
                >
                  <div className="flex items-center gap-1.5 mb-1">
                    <Icon size={13} className={cfg.color} />
                    <span className={`text-xs font-semibold ${cfg.color}`}>{count}</span>
                  </div>
                  <p className="text-[11px] text-slate-600 leading-tight">{cfg.label}</p>
                </button>
              );
            })}
          </div>

          {activeSection !== "all" && (
            <button
              onClick={() => setActiveSection("all")}
              className="mt-3 text-xs text-indigo-600 hover:underline"
            >
              ← Show all competencies
            </button>
          )}
        </div>

        {/* ── Competency list ──────────────────────────────────────────────── */}
        <div className="space-y-3">
          {visibleGaps.length === 0 && (
            <p className="text-sm text-slate-400 text-center py-8">
              No competencies in this category.
            </p>
          )}
          {visibleGaps.map((g) => (
            <CompetencyCard
              key={g.competency_id}
              gap={g}
              expanded={expandedIds.has(g.competency_id)}
              onToggle={() => toggleExpand(g.competency_id)}
              onAssess={() => router.push(`/assessment?competency=${g.competency_id}`)}
              onLearn={() => router.push("/courses")}
            />
          ))}
        </div>

        {/* ── Next steps ──────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
          <h2 className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
            <ArrowRight size={16} className="text-indigo-500" />
            Your Next Steps
          </h2>
          <ol className="space-y-3">
            {nextSteps.map((step, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <div>
                  <p className="text-sm font-semibold text-slate-800">{step.label}</p>
                  <p className="text-xs text-slate-500">{step.desc}</p>
                </div>
              </li>
            ))}
          </ol>

          <div className="mt-5 flex flex-wrap gap-3">
            <button
              onClick={() => router.push("/assessment")}
              className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-all"
            >
              Take DSA Assessment
            </button>
            <button
              onClick={() => router.push("/courses")}
              className="bg-white border border-indigo-300 text-indigo-700 hover:bg-indigo-50 text-sm font-semibold px-4 py-2 rounded-xl transition-all"
            >
              View Course Recommendations
            </button>
          </div>
        </div>

        {/* ── Readiness (secondary, collapsed) ────────────────────────────── */}
        <details className="group">
          <summary className="cursor-pointer text-xs text-slate-400 hover:text-slate-600 list-none flex items-center gap-1 select-none">
            <Info size={12} />
            View readiness score (secondary metric)
          </summary>
          <div className="mt-2 bg-slate-50 rounded-xl border border-slate-200 p-4 text-center">
            <p className="text-3xl font-bold text-indigo-600">{result.readiness_score}%</p>
            <p className="text-xs text-slate-500 mt-1">
              Weighted competency readiness — proportion of required levels already achieved.
              This is a secondary metric; the classifications above are the primary guidance.
            </p>
          </div>
        </details>
      </div>
    </AppShell>
  );
}

// ─── Competency Card ─────────────────────────────────────────────────────────

function CompetencyCard({
  gap,
  expanded,
  onToggle,
  onAssess,
  onLearn,
}: {
  gap: CompetencyGap;
  expanded: boolean;
  onToggle: () => void;
  onAssess: () => void;
  onLearn: () => void;
}) {
  const cfg = STATUS_CONFIG[gap.status];
  const Icon = cfg.icon;

  return (
    <div
      className={`bg-white rounded-xl border border-l-4 ${cfg.border} ${cfg.ring} border shadow-sm transition-all`}
    >
      {/* Card header — always visible */}
      <div
        onClick={onToggle}
        onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && onToggle()}
        role="button"
        tabIndex={0}
        className="w-full text-left p-4 flex items-start justify-between gap-3 cursor-pointer select-none"
        aria-expanded={expanded}
      >
        <div className="flex items-start gap-3 flex-1 min-w-0">
          <Icon size={16} className={`${cfg.color} mt-0.5 shrink-0`} />
          <div className="min-w-0">
            <p className="text-sm font-semibold text-slate-800 truncate">
              {gap.competency_name}
            </p>
            <div className="flex items-center gap-2 mt-0.5 flex-wrap">
              <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${cfg.bg} ${cfg.color}`}>
                {cfg.label}
              </span>
              <span className="text-[11px] text-slate-400">{gap.category}</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {/* Quick action button */}
          {gap.status === "needs_verification" || gap.status === "related" ? (
            <button
              onClick={(e) => { e.stopPropagation(); onAssess(); }}
              className="hidden sm:flex items-center gap-1 text-[11px] font-semibold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 px-2 py-1 rounded-lg transition-all"
            >
              <ClipboardCheck size={11} />
              {gap.action_label}
            </button>
          ) : gap.status === "needs_development" || gap.status === "missing" ? (
            <button
              onClick={(e) => { e.stopPropagation(); onLearn(); }}
              className="hidden sm:flex items-center gap-1 text-[11px] font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 px-2 py-1 rounded-lg transition-all"
            >
              <BookOpen size={11} />
              {gap.action_label}
            </button>
          ) : null}
          {expanded
            ? <ChevronUp size={14} className="text-slate-400" />
            : <ChevronDown size={14} className="text-slate-400" />
          }
        </div>
      </div>


      {/* Expanded content */}
      {expanded && (
        <div className="px-4 pb-4 pt-0 border-t border-slate-100 mt-0">
          {/* Why this classification */}
          <div className="mt-3 mb-3">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">
              Why we classified this
            </p>
            <p className="text-sm text-slate-600 leading-relaxed">
              {gap.status_reason}
            </p>
          </div>

          {/* Evidence bullets */}
          {gap.evidence_bullets && gap.evidence_bullets.length > 0 && (
            <div className="mb-3">
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">
                Evidence found
              </p>
              <ul className="space-y-1">
                {gap.evidence_bullets.map((b, i) => (
                  <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                    <span className="text-emerald-500 mt-0.5">✓</span>
                    {b}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Related skill callout */}
          {gap.related_skill_name && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg px-3 py-2 mb-3">
              <p className="text-xs text-blue-700">
                <span className="font-semibold">Related skill detected:</span>{" "}
                {gap.related_skill_name} — your experience here is transferable.
              </p>
            </div>
          )}

          {gap.status === "missing" && (
            <div className="mb-3 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
              <p className="text-xs font-semibold text-slate-600 mb-1.5">Build evidence for this skill</p>
              <div className="flex flex-wrap gap-2">
                {evidenceLinks(gap.competency_name).map((link) => (
                  <a
                    key={link.label}
                    href={link.url}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="inline-flex items-center gap-1 rounded-md bg-white border border-slate-200 px-2 py-1 text-[11px] font-semibold text-indigo-600 hover:border-indigo-300 hover:bg-indigo-50"
                  >
                    {link.label}
                    <ExternalLink size={10} />
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Confidence */}
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs text-slate-500">System confidence</span>
            <div className="flex items-center gap-2">
              <div className="w-24 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full bg-indigo-400 transition-all"
                  style={{ width: `${Math.round(gap.confidence * 100)}%` }}
                />
              </div>
              <span className="text-xs text-slate-500 w-8 text-right">
                {Math.round(gap.confidence * 100)}%
              </span>
            </div>
          </div>

          {/* Mobile action buttons */}
          <div className="flex gap-2 flex-wrap">
            {(gap.status === "needs_verification" || gap.status === "related") && (
              <button
                onClick={onAssess}
                className="flex items-center gap-1.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 px-3 py-1.5 rounded-lg transition-all"
              >
                <ClipboardCheck size={12} />
                {gap.action_label}
              </button>
            )}
            {(gap.status === "needs_development" || gap.status === "missing") && (
              <button
                onClick={onLearn}
                className="flex items-center gap-1.5 text-xs font-semibold text-indigo-700 bg-indigo-100 hover:bg-indigo-200 px-3 py-1.5 rounded-lg transition-all"
              >
                <BookOpen size={12} />
                {gap.action_label}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
