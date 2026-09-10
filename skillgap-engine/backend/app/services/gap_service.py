"""
Gap service — bridges the SQLAlchemy ORM layer and the deterministic gap engine.

Responsibilities:
- Load role requirements and user competency levels from the DB.
- Convert ORM rows to engine dataclasses.
- Call engine functions.
- Convert engine output back to Pydantic response schemas.
"""

from __future__ import annotations
from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models.models import (
    Role, RoleCompetency, UserCompetency, Course, CourseCompetency, Competency,
)
from app.engine.gap_engine import (
    CompetencyNode, RoleRequirement, UserLevel, CourseNode,
    analyse_gaps, compute_readiness_score, rank_courses,
)
from app.schemas.schemas import (
    GapAnalysisResult, CompetencyGap,
    CourseRecommendationResult, CourseRecommendation, CourseRead,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_competency_map(db: Session) -> dict[int, CompetencyNode]:
    rows = db.query(Competency).all()
    return {c.id: CompetencyNode(id=c.id, name=c.name, category=c.category) for c in rows}


def _load_role_requirements(role_id: int, db: Session) -> list[RoleRequirement]:
    rows = (
        db.query(RoleCompetency)
        .filter(RoleCompetency.role_id == role_id)
        .all()
    )
    return [
        RoleRequirement(
            competency_id=r.competency_id,
            required_level=r.required_level,
            importance=r.importance,
        )
        for r in rows
    ]


def _load_user_levels(user_id: int, db: Session) -> list[UserLevel]:
    rows = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == user_id)
        .all()
    )
    return [
        UserLevel(
            competency_id=uc.competency_id,
            current_level=uc.current_level,
            evidence_source=uc.evidence_source,
        )
        for uc in rows
    ]


def _load_courses(db: Session) -> list[CourseNode]:
    courses = (
        db.query(Course)
        .options(joinedload(Course.course_competencies))
        .all()
    )
    nodes = []
    for c in courses:
        coverage = {cc.competency_id: cc.coverage_level for cc in c.course_competencies}
        nodes.append(CourseNode(
            id=c.id,
            title=c.title,
            description=c.description or "",
            provider=c.provider or "",
            duration=c.duration or "",
            level=c.level or "",
            source=c.source or "",
            source_url=c.source_url or "",
            coverage=coverage,
        ))
    return nodes


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_gap_analysis(user_id: int, role_id: int, db: Session) -> GapAnalysisResult:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise ValueError(f"Role {role_id} not found")

    from app.models.models import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User {user_id} not found")

    comp_map = _load_competency_map(db)
    requirements = _load_role_requirements(role_id, db)
    user_levels = _load_user_levels(user_id, db)

    gap_rows = analyse_gaps(requirements, user_levels, comp_map)
    readiness = compute_readiness_score(gap_rows)

    gaps = [
        CompetencyGap(
            competency_id=g.competency_id,
            competency_name=g.competency_name,
            category=g.category,
            current_level=g.current_level,
            required_level=g.required_level,
            gap=g.gap,
            importance=g.importance,
            priority_score=round(g.priority_score, 4),
            evidence_source=g.evidence_source,
        )
        for g in gap_rows
    ]

    return GapAnalysisResult(
        user_id=user_id,
        role_id=role_id,
        role_name=role.name,
        user_name=user.name,
        gaps=gaps,
        covered_count=sum(1 for g in gap_rows if g.gap == 0),
        gap_count=sum(1 for g in gap_rows if g.gap > 0),
        readiness_score=readiness,
    )


def get_course_recommendations(
    user_id: int,
    role_id: int,
    db: Session,
    top_n: int = 8,
) -> CourseRecommendationResult:
    comp_map = _load_competency_map(db)
    requirements = _load_role_requirements(role_id, db)
    user_levels = _load_user_levels(user_id, db)
    courses = _load_courses(db)

    gap_rows = analyse_gaps(requirements, user_levels, comp_map)
    ranked = rank_courses(courses, gap_rows, comp_map, top_n=top_n)

    recommendations = [
        CourseRecommendation(
            course=CourseRead(
                id=ci.course.id,
                title=ci.course.title,
                description=ci.course.description,
                provider=ci.course.provider,
                duration=ci.course.duration,
                level=ci.course.level,
                source=ci.course.source,
                source_url=ci.course.source_url,
            ),
            impact_score=ci.impact_score,
            gaps_addressed=ci.gaps_addressed,
            gaps_addressed_count=len(ci.gaps_addressed),
            explanation=ci.explanation,
        )
        for ci in ranked
        if ci.impact_score > 0  # filter out completely irrelevant courses
    ]

    return CourseRecommendationResult(
        user_id=user_id,
        role_id=role_id,
        recommendations=recommendations,
    )
