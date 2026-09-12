"""
Deterministic gap engine.

All gap calculation, priority ranking, and course impact scoring is done
with pure Python arithmetic — no embeddings, no ML models.
Semantic similarity (from sentence-transformers) is only called when we
need to match free-text that lacks a direct competency link.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

MAX_LEVEL = 5  # competency scale ceiling


# ---------------------------------------------------------------------------
# Data containers (plain dataclasses — no ORM dependency)
# ---------------------------------------------------------------------------

@dataclass
class CompetencyNode:
    id: int
    name: str
    category: str


@dataclass
class RoleRequirement:
    competency_id: int
    required_level: int
    importance: float  # 0.0 – 1.0


@dataclass
class UserLevel:
    competency_id: int
    current_level: int
    evidence_source: Optional[str] = None


@dataclass
class CourseNode:
    id: int
    title: str
    description: str
    provider: str
    duration: str
    level: str
    source: str
    source_url: str
    # competency_id -> coverage_level (1-5)
    coverage: Dict[int, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Core gap formula
# ---------------------------------------------------------------------------

def compute_gap(required_level: int, current_level: int) -> int:
    """gap = max(required - current, 0)"""
    return max(required_level - current_level, 0)


def compute_priority_score(gap: int, importance: float) -> float:
    """priority = (gap / MAX_LEVEL) * importance"""
    if MAX_LEVEL == 0:
        return 0.0
    return (gap / MAX_LEVEL) * importance


# ---------------------------------------------------------------------------
# Gap analysis
# ---------------------------------------------------------------------------

@dataclass
class GapRow:
    competency_id: int
    competency_name: str
    category: str
    current_level: int
    required_level: int
    gap: int
    importance: float
    priority_score: float
    evidence_source: Optional[str]


def analyse_gaps(
    requirements: List[RoleRequirement],
    user_levels: List[UserLevel],
    competency_map: Dict[int, CompetencyNode],
) -> List[GapRow]:
    """
    For every competency required by the role, compute the gap row.
    Rows are sorted by priority_score descending.
    """
    user_lookup: Dict[int, UserLevel] = {u.competency_id: u for u in user_levels}
    rows: List[GapRow] = []

    for req in requirements:
        cnode = competency_map.get(req.competency_id)
        if cnode is None:
            continue

        ulevel = user_lookup.get(req.competency_id)
        current = ulevel.current_level if ulevel else 0
        evidence = ulevel.evidence_source if ulevel else None

        gap = compute_gap(req.required_level, current)
        priority = compute_priority_score(gap, req.importance)

        rows.append(GapRow(
            competency_id=req.competency_id,
            competency_name=cnode.name,
            category=cnode.category,
            current_level=current,
            required_level=req.required_level,
            gap=gap,
            importance=req.importance,
            priority_score=priority,
            evidence_source=evidence,
        ))

    rows.sort(key=lambda r: r.priority_score, reverse=True)
    return rows


def compute_readiness_score(gaps: List[GapRow]) -> float:
    """
    Secondary metric only.
    Weighted fraction of competency already acquired vs total required.
    Returns 0-100.
    """
    total_weighted_required = sum(r.required_level * r.importance for r in gaps)
    if total_weighted_required == 0:
        return 100.0
    total_weighted_achieved = sum(
        min(r.current_level, r.required_level) * r.importance for r in gaps
    )
    return round((total_weighted_achieved / total_weighted_required) * 100, 1)


# ---------------------------------------------------------------------------
# Course impact scoring
# ---------------------------------------------------------------------------

@dataclass
class CourseImpact:
    course: CourseNode
    impact_score: float
    gaps_addressed: List[str]  # competency names
    explanation: str


def score_course_impact(
    course: CourseNode,
    gaps: List[GapRow],
    competency_map: Dict[int, CompetencyNode],
) -> CourseImpact:
    """
    Estimate how much of the user's prioritised gap this course closes.

    Impact formula per matched competency:
        contribution = min(coverage_level, gap) / MAX_LEVEL * importance

    Total impact = sum of contributions (not normalised — allows comparison).
    """
    gap_lookup: Dict[int, GapRow] = {g.competency_id: g for g in gaps if g.gap > 0}

    addressed_names: List[str] = []
    total_impact = 0.0

    for comp_id, coverage in course.coverage.items():
        gap_row = gap_lookup.get(comp_id)
        if gap_row is None:
            continue
        contribution = (min(coverage, gap_row.gap) / MAX_LEVEL) * gap_row.importance
        total_impact += contribution
        addressed_names.append(gap_row.competency_name)

    # Build explanation string
    n = len(addressed_names)
    total_gaps = len(gap_lookup)
    if n == 0:
        explanation = "This course does not directly address your current priority gaps."
    elif n == 1:
        explanation = (
            f"This course addresses 1 of your {total_gaps} priority gap(s): "
            f"{addressed_names[0]}."
        )
    else:
        top = ", ".join(addressed_names[:3])
        rest = f" and {n - 3} more" if n > 3 else ""
        explanation = (
            f"This course addresses {n} of your {total_gaps} priority competency gap(s): "
            f"{top}{rest}. It has an estimated gap-closure impact of {round(total_impact, 3)}."
        )

    return CourseImpact(
        course=course,
        impact_score=round(total_impact, 4),
        gaps_addressed=addressed_names,
        explanation=explanation,
    )


def rank_courses(
    courses: List[CourseNode],
    gaps: List[GapRow],
    competency_map: Dict[int, CompetencyNode],
    top_n: int = 10,
) -> List[CourseImpact]:
    """Rank all courses by gap-closure impact, return top_n."""
    impacts = [score_course_impact(c, gaps, competency_map) for c in courses]
    impacts.sort(key=lambda ci: ci.impact_score, reverse=True)
    return impacts[:top_n]
