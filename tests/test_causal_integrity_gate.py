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
            name="Causal Integrity Controlled Source",
            source_type="test",
        ),
        confidence=confidence,
        provenance_note="Controlled causal integrity test evidence.",
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
        uncertainty="Controlled causal integrity test.",
    )

    return ResearchResult(
        analysis="Controlled causal integrity research.",
        signal=signal,
        claims=[claim],
    )


def test_same_signal_is_sensitive_to_material_evidence_changes():
    signal = Signal(
        title="Warehouse Optimization System",
        description="Evaluate operational optimization opportunity.",
        source="controlled-test",
    )

    supporting_result = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.9,
                "Strong evidence supports the opportunity.",
            )
        ],
    )

    insufficient_result = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.2,
                "Weak evidence provides limited support.",
            )
        ],
    )

    contradictory_result = make_research_result(
        signal=signal,
        counter=[
            make_evidence(
                0.9,
                "Strong evidence contradicts the opportunity.",
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

    assert (
        supporting_opportunity.evidence_state
        == "SUPPORTING"
    )

    assert (
        insufficient_opportunity.evidence_state
        == "INSUFFICIENT"
    )

    assert (
        contradictory_opportunity.evidence_state
        == "CONTRADICTORY"
    )


def test_irrelevant_ai_label_does_not_change_equivalent_evidence_evaluation():
    ai_signal = Signal(
        title="AI Warehouse Optimizer",
        description="Equivalent controlled opportunity.",
        source="controlled-test",
    )

    non_ai_signal = Signal(
        title="Warehouse Optimization System",
        description="Equivalent controlled opportunity.",
        source="controlled-test",
    )

    ai_result = make_research_result(
        signal=ai_signal,
        supporting=[
            make_evidence(
                0.9,
                "Equivalent strong supporting evidence.",
            )
        ],
    )

    non_ai_result = make_research_result(
        signal=non_ai_signal,
        supporting=[
            make_evidence(
                0.9,
                "Equivalent strong supporting evidence.",
            )
        ],
    )

    worker = StrategyWorker()

    ai_opportunity = worker.execute(
        ai_result
    )

    non_ai_opportunity = worker.execute(
        non_ai_result
    )

    assert ai_opportunity.score == non_ai_opportunity.score

    assert (
        ai_opportunity.evidence_state
        == non_ai_opportunity.evidence_state
    )

    assert (
        ai_opportunity.evidence_confidence
        == non_ai_opportunity.evidence_confidence
    )


def test_counter_evidence_injection_changes_evaluation_trajectory():
    signal = Signal(
        title="Industrial Efficiency Opportunity",
        description="Controlled opportunity.",
        source="controlled-test",
    )

    supporting_only = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.9,
                "Strong supporting evidence.",
            )
        ],
    )

    with_strong_counter_evidence = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.9,
                "Strong supporting evidence.",
            )
        ],
        counter=[
            make_evidence(
                0.9,
                "Strong contradictory evidence.",
            )
        ],
    )

    worker = StrategyWorker()

    before_counter = worker.execute(
        supporting_only
    )

    after_counter = worker.execute(
        with_strong_counter_evidence
    )

    assert before_counter.score > after_counter.score

    assert before_counter.evidence_state == "SUPPORTING"

    assert after_counter.evidence_state == "MIXED"


def test_persuasive_wording_without_strong_evidence_does_not_create_support():
    signal = Signal(
        title="Breakthrough High-Growth Revolutionary AI Opportunity",
        description=(
            "A highly persuasive description claiming enormous "
            "market potential and transformational impact."
        ),
        source="controlled-test",
    )

    research_result = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.2,
                "Weak unverified supporting evidence.",
            )
        ],
    )

    opportunity = StrategyWorker().execute(
        research_result
    )

    assert opportunity.evidence_state == "INSUFFICIENT"
    assert opportunity.score == 20


def test_strong_non_ai_opportunity_is_not_penalized_for_missing_ai_label():
    signal = Signal(
        title="Industrial Water Efficiency System",
        description="Controlled non-AI opportunity.",
        source="controlled-test",
    )

    research_result = make_research_result(
        signal=signal,
        supporting=[
            make_evidence(
                0.9,
                "Strong supporting evidence.",
            )
        ],
    )

    opportunity = StrategyWorker().execute(
        research_result
    )

    assert opportunity.evidence_state == "SUPPORTING"
    assert opportunity.score > 20