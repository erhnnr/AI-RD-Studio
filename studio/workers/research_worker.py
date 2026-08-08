from typing import Optional

from studio.workers.base import BaseWorker
from studio.workers.research_provider import ResearchProvider
from studio.core.project import Project
from studio.core.worker_context import WorkerContext
from studio.core.models import ResearchResult


class ResearchWorker(BaseWorker):
    """
    Worker responsible for project and signal research.
    """

    def __init__(
        self,
        provider: Optional[ResearchProvider] = None,
    ):
        super().__init__("ResearchWorker")

        self.provider = provider

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

    def execute(self, context) -> ResearchResult:

        if isinstance(context, WorkerContext):

            signal = context.signal

            if self.provider is not None:

                analysis = self.provider.research(
                    signal
                )

            else:

                analysis = (
                    f"Research analysis prepared for "
                    f"{signal.title}"
                )

            return ResearchResult(
                worker=self.name,
                signal=signal,
                analysis=analysis,
            )

        if isinstance(context, Project):

            return ResearchResult(
                worker=self.name,
                project_name=context.name,
                analysis=(
                    f"Research analysis prepared for "
                    f"{context.name}"
                ),
            )

        return ResearchResult(
            worker=self.name,
            analysis="Research analysis prepared.",
        )