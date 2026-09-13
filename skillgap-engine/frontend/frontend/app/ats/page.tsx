"use client";

import { useState, useRef } from "react";
import {
  Upload,
  FileText,
  Loader2,
  AlertCircle,
  ClipboardCheck,
  X,
} from "lucide-react";
import AppShell from "@/components/AppShell";
import AtsResultsPanel from "@/components/AtsResultsPanel";
import { api, type AtsAnalysisResult } from "@/lib/api";

type InputMode = "file" | "text";

export default function AtsPage() {
  const [mode, setMode] = useState<InputMode>("file");

  // File upload state
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  // Text paste state
  const [rawText, setRawText] = useState("");

  // Result state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AtsAnalysisResult | null>(null);

  // ── File handlers ──────────────────────────────────────────────────────
  function onDragOver(e: React.DragEvent) {
    e.preventDefault();
    setDragging(true);
  }
  function onDragLeave() {
    setDragging(false);
  }
  function onDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) pickFile(f);
  }
  function pickFile(f: File) {
    setFile(f);
    setResult(null);
    setError("");
  }

  // ── Submit ─────────────────────────────────────────────────────────────
  async function handleCheck() {
    setError("");
    setResult(null);
    setLoading(true);

    try {
      if (mode === "file") {
        if (!file) return;
        // Parse via /resume/parse which already bundles ATS analysis
        const parsed = await api.resume.parse(file);
        if (!parsed.ats_analysis) {
          setError("ATS analysis was not returned by the server. Try again.");
          return;
        }
        setResult(parsed.ats_analysis);
      } else {
        // Direct text check via /resume/ats-check
        if (rawText.trim().length < 20) {
          setError("Please paste at least a few lines of resume text.");
          return;
        }
        const data = await api.resume.atsCheck(rawText);
        setResult(data);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function reset() {
    setFile(null);
    setRawText("");
    setResult(null);
    setError("");
  }

  // ── Render ─────────────────────────────────────────────────────────────
  return (
    <AppShell>
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-7">
          <div className="flex items-center gap-2.5 mb-1">
            <ClipboardCheck size={20} className="text-indigo-600" />
            <h1 className="text-2xl font-bold text-slate-900">ATS Resume Checker</h1>
          </div>
          <p className="text-sm text-slate-500">
            Get an instant ATS score, AI content detection, and actionable improvement suggestions.
          </p>
        </div>

        {/* If we have a result, show it full-width with a reset button */}
        {result ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-700">Analysis complete</p>
              <button
                onClick={reset}
                className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-800 border border-slate-200 px-3 py-1.5 rounded-lg transition-colors"
              >
                <X size={12} /> Check another resume
              </button>
            </div>
            <AtsResultsPanel data={result} />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* ── Input card ── */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
              {/* Mode switcher */}
              <div className="flex gap-1 bg-slate-100 rounded-xl p-1 w-fit">
                {(["file", "text"] as InputMode[]).map((m) => (
                  <button
                    key={m}
                    onClick={() => { setMode(m); setError(""); }}
                    className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                      mode === m
                        ? "bg-white text-indigo-600 shadow-sm"
                        : "text-slate-500 hover:text-slate-700"
                    }`}
                  >
                    {m === "file" ? "Upload File" : "Paste Text"}
                  </button>
                ))}
              </div>

              {mode === "file" ? (
                <>
                  {/* Drop zone */}
                  <div
                    onDragOver={onDragOver}
                    onDragLeave={onDragLeave}
                    onDrop={onDrop}
                    onClick={() => fileRef.current?.click()}
                    className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer transition-all ${
                      dragging
                        ? "border-indigo-500 bg-indigo-50"
                        : "border-slate-200 hover:border-indigo-400 hover:bg-slate-50"
                    }`}
                  >
                    <div
                      className={`w-12 h-12 rounded-full flex items-center justify-center mb-3 transition-all ${
                        dragging ? "bg-indigo-100" : "bg-slate-100"
                      }`}
                    >
                      <Upload size={20} className={dragging ? "text-indigo-500" : "text-slate-400"} />
                    </div>
                    <p className="text-sm font-semibold text-slate-700">
                      Drag & drop your resume
                    </p>
                    <p className="text-xs text-slate-400 mt-1">
                      or click to{" "}
                      <span className="text-indigo-600">browse</span>
                    </p>
                    <p className="text-xs text-slate-400 mt-3">PDF, DOCX or TXT · max 10 MB</p>
                  </div>
                  <input
                    ref={fileRef}
                    type="file"
                    accept=".pdf,.docx,.txt"
                    className="hidden"
                    onChange={(e) => e.target.files?.[0] && pickFile(e.target.files[0])}
                  />

                  {/* Selected file pill */}
                  {file && (
                    <div className="flex items-center gap-3 p-3 bg-indigo-50 border border-indigo-200 rounded-xl">
                      <FileText size={16} className="text-indigo-600 shrink-0" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-slate-800 truncate">
                          {file.name}
                        </p>
                        <p className="text-xs text-slate-500">
                          {(file.size / 1024).toFixed(0)} KB
                        </p>
                      </div>
                      <button
                        onClick={(e) => { e.stopPropagation(); setFile(null); }}
                        className="text-slate-400 hover:text-red-500 transition-colors"
                      >
                        <X size={14} />
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <textarea
                  value={rawText}
                  onChange={(e) => setRawText(e.target.value)}
                  placeholder="Paste your resume text here…"
                  rows={12}
                  className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 resize-none custom-scrollbar"
                />
              )}

              {error && (
                <div className="flex items-start gap-2 p-3 bg-red-50 border border-red-200 rounded-xl">
                  <AlertCircle size={14} className="text-red-500 mt-0.5 shrink-0" />
                  <p className="text-xs text-red-600">{error}</p>
                </div>
              )}

              <button
                onClick={handleCheck}
                disabled={loading || (mode === "file" ? !file : rawText.trim().length < 20)}
                className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-semibold py-3 rounded-xl text-sm transition-all"
              >
                {loading ? (
                  <>
                    <Loader2 size={15} className="animate-spin" /> Analysing…
                  </>
                ) : (
                  <>
                    <ClipboardCheck size={15} /> Check My Resume
                  </>
                )}
              </button>
            </div>

            {/* ── Info / placeholder card ── */}
            <div className="bg-white rounded-2xl border border-dashed border-slate-200 p-6 flex flex-col justify-center gap-5">
              <div className="space-y-4">
                {[
                  {
                    color: "bg-indigo-100 text-indigo-600",
                    title: "ATS Score & Grade",
                    desc: "Overall score with sub-scores for formatting, keywords, impact, completeness and readability.",
                  },
                  {
                    color: "bg-violet-100 text-violet-600",
                    title: "AI Content Detection",
                    desc: "Detects AI-written patterns and highlights genuine human markers in your resume.",
                  },
                  {
                    color: "bg-amber-100 text-amber-600",
                    title: "Diagnostics",
                    desc: "Section health checks, action verb strength, quantifiable metrics count, and critical issues.",
                  },
                  {
                    color: "bg-emerald-100 text-emerald-600",
                    title: "Resume Builder Guide",
                    desc: "Bullet-by-bullet rewrites, missing keywords, sections to add, and a formatting checklist.",
                  },
                ].map((item) => (
                  <div key={item.title} className="flex items-start gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${item.color}`}
                    >
                      ✓
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-slate-700">{item.title}</p>
                      <p className="text-xs text-slate-400 mt-0.5">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-xs text-slate-400 border-t border-slate-100 pt-4">
                Powered by Groq · llama-3.3-70b-versatile. Your resume is not stored.
              </p>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
