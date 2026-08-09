from studio.core.models import PlanningResult, ValidationResult
from studio.workers.base import BaseWorker


class ValidationWorker(BaseWorker):
    """
    Worker responsible for validating execution plans.
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

        if not planning_result.objective:
            return ValidationResult(
                planning_result=planning_result,
                valid=False,
                reason="Planning objective is missing.",
                worker=self.name,
            )

        if not planning_result.steps:
            return ValidationResult(
                planning_result=planning_result,
                valid=False,
                reason="Planning steps are missing.",
                worker=self.name,
            )

        return ValidationResult(
            planning_result=planning_result,
            valid=True,
            reason="Plan passed validation.",
            worker=self.name,
        )