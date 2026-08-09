from studio.core.evidence import EvidenceAssessmentState
from studio.core.evidence_assessment import assess_research_evidence
from studio.core.models import Opportunity, ResearchResult
from studio.core.worker_context import WorkerContext
from studio.workers.base import BaseWorker


class StrategyWorker(BaseWorker):
    """
    Strategic analysis worker.
    Converts signals and research results into opportunities.
    """

    def __init__(self):
        super().__init__("StrategyWorker")

        self.capabilities = [
            "signal_analysis",
            "opportunity_scoring",
            "strategy_creation",
        ]

        self.input_types = [
            "Signal",
            "ResearchResult",
            "WorkerContext",
        ]

        self.output_types = [
            "Opportunity",
        ]

    def _neutral_scores(self) -> tuple[int, int, int, int]:
        return 5, 5, 5, 5

    def _scores_from_research(
        self,
        research_result: ResearchResult,
    ) -> tuple[int, int, int, int]:
        assessment = assess_research_evidence(
            research_result
        )

        impact, urgency, feasibility, strategic_fit = (
            self._neutral_scores()
        )

        if assessment.state == EvidenceAssessmentState.SUPPORTING:
            impact += 1
            feasibility += 1
            strategic_fit += 1

        elif assessment.state == EvidenceAssessmentState.CONTRADICTORY:
            impact -= 1
            feasibility -= 1
            strategic_fit -= 1

        return (
            impact,
            urgency,
            feasibility,
            strategic_fit,
        )

    def execute(self, context) -> Opportunity:

        research_result = None

        if isinstance(context, WorkerContext):
            if context.research_result is not None:
                research_result = context.research_result
                signal = research_result.signal
            else:
                signal = context.signal

        elif isinstance(context, ResearchResult):
            research_result = context
            signal = context.signal

        else:
            signal = context

        if signal is None:
            raise ValueError(
                "StrategyWorker requires a Signal "
                "or ResearchResult containing a Signal."
            )

        if research_result is not None:
            (
                impact,
                urgency,
                feasibility,
                strategic_fit,
            ) = self._scores_from_research(
                research_result
            )
        else:
            (
                impact,
                urgency,
                feasibility,
                strategic_fit,
            ) = self._neutral_scores()

        return Opportunity(
            signal=signal,
            impact=impact,
            urgency=urgency,
            feasibility=feasibility,
            strategic_fit=strategic_fit,
        )