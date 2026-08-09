import pytest

from studio.core.models import Signal
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.runtime.orchestrator import StudioOrchestrator
from studio.runtime.runtime_guard import RuntimeValidationError


def test_full_accept_pipeline_remains_stable():

    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="AI infrastructure opportunity",
        description="AI infrastructure demand is increasing.",
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


def test_full_reject_pipeline_remains_stable():

    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="Small idea",
        description="Low strategic value.",
        source="Internal",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.decision.decision != "ACCEPT"
    assert result.task is None
    assert result.knowledge is not None


def test_project_pipeline_remains_stable():

    project = Project(
        name="Stabilization Project",
        objective="Validate project execution",
        priority="HIGH",
    )

    context = ProjectContext(
        project=project,
        signals=[
            Signal(
                title="AI opportunity",
                description="High value AI signal.",
                source="Market",
            ),
            Signal(
                title="Small idea",
                description="Low value signal.",
                source="Internal",
            ),
        ],
    )

    orchestrator = StudioOrchestrator()

    execution = orchestrator.execute_project(
        context
    )

    assert execution.project is project
    assert execution.total_results == 2
    assert execution.accepted_count == 1
    assert execution.rejected_count == 1
    assert execution.status == "COMPLETED"


def test_missing_signal_remains_controlled():

    orchestrator = StudioOrchestrator()

    with pytest.raises(
        RuntimeValidationError,
        match="Signal is required",
    ):
        orchestrator.execute(None)