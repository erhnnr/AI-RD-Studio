from studio.core.models import Signal, Opportunity


class SignalEvaluator:
    """
    Evaluates signals and converts them into opportunities.
    """

    def evaluate(self, signal: Signal) -> Opportunity:
        """
        Create an opportunity score from a signal.

        v0.1 uses manual deterministic scoring.
        """

        return Opportunity(
            signal=signal,
            impact=5,
            urgency=5,
            feasibility=5,
            strategic_fit=5,
        )


class SignalEngine:
    """
    Entry point for external signals.
    """

    def __init__(self):
        self.evaluator = SignalEvaluator()

    def process(self, signal: Signal) -> Opportunity:
        """
        Signal -> Opportunity pipeline.
        """

        return self.evaluator.evaluate(signal)