"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type Role } from "@/lib/api";
import { saveSelectedRole } from "@/lib/session";
import {
  Search, ArrowRight, Cpu, BarChart2, Zap, Cog, Building2,
  TrendingUp, FlaskConical, Landmark, Layers, ChevronRight,
  Bell, SlidersHorizontal, X, ChevronDown,
} from "lucide-react";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SECTOR_ICONS: Record<string, React.ElementType> = {
  "IT": Cpu,
  "Analytics": BarChart2,
  "Electrical": Zap,
  "Electronics": Cpu,
  "Mechanical": Cog,
  "Civil": Building2,
  "Government / Statistics": Landmark,
  "Statistics": FlaskConical,
  "Management": TrendingUp,
};

const SECTOR_COLORS: Record<string, { bg: string; text: string; iconBg: string; iconText: string }> = {
  "IT":                      { bg: "bg-blue-50",   text: "text-blue-700",   iconBg: "bg-blue-100",   iconText: "text-blue-600" },
  "Analytics":               { bg: "bg-violet-50", text: "text-violet-700", iconBg: "bg-violet-100", iconText: "text-violet-600" },
  "Electrical":              { bg: "bg-yellow-50", text: "text-yellow-700", iconBg: "bg-yellow-100", iconText: "text-yellow-600" },
  "Electronics":             { bg: "bg-orange-50", text: "text-orange-700", iconBg: "bg-orange-100", iconText: "text-orange-600" },
  "Mechanical":              { bg: "bg-slate-50",  text: "text-slate-700",  iconBg: "bg-slate-100",  iconText: "text-slate-600" },
  "Civil":                   { bg: "bg-amber-50",  text: "text-amber-700",  iconBg: "bg-amber-100",  iconText: "text-amber-700" },
  "Government / Statistics": { bg: "bg-teal-50",   text: "text-teal-700",   iconBg: "bg-teal-100",   iconText: "text-teal-600" },
  "Management":              { bg: "bg-pink-50",   text: "text-pink-700",   iconBg: "bg-pink-100",   iconText: "text-pink-600" },
};

const DEFAULT_COLORS = { bg: "bg-slate-50", text: "text-slate-700", iconBg: "bg-slate-100", iconText: "text-slate-600" };

const CATEGORY_TABS = ["All", "3D Printing", "Electrical Engineering", "AutoCAD", "SolidWorks", "Project Management"];

const SECTOR_TO_CATEGORY: Record<string, string> = {
  "IT": "All",
  "Analytics": "All",
  "Electrical": "Electrical Engineering",
  "Electronics": "Electrical Engineering",
  "Mechanical": "3D Printing",
  "Civil": "AutoCAD",
  "Government / Statistics": "All",
  "Management": "Project Management",
};

// Match score simulated from sector (deterministic, not random)
function getMatchScore(role: Role): number {
  const hash = role.name.split("").reduce((acc, c) => acc + c.charCodeAt(0), 0);
  return Math.round(3 + (hash % 70) / 10);
}

const REQUIRED_SKILLS_ALL = [
  "3D Printing", "Electrical Engineering", "AutoCAD", "SolidWorks",
  "Project Management", "Python", "Data Analysis", "Machine Learning",
];

const JOB_TYPES = ["Work from Home", "Part-time", "Internship"];

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function TargetRolePage() {
  const router = useRouter();
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");
  const [selected, setSelected] = useState<Role | null>(null);
  const [viewMode, setViewMode] = useState<"role" | "jobs">("role");

  // Filter state
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [selectedJobTypes, setSelectedJobTypes] = useState<string[]>([]);
  const [salary, setSalary] = useState(0);
  const [experience, setExperience] = useState("");

  useEffect(() => {
    api.roles.list().then(setRoles).catch(console.error).finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    return roles.filter(r => {
      const matchSearch =
        r.name.toLowerCase().includes(search.toLowerCase()) ||
        (r.description ?? "").toLowerCase().includes(search.toLowerCase()) ||
        r.sector.toLowerCase().includes(search.toLowerCase());
      const cat = SECTOR_TO_CATEGORY[r.sector] ?? "All";
      const matchCat = activeCategory === "All" || cat === activeCategory;
      return matchSearch && matchCat;
    });
  }, [roles, search, activeCategory]);

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

  function clearFilters() {
    setSelectedSkills([]);
    setSelectedJobTypes([]);
    setSalary(0);
    setExperience("");
  }

  function handleSelect(role: Role) {
    setSelected(role);
    saveSelectedRole(role.id, role.name);
  }

  function goToAnalysis() {
    if (selected) router.push("/analysis");
  }

  return (
    <AppShell>
      <div className="flex h-full min-h-0">
        {/* ------------------------------------------------------------------ */}
        {/* Left Filter Sidebar                                                  */}
        {/* ------------------------------------------------------------------ */}
        <aside className="w-64 shrink-0 border-r border-slate-200 bg-white overflow-y-auto flex flex-col">
          {/* Save alert */}
          <div className="px-4 py-3 border-b border-slate-100">
            <button className="flex items-center gap-2 text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors">
              <Bell size={13} />
              Save this search as alert
            </button>
          </div>

          {/* Filters header */}
          <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-sm font-bold text-slate-800">
              <SlidersHorizontal size={14} />
              Filters
            </div>
            <button
              onClick={clearFilters}
              className="text-[11px] text-indigo-500 hover:text-indigo-700 font-medium transition-colors"
            >
              Clear all
            </button>
          </div>

          <div className="flex-1 px-4 py-4 space-y-6">
            {/* Profile section placeholder */}
            <div>
              <p className="text-xs font-bold text-slate-700 mb-2 uppercase tracking-wide">Profile</p>
            </div>

            {/* Required Skills */}
            <div>
              <p className="text-xs font-bold text-slate-700 mb-2.5 uppercase tracking-wide">Required Skills</p>
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

            {/* Job Type */}
            <div>
              <p className="text-xs font-bold text-slate-700 mb-2.5 uppercase tracking-wide">Job Type</p>
              <div className="space-y-2">
                {JOB_TYPES.map(jt => (
                  <label key={jt} className="flex items-center gap-2.5 cursor-pointer group">
                    <input
                      type="checkbox"
                      checked={selectedJobTypes.includes(jt)}
                      onChange={() => toggleJobType(jt)}
                      className="w-4 h-4 rounded border-slate-300 accent-indigo-600"
                    />
                    <span className="text-xs text-slate-600 group-hover:text-slate-900 transition-colors">{jt}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Annual Salary */}
            <div>
              <p className="text-xs font-bold text-slate-700 mb-2.5 uppercase tracking-wide">Annual Salary (in lakhs)</p>
              <input
                type="range"
                min={0}
                max={10}
                step={1}
                value={salary}
                onChange={e => setSalary(Number(e.target.value))}
                className="w-full accent-indigo-600"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                {[0, 2, 4, 6, 8, 10].map(v => <span key={v}>{v}</span>)}
              </div>
            </div>

            {/* Years of Experience */}
            <div>
              <p className="text-xs font-bold text-slate-700 mb-2.5 uppercase tracking-wide">Years of Experience</p>
              <div className="relative">
                <select
                  value={experience}
                  onChange={e => setExperience(e.target.value)}
                  className="w-full appearance-none text-xs text-slate-600 border border-slate-200 rounded-lg px-3 py-2 pr-8 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  <option value="">Select years of experience</option>
                  <option value="0">Fresher (0 years)</option>
                  <option value="1">1 year</option>
                  <option value="2">2 years</option>
                  <option value="3">3+ years</option>
                  <option value="5">5+ years</option>
                </select>
                <ChevronDown size={12} className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
              </div>
            </div>
          </div>

          {/* Apply Filters */}
          <div className="px-4 pb-4">
            <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold py-2.5 rounded-xl transition-all shadow-sm">
              Apply Filters
            </button>
          </div>
        </aside>

        {/* ------------------------------------------------------------------ */}
        {/* Main Content                                                         */}
        {/* ------------------------------------------------------------------ */}
        <div className="flex-1 overflow-y-auto bg-[#f8fafc]">
          <div className="max-w-4xl mx-auto px-6 py-8">
            {/* Header */}
            <div className="mb-5">
              <h1 className="text-2xl font-bold text-slate-900">What role are you preparing for?</h1>
              <p className="text-sm text-slate-500 mt-1">
                Explore roles across domains. We will map your gaps and jobs to the selected role.
              </p>
            </div>

            {/* Search */}
            <div className="relative mb-4">
              <Search size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search roles, e.g. Data Analyst, SDE, Statistical Officer..."
                className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 shadow-sm"
              />
            </div>

            {/* Category tabs */}
            <div className="flex gap-2 overflow-x-auto pb-1 mb-5 scrollbar-none">
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

            {/* Role View / Jobs View toggle */}
            <div className="flex mb-5 bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
              <button
                onClick={() => setViewMode("role")}
                className={`flex-1 py-2.5 text-sm font-semibold transition-all ${
                  viewMode === "role"
                    ? "bg-white text-slate-800 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                }`}
              >
                Role View
              </button>
              <button
                onClick={() => setViewMode("jobs")}
                className={`flex-1 py-2.5 text-sm font-semibold transition-all ${
                  viewMode === "jobs"
                    ? "bg-white text-slate-800 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                }`}
              >
                Jobs View
              </button>
            </div>

            {/* Role Cards Grid */}
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-28 bg-slate-100 rounded-2xl animate-pulse" />
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {filtered.map(role => {
                  const Icon = SECTOR_ICONS[role.sector] ?? Layers;
                  const colors = SECTOR_COLORS[role.sector] ?? DEFAULT_COLORS;
                  const isSelected = selected?.id === role.id;
                  const score = getMatchScore(role);

                  return (
                    <button
                      key={role.id}
                      onClick={() => handleSelect(role)}
                      className={`relative text-left p-5 rounded-2xl border-2 transition-all group bg-white ${
                        isSelected
                          ? "border-indigo-500 shadow-md shadow-indigo-100"
                          : "border-slate-200 hover:border-indigo-300 hover:shadow-sm"
                      }`}
                    >
                      {/* Match score badge */}
                      <div className={`absolute top-4 right-4 text-xs font-bold px-2 py-0.5 rounded-full ${
                        score >= 7 ? "bg-green-100 text-green-700" :
                        score >= 5 ? "bg-yellow-100 text-yellow-700" :
                        "bg-red-100 text-red-700"
                      }`}>
                        {score}
                      </div>

                      <div className="flex items-start gap-3 pr-10">
                        {/* Icon */}
                        <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${colors.iconBg}`}>
                          <Icon size={18} className={colors.iconText} />
                        </div>

                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <p className="text-sm font-bold text-slate-800 leading-snug">{role.name}</p>
                            <ChevronRight
                              size={14}
                              className={`shrink-0 transition-colors ${
                                isSelected ? "text-indigo-500" : "text-slate-300 group-hover:text-slate-400"
                              }`}
                            />
                          </div>
                          <span className={`inline-block text-[10px] font-semibold px-2.5 py-0.5 rounded-full mt-1.5 ${colors.bg} ${colors.text}`}>
                            {role.sector}
                          </span>
                          {role.description && (
                            <p className="text-xs text-slate-500 mt-2 line-clamp-2 leading-relaxed">
                              {role.description}
                            </p>
                          )}
                        </div>
                      </div>

                      {/* Selected check */}
                      {isSelected && (
                        <div className="absolute top-3 left-3 w-4 h-4 rounded-full bg-indigo-600 flex items-center justify-center">
                          <svg width="8" height="6" viewBox="0 0 8 6" fill="none">
                            <path d="M1 3l2 2 4-4" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        </div>
                      )}
                    </button>
                  );
                })}
                {filtered.length === 0 && (
                  <div className="col-span-2 text-center py-14 text-slate-400 text-sm">
                    No roles match your search. Try a different keyword or category.
                  </div>
                )}
              </div>
            )}

            {/* CTA */}
            {selected && (
              <div className="mt-6 flex items-center justify-between bg-indigo-50 border border-indigo-200 rounded-2xl p-5">
                <div>
                  <p className="text-sm font-bold text-indigo-900">Selected: {selected.name}</p>
                  <p className="text-xs text-indigo-600 mt-0.5">{selected.sector}</p>
                </div>
                <button
                  onClick={goToAnalysis}
                  className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-all shrink-0"
                >
                  View My Competency Analysis
                  <ArrowRight size={14} />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
