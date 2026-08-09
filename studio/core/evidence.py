from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


def _validate_confidence(value: float, field_name: str) -> None:
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"{field_name} must be a number between 0.0 and 1.0."
        )

    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(
            f"{field_name} must be between 0.0 and 1.0."
        )


@dataclass
class EvidenceSource:
    name: str
    source_type: str
    reference: Optional[str] = None
    metadata: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError(
                "EvidenceSource.name must be a non-empty string."
            )

        if (
            not isinstance(self.source_type, str)
            or not self.source_type.strip()
        ):
            raise ValueError(
                "EvidenceSource.source_type must be a non-empty string."
            )

        if self.reference is not None and not isinstance(
            self.reference,
            str,
        ):
            raise TypeError(
                "EvidenceSource.reference must be a string or None."
            )

        if self.metadata is not None and not isinstance(
            self.metadata,
            str,
        ):
            raise TypeError(
                "EvidenceSource.metadata must be a string or None."
            )


@dataclass
class Evidence:
    content: str
    source: EvidenceSource
    confidence: float = 0.5
    provenance_note: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError(
                "Evidence.content must be a non-empty string."
            )

        if not isinstance(self.source, EvidenceSource):
            raise TypeError(
                "Evidence.source must be an EvidenceSource."
            )

        _validate_confidence(
            self.confidence,
            "Evidence.confidence",
        )

        self.confidence = float(self.confidence)

        if self.provenance_note is not None and not isinstance(
            self.provenance_note,
            str,
        ):
            raise TypeError(
                "Evidence.provenance_note must be a string or None."
            )


@dataclass
class Claim:
    statement: str
    supporting_evidence: List[Evidence] = field(default_factory=list)
    counter_evidence: List[Evidence] = field(default_factory=list)
    confidence: float = 0.5
    uncertainty: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.statement, str) or not self.statement.strip():
            raise ValueError(
                "Claim.statement must be a non-empty string."
            )

        if not isinstance(self.supporting_evidence, list):
            raise TypeError(
                "Claim.supporting_evidence must be a list."
            )

        if not isinstance(self.counter_evidence, list):
            raise TypeError(
                "Claim.counter_evidence must be a list."
            )

        for evidence in self.supporting_evidence:
            if not isinstance(evidence, Evidence):
                raise TypeError(
                    "Claim.supporting_evidence must contain "
                    "Evidence objects."
                )

        for evidence in self.counter_evidence:
            if not isinstance(evidence, Evidence):
                raise TypeError(
                    "Claim.counter_evidence must contain "
                    "Evidence objects."
                )

        _validate_confidence(
            self.confidence,
            "Claim.confidence",
        )

        self.confidence = float(self.confidence)

        if self.uncertainty is not None and not isinstance(
            self.uncertainty,
            str,
        ):
            raise TypeError(
                "Claim.uncertainty must be a string or None."
            )


class EvidenceAssessmentState(str, Enum):
    SUPPORTING = "SUPPORTING"
    CONTRADICTORY = "CONTRADICTORY"
    MIXED = "MIXED"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass
class EvidenceAssessment:
    state: EvidenceAssessmentState
    supporting_strength: float
    counter_strength: float
    confidence: float
    rationale: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, EvidenceAssessmentState):
            raise TypeError(
                "EvidenceAssessment.state must be "
                "an EvidenceAssessmentState."
            )

        _validate_confidence(
            self.supporting_strength,
            "EvidenceAssessment.supporting_strength",
        )

        _validate_confidence(
            self.counter_strength,
            "EvidenceAssessment.counter_strength",
        )

        _validate_confidence(
            self.confidence,
            "EvidenceAssessment.confidence",
        )

        self.supporting_strength = float(
            self.supporting_strength
        )

        self.counter_strength = float(
            self.counter_strength
        )

        self.confidence = float(
            self.confidence
        )

        if not isinstance(self.rationale, str) or not self.rationale.strip():
            raise ValueError(
                "EvidenceAssessment.rationale must be "
                "a non-empty string."
            )