from studio.core.models import Opportunity


class ReviewDecision:
    """
    Result of opportunity evaluation.
    """

    def __init__(
        self,
        decision: str,
        reason: str,
        confidence: int,
        next_action: str,
    ):
        self.decision = decision
        self.reason = reason
        self.confidence = confidence
        self.next_action = next_action


class ReviewBoard:
    """
    Evaluates opportunities before execution.
    """

    def evaluate(
        self,
        opportunity: Opportunity,
    ) -> ReviewDecision:

        if opportunity.score >= 30:
            return ReviewDecision(
                decision="ACCEPT",
                reason="High strategic value",
                confidence=90,
                next_action="Create research task",
            )

        if opportunity.score >= 15:
            return ReviewDecision(
                decision="DEFER",
                reason="Needs more validation",
                confidence=70,
                next_action="Collect more information",
            )

        return ReviewDecision(
            decision="REJECT",
            reason="Insufficient strategic value",
            confidence=85,
            next_action="Do not allocate resources",
        )