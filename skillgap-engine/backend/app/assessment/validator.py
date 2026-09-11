"""Validate assessment items before they enter the live bank."""

from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = {
    "id",
    "topic",
    "difficulty",
    "qtype",
    "prompt",
    "explanation",
}

VALID_TYPES = {"concept", "problem", "tracing", "coding"}
VALID_DIFFICULTY = {1, 2, 3}


def validate_question(q: dict[str, Any], known_ids: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS - set(q.keys())
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")

    qid = q.get("id")
    if not qid or not isinstance(qid, str):
        errors.append("id must be a non-empty string")
    elif known_ids is not None and qid in known_ids:
        errors.append(f"duplicate id: {qid}")

    if q.get("qtype") not in VALID_TYPES:
        errors.append("invalid qtype")
    if q.get("difficulty") not in VALID_DIFFICULTY:
        errors.append("difficulty must be 1, 2, or 3")

    prompt = (q.get("prompt") or "").strip()
    if len(prompt) < 40:
        errors.append("prompt too short or ambiguous")

    banned_phrases = (
        "given an array of integers, return indices of the two numbers",
        "leetcode",
        "hackerrank",
        "geeksforgeeks",
        "gfg",
    )
    blob = (prompt + " " + (q.get("explanation") or "")).lower()
    if any(p in blob for p in banned_phrases):
        errors.append("prompt appears copied from a restricted source")

    qtype = q.get("qtype")
    if qtype in {"concept", "problem", "tracing"}:
        options = q.get("options") or []
        if len(options) < 3:
            errors.append("MCQ needs at least 3 options")
        answer = q.get("answer")
        if answer not in options:
            errors.append("answer must match one option exactly")
        if len(set(options)) != len(options):
            errors.append("duplicate options")
    elif qtype == "coding":
        tests = q.get("tests") or []
        if len(tests) < 2:
            errors.append("coding item needs at least 2 tests")
        starter = q.get("starter") or ""
        if "def solve" not in starter:
            errors.append("coding item must expose def solve")

    return errors


def validate_bank(questions: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    problems: list[str] = []
    for q in questions:
        errs = validate_question(q, seen)
        if q.get("id"):
            seen.add(q["id"])
        if errs:
            problems.append(f"{q.get('id')}: {'; '.join(errs)}")
    if problems:
        raise ValueError("Question bank failed validation:\n" + "\n".join(problems))
