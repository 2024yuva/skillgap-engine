"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type Role } from "@/lib/api";
import { saveSelectedRole } from "@/lib/session";
import {
  Search, ArrowRight, Cpu, BarChart2, Zap, Cog, Building2,
  TrendingUp, FlaskConical, Landmark, Layers, ChevronRight,
} from "lucide-react";

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

const SECTOR_COLORS: Record<string, string> = {
  "IT":                      "bg-blue-50 text-blue-700 border-blue-200",
  "Analytics":               "bg-violet-50 text-violet-700 border-violet-200",
  "Electrical":              "bg-yellow-50 text-yellow-700 border-yellow-200",
  "Electronics":             "bg-orange-50 text-orange-700 border-orange-200",
  "Mechanical":              "bg-slate-50 text-slate-700 border-slate-200",
  "Civil":                   "bg-amber-50 text-amber-700 border-amber-200",
  "Government / Statistics": "bg-teal-50 text-teal-700 border-teal-200",
  "Management":              "bg-pink-50 text-pink-700 border-pink-200",
};

const CATEGORY_TABS = ["All", "IT & Software", "Data & Analytics", "Core Engineering", "Government", "Management"];

const SECTOR_TO_CATEGORY: Record<string, string> = {
  "IT": "IT & Software",
  "Analytics": "Data & Analytics",
  "Electrical": "Core Engineering",
  "Electronics": "Core Engineering",
  "Mechanical": "Core Engineering",
  "Civil": "Core Engineering",
  "Government / Statistics": "Government",
  "Management": "Management",
};

export default function TargetRolePage() {
  const router = useRouter();
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");
  const [selected, setSelected] = useState<Role | null>(null);

  useEffect(() => {
    api.roles.list().then(setRoles).catch(console.error).finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    return roles.filter(r => {
      const matchSearch = r.name.toLowerCase().includes(search.toLowerCase()) ||
        (r.description ?? "").toLowerCase().includes(search.toLowerCase()) ||
        r.sector.toLowerCase().includes(search.toLowerCase());
      const cat = SECTOR_TO_CATEGORY[r.sector] ?? "IT & Software";
      const matchCat = activeCategory === "All" || cat === activeCategory;
      return matchSearch && matchCat;
    });
  }, [roles, search, activeCategory]);

  function handleSelect(role: Role) {
    setSelected(role);
    saveSelectedRole(role.id, role.name);
  }

  function goToAnalysis() {
    if (selected) router.push("/analysis");
  }

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-slate-900">What role are you preparing for?</h1>
          <p className="text-sm text-slate-500 mt-1">Explore roles across domains. We will map your gaps to the selected role.</p>
        </div>

        {/* Search */}
        <div className="relative mb-5">
          <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search roles, e.g. Data Analyst, SDE, Statistical Officer..."
            className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 shadow-sm"
          />
        </div>

        {/* Category tabs */}
        <div className="flex gap-2 overflow-x-auto pb-1 mb-6 scrollbar-none">
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
              const colorClass = SECTOR_COLORS[role.sector] ?? "bg-slate-50 text-slate-700 border-slate-200";
              const isSelected = selected?.id === role.id;

              return (
                <button
                  key={role.id}
                  onClick={() => handleSelect(role)}
                  className={`relative text-left p-5 rounded-2xl border-2 transition-all group ${
                    isSelected
                      ? "border-indigo-500 bg-indigo-50 shadow-md shadow-indigo-100"
                      : "border-slate-200 bg-white hover:border-indigo-300 hover:shadow-sm"
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center border shrink-0 ${colorClass}`}>
                      <Icon size={18} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-slate-800 leading-snug">{role.name}</p>
                      <span className={`inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full border mt-1 ${colorClass}`}>
                        {role.sector}
                      </span>
                      {role.description && (
                        <p className="text-xs text-slate-500 mt-1.5 line-clamp-2 leading-relaxed">{role.description}</p>
                      )}
                    </div>
                    <ChevronRight
                      size={16}
                      className={`shrink-0 mt-0.5 transition-colors ${isSelected ? "text-indigo-500" : "text-slate-300 group-hover:text-slate-400"}`}
                    />
                  </div>

                  {isSelected && (
                    <div className="absolute top-3 right-3 w-4 h-4 rounded-full bg-indigo-600 flex items-center justify-center">
                      <svg width="8" height="6" viewBox="0 0 8 6" fill="none">
                        <path d="M1 3l2 2 4-4" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </div>
                  )}
                </button>
              );
            })}
            {filtered.length === 0 && (
              <div className="col-span-2 text-center py-12 text-slate-400 text-sm">
                No roles match your search.
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
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-all shrink-0"
            >
              View My Competency Analysis
              <ArrowRight size={14} />
            </button>
          </div>
        )}
      </div>
    </AppShell>
  );
}
