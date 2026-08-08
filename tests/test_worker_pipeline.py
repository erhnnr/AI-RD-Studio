from studio.core.models import Signal, ResearchResult, Opportunity
from studio.core.worker_context import WorkerContext
from studio.workers.strategy_worker import StrategyWorker


def test_strategy_worker_consumes_research_result_from_context():

    signal = Signal(
        title="AI infrastructure opportunity",
        description="New AI infrastructure demand detected.",
        source="Market Research",
    )

    research_result = ResearchResult(
        analysis="Strong growth potential detected.",
        signal=signal,
    )

    context = WorkerContext(
        research_result=research_result,
    )

    worker = StrategyWorker()

    result = worker.execute(context)

    assert isinstance(result, Opportunity)
    assert result.signal is signal
    assert result.impact == 9
    assert result.urgency == 8
    assert result.feasibility == 8
    assert result.strategic_fit == 10
    assert result.score == 35


def test_strategy_worker_declares_research_result_contract():

    worker = StrategyWorker()

    metadata = worker.get_metadata()

    assert "ResearchResult" in metadata["input_types"]
    assert "Opportunity" in metadata["output_types"]