"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type GapAnalysisResult, type CompetencyGap } from "@/lib/api";
import { getSession, getSelectedRole } from "@/lib/session";
import { CheckCircle2, AlertTriangle, HelpCircle, BookOpen, Zap, Info } from "lucide-react";

const LEVEL_LABELS = ["No Evidence", "Awareness", "Basic", "Intermediate", "Advanced", "Expert"];

type ClassificationGroup = "strong_match" | "related" | "needs_verification" | "needs_development" | "missing_evidence";

export default function AnalysisPage() {
  const router = useRouter();
  const [result, setResult] = useState<GapAnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedId, setExpandedId] = useState<number | null>(null);

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

  // Group competencies by classification
  const groupedByClassification = useMemo(() => {
    if (!result) return {
      strong_match: [],
      related: [],
      needs_verification: [],
      needs_development: [],
      missing_evidence: [],
    };
    const groups: Record<ClassificationGroup, CompetencyGap[]> = {
      strong_match: [],
      related: [],
      needs_verification: [],
      needs_development: [],
      missing_evidence: [],
    };
    result.gaps.forEach(gap => {
      const classification = gap.classification as ClassificationGroup;
      if (groups[classification]) {
        groups[classification].push(gap);
      }
    });
    return groups;
  }, [result]);

  if (loading) return (
    <AppShell>
      <div className="flex items-center justify-center h-full min-h-96">
        <div className="text-center">
          <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-sm text-slate-500">Analyzing your competencies...</p>
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

  return (
    <AppShell>
      <div className="max-w-5xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-1">
            Your Path to {result.role_name}
          </h1>
          <p className="text-slate-600">
            Based on your profile, here's what you already have and what you need to develop.
          </p>
        </div>

        {/* SECTION 1: YOU ALREADY HAVE */}
        {groupedByClassification.strong_match.length > 0 && (
          <Section
            title="You Already Have"
            subtitle={`${groupedByClassification.strong_match.length} competency match`}
            icon={<CheckCircle2 size={20} className="text-emerald-600" />}
            items={groupedByClassification.strong_match}
            expandedId={expandedId}
            setExpandedId={setExpandedId}
          />
        )}

        {/* SECTION 2: RELATED EXPERIENCE */}
        {groupedByClassification.related.length > 0 && (
          <Section
            title="Related Experience"
            subtitle={`${groupedByClassification.related.length} transferable competency`}
            icon={<Zap size={20} className="text-amber-600" />}
            items={groupedByClassification.related}
            expandedId={expandedId}
            setExpandedId={setExpandedId}
          />
        )}

        {/* SECTION 3: NEEDS VERIFICATION */}
        {groupedByClassification.needs_verification.length > 0 && (
          <Section
            title="Needs Verification"
            subtitle={`${groupedByClassification.needs_verification.length} competency needs assessment`}
            icon={<HelpCircle size={20} className="text-blue-600" />}
            items={groupedByClassification.needs_verification}
            expandedId={expandedId}
            setExpandedId={setExpandedId}
          />
        )}

        {/* SECTION 4: NEEDS DEVELOPMENT */}
        {groupedByClassification.needs_development.length > 0 && (
          <Section
            title="Needs Development"
            subtitle={`${groupedByClassification.needs_development.length} competency below requirement`}
            icon={<AlertTriangle size={20} className="text-orange-600" />}
            items={groupedByClassification.needs_development}
            expandedId={expandedId}
            setExpandedId={setExpandedId}
          />
        )}

        {/* SECTION 5: MISSING EVIDENCE */}
        {groupedByClassification.missing_evidence.length > 0 && (
          <Section
            title="Missing Evidence"
            subtitle={`${groupedByClassification.missing_evidence.length} competency not found`}
            icon={<BookOpen size={20} className="text-slate-600" />}
            items={groupedByClassification.missing_evidence}
            expandedId={expandedId}
            setExpandedId={setExpandedId}
          />
        )}

        {/* CTA to courses */}
        <div className="mt-8 p-6 bg-gradient-to-r from-indigo-50 to-indigo-100 border border-indigo-200 rounded-2xl flex items-center justify-between gap-4">
          <div>
            <p className="text-lg font-semibold text-indigo-900">Next: Find Learning Resources</p>
            <p className="text-sm text-indigo-700 mt-1">
              Get personalized course recommendations ranked by impact on your gaps.
            </p>
          </div>
          <button
            onClick={() => router.push("/courses")}
            className="shrink-0 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-3 rounded-xl transition-all"
          >
            View Courses
          </button>
        </div>
      </div>
    </AppShell>
  );
}

// ---------------------------------------------------------------------------
// Section component
// ---------------------------------------------------------------------------
function Section({
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
  return (
    <div className="mb-6">
      <div className="flex items-center gap-2 mb-4">
        {icon}
        <div>
          <h2 className="text-lg font-bold text-slate-900">{title}</h2>
          <p className="text-xs text-slate-500">{subtitle}</p>
        </div>
      </div>
      <div className="space-y-3">
        {items.map(gap => (
          <CompetencyCard
            key={gap.competency_id}
            gap={gap}
            isExpanded={expandedId === gap.competency_id}
            onToggle={() => setExpandedId(expandedId === gap.competency_id ? null : gap.competency_id)}
          />
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Competency Card component
// ---------------------------------------------------------------------------
function CompetencyCard({
  gap,
  isExpanded,
  onToggle,
}: {
  gap: CompetencyGap;
  isExpanded: boolean;
  onToggle: () => void;
}) {
  const classificationColors: Record<string, { bg: string; border: string; badge: string }> = {
    strong_match: { bg: "bg-emerald-50", border: "border-emerald-200", badge: "bg-emerald-100 text-emerald-900" },
    related: { bg: "bg-amber-50", border: "border-amber-200", badge: "bg-amber-100 text-amber-900" },
    needs_verification: { bg: "bg-blue-50", border: "border-blue-200", badge: "bg-blue-100 text-blue-900" },
    needs_development: { bg: "bg-orange-50", border: "border-orange-200", badge: "bg-orange-100 text-orange-900" },
    missing_evidence: { bg: "bg-slate-50", border: "border-slate-200", badge: "bg-slate-100 text-slate-900" },
  };

  const colors = classificationColors[gap.classification] || classificationColors.missing_evidence;
  const classificationLabel = gap.classification.replace(/_/g, " ").toUpperCase();

  return (
    <div className={`rounded-xl border ${colors.border} ${colors.bg} p-4 cursor-pointer transition-all hover:shadow-md`} onClick={onToggle}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="font-semibold text-slate-900">{gap.competency_name}</h3>
            <span className={`text-[11px] font-semibold px-2 py-1 rounded-full ${colors.badge}`}>
              {classificationLabel}
            </span>
          </div>
          <p className="text-xs text-slate-600">{gap.category}</p>
        </div>
        <button className="text-slate-500 hover:text-slate-700 shrink-0">
          <Info size={16} />
        </button>
      </div>

      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-slate-200 space-y-3">
          <div>
            <p className="text-xs font-semibold text-slate-600 mb-2">EXPLANATION</p>
            <p className="text-sm text-slate-700 leading-relaxed">{gap.explanation}</p>
          </div>

          {gap.evidence && (
            <div>
              <p className="text-xs font-semibold text-slate-600 mb-1">EVIDENCE</p>
              <p className="text-sm text-slate-700 italic">{gap.evidence}</p>
            </div>
          )}

          {gap.evidence_source && (
            <div className="text-xs text-slate-500">
              Source: {gap.evidence_source}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 text-xs">
            <div>
              <p className="text-slate-500 mb-1">Your Level</p>
              <p className="font-semibold text-slate-900">{LEVEL_LABELS[gap.current_level]}</p>
            </div>
            <div>
              <p className="text-slate-500 mb-1">Required Level</p>
              <p className="font-semibold text-slate-900">{LEVEL_LABELS[gap.required_level]}</p>
            </div>
          </div>

          {gap.confidence < 1 && (
            <div className="bg-white/50 rounded border border-slate-200 p-2">
              <p className="text-xs text-slate-600">
                System confidence: <strong>{Math.round(gap.confidence * 100)}%</strong>
              </p>
            </div>
          )}

          {gap.classification === "needs_verification" && (
            <button className="w-full text-sm font-semibold text-indigo-600 hover:bg-indigo-50 px-3 py-2 rounded transition-colors">
              Take Quick Assessment
            </button>
          )}
        </div>
      )}
    </div>
  );
}
