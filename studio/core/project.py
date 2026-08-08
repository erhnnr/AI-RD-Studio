from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Project:
    """
    Represents a Studio managed project.
    """

    name: str
    objective: str
    priority: str
    status: str = "NEW"
    tasks: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


    def add_task(self, task: str):
        """
        Add task to project.
        """

        self.tasks.append(task)