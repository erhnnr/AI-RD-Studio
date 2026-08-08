from studio.workers.registry import WorkerRegistry
from studio.workers.strategy_worker import StrategyWorker
from studio.workers.research_worker import ResearchWorker


def test_worker_registry_returns_research_worker():

    registry = WorkerRegistry()

    worker = registry.get("research")

    assert isinstance(worker, ResearchWorker)
    assert worker.name == "ResearchWorker"


def test_worker_registry_returns_strategy_worker():

    registry = WorkerRegistry()

    worker = registry.get("strategy")

    assert isinstance(worker, StrategyWorker)
    assert worker.name == "StrategyWorker"


def test_all_registered_workers_have_contract_metadata():

    registry = WorkerRegistry()

    for worker in registry.workers.values():

        metadata = worker.get_metadata()

        assert metadata["name"] == worker.name
        assert len(metadata["capabilities"]) > 0
        assert len(metadata["input_types"]) > 0
        assert len(metadata["output_types"]) > 0