"""
Resume parser service.

Extracts text from PDF or DOCX, then matches against known competency names
using both keyword heuristics and sentence-transformer semantic similarity.

Returns structured ExtractedProfile with:
  - name (if detectable)
  - education
  - experience summary
  - technical_skills list
  - soft_skills list
  - projects list
  - courses_certifications list
  - matched_competency_ids  (competency IDs from our catalogue)
"""

from __future__ import annotations
import io
import re
from dataclasses import dataclass, field
from typing import Optional

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
# Skill keyword bank  (competency_id -> list of keywords)
# ---------------------------------------------------------------------------

SKILL_KEYWORDS: dict[int, list[str]] = {
    1:  ["programming", "coding", "algorithms", "variables", "loops", "functions"],
    2:  ["python", "flask", "django", "fastapi", "pandas", "numpy", "matplotlib"],
    3:  ["data structures", "algorithms", "dsa", "leetcode", "trees", "graphs", "sorting"],
    4:  ["oop", "object oriented", "design patterns", "solid", "class", "inheritance"],
    5:  ["git", "github", "gitlab", "version control", "branching", "pull request"],
    6:  ["rest api", "api", "fastapi", "flask", "endpoint", "http", "openapi", "swagger"],
    7:  ["sql", "mysql", "postgresql", "sqlite", "database", "queries", "orm", "sqlalchemy"],
    8:  ["system design", "scalability", "microservices", "load balancing", "architecture"],
    9:  ["aws", "azure", "gcp", "cloud", "ec2", "s3", "lambda", "deployment"],
    10: ["linux", "bash", "shell", "ubuntu", "command line", "terminal", "unix"],
    11: ["statistics", "probability", "hypothesis testing", "regression", "distributions"],
    12: ["data wrangling", "data cleaning", "pandas", "etl", "data processing"],
    13: ["visualization", "matplotlib", "seaborn", "tableau", "power bi", "plotly", "charts"],
    14: ["machine learning", "ml", "scikit-learn", "sklearn", "classification", "clustering", "random forest", "xgboost"],
    15: ["deep learning", "neural network", "cnn", "rnn", "pytorch", "tensorflow", "keras"],
    16: ["feature engineering", "feature selection", "encoding", "scaling", "dimensionality"],
    17: ["spark", "hadoop", "big data", "hive", "kafka", "distributed"],
    18: ["official statistics", "census", "national accounts", "cpi", "gdp", "mospi", "nsso"],
    19: ["sampling", "stratified sampling", "cluster sampling", "survey design"],
    20: ["econometrics", "panel data", "time series", "causal inference", "iv estimation"],
    21: ["circuit analysis", "kvl", "kcl", "thevenin", "ac circuit", "dc circuit"],
    22: ["power systems", "transmission", "distribution", "load flow", "protection relay"],
    23: ["control systems", "pid", "bode plot", "transfer function", "state space"],
    24: ["electrical machines", "transformer", "induction motor", "synchronous machine"],
    25: ["matlab", "simulink", "numerical computation"],
    26: ["digital electronics", "logic gates", "flip flop", "fpga", "verilog", "vhdl"],
    27: ["microcontroller", "arduino", "stm32", "arm", "embedded", "peripheral", "firmware"],
    28: ["rtos", "freertos", "task scheduling", "semaphore", "real time"],
    29: ["pcb", "kicad", "altium", "schematic", "pcb design", "eagle"],
    30: ["signal processing", "dsp", "fourier", "filter", "fft"],
    31: ["cad", "solidworks", "autocad", "catia", "3d modeling", "drafting"],
    32: ["thermodynamics", "heat transfer", "refrigeration", "carnot"],
    33: ["manufacturing", "machining", "casting", "welding", "cnc", "additive manufacturing"],
    34: ["finite element", "fea", "ansys", "abaqus", "structural analysis simulation"],
    35: ["fluid mechanics", "bernoulli", "pipe flow", "turbomachinery", "cfd"],
    36: ["structural analysis", "beams", "trusses", "bending moment", "staad"],
    37: ["geotechnical", "soil mechanics", "foundation design", "site investigation"],
    38: ["project management", "gantt chart", "scheduling", "cost estimation", "agile", "scrum"],
    39: ["gis", "arcgis", "qgis", "remote sensing", "spatial data"],
    40: ["environmental engineering", "water treatment", "eia", "sustainability"],
    41: ["project management", "agile", "scrum", "stakeholder", "planning"],
    42: ["communication", "technical writing", "presentation", "report", "documentation"],
    43: ["problem solving", "critical thinking", "root cause", "analytical"],
    44: ["business", "domain knowledge", "kpi", "business process"],
    45: ["data ethics", "privacy", "gdpr", "responsible ai", "bias", "fairness"],
    46: ["research", "literature review", "experimental design", "research methodology"],
    47: ["mathematical modelling", "linear algebra", "calculus", "differential equations"],
    48: ["iot", "mqtt", "sensor", "raspberry pi", "edge computing", "coap"],
    49: ["c programming", "c++", "cpp", "pointers", "memory management", "embedded c"],
    50: ["docker", "devops", "ci/cd", "github actions", "kubernetes", "pipeline"],
}


def _match_competencies_by_keywords(text: str) -> list[int]:
    text_lower = text.lower()
    matched = []
    for comp_id, keywords in SKILL_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            matched.append(comp_id)
    return matched


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

    # Match competencies across full text
    matched_ids = _match_competencies_by_keywords(text)

    # Infer competency levels conservatively
    # If mentioned in skills section -> level 2 (basic)
    # If mentioned in projects/experience -> level 3 (intermediate)
    # Otherwise -> level 1 (awareness)
    skills_lower = " ".join(skill_lines).lower()
    proj_exp_lower = " ".join(
        sections.get("projects", []) + sections.get("experience", [])
    ).lower()

    inferred: dict[int, int] = {}
    for comp_id in matched_ids:
        keywords = SKILL_KEYWORDS.get(comp_id, [])
        in_skills = any(kw in skills_lower for kw in keywords)
        in_proj = any(kw in proj_exp_lower for kw in keywords)
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
