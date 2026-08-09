import pytest

from studio.core.evidence import (
    EvidenceAssessment,
    EvidenceAssessmentState,
)


def test_create_supporting_evidence_assessment():
    assessment = EvidenceAssessment(
        state=EvidenceAssessmentState.SUPPORTING,
        supporting_strength=0.9,
        counter_strength=0.1,
        confidence=0.8,
        rationale="Supporting evidence clearly outweighs counter-evidence.",
    )

    assert assessment.state == EvidenceAssessmentState.SUPPORTING
    assert assessment.supporting_strength == 0.9
    assert assessment.counter_strength == 0.1
    assert assessment.confidence == 0.8
    assert (
        assessment.rationale
        == "Supporting evidence clearly outweighs counter-evidence."
    )


def test_create_contradictory_evidence_assessment():
    assessment = EvidenceAssessment(
        state=EvidenceAssessmentState.CONTRADICTORY,
        supporting_strength=0.2,
        counter_strength=0.9,
        confidence=0.8,
        rationale="Counter-evidence clearly outweighs supporting evidence.",
    )

    assert assessment.state == EvidenceAssessmentState.CONTRADICTORY
    assert assessment.counter_strength > assessment.supporting_strength


def test_create_mixed_evidence_assessment():
    assessment = EvidenceAssessment(
        state=EvidenceAssessmentState.MIXED,
        supporting_strength=0.8,
        counter_strength=0.7,
        confidence=0.5,
        rationale="Meaningful evidence exists on both sides.",
    )

    assert assessment.state == EvidenceAssessmentState.MIXED


def test_create_insufficient_evidence_assessment():
    assessment = EvidenceAssessment(
        state=EvidenceAssessmentState.INSUFFICIENT,
        supporting_strength=0.1,
        counter_strength=0.0,
        confidence=0.2,
        rationale="Available evidence is insufficient.",
    )

    assert assessment.state == EvidenceAssessmentState.INSUFFICIENT


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("supporting_strength", -0.1),
        ("supporting_strength", 1.1),
        ("counter_strength", -0.1),
        ("counter_strength", 1.1),
        ("confidence", -0.1),
        ("confidence", 1.1),
    ],
)
def test_evidence_assessment_rejects_out_of_range_values(
    field_name,
    value,
):
    values = {
        "supporting_strength": 0.5,
        "counter_strength": 0.5,
        "confidence": 0.5,
    }

    values[field_name] = value

    with pytest.raises(ValueError):
        EvidenceAssessment(
            state=EvidenceAssessmentState.MIXED,
            supporting_strength=values["supporting_strength"],
            counter_strength=values["counter_strength"],
            confidence=values["confidence"],
            rationale="Controlled test rationale.",
        )


def test_evidence_assessment_rejects_invalid_state():
    with pytest.raises(TypeError):
        EvidenceAssessment(
            state="SUPPORTING",
            supporting_strength=0.8,
            counter_strength=0.1,
            confidence=0.7,
            rationale="Controlled test rationale.",
        )


def test_evidence_assessment_rejects_empty_rationale():
    with pytest.raises(ValueError):
        EvidenceAssessment(
            state=EvidenceAssessmentState.INSUFFICIENT,
            supporting_strength=0.0,
            counter_strength=0.0,
            confidence=0.0,
            rationale="",
        )