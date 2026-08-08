from studio.core.models import Signal, KnowledgeRecord
from studio.runtime.orchestrator import StudioOrchestrator


def test_orchestrator_runs_accept_flow():

    signal = Signal(
        title="AI education opportunity",
        description="Personal AI teachers are becoming important",
        source="market",
    )

    orchestrator = StudioOrchestrator()

    record = orchestrator.execute(signal)

    assert isinstance(record, KnowledgeRecord)
    assert record.title == "Decision: ACCEPT"
    assert "Accepted opportunity" in record.content


def test_orchestrator_runs_reject_flow():

    signal = Signal(
        title="Small idea",
        description="Low value",
        source="internal",
    )

    orchestrator = StudioOrchestrator()

    record = orchestrator.execute(signal)

    assert isinstance(record, KnowledgeRecord)
    assert "Decision:" in record.content