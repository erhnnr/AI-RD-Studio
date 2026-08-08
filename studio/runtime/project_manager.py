from studio.core.project import Project


class ProjectManager:
    """
    Manages Studio projects.
    """

    def create_project(
        self,
        name: str,
        objective: str,
        priority: str,
    ) -> Project:
        """
        Create a new project.
        """

        return Project(
            name=name,
            objective=objective,
            priority=priority,
        )

    def add_task(
        self,
        project: Project,
        task: str,
    ):
        """
        Add task to existing project.
        """

        project.add_task(task)

    def start_project(
        self,
        project: Project,
    ):
        """
        Start project lifecycle.
        """

        project.status = "ACTIVE"

    def complete_project(
        self,
        project: Project,
    ):
        """
        Complete project lifecycle.
        """

        project.status = "COMPLETED"