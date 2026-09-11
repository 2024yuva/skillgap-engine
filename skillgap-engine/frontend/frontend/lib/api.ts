/**
 * Typed API client for SkillGap Engine backend.
 */

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`POST ${path} failed: ${res.status} ${text}`);
  }
  return res.json();
}

async function put<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`PUT ${path} failed: ${res.status}`);
  return res.json();
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface UserProfile {
  id: number;
  name: string;
  education: string | null;
  department: string | null;
  experience: number | null;
}

export interface UserCreate {
  name: string;
  education?: string;
  department?: string;
  experience?: number;
}

export interface Role {
  id: number;
  name: string;
  description: string | null;
  sector: string;
}

export interface Competency {
  id: number;
  name: string;
  description: string | null;
  category: string;
  parent_id: number | null;
  taxonomy_source: string | null;
  taxonomy_id: string | null;
}

export interface CompetencyGap {
  competency_id: number;
  competency_name: string;
  category: string;
  current_level: number;
  required_level: number;
  gap: number;
  importance: number;
  priority_score: number;
  evidence_source: string | null;
}

export interface GapAnalysisResult {
  user_id: number;
  role_id: number;
  role_name: string;
  user_name: string;
  gaps: CompetencyGap[];
  covered_count: number;
  gap_count: number;
  readiness_score: number;
}

export interface Course {
  id: number;
  title: string;
  description: string | null;
  provider: string | null;
  duration: string | null;
  level: string | null;
  source: string | null;
  source_url: string | null;
}

export interface CourseRecommendation {
  course: Course;
  impact_score: number;
  gaps_addressed: string[];
  gaps_addressed_count: number;
  explanation: string;
}

export interface CourseRecommendationResult {
  user_id: number;
  role_id: number;
  recommendations: CourseRecommendation[];
}

export interface UserCompetency {
  competency_id: number;
  current_level: number;
  evidence_source: string | null;
  last_demonstrated: string | null;
  competency: Competency;
}

export interface ParsedResumeProfile {
  name: string | null;
  education: string;
  experience_summary: string;
  technical_skills: string[];
  soft_skills: string[];
  projects: string[];
  courses_certifications: string[];
  matched_competency_ids: number[];
  inferred_levels: Record<string, number>;
}

// ---------------------------------------------------------------------------
// API calls
// ---------------------------------------------------------------------------

export const api = {
  users: {
    list: () => get<UserProfile[]>("/users/"),
    get: (id: number) => get<UserProfile>(`/users/${id}`),
    create: (body: UserCreate) => post<UserProfile>("/users/", body),
    update: (id: number, body: UserCreate) => put<UserProfile>(`/users/${id}`, body),
    competencies: (id: number) => get<UserCompetency[]>(`/users/${id}/competencies`),
  },
  roles: {
    list: () => get<Role[]>("/roles/"),
    get: (id: number) => get<Role>(`/roles/${id}`),
  },
  competencies: {
    list: () => get<Competency[]>("/competencies/"),
  },
  analysis: {
    gaps: (userId: number, roleId: number) =>
      get<GapAnalysisResult>(`/analysis/gap?user_id=${userId}&role_id=${roleId}`),
    recommendations: (userId: number, roleId: number, topN = 8) =>
      get<CourseRecommendationResult>(
        `/analysis/recommendations?user_id=${userId}&role_id=${roleId}&top_n=${topN}`
      ),
  },
  resume: {
    parse: async (file: File): Promise<ParsedResumeProfile> => {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`${BASE}/resume/parse`, { method: "POST", body: form });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Resume parse failed: ${res.status} ${text}`);
      }
      return res.json();
    },
    apply: (userId: number, body: { inferred_levels: Record<number, number>; name?: string; education?: string }) =>
      post<{ applied: number; user_id: number }>(`/resume/apply/${userId}`, body),
  },
};
