from typing import Iterable

from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceAssessment,
    EvidenceAssessmentState,
)
from studio.core.models import ResearchResult


MINIMUM_MEANINGFUL_STRENGTH = 0.5
DOMINANCE_MARGIN = 0.2


def _average_confidence(
    evidence_items: Iterable[Evidence],
) -> float:
    evidence_list = list(evidence_items)

    if not evidence_list:
        return 0.0

    total = sum(
        evidence.confidence
        for evidence in evidence_list
    )

    return total / len(evidence_list)


def _collect_supporting_evidence(
    claims: Iterable[Claim],
) -> list[Evidence]:
    evidence_items: list[Evidence] = []

    for claim in claims:
        evidence_items.extend(
            claim.supporting_evidence
        )

    return evidence_items


def _collect_counter_evidence(
    claims: Iterable[Claim],
) -> list[Evidence]:
    evidence_items: list[Evidence] = []

    for claim in claims:
        evidence_items.extend(
            claim.counter_evidence
        )

    return evidence_items


def _determine_state(
    supporting_strength: float,
    counter_strength: float,
) -> EvidenceAssessmentState:
    if (
        supporting_strength < MINIMUM_MEANINGFUL_STRENGTH
        and counter_strength < MINIMUM_MEANINGFUL_STRENGTH
    ):
        return EvidenceAssessmentState.INSUFFICIENT

    if (
        supporting_strength >= MINIMUM_MEANINGFUL_STRENGTH
        and supporting_strength - counter_strength
        >= DOMINANCE_MARGIN
    ):
        return EvidenceAssessmentState.SUPPORTING

    if (
        counter_strength >= MINIMUM_MEANINGFUL_STRENGTH
        and counter_strength - supporting_strength
        >= DOMINANCE_MARGIN
    ):
        return EvidenceAssessmentState.CONTRADICTORY

    return EvidenceAssessmentState.MIXED


def _assessment_confidence(
    supporting_strength: float,
    counter_strength: float,
    state: EvidenceAssessmentState,
) -> float:
    if state == EvidenceAssessmentState.INSUFFICIENT:
        return max(
            supporting_strength,
            counter_strength,
        )

    if state == EvidenceAssessmentState.MIXED:
        return abs(
            supporting_strength - counter_strength
        )

    return max(
        supporting_strength,
        counter_strength,
    )


def _build_rationale(
    state: EvidenceAssessmentState,
    supporting_strength: float,
    counter_strength: float,
) -> str:
    if state == EvidenceAssessmentState.SUPPORTING:
        return (
            "Supporting evidence materially outweighs "
            "counter-evidence."
        )

    if state == EvidenceAssessmentState.CONTRADICTORY:
        return (
            "Counter-evidence materially outweighs "
            "supporting evidence."
        )

    if state == EvidenceAssessmentState.MIXED:
        return (
            "Meaningful supporting and contradictory "
            "evidence are both present without clear dominance."
        )

    return (
        "Available evidence is too weak or insufficient "
        "for a stronger assessment."
    )


def assess_research_evidence(
    research_result: ResearchResult,
) -> EvidenceAssessment:
    if not isinstance(research_result, ResearchResult):
        raise TypeError(
            "research_result must be a ResearchResult."
        )

    supporting_evidence = _collect_supporting_evidence(
        research_result.claims
    )

    counter_evidence = _collect_counter_evidence(
        research_result.claims
    )

    supporting_strength = _average_confidence(
        supporting_evidence
    )

    counter_strength = _average_confidence(
        counter_evidence
    )

    state = _determine_state(
        supporting_strength,
        counter_strength,
    )

    confidence = _assessment_confidence(
        supporting_strength,
        counter_strength,
        state,
    )

    rationale = _build_rationale(
        state,
        supporting_strength,
        counter_strength,
    )

    return EvidenceAssessment(
        state=state,
        supporting_strength=supporting_strength,
        counter_strength=counter_strength,
        confidence=confidence,
        rationale=rationale,
    )