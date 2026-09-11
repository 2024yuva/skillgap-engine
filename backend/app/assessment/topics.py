"""DSA competency taxonomy for the Skill Assessment.

Topic groupings follow publicly described DSA curricula (arrays, hashing,
linked lists, stacks/queues, trees, graphs, sorting/search, DP) rather than
any vendor's copyrighted problem text.
"""

from __future__ import annotations

DSA_COMPETENCY_ID = 3

TOPICS: list[dict] = [
    {
        "id": "arrays_strings",
        "label": "Arrays + Strings",
        "weight": 0.15,
        "next_steps": [
            "Review in-place array transforms and two-index scans",
            "Practise prefix-sum reasoning on sequential records",
        ],
    },
    {
        "id": "hashing_two_pointers",
        "label": "Hashing + Two Pointers / Sliding Window",
        "weight": 0.15,
        "next_steps": [
            "Practise hash-map lookups for pair/frequency problems",
            "Practise sliding-window constraints on streams",
        ],
    },
    {
        "id": "linked_lists",
        "label": "Linked Lists",
        "weight": 0.10,
        "next_steps": [
            "Practise pointer rewiring: reverse and splice",
            "Practise fast/slow pointer cycle detection",
        ],
    },
    {
        "id": "stack_queue",
        "label": "Stacks & Queues",
        "weight": 0.10,
        "next_steps": [
            "Practise LIFO matching (nested delimiters, monotonic stacks)",
            "Practise FIFO scheduling and BFS-style queues",
        ],
    },
    {
        "id": "trees_bst",
        "label": "Trees + BST",
        "weight": 0.15,
        "next_steps": [
            "Practise recursive tree traversals and height reasoning",
            "Practise BST search/insert invariants",
        ],
    },
    {
        "id": "graphs",
        "label": "Graphs",
        "weight": 0.15,
        "next_steps": [
            "Learn BFS and DFS on adjacency lists",
            "Practise connectivity and shortest-path on unweighted graphs",
        ],
    },
    {
        "id": "sorting_searching",
        "label": "Sorting + Searching",
        "weight": 0.10,
        "next_steps": [
            "Review comparison-sort complexity trade-offs",
            "Practise binary search on sorted ranges and answer-space",
        ],
    },
    {
        "id": "dynamic_programming",
        "label": "Dynamic Programming",
        "weight": 0.10,
        "next_steps": [
            "Learn memoization versus tabulation",
            "Solve introductory subsequence / knapsack-style recurrences",
        ],
    },
]

TOPIC_BY_ID = {t["id"]: t for t in TOPICS}

LEVEL_LABELS = {
    0: "No Evidence",
    1: "Awareness",
    2: "Beginner",
    3: "Intermediate",
    4: "Advanced",
    5: "Expert",
}


def band_label(theta: float) -> str:
    if theta >= 3.6:
        return "Strong"
    if theta >= 2.3:
        return "Intermediate"
    return "Beginner"


def theta_to_level(theta: float) -> int:
    rounded = int(round(theta))
    return max(0, min(5, rounded))
