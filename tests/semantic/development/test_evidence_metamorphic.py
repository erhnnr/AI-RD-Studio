from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceSource,
)
from studio.core.evidence_assessment import assess_research_evidence
from studio.core.models import ResearchResult, Signal
from studio.workers.strategy_worker import StrategyWorker


def make_evidence(
    content: str,
    confidence: float,
) -> Evidence:
    return Evidence(
        content=content,
        source=EvidenceSource(
            name="Controlled Semantic Source",
            source_type="semantic_test",
        ),
        confidence=confidence,
        provenance_note="Controlled development semantic case.",
    )


def make_research_result(
    title: str,
    supporting_confidence: float = 0.0,
    counter_confidence: float = 0.0,
    analysis: str = "Controlled semantic analysis.",
) -> ResearchResult:
    supporting_evidence = []
    counter_evidence = []

    if supporting_confidence > 0:
        supporting_evidence.append(
            make_evidence(
                content="Controlled supporting evidence.",
                confidence=supporting_confidence,
            )
        )

    if counter_confidence > 0:
        counter_evidence.append(
            make_evidence(
                content="Controlled contradictory evidence.",
                confidence=counter_confidence,
            )
        )

    signal = Signal(
        title=title,
        description="Controlled semantic signal.",
        source="semantic-development",
    )

    claim = Claim(
        statement="The opportunity is worth further investigation.",
        supporting_evidence=supporting_evidence,
        counter_evidence=counter_evidence,
        confidence=0.5,
        uncertainty="Controlled semantic uncertainty.",
    )

    return ResearchResult(
        analysis=analysis,
        signal=signal,
        claims=[
            claim,
        ],
    )


def test_relevant_evidence_change_changes_progression_direction():
    supporting = make_research_result(
        title="Water Efficiency Opportunity",
        supporting_confidence=0.9,
    )

    insufficient = make_research_result(
        title="Water Efficiency Opportunity",
        supporting_confidence=0.3,
    )

    contradictory = make_research_result(
        title="Water Efficiency Opportunity",
        counter_confidence=0.9,
    )

    worker = StrategyWorker()

    supporting_opportunity = worker.execute(
        supporting
    )

    insufficient_opportunity = worker.execute(
        insufficient
    )

    contradictory_opportunity = worker.execute(
        contradictory
    )

    assert supporting_opportunity.evidence_state == "SUPPORTING"
    assert insufficient_opportunity.evidence_state == "INSUFFICIENT"
    assert contradictory_opportunity.evidence_state == "CONTRADICTORY"

    assert (
        supporting_opportunity.score
        > insufficient_opportunity.score
        > contradictory_opportunity.score
    )


def test_irrelevant_ai_label_does_not_change_evaluation():
    ai_case = make_research_result(
        title="AI Water Efficiency Opportunity",
        supporting_confidence=0.9,
    )

    neutral_case = make_research_result(
        title="Water Efficiency Opportunity",
        supporting_confidence=0.9,
    )

    worker = StrategyWorker()

    ai_opportunity = worker.execute(
        ai_case
    )

    neutral_opportunity = worker.execute(
        neutral_case
    )

    assert (
        ai_opportunity.evidence_state
        == neutral_opportunity.evidence_state
    )

    assert (
        ai_opportunity.evidence_confidence
        == neutral_opportunity.evidence_confidence
    )

    assert ai_opportunity.score == neutral_opportunity.score


def test_persuasive_analysis_does_not_upgrade_weak_evidence():
    neutral_wording = make_research_result(
        title="Manufacturing Opportunity",
        supporting_confidence=0.3,
        analysis="Controlled analysis.",
    )

    persuasive_wording = make_research_result(
        title="Manufacturing Opportunity",
        supporting_confidence=0.3,
        analysis=(
            "This is an extraordinary revolutionary market-changing "
            "opportunity with enormous transformative potential."
        ),
    )

    worker = StrategyWorker()

    neutral_opportunity = worker.execute(
        neutral_wording
    )

    persuasive_opportunity = worker.execute(
        persuasive_wording
    )

    assert neutral_opportunity.evidence_state == "INSUFFICIENT"
    assert persuasive_opportunity.evidence_state == "INSUFFICIENT"

    assert (
        neutral_opportunity.score
        == persuasive_opportunity.score
    )


def test_strong_counter_evidence_injection_weakens_support():
    support_only = make_research_result(
        title="Learning Platform Opportunity",
        supporting_confidence=0.9,
    )

    support_with_counter = make_research_result(
        title="Learning Platform Opportunity",
        supporting_confidence=0.9,
        counter_confidence=0.8,
    )

    worker = StrategyWorker()

    before = worker.execute(
        support_only
    )

    after = worker.execute(
        support_with_counter
    )

    assert before.evidence_state == "SUPPORTING"
    assert after.evidence_state == "MIXED"

    assert after.score < before.score


def test_semantically_irrelevant_analysis_wording_does_not_change_assessment():
    first = make_research_result(
        title="Energy Efficiency Opportunity",
        supporting_confidence=0.8,
        analysis="Demand appears to be increasing.",
    )

    second = make_research_result(
        title="Energy Efficiency Opportunity",
        supporting_confidence=0.8,
        analysis="Market demand shows sustained growth.",
    )

    first_assessment = assess_research_evidence(
        first
    )

    second_assessment = assess_research_evidence(
        second
    )

    assert first_assessment.state == second_assessment.state

    assert (
        first_assessment.supporting_strength
        == second_assessment.supporting_strength
    )

    assert (
        first_assessment.counter_strength
        == second_assessment.counter_strength
    )

    assert (
        first_assessment.confidence
        == second_assessment.confidence
    )