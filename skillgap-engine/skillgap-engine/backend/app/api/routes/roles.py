"""Role routes."""

from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.models.models import Role, RoleCompetency
from app.schemas.schemas import RoleRead, RoleCompetencyRead

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=List[RoleRead])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).order_by(Role.sector, Role.name).all()


@router.get("/{role_id}", response_model=RoleRead)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.get("/{role_id}/competencies", response_model=List[RoleCompetencyRead])
def get_role_competencies(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    rows = (
        db.query(RoleCompetency)
        .filter(RoleCompetency.role_id == role_id)
        .options(joinedload(RoleCompetency.competency))
        .all()
    )
    return rows
