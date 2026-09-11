/**
 * Lightweight client-side session store using localStorage.
 * No authentication needed for hackathon — just persists userId and name.
 */

export interface SessionUser {
  id: number;
  name: string;
  education?: string;
  department?: string;
}

const KEY = "sge_session";

export function getSession(): SessionUser | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as SessionUser) : null;
  } catch {
    return null;
  }
}

export function setSession(user: SessionUser): void {
  localStorage.setItem(KEY, JSON.stringify(user));
}

export function clearSession(): void {
  localStorage.removeItem(KEY);
  localStorage.removeItem("sge_role_id");
  localStorage.removeItem("sge_role_name");
}

export function saveSelectedRole(roleId: number, roleName: string): void {
  localStorage.setItem("sge_role_id", String(roleId));
  localStorage.setItem("sge_role_name", roleName);
}

export function getSelectedRole(): { id: number; name: string } | null {
  const id = localStorage.getItem("sge_role_id");
  const name = localStorage.getItem("sge_role_name");
  if (!id || !name) return null;
  return { id: Number(id), name };
}
