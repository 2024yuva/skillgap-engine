"""SQLAlchemy ORM models for SkillGap Engine."""

from datetime import date, datetime
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
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
    category = Column(String(100), nullable=False)          # e.g. "Technical", "Analytical"
    parent_id = Column(Integer, ForeignKey("competencies.id"), nullable=True)
    taxonomy_source = Column(String(100), nullable=True)    # e.g. "NSQF", "O*NET"
    taxonomy_id = Column(String(100), nullable=True)

    # relationships
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
    sector = Column(String(100), nullable=False)   # e.g. "IT", "Electrical", "Statistics"

    role_competencies = relationship("RoleCompetency", back_populates="role")


class RoleCompetency(Base):
    """Maps a role to the competencies it requires, with level and importance."""
    __tablename__ = "role_competencies"
    __table_args__ = (
        UniqueConstraint("role_id", "competency_id", name="uq_role_competency"),
    )

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    required_level = Column(
        Integer, nullable=False,
        # 0-5 scale
    )
    importance = Column(Float, nullable=False, default=1.0)  # 0.0 – 1.0 weight

    role = relationship("Role", back_populates="role_competencies")
    competency = relationship("Competency", back_populates="role_competencies")


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    education = Column(String(200), nullable=True)   # e.g. "B.Tech EEE"
    department = Column(String(200), nullable=True)  # e.g. "Electrical Engineering"
    experience = Column(Integer, nullable=True)      # years

    user_competencies = relationship("UserCompetency", back_populates="user")


class UserCompetency(Base):
    """Records a user's current competency level with evidence."""
    __tablename__ = "user_competencies"
    __table_args__ = (
        UniqueConstraint("user_id", "competency_id", name="uq_user_competency"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    current_level = Column(Integer, nullable=False, default=0)  # 0-5
    evidence_source = Column(String(300), nullable=True)        # e.g. "NPTEL certificate"
    last_demonstrated = Column(Date, nullable=True)

    user = relationship("User", back_populates="user_competencies")
    competency = relationship("Competency", back_populates="user_competencies")


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    provider = Column(String(200), nullable=True)   # e.g. "NPTEL", "Coursera"
    duration = Column(String(100), nullable=True)   # e.g. "12 weeks"
    level = Column(String(50), nullable=True)       # beginner / intermediate / advanced
    source = Column(String(100), nullable=True)     # e.g. "NPTEL", "Swayam"
    source_url = Column(String(500), nullable=True)

    course_competencies = relationship("CourseCompetency", back_populates="course")


class CourseCompetency(Base):
    """Maps a course to the competencies it covers and at what coverage level."""
    __tablename__ = "course_competencies"
    __table_args__ = (
        UniqueConstraint("course_id", "competency_id", name="uq_course_competency"),
    )

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    coverage_level = Column(Integer, nullable=False, default=1)  # 1-5: how deeply the course addresses this competency

    course = relationship("Course", back_populates="course_competencies")
    competency = relationship("Competency", back_populates="course_competencies")


# ---------------------------------------------------------------------------
# Assessment
# ---------------------------------------------------------------------------

class AssessmentAttempt(Base):
    """Persisted DSA Skill Assessment attempt (adaptive session + results)."""

    __tablename__ = "assessment_attempts"

    id = Column(String(36), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    assessment_type = Column(String(50), nullable=False, default="dsa")
    status = Column(String(30), nullable=False, default="in_progress")
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    questions_asked = Column(Integer, nullable=False, default=0)
    overall_level = Column(Integer, nullable=True)
    overall_label = Column(String(50), nullable=True)
    topic_results = Column(Text, nullable=True)
    next_steps = Column(Text, nullable=True)
    biggest_gaps = Column(Text, nullable=True)
    session_blob = Column(Text, nullable=True)
    early_stop = Column(Boolean, nullable=False, default=False)
    applied = Column(Boolean, nullable=False, default=False)
