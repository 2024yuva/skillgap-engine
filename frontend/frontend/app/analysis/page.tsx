"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import {
  AlertCircle,
  AlertTriangle,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  HelpCircle,
  Info,
  Loader2,
  TrendingUp,
  Zap,
} from "lucide-react";

import AppShell from "@/components/AppShell";
import {
  api,
  type CompetencyGap,
  type GapAnalysisResult,
} from "@/lib/api";
import { getSelectedRole, getSession } from "@/lib/session";

const LEVEL_LABELS = [
  "No Evidence",
  "Awareness",
  "Basic",
  "Intermediate",
  "Advanced",
  "Expert",
];

type ClassificationGroup =
  | "strong_match"
  | "related"
  | "needs_verification"
  | "needs_development"
  | "missing_evidence";

function getClassification(gap: CompetencyGap): ClassificationGroup {
  if (gap.classification === "missing_evidence") {
    return "missing_evidence";
  }

  if (
    gap.classification === "strong_match" ||
    gap.classification === "related" ||
    gap.classification === "needs_verification" ||
    gap.classification === "needs_development"
  ) {
    return gap.classification;
  }

  // Fallback to status if classification is unavailable
  if (gap.status === "missing") {
    return "missing_evidence";
  }

  return gap.status;
}

export default function AnalysisPage() {
  const router = useRouter();

  const [result, setResult] =
    useState<GapAnalysisResult | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [noRole, setNoRole] = useState(false);

  const [expandedId, setExpandedId] =
    useState<number | null>(null);

  useEffect(() => {
    const session = getSession();
    const role = getSelectedRole();

    if (!session) {
      router.replace("/");
      return;
    }

    if (!role) {
      setNoRole(true);
      setLoading(false);
      return;
    }

    api.analysis
      .gaps(session.id, role.id)
      .then(setResult)
      .catch((e: unknown) => {
        setError(
          e instanceof Error
            ? e.message
            : "Unable to analyze competencies."
        );
      })
      .finally(() => setLoading(false));
  }, [router]);

  const groupedByClassification = useMemo(() => {
    const groups: Record<
      ClassificationGroup,
      CompetencyGap[]
    > = {
      strong_match: [],
      related: [],
      needs_verification: [],
      needs_development: [],
      missing_evidence: [],
    };

    if (!result) {
      return groups;
    }

    result.gaps.forEach((gap) => {
      const classification = getClassification(gap);
      groups[classification].push(gap);
    });

    return groups;
  }, [result]);

  if (noRole) {
    return (
      <AppShell>
        <div className="flex min-h-96 h-full items-center justify-center">
          <div className="max-w-sm px-6 text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl border border-indigo-200 bg-indigo-50">
              <TrendingUp
                size={28}
                className="text-indigo-500"
              />
            </div>

            <h2 className="mb-2 text-lg font-bold text-slate-800">
              No Target Role Selected
            </h2>

            <p className="mb-5 text-sm text-slate-500">
              Choose a target role first so Skillora can analyze
              your competency gaps.
            </p>

            <button
              onClick={() => router.push("/role")}
              className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:bg-indigo-500"
            >
              Choose a Target Role
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </AppShell>
    );
  }

  if (loading) {
    return (
      <AppShell>
        <div className="flex min-h-96 h-full items-center justify-center">
          <div className="text-center">
            <Loader2
              size={32}
              className="mx-auto mb-4 animate-spin text-indigo-500"
            />

            <p className="text-sm text-slate-500">
              Analyzing your competencies...
            </p>
          </div>
        </div>
      </AppShell>
    );
  }

  if (error) {
    return (
      <AppShell>
        <div className="mx-auto max-w-lg px-6 py-16 text-center">
          <AlertCircle
            size={32}
            className="mx-auto mb-3 text-red-400"
          />

          <p className="text-sm font-medium text-red-600">
            {error}
          </p>

          <button
            onClick={() => router.push("/role")}
            className="mt-4 text-sm text-indigo-600 hover:underline"
          >
            Select a role
          </button>
        </div>
      </AppShell>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <AppShell>
      <div className="mx-auto max-w-5xl px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-indigo-600">
            Skill Gap Analysis
          </p>

          <h1 className="mb-2 text-3xl font-bold text-slate-900">
            Your Path to {result.role_name}
          </h1>

          <p className="text-slate-600">
            Based on your profile, here are your strengths,
            transferable skills, and areas to develop.
          </p>
        </div>

        {/* Summary */}
        <div className="mb-8 grid grid-cols-2 gap-4 md:grid-cols-5">
          <SummaryCard
            label="Strong Match"
            count={groupedByClassification.strong_match.length}
            icon={<CheckCircle2 size={18} />}
            className="border-emerald-200 bg-emerald-50 text-emerald-700"
          />

          <SummaryCard
            label="Related"
            count={groupedByClassification.related.length}
            icon={<Zap size={18} />}
            className="border-amber-200 bg-amber-50 text-amber-700"
          />

          <SummaryCard
            label="Verify"
            count={
              groupedByClassification.needs_verification.length
            }
            icon={<HelpCircle size={18} />}
            className="border-blue-200 bg-blue-50 text-blue-700"
          />

          <SummaryCard
            label="Develop"
            count={
              groupedByClassification.needs_development.length
            }
            icon={<TrendingUp size={18} />}
            className="border-orange-200 bg-orange-50 text-orange-700"
          />

          <SummaryCard
            label="Missing"
            count={
              groupedByClassification.missing_evidence.length
            }
            icon={<BookOpen size={18} />}
            className="border-slate-200 bg-slate-50 text-slate-700"
          />
        </div>

        {/* Strong Match */}
        <AnalysisSection
          title="You Already Have"
          subtitle={`${groupedByClassification.strong_match.length} competency match`}
          icon={
            <CheckCircle2
              size={20}
              className="text-emerald-600"
            />
          }
          items={groupedByClassification.strong_match}
          expandedId={expandedId}
          setExpandedId={setExpandedId}
        />

        {/* Related Skills */}
        <AnalysisSection
          title="Related Experience"
          subtitle={`${groupedByClassification.related.length} transferable competency`}
          icon={
            <Zap size={20} className="text-amber-600" />
          }
          items={groupedByClassification.related}
          expandedId={expandedId}
          setExpandedId={setExpandedId}
        />

        {/* Verification */}
        <AnalysisSection
          title="Needs Verification"
          subtitle={`${groupedByClassification.needs_verification.length} competency needs assessment`}
          icon={
            <HelpCircle
              size={20}
              className="text-blue-600"
            />
          }
          items={
            groupedByClassification.needs_verification
          }
          expandedId={expandedId}
          setExpandedId={setExpandedId}
        />

        {/* Development */}
        <AnalysisSection
          title="Needs Development"
          subtitle={`${groupedByClassification.needs_development.length} competency below the required level`}
          icon={
            <AlertTriangle
              size={20}
              className="text-orange-600"
            />
          }
          items={
            groupedByClassification.needs_development
          }
          expandedId={expandedId}
          setExpandedId={setExpandedId}
        />

        {/* Missing */}
        <AnalysisSection
          title="Missing Evidence"
          subtitle={`${groupedByClassification.missing_evidence.length} competency not found in your profile`}
          icon={
            <BookOpen
              size={20}
              className="text-slate-600"
            />
          }
          items={
            groupedByClassification.missing_evidence
          }
          expandedId={expandedId}
          setExpandedId={setExpandedId}
        />

        {/* Next Step */}
        <div className="mt-8 flex flex-col items-start justify-between gap-4 rounded-2xl border border-indigo-200 bg-gradient-to-r from-indigo-50 to-blue-50 p-6 md:flex-row md:items-center">
          <div>
            <p className="text-lg font-semibold text-indigo-900">
              Next: Build Your Learning Path
            </p>

            <p className="mt-1 text-sm text-indigo-700">
              Get personalized course recommendations based on
              your highest-priority skill gaps.
            </p>
          </div>

          <button
            onClick={() => router.push("/courses")}
            className="flex shrink-0 items-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white transition-all hover:bg-indigo-500"
          >
            View Courses
            <ArrowRight size={16} />
          </button>
        </div>

        {/* Readiness */}
        <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5">
          <div className="flex items-center gap-2">
            <Info size={16} className="text-indigo-500" />

            <p className="text-sm font-semibold text-slate-800">
              Career Readiness Score
            </p>
          </div>

          <div className="mt-4">
            <p className="text-4xl font-bold text-indigo-600">
              {result.readiness_score}%
            </p>

            <p className="mt-1 text-xs text-slate-500">
              This score represents your current readiness for the
              selected target role based on competency requirements.
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}

function SummaryCard({
  label,
  count,
  icon,
  className,
}: {
  label: string;
  count: number;
  icon: React.ReactNode;
  className: string;
}) {
  return (
    <div
      className={`rounded-xl border p-4 ${className}`}
    >
      <div className="mb-2 flex items-center gap-2">
        {icon}
        <span className="text-xl font-bold">{count}</span>
      </div>

      <p className="text-xs font-medium">{label}</p>
    </div>
  );
}

function AnalysisSection({
  title,
  subtitle,
  icon,
  items,
  expandedId,
  setExpandedId,
}: {
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  items: CompetencyGap[];
  expandedId: number | null;
  setExpandedId: (id: number | null) => void;
}) {
  if (items.length === 0) {
    return null;
  }

  return (
    <section className="mb-8">
      <div className="mb-4 flex items-center gap-3">
        {icon}

        <div>
          <h2 className="text-lg font-bold text-slate-900">
            {title}
          </h2>

          <p className="text-xs text-slate-500">
            {subtitle}
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {items.map((gap) => (
          <CompetencyCard
            key={gap.competency_id}
            gap={gap}
            isExpanded={
              expandedId === gap.competency_id
            }
            onToggle={() =>
              setExpandedId(
                expandedId === gap.competency_id
                  ? null
                  : gap.competency_id
              )
            }
          />
        ))}
      </div>
    </section>
  );
}

function CompetencyCard({
  gap,
  isExpanded,
  onToggle,
}: {
  gap: CompetencyGap;
  isExpanded: boolean;
  onToggle: () => void;
}) {
  const classification = getClassification(gap);

  const colors: Record<
    ClassificationGroup,
    {
      bg: string;
      border: string;
      badge: string;
    }
  > = {
    strong_match: {
      bg: "bg-emerald-50",
      border: "border-emerald-200",
      badge: "bg-emerald-100 text-emerald-800",
    },

    related: {
      bg: "bg-amber-50",
      border: "border-amber-200",
      badge: "bg-amber-100 text-amber-800",
    },

    needs_verification: {
      bg: "bg-blue-50",
      border: "border-blue-200",
      badge: "bg-blue-100 text-blue-800",
    },

    needs_development: {
      bg: "bg-orange-50",
      border: "border-orange-200",
      badge: "bg-orange-100 text-orange-800",
    },

    missing_evidence: {
      bg: "bg-slate-50",
      border: "border-slate-200",
      badge: "bg-slate-200 text-slate-700",
    },
  };

  const color = colors[classification];

  const label =
    gap.status_label ||
    classification.replace(/_/g, " ");

  const confidence =
    gap.confidence > 1
      ? gap.confidence
      : Math.round(gap.confidence * 100);

  return (
    <div
      className={`cursor-pointer rounded-xl border p-4 transition-all hover:shadow-md ${color.bg} ${color.border}`}
      onClick={onToggle}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <h3 className="font-semibold text-slate-900">
              {gap.competency_name}
            </h3>

            <span
              className={`rounded-full px-2 py-1 text-[10px] font-bold uppercase ${color.badge}`}
            >
              {label}
            </span>
          </div>

          <p className="text-xs text-slate-600">
            {gap.category}
          </p>
        </div>

        <Info
          size={17}
          className="shrink-0 text-slate-500"
        />
      </div>

      {isExpanded && (
        <div className="mt-4 space-y-4 border-t border-slate-200 pt-4">
          <div>
            <p className="mb-1 text-xs font-bold uppercase text-slate-500">
              Explanation
            </p>

            <p className="text-sm leading-relaxed text-slate-700">
              {gap.explanation ||
                gap.status_reason ||
                "Skill analysis based on your current competency profile."}
            </p>
          </div>

          {gap.evidence && (
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-slate-500">
                Evidence
              </p>

              <p className="text-sm italic text-slate-700">
                {gap.evidence}
              </p>
            </div>
          )}

          {gap.evidence_bullets &&
            gap.evidence_bullets.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-bold uppercase text-slate-500">
                  Evidence Found
                </p>

                <ul className="space-y-1">
                  {gap.evidence_bullets.map(
                    (item, index) => (
                      <li
                        key={`${gap.competency_id}-${index}`}
                        className="flex gap-2 text-sm text-slate-700"
                      >
                        <CheckCircle2
                          size={14}
                          className="mt-0.5 shrink-0 text-emerald-500"
                        />

                        {item}
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

          {gap.related_skill_name && (
            <div className="rounded-lg border border-blue-200 bg-blue-50 p-3">
              <p className="text-sm text-blue-800">
                <strong>Related skill detected:</strong>{" "}
                {gap.related_skill_name}
              </p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-slate-500">
                Your Level
              </p>

              <p className="mt-1 font-semibold text-slate-900">
                {LEVEL_LABELS[gap.current_level] ??
                  gap.current_level}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500">
                Required Level
              </p>

              <p className="mt-1 font-semibold text-slate-900">
                {LEVEL_LABELS[gap.required_level] ??
                  gap.required_level}
              </p>
            </div>
          </div>

          <div>
            <div className="mb-1 flex justify-between text-xs text-slate-500">
              <span>System Confidence</span>
              <span>{confidence}%</span>
            </div>

            <div className="h-2 overflow-hidden rounded-full bg-slate-200">
              <div
                className="h-full rounded-full bg-indigo-500"
                style={{
                  width: `${Math.min(
                    Math.max(confidence, 0),
                    100
                  )}%`,
                }}
              />
            </div>
          </div>

          {classification === "needs_verification" && (
            <button
              onClick={(event) => {
                event.stopPropagation();
                window.location.href = `/assessment?competency=${gap.competency_id}`;
              }}
              className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500"
            >
              Take Quick Assessment
            </button>
          )}

          {classification === "needs_development" && (
            <button
              onClick={(event) => {
                event.stopPropagation();
                window.location.href = "/courses";
              }}
              className="w-full rounded-lg border border-indigo-300 bg-white px-4 py-2 text-sm font-semibold text-indigo-700 transition hover:bg-indigo-50"
            >
              Explore Learning Resources
            </button>
          )}
        </div>
      )}
    </div>
  );
}