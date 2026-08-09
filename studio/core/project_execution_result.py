from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from studio.core.models import PipelineResult
from studio.core.project import Project


@dataclass
class ProjectExecutionResult:
    """
    Complete result of a project-level Studio execution.
    """

    project: Project
    results: List[PipelineResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total_results(self) -> int:
        """
        Number of completed signal pipelines.
        """
        return len(self.results)

    @property
    def accepted_count(self) -> int:
        """
        Number of accepted opportunities.
        """
        return sum(
            1
            for result in self.results
            if result.decision.decision == "ACCEPT"
        )

    @property
    def deferred_count(self) -> int:
        """
        Number of deferred opportunities.
        """
        return sum(
            1
            for result in self.results
            if result.decision.decision == "DEFER"
        )

    @property
    def rejected_count(self) -> int:
        """
        Number of rejected opportunities.
        """
        return sum(
            1
            for result in self.results
            if result.decision.decision == "REJECT"
        )

    @property
    def status(self) -> str:
        """
        Project execution status.
        """

        if not self.results:
            return "NO_SIGNALS"

        return "COMPLETED"