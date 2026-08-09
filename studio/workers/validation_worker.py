from studio.core.models import PlanningResult, ValidationResult
from studio.workers.base import BaseWorker


class ValidationWorker(BaseWorker):
    """
    Worker responsible for validating whether an R&D plan
    is sufficiently supported, testable, measurable, and bounded
    to justify progression.
    """

    def __init__(self):
        super().__init__("ValidationWorker")

        self.capabilities = [
            "validation",
            "plan_validation",
            "execution_validation",
        ]

        self.input_types = [
            "PlanningResult",
        ]

        self.output_types = [
            "ValidationResult",
        ]

    def execute(
        self,
        planning_result: PlanningResult,
    ) -> ValidationResult:

        if not isinstance(planning_result, PlanningResult):
            raise TypeError(
                "ValidationWorker requires a PlanningResult."
            )

        if not planning_result.objective:
            return self._invalid(
                planning_result,
                "Planning objective is missing.",
            )

        if not planning_result.steps:
            return self._invalid(
                planning_result,
                "Planning steps are missing.",
            )

        opportunity = planning_result.opportunity

        if opportunity is None:
            return self._invalid(
                planning_result,
                "PlanningResult must contain an Opportunity.",
            )

        evidence_state = opportunity.evidence_state

        if evidence_state == "CONTRADICTORY":
            return self._invalid(
                planning_result,
                (
                    "Progression is invalid because current evidence "
                    "materially contradicts the opportunity."
                ),
            )

        if evidence_state == "INSUFFICIENT":
            return self._invalid(
                planning_result,
                (
                    "Progression is invalid because available evidence "
                    "is insufficient."
                ),
            )

        if evidence_state == "MIXED":
            return self._invalid(
                planning_result,
                (
                    "Progression is invalid because supporting and "
                    "contradictory evidence remain unresolved."
                ),
            )

        if evidence_state != "SUPPORTING":
            return self._invalid(
                planning_result,
                (
                    "Progression requires an explicit SUPPORTING "
                    "evidence state."
                ),
            )

        hypothesis = planning_result.hypothesis

        if hypothesis is None:
            return self._invalid(
                planning_result,
                "A testable Hypothesis is required.",
            )

        if not hypothesis.statement:
            return self._invalid(
                planning_result,
                "Hypothesis statement is missing.",
            )

        if not hypothesis.success_criteria:
            return self._invalid(
                planning_result,
                "Hypothesis success criteria are missing.",
            )

        if not hypothesis.failure_criteria:
            return self._invalid(
                planning_result,
                "Hypothesis failure criteria are missing.",
            )

        experiment = planning_result.experiment

        if experiment is None:
            return self._invalid(
                planning_result,
                "An Experiment is required.",
            )

        if not experiment.objective:
            return self._invalid(
                planning_result,
                "Experiment objective is missing.",
            )

        if not experiment.method:
            return self._invalid(
                planning_result,
                "Experiment method is missing.",
            )

        if not experiment.measurements:
            return self._invalid(
                planning_result,
                "At least one Measurement is required.",
            )

        for measurement in experiment.measurements:
            if not measurement.metric:
                return self._invalid(
                    planning_result,
                    "Every Measurement must define a metric.",
                )

        if not experiment.stop_conditions:
            return self._invalid(
                planning_result,
                "At least one experiment stop condition is required.",
            )

        return ValidationResult(
            planning_result=planning_result,
            valid=True,
            reason=(
                "Plan passed R&D progression validation: "
                "supporting evidence, testable hypothesis, "
                "measurable experiment, and stop conditions are present."
            ),
            worker=self.name,
        )

    def _invalid(
        self,
        planning_result: PlanningResult,
        reason: str,
    ) -> ValidationResult:
        return ValidationResult(
            planning_result=planning_result,
            valid=False,
            reason=reason,
            worker=self.name,
        )