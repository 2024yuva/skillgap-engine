"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { label: "Profile", href: "/" },
  { label: "Dashboard", href: "/dashboard" },
];

export default function Navbar() {
  const path = usePathname();

  return (
    <nav className="bg-white border-b border-slate-200 px-6 py-3 flex items-center gap-8 shadow-sm">
      <Link href="/" className="flex items-center gap-2 mr-4">
        <span className="text-xl font-bold text-violet-700">SkillGap</span>
        <span className="text-xl font-semibold text-slate-700">Engine</span>
      </Link>
      {NAV.map((n) => (
        <Link
          key={n.href}
          href={n.href}
          className={`text-sm font-medium transition-colors ${
            path === n.href
              ? "text-violet-700 border-b-2 border-violet-700 pb-0.5"
              : "text-slate-600 hover:text-violet-700"
          }`}
        >
          {n.label}
        </Link>
      ))}
      <span className="ml-auto text-xs text-slate-400 bg-slate-100 px-2 py-1 rounded">
        Smart India Hackathon — MoSPI Track
      </span>
    </nav>
  );
}
