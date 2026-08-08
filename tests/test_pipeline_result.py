from studio.core.models import (
    DecisionRecord,
    KnowledgeRecord,
    Opportunity,
    PipelineResult,
    ResearchResult,
    ResearchTask,
    Signal,
)


def test_pipeline_result_preserves_runtime_trace():

    signal = Signal(
        title="AI infrastructure opportunity",
        description="Infrastructure demand is increasing.",
        source="Market Signal",
    )

    research_result = ResearchResult(
        analysis="Growth potential detected.",
        signal=signal,
    )

    opportunity = Opportunity(
        signal=signal,
        impact=9,
        urgency=8,
        feasibility=8,
        strategic_fit=10,
    )

    decision = DecisionRecord(
        decision="ACCEPT",
        reason="High strategic value.",
        confidence=90,
        next_action="Create research task.",
    )

    task = ResearchTask(
        opportunity=opportunity,
        objective=decision.next_action,
    )

    knowledge = KnowledgeRecord(
        title="Decision: ACCEPT",
        content="Opportunity accepted.",
        tags=["runtime", "decision"],
    )

    result = PipelineResult(
        signal=signal,
        research_result=research_result,
        opportunity=opportunity,
        decision=decision,
        task=task,
        knowledge=knowledge,
    )

    assert result.signal is signal
    assert result.research_result is research_result
    assert result.opportunity is opportunity
    assert result.decision is decision
    assert result.task is task
    assert result.knowledge is knowledge
    assert result.created_at is not None