from studio.core.models import Signal
from studio.core.worker_context import WorkerContext
from studio.workers.research_worker import ResearchWorker


class StubResearchProvider:
    def research(self, signal: Signal) -> str:
        return f"Provider research for {signal.title}"


def test_deterministic_research_worker_produces_signal_claim():
    signal = Signal(
        title="Test Signal",
        description="Controlled compatibility test.",
        source="test",
    )

    context = WorkerContext(
        signal=signal,
    )

    worker = ResearchWorker()

    result = worker.execute(context)

    assert result.analysis == "Research analysis prepared for Test Signal"
    assert result.signal is signal
    assert result.worker == "ResearchWorker"

    assert len(result.claims) == 1

    claim = result.claims[0]

    assert claim.statement == "Test Signal"
    assert claim.confidence == 0.3
    assert len(claim.supporting_evidence) == 1
    assert claim.counter_evidence == []

    evidence = claim.supporting_evidence[0]

    assert evidence.content == "Controlled compatibility test."
    assert evidence.confidence == 0.3
    assert evidence.source.name == "test"
    assert evidence.source.source_type == "signal_input"
    assert "Not independently verified" in evidence.provenance_note


def test_provider_research_worker_preserves_provider_analysis_and_signal_claim():
    signal = Signal(
        title="Provider Signal",
        description="Controlled provider compatibility test.",
        source="test-provider",
    )

    context = WorkerContext(
        signal=signal,
    )

    worker = ResearchWorker(
        provider=StubResearchProvider(),
    )

    result = worker.execute(context)

    assert result.analysis == "Provider research for Provider Signal"
    assert result.signal is signal
    assert result.worker == "ResearchWorker"

    assert len(result.claims) == 1

    claim = result.claims[0]

    assert claim.statement == "Provider Signal"

    evidence = claim.supporting_evidence[0]

    assert evidence.content == "Controlled provider compatibility test."
    assert evidence.source.name == "test-provider"
    assert evidence.source.source_type == "signal_input"


def test_generic_research_worker_result_keeps_empty_claims():
    worker = ResearchWorker()

    result = worker.execute(object())

    assert result.analysis == "Research analysis prepared."
    assert result.claims == []