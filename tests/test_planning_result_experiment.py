import pytest

from studio.core.experiment import (
    Experiment,
    Hypothesis,
    Measurement,
)
from studio.core.models import Opportunity, PlanningResult, Signal


def make_opportunity() -> Opportunity:
    return Opportunity(
        signal=Signal(
            title="Controlled Opportunity",
            description="Controlled signal.",
            source="test",
        ),
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
    )


def make_hypothesis() -> Hypothesis:
    return Hypothesis(
        statement="The intervention improves the target metric.",
        assumptions=[
            "The intervention is used consistently.",
        ],
        success_criteria=[
            "The target metric improves.",
        ],
        failure_criteria=[
            "The target metric does not improve.",
        ],
    )


def make_experiment() -> Experiment:
    return Experiment(
        objective="Test whether the target metric improves.",
        method="Run a controlled comparison.",
        measurements=[
            Measurement(
                metric="target metric",
                baseline=10,
                target=15,
                unit="points",
            )
        ],
        stop_conditions=[
            "Success criterion reached.",
            "Failure criterion reached.",
        ],
    )


def test_planning_result_accepts_hypothesis_and_experiment():
    opportunity = make_opportunity()
    hypothesis = make_hypothesis()
    experiment = make_experiment()

    result = PlanningResult(
        opportunity=opportunity,
        objective="Evaluate the controlled opportunity.",
        steps=[
            "Run the controlled experiment.",
        ],
        hypothesis=hypothesis,
        experiment=experiment,
    )

    assert result.hypothesis is hypothesis
    assert result.experiment is experiment


def test_planning_result_remains_backward_compatible():
    result = PlanningResult(
        opportunity=make_opportunity(),
        objective="Legacy-compatible plan.",
        steps=[
            "Review the opportunity.",
        ],
    )

    assert result.hypothesis is None
    assert result.experiment is None


def test_planning_result_rejects_invalid_hypothesis():
    with pytest.raises(
        TypeError,
        match="must be a Hypothesis or None",
    ):
        PlanningResult(
            opportunity=make_opportunity(),
            objective="Invalid plan.",
            hypothesis="not a hypothesis",
        )


def test_planning_result_rejects_invalid_experiment():
    with pytest.raises(
        TypeError,
        match="must be an Experiment or None",
    ):
        PlanningResult(
            opportunity=make_opportunity(),
            objective="Invalid plan.",
            experiment="not an experiment",
        )