from studio.core.models import ResearchResult, Signal


def test_research_result_stores_structured_research_data():

    signal = Signal(
        title="New AI research",
        description="A new AI architecture was published.",
        source="Research Journal",
    )

    result = ResearchResult(
        analysis="The research may create strategic value.",
        signal=signal,
    )

    assert result.worker == "ResearchWorker"
    assert result.analysis == (
        "The research may create strategic value."
    )
    assert result.signal is signal
    assert result.project_name is None
    assert result.created_at is not None