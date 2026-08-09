from studio.core.experiment import (
    Experiment,
    Hypothesis,
    Measurement,
)
from studio.core.models import (
    Opportunity,
    PlanningResult,
    Signal,
    ValidationResult,
)
from studio.workers.validation_worker import ValidationWorker


def create_opportunity(
    evidence_state: str = "SUPPORTING",
) -> Opportunity:
    return Opportunity(
        signal=Signal(
            title="AI education opportunity",
            description="Controlled validation signal.",
            source="test",
        ),
        impact=6,
        urgency=5,
        feasibility=6,
        strategic_fit=6,
        evidence_state=evidence_state,
        evidence_confidence=0.8,
        rationale="Controlled supporting evidence.",
    )


def create_hypothesis() -> Hypothesis:
    return Hypothesis(
        statement=(
            "A bounded test can determine whether "
            "the opportunity should progress."
        ),
        assumptions=[
            "The controlled test remains representative.",
        ],
        success_criteria=[
            "The measured outcome supports progression.",
        ],
        failure_criteria=[
            "The measured outcome does not support progression.",
        ],
    )


def create_experiment() -> Experiment:
    return Experiment(
        objective="Test the opportunity under controlled conditions.",
        method="Run a bounded controlled comparison.",
        measurements=[
            Measurement(
                metric="observable outcome",
            ),
        ],
        stop_conditions=[
            "Success criterion reached.",
            "Failure criterion reached.",
        ],
    )


def create_planning_result(
    evidence_state: str = "SUPPORTING",
) -> PlanningResult:
    return PlanningResult(
        opportunity=create_opportunity(
            evidence_state=evidence_state,
        ),
        objective=(
            "Test opportunity through a bounded R&D experiment: "
            "AI education opportunity"
        ),
        steps=[
            "Review the opportunity evidence and assumptions.",
            "Define the test boundary.",
            "Measure the observable outcome.",
            "Compare evidence with success and failure criteria.",
        ],
        hypothesis=create_hypothesis(),
        experiment=create_experiment(),
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
    assert result.worker == "ValidationWorker"


def test_validation_worker_rejects_missing_objective():
    planning_result = create_planning_result()
    planning_result.objective = ""

    result = ValidationWorker().execute(
        planning_result
    )

    assert result.valid is False
    assert "objective" in result.reason.lower()


def test_validation_worker_rejects_missing_steps():
    planning_result = create_planning_result()
    planning_result.steps = []

    result = ValidationWorker().execute(
        planning_result
    )

    assert result.valid is False
    assert "steps" in result.reason.lower()