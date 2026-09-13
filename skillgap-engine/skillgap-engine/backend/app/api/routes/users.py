"""User profile routes."""

from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.models import User, UserCompetency, Competency
from app.schemas.schemas import UserCreate, UserRead, UserCompetencyRead, UserCompetencyUpsert

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in payload.model_dump().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}/competencies", response_model=List[UserCompetencyRead])
def get_user_competencies(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    rows = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == user_id)
        .all()
    )
    return rows


@router.post(
    "/{user_id}/competencies",
    response_model=UserCompetencyRead,
    status_code=status.HTTP_201_CREATED,
)
def upsert_user_competency(
    user_id: int,
    payload: UserCompetencyUpsert,
    db: Session = Depends(get_db),
):
    """Create or update a single user competency level."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    comp = db.query(Competency).filter(Competency.id == payload.competency_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Competency not found")

    existing = (
        db.query(UserCompetency)
        .filter(
            UserCompetency.user_id == user_id,
            UserCompetency.competency_id == payload.competency_id,
        )
        .first()
    )

    if existing:
        existing.current_level = payload.current_level
        existing.evidence_source = payload.evidence_source
        existing.last_demonstrated = payload.last_demonstrated
        db.commit()
        db.refresh(existing)
        return existing
    else:
        uc = UserCompetency(
            user_id=user_id,
            **payload.model_dump(),
        )
        db.add(uc)
        db.commit()
        db.refresh(uc)
        return uc
