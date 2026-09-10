"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import { api, type UserProfile, type Role } from "@/lib/api";

export default function ProfilePage() {
  const router = useRouter();

  const [users, setUsers] = useState<UserProfile[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | "">("");
  const [selectedRoleId, setSelectedRoleId] = useState<number | "">("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form for creating a new user
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", education: "", department: "", experience: "" });
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    Promise.all([api.users.list(), api.roles.list()])
      .then(([u, r]) => {
        setUsers(u);
        setRoles(r);
        if (u.length > 0) setSelectedUserId(u[0].id);
        if (r.length > 0) setSelectedRoleId(r[0].id);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const selectedUser = users.find((u) => u.id === selectedUserId);
  const selectedRole = roles.find((r) => r.id === selectedRoleId);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    try {
      const user = await api.users.create({
        name: form.name,
        education: form.education || undefined,
        department: form.department || undefined,
        experience: form.experience ? Number(form.experience) : undefined,
      });
      setUsers((prev) => [...prev, user]);
      setSelectedUserId(user.id);
      setShowForm(false);
      setForm({ name: "", education: "", department: "", experience: "" });
    } catch (e: unknown) {
      if (e instanceof Error) setError(e.message);
    } finally {
      setCreating(false);
    }
  }

  function goToDashboard() {
    if (selectedUserId && selectedRoleId) {
      router.push(`/dashboard?user=${selectedUserId}&role=${selectedRoleId}`);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <main className="max-w-3xl mx-auto px-6 py-10">
        <h1 className="text-2xl font-bold text-slate-800 mb-1">
          Select Profile &amp; Target Role
        </h1>
        <p className="text-sm text-slate-500 mb-8">
          Choose an existing profile or create a new one, then pick the role you want to
          transition into.
        </p>

        {loading && (
          <div className="flex items-center gap-2 text-slate-500 text-sm">
            <span className="animate-spin">⟳</span> Loading data…
          </div>
        )}

        {error && (
          <div className="rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm p-4 mb-6">
            <strong>Could not connect to backend:</strong> {error}
            <p className="mt-1 text-xs text-red-500">
              Make sure the FastAPI server is running on{" "}
              <code>http://localhost:8000</code>
            </p>
          </div>
        )}

        {!loading && !error && (
          <div className="space-y-6">
            {/* User selector */}
            <div className="rounded-xl bg-white border border-slate-200 p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide">
                  Your Profile
                </h2>
                <button
                  onClick={() => setShowForm(!showForm)}
                  className="text-xs text-violet-600 hover:text-violet-800 font-medium"
                >
                  {showForm ? "Cancel" : "+ New profile"}
                </button>
              </div>

              {/* Existing user tiles */}
              <div className="grid grid-cols-2 gap-3 mb-4 sm:grid-cols-3">
                {users.map((u) => (
                  <button
                    key={u.id}
                    onClick={() => setSelectedUserId(u.id)}
                    className={`rounded-lg border p-3 text-left transition-all ${
                      selectedUserId === u.id
                        ? "border-violet-500 bg-violet-50 shadow-sm"
                        : "border-slate-200 hover:border-slate-300 bg-white"
                    }`}
                  >
                    <p className="text-sm font-semibold text-slate-800 truncate">{u.name}</p>
                    <p className="text-xs text-slate-500 truncate">{u.education ?? "—"}</p>
                    <p className="text-xs text-slate-400 truncate">{u.department ?? "—"}</p>
                    {u.experience !== null && (
                      <p className="text-xs text-slate-400">{u.experience}y exp</p>
                    )}
                  </button>
                ))}
              </div>

              {/* New user form */}
              {showForm && (
                <form onSubmit={handleCreate} className="border-t border-slate-100 pt-4 space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs text-slate-600 font-medium">Name *</label>
                      <input
                        required
                        value={form.name}
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                        className="mt-1 w-full rounded border border-slate-200 text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
                        placeholder="e.g. Anita Sharma"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-600 font-medium">Education</label>
                      <input
                        value={form.education}
                        onChange={(e) => setForm({ ...form, education: e.target.value })}
                        className="mt-1 w-full rounded border border-slate-200 text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
                        placeholder="e.g. B.Tech CSE"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-600 font-medium">Department</label>
                      <input
                        value={form.department}
                        onChange={(e) => setForm({ ...form, department: e.target.value })}
                        className="mt-1 w-full rounded border border-slate-200 text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
                        placeholder="e.g. Mechanical Engineering"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-slate-600 font-medium">Experience (years)</label>
                      <input
                        type="number"
                        min={0}
                        value={form.experience}
                        onChange={(e) => setForm({ ...form, experience: e.target.value })}
                        className="mt-1 w-full rounded border border-slate-200 text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
                        placeholder="0"
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    disabled={creating}
                    className="text-sm bg-violet-600 hover:bg-violet-700 text-white rounded px-4 py-2 font-medium disabled:opacity-50"
                  >
                    {creating ? "Creating…" : "Create Profile"}
                  </button>
                </form>
              )}
            </div>

            {/* Role selector */}
            <div className="rounded-xl bg-white border border-slate-200 p-6 shadow-sm">
              <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide mb-4">
                Target Role
              </h2>
              <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                {roles.map((r) => (
                  <button
                    key={r.id}
                    onClick={() => setSelectedRoleId(r.id)}
                    className={`rounded-lg border p-3 text-left transition-all ${
                      selectedRoleId === r.id
                        ? "border-violet-500 bg-violet-50 shadow-sm"
                        : "border-slate-200 hover:border-slate-300 bg-white"
                    }`}
                  >
                    <p className="text-sm font-semibold text-slate-800">{r.name}</p>
                    <p className="text-xs text-slate-500">{r.sector}</p>
                    {r.description && (
                      <p className="text-xs text-slate-400 mt-1 line-clamp-2">{r.description}</p>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Summary + CTA */}
            {selectedUser && selectedRole && (
              <div className="rounded-xl bg-violet-50 border border-violet-200 p-5 flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold text-violet-800">
                    {selectedUser.name}
                  </p>
                  <p className="text-xs text-violet-600">
                    {selectedUser.education} • {selectedUser.department}
                  </p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Targeting: <strong>{selectedRole.name}</strong>{" "}
                    <span className="text-slate-400">({selectedRole.sector})</span>
                  </p>
                </div>
                <button
                  onClick={goToDashboard}
                  className="ml-4 shrink-0 bg-violet-600 hover:bg-violet-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors"
                >
                  Analyse Gaps →
                </button>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
