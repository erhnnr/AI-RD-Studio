from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceSource,
)
from studio.core.models import ResearchResult, Signal
from studio.runtime.orchestrator import StudioOrchestrator


class ControlledResearchProvider:
    def __init__(
        self,
        supporting_confidence=None,
        counter_confidence=None,
    ):
        self.supporting_confidence = supporting_confidence
        self.counter_confidence = counter_confidence

    def research(self, signal):
        return "Controlled research provider output."


def make_evidence(
    confidence: float,
    content: str,
) -> Evidence:
    return Evidence(
        content=content,
        source=EvidenceSource(
            name="Controlled Orchestration Source",
            source_type="test",
        ),
        confidence=confidence,
        provenance_note="Controlled orchestration causal test.",
    )


def inject_research_result(
    orchestrator: StudioOrchestrator,
    signal: Signal,
    supporting=None,
    counter=None,
):
    supporting = supporting or []
    counter = counter or []

    claim = Claim(
        statement=signal.title,
        supporting_evidence=supporting,
        counter_evidence=counter,
        confidence=0.5,
        uncertainty="Controlled orchestration test.",
    )

    research_result = ResearchResult(
        analysis="Controlled structured research.",
        signal=signal,
        claims=[claim],
    )

    research_worker = orchestrator.worker_registry.get(
        "research"
    )

    original_execute = research_worker.execute

    def controlled_execute(context):
        return research_result

    research_worker.execute = controlled_execute

    return original_execute


def test_supporting_evidence_reaches_accept_decision():
    signal = Signal(
        title="Industrial Efficiency Opportunity",
        description="Controlled signal.",
        source="test",
    )

    orchestrator = StudioOrchestrator()

    inject_research_result(
        orchestrator,
        signal,
        supporting=[
            make_evidence(
                0.9,
                "Strong supporting evidence.",
            )
        ],
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.opportunity.evidence_state == "SUPPORTING"
    assert result.decision.decision == "ACCEPT"
    assert result.task is not None


def test_insufficient_evidence_reaches_defer_decision():
    signal = Signal(
        title="Industrial Efficiency Opportunity",
        description="Controlled signal.",
        source="test",
    )

    orchestrator = StudioOrchestrator()

    inject_research_result(
        orchestrator,
        signal,
        supporting=[
            make_evidence(
                0.2,
                "Weak supporting evidence.",
            )
        ],
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.opportunity.evidence_state == "INSUFFICIENT"
    assert result.decision.decision == "DEFER"
    assert result.task is None


def test_contradictory_evidence_reaches_reject_decision():
    signal = Signal(
        title="Industrial Efficiency Opportunity",
        description="Controlled signal.",
        source="test",
    )

    orchestrator = StudioOrchestrator()

    inject_research_result(
        orchestrator,
        signal,
        counter=[
            make_evidence(
                0.9,
                "Strong contradictory evidence.",
            )
        ],
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.opportunity.evidence_state == "CONTRADICTORY"
    assert result.decision.decision == "REJECT"
    assert result.task is None