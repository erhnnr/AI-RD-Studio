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


def make_opportunity() -> Opportunity:
    return Opportunity(
        signal=Signal(
            title="Controlled Outcome Opportunity",
            description="Controlled outcome test signal.",
            source="test",
        ),
        impact=6,
        urgency=5,
        feasibility=6,
        strategic_fit=6,
        evidence_state="SUPPORTING",
        evidence_confidence=0.9,
        rationale="Controlled supporting evidence.",
    )


def make_planning_result(
    opportunity: Opportunity,
) -> PlanningResult:
    return PlanningResult(
        opportunity=opportunity,
        objective="Run controlled outcome experiment.",
        steps=[
            "Run experiment.",
            "Observe result.",
        ],
    )


def make_decision():
    return SimpleNamespace(
        decision="ACCEPT",
        reason="Controlled acceptance.",
        confidence=80,
        next_action="Run experiment",
    )


def test_outcome_status_values():
    assert OutcomeStatus.SUCCESS.value == "SUCCESS"
    assert OutcomeStatus.FAILURE.value == "FAILURE"
    assert OutcomeStatus.PARTIAL.value == "PARTIAL"
    assert OutcomeStatus.INCONCLUSIVE.value == "INCONCLUSIVE"
    assert OutcomeStatus.NOT_OBSERVED.value == "NOT_OBSERVED"


def test_create_numeric_outcome_observation():
    observation = OutcomeObservation(
        metric="latency",
        observed_value=120,
        unit="ms",
        note="Observed after controlled test.",
    )

    assert observation.metric == "latency"
    assert observation.observed_value == 120
    assert observation.unit == "ms"


def test_create_textual_outcome_observation():
    observation = OutcomeObservation(
        metric="operator feedback",
        observed_value="usable",
    )

    assert observation.observed_value == "usable"


def test_outcome_observation_requires_metric():
    with pytest.raises(
        ValueError,
        match="metric",
    ):
        OutcomeObservation(
            metric="",
            observed_value=10,
        )


def test_outcome_observation_rejects_invalid_value():
    with pytest.raises(
        TypeError,
        match="observed_value",
    ):
        OutcomeObservation(
            metric="controlled metric",
            observed_value=["invalid"],
        )


def test_create_successful_decision_outcome():
    opportunity = make_opportunity()
    planning_result = make_planning_result(
        opportunity
    )

    outcome = DecisionOutcome(
        opportunity=opportunity,
        planning_result=planning_result,
        decision=make_decision(),
        status=OutcomeStatus.SUCCESS,
        observations=[
            OutcomeObservation(
                metric="target outcome",
                observed_value=17,
                unit="points",
            )
        ],
        summary="Target outcome exceeded the expected condition.",
    )

    assert outcome.opportunity is opportunity
    assert outcome.planning_result is planning_result
    assert outcome.status == OutcomeStatus.SUCCESS
    assert len(outcome.observations) == 1


def test_create_failure_decision_outcome():
    opportunity = make_opportunity()

    outcome = DecisionOutcome(
        opportunity=opportunity,
        planning_result=make_planning_result(
            opportunity
        ),
        decision=make_decision(),
        status=OutcomeStatus.FAILURE,
        observations=[
            OutcomeObservation(
                metric="target outcome",
                observed_value=4,
                unit="points",
            )
        ],
        summary="Observed outcome failed the bounded success condition.",
    )

    assert outcome.status == OutcomeStatus.FAILURE


def test_not_observed_outcome_allows_no_observations():
    opportunity = make_opportunity()

    outcome = DecisionOutcome(
        opportunity=opportunity,
        planning_result=make_planning_result(
            opportunity
        ),
        decision=make_decision(),
        status=OutcomeStatus.NOT_OBSERVED,
    )

    assert outcome.observations == []
    assert outcome.status != OutcomeStatus.SUCCESS


def test_not_observed_rejects_invented_observations():
    opportunity = make_opportunity()

    with pytest.raises(
        ValueError,
        match="cannot contain observations",
    ):
        DecisionOutcome(
            opportunity=opportunity,
            planning_result=make_planning_result(
                opportunity
            ),
            decision=make_decision(),
            status=OutcomeStatus.NOT_OBSERVED,
            observations=[
                OutcomeObservation(
                    metric="invented metric",
                    observed_value=10,
                )
            ],
        )


def test_observed_status_requires_observation():
    opportunity = make_opportunity()

    with pytest.raises(
        ValueError,
        match="requires at least one observation",
    ):
        DecisionOutcome(
            opportunity=opportunity,
            planning_result=make_planning_result(
                opportunity
            ),
            decision=make_decision(),
            status=OutcomeStatus.SUCCESS,
            summary="No observation exists.",
        )


def test_observed_status_requires_summary():
    opportunity = make_opportunity()

    with pytest.raises(
        ValueError,
        match="requires a summary",
    ):
        DecisionOutcome(
            opportunity=opportunity,
            planning_result=make_planning_result(
                opportunity
            ),
            decision=make_decision(),
            status=OutcomeStatus.PARTIAL,
            observations=[
                OutcomeObservation(
                    metric="target outcome",
                    observed_value=11,
                )
            ],
        )


def test_outcome_requires_same_opportunity_as_plan():
    opportunity = make_opportunity()
    other_opportunity = make_opportunity()

    planning_result = make_planning_result(
        other_opportunity
    )

    with pytest.raises(
        ValueError,
        match="same Opportunity",
    ):
        DecisionOutcome(
            opportunity=opportunity,
            planning_result=planning_result,
            decision=make_decision(),
            status=OutcomeStatus.NOT_OBSERVED,
        )


def test_outcome_requires_decision_contract():
    opportunity = make_opportunity()

    with pytest.raises(
        TypeError,
        match="must expose",
    ):
        DecisionOutcome(
            opportunity=opportunity,
            planning_result=make_planning_result(
                opportunity
            ),
            decision=SimpleNamespace(
                decision="ACCEPT",
            ),
            status=OutcomeStatus.NOT_OBSERVED,
        )


def test_outcome_rejects_invalid_status():
    opportunity = make_opportunity()

    with pytest.raises(
        TypeError,
        match="OutcomeStatus",
    ):
        DecisionOutcome(
            opportunity=opportunity,
            planning_result=make_planning_result(
                opportunity
            ),
            decision=make_decision(),
            status="SUCCESS",
        )