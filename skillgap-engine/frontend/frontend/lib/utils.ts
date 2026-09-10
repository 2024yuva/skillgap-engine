/** Competency level labels (0-5 scale). */
export const LEVEL_LABELS: Record<number, string> = {
  0: "No Evidence",
  1: "Awareness",
  2: "Basic",
  3: "Intermediate",
  4: "Advanced",
  5: "Expert",
};

/** Tailwind colour classes for gap severity. */
export function gapColor(gap: number): string {
  if (gap === 0) return "text-emerald-600";
  if (gap <= 1) return "text-yellow-500";
  if (gap <= 2) return "text-orange-500";
  return "text-red-600";
}

export function gapBg(gap: number): string {
  if (gap === 0) return "bg-emerald-50 border-emerald-200";
  if (gap <= 1) return "bg-yellow-50 border-yellow-200";
  if (gap <= 2) return "bg-orange-50 border-orange-200";
  return "bg-red-50 border-red-200";
}

export function priorityBadgeColor(score: number): string {
  if (score >= 0.5) return "bg-red-100 text-red-700";
  if (score >= 0.3) return "bg-orange-100 text-orange-700";
  if (score >= 0.1) return "bg-yellow-100 text-yellow-700";
  return "bg-emerald-100 text-emerald-700";
}

export function levelBarColor(level: number): string {
  const colours = [
    "#e5e7eb", // 0 - grey
    "#fbbf24", // 1 - amber
    "#f97316", // 2 - orange
    "#3b82f6", // 3 - blue
    "#8b5cf6", // 4 - violet
    "#10b981", // 5 - emerald
  ];
  return colours[Math.min(level, 5)] ?? "#e5e7eb";
}

export function impactBadge(score: number): string {
  if (score >= 1.0) return "High Impact";
  if (score >= 0.5) return "Medium Impact";
  return "Low Impact";
}

export function impactBadgeColor(score: number): string {
  if (score >= 1.0) return "bg-violet-100 text-violet-700";
  if (score >= 0.5) return "bg-blue-100 text-blue-700";
  return "bg-slate-100 text-slate-600";
}
