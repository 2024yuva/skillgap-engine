"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import {
  api,
  type AssessmentQuestion,
  type AssessmentResult,
  type AssessmentSession,
} from "@/lib/api";
import { getSession, getSelectedRole } from "@/lib/session";
import {
  ClipboardCheck,
  ArrowRight,
  Clock,
  Lock,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  Map,
} from "lucide-react";

function formatTime(total: number) {
  const s = Math.max(0, total);
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${String(m).padStart(2, "0")}:${String(r).padStart(2, "0")}`;
}

function bandClass(band: string) {
  if (band === "Strong") return "bg-emerald-50 text-emerald-700 border-emerald-200";
  if (band === "Intermediate") return "bg-indigo-50 text-indigo-700 border-indigo-200";
  return "bg-orange-50 text-orange-700 border-orange-200";
}

export default function AssessmentPage() {
  const router = useRouter();
  const [phase, setPhase] = useState<"landing" | "live" | "results">("landing");
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [latest, setLatest] = useState<AssessmentSession | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [question, setQuestion] = useState<AssessmentQuestion | null>(null);
  const [answered, setAnswered] = useState(0);
  const [maxQ, setMaxQ] = useState(16);
  const [remaining, setRemaining] = useState(3600);
  const [choice, setChoice] = useState("");
  const [code, setCode] = useState("");
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const remainingRef = useRef(3600);
  const expireSent = useRef(false);

  useEffect(() => {
    const session = getSession();
    if (!session) { router.replace("/"); return; }
    api.assessment.latest(session.id)
      .then((r) => {
        if (r.completed && r.result) setLatest(r);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  useEffect(() => {
    remainingRef.current = remaining;
  }, [remaining]);

  useEffect(() => {
    if (phase !== "live") return;
    const t = setInterval(() => {
      setRemaining((prev) => {
        if (prev <= 1) return 0;
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(t);
  }, [phase]);

  const applyPayload = useCallback((data: AssessmentSession) => {
    if (data.session_id) setSessionId(data.session_id);
    if (data.progress) {
      setAnswered(data.progress.answered);
      setMaxQ(data.progress.max_questions);
      setRemaining(data.progress.remaining_seconds);
    }
    if (data.completed && data.result) {
      setResult(data.result);
      setPhase("results");
      setQuestion(null);
      return;
    }
    setQuestion(data.question ?? null);
    setChoice("");
    setCode(data.question?.starter ?? "");
    setPhase("live");
    expireSent.current = false;
  }, []);

  async function start() {
    const session = getSession();
    const role = getSelectedRole();
    if (!session) { router.replace("/"); return; }
    if (!role) { router.replace("/role"); return; }
    setStarting(true);
    setError("");
    try {
      const data = await api.assessment.start(session.id, role.id);
      applyPayload(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not start assessment");
    } finally {
      setStarting(false);
    }
  }

  async function submit() {
    if (!sessionId || submitting) return;
    const answer = question?.qtype === "coding" ? code : choice;
    if (question?.qtype !== "coding" && !choice) return;
    setSubmitting(true);
    setError("");
    try {
      const data = await api.assessment.submit(sessionId, answer);
      applyPayload(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Submit failed");
    } finally {
      setSubmitting(false);
    }
  }

  useEffect(() => {
    if (phase !== "live" || remaining !== 0 || !sessionId || expireSent.current) return;
    expireSent.current = true;
    api.assessment.submit(sessionId, question?.qtype === "coding" ? code : choice)
      .then(applyPayload)
      .catch(() => {});
  }, [remaining, phase, sessionId, applyPayload, question, code, choice]);

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center h-full min-h-96">
          <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
        </div>
      </AppShell>
    );
  }

  if (phase === "results" && result) {
    return (
      <AppShell>
        <ResultsView result={result} onRetake={() => { setPhase("landing"); setResult(null); }} />
      </AppShell>
    );
  }

  if (phase === "live" && question) {
    const pct = Math.min(100, (answered / maxQ) * 100);
    const urgent = remaining < 300;
    return (
      <AppShell>
        <div className="max-w-3xl mx-auto px-6 py-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">DSA Skill Assessment</p>
              <h1 className="text-xl font-bold text-slate-900 mt-0.5">{question.topic_label}</h1>
            </div>
            <div className={`inline-flex items-center gap-2 px-3 py-2 rounded-xl border text-sm font-semibold ${
              urgent ? "bg-red-50 text-red-700 border-red-200" : "bg-white text-slate-700 border-slate-200"
            }`}>
              <Clock size={14} />
              {formatTime(remaining)} remaining
              <Lock size={12} className="text-slate-400" />
            </div>
          </div>

          <div className="mb-5">
            <div className="flex justify-between text-xs text-slate-500 mb-1.5">
              <span>Question {Math.min(answered + 1, maxQ)} of {maxQ}</span>
              <span>{question.difficulty_label} · {labelForType(question.qtype)}</span>
            </div>
            <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
              <div className="h-full bg-indigo-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
            </div>
          </div>

          {error && (
            <p className="text-sm text-red-600 mb-3">{error}</p>
          )}

          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
            <p className="text-sm text-slate-800 leading-relaxed">{question.prompt}</p>

            {question.qtype === "coding" ? (
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck={false}
                className="mt-5 w-full min-h-48 font-mono text-xs bg-slate-50 border border-slate-200 rounded-xl p-4 text-slate-800 focus:outline-none focus:border-indigo-400"
              />
            ) : (
              <div className="mt-5 space-y-2">
                {(question.options ?? []).map((opt) => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setChoice(opt)}
                    className={`w-full text-left text-sm px-4 py-3 rounded-xl border transition-all ${
                      choice === opt
                        ? "bg-indigo-50 border-indigo-400 text-indigo-900 font-medium"
                        : "bg-white border-slate-200 text-slate-700 hover:border-indigo-300"
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            )}

            <div className="mt-6 flex justify-end">
              <button
                onClick={submit}
                disabled={submitting || (question.qtype !== "coding" && !choice)}
                className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-all"
              >
                {submitting ? "Checking..." : answered + 1 >= maxQ ? "Finish" : "Submit"}
                <ArrowRight size={14} />
              </button>
            </div>
          </div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="max-w-2xl mx-auto px-6 py-16">
        <div className="text-center">
          <div className="w-16 h-16 rounded-2xl bg-indigo-50 border border-indigo-200 flex items-center justify-center mx-auto mb-5">
            <ClipboardCheck size={28} className="text-indigo-600" />
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">DSA Skill Assessment</h1>
          <p className="text-slate-500 text-sm leading-relaxed mb-8">
            Measures whether you have the data-structures and algorithms competency
            required by your target role. Difficulty adapts to your answers. Maximum
            duration is 60 minutes — it can finish earlier once the estimate is confident.
          </p>
        </div>

        {error && (
          <p className="text-sm text-red-600 text-center mb-4">{error}</p>
        )}

        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 text-left space-y-4 mb-8">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-wide">What to expect</p>
          {[
            "Up to 16 items across eight DSA areas (concept, tracing, and short coding)",
            "Adaptive difficulty from your resume evidence and live answers",
            "Locked timer (60:00 max) — no going back",
            "Results update your SkillGap DSA competency and learning path",
          ].map((f) => (
            <div key={f} className="flex items-center gap-3 text-sm text-slate-600">
              <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 shrink-0" />
              {f}
            </div>
          ))}
        </div>

        {latest?.result && (
          <div className="bg-white border border-slate-200 rounded-2xl p-5 mb-8 text-left">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Last result</p>
            <p className="text-sm text-slate-800">
              Overall: <strong>{latest.result.overall_label}</strong>
              <span className={`ml-2 text-xs px-2 py-0.5 rounded-full border ${bandClass(latest.result.overall_band)}`}>
                {latest.result.overall_band}
              </span>
            </p>
            <button
              onClick={() => { setResult(latest.result!); setPhase("results"); }}
              className="mt-2 text-sm text-indigo-600 hover:underline font-medium"
            >
              View last report
            </button>
          </div>
        )}

        <div className="text-center">
          <button
            onClick={start}
            disabled={starting}
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-6 py-3 rounded-xl text-sm font-semibold transition-all"
          >
            {starting ? "Preparing..." : "Start assessment"}
            <ArrowRight size={14} />
          </button>
        </div>
      </div>
    </AppShell>
  );
}

function labelForType(t: string) {
  if (t === "concept") return "Concept";
  if (t === "tracing") return "Code tracing";
  if (t === "coding") return "Short coding";
  return "Problem solving";
}

function ResultsView({ result, onRetake }: { result: AssessmentResult; onRetake: () => void }) {
  const router = useRouter();
  const gaps = result.biggest_gaps.map((g) => g.label).join(" and ");

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">DSA Skill Assessment</h1>
          <p className="text-sm text-slate-500 mt-1">
            Overall: <span className="font-semibold text-slate-800">{result.overall_label}</span>
            {result.early_stop && (
              <span className="text-slate-400"> · finished early with sufficient confidence</span>
            )}
            {result.timed_out && (
              <span className="text-slate-400"> · time limit reached</span>
            )}
          </p>
        </div>
        <div className={`inline-flex items-center gap-2 px-3 py-2 rounded-xl border text-sm font-semibold ${bandClass(result.overall_band)}`}>
          {result.overall_band}
        </div>
      </div>

      {result.biggest_gaps.length > 0 && (
        <div className="bg-orange-50 border border-orange-200 rounded-2xl p-4 mb-6">
          <div className="flex items-start gap-2">
            <AlertTriangle size={14} className="text-orange-500 mt-0.5 shrink-0" />
            <p className="text-xs text-orange-800 font-medium">
              Your biggest DSA gaps are {gaps}. These levels now feed SkillGap analysis
              for Data Structures &amp; Algorithms.
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8">
        {result.topics.map((t) => (
          <div key={t.topic} className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <p className="text-sm font-semibold text-slate-800">{t.label}</p>
              <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${bandClass(t.band)}`}>
                {t.band}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-2">
              {t.correct}/{t.asked} correct · confidence {Math.round(t.confidence * 100)}%
            </p>
          </div>
        ))}
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm mb-6">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Recommended next steps</p>
        <ol className="space-y-2">
          {result.next_steps.map((s, i) => (
            <li key={s} className="flex gap-3 text-sm text-slate-700">
              <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center shrink-0">
                {i + 1}
              </span>
              {s}
            </li>
          ))}
        </ol>
      </div>

      {result.review && result.review.length > 0 && (
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm mb-6">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Item review</p>
          <div className="space-y-3">
            {result.review.map((r) => (
              <div key={r.question_id} className="border border-slate-100 rounded-xl p-3">
                <div className="flex items-center gap-2 mb-1">
                  {r.correct
                    ? <CheckCircle2 size={14} className="text-emerald-500" />
                    : <AlertTriangle size={14} className="text-orange-500" />}
                  <span className="text-[10px] text-slate-400 font-medium">{r.topic_label}</span>
                </div>
                <p className="text-xs text-slate-700 leading-relaxed">{r.prompt}</p>
                <p className="text-xs text-slate-500 mt-1.5">{r.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => router.push("/analysis")}
          className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-all"
        >
          View updated analysis
          <ArrowRight size={14} />
        </button>
        <button
          onClick={() => router.push("/learning")}
          className="inline-flex items-center gap-2 bg-white border border-slate-200 hover:border-indigo-300 text-slate-700 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all"
        >
          <Map size={14} />
          Learning path
        </button>
        <button
          onClick={() => router.push("/courses")}
          className="inline-flex items-center gap-2 bg-white border border-slate-200 hover:border-indigo-300 text-slate-700 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all"
        >
          <BookOpen size={14} />
          Courses
        </button>
        <button
          onClick={onRetake}
          className="inline-flex items-center gap-2 text-slate-500 hover:text-indigo-600 px-3 py-2.5 text-sm font-medium"
        >
          Retake
        </button>
      </div>
    </div>
  );
}
