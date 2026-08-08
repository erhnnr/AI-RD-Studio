from studio.workers.registry import WorkerRegistry


def test_strategy_worker_has_capabilities():

    registry = WorkerRegistry()

    worker = registry.get("strategy")

    assert "signal_analysis" in worker.capabilities


def test_registry_find_worker_by_capability():

    registry = WorkerRegistry()

    worker = registry.find_by_capability(
        "opportunity_scoring"
    )

    assert worker is not None
    assert worker.name == "StrategyWorker"


def test_worker_metadata_contains_identity_and_capabilities():

    registry = WorkerRegistry()

    worker = registry.get("strategy")

    metadata = worker.get_metadata()

    assert metadata["name"] == "StrategyWorker"
    assert "signal_analysis" in metadata["capabilities"]
    assert "strategy_creation" in metadata["capabilities"]


def test_worker_metadata_contains_contract():

    registry = WorkerRegistry()

    worker = registry.get("strategy")

    metadata = worker.get_metadata()

    assert "Signal" in metadata["input_types"]
    assert "WorkerContext" in metadata["input_types"]
    assert "Opportunity" in metadata["output_types"]


def test_registry_find_worker_by_contract():

    registry = WorkerRegistry()

    worker = registry.find_by_contract(
        "opportunity_scoring",
        "Signal",
        "Opportunity"
    )

    assert worker is not None
    assert worker.name == "StrategyWorker"