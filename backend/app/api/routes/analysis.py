"""
Gap analysis and course recommendation routes.

These are the core engine endpoints.
"""

from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.schemas import GapAnalysisResult, CourseRecommendationResult
from app.services.gap_service import get_gap_analysis, get_course_recommendations

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/gap", response_model=GapAnalysisResult)
def gap_analysis(
    user_id: int = Query(..., description="User ID"),
    role_id: int = Query(..., description="Target role ID"),
    db: Session = Depends(get_db),
):
    """
    Return a competency-by-competency gap profile for a user against a target role.

    The response is sorted by priority_score (highest gap × highest importance first).
    The readiness_score is a secondary metric — the primary output is the gaps list.
    """
    try:
        return get_gap_analysis(user_id, role_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/recommendations", response_model=CourseRecommendationResult)
def course_recommendations(
    user_id: int = Query(..., description="User ID"),
    role_id: int = Query(..., description="Target role ID"),
    top_n: int = Query(8, ge=1, le=20, description="Number of courses to return"),
    db: Session = Depends(get_db),
):
    """
    Rank courses by how much of the user's weighted competency gap they are likely to close.

    Each recommendation includes:
    - impact_score: deterministic gap-closure estimate
    - gaps_addressed: list of competency names covered
    - explanation: human-readable reason for the recommendation
    """
    try:
        return get_course_recommendations(user_id, role_id, db, top_n=top_n)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/semantic-match")
def semantic_match(
    query: str = Query(..., description="Free text to match against competencies"),
    top_k: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """
    Use sentence-transformer embeddings to find the most semantically similar
    competencies to a free-text query.

    This is a utility endpoint — NOT used for gap calculation.
    """
    from app.models.models import Competency
    from app.services.semantic import top_matches

    comps = db.query(Competency).all()
    names = [c.name for c in comps]
    ids = [c.id for c in comps]

    matches = top_matches(query, names, top_k=top_k)
    return [
        {"competency_id": ids[idx], "name": name, "score": round(score, 4)}
        for idx, name, score in matches
    ]
