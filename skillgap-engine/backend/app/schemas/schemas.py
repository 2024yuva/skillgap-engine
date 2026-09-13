"""Pydantic v2 schemas for request/response validation."""

from __future__ import annotations
from datetime import date
from typing import Optional, List, Literal
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
# Competency Classification — user-facing status
# ---------------------------------------------------------------------------

# The five user-facing classifications (never expose raw numbers as primary UI)
CompetencyStatus = Literal[
    "strong_match",        # gap == 0, level >= required
    "related",             # user has a related/transferable skill
    "needs_verification",  # some evidence, can't confirm proficiency
    "needs_development",   # evidence exists but level below required
    "missing",             # no evidence found in user profile
]


class CompetencyGap(BaseModel):
<<<<<<< HEAD
    """A single competency's gap breakdown with user-friendly classification."""
=======
    """A single competency's gap breakdown — includes user-facing classification."""
>>>>>>> b6d616540781c1a28b1f39d1cecf61e27462cada
    competency_id: int
    competency_name: str
    category: str
    current_level: int
    required_level: int
    gap: int                          # max(required - current, 0)  — kept internally
    importance: float
<<<<<<< HEAD
    priority_score: float         # normalized_gap * importance (internal use)

    # Evidence and confidence
    evidence: Optional[str] = None                 # e.g. "Implemented ML project using Python, Pandas, NumPy"
    evidence_source: Optional[str] = None          # e.g. "resume_analysis"
    confidence: float = 0.5                        # 0.0-1.0: system confidence in the assessment

    # User-facing classification
    classification: str                            # strong_match, related, needs_verification, needs_development, missing_evidence
    explanation: str                               # Human-readable reason for classification
    verification_status: str                       # unverified, needs_assessment, verified
=======
    priority_score: float             # kept for internal ranking, not primary UI
    evidence_source: Optional[str] = None
    # ── User-facing fields ──────────────────────────────────────────────────
    status: CompetencyStatus = "missing"
    status_label: str = "Missing Evidence"
    status_reason: str = ""           # plain-English explanation of WHY
    related_skill_name: Optional[str] = None   # name of the related skill found
    confidence: float = 0.0           # 0.0–1.0, how confident we are in the status
    action_label: str = ""            # e.g. "Take Assessment", "View Resources"
    evidence_bullets: List[str] = Field(default_factory=list)  # what the system found
>>>>>>> b6d616540781c1a28b1f39d1cecf61e27462cada


class GapAnalysisResult(BaseModel):
    """Full gap analysis for a user against a role."""
    user_id: int
    role_id: int
    role_name: str
    user_name: str
    gaps: List[CompetencyGap]         # sorted by priority_score desc
    covered_count: int                # competencies with gap == 0
    gap_count: int                    # competencies with gap > 0
    readiness_score: float            # secondary metric only: 0-100
    # Counts by status for dashboard summary
    strong_match_count: int = 0
    related_count: int = 0
    needs_verification_count: int = 0
    needs_development_count: int = 0
    missing_count: int = 0


class CourseRecommendation(BaseModel):
    """A recommended course with explainable impact."""
    course: CourseRead
    impact_score: float
    gaps_addressed: List[str]         # competency names this course addresses
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


# ---------------------------------------------------------------------------
# Assessment schemas
# ---------------------------------------------------------------------------

class AssessmentQuestion(BaseModel):
    id: int
    topic: str
    question_text: str
    question_type: Literal["mcq", "trace", "complexity"]
    options: Optional[List[str]] = None       # for MCQ
    correct_answer: str
    explanation: str
    difficulty: Literal["easy", "medium", "hard"]


class AssessmentSubmission(BaseModel):
    user_id: int
    competency_id: int
    answers: dict[int, str]    # question_id -> user's answer


class TopicResult(BaseModel):
    topic: str
    score: int          # 0-100
    label: str          # "Strong" | "Intermediate" | "Beginner"
    questions_attempted: int
    questions_correct: int


class AssessmentResult(BaseModel):
    user_id: int
    competency_id: int
    competency_name: str
    overall_score: int      # 0-100
    verified_level: int     # 0-5 mapped from score
    topic_results: List[TopicResult]
    summary: str
    strongest_topics: List[str]
    development_areas: List[str]
