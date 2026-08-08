from studio.core.models import PipelineResult, Signal
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.core.project_execution_result import ProjectExecutionResult
from studio.runtime.orchestrator import StudioOrchestrator


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
    assert execution.rejected_count == 0
    assert execution.status == "NO_SIGNALS"


def test_project_execution_provides_summary():

    project = Project(
        name="AI Research Project",
        objective="Evaluate AI opportunities",
        priority="HIGH",
    )

    accepted_signal = Signal(
        title="AI infrastructure opportunity",
        description="Strong AI infrastructure demand.",
        source="Market",
    )

    rejected_signal = Signal(
        title="Small idea",
        description="Low strategic value.",
        source="Internal",
    )

    context = ProjectContext(
        project=project,
        signals=[
            accepted_signal,
            rejected_signal,
        ],
    )

    orchestrator = StudioOrchestrator()

    execution = orchestrator.execute_project(
        context
    )

    assert execution.total_results == 2
    assert execution.accepted_count == 1
    assert execution.rejected_count == 1
    assert execution.status == "COMPLETED"