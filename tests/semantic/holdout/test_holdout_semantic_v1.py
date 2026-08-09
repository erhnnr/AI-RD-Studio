from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceSource,
)
from studio.core.models import ResearchResult, Signal
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
            name="Holdout Source",
            source_type="holdout",
        ),
        confidence=confidence,
        provenance_note="Pristine Phase 5 holdout case.",
    )


def make_case(
    title: str,
    supporting_confidences=None,
    counter_confidences=None,
    analysis: str = "Holdout analysis.",
) -> ResearchResult:
    supporting_confidences = supporting_confidences or []
    counter_confidences = counter_confidences or []

    supporting = [
        make_evidence(
            content=f"Supporting holdout evidence {index}.",
            confidence=confidence,
        )
        for index, confidence in enumerate(
            supporting_confidences,
            start=1,
        )
    ]

    counter = [
        make_evidence(
            content=f"Counter holdout evidence {index}.",
            confidence=confidence,
        )
        for index, confidence in enumerate(
            counter_confidences,
            start=1,
        )
    ]

    signal = Signal(
        title=title,
        description="Independent holdout signal.",
        source="holdout",
    )

    return ResearchResult(
        analysis=analysis,
        signal=signal,
        claims=[
            Claim(
                statement=(
                    "The opportunity may justify additional R&D."
                ),
                supporting_evidence=supporting,
                counter_evidence=counter,
                confidence=0.5,
                uncertainty="Holdout uncertainty.",
            )
        ],
    )


def evaluate_case(
    research_result: ResearchResult,
):
    opportunity = StrategyWorker().execute(
        research_result
    )

    plan = PlanningWorker().execute(
        opportunity
    )

    validation = ValidationWorker().execute(
        plan
    )

    if validation.valid:
        decision = ReviewBoard().evaluate(
            opportunity
        ).decision
    elif opportunity.evidence_state == "CONTRADICTORY":
        decision = "REJECT"
    else:
        decision = "DEFER"

    return opportunity, validation, decision


def test_holdout_balanced_strong_evidence_stays_non_accept():
    opportunity, validation, decision = evaluate_case(
        make_case(
            title="Distributed Cooling Infrastructure",
            supporting_confidences=[0.88, 0.84],
            counter_confidences=[0.82, 0.80],
        )
    )

    assert opportunity.evidence_state == "MIXED"
    assert validation.valid is False
    assert decision == "DEFER"


def test_holdout_multiple_moderate_support_can_progress():
    opportunity, validation, decision = evaluate_case(
        make_case(
            title="Regional Water Recovery System",
            supporting_confidences=[0.72, 0.68, 0.70],
        )
    )

    assert opportunity.evidence_state == "SUPPORTING"
    assert validation.valid is True
    assert decision == "ACCEPT"


def test_holdout_prestige_language_does_not_rescue_weak_evidence():
    opportunity, validation, decision = evaluate_case(
        make_case(
            title="Globally Award-Winning Quantum AI Initiative",
            supporting_confidences=[0.34, 0.31],
            analysis=(
                "An elite, prestigious, transformative, world-leading "
                "initiative with extraordinary strategic importance."
            ),
        )
    )

    assert opportunity.evidence_state == "INSUFFICIENT"
    assert validation.valid is False
    assert decision == "DEFER"


def test_holdout_counter_dominance_blocks_progression():
    opportunity, validation, decision = evaluate_case(
        make_case(
            title="Autonomous Logistics Coordination",
            supporting_confidences=[0.62],
            counter_confidences=[0.91],
        )
    )

    assert opportunity.evidence_state == "CONTRADICTORY"
    assert validation.valid is False
    assert decision == "REJECT"


def test_holdout_title_variation_does_not_change_equivalent_evidence():
    first, first_validation, first_decision = evaluate_case(
        make_case(
            title="Smart Agriculture Optimization",
            supporting_confidences=[0.81],
        )
    )

    second, second_validation, second_decision = evaluate_case(
        make_case(
            title="Agricultural Optimization Program",
            supporting_confidences=[0.81],
        )
    )

    assert first.evidence_state == second.evidence_state
    assert first.evidence_confidence == second.evidence_confidence
    assert first.score == second.score
    assert first_validation.valid == second_validation.valid
    assert first_decision == second_decision