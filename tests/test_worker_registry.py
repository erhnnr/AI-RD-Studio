from studio.workers.registry import WorkerRegistry
from studio.workers.strategy_worker import StrategyWorker


def test_worker_registry_returns_strategy_worker():
    registry = WorkerRegistry()

    worker = registry.get("strategy")

    assert isinstance(worker, StrategyWorker)
    assert worker.name == "StrategyWorker"