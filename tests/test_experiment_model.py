import pytest

from studio.core.experiment import (
    Experiment,
    Hypothesis,
    Measurement,
)


def test_create_measurement():
    measurement = Measurement(
        metric="weekly study days",
        baseline=3,
        target=5,
        unit="days/week",
    )

    assert measurement.metric == "weekly study days"
    assert measurement.baseline == 3.0
    assert measurement.target == 5.0
    assert measurement.unit == "days/week"


def test_create_hypothesis():
    hypothesis = Hypothesis(
        statement=(
            "Personal AI Teacher increases "
            "daily study consistency."
        ),
        assumptions=[
            "The student uses the system regularly.",
        ],
        success_criteria=[
            "Weekly study frequency increases.",
        ],
        failure_criteria=[
            "Regular usage does not improve study frequency.",
        ],
    )

    assert (
        hypothesis.statement
        == "Personal AI Teacher increases daily study consistency."
    )

    assert len(hypothesis.assumptions) == 1
    assert len(hypothesis.success_criteria) == 1
    assert len(hypothesis.failure_criteria) == 1


def test_create_experiment():
    measurement = Measurement(
        metric="weekly study days",
        baseline=3,
        target=5,
        unit="days/week",
    )

    experiment = Experiment(
        objective="Measure whether study consistency improves.",
        method=(
            "Run a controlled four-week usage period "
            "and compare weekly study frequency."
        ),
        measurements=[
            measurement,
        ],
        stop_conditions=[
            "Four-week observation period completed.",
            "Failure criterion reached.",
        ],
    )

    assert (
        experiment.objective
        == "Measure whether study consistency improves."
    )

    assert experiment.measurements == [measurement]
    assert len(experiment.stop_conditions) == 2


def test_hypothesis_requires_statement():
    with pytest.raises(ValueError):
        Hypothesis(
            statement="",
        )


def test_hypothesis_rejects_invalid_assumptions():
    with pytest.raises(TypeError):
        Hypothesis(
            statement="Controlled hypothesis.",
            assumptions="not a list",
        )


def test_hypothesis_rejects_empty_success_criterion():
    with pytest.raises(ValueError):
        Hypothesis(
            statement="Controlled hypothesis.",
            success_criteria=[""],
        )


def test_hypothesis_rejects_empty_failure_criterion():
    with pytest.raises(ValueError):
        Hypothesis(
            statement="Controlled hypothesis.",
            failure_criteria=[""],
        )


def test_experiment_requires_objective():
    with pytest.raises(ValueError):
        Experiment(
            objective="",
            method="Controlled method.",
        )


def test_experiment_requires_method():
    with pytest.raises(ValueError):
        Experiment(
            objective="Controlled objective.",
            method="",
        )


def test_experiment_rejects_non_measurement_items():
    with pytest.raises(TypeError):
        Experiment(
            objective="Controlled objective.",
            method="Controlled method.",
            measurements=[
                "not measurement",
            ],
        )


def test_experiment_rejects_empty_stop_condition():
    with pytest.raises(ValueError):
        Experiment(
            objective="Controlled objective.",
            method="Controlled method.",
            stop_conditions=[""],
        )


def test_measurement_rejects_empty_metric():
    with pytest.raises(ValueError):
        Measurement(
            metric="",
        )


def test_measurement_rejects_invalid_baseline():
    with pytest.raises(TypeError):
        Measurement(
            metric="controlled metric",
            baseline="three",
        )


def test_measurement_rejects_invalid_target():
    with pytest.raises(TypeError):
        Measurement(
            metric="controlled metric",
            target="five",
        )