"use client";

import AppShell from "@/components/AppShell";
import { ClipboardCheck, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

export default function AssessmentPage() {
  const router = useRouter();

  return (
    <AppShell>
      <div className="max-w-2xl mx-auto px-6 py-16 text-center">
        <div className="w-16 h-16 rounded-2xl bg-indigo-50 border border-indigo-200 flex items-center justify-center mx-auto mb-5">
          <ClipboardCheck size={28} className="text-indigo-600" />
        </div>
        <h1 className="text-2xl font-bold text-slate-900 mb-2">AI-Generated Assessment</h1>
        <p className="text-slate-500 text-sm leading-relaxed mb-8">
          Take a short competency quiz to validate and update your skill profile. 
          This feature will be available in the next milestone.
        </p>

        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 text-left space-y-4 mb-8">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-wide">Coming in next milestone</p>
          {[
            "Questions generated from your gap competencies",
            "Adaptive difficulty based on your current level",
            "Automatic profile update on completion",
            "Track improvement over time",
          ].map(f => (
            <div key={f} className="flex items-center gap-3 text-sm text-slate-600">
              <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 shrink-0" />
              {f}
            </div>
          ))}
        </div>

        <button
          onClick={() => router.push("/analysis")}
          className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl text-sm font-semibold transition-all"
        >
          Back to Analysis
          <ArrowRight size={14} />
        </button>
      </div>
    </AppShell>
  );
}
