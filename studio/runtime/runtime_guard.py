from studio.core.evidence import Claim, Evidence, EvidenceSource
from studio.core.models import (
    KnowledgeRecord,
    Opportunity,
    PlanningResult,
    ResearchResult,
    ResearchTask,
    Signal,
    ValidationResult,
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

        if not isinstance(result.claims, list):
            raise RuntimeValidationError(
                "ResearchResult.claims must be a list."
            )

        for claim in result.claims:
            RuntimeGuard._validate_claim(claim)

    @staticmethod
    def _validate_claim(claim: Claim) -> None:

        if not isinstance(claim, Claim):
            raise RuntimeValidationError(
                "ResearchResult.claims must contain Claim objects."
            )

        if not claim.statement:
            raise RuntimeValidationError(
                "Claim must contain a statement."
            )

        if not 0.0 <= claim.confidence <= 1.0:
            raise RuntimeValidationError(
                "Claim confidence must be between 0.0 and 1.0."
            )

        if not isinstance(claim.supporting_evidence, list):
            raise RuntimeValidationError(
                "Claim.supporting_evidence must be a list."
            )

        if not isinstance(claim.counter_evidence, list):
            raise RuntimeValidationError(
                "Claim.counter_evidence must be a list."
            )

        for evidence in claim.supporting_evidence:
            RuntimeGuard._validate_evidence(evidence)

        for evidence in claim.counter_evidence:
            RuntimeGuard._validate_evidence(evidence)

    @staticmethod
    def _validate_evidence(evidence: Evidence) -> None:

        if not isinstance(evidence, Evidence):
            raise RuntimeValidationError(
                "Claim evidence entries must be Evidence objects."
            )

        if not evidence.content:
            raise RuntimeValidationError(
                "Evidence must contain content."
            )

        if not isinstance(evidence.source, EvidenceSource):
            raise RuntimeValidationError(
                "Evidence must contain an EvidenceSource."
            )

        if not evidence.source.name:
            raise RuntimeValidationError(
                "EvidenceSource must contain a name."
            )

        if not evidence.source.source_type:
            raise RuntimeValidationError(
                "EvidenceSource must contain a source_type."
            )

        if not 0.0 <= evidence.confidence <= 1.0:
            raise RuntimeValidationError(
                "Evidence confidence must be between 0.0 and 1.0."
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

    @staticmethod
    def validate_planning_result(
        result: PlanningResult,
    ) -> None:

        if not isinstance(result, PlanningResult):
            raise RuntimeValidationError(
                "Planning worker must return PlanningResult."
            )

        if result.opportunity is None:
            raise RuntimeValidationError(
                "PlanningResult must contain an Opportunity."
            )

    @staticmethod
    def validate_validation_result(
        result: ValidationResult,
    ) -> None:

        if not isinstance(result, ValidationResult):
            raise RuntimeValidationError(
                "Validation worker must return ValidationResult."
            )

        if result.planning_result is None:
            raise RuntimeValidationError(
                "ValidationResult must contain PlanningResult."
            )

    @staticmethod
    def validate_decision(decision) -> None:

        if decision is None:
            raise RuntimeValidationError(
                "ReviewBoard must return a decision."
            )

        required_attributes = (
            "decision",
            "reason",
            "next_action",
        )

        for attribute in required_attributes:

            if not hasattr(decision, attribute):
                raise RuntimeValidationError(
                    "ReviewBoard must return a valid decision object."
                )

        if not decision.decision:
            raise RuntimeValidationError(
                "Decision must contain a decision value."
            )

    @staticmethod
    def validate_task(
        task: ResearchTask,
    ) -> None:

        if not isinstance(task, ResearchTask):
            raise RuntimeValidationError(
                "TaskManager must return ResearchTask."
            )

        if task.opportunity is None:
            raise RuntimeValidationError(
                "ResearchTask must contain an Opportunity."
            )

    @staticmethod
    def validate_knowledge(
        knowledge: KnowledgeRecord,
    ) -> None:

        if not isinstance(knowledge, KnowledgeRecord):
            raise RuntimeValidationError(
                "KnowledgeWriter must return KnowledgeRecord."
            )

        if not knowledge.title:
            raise RuntimeValidationError(
                "KnowledgeRecord must contain a title."
            )