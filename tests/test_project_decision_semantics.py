from types import SimpleNamespace

from studio.core.models import (
    KnowledgeRecord,
    Opportunity,
    PipelineResult,
    ResearchResult,
    Signal,
)
from studio.core.project import Project
from studio.core.project_execution_result import ProjectExecutionResult


def make_pipeline_result(
    decision_value: str,
) -> PipelineResult:
    signal = Signal(
        title=f"{decision_value} opportunity",
        description="Controlled decision semantics test.",
        source="test",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=5,
        urgency=5,
        feasibility=5,
        strategic_fit=5,
    )

    decision = SimpleNamespace(
        decision=decision_value,
        reason="Controlled decision.",
        next_action="Controlled next action.",
    )

    return PipelineResult(
        signal=signal,
        research_result=ResearchResult(
            analysis="Controlled research.",
            signal=signal,
        ),
        opportunity=opportunity,
        decision=decision,
        task=None,
        knowledge=KnowledgeRecord(
            title=f"Decision: {decision_value}",
            content="Controlled knowledge record.",
        ),
    )


def test_project_execution_distinguishes_accept_defer_and_reject():
    project = Project(
        name="Decision Semantics Project",
        objective="Validate decision semantics.",
        priority="HIGH",
    )

    execution = ProjectExecutionResult(
        project=project,
        results=[
            make_pipeline_result("ACCEPT"),
            make_pipeline_result("DEFER"),
            make_pipeline_result("REJECT"),
        ],
    )

    assert execution.total_results == 3
    assert execution.accepted_count == 1
    assert execution.deferred_count == 1
    assert execution.rejected_count == 1


def test_defer_is_not_counted_as_reject():
    project = Project(
        name="Deferred Project",
        objective="Validate DEFER semantics.",
        priority="MEDIUM",
    )

    execution = ProjectExecutionResult(
        project=project,
        results=[
            make_pipeline_result("DEFER"),
        ],
    )

    assert execution.accepted_count == 0
    assert execution.deferred_count == 1
    assert execution.rejected_count == 0


def test_reject_is_not_counted_as_defer():
    project = Project(
        name="Rejected Project",
        objective="Validate REJECT semantics.",
        priority="LOW",
    )

    execution = ProjectExecutionResult(
        project=project,
        results=[
            make_pipeline_result("REJECT"),
        ],
    )

    assert execution.accepted_count == 0
    assert execution.deferred_count == 0
    assert execution.rejected_count == 1


def test_empty_project_has_zero_decision_counts():
    project = Project(
        name="Empty Project",
        objective="Validate empty semantics.",
        priority="LOW",
    )

    execution = ProjectExecutionResult(
        project=project,
    )

    assert execution.total_results == 0
    assert execution.accepted_count == 0
    assert execution.deferred_count == 0
    assert execution.rejected_count == 0
    assert execution.status == "NO_SIGNALS"