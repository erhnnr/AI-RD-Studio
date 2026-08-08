from studio.core.worker_context import WorkerContext
from studio.core.project import Project


def test_worker_context_creation():

    project = Project(
        name="AI Research",
        objective="Build AI system",
        priority="HIGH",
    )

    context = WorkerContext(
        project=project
    )

    assert context.project.name == "AI Research"