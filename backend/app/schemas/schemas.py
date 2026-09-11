"""Pydantic v2 schemas for request/response validation."""

from __future__ import annotations
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Competency
# ---------------------------------------------------------------------------

class CompetencyBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    parent_id: Optional[int] = None
    taxonomy_source: Optional[str] = None
    taxonomy_id: Optional[str] = None


class CompetencyRead(CompetencyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------------
# Role
# ---------------------------------------------------------------------------

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    sector: str


class RoleRead(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RoleCompetencyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    competency_id: int
    required_level: int
    importance: float
    competency: CompetencyRead


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str
    education: Optional[str] = None
    department: Optional[str] = None
    experience: Optional[int] = None


class UserRead(UserCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserCompetencyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    competency_id: int
    current_level: int
    evidence_source: Optional[str] = None
    last_demonstrated: Optional[date] = None
    competency: CompetencyRead


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    provider: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None


class CourseRead(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------------
# Gap Engine output schemas
# ---------------------------------------------------------------------------

class CompetencyGap(BaseModel):
    """A single competency's gap breakdown."""
    competency_id: int
    competency_name: str
    category: str
    current_level: int
    required_level: int
    gap: int                      # max(required - current, 0)
    importance: float
    priority_score: float         # normalized_gap * importance
    evidence_source: Optional[str] = None


class GapAnalysisResult(BaseModel):
    """Full gap analysis for a user against a role."""
    user_id: int
    role_id: int
    role_name: str
    user_name: str
    gaps: List[CompetencyGap]     # sorted by priority_score desc
    covered_count: int            # competencies with gap == 0
    gap_count: int                # competencies with gap > 0
    readiness_score: float        # secondary metric only: 0-100


class CourseRecommendation(BaseModel):
    """A recommended course with explainable impact."""
    course: CourseRead
    impact_score: float
    gaps_addressed: List[str]     # competency names this course addresses
    gaps_addressed_count: int
    explanation: str


class CourseRecommendationResult(BaseModel):
    user_id: int
    role_id: int
    recommendations: List[CourseRecommendation]  # sorted by impact_score desc


# ---------------------------------------------------------------------------
# User competency upsert
# ---------------------------------------------------------------------------

class UserCompetencyUpsert(BaseModel):
    competency_id: int
    current_level: int = Field(ge=0, le=5)
    evidence_source: Optional[str] = None
    last_demonstrated: Optional[date] = None
