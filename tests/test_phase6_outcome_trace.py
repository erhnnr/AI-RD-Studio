import pytest

from studio.core.evidence import (
    Claim,
    Evidence,
    EvidenceSource,
)
from studio.core.models import (
    ResearchResult,
    Signal,
)
from studio.core.outcome import (
    DecisionOutcome,
    OutcomeObservation,
    OutcomeStatus,
)
from studio.core.project import Project
from studio.core.project_execution_result import (
    ProjectExecutionResult,
)
from studio.knowledge.project_memory import (
    ProjectMemoryStore,
)
from studio.runtime.orchestrator import (
    StudioOrchestrator,
)


def create_pipeline_result():
    signal = Signal(
        title="Phase 6 Controlled Opportunity",
        description=(
            "Controlled signal for outcome trace validation."
        ),
        source="phase6-test",
    )

    source = EvidenceSource(
        name="Phase 6 Controlled Evidence Source",
        source_type="controlled_test",
        reference="phase6://evidence/1",
        metadata="Controlled evidence source.",
    )

    evidence = Evidence(
        content=(
            "Controlled strong supporting evidence."
        ),
        source=source,
        confidence=0.9,
        provenance_note=(
            "Explicit controlled evidence for Phase 6."
        ),
    )

    claim = Claim(
        statement=signal.title,
        supporting_evidence=[
            evidence,
        ],
        counter_evidence=[],
        confidence=0.9,
        uncertainty=(
            "Controlled test uncertainty."
        ),
    )

    research_result = ResearchResult(
        analysis=(
            "Controlled structured Phase 6 research."
        ),
        signal=signal,
        claims=[
            claim,
        ],
    )

    orchestrator = StudioOrchestrator()

    research_worker = (
        orchestrator.worker_registry.get(
            "research"
        )
    )

    def controlled_execute(_context):
        return research_result

    research_worker.execute = controlled_execute

    result = orchestrator.execute_with_trace(
        signal
    )

    return result


def create_observed_outcome(
    pipeline_result,
):
    measurement = (
        pipeline_result
        .planning_result
        .experiment
        .measurements[0]
    )

    return DecisionOutcome.from_pipeline_result(
        pipeline_result=pipeline_result,
        status=OutcomeStatus.INCONCLUSIVE,
        observations=[
            OutcomeObservation(
                metric=measurement.metric,
                observed_value=(
                    "Observed, but no explicit numeric "
                    "target was configured."
                ),
                unit=measurement.unit,
                note=(
                    "Controlled Phase 6 observation."
                ),
            )
        ],
        summary=(
            "The bounded outcome was observed, but the "
            "current generic plan does not provide enough "
            "numeric information for a deterministic "
            "success or failure judgment."
        ),
    )


def test_pipeline_result_has_trace_id():
    result = create_pipeline_result()

    assert isinstance(
        result.trace_id,
        str,
    )

    assert result.trace_id


def test_outcome_is_created_from_real_pipeline_trace():
    result = create_pipeline_result()

    outcome = create_observed_outcome(
        result
    )

    assert (
        outcome.opportunity
        is result.opportunity
    )

    assert (
        outcome.planning_result
        is result.planning_result
    )

    assert (
        outcome.decision
        is result.decision
    )

    assert (
        outcome.source_trace_id
        == result.trace_id
    )


def test_full_decision_outcome_trace_can_be_reconstructed(
    tmp_path,
):
    result = create_pipeline_result()

    assert result.decision.decision == "ACCEPT"
    assert result.validation_result.valid is True

    project = Project(
        name="Phase 6 Trace Project",
        objective=(
            "Validate full decision-outcome trace."
        ),
        priority="HIGH",
    )

    project_execution = ProjectExecutionResult(
        project=project,
        results=[
            result,
        ],
    )

    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    store.store_execution(
        project_execution
    )

    outcome = create_observed_outcome(
        result
    )

    store.store_outcome(
        project.name,
        outcome,
    )

    trace = store.get_decision_outcome_trace(
        project.name,
        result.trace_id,
    )

    assert trace is not None

    execution = trace["execution"]
    stored_outcome = trace["outcome"]

    assert (
        execution["trace_id"]
        == result.trace_id
    )

    assert execution["signal"]["title"] == (
        "Phase 6 Controlled Opportunity"
    )

    research = execution["research"]

    assert len(
        research["claims"]
    ) == 1

    claim = research["claims"][0]

    assert claim["statement"] == (
        "Phase 6 Controlled Opportunity"
    )

    assert len(
        claim["supporting_evidence"]
    ) == 1

    stored_evidence = (
        claim["supporting_evidence"][0]
    )

    assert stored_evidence["confidence"] == 0.9

    assert (
        stored_evidence["source"]["name"]
        == "Phase 6 Controlled Evidence Source"
    )

    assert (
        stored_evidence["provenance_note"]
        == "Explicit controlled evidence for Phase 6."
    )

    planning = execution["planning"]

    assert planning["hypothesis"] is not None

    assert (
        planning["hypothesis"]["statement"]
    )

    assert planning["experiment"] is not None

    assert (
        planning["experiment"]["method"]
    )

    assert len(
        planning["experiment"]["measurements"]
    ) >= 1

    assert execution["validation"]["valid"] is True

    assert (
        execution["decision"]["decision"]
        == "ACCEPT"
    )

    assert (
        stored_outcome["source_trace_id"]
        == result.trace_id
    )

    assert (
        stored_outcome["status"]
        == "INCONCLUSIVE"
    )

    assert len(
        stored_outcome["observations"]
    ) == 1


def test_outcome_cannot_reference_unknown_execution_trace(
    tmp_path,
):
    result = create_pipeline_result()

    project = Project(
        name="Phase 6 Invalid Trace Project",
        objective="Reject invalid trace references.",
        priority="HIGH",
    )

    project_execution = ProjectExecutionResult(
        project=project,
        results=[
            result,
        ],
    )

    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    store.store_execution(
        project_execution
    )

    outcome = create_observed_outcome(
        result
    )

    outcome.source_trace_id = (
        "missing-execution-trace"
    )

    with pytest.raises(
        KeyError,
        match="Execution trace not found",
    ):
        store.store_outcome(
            project.name,
            outcome,
        )