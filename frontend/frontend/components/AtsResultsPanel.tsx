"use client";

import {
  CheckCircle2,
  XCircle,
  AlertTriangle,
  TrendingUp,
  Zap,
  FileText,
  Bot,
  User,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useState } from "react";
import type {
  AtsAnalysisResult,
  SectionHealthItem,
  BulletPointImprovement,
  FormattingChecklistItem,
} from "@/lib/api";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function gradeColor(grade: string): string {
  switch (grade?.toUpperCase()) {
    case "A+":
    case "A":
      return "text-emerald-600 bg-emerald-50 border-emerald-200";
    case "B+":
    case "B":
      return "text-indigo-600 bg-indigo-50 border-indigo-200";
    case "C+":
    case "C":
      return "text-amber-600 bg-amber-50 border-amber-200";
    default:
      return "text-red-600 bg-red-50 border-red-200";
  }
}

function scoreColor(score: number): string {
  if (score >= 75) return "bg-emerald-500";
  if (score >= 50) return "bg-indigo-500";
  if (score >= 30) return "bg-amber-500";
  return "bg-red-500";
}

function sectionStatusIcon(status: SectionHealthItem["status"]) {
  if (status === "good")
    return <CheckCircle2 size={14} className="text-emerald-500 shrink-0" />;
  if (status === "warning")
    return <AlertTriangle size={14} className="text-amber-500 shrink-0" />;
  return <XCircle size={14} className="text-red-500 shrink-0" />;
}

function aiVerdictColor(score: number): string {
  if (score >= 70) return "text-red-600 bg-red-50 border-red-200";
  if (score >= 40) return "text-amber-600 bg-amber-50 border-amber-200";
  return "text-emerald-600 bg-emerald-50 border-emerald-200";
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function ScoreBar({ label, score }: { label: string; score: number }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-slate-600">{label}</span>
        <span className="font-semibold text-slate-800">{score}</span>
      </div>
      <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${scoreColor(score)}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

function Section({
  title,
  icon,
  children,
  defaultOpen = true,
}: {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <button
        className="w-full flex items-center justify-between px-5 py-4 hover:bg-slate-50 transition-colors no-ripple"
        onClick={() => setOpen((o) => !o)}
      >
        <div className="flex items-center gap-2.5">
          {icon}
          <span className="text-sm font-semibold text-slate-800">{title}</span>
        </div>
        {open ? (
          <ChevronUp size={15} className="text-slate-400" />
        ) : (
          <ChevronDown size={15} className="text-slate-400" />
        )}
      </button>
      {open && <div className="px-5 pb-5 border-t border-slate-100">{children}</div>}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function AtsResultsPanel({ data }: { data: AtsAnalysisResult }) {
  const { ai_detection, ats_scoring, diagnostics, resume_builder_guide } = data;

  return (
    <div className="space-y-4">
      {/* ── Top summary row ───────────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {/* ATS Overall */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 flex flex-col items-center gap-1">
          <span className="text-xs text-slate-500 font-medium">ATS Score</span>
          <span className="text-3xl font-extrabold text-slate-900">{ats_scoring.overall_score}</span>
          <span
            className={`text-xs font-bold px-2 py-0.5 rounded-full border ${gradeColor(ats_scoring.grade)}`}
          >
            {ats_scoring.grade}
          </span>
        </div>

        {/* AI detection */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 flex flex-col items-center gap-1">
          <span className="text-xs text-slate-500 font-medium">AI Probability</span>
          <span className="text-3xl font-extrabold text-slate-900">
            {ai_detection.ai_probability_score}%
          </span>
          <span
            className={`text-xs font-bold px-2 py-0.5 rounded-full border ${aiVerdictColor(ai_detection.ai_probability_score)}`}
          >
            {ai_detection.verdict}
          </span>
        </div>

        {/* Strengths */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 flex flex-col items-center gap-1">
          <span className="text-xs text-slate-500 font-medium">Key Strengths</span>
          <span className="text-3xl font-extrabold text-emerald-600">
            {diagnostics.key_strengths.length}
          </span>
          <span className="text-xs text-slate-400">identified</span>
        </div>

        {/* Critical issues */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 flex flex-col items-center gap-1">
          <span className="text-xs text-slate-500 font-medium">Issues</span>
          <span className="text-3xl font-extrabold text-red-500">
            {diagnostics.critical_issues.length}
          </span>
          <span className="text-xs text-slate-400">to fix</span>
        </div>
      </div>

      {/* ── ATS Scoring breakdown ─────────────────────────────────────── */}
      <Section
        title="ATS Score Breakdown"
        icon={<TrendingUp size={15} className="text-indigo-500" />}
      >
        <div className="mt-4 space-y-3">
          <ScoreBar label="Formatting" score={ats_scoring.formatting_score} />
          <ScoreBar label="Impact" score={ats_scoring.impact_score} />
          <ScoreBar label="Metrics & Numbers" score={ats_scoring.metrics_score} />
          <ScoreBar label="Completeness" score={ats_scoring.completeness_score} />
          <ScoreBar label="Readability" score={ats_scoring.readability_score} />
          <ScoreBar label="Keyword Match" score={ats_scoring.keyword_score} />
        </div>
      </Section>

      {/* ── AI Detection ─────────────────────────────────────────────── */}
      <Section
        title="AI Content Detection"
        icon={<Bot size={15} className="text-violet-500" />}
      >
        <div className="mt-4 space-y-4">
          {/* Human vs AI bar */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs text-slate-500">
              <span className="flex items-center gap-1">
                <Bot size={11} className="text-red-400" /> AI-generated
              </span>
              <span className="flex items-center gap-1">
                Human-written <User size={11} className="text-emerald-400" />
              </span>
            </div>
            <div className="flex h-3 w-full rounded-full overflow-hidden">
              <div
                className="bg-red-400 transition-all duration-500"
                style={{ width: `${ai_detection.ai_probability_score}%` }}
              />
              <div className="flex-1 bg-emerald-400" />
            </div>
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-red-500">{ai_detection.ai_probability_score}%</span>
              <span className="text-emerald-600">{ai_detection.human_score}%</span>
            </div>
          </div>

          <p className="text-xs text-slate-600 bg-slate-50 rounded-xl p-3 border border-slate-100">
            {ai_detection.verdict_summary}
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {ai_detection.flagged_ai_patterns.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-red-600 mb-2">Flagged AI patterns</p>
                <ul className="space-y-1">
                  {ai_detection.flagged_ai_patterns.map((p, i) => (
                    <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                      <XCircle size={11} className="text-red-400 mt-0.5 shrink-0" />
                      {p}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {ai_detection.human_markers.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-emerald-600 mb-2">Human markers</p>
                <ul className="space-y-1">
                  {ai_detection.human_markers.map((m, i) => (
                    <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                      <CheckCircle2 size={11} className="text-emerald-400 mt-0.5 shrink-0" />
                      {m}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </Section>

      {/* ── Diagnostics ──────────────────────────────────────────────── */}
      <Section
        title="Diagnostics"
        icon={<Zap size={15} className="text-amber-500" />}
      >
        <div className="mt-4 space-y-5">
          {/* Strengths & Issues */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {diagnostics.key_strengths.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-emerald-700 mb-2">Key Strengths</p>
                <ul className="space-y-1.5">
                  {diagnostics.key_strengths.map((s, i) => (
                    <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                      <CheckCircle2 size={11} className="text-emerald-400 mt-0.5 shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {diagnostics.critical_issues.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-red-600 mb-2">Critical Issues</p>
                <ul className="space-y-1.5">
                  {diagnostics.critical_issues.map((s, i) => (
                    <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                      <XCircle size={11} className="text-red-400 mt-0.5 shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Section health */}
          {diagnostics.section_health.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-slate-700 mb-2">Section Health</p>
              <div className="space-y-2">
                {diagnostics.section_health.map((sh, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-2 p-2.5 rounded-xl border border-slate-100 bg-slate-50"
                  >
                    {sectionStatusIcon(sh.status)}
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-semibold text-slate-700">{sh.section}</p>
                      <p className="text-xs text-slate-500">{sh.feedback}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Action verbs */}
          {(diagnostics.action_verbs_strong.length > 0 ||
            diagnostics.action_verbs_weak.length > 0) && (
            <div className="grid grid-cols-2 gap-3">
              {diagnostics.action_verbs_strong.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-emerald-700 mb-1.5">Strong verbs</p>
                  <div className="flex flex-wrap gap-1.5">
                    {diagnostics.action_verbs_strong.map((v, i) => (
                      <span
                        key={i}
                        className="text-[11px] font-medium px-2 py-0.5 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-full"
                      >
                        {v}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {diagnostics.action_verbs_weak.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-amber-700 mb-1.5">Weak verbs</p>
                  <div className="flex flex-wrap gap-1.5">
                    {diagnostics.action_verbs_weak.map((v, i) => (
                      <span
                        key={i}
                        className="text-[11px] font-medium px-2 py-0.5 bg-amber-50 border border-amber-200 text-amber-700 rounded-full"
                      >
                        {v}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Metrics */}
          {diagnostics.quantifiable_metrics_count > 0 && (
            <div>
              <p className="text-xs font-semibold text-slate-700 mb-1.5">
                Quantifiable metrics ({diagnostics.quantifiable_metrics_count} found)
              </p>
              <div className="flex flex-wrap gap-1.5">
                {diagnostics.quantifiable_metrics_examples.map((m, i) => (
                  <span
                    key={i}
                    className="text-[11px] font-medium px-2 py-0.5 bg-indigo-50 border border-indigo-200 text-indigo-700 rounded-full"
                  >
                    {m}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </Section>

      {/* ── Resume Builder Guide ──────────────────────────────────────── */}
      <Section
        title="Resume Builder Guide"
        icon={<FileText size={15} className="text-indigo-500" />}
        defaultOpen={false}
      >
        <div className="mt-4 space-y-5">
          {/* Top recommendations */}
          {resume_builder_guide.top_actionable_recommendations.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-slate-700 mb-2">Top Recommendations</p>
              <ol className="space-y-2">
                {resume_builder_guide.top_actionable_recommendations.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-600">
                    <span className="mt-0.5 w-4 h-4 rounded-full bg-indigo-100 text-indigo-600 font-bold text-[10px] flex items-center justify-center shrink-0">
                      {i + 1}
                    </span>
                    {r}
                  </li>
                ))}
              </ol>
            </div>
          )}

          {/* Missing keywords */}
          {resume_builder_guide.missing_critical_keywords.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-red-600 mb-1.5">Missing Critical Keywords</p>
              <div className="flex flex-wrap gap-1.5">
                {resume_builder_guide.missing_critical_keywords.map((k, i) => (
                  <span
                    key={i}
                    className="text-[11px] font-medium px-2 py-0.5 bg-red-50 border border-red-200 text-red-600 rounded-full"
                  >
                    {k}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Sections to add */}
          {resume_builder_guide.recommended_sections_to_add.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-amber-700 mb-1.5">Sections to Add</p>
              <div className="flex flex-wrap gap-1.5">
                {resume_builder_guide.recommended_sections_to_add.map((s, i) => (
                  <span
                    key={i}
                    className="text-[11px] font-medium px-2 py-0.5 bg-amber-50 border border-amber-200 text-amber-700 rounded-full"
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Bullet improvements */}
          {resume_builder_guide.bullet_point_improvements.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-slate-700 mb-2">Bullet Point Improvements</p>
              <div className="space-y-3">
                {resume_builder_guide.bullet_point_improvements.map(
                  (b: BulletPointImprovement, i: number) => (
                    <div
                      key={i}
                      className="rounded-xl border border-slate-100 overflow-hidden text-xs"
                    >
                      <div className="px-3 py-2 bg-red-50 border-b border-red-100 text-red-700">
                        <span className="font-semibold">Before: </span>
                        {b.original}
                      </div>
                      <div className="px-3 py-2 bg-emerald-50 border-b border-emerald-100 text-emerald-700">
                        <span className="font-semibold">After: </span>
                        {b.improved}
                      </div>
                      <div className="px-3 py-2 bg-slate-50 text-slate-500">
                        <span className="font-semibold text-slate-600">Formula: </span>
                        {b.formula_applied} — {b.explanation}
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}

          {/* Formatting checklist */}
          {resume_builder_guide.formatting_checklist.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-slate-700 mb-2">Formatting Checklist</p>
              <div className="space-y-2">
                {resume_builder_guide.formatting_checklist.map(
                  (item: FormattingChecklistItem, i: number) => (
                    <div key={i} className="flex items-start gap-2">
                      {item.passed ? (
                        <CheckCircle2 size={13} className="text-emerald-500 mt-0.5 shrink-0" />
                      ) : (
                        <XCircle size={13} className="text-red-400 mt-0.5 shrink-0" />
                      )}
                      <div>
                        <p className="text-xs text-slate-700">{item.item}</p>
                        {!item.passed && (
                          <p className="text-[11px] text-slate-400 mt-0.5">{item.tip}</p>
                        )}
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}
        </div>
      </Section>
    </div>
  );
}
