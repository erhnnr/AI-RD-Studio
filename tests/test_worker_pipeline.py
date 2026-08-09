from studio.core.models import Opportunity, ResearchResult, Signal
from studio.core.worker_context import WorkerContext
from studio.workers.strategy_worker import StrategyWorker


def test_strategy_worker_consumes_research_result_from_context():
    signal = Signal(
        title="AI infrastructure opportunity",
        description="New AI infrastructure demand detected.",
        source="Market Research",
    )

    research_result = ResearchResult(
        analysis="Research exists but contains no structured evidence.",
        signal=signal,
    )

    context = WorkerContext(
        research_result=research_result,
    )

    worker = StrategyWorker()

    result = worker.execute(context)

    assert isinstance(result, Opportunity)
    assert result.signal is signal

    # No structured evidence means the StrategyWorker
    # must remain at the neutral baseline.
    assert result.impact == 5
    assert result.urgency == 5
    assert result.feasibility == 5
    assert result.strategic_fit == 5
    assert result.score == 20


def test_strategy_worker_declares_research_result_contract():
    worker = StrategyWorker()

    metadata = worker.get_metadata()

    assert "ResearchResult" in metadata["input_types"]
    assert "Opportunity" in metadata["output_types"]