from types import SimpleNamespace

from studio.core.models import (
    KnowledgeRecord,
    Opportunity,
    Signal,
)
from studio.runtime.orchestrator import StudioOrchestrator
from studio.workers.strategy_worker import StrategyWorker


def supporting_strategy(
    self,
    research_result,
) -> Opportunity:
    return Opportunity(
        signal=research_result.signal,
        impact=6,
        urgency=5,
        feasibility=6,
        strategic_fit=6,
        evidence_state="SUPPORTING",
        evidence_confidence=0.9,
        rationale="Controlled supporting evidence.",
    )


def test_orchestrator_runs_controlled_accept_flow(
    monkeypatch,
):
    signal = Signal(
        title="Education opportunity",
        description="Controlled opportunity.",
        source="market",
    )

    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        supporting_strategy,
    )

    orchestrator = StudioOrchestrator()

    orchestrator.review_board.evaluate = (
        lambda opportunity: SimpleNamespace(
            decision="ACCEPT",
            reason=(
                "Accepted opportunity for controlled "
                "orchestration test."
            ),
            confidence=100,
            next_action="CREATE_TASK",
        )
    )

    record = orchestrator.execute(signal)

    assert isinstance(record, KnowledgeRecord)
    assert record.title == "Decision: ACCEPT"
    assert "Accepted opportunity" in record.content


def test_orchestrator_default_unverified_signal_does_not_auto_accept():
    signal = Signal(
        title="AI education opportunity",
        description="Unverified input signal.",
        source="market",
    )

    orchestrator = StudioOrchestrator()

    record = orchestrator.execute(signal)

    assert isinstance(record, KnowledgeRecord)
    assert record.title != "Decision: ACCEPT"
    assert "Decision:" in record.content