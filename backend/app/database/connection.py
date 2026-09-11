"""Database connection and session management."""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite (file-based, no server needed) when DATABASE_URL is not set.
# Set DATABASE_URL=postgresql://... in .env to switch to PostgreSQL.
_default_sqlite = f"sqlite:///{Path(__file__).parent.parent.parent / 'skillgap.db'}"
DATABASE_URL = os.getenv("DATABASE_URL", _default_sqlite)

# SQLite needs check_same_thread=False; PostgreSQL ignores connect_args
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, connect_args=_connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency — yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
