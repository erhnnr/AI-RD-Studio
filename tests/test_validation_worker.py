from studio.core.models import (
    Opportunity,
    PlanningResult,
    Signal,
    ValidationResult,
)
from studio.workers.validation_worker import ValidationWorker


def create_planning_result():

    signal = Signal(
        title="AI education opportunity",
        description="AI tutoring demand is increasing.",
        source="Market",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=9,
        urgency=8,
        feasibility=8,
        strategic_fit=10,
    )

    return PlanningResult(
        opportunity=opportunity,
        objective=(
            "Investigate and execute opportunity: "
            "AI education opportunity"
        ),
        steps=[
            "Review research findings",
            "Define execution objective",
        ],
    )


def test_validation_worker_accepts_valid_plan():

    planning_result = create_planning_result()

    worker = ValidationWorker()

    result = worker.execute(
        planning_result
    )

    assert isinstance(
        result,
        ValidationResult,
    )

    assert result.planning_result is planning_result
    assert result.valid is True
    assert result.reason == "Plan passed validation."
    assert result.worker == "ValidationWorker"
    assert result.created_at is not None


def test_validation_worker_rejects_plan_without_steps():

    planning_result = create_planning_result()

    planning_result.steps = []

    worker = ValidationWorker()

    result = worker.execute(
        planning_result
    )

    assert result.valid is False
    assert result.reason == (
        "Planning steps are missing."
    )


def test_validation_worker_declares_contract():

    worker = ValidationWorker()

    metadata = worker.get_metadata()

    assert "validation" in metadata["capabilities"]
    assert "PlanningResult" in metadata["input_types"]
    assert "ValidationResult" in metadata["output_types"]