from studio.core.models import DecisionRecord


class DecisionMemory:
    """
    Stores strategic decisions.
    """

    def __init__(self):
        self.records = []

    def store(
        self,
        decision,
        reason,
        confidence,
        next_action,
    ) -> DecisionRecord:

        record = DecisionRecord(
            decision=decision,
            reason=reason,
            confidence=confidence,
            next_action=next_action,
        )

        self.records.append(record)

        return record

    def all(self):
        return self.records