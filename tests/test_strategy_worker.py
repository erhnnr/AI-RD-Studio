from studio.core.models import Signal, Opportunity
from studio.workers.strategy import StrategyWorker


def test_strategy_worker_ai_signal():
    signal = Signal(
        title="AI Education",
        description="Growing demand for AI tutors",
        source="market",
    )

    worker = StrategyWorker()

    result = worker.execute(signal)

    assert isinstance(result, Opportunity)
    assert result.score == 35


def test_strategy_worker_normal_signal():
    signal = Signal(
        title="Local News",
        description="General update",
        source="news",
    )

    worker = StrategyWorker()

    result = worker.execute(signal)

    assert isinstance(result, Opportunity)
    assert result.score == 20