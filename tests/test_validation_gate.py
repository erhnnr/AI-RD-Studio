from studio.core.models import (
    Opportunity,
    Signal,
    ValidationResult,
)
from studio.core.review_board import ReviewDecision
from studio.runtime.orchestrator import StudioOrchestrator
from studio.workers.strategy_worker import StrategyWorker
from studio.workers.validation_worker import ValidationWorker


def make_signal() -> Signal:
    return Signal(
        title="Controlled Validation Gate Opportunity",
        description="Controlled runtime validation gate signal.",
        source="test",
    )


def supporting_strategy(
    self,
    research_result,
) -> Opportunity:
    return Opportunity(
        signal=research_result.signal,
        impact=6,
        urgency=5,
        feasibility=6,
        strategic_fit=6,
        evidence_state="SUPPORTING",
        evidence_confidence=0.9,
        rationale="Controlled supporting evidence.",
    )


def contradictory_strategy(
    self,
    research_result,
) -> Opportunity:
    return Opportunity(
        signal=research_result.signal,
        impact=6,
        urgency=5,
        feasibility=6,
        strategic_fit=6,
        evidence_state="CONTRADICTORY",
        evidence_confidence=0.9,
        rationale="Controlled contradictory evidence.",
    )


def invalid_validation(
    self,
    planning_result,
) -> ValidationResult:
    return ValidationResult(
        planning_result=planning_result,
        valid=False,
        reason="Controlled validation failure.",
        worker=self.name,
    )


def test_invalid_validation_blocks_accept(
    monkeypatch,
):
    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        supporting_strategy,
    )

    monkeypatch.setattr(
        ValidationWorker,
        "execute",
        invalid_validation,
    )

    orchestrator = StudioOrchestrator()

    def forbidden_review(_opportunity):
        raise AssertionError(
            "ReviewBoard must not run after validation failure."
        )

    monkeypatch.setattr(
        orchestrator.review_board,
        "evaluate",
        forbidden_review,
    )

    result = orchestrator.execute_with_trace(
        make_signal()
    )

    assert result.validation_result.valid is False
    assert result.decision.decision == "DEFER"
    assert result.task is None
    assert "Validation blocked progression" in result.decision.reason


def test_contradictory_validation_failure_rejects(
    monkeypatch,
):
    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        contradictory_strategy,
    )

    monkeypatch.setattr(
        ValidationWorker,
        "execute",
        invalid_validation,
    )

    orchestrator = StudioOrchestrator()

    def forbidden_review(_opportunity):
        raise AssertionError(
            "ReviewBoard must not run after validation failure."
        )

    monkeypatch.setattr(
        orchestrator.review_board,
        "evaluate",
        forbidden_review,
    )

    result = orchestrator.execute_with_trace(
        make_signal()
    )

    assert result.validation_result.valid is False
    assert result.decision.decision == "REJECT"
    assert result.task is None
    assert "Validation blocked progression" in result.decision.reason


def test_valid_validation_allows_review_board(
    monkeypatch,
):
    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        supporting_strategy,
    )

    orchestrator = StudioOrchestrator()

    review_called = {
        "value": False,
    }

    def controlled_review(opportunity):
        review_called["value"] = True

        return ReviewDecision(
            decision="ACCEPT",
            reason="Controlled strategic acceptance.",
            confidence=80,
            next_action="Create research task",
        )

    monkeypatch.setattr(
        orchestrator.review_board,
        "evaluate",
        controlled_review,
    )

    result = orchestrator.execute_with_trace(
        make_signal()
    )

    assert result.validation_result.valid is True
    assert review_called["value"] is True
    assert result.decision.decision == "ACCEPT"
    assert result.task is not None