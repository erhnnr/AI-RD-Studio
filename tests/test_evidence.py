import pytest

from studio.core.evidence import Claim, Evidence, EvidenceSource


def test_create_evidence_source():
    source = EvidenceSource(
        name="Example Source",
        source_type="document",
        reference="doc://example",
        metadata="Controlled test source",
    )

    assert source.name == "Example Source"
    assert source.source_type == "document"
    assert source.reference == "doc://example"
    assert source.metadata == "Controlled test source"


def test_create_evidence():
    source = EvidenceSource(
        name="Example Source",
        source_type="document",
    )

    evidence = Evidence(
        content="The prototype reduced processing time.",
        source=source,
        confidence=0.8,
        provenance_note="Observed in controlled test.",
    )

    assert evidence.content == "The prototype reduced processing time."
    assert evidence.source is source
    assert evidence.confidence == 0.8
    assert evidence.provenance_note == "Observed in controlled test."


def test_create_claim_with_supporting_and_counter_evidence():
    supporting_source = EvidenceSource(
        name="Supporting Source",
        source_type="dataset",
    )

    counter_source = EvidenceSource(
        name="Counter Source",
        source_type="document",
    )

    supporting = Evidence(
        content="Measured performance improved by 20 percent.",
        source=supporting_source,
        confidence=0.9,
    )

    counter = Evidence(
        content="The improvement disappeared under a second workload.",
        source=counter_source,
        confidence=0.7,
    )

    claim = Claim(
        statement="The proposed system improves performance.",
        supporting_evidence=[supporting],
        counter_evidence=[counter],
        confidence=0.6,
        uncertainty="Performance may depend on workload type.",
    )

    assert claim.statement == "The proposed system improves performance."
    assert claim.supporting_evidence == [supporting]
    assert claim.counter_evidence == [counter]
    assert claim.confidence == 0.6
    assert claim.uncertainty == "Performance may depend on workload type."


@pytest.mark.parametrize(
    "confidence",
    [-0.1, 1.1],
)
def test_evidence_rejects_invalid_confidence(confidence):
    source = EvidenceSource(
        name="Example Source",
        source_type="document",
    )

    with pytest.raises(ValueError):
        Evidence(
            content="Example evidence.",
            source=source,
            confidence=confidence,
        )


@pytest.mark.parametrize(
    "confidence",
    [-0.1, 1.1],
)
def test_claim_rejects_invalid_confidence(confidence):
    with pytest.raises(ValueError):
        Claim(
            statement="Example claim.",
            confidence=confidence,
        )


def test_claim_rejects_non_evidence_items():
    with pytest.raises(TypeError):
        Claim(
            statement="Example claim.",
            supporting_evidence=["not evidence"],
        )