"""Original question generation from competency blueprints.

Live scoring uses the validated static bank. This module can mint extra
original MCQs from scenario templates, then run the same validator. Optional
LLM generation is only used when an API key is configured — never published
without validation.
"""

from __future__ import annotations

import hashlib
import os
import random
from typing import Any

from app.assessment.validator import validate_question

BLUEPRINTS: list[dict[str, Any]] = [
    {
        "topic": "arrays_strings",
        "difficulty": 2,
        "qtype": "concept",
        "prompt": (
            "A {domain} system stores {n} sequential records in an array and must "
            "compute the sum of every contiguous block of length {k}. Which approach "
            "has the best typical time complexity?"
        ),
        "options": [
            "Recompute each block from scratch — O(n·k)",
            "Maintain a running window sum — O(n)",
            "Sort the array first — O(n log n)",
            "Build a balanced tree of records — O(n log n) per query",
        ],
        "answer": "Maintain a running window sum — O(n)",
        "explanation": "A sliding window (or prefix sums) updates the block sum in O(1), for O(n) overall.",
        "vars": {"domain": ["warehouse", "telemetry", "payroll"], "n": ["thousands of", "many"], "k": ["k", "w"]},
    },
    {
        "topic": "graphs",
        "difficulty": 2,
        "qtype": "problem",
        "prompt": (
            "Campus {place} are modelled as an unweighted graph. You must report the "
            "fewest hops from the {start} to every other node. Which algorithm is appropriate?"
        ),
        "options": [
            "Depth-first search with a recursion stack only",
            "Breadth-first search from the start node",
            "A binary-search over hop counts without a graph walk",
            "In-order traversal of a BST of place names",
        ],
        "answer": "Breadth-first search from the start node",
        "explanation": "On an unweighted graph, BFS layers correspond to hop distance.",
        "vars": {"place": ["buildings", "labs", "hostels"], "start": ["gate", "library", "admin block"]},
    },
]


def _fill(template: str, values: dict[str, str]) -> str:
    out = template
    for k, v in values.items():
        out = out.replace("{" + k + "}", v)
    return out


def generate_from_blueprint(seed: str | None = None) -> list[dict[str, Any]]:
    rng = random.Random(seed or "skillgap-dsa")
    minted: list[dict[str, Any]] = []
    known: set[str] = set()
    for i, bp in enumerate(BLUEPRINTS):
        values = {k: rng.choice(v) for k, v in bp["vars"].items()}
        prompt = _fill(bp["prompt"], values)
        digest = hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:8]
        item = {
            "id": f"gen_{bp['topic']}_{i}_{digest}",
            "topic": bp["topic"],
            "difficulty": bp["difficulty"],
            "qtype": bp["qtype"],
            "prompt": prompt,
            "options": list(bp["options"]),
            "answer": bp["answer"],
            "explanation": bp["explanation"],
            "generated": True,
        }
        errors = validate_question(item, known)
        if errors:
            continue
        known.add(item["id"])
        minted.append(item)
    return minted


def try_llm_generate(_spec: dict[str, Any]) -> dict[str, Any] | None:
    """Placeholder: never publish LLM output unless validated.

    Returns None unless a provider key is present. Callers must still run
    validate_question before storing the item.
    """
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        return None
    return None
