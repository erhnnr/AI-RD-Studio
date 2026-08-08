from studio.runtime.project_manager import ProjectManager


def test_project_status_update():

    manager = ProjectManager()

    project = manager.create_project(
        name="AI Research",
        objective="Build AI system",
        priority="HIGH",
    )

    manager.start_project(project)

    assert project.status == "ACTIVE"


def test_project_completion():

    manager = ProjectManager()

    project = manager.create_project(
        name="AI Research",
        objective="Build AI system",
        priority="HIGH",
    )

    manager.start_project(project)
    manager.complete_project(project)

    assert project.status == "COMPLETED"