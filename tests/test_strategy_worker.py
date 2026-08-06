from studio.workers.strategy_worker import StrategyWorker
from studio.core.models import Signal, Opportunity
from studio.runtime.task_manager import TaskManager


def test_strategy_worker_executes_task():
    signal = Signal(
        title="AI market",
        description="AI systems are expanding",
        source="research",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
    )

    task = TaskManager().create_task(
        opportunity,
        "Analyze AI market opportunity",
    )

    worker = StrategyWorker()

    result = worker.execute(task)

    assert result["worker"] == "StrategyWorker"
    assert result["task"] == "Analyze AI market opportunity"
    assert result["analysis"] == "Strategic analysis completed"