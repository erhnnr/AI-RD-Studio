from dataclasses import dataclass, field
from typing import List

from studio.core.models import Signal
from studio.core.project import Project


@dataclass
class ProjectContext:
    """
    Runtime context for executing a Studio project.
    """

    project: Project
    signals: List[Signal] = field(default_factory=list)