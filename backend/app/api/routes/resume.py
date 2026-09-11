"""
Resume upload, parsing, and ATS checker endpoint.
Powered by Groq API.

POST /api/v1/resume/parse
  - Accepts PDF, DOCX, or TXT upload (multipart/form-data)
  - Returns extracted profile + matched competency IDs + inferred levels + ATS analysis (AI detection, ATS scores, CV builder recommendations)

POST /api/v1/resume/ats-check
  - Accepts raw resume text or file
  - Returns comprehensive ATS & AI analysis directly

POST /api/v1/resume/apply/{user_id}
  - Takes parsed result and writes UserCompetency rows for the user
"""

from __future__ import annotations
from typing import Optional, Any, Dict, List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database.connection import get_db
from app.services.resume_parser import parse_resume, extract_text
from app.services.ats_service import analyze_resume_ats
from app.models.models import User, UserCompetency, Competency

router = APIRouter(prefix="/resume", tags=["resume"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


# ---------------------------------------------------------------------------
# ATS & AI Schemas
# ---------------------------------------------------------------------------

class AiDetectionSchema(BaseModel):
    ai_probability_score: int = Field(..., description="0 to 100 percentage")
    human_score: int = Field(..., description="0 to 100 percentage")
    verdict: str
    verdict_summary: str
    flagged_ai_patterns: List[str] = []
    human_markers: List[str] = []


class AtsScoringSchema(BaseModel):
    overall_score: int = Field(..., description="0 to 100")
    grade: str
    formatting_score: int
    impact_score: int
    metrics_score: int
    completeness_score: int
    readability_score: int
    keyword_score: int


class SectionHealthItem(BaseModel):
    section: str
    status: str  # good, warning, missing
    feedback: str


class AtsDiagnosticsSchema(BaseModel):
    key_strengths: List[str] = []
    critical_issues: List[str] = []
    quantifiable_metrics_count: int = 0
    quantifiable_metrics_examples: List[str] = []
    action_verbs_strong: List[str] = []
    action_verbs_weak: List[str] = []
    section_health: List[SectionHealthItem] = []


class BulletPointImprovement(BaseModel):
    original: str
    improved: str
    explanation: str
    formula_applied: str


class FormattingChecklistItem(BaseModel):
    item: str
    passed: bool
    tip: str


class ResumeBuilderGuideSchema(BaseModel):
    top_actionable_recommendations: List[str] = []
    bullet_point_improvements: List[BulletPointImprovement] = []
    missing_critical_keywords: List[str] = []
    recommended_sections_to_add: List[str] = []
    formatting_checklist: List[FormattingChecklistItem] = []


class AtsAnalysisResult(BaseModel):
    ai_detection: AiDetectionSchema
    ats_scoring: AtsScoringSchema
    diagnostics: AtsDiagnosticsSchema
    resume_builder_guide: ResumeBuilderGuideSchema


class ParsedProfileResponse(BaseModel):
    name: Optional[str]
    education: str
    experience_summary: str
    technical_skills: List[str]
    soft_skills: List[str]
    projects: List[str]
    courses_certifications: List[str]
    matched_competency_ids: List[int]
    inferred_levels: Dict[str, int]   # competency_id (str key for JSON) -> level
    ats_analysis: Optional[AtsAnalysisResult] = None


class ApplyResumePayload(BaseModel):
    inferred_levels: Dict[int, int]   # competency_id -> level
    name: Optional[str] = None
    education: Optional[str] = None


class RawTextAtsCheckPayload(BaseModel):
    text: str
    extracted_skills: Optional[List[str]] = []


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/parse", response_model=ParsedProfileResponse)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Upload a PDF or DOCX resume.
    Returns extracted skills, education, projects, matched competency IDs,
    AND comprehensive ATS scoring + AI content detection via Groq.
    """
    filename = file.filename or "upload.pdf"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Upload PDF, DOCX, or TXT.",
        )

    data = await file.read()
    if len(data) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    try:
        profile = parse_resume(filename, data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse resume: {e}")

    # Run ATS & AI detection analysis
    ats_data: Optional[Dict[str, Any]] = None
    try:
        ats_data = analyze_resume_ats(
            resume_text=profile.raw_text,
            extracted_skills=profile.technical_skills + profile.soft_skills
        )
    except Exception as e:
        # Failsafe fallback
        print(f"ATS analysis error: {e}")

    return ParsedProfileResponse(
        name=profile.name,
        education=profile.education,
        experience_summary=profile.experience_summary,
        technical_skills=profile.technical_skills,
        soft_skills=profile.soft_skills,
        projects=profile.projects,
        courses_certifications=profile.courses_certifications,
        matched_competency_ids=profile.matched_competency_ids,
        inferred_levels={str(k): v for k, v in profile.inferred_levels.items()},
        ats_analysis=ats_data,
    )


@router.post("/ats-check", response_model=AtsAnalysisResult)
async def ats_check_direct(payload: RawTextAtsCheckPayload):
    """
    Direct endpoint for ATS & AI detection analysis from raw resume text.
    """
    if not payload.text or len(payload.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Resume text is too short for analysis.")

    ats_data = analyze_resume_ats(
        resume_text=payload.text,
        extracted_skills=payload.extracted_skills or []
    )
    return ats_data


@router.post("/apply/{user_id}", status_code=200)
def apply_resume_to_user(
    user_id: int,
    payload: ApplyResumePayload,
    db: Session = Depends(get_db),
):
    """
    Persist the resume-inferred competency levels for a user.
    Also updates name and education if provided.
    Existing user competencies are updated (not duplicated).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.name:
        user.name = payload.name
    if payload.education:
        user.education = payload.education

    applied = 0
    for comp_id, level in payload.inferred_levels.items():
        comp = db.query(Competency).filter(Competency.id == comp_id).first()
        if not comp:
            continue
        existing = (
            db.query(UserCompetency)
            .filter(UserCompetency.user_id == user_id, UserCompetency.competency_id == comp_id)
            .first()
        )
        if existing:
            existing.current_level = max(existing.current_level, level)
            existing.evidence_source = "Resume upload"
        else:
            db.add(UserCompetency(
                user_id=user_id,
                competency_id=comp_id,
                current_level=level,
                evidence_source="Resume upload",
            ))
        applied += 1

    db.commit()
    return {"applied": applied, "user_id": user_id}
