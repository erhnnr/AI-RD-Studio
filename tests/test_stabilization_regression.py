from types import SimpleNamespace

import pytest

from studio.core.models import (
    Opportunity,
    Signal,
)
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.runtime.orchestrator import StudioOrchestrator
from studio.runtime.runtime_guard import RuntimeValidationError
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


def test_controlled_accept_pipeline_remains_stable(
    monkeypatch,
):
    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        supporting_strategy,
    )

    orchestrator = StudioOrchestrator()

    orchestrator.review_board.evaluate = (
        lambda opportunity: SimpleNamespace(
            decision="ACCEPT",
            reason="Controlled acceptance.",
            confidence=100,
            next_action="CREATE_TASK",
        )
    )

    signal = Signal(
        title="Infrastructure opportunity",
        description="Controlled accepted opportunity.",
        source="Market",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.signal is signal
    assert result.research_result.signal is signal
    assert result.opportunity.signal is signal
    assert result.planning_result is not None
    assert result.validation_result is not None
    assert result.validation_result.valid is True
    assert result.decision.decision == "ACCEPT"
    assert result.task is not None
    assert result.knowledge is not None


def test_default_unverified_pipeline_does_not_auto_accept():
    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="AI infrastructure opportunity",
        description="Unverified input signal.",
        source="Market",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.opportunity.evidence_state == "INSUFFICIENT"
    assert result.validation_result.valid is False
    assert result.decision.decision == "DEFER"
    assert result.task is None
    assert result.knowledge is not None


def test_project_pipeline_remains_stable_with_controlled_decisions(
    monkeypatch,
):
    project = Project(
        name="Stabilization Project",
        objective="Validate project execution",
        priority="HIGH",
    )

    accepted_signal = Signal(
        title="Primary opportunity",
        description="Controlled accepted signal.",
        source="Market",
    )

    rejected_signal = Signal(
        title="Secondary opportunity",
        description="Controlled rejected signal.",
        source="Internal",
    )

    context = ProjectContext(
        project=project,
        signals=[
            accepted_signal,
            rejected_signal,
        ],
    )

    monkeypatch.setattr(
        StrategyWorker,
        "execute",
        supporting_strategy,
    )

    orchestrator = StudioOrchestrator()

    def controlled_evaluate(opportunity):
        if opportunity.signal is accepted_signal:
            return SimpleNamespace(
                decision="ACCEPT",
                reason="Controlled acceptance.",
                confidence=100,
                next_action="CREATE_TASK",
            )

        return SimpleNamespace(
            decision="REJECT",
            reason="Controlled rejection.",
            confidence=100,
            next_action="STOP",
        )

    orchestrator.review_board.evaluate = controlled_evaluate

    execution = orchestrator.execute_project(
        context
    )

    assert execution.project is project
    assert execution.total_results == 2
    assert execution.accepted_count == 1
    assert execution.deferred_count == 0
    assert execution.rejected_count == 1
    assert execution.status == "COMPLETED"


def test_missing_signal_remains_controlled():
    orchestrator = StudioOrchestrator()

    with pytest.raises(
        RuntimeValidationError,
        match="Signal is required",
    ):
        orchestrator.execute(None)