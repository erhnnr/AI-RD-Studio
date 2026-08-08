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