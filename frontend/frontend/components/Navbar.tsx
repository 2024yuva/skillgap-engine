"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
      <Link href="/" className="text-sm font-bold text-slate-800 hover:text-violet-700 transition-colors">
        SkillGap Engine
      </Link>
      <nav className="flex items-center gap-4 text-xs font-medium text-slate-500">
        <Link href="/" className="hover:text-slate-800 transition-colors">Profiles</Link>
        <Link href="/dashboard" className="hover:text-slate-800 transition-colors">Dashboard</Link>
      </nav>
    </header>
  );
}
