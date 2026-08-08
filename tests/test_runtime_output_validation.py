import pytest

from studio.core.models import Signal
from studio.runtime.orchestrator import StudioOrchestrator
from studio.runtime.runtime_guard import RuntimeValidationError


def create_signal():

    return Signal(
        title="AI infrastructure opportunity",
        description="AI infrastructure demand is increasing.",
        source="Market",
    )


def test_orchestrator_rejects_invalid_decision_output():

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


def test_orchestrator_rejects_invalid_task_output():

    orchestrator = StudioOrchestrator()

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