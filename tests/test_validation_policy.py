from studio.core.experiment import (
    Experiment,
    Hypothesis,
    Measurement,
)
from studio.core.models import (
    Opportunity,
    PlanningResult,
    Signal,
)
from studio.workers.validation_worker import ValidationWorker


def make_opportunity(
    evidence_state: str = "SUPPORTING",
) -> Opportunity:
    return Opportunity(
        signal=Signal(
            title="Controlled R&D Opportunity",
            description="Controlled validation signal.",
            source="test",
        ),
        impact=6,
        urgency=5,
        feasibility=6,
        strategic_fit=6,
        evidence_state=evidence_state,
        evidence_confidence=0.9,
        rationale="Controlled validation evidence.",
    )


def make_hypothesis() -> Hypothesis:
    return Hypothesis(
        statement="The bounded intervention improves the target outcome.",
        assumptions=[
            "The controlled test conditions remain stable.",
        ],
        success_criteria=[
            "The measured target outcome improves.",
        ],
        failure_criteria=[
            "The measured target outcome does not improve.",
        ],
    )


def make_experiment() -> Experiment:
    return Experiment(
        objective="Test the target outcome under controlled conditions.",
        method="Run a bounded controlled comparison.",
        measurements=[
            Measurement(
                metric="target outcome",
            ),
        ],
        stop_conditions=[
            "Success criterion reached.",
            "Failure criterion reached.",
        ],
    )


def make_plan(
    evidence_state: str = "SUPPORTING",
) -> PlanningResult:
    return PlanningResult(
        opportunity=make_opportunity(
            evidence_state=evidence_state,
        ),
        objective="Run a bounded R&D validation test.",
        steps=[
            "Review evidence.",
            "Run controlled test.",
            "Measure outcome.",
            "Compare against criteria.",
        ],
        hypothesis=make_hypothesis(),
        experiment=make_experiment(),
    )


def test_complete_supported_plan_passes_validation():
    result = ValidationWorker().execute(
        make_plan()
    )

    assert result.valid is True
    assert "passed R&D progression validation" in result.reason


def test_insufficient_evidence_fails_validation():
    result = ValidationWorker().execute(
        make_plan(
            evidence_state="INSUFFICIENT",
        )
    )

    assert result.valid is False
    assert "insufficient" in result.reason.lower()


def test_mixed_evidence_fails_validation():
    result = ValidationWorker().execute(
        make_plan(
            evidence_state="MIXED",
        )
    )

    assert result.valid is False
    assert "unresolved" in result.reason.lower()


def test_contradictory_evidence_fails_validation():
    result = ValidationWorker().execute(
        make_plan(
            evidence_state="CONTRADICTORY",
        )
    )

    assert result.valid is False
    assert "contradicts" in result.reason.lower()


def test_missing_hypothesis_fails_validation():
    plan = make_plan()
    plan.hypothesis = None

    result = ValidationWorker().execute(
        plan
    )

    assert result.valid is False
    assert "Hypothesis" in result.reason


def test_missing_success_criteria_fails_validation():
    plan = make_plan()
    plan.hypothesis.success_criteria = []

    result = ValidationWorker().execute(
        plan
    )

    assert result.valid is False
    assert "success criteria" in result.reason


def test_missing_failure_criteria_fails_validation():
    plan = make_plan()
    plan.hypothesis.failure_criteria = []

    result = ValidationWorker().execute(
        plan
    )

    assert result.valid is False
    assert "failure criteria" in result.reason


def test_missing_experiment_fails_validation():
    plan = make_plan()
    plan.experiment = None

    result = ValidationWorker().execute(
        plan
    )

    assert result.valid is False
    assert "Experiment" in result.reason


def test_missing_measurement_fails_validation():
    plan = make_plan()
    plan.experiment.measurements = []

    result = ValidationWorker().execute(
        plan
    )

    assert result.valid is False
    assert "Measurement" in result.reason


def test_missing_stop_condition_fails_validation():
    plan = make_plan()
    plan.experiment.stop_conditions = []

    result = ValidationWorker().execute(
        plan
    )

    assert result.valid is False
    assert "stop condition" in result.reason