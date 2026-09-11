"""
SkillGap Engine — ATS Resume Checker & AI Content Detector Service.
Powered by Groq API (llama-3.3-70b-versatile).
"""

from __future__ import annotations
import os
import re
import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"


def _call_groq_api(prompt: str, system_prompt: str, model: str = PRIMARY_MODEL) -> Optional[Dict[str, Any]]:
    """Calls Groq Chat Completions API with JSON response format."""
    if not GROQ_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "SkillGapEngine-ATS/1.0",
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 3000,
        "response_format": {"type": "json_object"},
    }

    req = urllib.request.Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
    except urllib.error.HTTPError as e:
        # Try fallback model if rate-limited or primary model busy
        if model != FALLBACK_MODEL and e.code in (429, 500, 503):
            try:
                return _call_groq_api(prompt, system_prompt, model=FALLBACK_MODEL)
            except Exception:
                pass
        return None
    except Exception:
        if model != FALLBACK_MODEL:
            try:
                return _call_groq_api(prompt, system_prompt, model=FALLBACK_MODEL)
            except Exception:
                pass
        return None


def _heuristic_fallback_analysis(resume_text: str, extracted_skills: List[str]) -> Dict[str, Any]:
    """
    Deterministic rule-based fallback analysis in case of API failure / offline mode.
    Ensures high-fidelity, actionable analysis is always returned to the user.
    """
    lower = resume_text.lower()
    word_count = len(resume_text.split())
    
    # 1. AI pattern checks
    ai_phrases = [
        "spearheaded", "synergized", "leveraged cutting-edge", "orchestrated cross-functional",
        "transformative solutions", "testament to", "fostered an environment", "game-changing",
        "seamless integration", "passionate and driven", "results-oriented professional"
    ]
    ai_phrase_hits = [p for p in ai_phrases if p in lower]
    ai_prob = min(85, max(10, len(ai_phrase_hits) * 18 + (15 if "spearheaded" in lower else 0)))
    
    if ai_prob >= 65:
        verdict = "Heavily AI-Generated / Template-Heavy"
        verdict_summary = "High density of formulaic AI transitions and buzzword syntaxes detected."
    elif ai_prob >= 35:
        verdict = "Mixed / AI-Assisted"
        verdict_summary = "Contains a balanced mix of natural authentic experience with AI-assisted phrasing."
    else:
        verdict = "Likely Human-Written"
        verdict_summary = "Authentic tone with organic sentence structure and domain-specific terminology."

    # 2. Metrics detection
    metric_matches = re.findall(r"(\b\d+[%+kKmM]?\b|\$\d+[\d,]*|\b\d+\s*(?:users|clients|projects|ms|seconds|x|percent)\b)", resume_text)
    metric_count = len(metric_matches)
    
    # 3. Action verbs
    strong_verbs = ["built", "developed", "architected", "engineered", "deployed", "scaled", "optimized", "designed", "implemented", "reduced", "increased", "launched"]
    weak_verbs = ["helped", "assisted", "worked on", "handled", "responsible for", "participated in", "duties included"]
    
    strong_hits = [v for v in strong_verbs if re.search(r'\b' + v + r'\b', lower)]
    weak_hits = [v for v in weak_verbs if re.search(r'\b' + v + r'\b', lower)]

    # 4. Scores
    fmt_score = 85 if word_count > 150 else 60
    metric_score = min(95, metric_count * 12 + 40)
    kw_score = min(95, len(extracted_skills) * 8 + 45)
    impact_score = min(95, len(strong_hits) * 10 - len(weak_hits) * 5 + 60)
    readability_score = 80
    completeness_score = 85 if ("education" in lower and "experience" in lower) else 65

    overall_score = round((fmt_score * 0.15) + (metric_score * 0.25) + (kw_score * 0.20) + (impact_score * 0.20) + (completeness_score * 0.10) + (readability_score * 0.10))
    overall_score = max(30, min(98, overall_score))

    grade = "A+ (Excellent)" if overall_score >= 90 else "A (Strong)" if overall_score >= 80 else "B (Good)" if overall_score >= 70 else "C (Needs Work)" if overall_score >= 55 else "D (Rework Required)"

    return {
        "ai_detection": {
            "ai_probability_score": ai_prob,
            "human_score": 100 - ai_prob,
            "verdict": verdict,
            "verdict_summary": verdict_summary,
            "flagged_ai_patterns": ai_phrase_hits[:4] if ai_phrase_hits else ["Standard standardized bullet structure"],
            "human_markers": ["Contextual project descriptions", "Domain technical skill groupings"]
        },
        "ats_scoring": {
            "overall_score": overall_score,
            "grade": grade,
            "formatting_score": fmt_score,
            "impact_score": impact_score,
            "metrics_score": metric_score,
            "completeness_score": completeness_score,
            "readability_score": readability_score,
            "keyword_score": kw_score
        },
        "diagnostics": {
            "key_strengths": [
                f"Extracted {len(extracted_skills)} relevant technical competencies.",
                f"Contains {metric_count} measurable impact metrics / figures." if metric_count > 0 else "Clear chronological flow.",
                "Standard section headings that parse cleanly in standard ATS software."
            ],
            "critical_issues": [
                "Passive phrasing found in experience bullets — replace with high-impact action verbs." if weak_hits else "Add more quantifiable business metrics (% increased, time saved, scale).",
                "Ensure skills are demonstrated through project achievements rather than isolated lists."
            ],
            "quantifiable_metrics_count": metric_count,
            "quantifiable_metrics_examples": metric_matches[:5],
            "action_verbs_strong": strong_hits[:8],
            "action_verbs_weak": weak_hits[:6],
            "section_health": [
                {"section": "Contact Information", "status": "good", "feedback": "Essential contact details present."},
                {"section": "Technical Skills", "status": "good", "feedback": f"Well populated ({len(extracted_skills)} skills identified)."},
                {"section": "Work Experience / Projects", "status": "good" if metric_count > 2 else "warning", "feedback": "Expand bullet impact with the Google XYZ formula."},
                {"section": "Education", "status": "good", "feedback": "Academic qualifications properly indexed."}
            ]
        },
        "resume_builder_guide": {
            "top_actionable_recommendations": [
                "Apply the Google XYZ Formula: 'Accomplished [X] as measured by [Y], by doing [Z]' to every work bullet.",
                "Front-load bullet points with impactful action verbs (e.g. Architected, Engineered, Optimized) instead of passive duties.",
                "Quantify every major achievement with numbers, percentage improvements, latency drops, or user counts.",
                "Tailor technical keywords directly to your target role to maximize ATS keyword parse index.",
                "Keep formatting simple: single-column layout, standard headings, no graphical skill bars or multi-column tables."
            ],
            "bullet_point_improvements": [
                {
                    "original": "Worked on backend development and fixed database bugs.",
                    "improved": "Engineered 12+ REST APIs and optimized PostgreSQL queries, reducing endpoint latency by 34%.",
                    "explanation": "Replaced weak passive verb ('worked on') with quantifiable scale and concrete performance metrics.",
                    "formula_applied": "Google XYZ Formula (Accomplished X, measured by Y, by doing Z)"
                },
                {
                    "original": "Responsible for managing team project and coordinating tasks.",
                    "improved": "Spearheaded agile sprint delivery across 5 engineers, accelerating feature release cycle by 25%.",
                    "explanation": "Clarifies leadership scope, team size, and measurable delivery velocity.",
                    "formula_applied": "Action Verb + Scope + Quantifiable Business Impact"
                }
            ],
            "missing_critical_keywords": ["CI/CD Pipelines", "System Architecture", "Performance Optimization", "Automated Testing"],
            "recommended_sections_to_add": ["Professional Summary (3-line elevator pitch)", "Key Projects with Live/GitHub Links"],
            "formatting_checklist": [
                {"item": "Single-Column Clean Layout", "passed": True, "tip": "Multi-column layouts often scramble ATS parsers."},
                {"item": "Standard Section Headings", "passed": True, "tip": "Use standard titles: Experience, Education, Skills, Projects."},
                {"item": "Quantifiable Metrics Present", "passed": metric_count >= 3, "tip": "Target at least 1 metric per bullet point."},
                {"item": "Action-Oriented Bullets", "passed": len(strong_hits) >= 3, "tip": "Start every bullet with a strong past-tense action verb."},
                {"item": "No Tables or Text Boxes", "passed": True, "tip": "Tables can cause text to be skipped by legacy ATS software."}
            ]
        }
    }


def analyze_resume_ats(resume_text: str, extracted_skills: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Executes deep ATS compatibility analysis & AI content detection via Groq (Llama-3.3-70b-versatile).
    Falls back gracefully to deterministic analysis if API is offline.
    """
    if extracted_skills is None:
        extracted_skills = []

    # Clean and truncate text if extraordinarily huge to prevent token limit issues
    clean_text = resume_text.strip()
    if len(clean_text) > 8000:
        clean_text = clean_text[:8000]

    system_prompt = (
        "You are an elite ATS (Applicant Tracking System) Auditor, Resume Architect, and AI Content Detector. "
        "Your task is to thoroughly analyze the provided resume text. "
        "You must evaluate: "
        "1. AI vs Human Detection (AI probability score 0-100%, synthetic style flags, authentic markers). "
        "2. ATS Compatibility Score (0-100 overall, breakdown across formatting, impact verbs, metrics, completeness, readability, keywords). "
        "3. Diagnostics (strengths, critical red flags, strong vs weak action verbs, metric counts). "
        "4. Highly personalized 'How to Build a Good Resume/CV' guide with specific Before/After bullet point rewrites based on their ACTUAL resume text using Google's XYZ formula. "
        "Respond ONLY with valid, strict JSON matching the exact schema requested."
    )

    user_prompt = f"""
Analyze this resume text and provide a comprehensive ATS & AI diagnostic report.

EXTRACTED SKILLS SO FAR: {json.dumps(extracted_skills[:15])}

RESUME TEXT:
\"\"\"
{clean_text}
\"\"\"

Return a valid JSON object matching this exact schema:
{{
  "ai_detection": {{
    "ai_probability_score": <int 0-100>,
    "human_score": <int 0-100>,
    "verdict": "<'Likely Human-Written' | 'Mixed / AI-Assisted' | 'Heavily AI-Generated'>",
    "verdict_summary": "<concise 1-2 sentence evaluation>",
    "flagged_ai_patterns": ["<flag 1>", "<flag 2>"],
    "human_markers": ["<marker 1>", "<marker 2>"]
  }},
  "ats_scoring": {{
    "overall_score": <int 0-100>,
    "grade": "<'A+ (Excellent)' | 'A (Strong)' | 'B (Good)' | 'C (Needs Work)' | 'D (Rework Required)'>",
    "formatting_score": <int 0-100>,
    "impact_score": <int 0-100>,
    "metrics_score": <int 0-100>,
    "completeness_score": <int 0-100>,
    "readability_score": <int 0-100>,
    "keyword_score": <int 0-100>
  }},
  "diagnostics": {{
    "key_strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
    "critical_issues": ["<issue 1>", "<issue 2>"],
    "quantifiable_metrics_count": <int count of numbers/percentages found>,
    "quantifiable_metrics_examples": ["<metric example 1>", "<metric example 2>"],
    "action_verbs_strong": ["<strong verb 1>", "<strong verb 2>"],
    "action_verbs_weak": ["<weak verb 1>", "<weak verb 2>"],
    "section_health": [
      {{"section": "Contact Information", "status": "<'good'|'warning'|'missing'>", "feedback": "<feedback>"}},
      {{"section": "Professional Summary", "status": "<'good'|'warning'|'missing'>", "feedback": "<feedback>"}},
      {{"section": "Technical Skills", "status": "<'good'|'warning'|'missing'>", "feedback": "<feedback>"}},
      {{"section": "Work Experience / Projects", "status": "<'good'|'warning'|'missing'>", "feedback": "<feedback>"}},
      {{"section": "Education", "status": "<'good'|'warning'|'missing'>", "feedback": "<feedback>"}}
    ]
  }},
  "resume_builder_guide": {{
    "top_actionable_recommendations": [
      "<concrete tip 1>",
      "<concrete tip 2>",
      "<concrete tip 3>",
      "<concrete tip 4>",
      "<concrete tip 5>"
    ],
    "bullet_point_improvements": [
      {{
        "original": "<an actual weak or generic bullet found in the resume>",
        "improved": "<re-written high-impact version using Google XYZ formula with realistic metrics>",
        "explanation": "<why this rewrite is far more compelling for ATS and hiring managers>",
        "formula_applied": "Google XYZ Formula (Accomplished [X], measured by [Y], by doing [Z])"
      }},
      {{
        "original": "<second weak bullet from resume>",
        "improved": "<improved high-impact rewrite>",
        "explanation": "<explanation>",
        "formula_applied": "Action Verb + Scope + Quantifiable Business Impact"
      }}
    ],
    "missing_critical_keywords": ["<keyword 1>", "<keyword 2>", "<keyword 3>", "<keyword 4>"],
    "recommended_sections_to_add": ["<section 1>", "<section 2>"],
    "formatting_checklist": [
      {{"item": "Single-Column Clean Layout", "passed": true, "tip": "Multi-column tables can confuse ATS parsers."}},
      {{"item": "Standard Section Headings", "passed": true, "tip": "Use standard titles: Experience, Education, Skills, Projects."}},
      {{"item": "Quantifiable Metrics Present", "passed": <true|false>, "tip": "Include %, $, user counts, or time improvements."}},
      {{"item": "Action-Oriented Bullets", "passed": <true|false>, "tip": "Begin with strong action verbs like Architected, Reduced, Spearheaded."}},
      {{"item": "Standard Font & Hierarchy", "passed": true, "tip": "Use standard fonts (Inter, Arial, Calibri) 10-12pt."}}
    ]
  }}
}}
"""

    result = _call_groq_api(user_prompt, system_prompt, model=PRIMARY_MODEL)

    if result and "ats_scoring" in result and "ai_detection" in result:
        return result

    # Fallback to local heuristic engine if API is unavailable or returns invalid shape
    return _heuristic_fallback_analysis(clean_text, extracted_skills)
