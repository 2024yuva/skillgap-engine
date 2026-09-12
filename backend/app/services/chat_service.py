"""
Skillora AI Assistant — chat service.

Collects live user context (profile, skills, gap analysis, job matches,
salary records) from the DB and calls the Groq API to produce a
conversational, career-focused response.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

LEVEL_LABELS = ["No Evidence", "Awareness", "Basic", "Intermediate", "Advanced", "Expert"]


# ---------------------------------------------------------------------------
# Groq helper
# ---------------------------------------------------------------------------

def _call_groq(messages: List[Dict[str, str]], model: str = PRIMARY_MODEL) -> str:
    if not GROQ_API_KEY:
        return _offline_reply()

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 1200,
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Skillora-Chatbot/1.0",
    }
    req = urllib.request.Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        if model != FALLBACK_MODEL and e.code in (429, 500, 503):
            return _call_groq(messages, model=FALLBACK_MODEL)
        return _offline_reply()
    except Exception:
        if model != FALLBACK_MODEL:
            return _call_groq(messages, model=FALLBACK_MODEL)
        return _offline_reply()


def _offline_reply() -> str:
    return (
        "I'm having trouble reaching the AI service right now. "
        "Please check that your GROQ_API_KEY is set in the backend .env file, "
        "or try again in a moment."
    )


# ---------------------------------------------------------------------------
# Context builder — pulls live data from DB
# ---------------------------------------------------------------------------

def _build_user_context(user_id: int, db: Session) -> Dict[str, Any]:
    """Gather everything the AI needs to give personalised answers."""
    from app.models.models import (
        User, UserCompetency, Competency, Role, RoleCompetency,
        SkillCareerRecord,
    )
    from app.services.gap_service import get_role_matches, get_company_job_matches

    ctx: Dict[str, Any] = {}

    # ── User profile ──────────────────────────────────────────────────────
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return ctx
    ctx["user"] = {
        "id": user.id,
        "name": user.name,
        "education": user.education or "Not provided",
        "department": user.department or "Not specified",
        "experience_years": user.experience,
    }

    # ── User competencies ─────────────────────────────────────────────────
    user_comps = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == user_id)
        .all()
    )
    skill_lines = []
    for uc in user_comps:
        comp = db.query(Competency).filter(Competency.id == uc.competency_id).first()
        if comp:
            label = LEVEL_LABELS[min(uc.current_level, 5)]
            skill_lines.append(f"  - {comp.name} ({comp.category}): Level {uc.current_level}/5 [{label}]")
    ctx["skills"] = skill_lines

    # ── Role matches (top 5) ──────────────────────────────────────────────
    try:
        role_matches = get_role_matches(user_id, db)[:5]
        ctx["top_role_matches"] = [
            {
                "role": r["name"],
                "match_score": r["match_score"],
                "matched_skills": r["matched_skills"][:5],
                "missing_skills": r["missing_skills"][:5],
                "sector": r["sector"],
            }
            for r in role_matches
        ]
    except Exception:
        ctx["top_role_matches"] = []

    # ── Company job matches (top 5) ───────────────────────────────────────
    try:
        company_matches = get_company_job_matches(user_id, db)[:5]
        ctx["top_job_matches"] = [
            {
                "company": j["company_name"],
                "about": j["about_role"],
                "match_score": j["match_score"],
                "matched_skills": j["matched_skills"][:4],
                "missing_skills": j["missing_skills"][:4],
                "salary": j["salary_lpa"],
                "duration": j["working_duration"],
            }
            for j in company_matches
        ]
    except Exception:
        ctx["top_job_matches"] = []

    # ── Salary records for user's top skills (up to 6) ───────────────────
    try:
        top_skill_names = []
        for uc in sorted(user_comps, key=lambda x: x.current_level, reverse=True)[:6]:
            comp = db.query(Competency).filter(Competency.id == uc.competency_id).first()
            if comp:
                top_skill_names.append(comp.name)

        salary_data = []
        for skill_name in top_skill_names[:4]:
            records = (
                db.query(SkillCareerRecord)
                .filter(SkillCareerRecord.skill_name.ilike(f"%{skill_name}%"))
                .limit(2)
                .all()
            )
            for rec in records:
                if rec.salary_min_lpa and rec.salary_max_lpa:
                    salary_data.append({
                        "skill": rec.skill_name,
                        "role": rec.suitable_job_role,
                        "salary": f"₹{rec.salary_min_lpa}–{rec.salary_max_lpa} LPA",
                        "demand": rec.job_demand,
                        "growth": rec.career_growth,
                        "experience": rec.experience_range,
                    })
        ctx["salary_insights"] = salary_data[:6]
    except Exception:
        ctx["salary_insights"] = []

    return ctx


def _context_to_system_prompt(ctx: Dict[str, Any]) -> str:
    """Convert collected context into a rich system prompt for Groq."""
    lines = [
        "You are Skillora AI Assistant — an expert career guide embedded in the Skillora platform.",
        "You help users with career guidance, resume improvement, skill-gap analysis, job recommendations, salary insights, and personalized learning paths.",
        "Always be encouraging, concise, and actionable. Use bullet points and bold text (markdown) for clarity.",
        "Never make up data — use only the context provided below.",
        "",
        "=== USER PROFILE ===",
    ]

    if not ctx:
        lines.append("No user profile found. Ask the user to set up their profile first.")
        return "\n".join(lines)

    user = ctx.get("user", {})
    lines.append(f"Name: {user.get('name', 'Unknown')}")
    lines.append(f"Education: {user.get('education', 'Not provided')}")
    lines.append(f"Department: {user.get('department', 'Not specified')}")
    if user.get("experience_years"):
        lines.append(f"Experience: {user['experience_years']} year(s)")

    skills = ctx.get("skills", [])
    if skills:
        lines.append("")
        lines.append("=== CURRENT SKILLS & COMPETENCY LEVELS (0–5 scale) ===")
        lines.extend(skills)
    else:
        lines.append("\nNo skills recorded yet — advise them to upload their resume or complete an assessment.")

    top_roles = ctx.get("top_role_matches", [])
    if top_roles:
        lines.append("")
        lines.append("=== TOP MATCHING ROLES ===")
        for r in top_roles:
            lines.append(
                f"  • {r['role']} ({r['sector']}) — {r['match_score']}% match | "
                f"Has: {', '.join(r['matched_skills'][:3]) or 'none'} | "
                f"Missing: {', '.join(r['missing_skills'][:3]) or 'none'}"
            )

    top_jobs = ctx.get("top_job_matches", [])
    if top_jobs:
        lines.append("")
        lines.append("=== TOP COMPANY JOB MATCHES ===")
        for j in top_jobs:
            lines.append(
                f"  • {j['company']} — {j['match_score']}% match | Salary: {j['salary']} | "
                f"Duration: {j['duration']}"
            )
            if j["missing_skills"]:
                lines.append(f"    Skills to improve: {', '.join(j['missing_skills'][:3])}")

    salary_data = ctx.get("salary_insights", [])
    if salary_data:
        lines.append("")
        lines.append("=== SALARY INSIGHTS FOR USER'S SKILLS ===")
        for s in salary_data:
            lines.append(
                f"  • {s['skill']} → {s['role']}: {s['salary']} | "
                f"Demand: {s.get('demand', 'N/A')} | Growth: {s.get('growth', 'N/A')}"
            )

    lines.append("")
    lines.append(
        "When asked about skill gaps, use the competency levels above. "
        "gap = required_level − current_level (0–5 scale). "
        "When asked about jobs or salaries, refer to the data above. "
        "When asked about a learning path, suggest a step-by-step sequence based on missing skills. "
        "Keep responses under 400 words unless the user asks for detail."
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def get_chat_response(
    user_id: Optional[int],
    message: str,
    history: List[Dict[str, str]],
    page_context: str,
    db: Session,
) -> str:
    """
    Main function called by the API route.

    :param user_id:      Skillora user ID (None = unauthenticated)
    :param message:      Latest user message
    :param history:      Previous turns [{"role": "user"|"assistant", "content": "..."}]
    :param page_context: Current page name, e.g. "profile", "analysis"
    :param db:           SQLAlchemy session
    :returns:            AI reply string (markdown)
    """
    # Collect live context
    ctx = _build_user_context(user_id, db) if user_id else {}

    system_prompt = _context_to_system_prompt(ctx)
    if page_context:
        system_prompt += f"\n\nThe user is currently on the '{page_context}' page."

    # Build message list for Groq
    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    # Include last 6 turns of history to keep context window manageable
    for turn in history[-6:]:
        role = turn.get("role", "user")
        content = turn.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})

    return _call_groq(messages)
