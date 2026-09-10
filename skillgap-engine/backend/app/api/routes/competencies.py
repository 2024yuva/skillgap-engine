"""Competency catalogue routes."""

from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.models import Competency
from app.schemas.schemas import CompetencyRead

router = APIRouter(prefix="/competencies", tags=["competencies"])


@router.get("/", response_model=List[CompetencyRead])
def list_competencies(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db),
):
    q = db.query(Competency)
    if category:
        q = q.filter(Competency.category == category)
    return q.order_by(Competency.category, Competency.name).all()
