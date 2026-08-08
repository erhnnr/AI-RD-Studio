from dataclasses import dataclass
from typing import Optional

from studio.core.project import Project
from studio.core.models import ResearchResult


@dataclass
class WorkerContext:
    """
    Shared execution context for AI-RD-Studio workers.
    """

    project: Optional[Project] = None
    task: object = None
    signal: object = None
    opportunity: object = None
    research_result: Optional[ResearchResult] = None