import pytest

from studio.core.experiment import (
    Measurement,
    MeasurementDirection,
)
from studio.core.outcome import OutcomeObservation
from studio.core.outcome_comparison import (
    ComparisonStatus,
    compare_measurement_to_observation,
)


def test_at_least_target_is_met():
    measurement = Measurement(
        metric="throughput",
        target=100,
        unit="requests_per_second",
        direction=MeasurementDirection.AT_LEAST,
    )

    observation = OutcomeObservation(
        metric="throughput",
        observed_value=125,
        unit="requests_per_second",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.MET
    assert result.expected_target == 100
    assert result.observed_value == 125


def test_at_least_equal_value_is_met():
    measurement = Measurement(
        metric="accuracy",
        target=90,
        unit="percent",
        direction=MeasurementDirection.AT_LEAST,
    )

    observation = OutcomeObservation(
        metric="accuracy",
        observed_value=90,
        unit="percent",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.MET


def test_at_least_target_not_met():
    measurement = Measurement(
        metric="coverage",
        target=80,
        unit="percent",
        direction=MeasurementDirection.AT_LEAST,
    )

    observation = OutcomeObservation(
        metric="coverage",
        observed_value=65,
        unit="percent",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.NOT_MET


def test_at_most_target_is_met():
    measurement = Measurement(
        metric="latency",
        target=100,
        unit="ms",
        direction=MeasurementDirection.AT_MOST,
    )

    observation = OutcomeObservation(
        metric="latency",
        observed_value=80,
        unit="ms",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.MET


def test_at_most_target_not_met():
    measurement = Measurement(
        metric="error_rate",
        target=2,
        unit="percent",
        direction=MeasurementDirection.AT_MOST,
    )

    observation = OutcomeObservation(
        metric="error_rate",
        observed_value=5,
        unit="percent",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.NOT_MET


def test_exact_target_is_met():
    measurement = Measurement(
        metric="required_nodes",
        target=4,
        unit="count",
        direction=MeasurementDirection.EXACT,
    )

    observation = OutcomeObservation(
        metric="required_nodes",
        observed_value=4,
        unit="count",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.MET


def test_missing_target_is_not_comparable():
    measurement = Measurement(
        metric="latency",
        target=None,
        unit="ms",
        direction=MeasurementDirection.AT_MOST,
    )

    observation = OutcomeObservation(
        metric="latency",
        observed_value=120,
        unit="ms",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.NOT_COMPARABLE
    assert "no numeric target" in result.reason


def test_missing_direction_is_not_comparable():
    measurement = Measurement(
        metric="latency",
        target=100,
        unit="ms",
    )

    observation = OutcomeObservation(
        metric="latency",
        observed_value=80,
        unit="ms",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.NOT_COMPARABLE
    assert "no explicit target direction" in result.reason


def test_textual_observation_is_not_comparable():
    measurement = Measurement(
        metric="operator feedback",
        target=1,
        unit=None,
        direction=MeasurementDirection.AT_LEAST,
    )

    observation = OutcomeObservation(
        metric="operator feedback",
        observed_value="usable",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.NOT_COMPARABLE
    assert "not numeric" in result.reason


def test_different_metric_is_not_comparable():
    measurement = Measurement(
        metric="latency",
        target=100,
        unit="ms",
        direction=MeasurementDirection.AT_MOST,
    )

    observation = OutcomeObservation(
        metric="throughput",
        observed_value=120,
        unit="ms",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.NOT_COMPARABLE
    assert "do not match" in result.reason


def test_different_unit_is_not_comparable():
    measurement = Measurement(
        metric="latency",
        target=100,
        unit="ms",
        direction=MeasurementDirection.AT_MOST,
    )

    observation = OutcomeObservation(
        metric="latency",
        observed_value=1,
        unit="seconds",
    )

    result = compare_measurement_to_observation(
        measurement,
        observation,
    )

    assert result.status == ComparisonStatus.NOT_COMPARABLE
    assert "unit" in result.reason.lower()


def test_invalid_measurement_rejected():
    with pytest.raises(
        TypeError,
        match="Measurement",
    ):
        compare_measurement_to_observation(
            "invalid",
            OutcomeObservation(
                metric="metric",
                observed_value=1,
            ),
        )


def test_invalid_observation_rejected():
    with pytest.raises(
        TypeError,
        match="OutcomeObservation",
    ):
        compare_measurement_to_observation(
            Measurement(
                metric="metric",
                target=1,
                direction=MeasurementDirection.AT_LEAST,
            ),
            "invalid",
        )


def test_measurement_rejects_invalid_direction():
    with pytest.raises(
        TypeError,
        match="MeasurementDirection",
    ):
        Measurement(
            metric="metric",
            target=1,
            direction="AT_LEAST",
        )