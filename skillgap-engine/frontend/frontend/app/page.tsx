"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Leaf, ArrowRight, Users } from "lucide-react";
import { api } from "@/lib/api";
import { setSession, getSession } from "@/lib/session";

const STEPS = [
  "Upload Your Resume",
  "AI Extracts Your Skills",
  "Choose Your Target Role",
  "View Competency Analysis",
];

export default function SignUpPage() {
  const router = useRouter();
  const [tab, setTab] = useState<"signup" | "signin">("signup");
  const [name, setName] = useState("");
  const [education, setEducation] = useState("");
  const [department, setDepartment] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [users, setUsers] = useState<{ id: number; name: string; education: string | null }[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(false);

  useEffect(() => {
    const s = getSession();
    if (s) router.replace("/profile");
  }, [router]);

  useEffect(() => {
    if (tab === "signin") {
      setLoadingUsers(true);
      api.users.list().then(setUsers).catch(() => {}).finally(() => setLoadingUsers(false));
    }
  }, [tab]);

  async function handleSignUp(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) { setError("Name is required."); return; }
    setLoading(true); setError("");
    try {
      const user = await api.users.create({
        name: name.trim(),
        education: education.trim() || undefined,
        department: department.trim() || undefined,
      });
      setSession({ id: user.id, name: user.name, education: user.education ?? undefined, department: user.department ?? undefined });
      router.push("/profile");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handleSignIn(user: { id: number; name: string; education: string | null }) {
    setSession({ id: user.id, name: user.name, education: user.education ?? undefined });
    router.push("/profile");
  }

  return (
    <div className="min-h-screen bg-[#0f1117] flex">
      {/* Left panel */}
      <div className="hidden lg:flex lg:w-1/2 flex-col justify-between p-12 relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/40 via-[#0f1117] to-[#0f1117]" />
        <div className="absolute top-20 left-10 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-10 w-48 h-48 bg-violet-600/10 rounded-full blur-3xl" />

        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-10 h-10 rounded-xl bg-indigo-500 flex items-center justify-center">
              <Leaf size={20} className="text-white" />
            </div>
            <div>
              <p className="text-lg font-bold text-white">SkillGap Engine</p>
              <p className="text-xs text-slate-400">From Your Skills to Your Next Opportunity</p>
            </div>
          </div>

          <h1 className="text-3xl font-bold text-white leading-tight mb-3">
            AI-Powered Skill Gap<br />
            Analysis &amp; Learning<br />
            Recommendations
          </h1>
          <p className="text-slate-400 text-sm leading-relaxed mb-10">
            Upload your resume, discover your competency gaps, and get a
            personalised learning path to your dream role.
          </p>

          <div className="space-y-4">
            {STEPS.map((step, i) => (
              <div key={i} className="flex items-center gap-4">
                <div className="w-7 h-7 rounded-full bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-xs font-bold text-indigo-400 shrink-0">
                  {i + 1}
                </div>
                <p className="text-sm text-slate-300 font-medium">{step}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="relative z-10">
          <div className="flex gap-6 text-center">
            {[["7", "Domains"], ["50+", "Competencies"], ["36", "Courses"]].map(([n, l]) => (
              <div key={l}>
                <p className="text-2xl font-bold text-indigo-400">{n}</p>
                <p className="text-xs text-slate-500">{l}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex items-center justify-center p-6 lg:p-12">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="flex items-center gap-2 mb-8 lg:hidden">
            <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center">
              <Leaf size={15} className="text-white" />
            </div>
            <p className="text-base font-bold text-white">SkillGap Engine</p>
          </div>

          <div className="bg-[#1a1d2e] rounded-2xl p-8 border border-[#2d3152]">
            {/* Tab switcher */}
            <div className="flex bg-[#0f1117] rounded-xl p-1 mb-7">
              {(["signup", "signin"] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => { setTab(t); setError(""); }}
                  className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all ${
                    tab === t ? "bg-indigo-600 text-white shadow" : "text-slate-400 hover:text-white"
                  }`}
                >
                  {t === "signup" ? "Get Started" : "Sign In"}
                </button>
              ))}
            </div>

            {tab === "signup" ? (
              <>
                <h2 className="text-xl font-bold text-white mb-1">Create your profile</h2>
                <p className="text-xs text-slate-400 mb-6">No account needed. Just your name to begin.</p>

                <form onSubmit={handleSignUp} className="space-y-4">
                  <div>
                    <label className="text-xs font-semibold text-slate-400 mb-1.5 block">Full Name *</label>
                    <input
                      value={name}
                      onChange={e => setName(e.target.value)}
                      placeholder="e.g. Ananya Sharma"
                      className="w-full bg-[#0f1117] border border-[#2d3152] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-400 mb-1.5 block">Education</label>
                    <input
                      value={education}
                      onChange={e => setEducation(e.target.value)}
                      placeholder="e.g. B.E. Electrical &amp; Electronics"
                      className="w-full bg-[#0f1117] border border-[#2d3152] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-400 mb-1.5 block">Department</label>
                    <input
                      value={department}
                      onChange={e => setDepartment(e.target.value)}
                      placeholder="e.g. Electrical Engineering"
                      className="w-full bg-[#0f1117] border border-[#2d3152] rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all"
                    />
                  </div>

                  {error && <p className="text-xs text-red-400 bg-red-900/20 border border-red-800/40 rounded-lg px-3 py-2">{error}</p>}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-semibold py-3 rounded-xl text-sm transition-all"
                  >
                    {loading ? "Creating..." : "Continue"}
                    {!loading && <ArrowRight size={15} />}
                  </button>
                </form>
              </>
            ) : (
              <>
                <h2 className="text-xl font-bold text-white mb-1">Welcome back</h2>
                <p className="text-xs text-slate-400 mb-6">Select your existing profile to continue.</p>

                {loadingUsers ? (
                  <div className="text-center py-8 text-slate-500 text-sm">Loading profiles...</div>
                ) : users.length === 0 ? (
                  <div className="text-center py-8">
                    <Users size={28} className="text-slate-600 mx-auto mb-2" />
                    <p className="text-slate-400 text-sm">No profiles yet.</p>
                    <button onClick={() => setTab("signup")} className="mt-2 text-indigo-400 text-sm hover:underline">Create one</button>
                  </div>
                ) : (
                  <div className="space-y-2 max-h-72 overflow-y-auto sidebar-scroll pr-1">
                    {users.map(u => (
                      <button
                        key={u.id}
                        onClick={() => handleSignIn(u)}
                        className="w-full flex items-center gap-3 p-3 bg-[#0f1117] hover:bg-[#1e2130] border border-[#2d3152] hover:border-indigo-500/40 rounded-xl text-left transition-all group"
                      >
                        <div className="w-9 h-9 rounded-full bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-sm font-bold text-indigo-400 shrink-0">
                          {u.name.split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase()}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-white truncate">{u.name}</p>
                          <p className="text-xs text-slate-500 truncate">{u.education ?? "No education set"}</p>
                        </div>
                        <ArrowRight size={14} className="text-slate-600 group-hover:text-indigo-400 transition-colors shrink-0" />
                      </button>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>

          <p className="text-center text-xs text-slate-600 mt-5">
            Your data is used only for skill gap analysis.
          </p>
        </div>
      </div>
    </div>
  );
}
