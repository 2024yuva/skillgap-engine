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
        # Instead of just error, this will trigger the offline response
        raise Exception("No API key configured")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,  # More creative/casual
        "max_tokens": 800,   # Shorter responses
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Skillora-Chatbot/1.0",
    }
    
    try:
        req = urllib.request.Request(
            GROQ_API_URL,
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"].strip()
            
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise Exception(f"API authentication failed: {e.code}")
        elif e.code == 429:
            if model != FALLBACK_MODEL:
                return _call_groq(messages, model=FALLBACK_MODEL)
            raise Exception(f"Rate limit exceeded: {e.code}")
        elif e.code >= 500:
            if model != FALLBACK_MODEL:
                return _call_groq(messages, model=FALLBACK_MODEL)
            raise Exception(f"API server error: {e.code}")
        else:
            raise Exception(f"API error: {e.code}")
            
    except Exception as e:
        if model != FALLBACK_MODEL:
            return _call_groq(messages, model=FALLBACK_MODEL)
        raise Exception(f"Connection error: {str(e)}")



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
        "You are Skillora AI — a friendly, casual career mentor who helps people grow their careers.",
        "Chat naturally like a supportive friend who happens to be a career expert.",
        "Be encouraging, practical, and specific. Use emojis occasionally. Keep responses conversational and under 300 words.",
        "Always analyze their actual data to give personalized advice — never give generic tips.",
        "",
        "=== USER PROFILE ===",
    ]

    if not ctx:
        lines.extend([
            "No profile found yet.",
            "",
            "INSTRUCTIONS: Tell them to set up their profile first by uploading their resume or adding skills manually. Be friendly about it!"
        ])
        return "\n".join(lines)

    user = ctx.get("user", {})
    lines.append(f"👤 {user.get('name', 'User')}")
    lines.append(f"🎓 {user.get('education', 'No education info')}")
    if user.get("experience_years"):
        lines.append(f"💼 {user['experience_years']} years experience")

    skills = ctx.get("skills", [])
    if skills:
        lines.append("")
        lines.append("=== THEIR CURRENT SKILLS ===")
        lines.extend(skills[:10])  # Top 10 skills
    else:
        lines.append("\n🚨 NO SKILLS RECORDED — suggest they upload resume or take assessments")

    top_roles = ctx.get("top_role_matches", [])
    if top_roles:
        lines.append("")
        lines.append("=== BEST MATCHING ROLES ===")
        for r in top_roles[:3]:  # Top 3 only
            lines.append(f"  • {r['role']} - {r['match_score']}% match")
            if r['missing_skills']:
                lines.append(f"    Missing: {', '.join(r['missing_skills'][:2])}")

    salary_data = ctx.get("salary_insights", [])
    if salary_data:
        lines.append("")
        lines.append("=== SALARY DATA FOR THEIR SKILLS ===")
        for s in salary_data[:3]:
            lines.append(f"  • {s['skill']} → {s['role']}: {s['salary']} (Growth: {s.get('growth', 'Unknown')})")

    lines.extend([
        "",
        "CHAT RULES:",
        "- Be conversational and supportive, like talking to a friend",
        "- Use their actual data above to give specific advice", 
        "- For skill gaps: required_level - current_level (0-5 scale)",
        "- Suggest practical next steps based on what they're missing",
        "- If they ask about learning paths, give a 3-4 step roadmap",
        "- Be encouraging about their strengths and honest about gaps",
        "- Keep responses under 250 words unless they ask for details"
    ])

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
    
    # Try AI first, but fall back to intelligent responses if API fails
    try:
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
        
    except Exception:
        # If API completely fails, provide intelligent offline responses
        return _get_offline_response(message, user_id, db, page_context)


def _get_offline_response(message: str, user_id: Optional[int], db: Session, page_context: str) -> str:
    """Provide helpful responses when AI API is unavailable."""
    msg_lower = message.lower()
    
    # Analyze user's actual data if available
    if user_id:
        try:
            ctx = _build_user_context(user_id, db)
            user_name = ctx.get("user", {}).get("name", "there")
            skills = ctx.get("skills", [])
            top_roles = ctx.get("top_role_matches", [])
            salary_data = ctx.get("salary_insights", [])
        except:
            user_name = "there"
            skills = []
            top_roles = []
            salary_data = []
    else:
        user_name = "there"
        skills = []
        top_roles = []
        salary_data = []

    # Career guidance responses based on message content
    if any(word in msg_lower for word in ["resume", "cv", "improve"]):
        if skills:
            return f"Hey {user_name}! 📄 Based on your profile, here are some **resume tips**:\n\n• **Highlight your strongest skills**: {', '.join([s.split(':')[0].strip('- ') for s in skills[:3]])}\n• **Use action verbs** like 'Developed', 'Built', 'Optimized'\n• **Add metrics** - quantify your achievements with numbers\n• **Tailor keywords** to match job descriptions\n\n*Want a detailed ATS analysis? Try uploading your resume to the ATS Checker!*"
        else:
            return f"Hey {user_name}! 📄 **Great resume tips**:\n\n• **Start with a strong summary** highlighting your key skills\n• **Use action verbs** like 'Developed', 'Built', 'Led', 'Optimized'\n• **Quantify achievements** with numbers and percentages\n• **Include relevant keywords** for ATS systems\n• **Keep it concise** - 1-2 pages max\n\n*Upload your resume to get personalized feedback!*"
    
    elif any(word in msg_lower for word in ["skills", "analyze", "gap", "strength", "weakness"]):
        if skills:
            skill_names = [s.split(':')[0].strip('- ') for s in skills[:5]]
            return f"Hey {user_name}! 🧠 **Your current skills analysis**:\n\n**Top Skills**: {', '.join(skill_names)}\n\n**Recommendations**:\n• **Keep building** on your strongest areas\n• **Add complementary skills** to increase job market value\n• **Take assessments** to verify your skill levels\n• **Work on projects** to demonstrate practical application\n\n*Visit the Assessment page to validate your skills!*"
        else:
            return f"Hey {user_name}! 🧠 **Let's build your skills profile**:\n\n• **Upload your resume** to automatically detect skills\n• **Take skill assessments** to validate your knowledge\n• **Add skills manually** from your experience\n• **Complete projects** to demonstrate competency\n\n*Start by visiting the Profile page to set up your skills!*"
    
    elif any(word in msg_lower for word in ["job", "role", "career", "suitable", "match"]):
        if top_roles:
            role_info = "\n".join([f"• **{r['role']}** - {r['match_score']}% match" for r in top_roles[:3]])
            return f"Hey {user_name}! 💼 **Your best job matches**:\n\n{role_info}\n\n**Next steps**:\n• **Analyze skill gaps** for your target role\n• **Identify missing skills** to focus your learning\n• **Build relevant projects** to strengthen your profile\n• **Network in your industry** for opportunities\n\n*Check the Analysis page for detailed gap analysis!*"
        else:
            return f"Hey {user_name}! 💼 **Finding the right career path**:\n\n• **Set up your profile** with skills and experience\n• **Explore different roles** in the Target Role section\n• **Take assessments** to discover your strengths\n• **Research industry trends** and growth areas\n\n*Complete your profile first to get personalized job matches!*"
    
    elif any(word in msg_lower for word in ["salary", "pay", "money", "earn", "income"]):
        if salary_data:
            salary_info = "\n".join([f"• **{s['skill']}** → {s['role']}: {s['salary']}" for s in salary_data[:3]])
            return f"Hey {user_name}! 💰 **Salary insights for your skills**:\n\n{salary_info}\n\n**Factors affecting salary**:\n• **Experience level** (entry/mid/senior)\n• **Location** (metro cities pay more)\n• **Company size** (startups vs enterprises)\n• **Skill demand** in the market\n\n*Your actual salary may vary based on negotiation and performance!*"
        else:
            return f"Hey {user_name}! 💰 **General salary guidance**:\n\n• **Entry level**: ₹3-6 LPA for most tech roles\n• **Mid level** (3-5 years): ₹6-12 LPA\n• **Senior level** (5+ years): ₹12-25 LPA\n• **Specialist roles**: Can go much higher\n\n*Set up your skills profile to get personalized salary insights!*"
    
    elif any(word in msg_lower for word in ["learn", "course", "study", "path", "roadmap"]):
        if top_roles:
            target_role = top_roles[0]['role']
            missing = top_roles[0].get('missing_skills', [])[:3]
            if missing:
                return f"Hey {user_name}! 📚 **Learning path for {target_role}**:\n\n**Priority skills to learn**:\n" + \
                       "\n".join([f"• **{skill}** - High demand skill" for skill in missing]) + \
                       "\n\n**Learning approach**:\n• **Take online courses** (Coursera, Udemy)\n• **Build hands-on projects** \n• **Join communities** and forums\n• **Find mentors** in your field\n\n*Visit the Courses page for specific recommendations!*"
        
        return f"Hey {user_name}! 📚 **Creating your learning path**:\n\n**Steps to success**:\n• **Identify your goal** (target role/skill)\n• **Assess current level** through testing\n• **Find quality resources** (courses, books, projects)\n• **Practice consistently** with real projects\n• **Get feedback** from peers and mentors\n\n*Complete your profile to get a personalized learning roadmap!*"
    
    elif any(word in msg_lower for word in ["help", "what", "how", "can", "do"]):
        features = []
        if page_context == "profile":
            features = ["upload your resume", "add skills manually", "view extracted data"]
        elif page_context == "role":
            features = ["explore job roles", "see match percentages", "find suitable careers"]
        elif page_context == "analysis":
            features = ["analyze skill gaps", "get readiness scores", "see missing competencies"]
        elif page_context == "courses":
            features = ["find learning resources", "get course recommendations", "plan your learning"]
        elif page_context == "ats":
            features = ["check ATS compatibility", "get resume feedback", "improve formatting"]
        else:
            features = ["career guidance", "skill analysis", "job matching", "salary insights", "learning paths"]
            
        return f"Hey {user_name}! 👋 **I'm here to help you with**:\n\n" + \
               "\n".join([f"• **{feature.title()}**" for feature in features]) + \
               "\n\n**What would you like to focus on?** Just ask me about:\n• Resume improvement\n• Skill gap analysis\n• Job recommendations\n• Learning paths\n• Salary insights"
    
    # Default friendly response
    return f"Hey {user_name}! 😊 I understand you're asking about **{message[:50]}{'...' if len(message) > 50 else ''}**\n\n**I can help you with**:\n• 📄 **Resume improvement** and ATS optimization\n• 🧠 **Skill analysis** and gap identification\n• 💼 **Job matching** based on your profile\n• 💰 **Salary insights** for your skills\n• 📚 **Learning paths** and course recommendations\n\n*What specific area would you like to explore?*"
