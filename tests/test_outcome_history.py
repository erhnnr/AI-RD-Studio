from types import SimpleNamespace

import pytest

from studio.core.models import (
    Opportunity,
    PlanningResult,
    Signal,
)
from studio.core.outcome import (
    DecisionOutcome,
    OutcomeObservation,
    OutcomeStatus,
)
from studio.core.project import Project
from studio.core.project_context import ProjectContext
from studio.knowledge.project_memory import ProjectMemoryStore
from studio.runtime.orchestrator import StudioOrchestrator


def create_persisted_project(
    tmp_path,
):
    project = Project(
        name="Outcome History Project",
        objective="Test outcome persistence.",
        priority="HIGH",
    )

    signal = Signal(
        title="Outcome opportunity",
        description="Controlled outcome history signal.",
        source="Test",
    )

    execution = StudioOrchestrator().execute_project(
        ProjectContext(
            project=project,
            signals=[
                signal,
            ],
        )
    )

    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    store.store_execution(
        execution
    )

    return store, project


def create_outcome() -> DecisionOutcome:
    opportunity = Opportunity(
        signal=Signal(
            title="Observed efficiency opportunity",
            description="Controlled observed result.",
            source="test",
        ),
        impact=6,
        urgency=5,
        feasibility=6,
        strategic_fit=6,
        evidence_state="SUPPORTING",
        evidence_confidence=0.9,
        rationale="Controlled evidence.",
    )

    planning_result = PlanningResult(
        opportunity=opportunity,
        objective="Run bounded observed experiment.",
        steps=[
            "Run experiment.",
            "Observe result.",
        ],
    )

    decision = SimpleNamespace(
        decision="ACCEPT",
        reason="Controlled acceptance.",
        confidence=80,
        next_action="Run experiment",
    )

    return DecisionOutcome(
        opportunity=opportunity,
        planning_result=planning_result,
        decision=decision,
        status=OutcomeStatus.SUCCESS,
        observations=[
            OutcomeObservation(
                metric="efficiency",
                observed_value=18,
                unit="percent",
                note="Controlled observation.",
            )
        ],
        summary="Observed efficiency improved.",
    )


def test_store_and_retrieve_outcome_history(
    tmp_path,
):
    store, project = create_persisted_project(
        tmp_path
    )

    stored = store.store_outcome(
        project.name,
        create_outcome(),
    )

    assert stored["status"] == "SUCCESS"
    assert stored["decision"]["decision"] == "ACCEPT"
    assert len(stored["observations"]) == 1

    history = store.get_outcome_history(
        project.name
    )

    assert len(history) == 1
    assert history[0]["status"] == "SUCCESS"
    assert (
        history[0]["observations"][0]["metric"]
        == "efficiency"
    )


def test_failure_outcome_is_preserved(
    tmp_path,
):
    store, project = create_persisted_project(
        tmp_path
    )

    outcome = create_outcome()

    outcome.status = OutcomeStatus.FAILURE
    outcome.summary = (
        "Observed efficiency failed the expected condition."
    )

    store.store_outcome(
        project.name,
        outcome,
    )

    history = store.get_outcome_history(
        project.name
    )

    assert len(history) == 1
    assert history[0]["status"] == "FAILURE"


def test_not_observed_outcome_is_preserved_without_observations(
    tmp_path,
):
    store, project = create_persisted_project(
        tmp_path
    )

    opportunity = Opportunity(
        signal=Signal(
            title="Pending opportunity",
            description="No observation yet.",
            source="test",
        ),
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
    )

    planning_result = PlanningResult(
        opportunity=opportunity,
        objective="Pending experiment.",
        steps=[
            "Wait for observation.",
        ],
    )

    outcome = DecisionOutcome(
        opportunity=opportunity,
        planning_result=planning_result,
        decision=SimpleNamespace(
            decision="ACCEPT",
            reason="Controlled pending decision.",
            next_action="Observe result",
        ),
        status=OutcomeStatus.NOT_OBSERVED,
    )

    store.store_outcome(
        project.name,
        outcome,
    )

    history = store.get_outcome_history(
        project.name
    )

    assert len(history) == 1
    assert history[0]["status"] == "NOT_OBSERVED"
    assert history[0]["observations"] == []


def test_outcome_history_survives_new_store_instance(
    tmp_path,
):
    path = tmp_path / "project_memory.json"

    store, project = create_persisted_project(
        tmp_path
    )

    store.store_outcome(
        project.name,
        create_outcome(),
    )

    restored_store = ProjectMemoryStore(
        path=path
    )

    history = restored_store.get_outcome_history(
        project.name
    )

    assert len(history) == 1
    assert history[0]["summary"] == (
        "Observed efficiency improved."
    )


def test_unknown_project_returns_empty_outcome_history(
    tmp_path,
):
    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    assert store.get_outcome_history(
        "Unknown Project"
    ) == []


def test_store_outcome_requires_existing_project(
    tmp_path,
):
    store = ProjectMemoryStore(
        path=tmp_path / "project_memory.json"
    )

    with pytest.raises(
        KeyError,
        match="Project not found",
    ):
        store.store_outcome(
            "Missing Project",
            create_outcome(),
        )


def test_store_outcome_rejects_invalid_type(
    tmp_path,
):
    store, project = create_persisted_project(
        tmp_path
    )

    with pytest.raises(
        TypeError,
        match="DecisionOutcome",
    ):
        store.store_outcome(
            project.name,
            "invalid",
        )


def test_execution_persistence_includes_distinct_decision_counts(
    tmp_path,
):
    store, project = create_persisted_project(
        tmp_path
    )

    history = store.get_execution_history(
        project.name
    )

    first_run = history[0]

    assert "accepted_count" in first_run
    assert "deferred_count" in first_run
    assert "rejected_count" in first_run

    assert (
        first_run["total_results"]
        == first_run["accepted_count"]
        + first_run["deferred_count"]
        + first_run["rejected_count"]
    )


def test_execution_persistence_includes_planning_and_validation(
    tmp_path,
):
    store, project = create_persisted_project(
        tmp_path
    )

    history = store.get_execution_history(
        project.name
    )

    execution = history[0]["executions"][0]

    assert execution["planning"] is not None
    assert execution["planning"]["objective"]

    assert execution["validation"] is not None
    assert "valid" in execution["validation"]
    assert execution["validation"]["reason"]