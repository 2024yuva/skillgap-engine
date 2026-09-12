"""
Database initialisation and seed loader.

Run directly:
    python -m app.database.init_db

Or called from the FastAPI startup event.
"""

from __future__ import annotations
from sqlalchemy.orm import Session

from app.database.connection import Base, engine, SessionLocal
from app.models.models import (
    Competency, Role, RoleCompetency,
    User, UserCompetency, Course, CourseCompetency,
    SkillCareerRecord, SkilloraResource, CompanyJobReference,
)
from app.ingestion.seed_data import (
    COMPETENCIES, ROLES, ROLE_COMPETENCIES,
    USERS, USER_COMPETENCIES, COURSES, COURSE_COMPETENCIES,
    SKILL_CAREER_RECORDS, SKILLORA_RESOURCES, COMPANY_JOB_REFS,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("[init_db] Tables created (or already exist).")


def _already_seeded(db: Session) -> bool:
    return db.query(Competency).count() > 0


def seed(db: Session) -> None:
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

    # ── Skillora dataset tables ──────────────────────────────────────────
    print("[init_db] Seeding Skill Career Dataset (105 records) …")
    for rec in SKILL_CAREER_RECORDS:
        db.add(SkillCareerRecord(**rec))
    db.commit()

    print("[init_db] Seeding Skillora Learning Resources …")
    for res in SKILLORA_RESOURCES:
        db.add(SkilloraResource(**res))
    db.commit()

    print("[init_db] Seeding Company Job References (35 records) …")
    for ref in COMPANY_JOB_REFS:
        db.add(CompanyJobReference(**ref))
    db.commit()

    print("[init_db] Seed complete.")
    print(f"[init_db]   Competencies:          {len(COMPETENCIES)}")
    print(f"[init_db]   Roles:                 {len(ROLES)}")
    print(f"[init_db]   Courses:               {len(COURSES)}")
    print(f"[init_db]   Skill Career Records:  {len(SKILL_CAREER_RECORDS)}")
    print(f"[init_db]   Skillora Resources:    {len(SKILLORA_RESOURCES)}")
    print(f"[init_db]   Company Job Refs:      {len(COMPANY_JOB_REFS)}")


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
