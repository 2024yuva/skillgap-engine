"""Original DSA Skill Assessment bank.

Items test interview-style *patterns* (hash lookup, reverse list, BFS, etc.)
using original logistics / campus / ops scenarios. Do not paste third-party
problem statements into this file.
"""

from __future__ import annotations

from app.assessment.generator import generate_from_blueprint
from app.assessment.validator import validate_bank

QUESTIONS: list[dict] = [
    # ---- Arrays + Strings ----
    {
        "id": "arr_e_concept",
        "topic": "arrays_strings",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "A ticketing desk stores passenger names in a contiguous array. Staff must "
            "read the name at a known seat index. What is the typical time complexity?"
        ),
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "answer": "O(1)",
        "explanation": "Arrays support constant-time index access when the index is known.",
    },
    {
        "id": "arr_m_concept",
        "topic": "arrays_strings",
        "difficulty": 2,
        "qtype": "concept",
        "prompt": (
            "A warehouse records daily inbound counts in an array. Auditors repeatedly ask "
            "for the total between two dates (inclusive). After a linear preprocess, each "
            "query should be answered in which best time?"
        ),
        "options": [
            "O(1) using prefix sums",
            "O(n) by scanning the range every time, which is optimal",
            "O(log n) only if the array stays unsorted",
            "O(n²) because every pair of dates must be stored",
        ],
        "answer": "O(1) using prefix sums",
        "explanation": "Prefix sums turn a range total into two lookups and a subtraction.",
    },
    {
        "id": "arr_m_problem",
        "topic": "arrays_strings",
        "difficulty": 2,
        "qtype": "problem",
        "prompt": (
            "Sensor readings arrive as [4, -1, 2, 1, -5, 4]. You need the contiguous stretch "
            "with the largest sum (Kadane-style). What should the algorithm return?"
        ),
        "options": ["6", "5", "4", "7"],
        "answer": "6",
        "explanation": "The stretch [4, -1, 2, 1] sums to 6, which beats later alternatives.",
    },
    {
        "id": "arr_h_tracing",
        "topic": "arrays_strings",
        "difficulty": 3,
        "qtype": "tracing",
        "prompt": (
            "A function reverses characters of a string in place by swapping the first and "
            "last unread pair until the two indices meet. For input 'cargo', what is the "
            "result after the process finishes?"
        ),
        "options": ["ocrag", "ograc", "cagro", "cargo"],
        "answer": "ograc",
        "explanation": "Two-pointer reverse yields o-g-r-a-c.",
    },
    {
        "id": "arr_m_coding",
        "topic": "arrays_strings",
        "difficulty": 2,
        "qtype": "coding",
        "prompt": (
            "Implement solve(nums) to return the largest sum of any contiguous subarray. "
            "Assume nums is a non-empty list of integers (may include negatives)."
        ),
        "starter": "def solve(nums):\n    # return largest contiguous sum\n    pass\n",
        "tests": [
            {"args": [[4, -1, 2, 1, -5, 4]], "expected": 6},
            {"args": [[-2, -1, -3]], "expected": -1},
            {"args": [[5]], "expected": 5},
        ],
        "explanation": "Track a running sum that resets when it becomes harmful, keeping a global max.",
    },
    # ---- Hashing + two pointers / sliding window ----
    {
        "id": "hash_e_concept",
        "topic": "hashing_two_pointers",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "A lost-and-found desk must check whether any two claim tickets sum to a "
            "published target code. Tickets are unsorted. Which structure gives expected "
            "linear time for the scan?"
        ),
        "options": [
            "A hash set of values already seen",
            "A binary heap of all tickets",
            "A doubly linked list of tickets",
            "An adjacency matrix of ticket IDs",
        ],
        "answer": "A hash set of values already seen",
        "explanation": "Store complements in a hash set and probe as you scan — expected O(n).",
    },
    {
        "id": "hash_m_problem",
        "topic": "hashing_two_pointers",
        "difficulty": 2,
        "qtype": "problem",
        "prompt": (
            "Package weights are [9, 2, 7, 11, 15] and a route needs two packages whose "
            "weights add to 18. Using a one-pass hash map of value → index, which index "
            "pair is valid?"
        ),
        "options": ["(0, 2) because 9+7=16", "(1, 2) because 2+7=9", "(0, 3) because 9+11=20", "(2, 3) because 7+11=18"],
        "answer": "(2, 3) because 7+11=18",
        "explanation": "7 and 11 are the pair that meets the combined-weight target of 18.",
    },
    {
        "id": "hash_m_tracing",
        "topic": "hashing_two_pointers",
        "difficulty": 2,
        "qtype": "tracing",
        "prompt": (
            "A conveyor window may hold at most 3 consecutive items and must report the "
            "maximum of each window over [1, 3, 2, 6, 4]. Windows are [1,3,2], [3,2,6], "
            "[2,6,4]. What is the list of window maxima?"
        ),
        "options": ["[3, 6, 6]", "[3, 6, 4]", "[1, 3, 2, 6, 4]", "[3, 3, 6]"],
        "answer": "[3, 6, 6]",
        "explanation": "Max(1,3,2)=3, max(3,2,6)=6, max(2,6,4)=6.",
    },
    {
        "id": "hash_h_concept",
        "topic": "hashing_two_pointers",
        "difficulty": 3,
        "qtype": "concept",
        "prompt": (
            "You must find the shortest substring of a log line that contains every "
            "character from a required alphabet (each at least once). Which family of "
            "approaches is the right complexity class?"
        ),
        "options": [
            "Expanding/contracting sliding window with frequency maps",
            "Sorting the log line, then a binary search on characters",
            "Building a BST of every suffix",
            "Floyd cycle detection on the string indices",
        ],
        "answer": "Expanding/contracting sliding window with frequency maps",
        "explanation": "A two-pointer window plus counts finds the minimum covering span in linear time.",
    },
    {
        "id": "hash_m_coding",
        "topic": "hashing_two_pointers",
        "difficulty": 2,
        "qtype": "coding",
        "prompt": (
            "Implement solve(nums, target) returning True if two distinct elements of nums "
            "add to target, otherwise False. Aim for expected linear time."
        ),
        "starter": "def solve(nums, target):\n    # return True if any pair sums to target\n    pass\n",
        "tests": [
            {"args": [[9, 2, 7, 11], 18], "expected": True},
            {"args": [[1, 2, 3], 7], "expected": False},
            {"args": [[5, 5], 10], "expected": True},
        ],
        "explanation": "Record seen values in a set and check whether target - x was already seen.",
    },
    # ---- Linked lists ----
    {
        "id": "ll_e_concept",
        "topic": "linked_lists",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "A singly linked roster stores volunteers. Inserting a new volunteer at the "
            "head (you already hold the head pointer) is typically which complexity?"
        ),
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "answer": "O(1)",
        "explanation": "Rewiring the head pointer is constant work on a singly linked list.",
    },
    {
        "id": "ll_m_problem",
        "topic": "linked_lists",
        "difficulty": 2,
        "qtype": "problem",
        "prompt": (
            "A chain of delivery stops is A→B→C→D→None. After a standard in-place reverse "
            "of the whole list, what is the new head-to-tail order?"
        ),
        "options": ["D→C→B→A", "A→B→C→D", "B→A→D→C", "A→D→C→B"],
        "answer": "D→C→B→A",
        "explanation": "Iterative reverse walks next pointers and rebuilds links backward.",
    },
    {
        "id": "ll_m_tracing",
        "topic": "linked_lists",
        "difficulty": 2,
        "qtype": "tracing",
        "prompt": (
            "Two pointers start at the head of 10→20→30→40→50. The fast pointer moves two "
            "nodes per step and the slow pointer moves one. When fast can no longer take a "
            "full two-step, where is slow?"
        ),
        "options": ["On 30 (the middle node)", "On 10", "On 50", "On 40"],
        "answer": "On 30 (the middle node)",
        "explanation": "Fast/slow meeting at the midpoint is the classic tortoise-hare scan on an odd-length list.",
    },
    {
        "id": "ll_h_concept",
        "topic": "linked_lists",
        "difficulty": 3,
        "qtype": "concept",
        "prompt": (
            "A circular shuttle route accidentally created a loop in an otherwise linear "
            "stop list. Which method detects the loop with O(1) extra memory?"
        ),
        "options": [
            "Fast and slow pointers",
            "Storing every visited node in an array, then sorting it",
            "Converting the list to a balanced BST",
            "Binary search on node addresses",
        ],
        "answer": "Fast and slow pointers",
        "explanation": "If a cycle exists, the faster pointer eventually laps the slower one.",
    },
    # ---- Stack + queue ----
    {
        "id": "sq_e_concept",
        "topic": "stack_queue",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "A compiler checks that every opening bracket in a configuration file has a "
            "matching closer in the right order. Which structure models that process?"
        ),
        "options": ["Stack (LIFO)", "Queue (FIFO)", "Hash map only", "Union-find"],
        "answer": "Stack (LIFO)",
        "explanation": "The most recently opened delimiter must close first — classic stack matching.",
    },
    {
        "id": "sq_m_tracing",
        "topic": "stack_queue",
        "difficulty": 2,
        "qtype": "tracing",
        "prompt": (
            "Check the token stream '( [ ] { } )'. A stack-based matcher pushes openings "
            "and pops on closers. Does the stream balance?"
        ),
        "options": ["Yes, it balances", "No, a square bracket is leftover", "No, a curly brace is leftover", "No, the final ')' is unmatched"],
        "answer": "Yes, it balances",
        "explanation": "Each closer matches the current stack top; the stack is empty at the end.",
    },
    {
        "id": "sq_m_problem",
        "topic": "stack_queue",
        "difficulty": 2,
        "qtype": "problem",
        "prompt": (
            "Print-job IDs arrive 7, then 3, then 9. A queue always serves the earliest "
            "arrival. After two dequeue operations, which ID remains at the front?"
        ),
        "options": ["9", "7", "3", "The queue is empty"],
        "answer": "9",
        "explanation": "FIFO removes 7 then 3; 9 is left at the front.",
    },
    {
        "id": "sq_h_concept",
        "topic": "stack_queue",
        "difficulty": 3,
        "qtype": "concept",
        "prompt": (
            "You must report, for each day, the next warmer temperature in a forecast "
            "array (or none). Which stack pattern yields linear time?"
        ),
        "options": [
            "Monotonic stack of unresolved day indices",
            "Queue of all days sorted by date descending",
            "Two stacks simulating a queue, ignoring values",
            "DFS on a temperature graph",
        ],
        "answer": "Monotonic stack of unresolved day indices",
        "explanation": "A decreasing monotonic stack resolves next-greater in amortized O(1) per day.",
    },
    # ---- Trees + BST ----
    {
        "id": "tree_e_concept",
        "topic": "trees_bst",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "In a binary tree of org-chart reports, visiting left subtree, then the node, "
            "then the right subtree is which traversal?"
        ),
        "options": ["In-order", "Pre-order", "Post-order", "Level-order"],
        "answer": "In-order",
        "explanation": "In-order is left–node–right.",
    },
    {
        "id": "tree_m_problem",
        "topic": "trees_bst",
        "difficulty": 2,
        "qtype": "problem",
        "prompt": (
            "A BST stores badge IDs. In-order walk of a valid BST produces which property?"
        ),
        "options": [
            "Sorted IDs in non-decreasing order",
            "IDs grouped by tree height",
            "IDs in insertion order",
            "IDs in reverse insertion order",
        ],
        "answer": "Sorted IDs in non-decreasing order",
        "explanation": "BST in-order is sorted by key.",
    },
    {
        "id": "tree_m_tracing",
        "topic": "trees_bst",
        "difficulty": 2,
        "qtype": "tracing",
        "prompt": (
            "Tree: root 8, left 3 (left 1, right 6), right 10 (right 14). What is the "
            "pre-order sequence (node, left, right)?"
        ),
        "options": ["8, 3, 1, 6, 10, 14", "1, 3, 6, 8, 10, 14", "1, 6, 3, 14, 10, 8", "8, 10, 14, 3, 6, 1"],
        "answer": "8, 3, 1, 6, 10, 14",
        "explanation": "Pre-order emits the root before each subtree: 8, then left cluster, then right cluster.",
    },
    {
        "id": "tree_h_concept",
        "topic": "trees_bst",
        "difficulty": 3,
        "qtype": "concept",
        "prompt": (
            "Two employee nodes sit in a binary tree of reporting lines. You need their "
            "lowest common manager (lowest common ancestor). Which idea is correct?"
        ),
        "options": [
            "Recurse: if the two nodes split left/right of a root, that root is the LCA",
            "Always return the tree's overall root",
            "Convert the tree to an array and binary-search names",
            "Run Dijkstra from one employee using edge weights of 1 on parent links only",
        ],
        "answer": "Recurse: if the two nodes split left/right of a root, that root is the LCA",
        "explanation": "Standard LCA recursion returns the split point where the two nodes lie in different subtrees (or the node itself).",
    },
    {
        "id": "tree_m_coding",
        "topic": "trees_bst",
        "difficulty": 2,
        "qtype": "coding",
        "prompt": (
            "Nodes are dicts {'v': int, 'l': node|None, 'r': node|None}. Implement "
            "solve(root) to return the height of the tree (empty tree height 0, single node 1)."
        ),
        "starter": "def solve(root):\n    # return tree height\n    pass\n",
        "tests": [
            {"args": [{"v": 1, "l": None, "r": None}], "expected": 1},
            {
                "args": [{"v": 1, "l": {"v": 2, "l": None, "r": None}, "r": {"v": 3, "l": None, "r": None}}],
                "expected": 2,
            },
            {"args": [None], "expected": 0},
        ],
        "explanation": "Height is 0 for empty; otherwise 1 + max(left, right).",
    },
    # ---- Graphs ----
    {
        "id": "graph_e_concept",
        "topic": "graphs",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "Campus buildings and walkways are an unweighted undirected graph. To list every "
            "building reachable from the gate, exploring neighbours layer by layer, which "
            "traversal is the natural fit?"
        ),
        "options": ["BFS", "In-order BST walk", "Binary search", "Heap sort"],
        "answer": "BFS",
        "explanation": "BFS explores by hop distance and finds reachability (and shortest hops).",
    },
    {
        "id": "graph_m_problem",
        "topic": "graphs",
        "difficulty": 2,
        "qtype": "problem",
        "prompt": (
            "Five labs {0,1,2,3,4} have undirected corridors 0-1, 1-2, 3-4. Starting at 0, "
            "which labs are unreachable?"
        ),
        "options": ["3 and 4", "2 only", "1 and 2", "None — the graph is connected"],
        "answer": "3 and 4",
        "explanation": "0-1-2 is one component; 3-4 is a separate component.",
    },
    {
        "id": "graph_m_tracing",
        "topic": "graphs",
        "difficulty": 2,
        "qtype": "tracing",
        "prompt": (
            "Adjacency list: 0:[1,2], 1:[0,3], 2:[0], 3:[1]. BFS from 0, neighbours visited "
            "in listed order. What is a valid visit order?"
        ),
        "options": ["0, 1, 2, 3", "0, 3, 1, 2", "3, 1, 0, 2", "0, 2, 3, 1"],
        "answer": "0, 1, 2, 3",
        "explanation": "Queue processes 0, then 1 and 2, then 3 from 1.",
    },
    {
        "id": "graph_h_concept",
        "topic": "graphs",
        "difficulty": 3,
        "qtype": "concept",
        "prompt": (
            "Road travel times are positive on a directed map. You need the cheapest path "
            "from a depot to every city. Which algorithm is the standard choice?"
        ),
        "options": [
            "Dijkstra's algorithm",
            "Unweighted BFS ignoring travel times",
            "DFS that stops at the first destination found",
            "In-order traversal of cities sorted by name",
        ],
        "answer": "Dijkstra's algorithm",
        "explanation": "Non-negative weighted shortest paths from one source are Dijkstra's setting.",
    },
    # ---- Sorting + searching ----
    {
        "id": "ss_e_concept",
        "topic": "sorting_searching",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "Employee IDs are already sorted. Looking up whether ID 407 exists should use "
            "which approach for logarithmic time?"
        ),
        "options": ["Binary search", "Linear scan from the start every time", "Bubble sort first", "DFS on a grid"],
        "answer": "Binary search",
        "explanation": "Binary search halves a sorted range each step — O(log n).",
    },
    {
        "id": "ss_m_concept",
        "topic": "sorting_searching",
        "difficulty": 2,
        "qtype": "concept",
        "prompt": (
            "You must sort 10⁵ shipment records that do not fit a tiny O(n²) budget. Which "
            "family has O(n log n) worst-case comparisons in standard textbooks?"
        ),
        "options": ["Mergesort (or heapsort)", "Bubble sort", "Insertion sort on the full list", "Bogosort"],
        "answer": "Mergesort (or heapsort)",
        "explanation": "Mergesort and heapsort are classic O(n log n) worst-case comparison sorts.",
    },
    {
        "id": "ss_m_tracing",
        "topic": "sorting_searching",
        "difficulty": 2,
        "qtype": "tracing",
        "prompt": (
            "Binary search for 7 in [1, 3, 5, 7, 9, 11]. The first mid index (low=0, high=5, "
            "integer mid=(low+high)//2) inspects which value?"
        ),
        "options": ["5", "7", "9", "1"],
        "answer": "5",
        "explanation": "mid = (0+5)//2 = 2, and the value there is 5.",
    },
    {
        "id": "ss_h_problem",
        "topic": "sorting_searching",
        "difficulty": 3,
        "qtype": "problem",
        "prompt": (
            "A rotating shift roster is a sorted ID list rotated at an unknown pivot, e.g. "
            "[15, 18, 2, 7, 12]. To find 7 efficiently you should:"
        ),
        "options": [
            "Adapt binary search using the sorted half on each step",
            "Always scan from the left in O(n) as the only correct method",
            "Heapify the roster, then pop until 7 appears",
            "Treat IDs as a graph and run BFS",
        ],
        "answer": "Adapt binary search using the sorted half on each step",
        "explanation": "Rotated-array search keeps the binary-search skeleton by testing which side is sorted.",
    },
    # ---- Dynamic programming ----
    {
        "id": "dp_e_concept",
        "topic": "dynamic_programming",
        "difficulty": 1,
        "qtype": "concept",
        "prompt": (
            "A recursive planner recomputes the same sub-schedule many times. Storing each "
            "sub-result the first time it is solved is called:"
        ),
        "options": ["Memoization", "Two-pointer scanning", "Bit reversal", "Prim's algorithm"],
        "answer": "Memoization",
        "explanation": "Memoization caches recursive subproblems; tabulation fills a table bottom-up.",
    },
    {
        "id": "dp_m_concept",
        "topic": "dynamic_programming",
        "difficulty": 2,
        "qtype": "concept",
        "prompt": (
            "You fill a table from smaller parcel-counts up to n, each cell depending only "
            "on earlier cells. That style is:"
        ),
        "options": ["Tabulation (bottom-up DP)", "Greedy choice with no overlapping subproblems", "Pure DFS with no cache", "Binary search on the answer only"],
        "answer": "Tabulation (bottom-up DP)",
        "explanation": "Bottom-up DP / tabulation iterates from base cases to the full problem.",
    },
    {
        "id": "dp_m_tracing",
        "topic": "dynamic_programming",
        "difficulty": 2,
        "qtype": "tracing",
        "prompt": (
            "Ways to climb a 4-step stair taking 1 or 2 steps at a time (order matters): "
            "let w(0)=1, w(1)=1, w(n)=w(n-1)+w(n-2). What is w(4)?"
        ),
        "options": ["5", "4", "3", "8"],
        "answer": "5",
        "explanation": "w(2)=2, w(3)=3, w(4)=5 — the classic step-combination recurrence.",
    },
    {
        "id": "dp_h_problem",
        "topic": "dynamic_programming",
        "difficulty": 3,
        "qtype": "problem",
        "prompt": (
            "A courier may take or skip each parcel along a line; adjacent parcels cannot "
            "both be taken. Values [4, 1, 6, 7]. What is the maximum total using this "
            "standard recurrence?"
        ),
        "options": ["11", "18", "10", "7"],
        "answer": "11",
        "explanation": "Optimal is 4+7=11 (skip 1 and 6) or 1+7=8 or 4+6=10; 11 wins.",
    },
    {
        "id": "dp_m_coding",
        "topic": "dynamic_programming",
        "difficulty": 2,
        "qtype": "coding",
        "prompt": (
            "Implement solve(n) returning the number of ways to climb n stairs taking 1 or 2 "
            "steps at a time. Use solve(0)=1 and solve(1)=1."
        ),
        "starter": "def solve(n):\n    # number of 1-2 step sequences\n    pass\n",
        "tests": [
            {"args": [4], "expected": 5},
            {"args": [1], "expected": 1},
            {"args": [3], "expected": 3},
        ],
        "explanation": "Fibonacci-style DP: ways(n) = ways(n-1) + ways(n-2).",
    },
]


def load_questions() -> list[dict]:
    bank = list(QUESTIONS) + generate_from_blueprint("skillgap-dsa-v1")
    validate_bank(bank)
    return bank


QUESTION_BANK = load_questions()
QUESTION_BY_ID = {q["id"]: q for q in QUESTION_BANK}
