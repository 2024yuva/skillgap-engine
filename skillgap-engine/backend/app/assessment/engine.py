"""Adaptive DSA Skill Assessment engine.

Resume-derived DSA level seeds per-topic ability. Each answer updates
ability and confidence; the next item's difficulty follows the estimate.
The session may finish before 60 minutes once coverage + confidence suffice.
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.assessment.question_bank import QUESTION_BANK, QUESTION_BY_ID
from app.assessment.topics import (
    DSA_COMPETENCY_ID,
    LEVEL_LABELS,
    TOPIC_BY_ID,
    TOPICS,
    band_label,
    theta_to_level,
)
from app.models.models import AssessmentAttempt, User, UserCompetency

MAX_DURATION_SEC = 60 * 60
MAX_QUESTIONS = 16
MIN_QUESTIONS_FOR_EARLY_STOP = 10
CONFIDENCE_STOP = 0.72
QUESTIONS_PER_TOPIC_CAP = 2

_lock = threading.Lock()
_LIVE: dict[str, dict[str, Any]] = {}


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _public_question(q: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "id": q["id"],
        "topic": q["topic"],
        "topic_label": TOPIC_BY_ID[q["topic"]]["label"],
        "difficulty": q["difficulty"],
        "difficulty_label": {1: "Easy", 2: "Medium", 3: "Hard"}[q["difficulty"]],
        "qtype": q["qtype"],
        "prompt": q["prompt"],
    }
    if q["qtype"] == "coding":
        payload["starter"] = q.get("starter", "def solve(*args):\n    pass\n")
    else:
        payload["options"] = q["options"]
    return payload


def _initial_theta(dsa_level: int) -> float:
    return {0: 2.2, 1: 2.3, 2: 2.6, 3: 3.1, 4: 3.7, 5: 4.2}.get(dsa_level, 2.2)


def _difficulty_for_theta(theta: float) -> int:
    if theta >= 3.5:
        return 3
    if theta >= 2.4:
        return 2
    return 1


def _update_estimate(state: dict[str, Any], topic: str, difficulty: int, correct: bool) -> None:
    est = state["estimates"][topic]
    step_up = 0.45 + 0.15 * difficulty
    step_down = 0.35 + 0.12 * (4 - difficulty)
    if correct:
        est["theta"] = min(5.0, est["theta"] + step_up)
        est["confidence"] = min(1.0, est["confidence"] + 0.28)
        est["correct"] += 1
    else:
        est["theta"] = max(0.8, est["theta"] - step_down)
        est["confidence"] = min(1.0, est["confidence"] + 0.22)
        est["incorrect"] += 1
    est["asked"] += 1


def _pick_next(state: dict[str, Any]) -> dict[str, Any] | None:
    used = set(state["used_ids"])
    topic_order: list[str] = state["topic_order"]
    start = state["topic_cursor"]

    for offset in range(len(topic_order)):
        topic = topic_order[(start + offset) % len(topic_order)]
        est = state["estimates"][topic]
        if est["asked"] >= QUESTIONS_PER_TOPIC_CAP:
            continue
        want = _difficulty_for_theta(est["theta"])
        candidates = [
            q for q in QUESTION_BANK
            if q["topic"] == topic and q["id"] not in used
        ]
        if not candidates:
            continue
        same = [q for q in candidates if q["difficulty"] == want]
        pool = same or sorted(candidates, key=lambda q: abs(q["difficulty"] - want))
        # Prefer unused qtype variety: concept then problem/coding
        asked_types = {h["qtype"] for h in state["history"] if h["topic"] == topic}
        varied = [q for q in pool if q["qtype"] not in asked_types]
        chosen = (varied or pool)[0]
        state["topic_cursor"] = (start + offset + 1) % len(topic_order)
        return chosen
    return None


def _coverage_ready(state: dict[str, Any]) -> bool:
    if len(state["history"]) < MIN_QUESTIONS_FOR_EARLY_STOP:
        return False
    estimates = state["estimates"]
    if any(estimates[t["id"]]["asked"] < 1 for t in TOPICS):
        return False
    confs = [estimates[t["id"]]["confidence"] for t in TOPICS]
    return sum(confs) / len(confs) >= CONFIDENCE_STOP


def remaining_seconds(state: dict[str, Any]) -> int:
    elapsed = time.time() - state["started_ts"]
    return max(0, int(MAX_DURATION_SEC - elapsed))


def _run_coding(source: str, tests: list[dict[str, Any]]) -> bool:
    banned = ("import", "open(", "exec(", "eval(", "os.", "sys.", "subprocess", "__", "compile(")
    lowered = source.lower()
    if any(tok in lowered for tok in banned):
        return False
    if "def solve" not in source:
        return False
    safe_builtins = {
        "range": range,
        "len": len,
        "enumerate": enumerate,
        "min": min,
        "max": max,
        "sum": sum,
        "abs": abs,
        "sorted": sorted,
        "reversed": reversed,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "True": True,
        "False": False,
        "None": None,
        "isinstance": isinstance,
        "zip": zip,
        "map": map,
        "filter": filter,
        "all": all,
        "any": any,
        "print": lambda *a, **k: None,
    }
    ns: dict[str, Any] = {}
    try:
        exec(source, {"__builtins__": safe_builtins}, ns)  # noqa: S102 — restricted student snippet
    except Exception:
        return False
    fn = ns.get("solve")
    if not callable(fn):
        return False
    try:
        for t in tests:
            got = fn(*t["args"])
            if got != t["expected"]:
                return False
    except Exception:
        return False
    return True


def grade(question: dict[str, Any], answer: str) -> bool:
    if question["qtype"] == "coding":
        return _run_coding(answer or "", question.get("tests") or [])
    submitted = (answer or "").strip()
    return submitted == str(question["answer"]).strip()


def _serialize_live(state: dict[str, Any]) -> str:
    blob = dict(state)
    return json.dumps(blob)


def _progress_payload(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "answered": len(state["history"]),
        "max_questions": MAX_QUESTIONS,
        "remaining_seconds": remaining_seconds(state),
        "max_duration_seconds": MAX_DURATION_SEC,
    }


def _result_from_state(state: dict[str, Any], early_stop: bool, timed_out: bool) -> dict[str, Any]:
    topic_rows = []
    weighted = 0.0
    for t in TOPICS:
        est = state["estimates"][t["id"]]
        theta = est["theta"]
        topic_rows.append({
            "topic": t["id"],
            "label": t["label"],
            "weight": t["weight"],
            "theta": round(theta, 2),
            "level": theta_to_level(theta),
            "band": band_label(theta),
            "confidence": round(est["confidence"], 2),
            "asked": est["asked"],
            "correct": est["correct"],
            "next_steps": t["next_steps"],
        })
        weighted += theta * t["weight"]

    overall_level = theta_to_level(weighted)
    overall_label = LEVEL_LABELS[overall_level]
    overall_band = band_label(weighted)

    ranked = sorted(topic_rows, key=lambda r: r["theta"])
    biggest = [r for r in ranked if r["band"] != "Strong"][:2]
    if not biggest:
        biggest = ranked[:2]

    next_steps: list[str] = []
    for row in biggest:
        next_steps.extend(row["next_steps"])
    next_steps.append("Reassess after a focused practice block")

    review = []
    for h in state["history"]:
        q = QUESTION_BY_ID[h["question_id"]]
        review.append({
            "question_id": q["id"],
            "topic": q["topic"],
            "topic_label": TOPIC_BY_ID[q["topic"]]["label"],
            "prompt": q["prompt"],
            "qtype": q["qtype"],
            "correct": h["correct"],
            "explanation": q.get("explanation", ""),
            "expected": None if q["qtype"] == "coding" else q.get("answer"),
        })

    return {
        "overall_level": overall_level,
        "overall_label": overall_label,
        "overall_band": overall_band,
        "weighted_theta": round(weighted, 2),
        "topics": topic_rows,
        "biggest_gaps": [{"label": r["label"], "band": r["band"]} for r in biggest],
        "next_steps": next_steps,
        "early_stop": early_stop,
        "timed_out": timed_out,
        "questions_asked": len(state["history"]),
        "review": review,
    }


def _apply_to_profile(db: Session, user_id: int, result: dict[str, Any]) -> None:
    existing = (
        db.query(UserCompetency)
        .filter(
            UserCompetency.user_id == user_id,
            UserCompetency.competency_id == DSA_COMPETENCY_ID,
        )
        .first()
    )
    level = result["overall_level"]
    source = "DSA Skill Assessment"
    if existing:
        existing.current_level = level
        existing.evidence_source = source
        existing.last_demonstrated = date.today()
    else:
        db.add(UserCompetency(
            user_id=user_id,
            competency_id=DSA_COMPETENCY_ID,
            current_level=level,
            evidence_source=source,
            last_demonstrated=date.today(),
        ))


def _persist_attempt(db: Session, attempt: AssessmentAttempt, state: dict[str, Any], result: dict[str, Any] | None) -> None:
    attempt.questions_asked = len(state["history"])
    attempt.session_blob = _serialize_live(state)
    if result:
        attempt.status = "completed"
        attempt.completed_at = _utcnow()
        attempt.overall_level = result["overall_level"]
        attempt.overall_label = result["overall_label"]
        attempt.topic_results = json.dumps(result["topics"])
        attempt.next_steps = json.dumps(result["next_steps"])
        attempt.biggest_gaps = json.dumps(result["biggest_gaps"])
        attempt.early_stop = bool(result["early_stop"])
        attempt.applied = True
        _apply_to_profile(db, attempt.user_id, result)
    db.commit()
    db.refresh(attempt)


def _hydrate_state(blob: str) -> dict[str, Any]:
    return json.loads(blob)


def start_assessment(db: Session, user_id: int, role_id: int) -> dict[str, Any]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    uc = (
        db.query(UserCompetency)
        .filter(
            UserCompetency.user_id == user_id,
            UserCompetency.competency_id == DSA_COMPETENCY_ID,
        )
        .first()
    )
    seed_level = uc.current_level if uc else 0
    theta0 = _initial_theta(seed_level)
    session_id = str(uuid.uuid4())
    state = {
        "session_id": session_id,
        "user_id": user_id,
        "role_id": role_id,
        "started_ts": time.time(),
        "used_ids": [],
        "history": [],
        "topic_order": [t["id"] for t in TOPICS],
        "topic_cursor": 0,
        "seed_level": seed_level,
        "estimates": {
            t["id"]: {
                "theta": theta0,
                "confidence": 0.15 if seed_level <= 1 else 0.25,
                "asked": 0,
                "correct": 0,
                "incorrect": 0,
            }
            for t in TOPICS
        },
        "status": "in_progress",
    }
    question = _pick_next(state)
    if not question:
        raise RuntimeError("Question bank is empty")
    state["current_id"] = question["id"]

    attempt = AssessmentAttempt(
        id=session_id,
        user_id=user_id,
        role_id=role_id,
        assessment_type="dsa",
        status="in_progress",
        started_at=_utcnow(),
        questions_asked=0,
        session_blob=_serialize_live(state),
        early_stop=False,
        applied=False,
    )
    db.add(attempt)
    db.commit()

    with _lock:
        _LIVE[session_id] = state

    return {
        "session_id": session_id,
        "status": "in_progress",
        "assessment_name": "DSA Skill Assessment",
        "seed_level": seed_level,
        "initial_difficulty": {1: "Easy", 2: "Medium", 3: "Hard"}[_difficulty_for_theta(theta0)],
        "question": _public_question(question),
        "progress": _progress_payload(state),
        "completed": False,
    }


def _load_state(db: Session, session_id: str) -> tuple[AssessmentAttempt, dict[str, Any]]:
    with _lock:
        state = _LIVE.get(session_id)
    attempt = db.query(AssessmentAttempt).filter(AssessmentAttempt.id == session_id).first()
    if not attempt:
        raise ValueError("Assessment session not found")
    if state is None:
        if not attempt.session_blob:
            raise ValueError("Assessment session not found")
        state = _hydrate_state(attempt.session_blob)
        with _lock:
            _LIVE[session_id] = state
    return attempt, state


def submit_answer(db: Session, session_id: str, answer: str) -> dict[str, Any]:
    attempt, state = _load_state(db, session_id)
    if attempt.status == "completed" or state.get("status") == "completed":
        return get_session_view(db, session_id)

    timed_out = remaining_seconds(state) <= 0
    current_id = state.get("current_id")
    if current_id and not timed_out:
        question = QUESTION_BY_ID[current_id]
        correct = grade(question, answer)
        state["used_ids"].append(current_id)
        state["history"].append({
            "question_id": current_id,
            "topic": question["topic"],
            "qtype": question["qtype"],
            "difficulty": question["difficulty"],
            "correct": correct,
        })
        _update_estimate(state, question["topic"], question["difficulty"], correct)
        state["current_id"] = None

    early = _coverage_ready(state)
    next_q = None
    if not timed_out and len(state["history"]) < MAX_QUESTIONS and not early:
        next_q = _pick_next(state)

    if timed_out or len(state["history"]) >= MAX_QUESTIONS or early or next_q is None:
        result = _result_from_state(state, early_stop=early and not timed_out, timed_out=timed_out)
        state["status"] = "completed"
        state["result"] = result
        _persist_attempt(db, attempt, state, result)
        with _lock:
            _LIVE[session_id] = state
        return {
            "session_id": session_id,
            "status": "completed",
            "completed": True,
            "assessment_name": "DSA Skill Assessment",
            "progress": _progress_payload(state),
            "result": result,
        }

    state["current_id"] = next_q["id"]
    _persist_attempt(db, attempt, state, None)
    with _lock:
        _LIVE[session_id] = state
    return {
        "session_id": session_id,
        "status": "in_progress",
        "completed": False,
        "assessment_name": "DSA Skill Assessment",
        "question": _public_question(next_q),
        "progress": _progress_payload(state),
    }


def get_session_view(db: Session, session_id: str) -> dict[str, Any]:
    attempt, state = _load_state(db, session_id)
    if attempt.status == "completed" or state.get("status") == "completed":
        result = state.get("result")
        if not result and attempt.topic_results:
            result = {
                "overall_level": attempt.overall_level,
                "overall_label": attempt.overall_label,
                "overall_band": band_label(float(attempt.overall_level or 0)),
                "topics": json.loads(attempt.topic_results or "[]"),
                "biggest_gaps": json.loads(attempt.biggest_gaps or "[]"),
                "next_steps": json.loads(attempt.next_steps or "[]"),
                "early_stop": attempt.early_stop,
                "timed_out": False,
                "questions_asked": attempt.questions_asked,
                "review": [],
            }
        return {
            "session_id": session_id,
            "status": "completed",
            "completed": True,
            "assessment_name": "DSA Skill Assessment",
            "progress": _progress_payload(state),
            "result": result,
        }

    if remaining_seconds(state) <= 0:
        return submit_answer(db, session_id, "")

    qid = state.get("current_id")
    question = QUESTION_BY_ID[qid] if qid else None
    return {
        "session_id": session_id,
        "status": "in_progress",
        "completed": False,
        "assessment_name": "DSA Skill Assessment",
        "question": _public_question(question) if question else None,
        "progress": _progress_payload(state),
    }


def latest_for_user(db: Session, user_id: int) -> dict[str, Any] | None:
    row = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.assessment_type == "dsa",
            AssessmentAttempt.status == "completed",
        )
        .order_by(AssessmentAttempt.completed_at.desc())
        .first()
    )
    if not row:
        return None
    return {
        "session_id": row.id,
        "status": "completed",
        "completed": True,
        "assessment_name": "DSA Skill Assessment",
        "completed_at": row.completed_at.isoformat() if row.completed_at else None,
        "result": {
            "overall_level": row.overall_level,
            "overall_label": row.overall_label,
            "overall_band": band_label(float(row.overall_level or 0)),
            "topics": json.loads(row.topic_results or "[]"),
            "biggest_gaps": json.loads(row.biggest_gaps or "[]"),
            "next_steps": json.loads(row.next_steps or "[]"),
            "early_stop": row.early_stop,
            "timed_out": False,
            "questions_asked": row.questions_asked,
        },
    }
