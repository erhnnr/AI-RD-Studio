from studio.core.models import Signal
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.knowledge.project_memory import ProjectMemoryStore
from studio.runtime.orchestrator import StudioOrchestrator


def create_persisted_project(tmp_path):

    project = Project(
        name="Memory Retrieval Project",
        objective="Test memory retrieval",
        priority="HIGH",
    )

    signal_1 = Signal(
        title="AI infrastructure opportunity",
        description="Strong AI infrastructure demand.",
        source="Market",
    )

    signal_2 = Signal(
        title="Small idea",
        description="Low strategic value.",
        source="Internal",
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

    memory_path = (
        tmp_path / "project_memory.json"
    )

    store = ProjectMemoryStore(
        path=memory_path
    )

    store.store_execution(
        execution
    )

    return store


def test_project_memory_returns_research_history(
    tmp_path,
):

    store = create_persisted_project(
        tmp_path
    )

    history = store.get_research_history(
        "Memory Retrieval Project"
    )

    assert len(history) == 2

    assert history[0]["analysis"]
    assert history[1]["analysis"]

    assert history[0]["worker"] == (
        "ResearchWorker"
    )


def test_project_memory_returns_decision_history(
    tmp_path,
):

    store = create_persisted_project(
        tmp_path
    )

    history = store.get_decision_history(
        "Memory Retrieval Project"
    )

    assert len(history) == 2

    assert history[0]["decision"]
    assert history[0]["reason"]

    assert history[1]["decision"]
    assert history[1]["reason"]


def test_project_memory_returns_knowledge_history(
    tmp_path,
):

    store = create_persisted_project(
        tmp_path
    )

    history = store.get_knowledge_history(
        "Memory Retrieval Project"
    )

    assert len(history) == 2

    assert history[0]["title"]
    assert history[0]["content"]

    assert history[1]["title"]
    assert history[1]["content"]


def test_unknown_project_returns_empty_histories(
    tmp_path,
):

    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    assert store.get_research_history(
        "Unknown Project"
    ) == []

    assert store.get_decision_history(
        "Unknown Project"
    ) == []

    assert store.get_knowledge_history(
        "Unknown Project"
    ) == []