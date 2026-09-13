"""
Competency classification service.

Maps numerical gap data to user-friendly classifications:
- STRONG_MATCH: Clear evidence, requirement met
- RELATED: Related technology/experience found, not direct match
- NEEDS_VERIFICATION: Some evidence, confidence below threshold
- NEEDS_DEVELOPMENT: Evidence exists but below required level
- MISSING_EVIDENCE: No meaningful evidence found
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class CompetencyClassification(str, Enum):
    """User-facing competency classification."""
    STRONG_MATCH = "strong_match"
    RELATED = "related"
    NEEDS_VERIFICATION = "needs_verification"
    NEEDS_DEVELOPMENT = "needs_development"
    MISSING_EVIDENCE = "missing_evidence"


@dataclass
class ClassifiedCompetency:
    """Competency with classification and explanation."""
    competency_id: int
    competency_name: str
    category: str
    
    # Numerical values (internal)
    current_level: int
    required_level: int
    gap: int
    importance: float
    priority_score: float
    
    # Evidence and confidence
    evidence: Optional[str]
    evidence_source: Optional[str]
    confidence: float
    
    # Classification
    classification: CompetencyClassification
    explanation: str
    
    # Verification
    verification_status: str  # unverified, needs_assessment, verified
    verified_level: Optional[int] = None
    
    # Assessment result (if taken)
    assessment_score: Optional[float] = None


def classify_competency(
    competency_id: int,
    competency_name: str,
    category: str,
    current_level: int,
    required_level: int,
    gap: int,
    importance: float,
    priority_score: float,
    evidence: Optional[str],
    evidence_source: Optional[str],
    confidence: float,
    verification_status: str = "unverified",
    verified_level: Optional[int] = None,
    assessment_score: Optional[float] = None,
) -> ClassifiedCompetency:
    """
    Classify a competency based on gap, evidence, and confidence.
    
    Logic:
    1. If verified_level exists and meets requirement → STRONG_MATCH
    2. If gap == 0 (current >= required) → STRONG_MATCH
    3. If gap > 0 and confidence < 0.5 and evidence exists → RELATED
    4. If gap > 0 and confidence < 0.6 → NEEDS_VERIFICATION
    5. If gap > 0 and current_level > 0 → NEEDS_DEVELOPMENT
    6. If no evidence and current_level == 0 → MISSING_EVIDENCE
    """
    
    classification: CompetencyClassification
    explanation: str
    
    # Rule 1: Verified and sufficient
    if verified_level is not None and verified_level >= required_level:
        classification = CompetencyClassification.STRONG_MATCH
        explanation = f"Your verified proficiency in {competency_name} meets the role requirement."
    
    # Rule 2: Gap is zero (current >= required)
    elif gap == 0:
        classification = CompetencyClassification.STRONG_MATCH
        explanation = (
            f"Your demonstrated {competency_name} experience meets the role requirement. "
            f"Evidence: {evidence_source or 'resume/profile'}."
        )
        if evidence:
            explanation += f" Details: {evidence}"
    
    # Rule 3: Low confidence but evidence exists → RELATED
    elif gap > 0 and confidence < 0.5 and evidence:
        classification = CompetencyClassification.RELATED
        explanation = (
            f"Your {evidence_source or 'experience'} suggests related knowledge in {competency_name}, "
            f"though the system cannot confirm proficiency with high confidence. "
            f"Details: {evidence}"
        )
    
    # Rule 4: Gap exists, medium-low confidence → NEEDS_VERIFICATION
    elif gap > 0 and confidence < 0.6:
        if current_level > 0:
            classification = CompetencyClassification.NEEDS_VERIFICATION
            explanation = (
                f"Your profile shows some experience with {competency_name}, "
                f"but the system needs verification of your proficiency level to accurately assess your fit. "
                f"Consider taking a quick skill assessment."
            )
        else:
            classification = CompetencyClassification.NEEDS_VERIFICATION
            explanation = (
                f"The system could not confidently determine your {competency_name} proficiency. "
                f"This is important for your {category} goals. "
                f"Consider taking a quick assessment or providing more information."
            )
    
    # Rule 5: Gap exists, current level > 0 → NEEDS_DEVELOPMENT
    elif gap > 0 and current_level > 0:
        classification = CompetencyClassification.NEEDS_DEVELOPMENT
        explanation = (
            f"Your {competency_name} experience is below the role requirement. "
            f"Evidence: {evidence_source or 'profile'}. "
            f"Development recommended."
        )
        if evidence:
            explanation += f" Current experience: {evidence}"
    
    # Rule 6: No evidence, no current level → MISSING_EVIDENCE
    else:
        classification = CompetencyClassification.MISSING_EVIDENCE
        explanation = (
            f"We could not find evidence of {competency_name} in your profile. "
            f"This is important for your target role. "
            f"Learning resources are available to help you develop this competency."
        )
    
    return ClassifiedCompetency(
        competency_id=competency_id,
        competency_name=competency_name,
        category=category,
        current_level=current_level,
        required_level=required_level,
        gap=gap,
        importance=importance,
        priority_score=priority_score,
        evidence=evidence,
        evidence_source=evidence_source,
        confidence=confidence,
        classification=classification,
        explanation=explanation,
        verification_status=verification_status,
        verified_level=verified_level,
        assessment_score=assessment_score,
    )
