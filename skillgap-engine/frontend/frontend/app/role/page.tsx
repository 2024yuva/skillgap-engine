"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type RoleMatch, type CompanyJobMatch } from "@/lib/api";
import { getSession, saveSelectedRole } from "@/lib/session";
import {
  Search, ArrowRight, Cpu, BarChart2, Zap, Cog,
  TrendingUp, FlaskConical, Landmark, Layers,
  SlidersHorizontal, X, ExternalLink, Briefcase, Award, CheckCircle2
} from "lucide-react";

// ---------------------------------------------------------------------------
// Constants & Icons
// ---------------------------------------------------------------------------

const ROLE_DOMAIN_ICONS: Record<string, React.ElementType> = {
  "Software Development Engineer": Cpu,
  "Data Analyst":                  BarChart2,
  "Data Scientist":                FlaskConical,
  "ML Engineer":                   TrendingUp,
  "Embedded Systems Engineer":     Cog,
  "IoT Solutions Engineer":        Zap,
  "Electrical Design Engineer":    Zap,
  "Statistical Officer (MoSPI)":   Landmark,
};

const ROLE_DOMAIN_COLORS: Record<string, { bg: string; text: string; iconBg: string; iconText: string }> = {
  "Software Development Engineer": { bg: "bg-blue-50",    text: "text-blue-700",    iconBg: "bg-blue-100",    iconText: "text-blue-600" },
  "Data Analyst":                  { bg: "bg-violet-50",  text: "text-violet-700",  iconBg: "bg-violet-100",  iconText: "text-violet-600" },
  "Data Scientist":                { bg: "bg-indigo-50",  text: "text-indigo-700",  iconBg: "bg-indigo-100",  iconText: "text-indigo-600" },
  "ML Engineer":                   { bg: "bg-purple-50",  text: "text-purple-700",  iconBg: "bg-purple-100",  iconText: "text-purple-600" },
  "Embedded Systems Engineer":     { bg: "bg-orange-50",  text: "text-orange-700",  iconBg: "bg-orange-100",  iconText: "text-orange-600" },
  "IoT Solutions Engineer":        { bg: "bg-cyan-50",    text: "text-cyan-700",    iconBg: "bg-cyan-100",    iconText: "text-cyan-600" },
  "Electrical Design Engineer":    { bg: "bg-yellow-50",  text: "text-yellow-700",  iconBg: "bg-yellow-100",  iconText: "text-yellow-600" },
  "Statistical Officer (MoSPI)":   { bg: "bg-teal-50",    text: "text-teal-700",    iconBg: "bg-teal-100",    iconText: "text-teal-600" },
};

const DEFAULT_COLORS = { bg: "bg-slate-50", text: "text-slate-700", iconBg: "bg-slate-100", iconText: "text-slate-600" };

const CATEGORY_TABS = [
  "All",
  "Software",
  "AI / Data Science",
  "Electronics / Embedded",
  "Electrical Engineering",
  "Government",
];

function getRoleCategory(name: string): string {
  if (name === "Software Development Engineer") return "Software";
  if (name === "Data Analyst" || name === "Data Scientist" || name === "ML Engineer" || name === "Statistical Officer (MoSPI)") return "AI / Data Science";
  if (name === "Embedded Systems Engineer" || name === "IoT Solutions Engineer") return "Electronics / Embedded";
  if (name === "Electrical Design Engineer") return "Electrical Engineering";
  if (name === "Statistical Officer (MoSPI)") return "Government";
  return "All";
}

const JOB_TYPES = ["Full-time", "Internship", "Remote / Hybrid"];
const REQUIRED_SKILLS_ALL = ["Python", "Machine Learning", "Embedded Systems", "MATLAB", "IoT", "Data Analysis", "C Programming", "Statistics"];

// ---------------------------------------------------------------------------
// Main Component
// ---------------------------------------------------------------------------

export default function TargetRolePage() {
  const router = useRouter();
  const session = getSession();

  const [roleMatches, setRoleMatches] = useState<RoleMatch[]>([]);
  const [companyMatches, setCompanyMatches] = useState<CompanyJobMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");
  const [selectedRole, setSelectedRole] = useState<RoleMatch | null>(null);
  const [viewMode, setViewMode] = useState<"role" | "jobs">("role");

  // Filters
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [selectedJobTypes, setSelectedJobTypes] = useState<string[]>([]);

  useEffect(() => {
    const userId = session?.id ?? 1;
    Promise.all([
      api.roles.matches(userId),
      api.roles.companyMatches(userId),
    ])
      .then(([rMatches, cMatches]) => {
        setRoleMatches(rMatches);
        setCompanyMatches(cMatches);
        if (rMatches.length > 0) setSelectedRole(rMatches[0]);
      })
      .catch(err => {
        console.error("Failed to fetch matches:", err);
        api.roles.list().then(roles => {
          const fallbackMatches: RoleMatch[] = roles.map(r => ({
            id: r.id,
            name: r.name,
            sector: r.sector,
            description: r.description,
            match_score: 50,
            matched_count: 3,
            total_required: 6,
            matched_skills: [],
            missing_skills: [],
          }));
          setRoleMatches(fallbackMatches);
          if (fallbackMatches.length > 0) setSelectedRole(fallbackMatches[0]);
        });
      })
      .finally(() => setLoading(false));
  }, []);

  const filteredRoles = useMemo(() => {
    return roleMatches.filter(r => {
      const matchSearch =
        r.name.toLowerCase().includes(search.toLowerCase()) ||
        (r.description ?? "").toLowerCase().includes(search.toLowerCase()) ||
        r.sector.toLowerCase().includes(search.toLowerCase());
      const cat = getRoleCategory(r.name);
      const matchCat = activeCategory === "All" || cat === activeCategory;
      return matchSearch && matchCat;
    });
  }, [roleMatches, search, activeCategory]);

  const filteredCompanies = useMemo(() => {
    return companyMatches.filter(c => {
      const matchSearch =
        c.company_name.toLowerCase().includes(search.toLowerCase()) ||
        c.about_role.toLowerCase().includes(search.toLowerCase()) ||
        c.required_skills.toLowerCase().includes(search.toLowerCase());
      const matchCat =
        activeCategory === "All" ||
        (activeCategory === "Software" && c.category === "Software") ||
        (activeCategory === "Electronics / Embedded" && c.category === "Hardware") ||
        activeCategory === "AI / Data Science";
      return matchSearch && matchCat;
    });
  }, [companyMatches, search, activeCategory]);

  function toggleSkill(skill: string) {
    setSelectedSkills(prev =>
      prev.includes(skill) ? prev.filter(s => s !== skill) : [...prev, skill]
    );
  }

  function toggleJobType(jt: string) {
    setSelectedJobTypes(prev =>
      prev.includes(jt) ? prev.filter(j => j !== jt) : [...prev, jt]
    );
  }

  function handleSelect(role: RoleMatch) {
    setSelectedRole(role);
    saveSelectedRole(role.id, role.name);
  }

  function goToDashboard() {
    if (selectedRole) {
      saveSelectedRole(selectedRole.id, selectedRole.name);
      router.push("/dashboard");
    }
  }

  return (
    <AppShell>
      <div className="flex h-full min-h-0">
        {/* ------------------------------------------------------------------ */}
        {/* Sidebar Filters                                                     */}
        {/* ------------------------------------------------------------------ */}
        <aside className="w-64 shrink-0 border-r border-slate-200 bg-white overflow-y-auto flex flex-col custom-scrollbar">
          <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-sm font-bold text-slate-800">
              <SlidersHorizontal size={14} />
              Filters
            </div>
            <button
              onClick={() => { setSelectedSkills([]); setSelectedJobTypes([]); }}
              className="text-[11px] text-indigo-500 hover:text-indigo-700 font-medium"
            >
              Clear all
            </button>
          </div>

          <div className="flex-1 px-4 py-4 space-y-6">
            <div>
              <p className="text-xs font-bold text-slate-700 mb-2.5 uppercase tracking-wide">Filter Skills</p>
              <div className="flex flex-wrap gap-1.5">
                {REQUIRED_SKILLS_ALL.map(skill => (
                  <button
                    key={skill}
                    onClick={() => toggleSkill(skill)}
                    className={`flex items-center gap-1 text-[11px] font-medium px-2.5 py-1 rounded-full border transition-all ${
                      selectedSkills.includes(skill)
                        ? "bg-indigo-600 text-white border-indigo-600"
                        : "bg-white text-slate-600 border-slate-300 hover:border-indigo-400"
                    }`}
                  >
                    {skill}
                    {selectedSkills.includes(skill) && <X size={10} />}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs font-bold text-slate-700 mb-2.5 uppercase tracking-wide">Job Mode</p>
              <div className="space-y-2">
                {JOB_TYPES.map(jt => (
                  <label key={jt} className="flex items-center gap-2.5 cursor-pointer group">
                    <input
                      type="checkbox"
                      checked={selectedJobTypes.includes(jt)}
                      onChange={() => toggleJobType(jt)}
                      className="w-4 h-4 rounded border-slate-300 accent-indigo-600"
                    />
                    <span className="text-xs text-slate-600 group-hover:text-slate-900">{jt}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* ------------------------------------------------------------------ */}
        {/* Main Content Area                                                   */}
        {/* ------------------------------------------------------------------ */}
        <div className="flex-1 overflow-y-auto bg-[#f8fafc] custom-scrollbar">
          <div className="max-w-4xl mx-auto px-6 py-8">
            {/* Header */}
            <div className="mb-5 flex items-start justify-between">
              <div>
                <h1 className="text-2xl font-bold text-slate-900">Your Recommended Target Roles &amp; Jobs</h1>
                <p className="text-sm text-slate-500 mt-1">
                  Ranked from <strong>most matched</strong> to least matched based on your resume &amp; skills.
                </p>
              </div>
            </div>

            {/* Search Bar */}
            <div className="relative mb-4">
              <Search size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search target roles or companies (e.g. Google, Microsoft, Data Analyst, SDE)..."
                className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 shadow-sm"
              />
            </div>

            {/* Category Tabs */}
            <div className="flex gap-2 overflow-x-auto pb-2 mb-5 thin-scrollbar">
              {CATEGORY_TABS.map(cat => (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`shrink-0 px-4 py-1.5 rounded-full text-xs font-semibold border transition-all ${
                    activeCategory === cat
                      ? "bg-indigo-600 text-white border-indigo-600"
                      : "bg-white text-slate-600 border-slate-200 hover:border-indigo-300"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* View Switcher (Role View vs Jobs View) */}
            <div className="flex mb-6 bg-white border border-slate-200 rounded-xl p-1 shadow-sm">
              <button
                onClick={() => setViewMode("role")}
                className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all flex items-center justify-center gap-2 ${
                  viewMode === "role"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                <Award size={15} />
                Target Roles ({filteredRoles.length})
              </button>
              <button
                onClick={() => setViewMode("jobs")}
                className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all flex items-center justify-center gap-2 ${
                  viewMode === "jobs"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                <Briefcase size={15} />
                Company Jobs ({filteredCompanies.length})
              </button>
            </div>

            {/* Loading Skeleton */}
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-32 bg-slate-200 rounded-2xl animate-pulse" />
                ))}
              </div>
            ) : viewMode === "role" ? (
              /* ------------------------------------------------------------ */
              /* TARGET ROLES VIEW (Ranked Most Matched First)                 */
              /* ------------------------------------------------------------ */
              <div className="space-y-4">
                {filteredRoles.map((role, idx) => {
                  const Icon = ROLE_DOMAIN_ICONS[role.name] ?? Layers;
                  const colors = ROLE_DOMAIN_COLORS[role.name] ?? DEFAULT_COLORS;
                  const isSelected = selectedRole?.id === role.id;

                  return (
                    <div
                      key={role.id}
                      onClick={() => handleSelect(role)}
                      className={`relative p-5 rounded-2xl border-2 transition-all cursor-pointer bg-white ${
                        isSelected
                          ? "border-indigo-600 shadow-md shadow-indigo-100"
                          : "border-slate-200 hover:border-indigo-300 hover:shadow-sm"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex items-start gap-3 flex-1 min-w-0">
                          <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 ${colors.iconBg}`}>
                            <Icon size={20} className={colors.iconText} />
                          </div>

                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-xs font-bold text-slate-400">#{idx + 1} Match</span>
                              <h3 className="text-base font-bold text-slate-800 leading-snug">{role.name}</h3>
                              <span className={`text-[10px] font-semibold px-2.5 py-0.5 rounded-full ${colors.bg} ${colors.text}`}>
                                {role.sector}
                              </span>
                            </div>

                            {role.description && (
                              <p className="text-xs text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                                {role.description}
                              </p>
                            )}

                            {/* Matched vs Missing Skills chips */}
                            <div className="mt-3 flex flex-wrap items-center gap-1.5">
                              {role.matched_skills.slice(0, 4).map(skill => (
                                <span key={skill} className="inline-flex items-center gap-1 text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-0.5 rounded-full">
                                  <CheckCircle2 size={11} className="text-emerald-500" />
                                  {skill}
                                </span>
                              ))}
                              {role.missing_skills.slice(0, 3).map(skill => (
                                <span key={skill} className="inline-flex items-center gap-1 text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200 px-2.5 py-0.5 rounded-full">
                                  Need: {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>

                        {/* Match Score Badge */}
                        <div className="text-right shrink-0">
                          <div className={`inline-flex flex-col items-center justify-center px-3 py-1.5 rounded-xl border ${
                            role.match_score >= 70
                              ? "bg-emerald-50 border-emerald-200 text-emerald-700"
                              : role.match_score >= 40
                              ? "bg-indigo-50 border-indigo-200 text-indigo-700"
                              : "bg-slate-50 border-slate-200 text-slate-600"
                          }`}>
                            <span className="text-lg font-extrabold leading-none">{role.match_score}%</span>
                            <span className="text-[10px] font-medium mt-0.5">Match</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}

                {filteredRoles.length === 0 && (
                  <div className="text-center py-12 text-slate-400 text-sm">
                    No roles match your search filter.
                  </div>
                )}
              </div>
            ) : (
              /* ------------------------------------------------------------ */
              /* COMPANY JOBS VIEW (Ranked Most Matched First)                 */
              /* ------------------------------------------------------------ */
              <div className="space-y-4">
                {filteredCompanies.map((job, idx) => (
                  <div
                    key={idx}
                    className="p-5 rounded-2xl border border-slate-200 bg-white hover:border-indigo-300 hover:shadow-sm transition-all"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap mb-1">
                          <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-0.5 rounded-md">
                            {job.company_name}
                          </span>
                          <span className="text-xs font-medium text-slate-400">• {job.category}</span>
                          <span className="text-xs text-slate-500">💰 {job.salary_lpa}</span>
                        </div>

                        <h3 className="text-base font-bold text-slate-800 leading-snug">{job.about_role}</h3>
                        <p className="text-xs text-slate-500 mt-1">🕒 {job.working_duration}</p>

                        {/* Matched vs Missing Skills */}
                        <div className="mt-3 flex flex-wrap items-center gap-1.5">
                          {job.matched_skills.map(s => (
                            <span key={s} className="text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                              <CheckCircle2 size={10} className="text-emerald-500" />
                              {s}
                            </span>
                          ))}
                          {job.missing_skills.map(s => (
                            <span key={s} className="text-[11px] font-medium bg-slate-100 text-slate-600 px-2.5 py-0.5 rounded-full">
                              Missing: {s}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="flex flex-col items-end gap-3 shrink-0">
                        <div className={`px-3 py-1 rounded-xl text-xs font-bold border ${
                          job.match_score >= 70
                            ? "bg-emerald-50 border-emerald-200 text-emerald-700"
                            : job.match_score >= 40
                            ? "bg-indigo-50 border-indigo-200 text-indigo-700"
                            : "bg-slate-50 border-slate-200 text-slate-600"
                        }`}>
                          {job.match_score}% Match
                        </div>

                        <a
                          href={job.application_link}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-4 py-2 rounded-xl transition-all shadow-sm"
                        >
                          Apply Official <ExternalLink size={12} />
                        </a>
                      </div>
                    </div>
                  </div>
                ))}

                {filteredCompanies.length === 0 && (
                  <div className="text-center py-12 text-slate-400 text-sm">
                    No company job reference matches your filter.
                  </div>
                )}
              </div>
            )}

            {/* Selected Target Role CTA Banner */}
            {selectedRole && (
              <div className="mt-8 flex items-center justify-between bg-indigo-600 text-white rounded-2xl p-5 shadow-lg shadow-indigo-200">
                <div>
                  <p className="text-xs font-semibold text-indigo-200 uppercase tracking-wider">Target Role Selected</p>
                  <p className="text-lg font-bold mt-0.5">{selectedRole.name}</p>
                  <p className="text-xs text-indigo-100 mt-0.5">{selectedRole.match_score}% Skill Match • {selectedRole.sector}</p>
                </div>
                <button
                  onClick={goToDashboard}
                  className="flex items-center gap-2 bg-white text-indigo-700 hover:bg-indigo-50 px-5 py-2.5 rounded-xl text-sm font-bold transition-all shrink-0 shadow-sm"
                >
                  View Learning &amp; Course Path
                  <ArrowRight size={15} />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
