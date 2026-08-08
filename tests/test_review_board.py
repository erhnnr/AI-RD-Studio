from studio.core.models import Signal, Opportunity
from studio.core.review_board import ReviewBoard


def test_review_board_accepts_high_value_opportunity():

    signal = Signal(
        title="AI Platform",
        description="AI education opportunity",
        source="market",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=9,
        urgency=8,
        feasibility=8,
        strategic_fit=10,
    )

    result = ReviewBoard().evaluate(opportunity)

    assert result.decision == "ACCEPT"
    assert result.confidence == 90


def test_review_board_defers_medium_value_opportunity():

    signal = Signal(
        title="New Tool",
        description="Potential opportunity",
        source="market",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
    )

    result = ReviewBoard().evaluate(opportunity)

    assert result.decision == "DEFER"


def test_review_board_rejects_low_value_opportunity():

    signal = Signal(
        title="Small Idea",
        description="Low impact",
        source="internal",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=2,
        urgency=2,
        feasibility=2,
        strategic_fit=2,
    )

    result = ReviewBoard().evaluate(opportunity)

    assert result.decision == "REJECT"