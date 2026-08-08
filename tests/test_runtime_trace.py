from studio.core.models import (
    PipelineResult,
    ResearchResult,
    Signal,
)
from studio.runtime.orchestrator import StudioOrchestrator


def test_execute_with_trace_returns_complete_pipeline_result():

    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="AI infrastructure opportunity",
        description="AI infrastructure demand is increasing.",
        source="Market Signal",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert isinstance(result, PipelineResult)

    assert result.signal is signal

    assert isinstance(
        result.research_result,
        ResearchResult,
    )

    assert result.research_result.signal is signal

    assert result.opportunity.signal is signal

    assert result.decision is not None

    assert result.knowledge is not None

    assert result.created_at is not None


def test_execute_still_returns_only_knowledge_record():

    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="AI infrastructure opportunity",
        description="AI infrastructure demand is increasing.",
        source="Market Signal",
    )

    result = orchestrator.execute(
        signal
    )

    assert result.title.startswith(
        "Decision:"
    )