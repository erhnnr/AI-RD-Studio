from studio.core.models import Signal, ResearchTask
from studio.workers.strategy import StrategyWorker
from studio.runtime.task_manager import TaskManager


def test_strategy_to_task_flow():
    signal = Signal(
        title="AI Education Platform",
        description="AI tutors market opportunity",
        source="market",
    )

    strategy = StrategyWorker()
    opportunity = strategy.execute(signal)

    manager = TaskManager()

    task = manager.create_task(
        opportunity,
        "Research AI education market",
    )

    assert isinstance(task, ResearchTask)
    assert task.status == "NEW"
    assert task.objective == "Research AI education market"