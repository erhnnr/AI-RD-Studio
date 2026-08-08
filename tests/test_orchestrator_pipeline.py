from studio.core.models import Signal, ResearchResult
from studio.runtime.orchestrator import StudioOrchestrator


def test_orchestrator_runs_research_before_strategy():

    orchestrator = StudioOrchestrator()

    research_worker = orchestrator.worker_registry.get(
        "research"
    )

    strategy_worker = orchestrator.worker_registry.get(
        "strategy"
    )

    calls = {
        "research": False,
        "strategy_received_research_result": False,
    }

    original_research_execute = research_worker.execute
    original_strategy_execute = strategy_worker.execute

    def tracked_research_execute(context):

        calls["research"] = True

        return original_research_execute(context)

    def tracked_strategy_execute(context):

        if isinstance(context, ResearchResult):
            calls[
                "strategy_received_research_result"
            ] = True

        return original_strategy_execute(context)

    research_worker.execute = tracked_research_execute
    strategy_worker.execute = tracked_strategy_execute

    signal = Signal(
        title="AI infrastructure opportunity",
        description=(
            "Demand for AI infrastructure is increasing."
        ),
        source="Market Signal",
    )

    result = orchestrator.execute(signal)

    assert calls["research"] is True

    assert (
        calls["strategy_received_research_result"]
        is True
    )

    assert result is not None