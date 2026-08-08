from studio.core.models import Signal
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.knowledge.project_memory import ProjectMemoryStore
from studio.runtime.orchestrator import StudioOrchestrator


def test_project_memory_persists_execution(tmp_path):

    project = Project(
        name="AI Education Platform",
        objective="Build an AI learning platform",
        priority="HIGH",
    )

    signal = Signal(
        title="AI tutoring demand",
        description="Demand for AI tutoring is increasing.",
        source="Market",
    )

    context = ProjectContext(
        project=project,
        signals=[signal],
    )

    orchestrator = StudioOrchestrator()

    execution = orchestrator.execute_project(
        context
    )

    memory_path = (
        tmp_path / "project_memory.json"
    )

    store = ProjectMemoryStore(
        path=memory_path
    )

    stored = store.store_execution(
        execution
    )

    assert stored["project"]["name"] == (
        "AI Education Platform"
    )

    assert len(stored["history"]) == 1

    first_run = stored["history"][0]

    assert first_run["total_results"] == 1
    assert len(first_run["executions"]) == 1


def test_project_memory_survives_new_store_instance(
    tmp_path,
):

    project = Project(
        name="Persistent Project",
        objective="Test persistent memory",
        priority="HIGH",
    )

    signal = Signal(
        title="AI opportunity",
        description="Persistent memory test.",
        source="Test",
    )

    context = ProjectContext(
        project=project,
        signals=[signal],
    )

    orchestrator = StudioOrchestrator()

    execution = orchestrator.execute_project(
        context
    )

    memory_path = (
        tmp_path / "project_memory.json"
    )

    first_store = ProjectMemoryStore(
        path=memory_path
    )

    first_store.store_execution(
        execution
    )

    second_store = ProjectMemoryStore(
        path=memory_path
    )

    restored = second_store.get_project(
        "Persistent Project"
    )

    assert restored is not None

    assert restored["project"]["name"] == (
        "Persistent Project"
    )

    assert len(restored["history"]) == 1

    first_run = restored["history"][0]

    assert first_run["total_results"] == 1
    assert len(first_run["executions"]) == 1

    first_execution = (
        first_run["executions"][0]
    )

    assert (
        first_execution["research"]["analysis"]
    )

    assert (
        first_execution["decision"]["decision"]
    )

    assert (
        first_execution["knowledge"]["title"]
    )