"""
Database initialisation and seed loader.

Run directly:
    python -m app.database.init_db

Or call init_db() from the FastAPI startup event.
"""

from __future__ import annotations
import sys
from sqlalchemy.orm import Session

from app.database.connection import Base, engine, SessionLocal
from app.models.models import (
    Competency, Role, RoleCompetency,
    User, UserCompetency, Course, CourseCompetency,
    AssessmentAttempt,
)
from app.ingestion.seed_data import (
    COMPETENCIES, ROLES, ROLE_COMPETENCIES,
    USERS, USER_COMPETENCIES, COURSES, COURSE_COMPETENCIES,
)


def create_tables() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("[init_db] Tables created (or already exist).")


def _already_seeded(db: Session) -> bool:
    return db.query(Competency).count() > 0


def seed(db: Session) -> None:
    """Insert seed data if the database is empty."""
    if _already_seeded(db):
        print("[init_db] Database already seeded — skipping.")
        return

    print("[init_db] Seeding competencies …")
    for c in COMPETENCIES:
        db.add(Competency(**c))
    db.commit()

    print("[init_db] Seeding roles …")
    for r in ROLES:
        db.add(Role(**r))
    db.commit()

    print("[init_db] Seeding role competencies …")
    for rc in ROLE_COMPETENCIES:
        db.add(RoleCompetency(**rc))
    db.commit()

    print("[init_db] Seeding users …")
    for u in USERS:
        db.add(User(**u))
    db.commit()

    print("[init_db] Seeding user competencies …")
    for uc in USER_COMPETENCIES:
        db.add(UserCompetency(**uc))
    db.commit()

    print("[init_db] Seeding courses …")
    for c in COURSES:
        db.add(Course(**c))
    db.commit()

    print("[init_db] Seeding course competencies …")
    for cc in COURSE_COMPETENCIES:
        db.add(CourseCompetency(**cc))
    db.commit()

    print("[init_db] Seed complete.")


def init_db() -> None:
    create_tables()
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("[init_db] Done.")
