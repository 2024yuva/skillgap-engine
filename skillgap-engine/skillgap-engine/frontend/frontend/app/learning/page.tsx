"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, type CourseRecommendation } from "@/lib/api";
import { getSession, getSelectedRole } from "@/lib/session";
import { Map, ArrowRight, Clock, ChevronRight } from "lucide-react";

export default function LearningPathPage() {
  const router = useRouter();
  const [recs, setRecs] = useState<CourseRecommendation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const session = getSession();
    const role = getSelectedRole();
    if (!session) { router.replace("/"); return; }
    if (!role) { router.replace("/role"); return; }
    api.analysis.recommendations(session.id, role.id, 8)
      .then(r => setRecs(r.recommendations))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  const role = typeof window !== "undefined" ? getSelectedRole() : null;

  return (
    <AppShell>
      <div className="max-w-3xl mx-auto px-6 py-8">
        <div className="mb-7">
          <h1 className="text-2xl font-bold text-slate-900">Your Learning Path</h1>
          <p className="text-sm text-slate-500 mt-1">
            A recommended sequence to achieve your goal{role ? ` of ${role.name}` : ""}.
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center min-h-48">
            <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
          </div>
        ) : recs.length === 0 ? (
          <div className="text-center py-16 text-slate-400 text-sm">
            <Map size={32} className="mx-auto mb-3 opacity-30" />
            No learning path data yet. Complete your profile and select a role first.
          </div>
        ) : (
          <div className="relative">
            {/* Vertical connector */}
            <div className="absolute left-5 top-10 bottom-10 w-0.5 bg-slate-200" />

            <div className="space-y-4">
              {recs.map((rec, i) => (
                <div key={rec.course.id} className="flex gap-4 items-start">
                  {/* Step number */}
                  <div className="w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center text-sm font-bold shrink-0 relative z-10">
                    {i + 1}
                  </div>

                  <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                    <p className="text-sm font-bold text-slate-800">{rec.course.title}</p>
                    <p className="text-xs text-slate-500 mt-1">{rec.course.description}</p>
                    <div className="flex items-center gap-3 mt-2 text-xs text-slate-400">
                      {rec.course.duration && (
                        <span className="flex items-center gap-1">
                          <Clock size={11} /> {rec.course.duration}
                        </span>
                      )}
                      {rec.course.provider && <span>{rec.course.provider}</span>}
                    </div>
                    {rec.gaps_addressed.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {rec.gaps_addressed.slice(0, 3).map(g => (
                          <span key={g} className="text-[10px] bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded-full">
                            {g}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Final goal */}
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 rounded-full bg-emerald-500 text-white flex items-center justify-center shrink-0 relative z-10">
                  <svg width="16" height="12" viewBox="0 0 16 12" fill="none">
                    <path d="M1 6l4 4L15 1" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <div className="flex-1 bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
                  <p className="text-sm font-bold text-emerald-800">Target Role Readiness</p>
                  <p className="text-xs text-emerald-600 mt-0.5">Continue learning to bridge remaining gaps.</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
