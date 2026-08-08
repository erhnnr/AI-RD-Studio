from studio.core.project import Project


def test_project_creation():

    project = Project(
        name="AI Education Platform",
        objective="Build personal AI teacher",
        priority="HIGH",
    )

    assert project.name == "AI Education Platform"
    assert project.status == "NEW"
    assert len(project.tasks) == 0


def test_project_add_task():

    project = Project(
        name="AI Research",
        objective="Explore AI systems",
        priority="MEDIUM",
    )

    project.add_task("Research existing models")

    assert len(project.tasks) == 1
    assert project.tasks[0] == "Research existing models"