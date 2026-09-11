"use client";

import { useEffect, useState, useRef, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type AssessmentQuestion, type AssessmentResult, type TopicResult } from "@/lib/api";
import { getSession } from "@/lib/session";
import {
  Clock,
  CheckCircle2,
  AlertCircle,
  ChevronLeft,
  ChevronRight,
  Loader2,
  BarChart2,
  TrendingUp,
  Award,
} from "lucide-react";

const TOTAL_MINUTES = 60;

export default function AssessmentPage() {
  return (
    <Suspense fallback={
      <AppShell>
        <div className="flex items-center justify-center min-h-96">
          <Loader2 size={28} className="animate-spin text-indigo-500" />
        </div>
      </AppShell>
    }>
      <AssessmentContent />
    </Suspense>
  );
}

function AssessmentContent() {
  const router = useRouter();
  const params = useSearchParams();
  const competencyId = Number(params.get("competency") ?? 4);

  const [phase, setPhase] = useState<"intro" | "quiz" | "results">("intro");
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [secondsLeft, setSecondsLeft] = useState(TOTAL_MINUTES * 60);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Load questions on mount
  useEffect(() => {
    setLoading(true);
    api.assessment.questions(competencyId)
      .then(setQuestions)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [competencyId]);

  // Timer
  useEffect(() => {
    if (phase !== "quiz") return;
    timerRef.current = setInterval(() => {
      setSecondsLeft((s) => {
        if (s <= 1) { handleSubmit(); return 0; }
        return s - 1;
      });
    }, 1000);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [phase]); // eslint-disable-line

  function startQuiz() {
    setPhase("quiz");
    setSecondsLeft(TOTAL_MINUTES * 60);
  }

  async function handleSubmit() {
    if (timerRef.current) clearInterval(timerRef.current);
    const session = getSession();
    setLoading(true);
    try {
      const res = await api.assessment.submit({
        user_id: session?.id ?? 0,
        competency_id: competencyId,
        answers,
      });
      setResult(res);
      setPhase("results");
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Submission failed");
    } finally {
      setLoading(false);
    }
  }

  const currentQ = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;
  const progressPct = questions.length > 0 ? Math.round((answeredCount / questions.length) * 100) : 0;

  const mm = String(Math.floor(secondsLeft / 60)).padStart(2, "0");
  const ss = String(secondsLeft % 60).padStart(2, "0");
  const timerUrgent = secondsLeft < 300;

  // ── Loading ────────────────────────────────────────────────────────────
  if (loading && phase === "intro") return (
    <AppShell>
      <div className="flex items-center justify-center min-h-96">
        <Loader2 size={28} className="animate-spin text-indigo-500" />
      </div>
    </AppShell>
  );

  if (error) return (
    <AppShell>
      <div className="max-w-lg mx-auto px-6 py-16 text-center">
        <AlertCircle size={32} className="text-red-400 mx-auto mb-3" />
        <p className="text-red-600 text-sm">{error}</p>
        <button onClick={() => router.push("/analysis")} className="mt-4 text-indigo-600 text-sm hover:underline">
          ← Back to Analysis
        </button>
      </div>
    </AppShell>
  );

  // ── INTRO ──────────────────────────────────────────────────────────────
  if (phase === "intro") return (
    <AppShell>
      <div className="max-w-2xl mx-auto px-4 py-10">
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
              <BarChart2 size={20} className="text-indigo-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">DSA Skills Assessment</h1>
              <p className="text-sm text-slate-500">Data Structures &amp; Algorithms</p>
            </div>
          </div>

          <div className="space-y-3 mb-6">
            {[
              ["Questions", `${questions.length} original questions across 9 topics`],
              ["Duration", `Up to ${TOTAL_MINUTES} minutes`],
              ["Topics", "Arrays, Hashing, Trees, Graphs, DP and more"],
              ["Result", "Per-topic competency estimate, not just a score"],
            ].map(([label, value]) => (
              <div key={label} className="flex items-start gap-3">
                <CheckCircle2 size={14} className="text-emerald-500 mt-0.5 shrink-0" />
                <div>
                  <span className="text-sm font-semibold text-slate-700">{label}: </span>
                  <span className="text-sm text-slate-500">{value}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 mb-6">
            <p className="text-sm text-indigo-700">
              <span className="font-semibold">How it works:</span> Answer at your own pace. Your responses update your competency profile. There is no pass/fail — the results show your current strengths and development areas.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={startQuiz}
              disabled={questions.length === 0}
              className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm px-5 py-2.5 rounded-xl transition-all disabled:opacity-50"
            >
              Start Assessment
            </button>
            <button
              onClick={() => router.push("/analysis")}
              className="text-slate-500 hover:text-slate-700 text-sm font-medium px-4 py-2.5"
            >
              Back to Analysis
            </button>
          </div>
        </div>
      </div>
    </AppShell>
  );

  // ── QUIZ ───────────────────────────────────────────────────────────────
  if (phase === "quiz" && currentQ) return (
    <AppShell>
      <div className="max-w-3xl mx-auto px-4 py-6">

        {/* Top bar */}
        <div className="flex items-center justify-between mb-4">
          <div className="text-sm text-slate-500">
            Question <strong className="text-slate-800">{currentIndex + 1}</strong> of{" "}
            <strong className="text-slate-800">{questions.length}</strong>
          </div>
          <div className={`flex items-center gap-1.5 text-sm font-semibold tabular-nums ${timerUrgent ? "text-red-600" : "text-slate-600"}`}>
            <Clock size={14} />
            {mm}:{ss}
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-1.5 bg-slate-100 rounded-full mb-6 overflow-hidden">
          <div
            className="h-full bg-indigo-500 rounded-full transition-all"
            style={{ width: `${progressPct}%` }}
          />
        </div>

        {/* Question card */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 mb-4">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs font-semibold text-indigo-600 bg-indigo-100 px-2 py-0.5 rounded-full">
              {currentQ.topic}
            </span>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
              currentQ.difficulty === "easy"   ? "bg-emerald-100 text-emerald-700" :
              currentQ.difficulty === "medium" ? "bg-yellow-100 text-yellow-700" :
              "bg-red-100 text-red-700"
            }`}>
              {currentQ.difficulty}
            </span>
            <span className="text-xs text-slate-400 ml-auto capitalize">
              {currentQ.question_type.replace("_", " ")}
            </span>
          </div>

          <p className="text-sm font-medium text-slate-800 leading-relaxed whitespace-pre-wrap mb-5">
            {currentQ.question_text}
          </p>

          {/* MCQ / Complexity options */}
          {currentQ.options && (
            <div className="space-y-2">
              {currentQ.options.map((opt) => {
                const letter = opt[0]; // "A", "B", "C", "D"
                const selected = answers[currentQ.id] === letter;
                return (
                  <button
                    key={opt}
                    onClick={() => setAnswers((a) => ({ ...a, [currentQ.id]: letter }))}
                    className={`w-full text-left text-sm px-4 py-3 rounded-xl border transition-all ${
                      selected
                        ? "bg-indigo-600 text-white border-indigo-600 font-semibold"
                        : "bg-white text-slate-700 border-slate-200 hover:border-indigo-300 hover:bg-indigo-50"
                    }`}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>
          )}

          {/* Trace / free-text */}
          {!currentQ.options && (
            <div>
              <p className="text-xs text-slate-500 mb-2">Type your answer:</p>
              <input
                type="text"
                value={answers[currentQ.id] ?? ""}
                onChange={(e) => setAnswers((a) => ({ ...a, [currentQ.id]: e.target.value }))}
                placeholder="Your answer…"
                className="w-full text-sm px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-300 font-mono"
              />
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="flex items-center justify-between gap-3">
          <button
            onClick={() => setCurrentIndex((i) => Math.max(0, i - 1))}
            disabled={currentIndex === 0}
            className="flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700 disabled:opacity-30 px-3 py-2"
          >
            <ChevronLeft size={16} /> Previous
          </button>

          <span className="text-xs text-slate-400">{answeredCount} / {questions.length} answered</span>

          {currentIndex < questions.length - 1 ? (
            <button
              onClick={() => setCurrentIndex((i) => i + 1)}
              className="flex items-center gap-1 text-sm font-semibold text-indigo-600 hover:text-indigo-800 px-3 py-2"
            >
              Next <ChevronRight size={16} />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold px-5 py-2 rounded-xl transition-all disabled:opacity-50"
            >
              {loading && <Loader2 size={14} className="animate-spin" />}
              Submit Assessment
            </button>
          )}
        </div>
      </div>
    </AppShell>
  );

  // ── RESULTS ────────────────────────────────────────────────────────────
  if (phase === "results" && result) return (
    <AppShell>
      <div className="max-w-2xl mx-auto px-4 py-8">

        {/* Score header */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 mb-6 text-center">
          <Award size={36} className="text-indigo-500 mx-auto mb-3" />
          <h1 className="text-xl font-bold text-slate-900 mb-1">Assessment Complete</h1>
          <p className="text-slate-500 text-sm mb-4">{result.competency_name}</p>

          <div className="flex items-center justify-center gap-6">
            <div>
              <p className="text-4xl font-bold text-indigo-600">{result.overall_score}<span className="text-lg text-slate-400">%</span></p>
              <p className="text-xs text-slate-500 mt-1">Overall score</p>
            </div>
            <div className="w-px h-12 bg-slate-200" />
            <div>
              <p className="text-3xl font-bold text-slate-700">{result.verified_level}<span className="text-sm text-slate-400">/5</span></p>
              <p className="text-xs text-slate-500 mt-1">Verified level</p>
            </div>
          </div>

          <p className="text-sm text-slate-600 mt-4 leading-relaxed max-w-md mx-auto">
            {result.summary}
          </p>
        </div>

        {/* Per-topic breakdown */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 mb-6">
          <h2 className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
            <TrendingUp size={16} className="text-indigo-500" />
            By Topic
          </h2>
          <div className="space-y-3">
            {result.topic_results.map((t) => (
              <TopicBar key={t.topic} result={t} />
            ))}
          </div>
        </div>

        <div className="flex gap-3 flex-wrap">
          <button
            onClick={() => router.push("/analysis")}
            className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-all"
          >
            Back to Analysis
          </button>
          <button
            onClick={() => router.push("/courses")}
            className="border border-indigo-300 text-indigo-700 hover:bg-indigo-50 text-sm font-semibold px-5 py-2.5 rounded-xl transition-all"
          >
            View Course Recommendations
          </button>
        </div>
      </div>
    </AppShell>
  );

  return null;
}

function TopicBar({ result }: { result: TopicResult }) {
  const pct = result.score;
  const color =
    result.label === "Strong" ? "bg-emerald-500" :
    result.label === "Intermediate" ? "bg-yellow-400" : "bg-orange-400";
  const textColor =
    result.label === "Strong" ? "text-emerald-700" :
    result.label === "Intermediate" ? "text-yellow-700" : "text-orange-700";
  const bg =
    result.label === "Strong" ? "bg-emerald-100" :
    result.label === "Intermediate" ? "bg-yellow-100" : "bg-orange-100";

  return (
    <div className="flex items-center gap-3">
      <div className="w-36 shrink-0">
        <p className="text-xs text-slate-700 font-medium truncate">{result.topic}</p>
        <p className="text-[11px] text-slate-400">
          {result.questions_correct}/{result.questions_attempted} correct
        </p>
      </div>
      <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all`} style={{ width: `${pct}%` }} />
      </div>
      <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${bg} ${textColor} shrink-0`}>
        {result.label}
      </span>
    </div>
  );
}
