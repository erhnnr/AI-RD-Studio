from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from studio.core.models import Opportunity, PlanningResult


ObservedValue = Union[int, float, str]


class OutcomeStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PARTIAL = "PARTIAL"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_OBSERVED = "NOT_OBSERVED"


@dataclass
class OutcomeObservation:
    metric: str
    observed_value: ObservedValue
    unit: Optional[str] = None
    note: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.metric, str) or not self.metric.strip():
            raise ValueError(
                "OutcomeObservation.metric must be a non-empty string."
            )

        if not isinstance(
            self.observed_value,
            (int, float, str),
        ):
            raise TypeError(
                "OutcomeObservation.observed_value must be "
                "an int, float, or string."
            )

        if isinstance(self.observed_value, str):
            if not self.observed_value.strip():
                raise ValueError(
                    "OutcomeObservation.observed_value must not "
                    "be an empty string."
                )

        if self.unit is not None:
            if not isinstance(self.unit, str):
                raise TypeError(
                    "OutcomeObservation.unit must be a string or None."
                )

            if not self.unit.strip():
                raise ValueError(
                    "OutcomeObservation.unit must not be empty "
                    "when provided."
                )

        if self.note is not None:
            if not isinstance(self.note, str):
                raise TypeError(
                    "OutcomeObservation.note must be a string or None."
                )

            if not self.note.strip():
                raise ValueError(
                    "OutcomeObservation.note must not be empty "
                    "when provided."
                )


@dataclass
class DecisionOutcome:
    opportunity: Opportunity
    planning_result: PlanningResult
    decision: object
    status: OutcomeStatus
    observations: List[OutcomeObservation] = field(
        default_factory=list
    )
    summary: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not isinstance(self.opportunity, Opportunity):
            raise TypeError(
                "DecisionOutcome.opportunity must be an Opportunity."
            )

        if not isinstance(self.planning_result, PlanningResult):
            raise TypeError(
                "DecisionOutcome.planning_result must be "
                "a PlanningResult."
            )

        if self.planning_result.opportunity is not self.opportunity:
            raise ValueError(
                "DecisionOutcome planning_result must reference "
                "the same Opportunity."
            )

        if self.decision is None:
            raise TypeError(
                "DecisionOutcome.decision is required."
            )

        required_decision_attributes = (
            "decision",
            "reason",
            "next_action",
        )

        for attribute in required_decision_attributes:
            if not hasattr(
                self.decision,
                attribute,
            ):
                raise TypeError(
                    "DecisionOutcome.decision must expose "
                    "decision, reason, and next_action."
                )

        if not isinstance(self.status, OutcomeStatus):
            raise TypeError(
                "DecisionOutcome.status must be an OutcomeStatus."
            )

        if not isinstance(self.observations, list):
            raise TypeError(
                "DecisionOutcome.observations must be a list."
            )

        for observation in self.observations:
            if not isinstance(
                observation,
                OutcomeObservation,
            ):
                raise TypeError(
                    "DecisionOutcome.observations must contain "
                    "OutcomeObservation objects."
                )

        if not isinstance(self.summary, str):
            raise TypeError(
                "DecisionOutcome.summary must be a string."
            )

        if self.status == OutcomeStatus.NOT_OBSERVED:
            if self.observations:
                raise ValueError(
                    "NOT_OBSERVED outcome cannot contain observations."
                )

        else:
            if not self.observations:
                raise ValueError(
                    "Observed outcome status requires at least "
                    "one observation."
                )

            if not self.summary.strip():
                raise ValueError(
                    "Observed outcome status requires a summary."
                )