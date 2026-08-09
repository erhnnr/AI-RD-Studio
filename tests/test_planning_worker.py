from studio.core.models import Opportunity, PlanningResult, Signal
from studio.workers.planning_worker import PlanningWorker


def create_opportunity() -> Opportunity:
    return Opportunity(
        signal=Signal(
            title="AI education opportunity",
            description="Controlled planning signal.",
            source="test",
        ),
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
        evidence_state="SUPPORTING",
        evidence_confidence=0.8,
        rationale="Controlled supporting evidence.",
    )


def test_planning_worker_creates_testable_structured_plan():
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
        "Test opportunity through a bounded R&D experiment: "
        "AI education opportunity"
    )

    assert result.hypothesis is not None
    assert result.experiment is not None

    assert len(result.hypothesis.assumptions) > 0
    assert len(result.hypothesis.success_criteria) > 0
    assert len(result.hypothesis.failure_criteria) > 0

    assert len(result.experiment.measurements) > 0
    assert len(result.experiment.stop_conditions) > 0

    assert len(result.steps) == 5


def test_planning_worker_contract():
    worker = PlanningWorker()

    metadata = worker.get_metadata()

    assert "planning" in metadata["capabilities"]
    assert "Opportunity" in metadata["input_types"]
    assert "PlanningResult" in metadata["output_types"]