from studio.core.models import Signal
from studio.runtime.orchestrator import StudioOrchestrator
from studio.workers.research_provider import ResearchProvider


class FakeResearchProvider(ResearchProvider):

    def research(self, signal: Signal) -> str:

        return (
            f"Provider research for "
            f"{signal.title}"
        )


def test_orchestrator_uses_injected_research_provider():

    provider = FakeResearchProvider()

    orchestrator = StudioOrchestrator(
        research_provider=provider
    )

    signal = Signal(
        title="AI infrastructure opportunity",
        description="AI infrastructure demand is increasing.",
        source="Market",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.research_result.analysis == (
        "Provider research for "
        "AI infrastructure opportunity"
    )


def test_orchestrator_keeps_default_research_behavior():

    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="AI market signal",
        description="AI demand is increasing.",
        source="Market",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.research_result.analysis == (
        "Research analysis prepared for "
        "AI market signal"
    )