import pytest

from studio.core.evidence import Claim, Evidence, EvidenceSource
from studio.core.models import ResearchResult


def test_research_result_defaults_to_empty_claims():
    result = ResearchResult(
        analysis="Legacy prose research remains supported."
    )

    assert result.analysis == "Legacy prose research remains supported."
    assert result.claims == []


def test_research_result_accepts_structured_claims():
    source = EvidenceSource(
        name="Controlled Benchmark",
        source_type="dataset",
        reference="dataset://benchmark-001",
    )

    evidence = Evidence(
        content="Measured performance improved in the controlled benchmark.",
        source=source,
        confidence=0.9,
    )

    claim = Claim(
        statement="The proposed system improves benchmark performance.",
        supporting_evidence=[evidence],
        confidence=0.8,
        uncertainty="Performance outside the benchmark is not yet known.",
    )

    result = ResearchResult(
        analysis="Structured research result.",
        claims=[claim],
    )

    assert result.claims == [claim]
    assert result.claims[0].supporting_evidence == [evidence]
    assert result.claims[0].confidence == 0.8


def test_research_result_rejects_non_claim_items():
    with pytest.raises(TypeError):
        ResearchResult(
            analysis="Invalid structured research.",
            claims=["not a claim"],
        )


def test_research_result_rejects_non_list_claims():
    with pytest.raises(TypeError):
        ResearchResult(
            analysis="Invalid structured research.",
            claims="not a list",
        )