"""
Deterministic gap engine — extended with evidence-based classification.

Gap calculation:
    gap          = max(required_level - current_level, 0)
    priority     = (gap / MAX_LEVEL) * importance

Classification (user-facing):
    STRONG MATCH      gap == 0
    RELATED           user has a related/transferable skill (RELATED_SKILLS map)
    NEEDS VERIFICATION gap == 1 OR (has some evidence but low confidence)
    NEEDS DEVELOPMENT  has some evidence (current > 0) but gap > 1
    MISSING            no evidence at all (current == 0 and no related skill)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

MAX_LEVEL = 5  # competency scale ceiling

LEVEL_LABELS = ["No Evidence", "Awareness", "Basic", "Intermediate", "Advanced", "Expert"]


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
# Classification logic
# ---------------------------------------------------------------------------

def _classify_competency(
    comp_id: int,
    comp_name: str,
    current_level: int,
    required_level: int,
    gap: int,
    evidence_source: Optional[str],
    user_competency_ids: set[int],
    related_skills_map: Dict[int, List[int]],
    competency_map: Dict[int, CompetencyNode],
) -> Tuple[str, str, str, Optional[str], float, str, List[str]]:
    """
    Returns:
        (status, status_label, status_reason, related_skill_name, confidence,
         action_label, evidence_bullets)

    status values match schemas.CompetencyStatus Literal.
    """
    evidence_bullets: List[str] = []

    # Build evidence bullets from source
    if evidence_source and evidence_source.lower() not in ("none", ""):
        evidence_bullets.append(evidence_source)
    if current_level > 0:
        evidence_bullets.append(
            f"Competency level recorded: {LEVEL_LABELS[current_level]}"
        )

    # ── 1. STRONG MATCH ──────────────────────────────────────────────────────
    if gap == 0:
        confidence = min(0.6 + current_level * 0.08, 1.0)
        reason = (
            f"Your recorded level ({LEVEL_LABELS[current_level]}) meets or exceeds "
            f"the required level ({LEVEL_LABELS[required_level]}) for this role."
        )
        return (
            "strong_match", "Strong Match", reason,
            None, confidence, "View Details", evidence_bullets,
        )

    # ── 2. Check for RELATED skills in user profile ───────────────────────────
    related_for_this = related_skills_map.get(comp_id, [])
    found_related_id: Optional[int] = None
    for rel_id in related_for_this:
        if rel_id in user_competency_ids:
            found_related_id = rel_id
            break

    if found_related_id is not None:
        rel_node = competency_map.get(found_related_id)
        rel_name = rel_node.name if rel_node else f"Competency #{found_related_id}"
        reason = (
            f"We found {rel_name} in your profile, which is related to "
            f"{comp_name}. Your experience provides transferable knowledge, "
            f"though the target role requires verified proficiency."
        )
        evidence_bullets.append(f"Related skill found: {rel_name}")
        confidence = 0.45 + (current_level * 0.05)
        action = "Take Assessment" if gap >= 2 else "Verify Skills"
        return (
            "related", "Related / Transferable",
            reason, rel_name, confidence, action, evidence_bullets,
        )

    # ── 3. NEEDS VERIFICATION ── small gap or evidence present but uncertain ──
    if current_level > 0 and gap == 1:
        reason = (
            f"You have {LEVEL_LABELS[current_level]}-level evidence for {comp_name}, "
            f"which is close to the required level ({LEVEL_LABELS[required_level]}). "
            f"A short assessment can confirm your proficiency."
        )
        confidence = 0.4 + current_level * 0.05
        return (
            "needs_verification", "Needs Verification",
            reason, None, confidence, "Take Assessment", evidence_bullets,
        )

    if current_level > 0 and gap == 2:
        # Evidence exists but gap is notable — borderline between verification and development
        reason = (
            f"We found some evidence of {comp_name} ({LEVEL_LABELS[current_level]}), "
            f"but the required level is {LEVEL_LABELS[required_level]}. "
            f"An assessment can determine how much development is needed."
        )
        confidence = 0.35 + current_level * 0.04
        return (
            "needs_verification", "Needs Verification",
            reason, None, confidence, "Take Assessment", evidence_bullets,
        )

    # ── 4. NEEDS DEVELOPMENT ── has evidence but gap > 2 ─────────────────────
    if current_level > 0:
        reason = (
            f"Your profile shows {LEVEL_LABELS[current_level]}-level evidence for "
            f"{comp_name}, but the role requires {LEVEL_LABELS[required_level]}. "
            f"Focused learning can close this gap."
        )
        confidence = 0.3 + current_level * 0.04
        return (
            "needs_development", "Needs Development",
            reason, None, confidence, "View Learning Resources", evidence_bullets,
        )

    # ── 5. MISSING / NO EVIDENCE ─────────────────────────────────────────────
    reason = (
        f"We could not find evidence of {comp_name} in your profile. "
        f"This does not mean you don't have this skill — it means our system "
        f"could not confirm it from the information provided."
    )
    return (
        "missing", "Missing Evidence",
        reason, None, 0.0, "View Resources", [],
    )


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
    # Classification fields
    status: str = "missing"
    status_label: str = "Missing Evidence"
    status_reason: str = ""
    related_skill_name: Optional[str] = None
    confidence: float = 0.0
    action_label: str = ""
    evidence_bullets: list = field(default_factory=list)


def analyse_gaps(
    requirements: List[RoleRequirement],
    user_levels: List[UserLevel],
    competency_map: Dict[int, CompetencyNode],
    related_skills_map: Optional[Dict[int, List[int]]] = None,
) -> List[GapRow]:
    """
    For every competency required by the role, compute the gap row
    with user-facing classification.
    Rows are sorted by priority_score descending.
    """
    if related_skills_map is None:
        related_skills_map = {}

    user_lookup: Dict[int, UserLevel] = {u.competency_id: u for u in user_levels}
    user_competency_ids: set[int] = set(user_lookup.keys())
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

        status, label, reason, rel_name, confidence, action, bullets = _classify_competency(
            comp_id=req.competency_id,
            comp_name=cnode.name,
            current_level=current,
            required_level=req.required_level,
            gap=gap,
            evidence_source=evidence,
            user_competency_ids=user_competency_ids,
            related_skills_map=related_skills_map,
            competency_map=competency_map,
        )

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
            status=status,
            status_label=label,
            status_reason=reason,
            related_skill_name=rel_name,
            confidence=confidence,
            action_label=action,
            evidence_bullets=bullets,
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
            f"This course addresses 1 of your {total_gaps} gap(s): "
            f"{addressed_names[0]}."
        )
    else:
        top = ", ".join(addressed_names[:3])
        rest = f" and {n - 3} more" if n > 3 else ""
        explanation = (
            f"This course addresses {n} of your {total_gaps} competency gap(s): "
            f"{top}{rest}. Estimated gap-closure impact: {round(total_impact, 3)}."
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
