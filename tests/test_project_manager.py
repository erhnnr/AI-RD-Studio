from studio.core.project import Project
from studio.runtime.project_manager import ProjectManager


def test_project_manager_creates_project():

    manager = ProjectManager()

    project = manager.create_project(
        name="AI Research Platform",
        objective="Build AI R&D system",
        priority="HIGH",
    )

    assert isinstance(project, Project)
    assert project.name == "AI Research Platform"
    assert project.status == "NEW"


def test_project_manager_adds_task():

    manager = ProjectManager()

    project = manager.create_project(
        name="AI Project",
        objective="Research",
        priority="MEDIUM",
    )

    manager.add_task(
        project,
        "Analyze existing solutions",
    )

    assert len(project.tasks) == 1
    assert project.tasks[0] == "Analyze existing solutions"