from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceSource,
)
from studio.core.models import (
    ResearchResult,
    Signal,
)
from studio.core.review_board import ReviewBoard
from studio.workers.planning_worker import PlanningWorker
from studio.workers.strategy_worker import StrategyWorker
from studio.workers.validation_worker import ValidationWorker


def make_evidence(
    content: str,
    confidence: float,
) -> Evidence:
    return Evidence(
        content=content,
        source=EvidenceSource(
            name="Semantic Development Source",
            source_type="semantic_test",
        ),
        confidence=confidence,
        provenance_note="Controlled end-to-end semantic case.",
    )


def make_research_result(
    supporting_confidence: float = 0.0,
    counter_confidence: float = 0.0,
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
        title="Controlled Semantic Opportunity",
        description="Controlled semantic signal.",
        source="semantic-development",
    )

    claim = Claim(
        statement="The opportunity may justify further R&D.",
        supporting_evidence=supporting_evidence,
        counter_evidence=counter_evidence,
        confidence=0.5,
        uncertainty="Controlled uncertainty.",
    )

    return ResearchResult(
        analysis="Controlled semantic analysis.",
        signal=signal,
        claims=[
            claim,
        ],
    )


def run_semantic_pipeline(
    research_result: ResearchResult,
):
    opportunity = StrategyWorker().execute(
        research_result
    )

    planning_result = PlanningWorker().execute(
        opportunity
    )

    validation_result = ValidationWorker().execute(
        planning_result
    )

    if validation_result.valid:
        decision = ReviewBoard().evaluate(
            opportunity
        )
    else:
        if opportunity.evidence_state == "CONTRADICTORY":
            decision_value = "REJECT"
        else:
            decision_value = "DEFER"

        decision = type(
            "ControlledDecision",
            (),
            {
                "decision": decision_value,
            },
        )()

    return (
        opportunity,
        planning_result,
        validation_result,
        decision,
    )


def test_strong_support_can_progress_end_to_end():
    (
        opportunity,
        planning_result,
        validation_result,
        decision,
    ) = run_semantic_pipeline(
        make_research_result(
            supporting_confidence=0.9,
        )
    )

    assert opportunity.evidence_state == "SUPPORTING"
    assert planning_result.hypothesis is not None
    assert planning_result.experiment is not None
    assert validation_result.valid is True
    assert decision.decision == "ACCEPT"


def test_insufficient_evidence_is_deferred_end_to_end():
    (
        opportunity,
        planning_result,
        validation_result,
        decision,
    ) = run_semantic_pipeline(
        make_research_result(
            supporting_confidence=0.3,
        )
    )

    assert opportunity.evidence_state == "INSUFFICIENT"
    assert planning_result.hypothesis is not None
    assert planning_result.experiment is not None
    assert validation_result.valid is False
    assert decision.decision == "DEFER"


def test_contradictory_evidence_is_rejected_end_to_end():
    (
        opportunity,
        planning_result,
        validation_result,
        decision,
    ) = run_semantic_pipeline(
        make_research_result(
            counter_confidence=0.9,
        )
    )

    assert opportunity.evidence_state == "CONTRADICTORY"
    assert planning_result.hypothesis is not None
    assert planning_result.experiment is not None
    assert validation_result.valid is False
    assert decision.decision == "REJECT"


def test_mixed_evidence_does_not_progress_end_to_end():
    (
        opportunity,
        planning_result,
        validation_result,
        decision,
    ) = run_semantic_pipeline(
        make_research_result(
            supporting_confidence=0.9,
            counter_confidence=0.8,
        )
    )

    assert opportunity.evidence_state == "MIXED"
    assert planning_result.hypothesis is not None
    assert planning_result.experiment is not None
    assert validation_result.valid is False
    assert decision.decision == "DEFER"