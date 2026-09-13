"""SQLAlchemy ORM models for SkillGap Engine.

Tables:
  competencies          — canonical competency catalogue
  roles                 — job roles
  role_competencies     — role ↔ competency requirement mapping
  users                 — user profiles
  user_competencies     — user ↔ competency level evidence
  courses               — learning resources (used by gap engine)
  course_competencies   — course ↔ competency coverage
  skill_career_records  — Skillora "Skill Career Dataset" sheet (105 rows)
  skillora_resources    — Skillora "Learning Resources" sheet (paid + free per skill)
  company_job_refs      — Skillora "Company Job References" sheet (35 rows)
"""

from datetime import date
from typing import Optional
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Text,
    Float,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from datetime import datetime
from sqlalchemy.orm import relationship

from app.database.connection import Base


# ---------------------------------------------------------------------------
# Competency
# ---------------------------------------------------------------------------

class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("competencies.id"), nullable=True)
    taxonomy_source = Column(String(100), nullable=True)
    taxonomy_id = Column(String(100), nullable=True)

    children = relationship("Competency", backref="parent", remote_side=[id])
    role_competencies = relationship("RoleCompetency", back_populates="competency")
    user_competencies = relationship("UserCompetency", back_populates="competency")
    course_competencies = relationship("CourseCompetency", back_populates="competency")


# ---------------------------------------------------------------------------
# Role
# ---------------------------------------------------------------------------

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    sector = Column(String(100), nullable=False)

    role_competencies = relationship("RoleCompetency", back_populates="role")


class RoleCompetency(Base):
    __tablename__ = "role_competencies"
    __table_args__ = (
        UniqueConstraint("role_id", "competency_id", name="uq_role_competency"),
    )

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    required_level = Column(Integer, nullable=False)
    importance = Column(Float, nullable=False, default=1.0)

    role = relationship("Role", back_populates="role_competencies")
    competency = relationship("Competency", back_populates="role_competencies")


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    education = Column(String(200), nullable=True)
    department = Column(String(200), nullable=True)
    experience = Column(Integer, nullable=True)

    user_competencies = relationship("UserCompetency", back_populates="user")


class UserCompetency(Base):
<<<<<<< HEAD
    """Records a user's current competency level with evidence and verification."""
=======
>>>>>>> b6d616540781c1a28b1f39d1cecf61e27462cada
    __tablename__ = "user_competencies"
    __table_args__ = (
        UniqueConstraint("user_id", "competency_id", name="uq_user_competency"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
<<<<<<< HEAD

    # Estimated level from resume/profile analysis
    current_level = Column(Integer, nullable=False, default=0)  # 0-5

    # Verified level after assessment (if user takes assessment)
    verified_level = Column(Integer, nullable=True)  # 0-5, null if not verified

    # Evidence and confidence
    evidence = Column(Text, nullable=True)                     # e.g. "Implemented ML project using Python, Pandas, NumPy"
    evidence_source = Column(String(300), nullable=True)       # e.g. "resume_analysis", "assessment", "user_input"
    confidence = Column(Float, nullable=True, default=0.5)     # 0.0-1.0, how confident is the system

    # Verification tracking
    verification_status = Column(
        String(50),
        nullable=False,
        default="unverified"
    )  # unverified, needs_assessment, verified

=======
    current_level = Column(Integer, nullable=False, default=0)
    evidence_source = Column(String(300), nullable=True)
>>>>>>> b6d616540781c1a28b1f39d1cecf61e27462cada
    last_demonstrated = Column(Date, nullable=True)
    last_verified = Column(Date, nullable=True)

    # Assessment tracking
    assessment_score = Column(Float, nullable=True)  # 0-100
    assessment_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="user_competencies")
    competency = relationship("Competency", back_populates="user_competencies")


# ---------------------------------------------------------------------------
# Course  (used by gap engine for recommendations)
# ---------------------------------------------------------------------------

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    provider = Column(String(200), nullable=True)
    duration = Column(String(100), nullable=True)
    level = Column(String(50), nullable=True)
    source = Column(String(100), nullable=True)
    source_url = Column(String(500), nullable=True)

    course_competencies = relationship("CourseCompetency", back_populates="course")


class CourseCompetency(Base):
    __tablename__ = "course_competencies"
    __table_args__ = (
        UniqueConstraint("course_id", "competency_id", name="uq_course_competency"),
    )

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    coverage_level = Column(Integer, nullable=False, default=1)

    course = relationship("Course", back_populates="course_competencies")
    competency = relationship("Competency", back_populates="course_competencies")


# ---------------------------------------------------------------------------
# SkillCareerRecord  — Skillora "Skill Career Dataset" sheet (105 rows)
# Each row = one skill ↔ role pairing with salary, demand, career info
# ---------------------------------------------------------------------------

class SkillCareerRecord(Base):
    """
    Direct representation of the Skillora Skill Career Dataset.
    One row per skill-to-role mapping (105 total).
    """
    __tablename__ = "skill_career_records"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(String(20), nullable=False, index=True)   # e.g. "SKL0001"
    skill_name = Column(String(200), nullable=False, index=True)
    skill_category = Column(String(100), nullable=False)
    suitable_job_role = Column(String(200), nullable=False, index=True)
    role_description = Column(Text, nullable=True)
    primary_required_skill = Column(String(200), nullable=True)
    recommended_supporting_skills = Column(Text, nullable=True)  # comma-separated
    experience_level = Column(String(100), nullable=True)         # "Entry Level: 0–2 years"
    experience_range = Column(String(50), nullable=True)          # "0–2 years"
    salary_min_lpa = Column(Float, nullable=True)                 # India INR LPA
    salary_max_lpa = Column(Float, nullable=True)
    salary_basis = Column(Text, nullable=True)
    learning_duration = Column(Text, nullable=True)
    working_duration = Column(String(200), nullable=True)
    work_mode = Column(String(200), nullable=True)
    job_demand = Column(String(100), nullable=True)               # "Medium to High"
    career_growth = Column(String(200), nullable=True)
    education_background = Column(Text, nullable=True)
    suitable_industry = Column(String(200), nullable=True)
    suggested_portfolio_project = Column(Text, nullable=True)
    skill_match_logic = Column(Text, nullable=True)
    missing_skill_recommendation = Column(Text, nullable=True)
    dataset_notes = Column(Text, nullable=True)

    # FK to canonical competency (nullable — resolved by normalization)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=True)


# ---------------------------------------------------------------------------
# SkilloraResource  — Skillora "Learning Resources" sheet
# Up to 4 paid + 4 free resources per skill
# ---------------------------------------------------------------------------

class SkilloraResource(Base):
    """
    Direct representation of the Skillora Learning Resources sheet.
    Each row = one learning resource for a given skill.
    """
    __tablename__ = "skillora_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(200), nullable=False, index=True)
    roles = Column(Text, nullable=True)            # semicolon-separated role names
    platform = Column(String(200), nullable=False)
    course_title = Column(String(400), nullable=False)
    course_url = Column(String(1000), nullable=False)
    is_free = Column(Boolean, nullable=False, default=False)  # True=free, False=paid
    slot_number = Column(Integer, nullable=False)  # 1-4 within paid or free group

    # FK to canonical competency
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=True)


# ---------------------------------------------------------------------------
# CompanyJobReference  — Skillora "Company Job References" sheet (35 rows)
# ---------------------------------------------------------------------------

class CompanyJobReference(Base):
    """
    Direct representation of the Skillora Company Job References sheet.
    """
    __tablename__ = "company_job_refs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)    # "Software" or "Hardware"
    serial_number = Column(Integer, nullable=False)
    company_name = Column(String(200), nullable=False, index=True)
    about_role = Column(Text, nullable=True)
    required_skills = Column(Text, nullable=True)    # comma-separated
    working_duration = Column(String(200), nullable=True)
    application_link = Column(String(1000), nullable=True)
