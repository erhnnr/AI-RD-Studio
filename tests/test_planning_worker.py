from studio.core.models import (
    Opportunity,
    PlanningResult,
    Signal,
)
from studio.workers.planning_worker import PlanningWorker


def create_opportunity():

    signal = Signal(
        title="AI education opportunity",
        description="AI tutoring demand is increasing.",
        source="Market",
    )

    return Opportunity(
        signal=signal,
        impact=9,
        urgency=8,
        feasibility=8,
        strategic_fit=10,
    )


def test_planning_worker_creates_structured_plan():

    opportunity = create_opportunity()

    worker = PlanningWorker()

    result = worker.execute(
        opportunity
    )

    assert isinstance(
        result,
        PlanningResult,
    )

    assert result.opportunity is opportunity
    assert result.worker == "PlanningWorker"

    assert result.objective == (
        "Investigate and execute opportunity: "
        "AI education opportunity"
    )

    assert len(result.steps) == 4
    assert result.created_at is not None


def test_planning_worker_declares_contract():

    worker = PlanningWorker()

    metadata = worker.get_metadata()

    assert "planning" in metadata["capabilities"]
    assert "Opportunity" in metadata["input_types"]
    assert "PlanningResult" in metadata["output_types"]