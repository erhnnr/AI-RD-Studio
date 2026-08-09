from studio.core.models import Opportunity, Signal
from studio.core.review_board import ReviewBoard


def make_signal() -> Signal:
    return Signal(
        title="Controlled Opportunity",
        description="Controlled review-board test.",
        source="test",
    )


def make_opportunity(
    score_value: int,
    evidence_state: str,
) -> Opportunity:
    base = score_value // 4
    remainder = score_value - (base * 4)

    values = [
        base,
        base,
        base,
        base,
    ]

    for index in range(remainder):
        values[index] += 1

    return Opportunity(
        signal=make_signal(),
        impact=values[0],
        urgency=values[1],
        feasibility=values[2],
        strategic_fit=values[3],
        evidence_state=evidence_state,
        evidence_confidence=0.9,
        rationale="Controlled evidence-aware review.",
    )


def test_supporting_evidence_can_progress_when_strategically_eligible():
    opportunity = make_opportunity(
        score_value=23,
        evidence_state="SUPPORTING",
    )

    decision = ReviewBoard().evaluate(
        opportunity
    )

    assert decision.decision == "ACCEPT"
    assert decision.next_action == "Create research task"


def test_supporting_evidence_does_not_guarantee_accept():
    opportunity = make_opportunity(
        score_value=20,
        evidence_state="SUPPORTING",
    )

    decision = ReviewBoard().evaluate(
        opportunity
    )

    assert decision.decision == "DEFER"


def test_insufficient_evidence_prevents_accept():
    opportunity = make_opportunity(
        score_value=40,
        evidence_state="INSUFFICIENT",
    )

    decision = ReviewBoard().evaluate(
        opportunity
    )

    assert decision.decision == "DEFER"


def test_mixed_evidence_prevents_accept():
    opportunity = make_opportunity(
        score_value=40,
        evidence_state="MIXED",
    )

    decision = ReviewBoard().evaluate(
        opportunity
    )

    assert decision.decision == "DEFER"


def test_contradictory_evidence_prevents_accept():
    opportunity = make_opportunity(
        score_value=40,
        evidence_state="CONTRADICTORY",
    )

    decision = ReviewBoard().evaluate(
        opportunity
    )

    assert decision.decision == "REJECT"


def test_legacy_opportunity_without_evidence_uses_score_fallback():
    opportunity = Opportunity(
        signal=make_signal(),
        impact=9,
        urgency=8,
        feasibility=8,
        strategic_fit=10,
    )

    decision = ReviewBoard().evaluate(
        opportunity
    )

    assert decision.decision == "ACCEPT"