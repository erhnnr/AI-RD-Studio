from studio.core.models import Signal
from studio.core.project import Project
from studio.core.project_context import ProjectContext


def test_project_context_groups_project_and_signals():

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
        description="Adaptive systems are improving.",
        source="Research",
    )

    context = ProjectContext(
        project=project,
        signals=[
            signal_1,
            signal_2,
        ],
    )

    assert context.project is project
    assert len(context.signals) == 2
    assert context.signals[0] is signal_1
    assert context.signals[1] is signal_2