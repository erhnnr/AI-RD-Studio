from studio.core.models import (
    PlanningResult,
    Signal,
    ValidationResult,
)
from studio.runtime.orchestrator import StudioOrchestrator


def test_orchestrator_runs_planning_and_validation_workers():
    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="AI education opportunity",
        description="AI tutoring demand is increasing.",
        source="Market",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert isinstance(
        result.planning_result,
        PlanningResult,
    )

    assert (
        result.planning_result.opportunity
        is result.opportunity
    )

    assert isinstance(
        result.validation_result,
        ValidationResult,
    )

    assert (
        result.validation_result.planning_result
        is result.planning_result
    )

    # Default signal-derived evidence is intentionally
    # unverified and insufficient for progression.
    assert result.validation_result.valid is False
    assert result.opportunity.evidence_state == "INSUFFICIENT"
    assert result.decision.decision == "DEFER"
    assert result.task is None


def test_multi_worker_pipeline_preserves_full_trace():
    orchestrator = StudioOrchestrator()

    signal = Signal(
        title="AI infrastructure opportunity",
        description="AI infrastructure demand is increasing.",
        source="Market",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    assert result.signal is signal
    assert result.research_result.signal is signal
    assert result.opportunity.signal is signal

    assert (
        result.planning_result.opportunity
        is result.opportunity
    )

    assert (
        result.validation_result.planning_result
        is result.planning_result
    )

    assert result.decision is not None
    assert result.knowledge is not None