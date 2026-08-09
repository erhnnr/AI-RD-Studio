from studio.core.models import Opportunity, Signal
from studio.workers.strategy_worker import StrategyWorker


def test_strategy_worker_ai_signal_uses_neutral_baseline_without_research():
    signal = Signal(
        title="AI Education",
        description="Growing demand for AI tutors",
        source="market",
    )

    worker = StrategyWorker()

    result = worker.execute(signal)

    assert isinstance(result, Opportunity)

    assert result.impact == 5
    assert result.urgency == 5
    assert result.feasibility == 5
    assert result.strategic_fit == 5
    assert result.score == 20


def test_strategy_worker_non_ai_signal_uses_same_neutral_baseline():
    signal = Signal(
        title="Education Platform",
        description="Growing demand for digital tutors",
        source="market",
    )

    worker = StrategyWorker()

    result = worker.execute(signal)

    assert isinstance(result, Opportunity)

    assert result.impact == 5
    assert result.urgency == 5
    assert result.feasibility == 5
    assert result.strategic_fit == 5
    assert result.score == 20