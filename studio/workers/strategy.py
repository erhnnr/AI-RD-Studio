from studio.workers.base import BaseWorker
from studio.core.models import Signal, Opportunity


class StrategyWorker(BaseWorker):
    """
    Evaluates signals and creates opportunities.
    """

    def __init__(self):
        super().__init__("StrategyWorker")

    def execute(self, signal: Signal) -> Opportunity:
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