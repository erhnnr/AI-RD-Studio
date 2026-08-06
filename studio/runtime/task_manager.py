from studio.core.models import ResearchTask, Opportunity


class TaskManager:
    """
    Creates research tasks from opportunities.
    """

    def create_task(
        self,
        opportunity: Opportunity,
        objective: str,
    ) -> ResearchTask:
        return ResearchTask(
            opportunity=opportunity,
            objective=objective,
        )