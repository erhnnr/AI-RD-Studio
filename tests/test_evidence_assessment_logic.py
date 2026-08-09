import pytest

from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceAssessmentState,
    EvidenceSource,
)
from studio.core.evidence_assessment import (
    DOMINANCE_MARGIN,
    MINIMUM_MEANINGFUL_STRENGTH,
    assess_research_evidence,
)
from studio.core.models import ResearchResult


def make_evidence(
    confidence: float,
    content: str = "Controlled evidence.",
) -> Evidence:
    source = EvidenceSource(
        name="Controlled Source",
        source_type="test",
    )

    return Evidence(
        content=content,
        source=source,
        confidence=confidence,
    )


def make_result(
    supporting=None,
    counter=None,
) -> ResearchResult:
    supporting = supporting or []
    counter = counter or []

    claim = Claim(
        statement="Controlled claim.",
        supporting_evidence=supporting,
        counter_evidence=counter,
        confidence=0.5,
    )

    return ResearchResult(
        analysis="Controlled research.",
        claims=[claim],
    )


def test_assessment_constants_are_explicit():
    assert MINIMUM_MEANINGFUL_STRENGTH == 0.5
    assert DOMINANCE_MARGIN == 0.2


def test_strong_supporting_evidence_is_supporting():
    result = make_result(
        supporting=[
            make_evidence(0.9),
            make_evidence(0.8),
        ],
        counter=[
            make_evidence(0.2),
        ],
    )

    assessment = assess_research_evidence(result)

    assert (
        assessment.state
        == EvidenceAssessmentState.SUPPORTING
    )
    assert assessment.supporting_strength == pytest.approx(0.85)
    assert assessment.counter_strength == pytest.approx(0.2)


def test_strong_counter_evidence_is_contradictory():
    result = make_result(
        supporting=[
            make_evidence(0.2),
        ],
        counter=[
            make_evidence(0.9),
            make_evidence(0.8),
        ],
    )

    assessment = assess_research_evidence(result)

    assert (
        assessment.state
        == EvidenceAssessmentState.CONTRADICTORY
    )
    assert assessment.supporting_strength == pytest.approx(0.2)
    assert assessment.counter_strength == pytest.approx(0.85)


def test_balanced_strong_evidence_is_mixed():
    result = make_result(
        supporting=[
            make_evidence(0.8),
        ],
        counter=[
            make_evidence(0.7),
        ],
    )

    assessment = assess_research_evidence(result)

    assert (
        assessment.state
        == EvidenceAssessmentState.MIXED
    )


def test_weak_evidence_is_insufficient():
    result = make_result(
        supporting=[
            make_evidence(0.3),
        ],
        counter=[
            make_evidence(0.1),
        ],
    )

    assessment = assess_research_evidence(result)

    assert (
        assessment.state
        == EvidenceAssessmentState.INSUFFICIENT
    )


def test_no_claims_is_insufficient():
    result = ResearchResult(
        analysis="No structured evidence.",
    )

    assessment = assess_research_evidence(result)

    assert (
        assessment.state
        == EvidenceAssessmentState.INSUFFICIENT
    )
    assert assessment.supporting_strength == 0.0
    assert assessment.counter_strength == 0.0
    assert assessment.confidence == 0.0


def test_multiple_claims_are_aggregated():
    claim_one = Claim(
        statement="First claim.",
        supporting_evidence=[
            make_evidence(0.8),
        ],
        confidence=0.7,
    )

    claim_two = Claim(
        statement="Second claim.",
        supporting_evidence=[
            make_evidence(0.6),
        ],
        counter_evidence=[
            make_evidence(0.2),
        ],
        confidence=0.6,
    )

    result = ResearchResult(
        analysis="Multiple claims.",
        claims=[
            claim_one,
            claim_two,
        ],
    )

    assessment = assess_research_evidence(result)

    assert assessment.supporting_strength == pytest.approx(0.7)
    assert assessment.counter_strength == pytest.approx(0.2)
    assert (
        assessment.state
        == EvidenceAssessmentState.SUPPORTING
    )


def test_mixed_state_confidence_reflects_difference():
    result = make_result(
        supporting=[
            make_evidence(0.8),
        ],
        counter=[
            make_evidence(0.7),
        ],
    )

    assessment = assess_research_evidence(result)

    assert assessment.confidence == pytest.approx(0.1)


def test_rejects_non_research_result():
    with pytest.raises(
        TypeError,
        match="must be a ResearchResult",
    ):
        assess_research_evidence(
            "not research"
        )