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

    Evidence-aware opportunities use evidence state as a gate.
    Opportunities without evidence metadata temporarily use the
    legacy score-based fallback.
    """

    def evaluate(
        self,
        opportunity: Opportunity,
    ) -> ReviewDecision:

        evidence_state = opportunity.evidence_state

        if evidence_state == "CONTRADICTORY":
            return ReviewDecision(
                decision="REJECT",
                reason=(
                    "Current evidence materially contradicts "
                    "progression."
                ),
                confidence=85,
                next_action="Do not allocate resources",
            )

        if evidence_state == "INSUFFICIENT":
            return ReviewDecision(
                decision="DEFER",
                reason=(
                    "Available evidence is insufficient "
                    "for progression."
                ),
                confidence=70,
                next_action="Collect more information",
            )

        if evidence_state == "MIXED":
            return ReviewDecision(
                decision="DEFER",
                reason=(
                    "Supporting and contradictory evidence "
                    "must be resolved before progression."
                ),
                confidence=65,
                next_action="Resolve conflicting evidence",
            )

        if evidence_state == "SUPPORTING":
            if opportunity.score >= 23:
                return ReviewDecision(
                    decision="ACCEPT",
                    reason=(
                        "Evidence supports progression and the "
                        "opportunity meets the current strategic "
                        "eligibility threshold."
                    ),
                    confidence=80,
                    next_action="Create research task",
                )

            return ReviewDecision(
                decision="DEFER",
                reason=(
                    "Evidence supports the opportunity, but current "
                    "strategic evaluation is not sufficient "
                    "for progression."
                ),
                confidence=65,
                next_action="Refine strategic evaluation",
            )

        # Temporary legacy compatibility path for Opportunity objects
        # that do not yet carry evidence metadata.
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