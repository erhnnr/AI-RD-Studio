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
    source = EvidenceSource(
        name="Controlled Source",
        source_type="test",
    )

    return Evidence(
        content=content,
        source=source,
        confidence=confidence,
    )


def make_research_result(
    signal: Signal,
    supporting=None,
    counter=None,
) -> ResearchResult:
    supporting = supporting or []
    counter = counter or []

    claim = Claim(
        statement=signal.title,
        supporting_evidence=supporting,
        counter_evidence=counter,
        confidence=0.5,
    )

    return ResearchResult(
        analysis="Controlled research.",
        signal=signal,
        claims=[claim],
    )


def test_supporting_evidence_produces_stronger_opportunity_than_contradictory():
    signal = Signal(
        title="Warehouse Optimization System",
        description="Controlled signal.",
        source="test",
    )

    supporting_result = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.9,
                "Strong supporting evidence.",
            )
        ],
    )

    contradictory_result = make_research_result(
        signal=signal,
        counter=[
            make_evidence(
                0.9,
                "Strong contradictory evidence.",
            )
        ],
    )

    worker = StrategyWorker()

    supporting_opportunity = worker.execute(
        supporting_result
    )

    contradictory_opportunity = worker.execute(
        contradictory_result
    )

    assert (
        supporting_opportunity.score
        > contradictory_opportunity.score
    )


def test_insufficient_evidence_stays_between_supporting_and_contradictory():
    signal = Signal(
        title="Warehouse Optimization System",
        description="Controlled signal.",
        source="test",
    )

    supporting_result = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.9,
                "Strong supporting evidence.",
            )
        ],
    )

    insufficient_result = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.2,
                "Weak supporting evidence.",
            )
        ],
    )

    contradictory_result = make_research_result(
        signal=signal,
        counter=[
            make_evidence(
                0.9,
                "Strong contradictory evidence.",
            )
        ],
    )

    worker = StrategyWorker()

    supporting_opportunity = worker.execute(
        supporting_result
    )

    insufficient_opportunity = worker.execute(
        insufficient_result
    )

    contradictory_opportunity = worker.execute(
        contradictory_result
    )

    assert (
        supporting_opportunity.score
        > insufficient_opportunity.score
        > contradictory_opportunity.score
    )


def test_ai_keyword_does_not_create_strategic_advantage_without_evidence():
    ai_signal = Signal(
        title="AI Warehouse Optimizer",
        description="Controlled signal.",
        source="test",
    )

    neutral_signal = Signal(
        title="Warehouse Optimization System",
        description="Controlled signal.",
        source="test",
    )

    worker = StrategyWorker()

    ai_opportunity = worker.execute(
        ai_signal
    )

    neutral_opportunity = worker.execute(
        neutral_signal
    )

    assert ai_opportunity.score == neutral_opportunity.score


def test_equivalent_evidence_produces_equivalent_scores_despite_ai_label():
    ai_signal = Signal(
        title="AI Warehouse Optimizer",
        description="Controlled signal.",
        source="test",
    )

    neutral_signal = Signal(
        title="Warehouse Optimization System",
        description="Controlled signal.",
        source="test",
    )

    ai_result = make_research_result(
        signal=ai_signal,
        supporting=[
            make_evidence(
                0.9,
                "Equivalent supporting evidence.",
            )
        ],
    )

    neutral_result = make_research_result(
        signal=neutral_signal,
        supporting=[
            make_evidence(
                0.9,
                "Equivalent supporting evidence.",
            )
        ],
    )

    worker = StrategyWorker()

    ai_opportunity = worker.execute(
        ai_result
    )

    neutral_opportunity = worker.execute(
        neutral_result
    )

    assert ai_opportunity.score == neutral_opportunity.score