from studio.core.models import Signal, Opportunity
from studio.runtime.task_manager import TaskManager


def test_task_manager_creates_research_task():
    signal = Signal(
        title="New AI technology",
        description="A new AI development appeared",
        source="research",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
    )

    manager = TaskManager()

    task = manager.create_task(
        opportunity,
        "Analyze technology impact",
    )

    assert task.opportunity == opportunity
    assert task.objective == "Analyze technology impact"
    assert task.status == "NEW"