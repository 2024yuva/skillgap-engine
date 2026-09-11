# SkillGap Engine

Competency-based skill gap analysis and personalised course recommendation system.
Built for the **Smart India Hackathon** — Ministry of Statistics and Programme Implementation (MoSPI) track.

---

## What it does

1. Models **people, roles, and courses** in a shared competency space (0–5 scale).
2. Calculates **competency-level skill gaps** for a user against any target role.
3. Ranks gaps by `(gap / 5) × importance` — the primary output.
4. Ranks courses by **estimated gap-closure impact** (deterministic, explainable).
5. Shows **why** each course was recommended.
6. Supports **7 domains**: CSE, EEE, ECE, Mechanical, Civil, Statistics, Management.
7. Includes **cross-domain transitions**: EEE → SDE, Mechanical → Data Analyst, etc.
8. Includes a **Statistical Officer (MoSPI)** target role with official-statistics competencies.

---

## Architecture

```
skillgap-engine/
├── backend/               # FastAPI + Python
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── database/      # SQLAlchemy engine, session, init + seed
│   │   ├── models/        # ORM models
│   │   ├── schemas/       # Pydantic v2 schemas
│   │   ├── engine/        # Deterministic gap engine (pure Python)
│   │   ├── services/      # gap_service.py, semantic.py
│   │   ├── api/routes/    # users, roles, competencies, analysis
│   │   └── ingestion/     # seed_data.py
│   └── .env               # DATABASE_URL
├── frontend/frontend/     # Next.js 16 + TypeScript + Tailwind + Recharts
│   ├── app/
│   │   ├── page.tsx       # Profile + role selector
│   │   └── dashboard/     # Hero gap analysis + course recommendations
│   ├── components/        # CompetencyBar, CourseCard, RadarChart, Gauge
│   └── lib/               # api.ts (typed API client), utils.ts
└── data/                  # (reserved for future CSV/JSON sources)
```

---

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.10+ |
| PostgreSQL | 14+ |
| Node.js | 18+ |
| npm | 9+ |

---

## Quick Start

### 1. PostgreSQL setup

```sql
CREATE USER skillgap WITH PASSWORD 'skillgap';
CREATE DATABASE skillgap_db OWNER skillgap;
```

### 2. Backend

```bash
cd skillgap-engine/backend

# Create and activate the virtual environment (already done if venv/ exists)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv \
            python-multipart PyPDF2 python-docx sentence-transformers pandas numpy networkx

# Configure database URL
copy .env.example .env         # then edit if needed

# Run the server (tables + seed data are created automatically on startup)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: http://localhost:8000/docs

### 3. Frontend

```bash
cd skillgap-engine/frontend/frontend

npm install
npm run dev
```

Open: http://localhost:3000

---

## Core API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/users/` | List all user profiles |
| POST | `/api/v1/users/` | Create a new profile |
| GET | `/api/v1/roles/` | List all target roles |
| GET | `/api/v1/competencies/` | List competency catalogue |
| GET | `/api/v1/analysis/gap?user_id=1&role_id=1` | **Gap analysis** (primary endpoint) |
| GET | `/api/v1/analysis/recommendations?user_id=1&role_id=1` | Course recommendations |
| GET | `/api/v1/analysis/semantic-match?query=...` | Semantic competency search |

---

## Demo profiles

| User | Background | Transition |
|---|---|---|
| Arjun Verma | B.Tech EEE | → Software Development Engineer |
| Priya Nair | B.Tech Mechanical | → Data Analyst |
| Rahul Das | B.Tech ECE | → Embedded Systems Engineer |
| Sneha Kulkarni | B.Sc Statistics | → Data Scientist |
| Vikram Singh | B.Tech CSE | → Data Analyst |

---

## Competency scale

| Level | Label |
|---|---|
| 0 | No Evidence |
| 1 | Awareness |
| 2 | Basic |
| 3 | Intermediate |
| 4 | Advanced |
| 5 | Expert |

---

## Gap formula

```
gap             = max(required_level − current_level, 0)
priority_score  = (gap / 5) × importance
```

Course impact is the sum of `min(coverage_level, gap) / 5 × importance` across all matched competencies — fully deterministic, no embeddings involved.

---

## Milestone 1 status

| Component | Status |
|---|---|
| Backend structure | ✅ |
| ORM models (7 tables) | ✅ |
| Pydantic schemas | ✅ |
| Deterministic gap engine | ✅ |
| Seed data (50 competencies, 10 roles, 36 courses, 5 users) | ✅ |
| FastAPI routes | ✅ |
| Semantic matching service | ✅ |
| Next.js dashboard | ✅ |
| Frontend ↔ backend connected | ✅ |

## Next recommended milestone

- Add user competency self-assessment UI (sliders per competency)
- Add a Learning Path view (ordered sequence of top courses)
- Connect real NPTEL/Swayam course data via scraper
- Add AI-generated competency assessment quiz
- Persist selected profile in localStorage
