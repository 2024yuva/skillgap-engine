"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type ParsedResumeProfile } from "@/lib/api";
import { getSession, setSession, getSelectedRole } from "@/lib/session";
import {
  Upload, FileText, CheckCircle2, AlertCircle, Edit3,
  Plus, X, ArrowRight, Loader2, User, GraduationCap,
} from "lucide-react";

const LEVEL_LABELS = ["No Evidence", "Awareness", "Basic", "Intermediate", "Advanced", "Expert"];

export default function ProfilePage() {
  const router = useRouter();
  const session = getSession();
  const fileRef = useRef<HTMLInputElement>(null);

  const [tab, setTab] = useState<"upload" | "manual">("upload");
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [parsing, setParsing] = useState(false);
  const [parsed, setParsed] = useState<ParsedResumeProfile | null>(null);
  const [parseError, setParseError] = useState("");

  // Manual form
  const [manualSkills, setManualSkills] = useState<string[]>([]);
  const [skillInput, setSkillInput] = useState("");

  // Editable state after parsing
  const [editedSkills, setEditedSkills] = useState<string[]>([]);
  const [editedSoftSkills, setEditedSoftSkills] = useState<string[]>([]);
  const [applying, setApplying] = useState(false);
  const [applied, setApplied] = useState(false);

  const selectedRole = typeof window !== "undefined" ? getSelectedRole() : null;

  function onDragOver(e: React.DragEvent) { e.preventDefault(); setDragging(true); }
  function onDragLeave() { setDragging(false); }
  function onDrop(e: React.DragEvent) {
    e.preventDefault(); setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) pickFile(f);
  }
  function pickFile(f: File) {
    setFile(f); setParsed(null); setParseError(""); setApplied(false);
  }

  async function handleParse() {
    if (!file) return;
    setParsing(true); setParseError("");
    try {
      const result = await api.resume.parse(file);
      setParsed(result);
      setEditedSkills(result.technical_skills);
      setEditedSoftSkills(result.soft_skills);
      // Update session name if detected
      if (result.name && session) {
        setSession({ ...session, name: result.name, education: result.education || session.education });
      }
    } catch (e) {
      setParseError(e instanceof Error ? e.message : "Parsing failed.");
    } finally {
      setParsing(false);
    }
  }

  async function handleApply() {
    if (!parsed || !session) return;
    setApplying(true);
    try {
      const levels: Record<number, number> = {};
      for (const [k, v] of Object.entries(parsed.inferred_levels)) {
        levels[Number(k)] = v;
      }
      await api.resume.apply(session.id, {
        inferred_levels: levels,
        name: parsed.name ?? undefined,
        education: parsed.education || undefined,
      });
      setApplied(true);
    } catch (e) {
      setParseError(e instanceof Error ? e.message : "Failed to apply.");
    } finally {
      setApplying(false);
    }
  }

  function addManualSkill() {
    const s = skillInput.trim();
    if (s && !manualSkills.includes(s)) setManualSkills(p => [...p, s]);
    setSkillInput("");
  }

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-7">
          <h1 className="text-2xl font-bold text-slate-900">Create Your Profile</h1>
          <p className="text-sm text-slate-500 mt-1">
            Let AI understand your background by uploading your resume, or add skills manually.
          </p>
        </div>

        {/* Tab switcher */}
        <div className="flex gap-1 bg-white border border-slate-200 rounded-xl p-1 w-fit mb-6 shadow-sm">
          {(["upload", "manual"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-5 py-2 rounded-lg text-sm font-semibold transition-all ${
                tab === t ? "bg-indigo-600 text-white shadow-sm" : "text-slate-500 hover:text-slate-700"
              }`}
            >
              {t === "upload" ? "Upload Resume" : "Manual Input"}
            </button>
          ))}
        </div>

        {tab === "upload" ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Upload card */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
              <h2 className="text-sm font-semibold text-slate-700 mb-4">Upload Your Resume</h2>

              {/* Drop zone */}
              <div
                onDragOver={onDragOver}
                onDragLeave={onDragLeave}
                onDrop={onDrop}
                onClick={() => fileRef.current?.click()}
                className={`
                  border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer transition-all
                  ${dragging ? "border-indigo-500 bg-indigo-50" : "border-slate-200 hover:border-indigo-400 hover:bg-slate-50"}
                `}
              >
                <div className={`w-14 h-14 rounded-full flex items-center justify-center mb-3 transition-all ${dragging ? "bg-indigo-100" : "bg-slate-100"}`}>
                  <Upload size={24} className={dragging ? "text-indigo-500" : "text-slate-400"} />
                </div>
                <p className="text-sm font-semibold text-slate-700">Drag and drop your resume here</p>
                <p className="text-xs text-slate-400 mt-1">or click to <span className="text-indigo-600">upload</span></p>
                <p className="text-xs text-slate-400 mt-3">Supports PDF, DOCX (Max 10MB)</p>
              </div>
              <input
                ref={fileRef}
                type="file"
                accept=".pdf,.docx,.txt"
                className="hidden"
                onChange={e => e.target.files?.[0] && pickFile(e.target.files[0])}
              />

              {/* Selected file */}
              {file && (
                <div className="mt-4 flex items-center gap-3 p-3 bg-indigo-50 border border-indigo-200 rounded-xl">
                  <FileText size={18} className="text-indigo-600 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-slate-800 truncate">{file.name}</p>
                    <p className="text-xs text-slate-500">{(file.size / 1024).toFixed(0)} KB</p>
                  </div>
                  <CheckCircle2 size={16} className="text-emerald-500 shrink-0" />
                </div>
              )}

              {parseError && (
                <div className="mt-3 flex items-start gap-2 p-3 bg-red-50 border border-red-200 rounded-xl">
                  <AlertCircle size={14} className="text-red-500 mt-0.5 shrink-0" />
                  <p className="text-xs text-red-600">{parseError}</p>
                </div>
              )}

              <button
                onClick={handleParse}
                disabled={!file || parsing}
                className="mt-5 w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-semibold py-3 rounded-xl text-sm transition-all"
              >
                {parsing ? <><Loader2 size={15} className="animate-spin" /> Analysing...</> : <><Upload size={15} /> Analyse My Resume</>}
              </button>

              <p className="text-xs text-slate-400 text-center mt-3">
                Your data is secure and used only for analysis.
              </p>
            </div>

            {/* Parsed results */}
            {parsed ? (
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-sm font-semibold text-slate-700">Extracted Skills Preview</h2>
                  <span className="text-xs text-slate-400 bg-emerald-50 text-emerald-600 border border-emerald-200 px-2 py-0.5 rounded-full font-medium">
                    {parsed.matched_competency_ids.length} competencies matched
                  </span>
                </div>

                <p className="text-xs text-slate-400 mb-4">
                  We found the following from your resume. You can add or remove items.
                </p>

                <div className="space-y-4 flex-1 overflow-y-auto custom-scrollbar pr-1">
                  {/* Name + Education */}
                  {(parsed.name || parsed.education) && (
                    <section>
                      <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Profile</h3>
                      {parsed.name && <p className="text-sm text-slate-700 font-medium">{parsed.name}</p>}
                      {parsed.education && <p className="text-xs text-slate-500">{parsed.education}</p>}
                    </section>
                  )}

                  {/* Technical Skills */}
                  <SkillChipGroup
                    label="Technical Skills"
                    color="indigo"
                    items={editedSkills}
                    onRemove={(s) => setEditedSkills(p => p.filter(x => x !== s))}
                  />

                  {/* Soft Skills */}
                  {editedSoftSkills.length > 0 && (
                    <SkillChipGroup
                      label="Soft Skills"
                      color="violet"
                      items={editedSoftSkills}
                      onRemove={(s) => setEditedSoftSkills(p => p.filter(x => x !== s))}
                    />
                  )}

                  {/* Education */}
                  {parsed.education && (
                    <section>
                      <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Education</h3>
                      <p className="text-xs text-slate-600">{parsed.education}</p>
                    </section>
                  )}

                  {/* Experience */}
                  {parsed.experience_summary && (
                    <section>
                      <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Experience</h3>
                      <p className="text-xs text-slate-600">{parsed.experience_summary}</p>
                    </section>
                  )}

                  {/* Courses */}
                  {parsed.courses_certifications.length > 0 && (
                    <section>
                      <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Courses / Certifications</h3>
                      <ul className="space-y-1">
                        {parsed.courses_certifications.map((c, i) => (
                          <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                            <span className="text-indigo-400 mt-0.5">•</span>{c}
                          </li>
                        ))}
                      </ul>
                    </section>
                  )}

                  {/* Inferred levels preview */}
                  <section>
                    <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Inferred Competency Levels</h3>
                    <div className="space-y-1">
                      {Object.entries(parsed.inferred_levels).slice(0, 5).map(([id, level]) => (
                        <div key={id} className="flex items-center justify-between">
                          <span className="text-xs text-slate-600">Competency #{id}</span>
                          <span className="text-xs font-medium text-indigo-600">{LEVEL_LABELS[level]}</span>
                        </div>
                      ))}
                      {Object.keys(parsed.inferred_levels).length > 5 && (
                        <p className="text-xs text-slate-400">+{Object.keys(parsed.inferred_levels).length - 5} more</p>
                      )}
                    </div>
                  </section>
                </div>

                {/* Actions */}
                <div className="flex gap-3 mt-5 pt-4 border-t border-slate-100">
                  <button
                    onClick={handleApply}
                    disabled={applying || applied}
                    className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                      applied
                        ? "bg-emerald-50 text-emerald-600 border border-emerald-200"
                        : "bg-slate-100 hover:bg-slate-200 text-slate-700"
                    }`}
                  >
                    {applying ? <Loader2 size={13} className="animate-spin" /> : applied ? <CheckCircle2 size={13} /> : <Edit3 size={13} />}
                    {applied ? "Applied!" : applying ? "Applying..." : "Edit Skills"}
                  </button>
                  <button
                    onClick={() => {
                      if (!applied) handleApply().then(() => router.push("/role"));
                      else router.push("/role");
                    }}
                    className="flex-1 flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white py-2.5 rounded-xl text-sm font-semibold transition-all"
                  >
                    Confirm &amp; Continue
                    <ArrowRight size={13} />
                  </button>
                </div>
              </div>
            ) : (
              /* Placeholder when nothing parsed yet */
              <div className="bg-white rounded-2xl border border-dashed border-slate-200 p-6 flex flex-col items-center justify-center text-center min-h-64">
                <FileText size={32} className="text-slate-200 mb-3" />
                <p className="text-sm font-semibold text-slate-400">Skills Preview</p>
                <p className="text-xs text-slate-300 mt-1">Upload and analyse your resume to see extracted skills here.</p>
              </div>
            )}
          </div>
        ) : (
          /* Manual input tab */
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 max-w-xl">
            <h2 className="text-sm font-semibold text-slate-700 mb-4">Add Skills Manually</h2>
            <div className="flex gap-2 mb-4">
              <input
                value={skillInput}
                onChange={e => setSkillInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && (e.preventDefault(), addManualSkill())}
                placeholder="e.g. Python, MATLAB, Circuit Analysis..."
                className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
              />
              <button
                onClick={addManualSkill}
                className="bg-indigo-600 text-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-indigo-500 transition-all"
              >
                <Plus size={16} />
              </button>
            </div>
            <div className="flex flex-wrap gap-2 min-h-16">
              {manualSkills.map(s => (
                <span key={s} className="inline-flex items-center gap-1.5 bg-indigo-50 text-indigo-700 border border-indigo-200 px-3 py-1 rounded-full text-xs font-medium">
                  {s}
                  <button onClick={() => setManualSkills(p => p.filter(x => x !== s))} className="hover:text-red-500 transition-colors">
                    <X size={11} />
                  </button>
                </span>
              ))}
              {manualSkills.length === 0 && (
                <p className="text-xs text-slate-400">Add skills above to get started.</p>
              )}
            </div>
            {manualSkills.length > 0 && (
              <button
                onClick={() => router.push("/role")}
                className="mt-5 w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white py-3 rounded-xl text-sm font-semibold transition-all"
              >
                Continue to Target Role <ArrowRight size={14} />
              </button>
            )}
          </div>
        )}

        {/* Progress hint */}
        <div className="mt-8 flex items-center gap-2">
          {[
            { label: "Profile", active: true, done: true },
            { label: "Target Role", active: false, done: false },
            { label: "Analysis", active: false, done: false },
            { label: "Courses", active: false, done: false },
          ].map((s, i) => (
            <div key={s.label} className="flex items-center gap-2">
              {i > 0 && <div className="w-8 h-px bg-slate-200" />}
              <div className={`flex items-center gap-1.5 text-xs font-medium ${s.active ? "text-indigo-600" : "text-slate-400"}`}>
                <div className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${s.done ? "bg-indigo-600 text-white" : s.active ? "border-2 border-indigo-600 text-indigo-600" : "border-2 border-slate-200 text-slate-400"}`}>
                  {i + 1}
                </div>
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}

function SkillChipGroup({ label, color, items, onRemove }: {
  label: string;
  color: "indigo" | "violet";
  items: string[];
  onRemove: (s: string) => void;
}) {
  const bg = color === "indigo" ? "bg-indigo-50 text-indigo-700 border-indigo-200" : "bg-violet-50 text-violet-700 border-violet-200";
  return (
    <section>
      <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">{label}</h3>
      <div className="flex flex-wrap gap-1.5">
        {items.map(s => (
          <span key={s} className={`inline-flex items-center gap-1.5 border px-2.5 py-1 rounded-full text-xs font-medium ${bg}`}>
            {s}
            <button onClick={() => onRemove(s)} className="opacity-60 hover:opacity-100 transition-opacity">
              <X size={10} />
            </button>
          </span>
        ))}
        {items.length === 0 && <p className="text-xs text-slate-400">None detected.</p>}
      </div>
    </section>
  );
}
