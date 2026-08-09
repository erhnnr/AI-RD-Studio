from studio.core.models import Signal
from studio.runtime.orchestrator import StudioOrchestrator
from studio.workers.lm_studio_research_provider import (
    LMStudioResearchProvider,
)


def main():

    provider = LMStudioResearchProvider(
        base_url="http://localhost:1234/v1",
        model="local-model",
        timeout=60,
    )

    orchestrator = StudioOrchestrator(
        research_provider=provider
    )

    signal = Signal(
        title="AI education opportunity",
        description=(
            "Personalized AI tutoring systems "
            "are becoming more capable."
        ),
        source="Manual Full Pipeline Smoke Test",
    )

    result = orchestrator.execute_with_trace(
        signal
    )

    print("=" * 60)
    print("AI-RD-STUDIO FULL PIPELINE SMOKE TEST")
    print("=" * 60)

    print("\nSIGNAL:")
    print(result.signal.title)

    print("\nRESEARCH:")
    print(result.research_result.analysis)

    print("\nOPPORTUNITY:")
    print(f"Impact: {result.opportunity.impact}")
    print(f"Urgency: {result.opportunity.urgency}")
    print(f"Feasibility: {result.opportunity.feasibility}")
    print(
        f"Strategic Fit: "
        f"{result.opportunity.strategic_fit}"
    )
    print(f"Score: {result.opportunity.score}")

    print("\nDECISION:")
    print(result.decision.decision)
    print(result.decision.reason)

    print("\nTASK:")
    if result.task is None:
        print("No task created.")
    else:
        print(result.task.objective)
        print(result.task.status)

    print("\nKNOWLEDGE:")
    print(result.knowledge.title)
    print(result.knowledge.content)

    print("\nRESULT:")
    print("FULL PIPELINE COMPLETED")

    print("=" * 60)


if __name__ == "__main__":
    main()