from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Measurement:
    metric: str
    baseline: Optional[float] = None
    target: Optional[float] = None
    unit: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.metric, str) or not self.metric.strip():
            raise ValueError(
                "Measurement.metric must be a non-empty string."
            )

        if self.baseline is not None and not isinstance(
            self.baseline,
            (int, float),
        ):
            raise TypeError(
                "Measurement.baseline must be a number or None."
            )

        if self.target is not None and not isinstance(
            self.target,
            (int, float),
        ):
            raise TypeError(
                "Measurement.target must be a number or None."
            )

        if self.unit is not None and not isinstance(
            self.unit,
            str,
        ):
            raise TypeError(
                "Measurement.unit must be a string or None."
            )

        if self.baseline is not None:
            self.baseline = float(self.baseline)

        if self.target is not None:
            self.target = float(self.target)


@dataclass
class Hypothesis:
    statement: str
    assumptions: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    failure_criteria: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.statement, str) or not self.statement.strip():
            raise ValueError(
                "Hypothesis.statement must be a non-empty string."
            )

        self._validate_string_list(
            self.assumptions,
            "Hypothesis.assumptions",
        )

        self._validate_string_list(
            self.success_criteria,
            "Hypothesis.success_criteria",
        )

        self._validate_string_list(
            self.failure_criteria,
            "Hypothesis.failure_criteria",
        )

    @staticmethod
    def _validate_string_list(
        values,
        field_name: str,
    ) -> None:
        if not isinstance(values, list):
            raise TypeError(
                f"{field_name} must be a list."
            )

        for value in values:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field_name} must contain non-empty strings."
                )


@dataclass
class Experiment:
    objective: str
    method: str
    measurements: List[Measurement] = field(default_factory=list)
    stop_conditions: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.objective, str) or not self.objective.strip():
            raise ValueError(
                "Experiment.objective must be a non-empty string."
            )

        if not isinstance(self.method, str) or not self.method.strip():
            raise ValueError(
                "Experiment.method must be a non-empty string."
            )

        if not isinstance(self.measurements, list):
            raise TypeError(
                "Experiment.measurements must be a list."
            )

        for measurement in self.measurements:
            if not isinstance(measurement, Measurement):
                raise TypeError(
                    "Experiment.measurements must contain "
                    "Measurement objects."
                )

        if not isinstance(self.stop_conditions, list):
            raise TypeError(
                "Experiment.stop_conditions must be a list."
            )

        for condition in self.stop_conditions:
            if not isinstance(condition, str) or not condition.strip():
                raise ValueError(
                    "Experiment.stop_conditions must contain "
                    "non-empty strings."
                )