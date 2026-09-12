"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import {
  User,
  Target,
  BarChart2,
  BookOpen,
  Map,
  ClipboardCheck,
  FileSearch,
  LogOut,
  Leaf,
  Menu,
  X,
} from "lucide-react";
import { getSession, clearSession, type SessionUser } from "@/lib/session";
import SkilloraChat from "@/components/SkilloraChat";

const NAV = [
  { label: "Profile",       href: "/profile",    icon: User },
  { label: "Target Role",   href: "/role",        icon: Target },
  { label: "Analysis",      href: "/analysis",    icon: BarChart2 },
  { label: "Courses",       href: "/courses",     icon: BookOpen },
  { label: "Learning Path", href: "/learning",    icon: Map },
  { label: "Assessment",    href: "/assessment",  icon: ClipboardCheck },
  { label: "ATS Checker",   href: "/ats",         icon: FileSearch },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<SessionUser | null>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const s = getSession();
    if (!s) { router.replace("/"); return; }
    setUser(s);
  }, [router]);

  function handleSignOut() {
    clearSession();
    router.replace("/");
  }

  const initials = user?.name
    ? user.name.split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase()
    : "?";

  return (
    <div className="flex h-screen overflow-hidden bg-[#f8fafc]">
      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-30
          flex flex-col w-60 shrink-0
          bg-[#0f1117] text-white
          transition-transform duration-200
          ${open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
        `}
      >
        {/* Logo */}
        <div className="flex items-center gap-2.5 px-5 py-5 border-b border-[#1e2130]">
          <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center shrink-0">
            <Leaf size={16} className="text-white" />
          </div>
          <div>
            <p className="text-sm font-bold text-white leading-none">SkillGap Engine</p>
            <p className="text-[10px] text-slate-400 mt-0.5 leading-none">From skills to opportunity</p>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto sidebar-scroll">
          {NAV.map(({ label, href, icon: Icon }) => {
            const active = pathname === href || pathname.startsWith(href + "/");
            return (
              <Link
                key={href}
                href={href}
                onClick={() => setOpen(false)}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all
                  ${active
                    ? "bg-indigo-600 text-white"
                    : "text-slate-400 hover:bg-[#1e2130] hover:text-white"}
                `}
              >
                <Icon size={16} />
                {label}
              </Link>
            );
          })}
        </nav>

        {/* User + sign out */}
        <div className="px-3 py-4 border-t border-[#1e2130]">
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-[#1e2130] mb-2">
            <div className="w-7 h-7 rounded-full bg-indigo-500 flex items-center justify-center text-xs font-bold text-white shrink-0">
              {initials}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-white truncate">{user?.name ?? "..."}</p>
              <p className="text-[10px] text-slate-400 truncate">{user?.education ?? "Set up your profile"}</p>
            </div>
          </div>
          <button
            onClick={handleSignOut}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-xs text-slate-400 hover:text-red-400 hover:bg-[#1e2130] transition-all"
          >
            <LogOut size={13} />
            Sign out
          </button>
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Mobile topbar */}
        <div className="lg:hidden flex items-center gap-3 px-4 py-3 bg-[#0f1117] border-b border-[#1e2130]">
          <button onClick={() => setOpen(true)} className="text-slate-400 hover:text-white">
            <Menu size={20} />
          </button>
          <span className="text-sm font-bold text-white">SkillGap Engine</span>
        </div>

        <main className="flex-1 overflow-y-auto flex flex-col custom-scrollbar">
          {children}
        </main>
      </div>

      {/* Skillora AI Assistant — floats over all pages */}
      <SkilloraChat />
    </div>
  );
}
