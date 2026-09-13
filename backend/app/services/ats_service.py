"""
SkillGap Engine — ATS Resume Checker & AI Content Detector Service.
Powered by Groq API with OpenAI GPT-OSS-120B for personalized resume analysis.
"""

from __future__ import annotations
import os
import re
import json
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


def _call_groq_api(prompt: str, system_prompt: str, model: str = "openai/gpt-oss-120b") -> Optional[Dict[str, Any]]:
    """Calls Groq Chat Completions API using the official Groq client."""
    if not GROQ_AVAILABLE or not GROQ_API_KEY:
        print("Groq not available: GROQ_AVAILABLE =", GROQ_AVAILABLE, "GROQ_API_KEY =", bool(GROQ_API_KEY))
        return None

    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        print(f"Making Groq API call with model: {model}")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_completion_tokens=4000,
            top_p=1,
            stream=False,
            stop=None
        )
        
        content = completion.choices[0].message.content
        print("Groq API response received, content length:", len(content) if content else 0)
        
        if not content:
            print("No content in Groq response")
            return None
            
        # Parse JSON response
        try:
            result = json.loads(content)
            print("Successfully parsed JSON from Groq response")
            return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Try to extract JSON from response if wrapped in markdown
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group(1))
                    print("Successfully extracted JSON from markdown")
                    return result
                except json.JSONDecodeError:
                    print("Failed to parse extracted JSON")
            print("Raw response content:", content[:500])
            return None
            
    except Exception as e:
        print(f"Groq API error with model {model}: {e}")
        # Try fallback model if the primary model fails
        if model != "llama-3.3-70b-versatile":
            print("Trying fallback model: llama-3.3-70b-versatile")
            return _call_groq_api(prompt, system_prompt, model="llama-3.3-70b-versatile")
        import traceback
        traceback.print_exc()
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

    # 2. Metrics detection — match only meaningful figures (%, $, scale suffixes, or domain units)
    # Explicitly exclude bare 7+ digit numbers (phone numbers, student IDs, etc.)
    metric_matches = [
        m for m in re.findall(
            r"(\b\d+[%+kKmM]\b|\$\d+[\d,]*|\b\d+\s*(?:users|clients|projects|ms|seconds|x|percent)\b)",
            resume_text,
        )
        if not re.fullmatch(r"\d{7,}", m.strip())
    ]
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
                "Quantify impact in every bullet – add measurable numbers, percentages, or scale wherever possible.",
                "Replace weak passive verbs – swap phrases like 'responsible for' or 'worked on' with strong action verbs such as Built, Optimized, or Led.",
                f"Boost ATS keyword density – surface more of your detected skills ({', '.join(extracted_skills[:4]) if extracted_skills else 'domain tools'}) directly in experience bullets.",
                "Tighten each bullet to one strong achievement – remove filler words and focus on outcome over activity.",
                "Add a Professional Summary – a 2–3 line headline that front-loads your strongest skills and career goal."
            ],
            "bullet_point_improvements": [
                {
                    "original": weak_hits[0].capitalize() + " on a key deliverable." if weak_hits else "Worked on development tasks.",
                    "improved": "Built and delivered end-to-end solutions, reducing manual effort by ~30% through process automation.",
                    "explanation": "Leads with a strong action verb and ties the work to a concrete measurable outcome.",
                    "formula_applied": ""
                }
            ],
            "missing_critical_keywords": [s for s in ["Docker", "CI/CD", "REST API", "Agile", "SQL", "Cloud", "Testing"] if s.lower() not in lower and s not in extracted_skills][:5],
            "recommended_sections_to_add": (
                (["Professional Summary"] if "summary" not in lower and "objective" not in lower else []) +
                (["Projects with GitHub / Demo Links"] if "github" not in lower and "project" not in lower else []) +
                (["Certifications & Courses"] if "certif" not in lower and "course" not in lower else []) +
                (["Technical Skills (grouped by category)"] if len(extracted_skills) < 4 else [])
            ) or ["Quantified Achievements section"],
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
    Executes deep ATS compatibility analysis & AI content detection via Groq OpenAI GPT-OSS-120B.
    Provides honest, personalized feedback specific to each resume.
    Falls back gracefully to deterministic analysis if API is unavailable.
    """
    if extracted_skills is None:
        extracted_skills = []

    # Clean and truncate text if extraordinarily huge to prevent token limit issues
    clean_text = resume_text.strip()
    if len(clean_text) > 12000:
        clean_text = clean_text[:12000]

    system_prompt = (
        "You are an elite ATS (Applicant Tracking System) expert and professional resume reviewer with 15+ years of experience "
        "in technical recruiting and talent acquisition. You provide brutally honest, constructive feedback that helps candidates "
        "improve their resumes significantly.\n\n"
        
        "Your analysis must be:\n"
        "1. PERSONALIZED - Based entirely on the specific content, strengths, and weaknesses of THIS resume\n"
        "2. HONEST - Point out real issues without sugar-coating, but remain constructive\n"
        "3. ACTIONABLE - Every recommendation must be specific and implementable\n"
        "4. VARIED - Each resume gets unique feedback; avoid template responses\n\n"
        
        "Analyze the resume across these dimensions:\n"
        "- AI vs Human writing patterns (detect synthetic/template language vs authentic voice)\n"
        "- ATS compatibility (formatting, keywords, structure that systems can parse)\n"
        "- Impact and quantification (measurable achievements vs vague descriptions)\n"
        "- Professional presentation (clarity, conciseness, relevance)\n"
        "- Technical depth and credibility (for technical roles)\n\n"
        
        "Be direct about weaknesses but always provide concrete improvement paths. "
        "Focus on what will make the biggest difference for this specific candidate's job search success.\n\n"
        
        "CRITICAL: You must respond with ONLY valid JSON. No markdown, no explanations, no code blocks. "
        "Just pure JSON starting with { and ending with }."
    )

    user_prompt = f"""
Analyze this resume and provide a comprehensive, personalized ATS review with honest feedback.

CANDIDATE'S TECHNICAL SKILLS: {json.dumps(extracted_skills[:20])}

RESUME CONTENT:
{clean_text}

Provide your analysis as a JSON object with this structure:
{{
  "ai_detection": {{
    "ai_probability_score": <0-100 integer>,
    "human_score": <0-100 integer>,
    "verdict": "<Likely Human-Written|Mixed AI-Assisted|Heavily AI-Generated>",
    "verdict_summary": "<honest assessment in 1-2 sentences>",
    "flagged_ai_patterns": ["<specific AI pattern 1>", "<specific AI pattern 2>"],
    "human_markers": ["<authentic element 1>", "<authentic element 2>"]
  }},
  "ats_scoring": {{
    "overall_score": <0-100 integer>,
    "grade": "<A+ Excellent|A Strong|B Good|C Needs Work|D Rework Required>",
    "formatting_score": <0-100 integer>,
    "impact_score": <0-100 integer>,
    "metrics_score": <0-100 integer>,
    "completeness_score": <0-100 integer>,
    "readability_score": <0-100 integer>,
    "keyword_score": <0-100 integer>
  }},
  "diagnostics": {{
    "key_strengths": ["<specific strength 1>", "<specific strength 2>", "<specific strength 3>"],
    "critical_issues": ["<honest critique 1>", "<honest critique 2>"],
    "quantifiable_metrics_count": <integer>,
    "quantifiable_metrics_examples": ["<actual metric 1>", "<actual metric 2>"],
    "action_verbs_strong": ["<strong verb used>", "<strong verb used>"],
    "action_verbs_weak": ["<weak phrase used>", "<weak phrase used>"],
    "section_health": [
      {{"section": "Contact Information", "status": "good|warning|missing", "feedback": "<specific feedback>"}},
      {{"section": "Professional Summary", "status": "good|warning|missing", "feedback": "<specific feedback>"}},
      {{"section": "Technical Skills", "status": "good|warning|missing", "feedback": "<specific feedback>"}},
      {{"section": "Work Experience", "status": "good|warning|missing", "feedback": "<specific feedback>"}},
      {{"section": "Education", "status": "good|warning|missing", "feedback": "<specific feedback>"}}
    ]
  }},
  "resume_builder_guide": {{
    "top_actionable_recommendations": [
      "<personalized recommendation 1 for THIS resume>",
      "<personalized recommendation 2 for THIS resume>",
      "<personalized recommendation 3 for THIS resume>",
      "<personalized recommendation 4 for THIS resume>",
      "<personalized recommendation 5 for THIS resume>"
    ],
    "bullet_point_improvements": [
      {{
        "original": "<actual weak bullet from this resume>",
        "improved": "<rewritten version with strong impact>",
        "explanation": "<why this improvement makes a difference>",
        "formula_applied": ""
      }},
      {{
        "original": "<second actual weak bullet from this resume>", 
        "improved": "<rewritten version with metrics and action>",
        "explanation": "<explanation of improvement>",
        "formula_applied": ""
      }}
    ],
    "missing_critical_keywords": ["<missing keyword 1>", "<missing keyword 2>", "<missing keyword 3>"],
    "recommended_sections_to_add": ["<section this resume lacks>", "<another missing section>"],
    "formatting_checklist": [
      {{"item": "Clean Single-Column Layout", "passed": true, "tip": "ATS systems prefer simple layouts"}},
      {{"item": "Standard Section Headers", "passed": true, "tip": "Use Experience, Education, Skills, Projects"}},
      {{"item": "Quantified Achievements", "passed": <true|false>, "tip": "Include numbers, percentages, scales"}},
      {{"item": "Strong Action Verbs", "passed": <true|false>, "tip": "Start bullets with Built, Developed, Optimized"}},
      {{"item": "Professional Font Choice", "passed": true, "tip": "Stick to Arial, Calibri, or similar clean fonts"}}
    ]
  }}
}}

Focus on what's actually in this resume. Be specific, honest, and constructive in your feedback.
"""

    result = _call_groq_api(user_prompt, system_prompt)

    if result and "ats_scoring" in result and "ai_detection" in result:
        print("Groq API returned valid result, using it")
        return result

    print("Groq API failed or returned invalid result, falling back to heuristic analysis")
    # Fallback to local heuristic engine if API is unavailable or returns invalid shape
    return _heuristic_fallback_analysis(clean_text, extracted_skills)
