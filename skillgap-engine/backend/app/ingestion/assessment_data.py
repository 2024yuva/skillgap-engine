"""
DSA Assessment question bank.

These are original questions created for the SkillGap Engine assessment system.
They are NOT copied from LeetCode, GeeksforGeeks, HackerRank or any other
competitive programming platform.

Question types:
  mcq       — multiple choice (4 options, 1 correct)
  trace     — code tracing: what does this code output?
  complexity — time/space complexity analysis

Topics and approximate distribution:
  Arrays & Strings     — 4 questions
  Hashing              — 3 questions
  Two Pointers / Sliding Window — 3 questions
  Linked Lists         — 3 questions
  Stack & Queue        — 3 questions
  Trees / BST          — 4 questions
  Graphs               — 3 questions
  Sorting & Searching  — 3 questions
  Dynamic Programming  — 4 questions
  Total: 30 questions
"""

from __future__ import annotations
from typing import Any

DSA_QUESTIONS: list[dict[str, Any]] = [

    # ─────────────────────────────────────────────────────────────────────────
    # ARRAYS & STRINGS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 1,
        "topic": "Arrays & Strings",
        "question_text": "An array contains n integers. You want to find the maximum sum of any contiguous subarray. Which approach gives the optimal time complexity?",
        "question_type": "mcq",
        "options": [
            "A) Sort the array first, then sum from both ends",
            "B) Use a divide-and-conquer approach that runs in O(n log n)",
            "C) Use Kadane's algorithm, tracking a running maximum in a single pass",
            "D) Check all pairs of start and end indices using two nested loops"
        ],
        "correct_answer": "C",
        "explanation": "Kadane's algorithm scans the array once, maintaining a running current-sum and updating a global maximum, giving O(n) time and O(1) space.",
        "difficulty": "easy",
    },
    {
        "id": 2,
        "topic": "Arrays & Strings",
        "question_text": "What does the following Python snippet print?\n\narr = [1, 2, 3, 4, 5]\nresult = []\nfor i in range(len(arr) - 1, -1, -1):\n    result.append(arr[i])\nprint(result)",
        "question_type": "trace",
        "options": None,
        "correct_answer": "[5, 4, 3, 2, 1]",
        "explanation": "The loop iterates from index 4 down to 0, appending each element, so the output is the reverse of the original array.",
        "difficulty": "easy",
    },
    {
        "id": 3,
        "topic": "Arrays & Strings",
        "question_text": "You are given a string s. You want to check whether any permutation of s is a palindrome. Which condition must hold?",
        "question_type": "mcq",
        "options": [
            "A) All characters must appear an even number of times",
            "B) At most one character may appear an odd number of times",
            "C) The string must already be sorted",
            "D) The string length must be even"
        ],
        "correct_answer": "B",
        "explanation": "A palindrome can have at most one character with an odd frequency (the middle character). Even-length palindromes require all counts to be even.",
        "difficulty": "medium",
    },
    {
        "id": 4,
        "topic": "Arrays & Strings",
        "question_text": "What is the time complexity of rotating an array of n elements to the right by k positions using the reversal algorithm (reverse full array, reverse first k, reverse remaining)?",
        "question_type": "complexity",
        "options": [
            "A) O(n log n)",
            "B) O(k)",
            "C) O(n)",
            "D) O(n * k)"
        ],
        "correct_answer": "C",
        "explanation": "The reversal algorithm performs three reversal passes, each O(n) in the worst case, for a total of O(n) time and O(1) space.",
        "difficulty": "medium",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # HASHING
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 5,
        "topic": "Hashing",
        "question_text": "You have an unsorted array of integers. You want to determine whether any two distinct elements sum to a given target value T. What is the optimal approach?",
        "question_type": "mcq",
        "options": [
            "A) Sort and binary-search for the complement — O(n log n)",
            "B) Store each element in a hash set and check if (T - element) exists — O(n)",
            "C) Check all pairs with two nested loops — O(n²)",
            "D) Use a priority queue to compare elements — O(n log n)"
        ],
        "correct_answer": "B",
        "explanation": "A hash set gives O(1) average-case lookup. For each element x, check if T - x is already in the set. Total time: O(n).",
        "difficulty": "easy",
    },
    {
        "id": 6,
        "topic": "Hashing",
        "question_text": "What does this Python code print?\n\nfrom collections import Counter\nwords = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']\nc = Counter(words)\nprint(c.most_common(2))",
        "question_type": "trace",
        "options": None,
        "correct_answer": "[('apple', 3), ('banana', 2)]",
        "explanation": "Counter counts occurrences: apple=3, banana=2, cherry=1. most_common(2) returns the two most frequent items as (element, count) tuples.",
        "difficulty": "easy",
    },
    {
        "id": 7,
        "topic": "Hashing",
        "question_text": "A hash table uses chaining for collision resolution. In the worst case (all keys hash to the same bucket), what is the time complexity of a lookup?",
        "question_type": "complexity",
        "options": [
            "A) O(1)",
            "B) O(log n)",
            "C) O(n)",
            "D) O(n²)"
        ],
        "correct_answer": "C",
        "explanation": "If all n keys collide, the chain is effectively a linked list, and lookup degrades to O(n). Average case with a good hash function is O(1).",
        "difficulty": "medium",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # TWO POINTERS / SLIDING WINDOW
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 8,
        "topic": "Two Pointers / Sliding Window",
        "question_text": "You need to find the length of the longest subarray containing at most k distinct integers. Which technique is most appropriate?",
        "question_type": "mcq",
        "options": [
            "A) Brute force — check all subarrays",
            "B) Sliding window with a frequency hash map",
            "C) Binary search on the answer",
            "D) Depth-first search"
        ],
        "correct_answer": "B",
        "explanation": "A sliding window with a hash map tracking element frequencies allows O(n) amortised solution: expand right, shrink left when distinct count exceeds k.",
        "difficulty": "medium",
    },
    {
        "id": 9,
        "topic": "Two Pointers / Sliding Window",
        "question_text": "Given a sorted array and a target sum, which approach finds a pair of elements summing to the target in O(n) time and O(1) space?",
        "question_type": "mcq",
        "options": [
            "A) Two nested loops",
            "B) One pointer at each end, move inward based on the sum",
            "C) Hashing each element",
            "D) Binary search for each element"
        ],
        "correct_answer": "B",
        "explanation": "Since the array is sorted, start with left=0 and right=n-1. If sum is too large, decrement right; if too small, increment left. This is O(n).",
        "difficulty": "easy",
    },
    {
        "id": 10,
        "topic": "Two Pointers / Sliding Window",
        "question_text": "A fixed-size sliding window of size k moves across an array of n elements. How many window positions exist?",
        "question_type": "complexity",
        "options": [
            "A) k",
            "B) n",
            "C) n - k + 1",
            "D) n * k"
        ],
        "correct_answer": "C",
        "explanation": "The window can start at index 0, 1, …, n-k, giving n - k + 1 positions.",
        "difficulty": "easy",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # LINKED LISTS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 11,
        "topic": "Linked Lists",
        "question_text": "You want to detect whether a singly linked list has a cycle. Which approach uses O(1) extra space?",
        "question_type": "mcq",
        "options": [
            "A) Store all visited node addresses in a hash set",
            "B) Mark each node with a visited flag by modifying the node value",
            "C) Use two pointers: one advances one step, the other two steps",
            "D) Reverse the list and compare with the original"
        ],
        "correct_answer": "C",
        "explanation": "Floyd's cycle-detection (tortoise and hare): the fast pointer catches the slow pointer if a cycle exists. O(n) time, O(1) space.",
        "difficulty": "medium",
    },
    {
        "id": 12,
        "topic": "Linked Lists",
        "question_text": "What is the time complexity of inserting a new node at the beginning of a singly linked list?",
        "question_type": "complexity",
        "options": [
            "A) O(n)",
            "B) O(log n)",
            "C) O(1)",
            "D) O(n²)"
        ],
        "correct_answer": "C",
        "explanation": "Prepending requires only updating the new node's next pointer and the head reference — constant time regardless of list length.",
        "difficulty": "easy",
    },
    {
        "id": 13,
        "topic": "Linked Lists",
        "question_text": "To find the k-th node from the end of a linked list in a single pass, what is the best strategy?",
        "question_type": "mcq",
        "options": [
            "A) Traverse to the end, then count backward",
            "B) Use two pointers k nodes apart; advance both until the front reaches the end",
            "C) Store all nodes in an array and index from the end",
            "D) Reverse the list and take the k-th element"
        ],
        "correct_answer": "B",
        "explanation": "Start the leading pointer k nodes ahead. When it reaches the end, the trailing pointer is at the k-th node from the end. Single pass, O(n) time, O(1) space.",
        "difficulty": "medium",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # STACK & QUEUE
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 14,
        "topic": "Stack & Queue",
        "question_text": "What does the following code print?\n\nstack = []\nfor x in [3, 1, 4, 1, 5]:\n    stack.append(x)\nresult = []\nwhile stack:\n    result.append(stack.pop())\nprint(result)",
        "question_type": "trace",
        "options": None,
        "correct_answer": "[5, 1, 4, 1, 3]",
        "explanation": "Elements are pushed onto the stack in order. Popping yields LIFO order, reversing the sequence.",
        "difficulty": "easy",
    },
    {
        "id": 15,
        "topic": "Stack & Queue",
        "question_text": "You need to evaluate a sequence of balanced parentheses to check validity. Which data structure is most naturally suited?",
        "question_type": "mcq",
        "options": [
            "A) Queue (FIFO)",
            "B) Stack (LIFO)",
            "C) Heap (priority queue)",
            "D) Hash map"
        ],
        "correct_answer": "B",
        "explanation": "Push opening brackets onto a stack; when a closing bracket appears, pop and verify it matches. A stack naturally tracks the nesting order.",
        "difficulty": "easy",
    },
    {
        "id": 16,
        "topic": "Stack & Queue",
        "question_text": "How can a queue be implemented using two stacks such that enqueue is O(1) amortised and dequeue is O(1) amortised?",
        "question_type": "mcq",
        "options": [
            "A) Always copy all elements between the stacks on each operation",
            "B) Push to stack1 on enqueue; lazy-transfer all to stack2 only when stack2 is empty on dequeue",
            "C) Maintain both stacks in sorted order at all times",
            "D) Use only one stack with recursive dequeue"
        ],
        "correct_answer": "B",
        "explanation": "Lazy transfer: enqueue always pushes to stack1 (O(1)). Dequeue uses stack2 if non-empty, otherwise reverses stack1 into stack2. Each element is moved at most once, giving O(1) amortised dequeue.",
        "difficulty": "hard",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # TREES / BST
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 17,
        "topic": "Trees / BST",
        "question_text": "In an in-order traversal of a Binary Search Tree, the output is:",
        "question_type": "mcq",
        "options": [
            "A) Nodes in reverse sorted order",
            "B) Nodes in sorted (ascending) order",
            "C) Nodes in level-order (BFS) order",
            "D) Nodes in insertion order"
        ],
        "correct_answer": "B",
        "explanation": "BST in-order traversal visits left subtree, then root, then right subtree, producing elements in ascending order.",
        "difficulty": "easy",
    },
    {
        "id": 18,
        "topic": "Trees / BST",
        "question_text": "What does the following recursive function compute for a binary tree?\n\ndef f(node):\n    if node is None:\n        return 0\n    return 1 + max(f(node.left), f(node.right))",
        "question_type": "trace",
        "options": None,
        "correct_answer": "The height (depth) of the binary tree",
        "explanation": "The base case returns 0 for None. Recursively, each node adds 1 to the maximum depth of its children, yielding the tree height.",
        "difficulty": "medium",
    },
    {
        "id": 19,
        "topic": "Trees / BST",
        "question_text": "What is the average-case time complexity for search in a balanced BST with n nodes?",
        "question_type": "complexity",
        "options": [
            "A) O(n)",
            "B) O(n log n)",
            "C) O(log n)",
            "D) O(1)"
        ],
        "correct_answer": "C",
        "explanation": "Each comparison eliminates half the remaining nodes in a balanced BST, giving O(log n) average search time.",
        "difficulty": "easy",
    },
    {
        "id": 20,
        "topic": "Trees / BST",
        "question_text": "Which traversal algorithm is typically used to print the nodes of a binary tree level by level?",
        "question_type": "mcq",
        "options": [
            "A) In-order DFS",
            "B) Pre-order DFS",
            "C) Post-order DFS",
            "D) Breadth-first search (BFS) using a queue"
        ],
        "correct_answer": "D",
        "explanation": "BFS processes all nodes at depth d before depth d+1, naturally producing level-order output. A queue manages the frontier.",
        "difficulty": "easy",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # GRAPHS
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 21,
        "topic": "Graphs",
        "question_text": "You need to find the shortest path (fewest edges) between two nodes in an unweighted graph. Which algorithm is correct?",
        "question_type": "mcq",
        "options": [
            "A) Depth-first search (DFS)",
            "B) Dijkstra's algorithm",
            "C) Breadth-first search (BFS)",
            "D) Bellman-Ford algorithm"
        ],
        "correct_answer": "C",
        "explanation": "BFS explores nodes layer by layer (edge count), guaranteeing the shortest path in an unweighted graph. Dijkstra handles weighted graphs.",
        "difficulty": "easy",
    },
    {
        "id": 22,
        "topic": "Graphs",
        "question_text": "Which algorithm detects whether a directed graph contains a cycle?",
        "question_type": "mcq",
        "options": [
            "A) BFS from every node",
            "B) DFS with a 'currently visiting' colour state",
            "C) Topological sort (Kahn's algorithm) checks for remaining in-degree nodes",
            "D) Both B and C are correct"
        ],
        "correct_answer": "D",
        "explanation": "DFS with three-colour marking detects back edges (cycles). Kahn's topological sort detects cycles if not all nodes can be ordered (remaining non-zero in-degrees after BFS).",
        "difficulty": "hard",
    },
    {
        "id": 23,
        "topic": "Graphs",
        "question_text": "For a graph with V vertices and E edges stored as an adjacency list, what is the time complexity of running DFS?",
        "question_type": "complexity",
        "options": [
            "A) O(V²)",
            "B) O(V + E)",
            "C) O(E log V)",
            "D) O(V * E)"
        ],
        "correct_answer": "B",
        "explanation": "DFS visits each vertex once and processes each edge once, giving O(V + E). An adjacency matrix representation would give O(V²).",
        "difficulty": "medium",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # SORTING & SEARCHING
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 24,
        "topic": "Sorting & Searching",
        "question_text": "Which sorting algorithm has the best worst-case time complexity?",
        "question_type": "mcq",
        "options": [
            "A) Quick Sort — O(n log n)",
            "B) Merge Sort — O(n log n)",
            "C) Heap Sort — O(n log n)",
            "D) Both B and C, since Quick Sort degrades to O(n²)"
        ],
        "correct_answer": "D",
        "explanation": "Merge Sort and Heap Sort guarantee O(n log n) in all cases. Quick Sort's worst case (e.g., sorted input with naive pivot) is O(n²).",
        "difficulty": "medium",
    },
    {
        "id": 25,
        "topic": "Sorting & Searching",
        "question_text": "Binary search on a sorted array of n elements finds the target in how many comparisons at most?",
        "question_type": "complexity",
        "options": [
            "A) O(n)",
            "B) O(√n)",
            "C) O(log₂ n)",
            "D) O(n/2)"
        ],
        "correct_answer": "C",
        "explanation": "Binary search halves the search space each step, so the number of steps is at most ⌈log₂ n⌉.",
        "difficulty": "easy",
    },
    {
        "id": 26,
        "topic": "Sorting & Searching",
        "question_text": "Counting sort can sort n integers in O(n + k) where k is the range. When is it significantly better than comparison-based sorting?",
        "question_type": "mcq",
        "options": [
            "A) When k ≫ n (range much larger than array)",
            "B) When k is small relative to n, making O(n + k) ≈ O(n)",
            "C) When the array is already nearly sorted",
            "D) When sorting floating-point numbers"
        ],
        "correct_answer": "B",
        "explanation": "Counting sort shines when k = O(n), giving true O(n) time. If k ≫ n, the k-sized count array dominates and it becomes worse than comparison sorts.",
        "difficulty": "medium",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # DYNAMIC PROGRAMMING
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 27,
        "topic": "Dynamic Programming",
        "question_text": "Which property must a problem have for dynamic programming to be applicable?",
        "question_type": "mcq",
        "options": [
            "A) Greedy choice property only",
            "B) Optimal substructure AND overlapping subproblems",
            "C) The problem must be solvable in polynomial time",
            "D) The state space must be one-dimensional"
        ],
        "correct_answer": "B",
        "explanation": "DP requires optimal substructure (optimal solution built from optimal sub-solutions) and overlapping subproblems (same sub-problems solved multiple times).",
        "difficulty": "medium",
    },
    {
        "id": 28,
        "topic": "Dynamic Programming",
        "question_text": "What does the following DP code compute?\n\ndef dp(n):\n    if n <= 1: return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\nprint(dp(7))",
        "question_type": "trace",
        "options": None,
        "correct_answer": "13",
        "explanation": "This computes the nth Fibonacci number iteratively. dp(7) = 13 (F0=0,F1=1,F2=1,F3=2,F4=3,F5=5,F6=8,F7=13).",
        "difficulty": "easy",
    },
    {
        "id": 29,
        "topic": "Dynamic Programming",
        "question_text": "The 0/1 Knapsack problem has n items and a knapsack capacity W. The standard DP solution has time complexity:",
        "question_type": "complexity",
        "options": [
            "A) O(n log W)",
            "B) O(n + W)",
            "C) O(n * W)",
            "D) O(2ⁿ)"
        ],
        "correct_answer": "C",
        "explanation": "The 2D DP table has n rows and W+1 columns, so filling it requires O(n * W) operations.",
        "difficulty": "medium",
    },
    {
        "id": 30,
        "topic": "Dynamic Programming",
        "question_text": "When computing the Longest Common Subsequence (LCS) of two strings of lengths m and n, the standard DP solution uses a table of size:",
        "question_type": "complexity",
        "options": [
            "A) O(m + n) time, O(1) space",
            "B) O(m * n) time, O(m * n) space",
            "C) O(m * n) time, O(min(m, n)) space with row optimization",
            "D) Both B and C are achievable"
        ],
        "correct_answer": "D",
        "explanation": "Standard LCS DP is O(m*n) time and space. Space can be reduced to O(min(m,n)) by only keeping two rows at a time, while time remains O(m*n).",
        "difficulty": "hard",
    },
]

# Topic list in order (for UI display)
DSA_TOPICS = [
    "Arrays & Strings",
    "Hashing",
    "Two Pointers / Sliding Window",
    "Linked Lists",
    "Stack & Queue",
    "Trees / BST",
    "Graphs",
    "Sorting & Searching",
    "Dynamic Programming",
]

# DSA competency ID in our catalogue
DSA_COMPETENCY_ID = 4
DSA_COMPETENCY_NAME = "Data Structures & Algorithms"
