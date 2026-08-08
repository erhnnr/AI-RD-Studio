from studio.core.models import Signal
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.knowledge.project_memory import ProjectMemoryStore
from studio.runtime.orchestrator import StudioOrchestrator


def create_execution(
    project,
    signal_title,
):

    signal = Signal(
        title=signal_title,
        description="Memory history test.",
        source="Test",
    )

    context = ProjectContext(
        project=project,
        signals=[signal],
    )

    orchestrator = StudioOrchestrator()

    return orchestrator.execute_project(
        context
    )


def test_same_project_keeps_multiple_execution_runs(
    tmp_path,
):

    project = Project(
        name="Repeated Project",
        objective="Test execution history",
        priority="HIGH",
    )

    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    first_execution = create_execution(
        project,
        "AI opportunity one",
    )

    second_execution = create_execution(
        project,
        "AI opportunity two",
    )

    store.store_execution(
        first_execution
    )

    store.store_execution(
        second_execution
    )

    history = store.get_execution_history(
        "Repeated Project"
    )

    assert len(history) == 2

    assert (
        history[0]["executions"][0]
        ["signal"]["title"]
        == "AI opportunity one"
    )

    assert (
        history[1]["executions"][0]
        ["signal"]["title"]
        == "AI opportunity two"
    )


def test_retrieval_combines_records_from_all_runs(
    tmp_path,
):

    project = Project(
        name="Aggregated History Project",
        objective="Test aggregated history",
        priority="HIGH",
    )

    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    store.store_execution(
        create_execution(
            project,
            "AI opportunity one",
        )
    )

    store.store_execution(
        create_execution(
            project,
            "AI opportunity two",
        )
    )

    research_history = (
        store.get_research_history(
            "Aggregated History Project"
        )
    )

    decision_history = (
        store.get_decision_history(
            "Aggregated History Project"
        )
    )

    knowledge_history = (
        store.get_knowledge_history(
            "Aggregated History Project"
        )
    )

    assert len(research_history) == 2
    assert len(decision_history) == 2
    assert len(knowledge_history) == 2