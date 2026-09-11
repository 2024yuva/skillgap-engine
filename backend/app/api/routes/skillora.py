"""
Skillora dataset routes.

Exposes the three Skillora Excel sheets via REST:
  GET /skillora/career-records        — Skill Career Dataset (105 rows)
  GET /skillora/career-records/{id}
  GET /skillora/resources             — Learning Resources (paid + free per skill)
  GET /skillora/jobs                  — Company Job References (35 rows)
  GET /skillora/jobs/{id}
"""

from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.database.connection import get_db
from app.models.models import SkillCareerRecord, SkilloraResource, CompanyJobReference

router = APIRouter(prefix="/skillora", tags=["skillora-dataset"])


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class SkillCareerRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    skill_id: str
    skill_name: str
    skill_category: str
    suitable_job_role: str
    role_description: Optional[str]
    primary_required_skill: Optional[str]
    recommended_supporting_skills: Optional[str]
    experience_level: Optional[str]
    experience_range: Optional[str]
    salary_min_lpa: Optional[float]
    salary_max_lpa: Optional[float]
    salary_basis: Optional[str]
    learning_duration: Optional[str]
    working_duration: Optional[str]
    work_mode: Optional[str]
    job_demand: Optional[str]
    career_growth: Optional[str]
    education_background: Optional[str]
    suitable_industry: Optional[str]
    suggested_portfolio_project: Optional[str]
    skill_match_logic: Optional[str]
    missing_skill_recommendation: Optional[str]
    competency_id: Optional[int]


class SkilloraResourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    skill_name: str
    roles: Optional[str]
    platform: str
    course_title: str
    course_url: str
    is_free: bool
    slot_number: int
    competency_id: Optional[int]


class CompanyJobRefRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category: str
    serial_number: int
    company_name: str
    about_role: Optional[str]
    required_skills: Optional[str]
    working_duration: Optional[str]
    application_link: Optional[str]


# ---------------------------------------------------------------------------
# Skill Career Dataset
# ---------------------------------------------------------------------------

@router.get("/career-records", response_model=List[SkillCareerRecordRead])
def list_career_records(
    skill_name: Optional[str] = Query(None, description="Filter by skill name (case-insensitive)"),
    role: Optional[str] = Query(None, description="Filter by job role (case-insensitive)"),
    category: Optional[str] = Query(None, description="Filter by skill category"),
    db: Session = Depends(get_db),
):
    """
    Return all 105 Skillora Skill Career Dataset records.
    Optionally filter by skill_name, role, or category.
    """
    q = db.query(SkillCareerRecord)
    if skill_name:
        q = q.filter(SkillCareerRecord.skill_name.ilike(f"%{skill_name}%"))
    if role:
        q = q.filter(SkillCareerRecord.suitable_job_role.ilike(f"%{role}%"))
    if category:
        q = q.filter(SkillCareerRecord.skill_category.ilike(f"%{category}%"))
    return q.order_by(SkillCareerRecord.skill_id).all()


@router.get("/career-records/{record_id}", response_model=SkillCareerRecordRead)
def get_career_record(record_id: int, db: Session = Depends(get_db)):
    rec = db.query(SkillCareerRecord).filter(SkillCareerRecord.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail=f"Career record {record_id} not found")
    return rec


# ---------------------------------------------------------------------------
# Learning Resources
# ---------------------------------------------------------------------------

@router.get("/resources", response_model=List[SkilloraResourceRead])
def list_resources(
    skill_name: Optional[str] = Query(None, description="Filter by skill name"),
    is_free: Optional[bool] = Query(None, description="True = free only, False = paid only"),
    competency_id: Optional[int] = Query(None, description="Filter by competency ID"),
    db: Session = Depends(get_db),
):
    """
    Return Skillora learning resources (4 paid + 4 free per skill).
    """
    q = db.query(SkilloraResource)
    if skill_name:
        q = q.filter(SkilloraResource.skill_name.ilike(f"%{skill_name}%"))
    if is_free is not None:
        q = q.filter(SkilloraResource.is_free == is_free)
    if competency_id is not None:
        q = q.filter(SkilloraResource.competency_id == competency_id)
    return q.order_by(SkilloraResource.skill_name, SkilloraResource.is_free, SkilloraResource.slot_number).all()


# ---------------------------------------------------------------------------
# Company Job References
# ---------------------------------------------------------------------------

@router.get("/jobs", response_model=List[CompanyJobRefRead])
def list_jobs(
    category: Optional[str] = Query(None, description="'Software' or 'Hardware'"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    db: Session = Depends(get_db),
):
    """Return all 35 company job references from the Skillora dataset."""
    q = db.query(CompanyJobReference)
    if category:
        q = q.filter(CompanyJobReference.category.ilike(f"%{category}%"))
    if company:
        q = q.filter(CompanyJobReference.company_name.ilike(f"%{company}%"))
    return q.order_by(CompanyJobReference.category, CompanyJobReference.serial_number).all()


@router.get("/jobs/{job_id}", response_model=CompanyJobRefRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(CompanyJobReference).filter(CompanyJobReference.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job reference {job_id} not found")
    return job
