from studio.workers.base import BaseWorker
from studio.core.project import Project


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
            "Project",
        ]

        self.output_types = [
            "ResearchAnalysis",
        ]

    def execute(self, project: Project):

        return {
            "worker": self.name,
            "project": project.name,
            "analysis": (
                f"Research analysis prepared for {project.name}"
            ),
        }