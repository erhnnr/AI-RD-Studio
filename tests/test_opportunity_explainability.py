from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceSource,
)
from studio.core.models import ResearchResult, Signal
from studio.workers.strategy_worker import StrategyWorker


def make_evidence(
    confidence: float,
    content: str,
) -> Evidence:
    return Evidence(
        content=content,
        source=EvidenceSource(
            name="Controlled Source",
            source_type="test",
        ),
        confidence=confidence,
    )


def test_supporting_opportunity_exposes_evidence_explanation():
    signal = Signal(
        title="Warehouse Optimization",
        description="Controlled signal.",
        source="test",
    )

    claim = Claim(
        statement="The opportunity is supported.",
        supporting_evidence=[
            make_evidence(
                0.9,
                "Strong supporting evidence.",
            )
        ],
        confidence=0.8,
    )

    research_result = ResearchResult(
        analysis="Controlled research.",
        signal=signal,
        claims=[claim],
    )

    opportunity = StrategyWorker().execute(
        research_result
    )

    assert opportunity.evidence_state == "SUPPORTING"
    assert opportunity.evidence_confidence == 0.9
    assert opportunity.rationale is not None
    assert "Supporting evidence" in opportunity.rationale


def test_contradictory_opportunity_exposes_evidence_explanation():
    signal = Signal(
        title="Warehouse Optimization",
        description="Controlled signal.",
        source="test",
    )

    claim = Claim(
        statement="The opportunity is challenged.",
        counter_evidence=[
            make_evidence(
                0.9,
                "Strong contradictory evidence.",
            )
        ],
        confidence=0.8,
    )

    research_result = ResearchResult(
        analysis="Controlled research.",
        signal=signal,
        claims=[claim],
    )

    opportunity = StrategyWorker().execute(
        research_result
    )

    assert opportunity.evidence_state == "CONTRADICTORY"
    assert opportunity.evidence_confidence == 0.9
    assert opportunity.rationale is not None
    assert "Counter-evidence" in opportunity.rationale


def test_insufficient_opportunity_exposes_uncertainty():
    signal = Signal(
        title="Warehouse Optimization",
        description="Controlled signal.",
        source="test",
    )

    claim = Claim(
        statement="Weakly supported opportunity.",
        supporting_evidence=[
            make_evidence(
                0.2,
                "Weak evidence.",
            )
        ],
        confidence=0.2,
    )

    research_result = ResearchResult(
        analysis="Controlled research.",
        signal=signal,
        claims=[claim],
    )

    opportunity = StrategyWorker().execute(
        research_result
    )

    assert opportunity.evidence_state == "INSUFFICIENT"
    assert opportunity.evidence_confidence == 0.2
    assert "insufficient" in opportunity.rationale.lower()


def test_direct_signal_uses_neutral_explanation():
    signal = Signal(
        title="AI Warehouse Optimization",
        description="Controlled signal.",
        source="test",
    )

    opportunity = StrategyWorker().execute(
        signal
    )

    assert opportunity.score == 20
    assert opportunity.evidence_state is None
    assert opportunity.evidence_confidence is None
    assert opportunity.rationale is not None
    assert "Neutral strategic baseline" in opportunity.rationale