"""
SkillGap Engine — FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_db import init_db
from app.api.routes import users, roles, competencies, analysis, resume

app = FastAPI(
    title="SkillGap Engine API",
    description=(
        "Competency-based skill gap analysis and course recommendation engine. "
        "Supports multiple academic/career domains and cross-domain transitions."
    ),
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS — allow the Next.js dev server (port 3000)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Startup: create tables + seed
# ---------------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    init_db()


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(users.router,        prefix="/api/v1")
app.include_router(roles.router,        prefix="/api/v1")
app.include_router(competencies.router, prefix="/api/v1")
app.include_router(analysis.router,     prefix="/api/v1")
app.include_router(resume.router,       prefix="/api/v1")


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "SkillGap Engine API"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
