from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List
from uuid import uuid4


class ProblemStatus(str, Enum):
    DRAFT = "DRAFT"
    DEFINED = "DEFINED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"


@dataclass
class ProblemDefinition:
    """
    Structured representation of a real problem that the Studio may
    investigate.

    A ProblemDefinition describes the problem space. It must not be used
    as a container for implementation details, architecture, features,
    or technology choices.
    """

    title: str
    description: str
    source_goal: str

    stakeholders: List[str] = field(default_factory=list)
    target_users: List[str] = field(default_factory=list)
    pain_points: List[str] = field(default_factory=list)
    context: str = ""
    constraints: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    non_goals: List[str] = field(default_factory=list)

    status: ProblemStatus = ProblemStatus.DRAFT
    problem_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        self._require_non_empty_string("title", self.title)
        self._require_non_empty_string("description", self.description)
        self._require_non_empty_string("source_goal", self.source_goal)

        self._require_string_list("stakeholders", self.stakeholders)
        self._require_string_list("target_users", self.target_users)
        self._require_string_list("pain_points", self.pain_points)
        self._require_string_list("constraints", self.constraints)
        self._require_string_list(
            "success_criteria",
            self.success_criteria,
        )
        self._require_string_list("non_goals", self.non_goals)

        if not isinstance(self.context, str):
            raise TypeError(
                "ProblemDefinition.context must be a string."
            )

        if not isinstance(self.status, ProblemStatus):
            raise TypeError(
                "ProblemDefinition.status must be a ProblemStatus."
            )

        self._require_non_empty_string(
            "problem_id",
            self.problem_id,
        )

    @staticmethod
    def _require_non_empty_string(
        field_name: str,
        value: str,
    ) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"ProblemDefinition.{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"ProblemDefinition.{field_name} must not be empty."
            )

    @staticmethod
    def _require_string_list(
        field_name: str,
        value: List[str],
    ) -> None:
        if not isinstance(value, list):
            raise TypeError(
                f"ProblemDefinition.{field_name} must be a list."
            )

        for item in value:
            if not isinstance(item, str):
                raise TypeError(
                    f"ProblemDefinition.{field_name} "
                    "must contain strings."
                )

            if not item.strip():
                raise ValueError(
                    f"ProblemDefinition.{field_name} "
                    "must not contain empty strings."
                )