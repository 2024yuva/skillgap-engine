"use client";

export default function ReadinessGauge({
  score,
  coveredCount,
  gapCount,
}: {
  score: number;
  coveredCount: number;
  gapCount: number;
}) {
  const pct = Math.round(score * 100);
  const circumference = 2 * Math.PI * 54;
  const strokeDashoffset = circumference * (1 - score);

  const color =
    pct >= 70 ? "#10b981"   // emerald
    : pct >= 40 ? "#f59e0b" // amber
    : "#ef4444";             // red

  const label =
    pct >= 70 ? "High"
    : pct >= 40 ? "Medium"
    : "Low";

  return (
    <div className="flex flex-col items-center gap-3">
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Readiness Score</p>
      <div className="relative w-32 h-32">
        <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
          {/* Track */}
          <circle
            cx="60" cy="60" r="54"
            fill="none"
            stroke="#f1f5f9"
            strokeWidth="12"
          />
          {/* Progress */}
          <circle
            cx="60" cy="60" r="54"
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            style={{ transition: "stroke-dashoffset 0.6s ease" }}
          />
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-extrabold text-slate-800">{pct}%</span>
          <span className="text-[10px] font-semibold uppercase tracking-wide" style={{ color }}>
            {label}
          </span>
        </div>
      </div>

      {/* Stats */}
      <div className="flex gap-4 text-center">
        <div>
          <p className="text-lg font-bold text-emerald-600">{coveredCount}</p>
          <p className="text-[10px] text-slate-400">Met</p>
        </div>
        <div className="w-px bg-slate-200" />
        <div>
          <p className="text-lg font-bold text-red-500">{gapCount}</p>
          <p className="text-[10px] text-slate-400">Gaps</p>
        </div>
      </div>
    </div>
  );
}
