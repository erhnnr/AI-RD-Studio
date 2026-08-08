import pytest

from studio.core.models import Signal
from studio.runtime.orchestrator import StudioOrchestrator
from studio.runtime.runtime_guard import RuntimeValidationError


def test_orchestrator_rejects_missing_signal():

    orchestrator = StudioOrchestrator()

    with pytest.raises(
        RuntimeValidationError,
        match="Signal is required",
    ):
        orchestrator.execute(None)


def test_orchestrator_rejects_invalid_research_output():

    orchestrator = StudioOrchestrator()

    research_worker = orchestrator.worker_registry.get(
        "research"
    )

    def invalid_execute(context):
        return {
            "analysis": "invalid"
        }

    research_worker.execute = invalid_execute

    signal = Signal(
        title="AI signal",
        description="AI demand is increasing.",
        source="Market",
    )

    with pytest.raises(
        RuntimeValidationError,
        match="Research worker must return ResearchResult",
    ):
        orchestrator.execute(signal)


def test_orchestrator_rejects_invalid_strategy_output():

    orchestrator = StudioOrchestrator()

    strategy_worker = orchestrator.worker_registry.get(
        "strategy"
    )

    def invalid_execute(context):
        return {
            "score": 100
        }

    strategy_worker.execute = invalid_execute

    signal = Signal(
        title="AI signal",
        description="AI demand is increasing.",
        source="Market",
    )

    with pytest.raises(
        RuntimeValidationError,
        match="Strategy worker must return Opportunity",
    ):
        orchestrator.execute(signal)


def test_orchestrator_rejects_missing_research_worker():

    orchestrator = StudioOrchestrator()

    orchestrator.worker_registry.workers[
        "research"
    ] = None

    signal = Signal(
        title="AI signal",
        description="AI demand is increasing.",
        source="Market",
    )

    with pytest.raises(
        RuntimeValidationError,
        match="No worker available",
    ):
        orchestrator.execute(signal)