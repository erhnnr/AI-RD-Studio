from studio.core.models import Signal
from studio.core.worker_context import WorkerContext
from studio.workers.research_provider import ResearchProvider
from studio.workers.research_worker import ResearchWorker


class FakeResearchProvider(ResearchProvider):

    def research(self, signal: Signal) -> str:

        return (
            f"External research completed for "
            f"{signal.title}"
        )


def test_research_worker_uses_provider():

    signal = Signal(
        title="AI infrastructure opportunity",
        description="AI infrastructure demand is growing.",
        source="Market",
    )

    provider = FakeResearchProvider()

    worker = ResearchWorker(
        provider=provider
    )

    context = WorkerContext(
        signal=signal
    )

    result = worker.execute(
        context
    )

    assert result.signal is signal

    assert result.analysis == (
        "External research completed for "
        "AI infrastructure opportunity"
    )


def test_research_worker_keeps_default_behavior_without_provider():

    signal = Signal(
        title="AI market signal",
        description="AI demand is increasing.",
        source="Market",
    )

    worker = ResearchWorker()

    context = WorkerContext(
        signal=signal
    )

    result = worker.execute(
        context
    )

    assert result.signal is signal

    assert result.analysis == (
        "Research analysis prepared for "
        "AI market signal"
    )