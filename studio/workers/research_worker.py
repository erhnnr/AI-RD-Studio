from studio.workers.base import BaseWorker
from studio.core.project import Project
from studio.core.worker_context import WorkerContext


class ResearchWorker(BaseWorker):
    """
    Worker responsible for project research.
    """

    def __init__(self):
        super().__init__("ResearchWorker")

        self.capabilities = [
            "research",
            "information_analysis",
            "knowledge_generation",
        ]

        self.input_types = [
            "Signal",
            "WorkerContext",
            "Project",
        ]

        self.output_types = [
            "ResearchResult",
        ]

    def execute(self, context):

        if isinstance(context, WorkerContext):
            signal = context.signal

            return {
                "worker": self.name,
                "signal": signal.title,
                "analysis": (
                    f"Research analysis prepared for "
                    f"{signal.title}"
                ),
            }

        if isinstance(context, Project):
            return {
                "worker": self.name,
                "project": context.name,
                "analysis": (
                    f"Research analysis prepared for "
                    f"{context.name}"
                ),
            }

        return {
            "worker": self.name,
            "analysis": "Research analysis prepared.",
        }