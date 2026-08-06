from studio.core.models import Signal, KnowledgeRecord
from studio.runtime.orchestrator import StudioOrchestrator


def test_orchestrator_runs_full_flow():
    signal = Signal(
        title="AI education opportunity",
        description="Personal AI teachers are becoming important",
        source="market",
    )

    orchestrator = StudioOrchestrator()

    record = orchestrator.execute(signal)

    assert isinstance(record, KnowledgeRecord)
    assert record.title == "Research opportunity"
    assert "AI education opportunity" in record.content
    assert "strategy" in record.tags