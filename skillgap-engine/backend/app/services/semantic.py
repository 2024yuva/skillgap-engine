"""
Semantic similarity service using Sentence Transformers.

Used ONLY for:
- Matching free-text role/course descriptions to competency names
  when no explicit competency link exists.

NOT used for gap calculation, priority, or course ranking
(those are deterministic in gap_engine.py).
"""

from __future__ import annotations
from typing import List, Tuple
import threading

_model = None
_model_lock = threading.Lock()

MODEL_NAME = "all-MiniLM-L6-v2"


def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer
                _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed(texts: List[str]):
    """Encode a list of strings to embeddings."""
    model = _get_model()
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)


def top_matches(
    query: str,
    candidates: List[str],
    top_k: int = 5,
    threshold: float = 0.35,
) -> List[Tuple[int, str, float]]:
    """
    Return (index, candidate, score) tuples for the top_k most similar
    candidates above the threshold.
    """
    import numpy as np

    if not candidates:
        return []

    query_emb = embed([query])[0]
    cand_embs = embed(candidates)

    # cosine similarity
    query_norm = query_emb / (np.linalg.norm(query_emb) + 1e-10)
    cand_norms = cand_embs / (np.linalg.norm(cand_embs, axis=1, keepdims=True) + 1e-10)
    scores = cand_norms @ query_norm

    indexed = sorted(enumerate(scores.tolist()), key=lambda x: x[1], reverse=True)
    results = [
        (idx, candidates[idx], score)
        for idx, score in indexed
        if score >= threshold
    ]
    return results[:top_k]
