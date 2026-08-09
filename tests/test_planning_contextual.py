from studio.core.models import Opportunity, Signal
from studio.workers.planning_worker import PlanningWorker


def make_opportunity(
    title: str,
    evidence_state: str,
) -> Opportunity:
    return Opportunity(
        signal=Signal(
            title=title,
            description="Controlled planning signal.",
            source="test",
        ),
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
        evidence_state=evidence_state,
        evidence_confidence=0.8,
        rationale="Controlled planning evidence.",
    )


def test_planning_worker_produces_hypothesis_and_experiment():
    opportunity = make_opportunity(
        title="Industrial Water Efficiency System",
        evidence_state="SUPPORTING",
    )

    result = PlanningWorker().execute(
        opportunity
    )

    assert result.hypothesis is not None
    assert result.experiment is not None

    assert (
        "Industrial Water Efficiency System"
        in result.hypothesis.statement
    )

    assert len(result.hypothesis.success_criteria) > 0
    assert len(result.hypothesis.failure_criteria) > 0

    assert len(result.experiment.measurements) > 0
    assert len(result.experiment.stop_conditions) > 0


def test_planning_changes_method_for_different_evidence_states():
    supporting = make_opportunity(
        title="Industrial Efficiency System",
        evidence_state="SUPPORTING",
    )

    contradictory = make_opportunity(
        title="Industrial Efficiency System",
        evidence_state="CONTRADICTORY",
    )

    worker = PlanningWorker()

    supporting_plan = worker.execute(
        supporting
    )

    contradictory_plan = worker.execute(
        contradictory
    )

    assert (
        supporting_plan.experiment.method
        != contradictory_plan.experiment.method
    )

    assert (
        "prototype or controlled comparison"
        in supporting_plan.experiment.method
    )

    assert (
        "falsification-focused"
        in contradictory_plan.experiment.method
    )


def test_planning_changes_content_for_different_opportunities():
    water_opportunity = make_opportunity(
        title="Industrial Water Efficiency System",
        evidence_state="SUPPORTING",
    )

    education_opportunity = make_opportunity(
        title="Personal Learning Support System",
        evidence_state="SUPPORTING",
    )

    worker = PlanningWorker()

    water_plan = worker.execute(
        water_opportunity
    )

    education_plan = worker.execute(
        education_opportunity
    )

    assert (
        water_plan.hypothesis.statement
        != education_plan.hypothesis.statement
    )

    assert (
        water_plan.experiment.measurements[0].metric
        != education_plan.experiment.measurements[0].metric
    )

    assert water_plan.steps != education_plan.steps


def test_insufficient_evidence_plan_focuses_on_reducing_uncertainty():
    opportunity = make_opportunity(
        title="Controlled Opportunity",
        evidence_state="INSUFFICIENT",
    )

    plan = PlanningWorker().execute(
        opportunity
    )

    assert (
        "reducing the current uncertainty"
        in plan.experiment.method
    )


def test_experiment_is_capable_of_failure():
    opportunity = make_opportunity(
        title="Controlled Opportunity",
        evidence_state="SUPPORTING",
    )

    plan = PlanningWorker().execute(
        opportunity
    )

    assert len(plan.hypothesis.failure_criteria) > 0
    assert "fails" in plan.hypothesis.failure_criteria[0].lower()