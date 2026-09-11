"""
Resume upload and parsing endpoint.

POST /api/v1/resume/parse
  - Accepts PDF or DOCX upload (multipart/form-data)
  - Returns extracted profile + matched competency IDs + inferred levels

POST /api/v1/resume/apply/{user_id}
  - Takes parsed result and writes UserCompetency rows for the user
"""

from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.services.resume_parser import parse_resume
from app.models.models import User, UserCompetency, Competency

router = APIRouter(prefix="/resume", tags=["resume"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


class ParsedProfileResponse(BaseModel):
    name: Optional[str]
    education: str
    experience_summary: str
    technical_skills: list[str]
    soft_skills: list[str]
    projects: list[str]
    courses_certifications: list[str]
    matched_competency_ids: list[int]
    inferred_levels: dict[str, int]   # competency_id (str key for JSON) -> level


class ApplyResumePayload(BaseModel):
    inferred_levels: dict[int, int]   # competency_id -> level
    name: Optional[str] = None
    education: Optional[str] = None


@router.post("/parse", response_model=ParsedProfileResponse)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Upload a PDF or DOCX resume.
    Returns extracted skills, education, projects, and matched competency IDs.
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
    )


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
