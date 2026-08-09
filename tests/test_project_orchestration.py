from types import SimpleNamespace

from studio.core.models import (
    Opportunity,
    PipelineResult,
    Signal,
)
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.core.project_execution_result import ProjectExecutionResult
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


def test_orchestrator_executes_all_project_signals():
    project = Project(
        name="AI Education Platform",
        objective="Build an AI learning platform",
        priority="HIGH",
    )

    signal_1 = Signal(
        title="AI tutoring demand",
        description="Demand for AI tutoring is increasing.",
        source="Market",
    )

    signal_2 = Signal(
        title="Adaptive learning opportunity",
        description="Adaptive learning systems are improving.",
        source="Research",
    )

    context = ProjectContext(
        project=project,
        signals=[
            signal_1,
            signal_2,
        ],
    )

    orchestrator = StudioOrchestrator()

    execution = orchestrator.execute_project(
        context
    )

    assert isinstance(
        execution,
        ProjectExecutionResult,
    )

    assert execution.project is project
    assert len(execution.results) == 2

    assert all(
        isinstance(result, PipelineResult)
        for result in execution.results
    )

    assert execution.results[0].signal is signal_1
    assert execution.results[1].signal is signal_2

    assert (
        execution.results[0].research_result.signal
        is signal_1
    )

    assert (
        execution.results[1].research_result.signal
        is signal_2
    )

    assert execution.created_at is not None


def test_project_execution_with_no_signals_returns_empty_result():
    project = Project(
        name="Empty Project",
        objective="Test empty execution",
        priority="LOW",
    )

    context = ProjectContext(
        project=project,
    )

    orchestrator = StudioOrchestrator()

    execution = orchestrator.execute_project(
        context
    )

    assert isinstance(
        execution,
        ProjectExecutionResult,
    )

    assert execution.project is project
    assert execution.results == []
    assert execution.total_results == 0
    assert execution.accepted_count == 0
    assert execution.deferred_count == 0
    assert execution.rejected_count == 0
    assert execution.status == "NO_SIGNALS"


def test_project_execution_provides_summary_from_controlled_decisions(
    monkeypatch,
):
    project = Project(
        name="Research Project",
        objective="Evaluate opportunities",
        priority="HIGH",
    )

    accepted_signal = Signal(
        title="Infrastructure opportunity",
        description="Controlled accepted case.",
        source="Market",
    )

    rejected_signal = Signal(
        title="Secondary opportunity",
        description="Controlled rejected case.",
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

    assert execution.total_results == 2
    assert execution.accepted_count == 1
    assert execution.deferred_count == 0
    assert execution.rejected_count == 1
    assert execution.status == "COMPLETED"