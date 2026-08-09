from dataclasses import dataclass
from enum import Enum
from typing import Optional

from studio.core.experiment import Measurement
from studio.core.outcome import OutcomeObservation


class ComparisonStatus(str, Enum):
    MET = "MET"
    NOT_MET = "NOT_MET"
    NOT_COMPARABLE = "NOT_COMPARABLE"


@dataclass
class OutcomeComparison:
    metric: str
    status: ComparisonStatus
    expected_target: Optional[float]
    observed_value: object
    reason: str


def compare_measurement_to_observation(
    measurement: Measurement,
    observation: OutcomeObservation,
) -> OutcomeComparison:
    if not isinstance(measurement, Measurement):
        raise TypeError(
            "measurement must be a Measurement."
        )

    if not isinstance(observation, OutcomeObservation):
        raise TypeError(
            "observation must be an OutcomeObservation."
        )

    if measurement.metric != observation.metric:
        return OutcomeComparison(
            metric=measurement.metric,
            status=ComparisonStatus.NOT_COMPARABLE,
            expected_target=measurement.target,
            observed_value=observation.observed_value,
            reason=(
                "Measurement metric and observation metric "
                "do not match."
            ),
        )

    if measurement.target is None:
        return OutcomeComparison(
            metric=measurement.metric,
            status=ComparisonStatus.NOT_COMPARABLE,
            expected_target=None,
            observed_value=observation.observed_value,
            reason=(
                "Measurement has no numeric target for "
                "deterministic comparison."
            ),
        )

    if not isinstance(
        observation.observed_value,
        (int, float),
    ):
        return OutcomeComparison(
            metric=measurement.metric,
            status=ComparisonStatus.NOT_COMPARABLE,
            expected_target=measurement.target,
            observed_value=observation.observed_value,
            reason=(
                "Observed value is not numeric."
            ),
        )

    if measurement.unit != observation.unit:
        return OutcomeComparison(
            metric=measurement.metric,
            status=ComparisonStatus.NOT_COMPARABLE,
            expected_target=measurement.target,
            observed_value=observation.observed_value,
            reason=(
                "Measurement unit and observation unit "
                "do not match."
            ),
        )

    if float(observation.observed_value) >= measurement.target:
        return OutcomeComparison(
            metric=measurement.metric,
            status=ComparisonStatus.MET,
            expected_target=measurement.target,
            observed_value=observation.observed_value,
            reason=(
                "Observed numeric value meets or exceeds "
                "the configured target."
            ),
        )

    return OutcomeComparison(
        metric=measurement.metric,
        status=ComparisonStatus.NOT_MET,
        expected_target=measurement.target,
        observed_value=observation.observed_value,
        reason=(
            "Observed numeric value is below "
            "the configured target."
        ),
    )