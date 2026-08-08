from studio.core.models import DecisionRecord
from studio.core.decision_memory import DecisionMemory


def test_decision_memory_store():

    memory = DecisionMemory()

    record = memory.store(
        decision="ACCEPT",
        reason="High value opportunity",
        confidence=90,
        next_action="Create research task",
    )

    assert isinstance(record, DecisionRecord)
    assert record.decision == "ACCEPT"
    assert len(memory.all()) == 1