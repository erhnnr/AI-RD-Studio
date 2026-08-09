from studio.core.models import Opportunity, PlanningResult
from studio.workers.base import BaseWorker


class PlanningWorker(BaseWorker):
    """
    Worker responsible for converting an opportunity
    into an actionable execution plan.
    """

    def __init__(self):
        super().__init__("PlanningWorker")

        self.capabilities = [
            "planning",
            "task_planning",
            "execution_planning",
        ]

        self.input_types = [
            "Opportunity",
        ]

        self.output_types = [
            "PlanningResult",
        ]

    def execute(
        self,
        opportunity: Opportunity,
    ) -> PlanningResult:

        objective = (
            f"Investigate and execute opportunity: "
            f"{opportunity.signal.title}"
        )

        steps = [
            "Review research findings",
            "Define execution objective",
            "Prepare implementation tasks",
            "Validate expected outcome",
        ]

        return PlanningResult(
            opportunity=opportunity,
            objective=objective,
            steps=steps,
            worker=self.name,
        )