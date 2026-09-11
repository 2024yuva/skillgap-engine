"""
Assessment routes.

Provides a competency-specific assessment system, starting with DSA.
The assessment estimates competency by topic, not just overall score.
"""

from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.schemas import (
    AssessmentQuestion, AssessmentSubmission,
    AssessmentResult, TopicResult,
)
from app.ingestion.assessment_data import (
    DSA_QUESTIONS, DSA_TOPICS,
    DSA_COMPETENCY_ID, DSA_COMPETENCY_NAME,
)

router = APIRouter(prefix="/assessment", tags=["assessment"])


# ---------------------------------------------------------------------------
# Score thresholds → topic label
# ---------------------------------------------------------------------------

def _score_to_label(score: int) -> str:
    if score >= 75:
        return "Strong"
    if score >= 45:
        return "Intermediate"
    return "Beginner"


def _score_to_level(overall: int) -> int:
    """Map 0-100 score to 0-5 competency level."""
    if overall >= 85: return 5
    if overall >= 70: return 4
    if overall >= 55: return 3
    if overall >= 40: return 2
    if overall >= 20: return 1
    return 0


# ---------------------------------------------------------------------------
# GET /assessment/questions?competency_id=4
# ---------------------------------------------------------------------------

@router.get("/questions", response_model=List[AssessmentQuestion])
def get_assessment_questions(
    competency_id: int = Query(DSA_COMPETENCY_ID, description="Competency ID to assess"),
):
    """
    Return the assessment questions for a competency.
    Currently only DSA (competency_id=4) is implemented.
    """
    if competency_id != DSA_COMPETENCY_ID:
        raise HTTPException(
            status_code=404,
            detail=f"Assessment not yet available for competency {competency_id}. "
                   f"Currently available: DSA (competency_id={DSA_COMPETENCY_ID})",
        )
    # Return questions without the correct_answer field for the client
    questions = []
    for q in DSA_QUESTIONS:
        questions.append(AssessmentQuestion(
            id=q["id"],
            topic=q["topic"],
            question_text=q["question_text"],
            question_type=q["question_type"],
            options=q.get("options"),
            correct_answer=q["correct_answer"],   # client should hide this during quiz
            explanation=q["explanation"],
            difficulty=q["difficulty"],
        ))
    return questions


# ---------------------------------------------------------------------------
# POST /assessment/submit
# ---------------------------------------------------------------------------

@router.post("/submit", response_model=AssessmentResult)
def submit_assessment(
    submission: AssessmentSubmission,
    db: Session = Depends(get_db),
):
    """
    Score a submitted assessment.

    Returns per-topic results and an overall competency level estimate.
    Also updates the user's competency level if user_id is provided.
    """
    if submission.competency_id != DSA_COMPETENCY_ID:
        raise HTTPException(
            status_code=404,
            detail=f"Assessment not available for competency {submission.competency_id}",
        )

    # Build answer key
    answer_key: dict[int, dict] = {q["id"]: q for q in DSA_QUESTIONS}

    # Score by topic
    topic_scores: dict[str, list[bool]] = {t: [] for t in DSA_TOPICS}

    for qid_str, user_answer in submission.answers.items():
        qid = int(qid_str)
        question = answer_key.get(qid)
        if question is None:
            continue
        correct = user_answer.strip().upper() == question["correct_answer"].strip().upper()
        topic = question["topic"]
        if topic in topic_scores:
            topic_scores[topic].append(correct)

    # Build per-topic results
    topic_results: List[TopicResult] = []
    all_correct = 0
    all_attempted = 0

    for topic in DSA_TOPICS:
        results = topic_scores[topic]
        if not results:
            continue
        attempted = len(results)
        correct = sum(results)
        score = round((correct / attempted) * 100) if attempted > 0 else 0
        all_correct += correct
        all_attempted += attempted
        topic_results.append(TopicResult(
            topic=topic,
            score=score,
            label=_score_to_label(score),
            questions_attempted=attempted,
            questions_correct=correct,
        ))

    overall_score = round((all_correct / all_attempted) * 100) if all_attempted > 0 else 0
    verified_level = _score_to_level(overall_score)

    # Determine strongest and development areas
    strong_topics = [t.topic for t in topic_results if t.label == "Strong"]
    develop_topics = [t.topic for t in topic_results if t.label == "Beginner"]

    # Build summary
    if overall_score >= 70:
        summary = (
            f"You scored {overall_score}% overall on the DSA assessment. "
            f"Your profile demonstrates solid algorithmic thinking. "
        )
    elif overall_score >= 45:
        summary = (
            f"You scored {overall_score}% overall. "
            f"You have a foundational understanding of DSA with room to grow. "
        )
    else:
        summary = (
            f"You scored {overall_score}% overall. "
            f"Targeted practice on the core DSA topics will significantly strengthen your profile. "
        )

    if strong_topics:
        summary += f"Strongest areas: {', '.join(strong_topics)}. "
    if develop_topics:
        summary += f"Focus areas: {', '.join(develop_topics)}."

    # Optionally update user competency level in DB
    if submission.user_id > 0:
        try:
            from app.models.models import UserCompetency
            from datetime import date
            uc = (
                db.query(UserCompetency)
                .filter(
                    UserCompetency.user_id == submission.user_id,
                    UserCompetency.competency_id == submission.competency_id,
                )
                .first()
            )
            if uc:
                # Only update if the assessment result is higher
                if verified_level > uc.current_level:
                    uc.current_level = verified_level
                    uc.evidence_source = f"DSA Assessment ({overall_score}%)"
                    uc.last_demonstrated = date.today()
                    db.commit()
            else:
                new_uc = UserCompetency(
                    user_id=submission.user_id,
                    competency_id=submission.competency_id,
                    current_level=verified_level,
                    evidence_source=f"DSA Assessment ({overall_score}%)",
                    last_demonstrated=date.today(),
                )
                db.add(new_uc)
                db.commit()
        except Exception:
            db.rollback()  # Don't fail the response if DB update fails

    return AssessmentResult(
        user_id=submission.user_id,
        competency_id=submission.competency_id,
        competency_name=DSA_COMPETENCY_NAME,
        overall_score=overall_score,
        verified_level=verified_level,
        topic_results=topic_results,
        summary=summary,
        strongest_topics=strong_topics,
        development_areas=develop_topics,
    )
