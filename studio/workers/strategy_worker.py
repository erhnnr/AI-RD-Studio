from studio.workers.base import BaseWorker
from studio.core.worker_context import WorkerContext
from studio.core.models import Opportunity


class StrategyWorker(BaseWorker):
    """
    Strategic analysis worker.
    Converts signals into opportunities.
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
            "WorkerContext",
        ]

        self.output_types = [
            "Opportunity",
        ]

    def execute(self, context) -> Opportunity:

        if isinstance(context, WorkerContext):
            signal = context.signal

        else:
            signal = context

        title = signal.title.lower()

        if "ai" in title:
            impact = 9
            urgency = 8
            feasibility = 8
            strategic_fit = 10
        else:
            impact = 5
            urgency = 5
            feasibility = 5
            strategic_fit = 5

        return Opportunity(
            signal=signal,
            impact=impact,
            urgency=urgency,
            feasibility=feasibility,
            strategic_fit=strategic_fit,
        )