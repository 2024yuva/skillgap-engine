"""
Resume parser service.

Extracts text from PDF or DOCX, then matches against known competency names
using keyword heuristics + skill normalization.

Returns structured ExtractedProfile with:
  - name (if detectable)
  - education
  - experience summary
  - technical_skills list
  - soft_skills list
  - projects list
  - courses_certifications list
  - matched_competency_ids  (canonical competency IDs from our catalogue)
  - inferred_levels (dict[int, int])  — conservative level estimates
"""

from __future__ import annotations
import io
import re
from dataclasses import dataclass, field
from typing import Optional

# Import the canonical normalization map
from app.ingestion.seed_data import SKILL_NORMALIZATION_MAP

# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def extract_text_from_pdf(data: bytes) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(io.BytesIO(data))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def extract_text_from_docx(data: bytes) -> str:
    from docx import Document
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(filename: str, data: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(data)
    if lower.endswith(".docx"):
        return extract_text_from_docx(data)
    # plain text fallback
    return data.decode("utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# Section detection helpers
# ---------------------------------------------------------------------------

SECTION_PATTERNS = {
    "education": re.compile(
        r"(education|academic|qualification|degree|university|college|b\.?tech|b\.?e\b|m\.?tech|m\.?sc|b\.?sc)",
        re.I,
    ),
    "experience": re.compile(
        r"(experience|work history|employment|internship|project experience|career)",
        re.I,
    ),
    "skills": re.compile(
        r"(skills|technical skills|core competencies|technologies|tools|expertise|proficiencies)",
        re.I,
    ),
    "projects": re.compile(r"(projects|personal projects|academic projects|portfolio)", re.I),
    "certifications": re.compile(
        r"(certifications?|courses?|training|mooc|nptel|coursera|udemy|swayam|achievements?|awards?)",
        re.I,
    ),
}

def _split_sections(text: str) -> dict[str, list[str]]:
    """Rough section splitter by heading detection."""
    lines = text.splitlines()
    sections: dict[str, list[str]] = {k: [] for k in SECTION_PATTERNS}
    sections["other"] = []
    current = "other"
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        matched = False
        for section, pat in SECTION_PATTERNS.items():
            if pat.search(stripped) and len(stripped) < 80:
                current = section
                matched = True
                break
        if not matched:
            sections[current].append(stripped)
    return sections


# ---------------------------------------------------------------------------
# Skill matching via SKILL_NORMALIZATION_MAP
# ---------------------------------------------------------------------------

def _match_competencies_by_keywords(text: str) -> list[int]:
    """
    Match the resume text against the canonical SKILL_NORMALIZATION_MAP.
    Returns a deduplicated list of canonical competency IDs found.

    Normalization ensures that 'Python', 'Python Programming', 'Python Scripting',
    'Pandas', 'NumPy' etc. all map to the same canonical competency ID (3).
    """
    text_lower = text.lower()
    matched_ids: set[int] = set()

    # Sort by keyword length descending so longer phrases match before substrings
    sorted_keywords = sorted(SKILL_NORMALIZATION_MAP.keys(), key=len, reverse=True)
    for kw in sorted_keywords:
        # Use word-boundary-aware search to avoid partial matches
        pattern = r'(?<![a-z0-9])' + re.escape(kw) + r'(?![a-z0-9])'
        if re.search(pattern, text_lower):
            matched_ids.add(SKILL_NORMALIZATION_MAP[kw])

    return list(matched_ids)


# ---------------------------------------------------------------------------
# Name extraction (simple heuristic)
# ---------------------------------------------------------------------------

def _extract_name(text: str) -> Optional[str]:
    """Try to extract the candidate's name from the first few lines."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # Name is usually one of the first 3 lines, title-cased, no numbers
    for line in lines[:5]:
        if (
            len(line.split()) in (2, 3, 4)
            and not any(c.isdigit() for c in line)
            and not any(sym in line for sym in ["@", "http", "|", "/", "\\"])
            and line[0].isupper()
        ):
            return line
    return None


def _extract_education(sections: dict[str, list[str]]) -> str:
    lines = sections.get("education", [])
    return " | ".join(lines[:3]) if lines else ""


def _extract_experience_summary(sections: dict[str, list[str]]) -> str:
    lines = sections.get("experience", [])
    return " | ".join(lines[:3]) if lines else ""


def _extract_list_items(lines: list[str]) -> list[str]:
    """Clean up bullet/dash prefixes and return non-empty items."""
    cleaned = []
    for line in lines:
        line = re.sub(r"^[\-\•\*\u2022\u25cf\u2013\u2014\uf0b7]+\s*", "", line)
        if line.strip():
            cleaned.append(line.strip())
    return cleaned[:20]


# ---------------------------------------------------------------------------
# Main extractor
# ---------------------------------------------------------------------------

@dataclass
class ExtractedProfile:
    name: Optional[str]
    education: str
    experience_summary: str
    technical_skills: list[str] = field(default_factory=list)
    soft_skills: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    courses_certifications: list[str] = field(default_factory=list)
    matched_competency_ids: list[int] = field(default_factory=list)
    # competency_id -> inferred level (1-3, conservative)
    inferred_levels: dict[int, int] = field(default_factory=dict)


SOFT_SKILL_WORDS = [
    "communication", "leadership", "teamwork", "problem solving",
    "time management", "adaptability", "collaboration", "presentation",
    "negotiation", "conflict resolution", "critical thinking",
]

TECH_SECTION_MARKERS = re.compile(
    r"(python|java|c\+\+|sql|react|node|aws|docker|git|matlab|arduino|"
    r"tensorflow|pytorch|scikit|tableau|power bi|solidworks|ansys|autocad)",
    re.I,
)


def parse_resume(filename: str, data: bytes) -> ExtractedProfile:
    text = extract_text(filename, data)
    sections = _split_sections(text)

    name = _extract_name(text)
    education = _extract_education(sections)
    experience_summary = _extract_experience_summary(sections)

    skill_lines = _extract_list_items(sections.get("skills", []))
    project_lines = _extract_list_items(sections.get("projects", []))
    cert_lines = _extract_list_items(sections.get("certifications", []))

    # Split skills into tech vs soft
    tech_skills = [s for s in skill_lines if not any(sw in s.lower() for sw in SOFT_SKILL_WORDS)]
    soft_skills = [s for s in skill_lines if any(sw in s.lower() for sw in SOFT_SKILL_WORDS)]

    # Also pull tech tokens from skills section text
    skills_text = " ".join(skill_lines)
    for token in re.findall(r"[A-Za-z][A-Za-z0-9+#./\- ]{1,30}", skills_text):
        token = token.strip()
        if TECH_SECTION_MARKERS.search(token) and token not in tech_skills:
            tech_skills.append(token)

    # Match competencies across full text using normalization map
    matched_ids = _match_competencies_by_keywords(text)

    # Infer competency levels conservatively
    # If mentioned in projects/experience section -> level 3 (intermediate)
    # If mentioned in skills section -> level 2 (basic)
    # Otherwise -> level 1 (awareness)
    skills_lower = " ".join(skill_lines).lower()
    proj_exp_lower = " ".join(
        sections.get("projects", []) + sections.get("experience", [])
    ).lower()

    inferred: dict[int, int] = {}
    for comp_id in matched_ids:
        # Find keywords for this competency from the normalization map
        comp_keywords = [kw for kw, cid in SKILL_NORMALIZATION_MAP.items() if cid == comp_id]
        in_skills = any(kw in skills_lower for kw in comp_keywords)
        in_proj = any(kw in proj_exp_lower for kw in comp_keywords)
        if in_proj:
            inferred[comp_id] = 3
        elif in_skills:
            inferred[comp_id] = 2
        else:
            inferred[comp_id] = 1

    return ExtractedProfile(
        name=name,
        education=education,
        experience_summary=experience_summary,
        technical_skills=list(dict.fromkeys(tech_skills))[:15],
        soft_skills=list(dict.fromkeys(soft_skills))[:8],
        projects=project_lines[:8],
        courses_certifications=cert_lines[:10],
        matched_competency_ids=matched_ids,
        inferred_levels=inferred,
    )
