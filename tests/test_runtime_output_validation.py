from types import SimpleNamespace

import pytest

from studio.core.models import (
    Opportunity,
    Signal,
)
from studio.runtime.orchestrator import StudioOrchestrator
from studio.runtime.runtime_guard import RuntimeValidationError
from studio.workers.strategy_worker import StrategyWorker


def create_signal():
    return Signal(
        title="Infrastructure opportunity",
        description="Controlled opportunity.",
        source="Market",
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


def test_orchestrator_rejects_invalid_decision_output(
    monkeypatch,
):
    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        supporting_strategy,
    )

    orchestrator = StudioOrchestrator()

    def invalid_evaluate(opportunity):
        return {
            "decision": "ACCEPT"
        }

    orchestrator.review_board.evaluate = (
        invalid_evaluate
    )

    with pytest.raises(
        RuntimeValidationError,
        match="ReviewBoard must return a valid decision object",
    ):
        orchestrator.execute(
            create_signal()
        )


def test_orchestrator_rejects_invalid_task_output(
    monkeypatch,
):
    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        supporting_strategy,
    )

    orchestrator = StudioOrchestrator()

    orchestrator.review_board.evaluate = (
        lambda opportunity: SimpleNamespace(
            decision="ACCEPT",
            reason="Controlled acceptance.",
            confidence=100,
            next_action="CREATE_TASK",
        )
    )

    def invalid_create_task(
        opportunity,
        objective,
    ):
        return {
            "task": "invalid"
        }

    orchestrator.task_manager.create_task = (
        invalid_create_task
    )

    with pytest.raises(
        RuntimeValidationError,
        match="TaskManager must return ResearchTask",
    ):
        orchestrator.execute(
            create_signal()
        )


def test_orchestrator_rejects_invalid_knowledge_output():
    orchestrator = StudioOrchestrator()

    def invalid_write(
        title,
        content,
        tags,
    ):
        return {
            "knowledge": "invalid"
        }

    orchestrator.knowledge_writer.write = (
        invalid_write
    )

    with pytest.raises(
        RuntimeValidationError,
        match="KnowledgeWriter must return KnowledgeRecord",
    ):
        orchestrator.execute(
            create_signal()
        )