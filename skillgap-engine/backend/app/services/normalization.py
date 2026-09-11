"""
Skill normalization service.

Maps extracted resume skills to canonical competencies in the system.
Handles variations in terminology (e.g., "Python", "Python Programming", "Python Development"
all map to the canonical "Python Programming" competency).

This prevents duplicate competency records and improves matching accuracy.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Tuple
from fuzzywuzzy import fuzz  # approximate string matching
from sqlalchemy.orm import Session

from app.models.models import Competency


class SkillNormalizer:
    """Normalizes extracted skills to canonical competencies."""
    
    def __init__(self, db: Session):
        """Initialize normalizer with database competency list."""
        self.db = db
        self.competencies = self._load_competencies()
        # Build a lookup map for faster access
        self.competency_map: Dict[str, Competency] = {
            c.name.lower(): c for c in self.competencies
        }
    
    def _load_competencies(self) -> List[Competency]:
        """Load all competencies from database."""
        return self.db.query(Competency).all()
    
    def normalize_skill(self, skill: str, threshold: int = 80) -> Optional[Competency]:
        """
        Normalize a skill string to a canonical competency.
        
        Strategy:
        1. Exact match (case-insensitive)
        2. Fuzzy match with high threshold (80+)
        3. No match -> None
        
        Args:
            skill: The skill string to normalize
            threshold: Fuzzy matching threshold (0-100). Default 80.
        
        Returns:
            Matched Competency or None if no match found
        """
        skill_lower = skill.strip().lower()
        
        # Try exact match first
        if skill_lower in self.competency_map:
            return self.competency_map[skill_lower]
        
        # Try fuzzy match
        best_match: Optional[Tuple[Competency, int]] = None
        for competency in self.competencies:
            score = fuzz.token_set_ratio(skill_lower, competency.name.lower())
            if score >= threshold:
                if best_match is None or score > best_match[1]:
                    best_match = (competency, score)
        
        return best_match[0] if best_match else None
    
    def normalize_skills(self, skills: List[str], threshold: int = 80) -> List[Competency]:
        """
        Normalize a list of skills to canonical competencies.
        Removes duplicates.
        
        Args:
            skills: List of skill strings
            threshold: Fuzzy matching threshold
        
        Returns:
            List of unique Competencies
        """
        seen_ids = set()
        normalized = []
        
        for skill in skills:
            competency = self.normalize_skill(skill, threshold)
            if competency and competency.id not in seen_ids:
                normalized.append(competency)
                seen_ids.add(competency.id)
        
        return normalized
    
    def get_similar_competencies(self, skill: str, top_k: int = 5, threshold: int = 60) -> List[Tuple[Competency, int]]:
        """
        Get semantically similar competencies for a skill that doesn't match exactly.
        Useful for showing suggestions to users.
        
        Args:
            skill: The skill string
            top_k: Number of suggestions to return
            threshold: Minimum fuzzy match score
        
        Returns:
            List of (Competency, match_score) tuples, sorted by score descending
        """
        skill_lower = skill.strip().lower()
        matches: List[Tuple[Competency, int]] = []
        
        for competency in self.competencies:
            score = fuzz.token_set_ratio(skill_lower, competency.name.lower())
            if score >= threshold:
                matches.append((competency, score))
        
        # Sort by score descending, return top_k
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_k]


def normalize_extracted_skills(
    db: Session,
    extracted_skills: List[str],
    threshold: int = 80,
) -> Tuple[List[Competency], Dict[str, Optional[int]]]:
    """
    Normalize extracted resume skills to canonical competencies.
    
    Args:
        db: Database session
        extracted_skills: Raw list of skills from resume extraction
        threshold: Fuzzy matching threshold
    
    Returns:
        Tuple of:
        - List of canonical Competencies
        - Mapping of original skill string -> competency_id (or None if not matched)
    """
    normalizer = SkillNormalizer(db)
    competencies = normalizer.normalize_skills(extracted_skills, threshold)
    
    # Build mapping of original skills to competency IDs
    mapping: Dict[str, Optional[int]] = {}
    for skill in extracted_skills:
        matched = normalizer.normalize_skill(skill, threshold)
        mapping[skill] = matched.id if matched else None
    
    return competencies, mapping
