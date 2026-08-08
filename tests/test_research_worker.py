from studio.workers.research_worker import ResearchWorker
from studio.core.project import Project


def test_research_worker_creates_report():

    worker = ResearchWorker()

    project = Project(
        name="AI Education Platform",
        objective="Build AI teacher",
        priority="HIGH",
    )

    result = worker.execute(project)

    assert result["worker"] == "ResearchWorker"
    assert "analysis" in result
    assert result["project"] == "AI Education Platform"


def test_research_worker_supports_signal_context_contract():

    worker = ResearchWorker()

    metadata = worker.get_metadata()

    assert "Signal" in metadata["input_types"]
    assert "WorkerContext" in metadata["input_types"]
    assert "ResearchResult" in metadata["output_types"]