from studio.core.models import Signal
from studio.runtime.orchestrator import StudioOrchestrator


def test_orchestrator_runs_full_flow():
    signal = Signal(
        title="AI education opportunity",
        description="Personal AI teachers are becoming important",
        source="market",
    )

    orchestrator = StudioOrchestrator()

    record = orchestrator.execute(signal)

    assert record.title == "Research opportunity"
    assert record.content == "Personal AI teachers are becoming important"
    assert "runtime" in record.tags