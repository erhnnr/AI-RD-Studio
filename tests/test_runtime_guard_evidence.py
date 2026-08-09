import pytest

from studio.core.evidence import Claim, Evidence, EvidenceSource
from studio.core.models import ResearchResult, Signal
from studio.runtime.runtime_guard import (
    RuntimeGuard,
    RuntimeValidationError,
)


def make_signal() -> Signal:
    return Signal(
        title="Evidence Test Signal",
        description="Controlled runtime evidence test.",
        source="test",
    )


def make_valid_claim() -> Claim:
    source = EvidenceSource(
        name="Controlled Source",
        source_type="test",
    )

    evidence = Evidence(
        content="Controlled supporting evidence.",
        source=source,
        confidence=0.8,
    )

    return Claim(
        statement="Controlled claim.",
        supporting_evidence=[evidence],
        confidence=0.7,
        uncertainty="Limited to the controlled test.",
    )


def test_runtime_guard_accepts_valid_structured_research_result():
    result = ResearchResult(
        analysis="Controlled research.",
        signal=make_signal(),
        claims=[make_valid_claim()],
    )

    RuntimeGuard.validate_research_result(result)


def test_runtime_guard_accepts_research_result_without_claims():
    result = ResearchResult(
        analysis="Legacy-compatible research.",
        signal=make_signal(),
    )

    RuntimeGuard.validate_research_result(result)


def test_runtime_guard_rejects_invalid_claim_in_research_result():
    result = ResearchResult(
        analysis="Controlled research.",
        signal=make_signal(),
    )

    result.claims = ["not a claim"]

    with pytest.raises(
        RuntimeValidationError,
        match="must contain Claim objects",
    ):
        RuntimeGuard.validate_research_result(result)


def test_runtime_guard_rejects_invalid_supporting_evidence():
    claim = make_valid_claim()

    claim.supporting_evidence = ["not evidence"]

    result = ResearchResult(
        analysis="Controlled research.",
        signal=make_signal(),
        claims=[claim],
    )

    with pytest.raises(
        RuntimeValidationError,
        match="must be Evidence objects",
    ):
        RuntimeGuard.validate_research_result(result)


def test_runtime_guard_rejects_invalid_counter_evidence():
    claim = make_valid_claim()

    claim.counter_evidence = ["not evidence"]

    result = ResearchResult(
        analysis="Controlled research.",
        signal=make_signal(),
        claims=[claim],
    )

    with pytest.raises(
        RuntimeValidationError,
        match="must be Evidence objects",
    ):
        RuntimeGuard.validate_research_result(result)


def test_runtime_guard_rejects_out_of_range_claim_confidence():
    claim = make_valid_claim()
    claim.confidence = 1.5

    result = ResearchResult(
        analysis="Controlled research.",
        signal=make_signal(),
        claims=[claim],
    )

    with pytest.raises(
        RuntimeValidationError,
        match="Claim confidence",
    ):
        RuntimeGuard.validate_research_result(result)


def test_runtime_guard_rejects_out_of_range_evidence_confidence():
    claim = make_valid_claim()
    claim.supporting_evidence[0].confidence = -0.1

    result = ResearchResult(
        analysis="Controlled research.",
        signal=make_signal(),
        claims=[claim],
    )

    with pytest.raises(
        RuntimeValidationError,
        match="Evidence confidence",
    ):
        RuntimeGuard.validate_research_result(result)