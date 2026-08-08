from studio.core.models import (
    Opportunity,
    ResearchResult,
    Signal,
)


class RuntimeValidationError(ValueError):
    """
    Raised when runtime pipeline data violates
    a required Studio contract.
    """

    pass


class RuntimeGuard:
    """
    Validates critical runtime pipeline inputs and outputs.
    """

    @staticmethod
    def validate_signal(signal: Signal) -> None:

        if signal is None:
            raise RuntimeValidationError(
                "Signal is required."
            )

        if not isinstance(signal, Signal):
            raise RuntimeValidationError(
                "Runtime input must be a Signal."
            )

        if not signal.title:
            raise RuntimeValidationError(
                "Signal title is required."
            )

    @staticmethod
    def require_worker(worker, capability: str) -> None:

        if worker is None:
            raise RuntimeValidationError(
                f"No worker available for capability: "
                f"{capability}"
            )

    @staticmethod
    def validate_research_result(
        result: ResearchResult,
    ) -> None:

        if not isinstance(result, ResearchResult):
            raise RuntimeValidationError(
                "Research worker must return ResearchResult."
            )

        if result.signal is None:
            raise RuntimeValidationError(
                "ResearchResult must contain a Signal."
            )

    @staticmethod
    def validate_opportunity(
        opportunity: Opportunity,
    ) -> None:

        if not isinstance(opportunity, Opportunity):
            raise RuntimeValidationError(
                "Strategy worker must return Opportunity."
            )

        if opportunity.signal is None:
            raise RuntimeValidationError(
                "Opportunity must contain a Signal."
            )