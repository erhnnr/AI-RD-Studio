from studio.workers.registry import WorkerRegistry
from studio.workers.strategy_worker import StrategyWorker
from studio.workers.research_worker import ResearchWorker
from studio.workers.planning_worker import PlanningWorker
from studio.workers.validation_worker import ValidationWorker


def test_worker_registry_returns_research_worker():

    registry = WorkerRegistry()

    worker = registry.get("research")

    assert isinstance(
        worker,
        ResearchWorker,
    )

    assert worker.name == "ResearchWorker"


def test_worker_registry_returns_strategy_worker():

    registry = WorkerRegistry()

    worker = registry.get("strategy")

    assert isinstance(
        worker,
        StrategyWorker,
    )

    assert worker.name == "StrategyWorker"


def test_worker_registry_returns_planning_worker():

    registry = WorkerRegistry()

    worker = registry.get("planning")

    assert isinstance(
        worker,
        PlanningWorker,
    )

    assert worker.name == "PlanningWorker"


def test_worker_registry_returns_validation_worker():

    registry = WorkerRegistry()

    worker = registry.get("validation")

    assert isinstance(
        worker,
        ValidationWorker,
    )

    assert worker.name == "ValidationWorker"


def test_worker_registry_finds_planning_worker_by_contract():

    registry = WorkerRegistry()

    worker = registry.find_by_contract(
        capability="planning",
        input_type="Opportunity",
        output_type="PlanningResult",
    )

    assert isinstance(
        worker,
        PlanningWorker,
    )


def test_worker_registry_finds_validation_worker_by_contract():

    registry = WorkerRegistry()

    worker = registry.find_by_contract(
        capability="validation",
        input_type="PlanningResult",
        output_type="ValidationResult",
    )

    assert isinstance(
        worker,
        ValidationWorker,
    )


def test_all_registered_workers_have_contract_metadata():

    registry = WorkerRegistry()

    for worker in registry.workers.values():

        metadata = worker.get_metadata()

        assert metadata["name"] == worker.name

        assert len(
            metadata["capabilities"]
        ) > 0

        assert len(
            metadata["input_types"]
        ) > 0

        assert len(
            metadata["output_types"]
        ) > 0