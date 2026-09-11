"""DSA Skill Assessment routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.assessment.engine import get_session_view, latest_for_user, start_assessment, submit_answer

router = APIRouter(prefix="/assessment", tags=["assessment"])


class StartPayload(BaseModel):
    user_id: int
    role_id: int


class SubmitPayload(BaseModel):
    answer: str = ""


@router.post("/start")
def start(payload: StartPayload, db: Session = Depends(get_db)):
    try:
        return start_assessment(db, payload.user_id, payload.role_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{session_id}/submit")
def submit(session_id: str, payload: SubmitPayload, db: Session = Depends(get_db)):
    try:
        return submit_answer(db, session_id, payload.answer)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/latest")
def latest(user_id: int, db: Session = Depends(get_db)):
    result = latest_for_user(db, user_id)
    if not result:
        return {"completed": False, "result": None}
    return result


@router.get("/{session_id}")
def get_one(session_id: str, db: Session = Depends(get_db)):
    try:
        return get_session_view(db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
