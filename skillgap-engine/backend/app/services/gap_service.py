"""
Gap service — bridges the SQLAlchemy ORM layer and the deterministic gap engine.

Responsibilities:
- Load role requirements and user competency levels from the DB.
- Apply skill normalization (SKILL_NORMALIZATION_MAP).
- Apply related-skill map (RELATED_SKILLS).
- Call engine functions.
<<<<<<< HEAD
- Classify competencies using user-friendly categories.
- Convert engine output back to Pydantic response schemas.
=======
- Convert engine output back to Pydantic response schemas, including
  user-facing classification fields.
>>>>>>> b6d616540781c1a28b1f39d1cecf61e27462cada
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
from app.services.classification import classify_competency
from app.schemas.schemas import (
    GapAnalysisResult, CompetencyGap,
    CourseRecommendationResult, CourseRecommendation, CourseRead,
)
from app.ingestion.seed_data import RELATED_SKILLS


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


def _load_user_competency_details(user_id: int, db: Session) -> dict:
    """Load full UserCompetency details including evidence, confidence, verification."""
    rows = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == user_id)
        .all()
    )
    return {
        uc.competency_id: {
            "evidence": uc.evidence,
            "evidence_source": uc.evidence_source,
            "confidence": uc.confidence or 0.5,
            "verification_status": uc.verification_status or "unverified",
            "verified_level": uc.verified_level,
            "assessment_score": uc.assessment_score,
        }
        for uc in rows
    }


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
    user_details = _load_user_competency_details(user_id, db)

    gap_rows = analyse_gaps(
        requirements, user_levels, comp_map,
        related_skills_map=RELATED_SKILLS,
    )
    readiness = compute_readiness_score(gap_rows)

    gaps: List[CompetencyGap] = []
    for g in gap_rows:
        gaps.append(CompetencyGap(
            competency_id=g.competency_id,
            competency_name=g.competency_name,
            category=g.category,
            current_level=g.current_level,
            required_level=g.required_level,
            gap=g.gap,
            importance=g.importance,
            priority_score=round(g.priority_score, 4),
            evidence=user_details.get(g.competency_id, {}).get("evidence"),
            evidence_source=g.evidence_source,
<<<<<<< HEAD
            confidence=user_details.get(g.competency_id, {}).get("confidence", 0.5),
            classification=(
                classify_competency(
                    competency_id=g.competency_id,
                    competency_name=g.competency_name,
                    category=g.category,
                    current_level=g.current_level,
                    required_level=g.required_level,
                    gap=g.gap,
                    importance=g.importance,
                    priority_score=g.priority_score,
                    evidence=user_details.get(g.competency_id, {}).get("evidence"),
                    evidence_source=g.evidence_source,
                    confidence=user_details.get(g.competency_id, {}).get("confidence", 0.5),
                    verification_status=user_details.get(g.competency_id, {}).get("verification_status", "unverified"),
                    verified_level=user_details.get(g.competency_id, {}).get("verified_level"),
                    assessment_score=user_details.get(g.competency_id, {}).get("assessment_score"),
                ).classification.value
            ),
            explanation=(
                classify_competency(
                    competency_id=g.competency_id,
                    competency_name=g.competency_name,
                    category=g.category,
                    current_level=g.current_level,
                    required_level=g.required_level,
                    gap=g.gap,
                    importance=g.importance,
                    priority_score=g.priority_score,
                    evidence=user_details.get(g.competency_id, {}).get("evidence"),
                    evidence_source=g.evidence_source,
                    confidence=user_details.get(g.competency_id, {}).get("confidence", 0.5),
                    verification_status=user_details.get(g.competency_id, {}).get("verification_status", "unverified"),
                    verified_level=user_details.get(g.competency_id, {}).get("verified_level"),
                    assessment_score=user_details.get(g.competency_id, {}).get("assessment_score"),
                ).explanation
            ),
            verification_status=user_details.get(g.competency_id, {}).get("verification_status", "unverified"),
        )
        for g in gap_rows
    ]
=======
            # User-facing classification fields
            status=g.status,
            status_label=g.status_label,
            status_reason=g.status_reason,
            related_skill_name=g.related_skill_name,
            confidence=round(g.confidence, 3),
            action_label=g.action_label,
            evidence_bullets=g.evidence_bullets,
        ))

    # Status counts for dashboard summary
    strong   = sum(1 for g in gap_rows if g.status == "strong_match")
    related  = sum(1 for g in gap_rows if g.status == "related")
    verify   = sum(1 for g in gap_rows if g.status == "needs_verification")
    develop  = sum(1 for g in gap_rows if g.status == "needs_development")
    missing  = sum(1 for g in gap_rows if g.status == "missing")
>>>>>>> b6d616540781c1a28b1f39d1cecf61e27462cada

    return GapAnalysisResult(
        user_id=user_id,
        role_id=role_id,
        role_name=role.name,
        user_name=user.name,
        gaps=gaps,
        covered_count=sum(1 for g in gap_rows if g.gap == 0),
        gap_count=sum(1 for g in gap_rows if g.gap > 0),
        readiness_score=readiness,
        strong_match_count=strong,
        related_count=related,
        needs_verification_count=verify,
        needs_development_count=develop,
        missing_count=missing,
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

    gap_rows = analyse_gaps(
        requirements, user_levels, comp_map,
        related_skills_map=RELATED_SKILLS,
    )
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
        if ci.impact_score > 0
    ]

    return CourseRecommendationResult(
        user_id=user_id,
        role_id=role_id,
        recommendations=recommendations,
    )


def get_role_matches(user_id: int, db: Session) -> list[dict]:
    """
    Calculate match scores for all target roles in DB for a user.
    Returns list of role match objects sorted from highest match score to lowest.
    """
    from app.models.models import Role, RoleCompetency, UserCompetency
    
    roles = db.query(Role).all()
    user_comps = db.query(UserCompetency).filter(UserCompetency.user_id == user_id).all()
    user_level_map = {uc.competency_id: uc.current_level for uc in user_comps}
    
    comp_map = _load_competency_map(db)

    results = []
    for r in roles:
        reqs = db.query(RoleCompetency).filter(RoleCompetency.role_id == r.id).all()
        if not reqs:
            results.append({
                "id": r.id, "name": r.name, "sector": r.sector, "description": r.description,
                "match_score": 0, "matched_count": 0, "total_required": 0,
                "matched_skills": [], "missing_skills": [],
            })
            continue

        total_max = sum(rq.required_level for rq in reqs)
        achieved = sum(min(user_level_map.get(rq.competency_id, 0), rq.required_level) for rq in reqs)
        
        matched_names = []
        missing_names = []
        for rq in reqs:
            cname = comp_map[rq.competency_id].name if rq.competency_id in comp_map else f"Skill #{rq.competency_id}"
            user_l = user_level_map.get(rq.competency_id, 0)
            if user_l > 0:
                matched_names.append(cname)
            else:
                rel_ids = RELATED_SKILLS.get(rq.competency_id, [])
                has_rel = any(user_level_map.get(rid, 0) > 0 for rid in rel_ids)
                if has_rel:
                    rel_name = comp_map[next(rid for rid in rel_ids if user_level_map.get(rid, 0) > 0)].name
                    matched_names.append(f"{cname} (via {rel_name})")
                else:
                    missing_names.append(cname)

        match_score = round((achieved / total_max) * 100) if total_max > 0 else 0

        results.append({
            "id": r.id,
            "name": r.name,
            "sector": r.sector,
            "description": r.description,
            "match_score": match_score,
            "matched_count": len(matched_names),
            "total_required": len(reqs),
            "matched_skills": matched_names,
            "missing_skills": missing_names,
        })

    # Sort descending by match_score
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results



def get_company_job_matches(user_id: int, db: Session) -> list[dict]:
    """
    Match user's skills against all 35 COMPANY_JOB_REFS in seed_data.py.
    Returns company job references sorted from highest match to lowest.
    """
    from app.ingestion.seed_data import COMPANY_JOB_REFS, SKILL_NORMALIZATION_MAP
    from app.models.models import UserCompetency

    user_comps = db.query(UserCompetency).filter(UserCompetency.user_id == user_id).all()
    user_comp_ids = {uc.competency_id for uc in user_comps if uc.current_level > 0}
    comp_map = _load_competency_map(db)
    user_skill_names = {comp_map[cid].name.lower() for cid in user_comp_ids if cid in comp_map}

    company_matches = []
    for ref in COMPANY_JOB_REFS:
        req_str = ref["required_skills"]
        # Split skills by comma or slash
        req_tokens = [s.strip() for s in req_str.replace("/", ",").split(",") if s.strip()]
        
        matched_tokens = []
        missing_tokens = []
        
        for tok in req_tokens:
            tok_lower = tok.lower()
            # Check direct match or via normalization map
            cid = SKILL_NORMALIZATION_MAP.get(tok_lower)
            if cid and cid in user_comp_ids:
                matched_tokens.append(tok)
            elif any(u_skill in tok_lower or tok_lower in u_skill for u_skill in user_skill_names):
                matched_tokens.append(tok)
            else:
                missing_tokens.append(tok)

        total_skills = len(req_tokens)
        match_score = round((len(matched_tokens) / total_skills) * 100) if total_skills > 0 else 0

        # Baseline salary estimate based on software vs hardware category
        salary_lpa = "5 - 14 LPA" if ref["category"] == "Software" else "4 - 12 LPA"

        company_matches.append({
            "company_name": ref["company_name"],
            "about_role": ref["about_role"],
            "category": ref["category"],
            "required_skills": ref["required_skills"],
            "matched_skills": matched_tokens,
            "missing_skills": missing_tokens,
            "match_score": match_score,
            "working_duration": ref["working_duration"],
            "application_link": ref["application_link"],
            "salary_lpa": salary_lpa,
        })

    company_matches.sort(key=lambda x: x["match_score"], reverse=True)
    return company_matches

