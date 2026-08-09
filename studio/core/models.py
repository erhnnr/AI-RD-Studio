from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from studio.core.evidence import Claim


@dataclass
class Signal:
    title: str
    description: str
    source: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Opportunity:
    signal: Signal
    impact: int
    urgency: int
    feasibility: int
    strategic_fit: int
    evidence_state: Optional[str] = None
    evidence_confidence: Optional[float] = None
    rationale: Optional[str] = None

    @property
    def score(self) -> int:
        return (
            self.impact
            + self.urgency
            + self.feasibility
            + self.strategic_fit
        )


@dataclass
class ResearchTask:
    opportunity: Opportunity
    objective: str
    status: str = "NEW"


@dataclass
class ResearchResult:
    analysis: str
    worker: str = "ResearchWorker"
    signal: Optional[Signal] = None
    project_name: Optional[str] = None
    claims: List[Claim] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not isinstance(self.claims, list):
            raise TypeError("ResearchResult.claims must be a list.")

        for claim in self.claims:
            if not isinstance(claim, Claim):
                raise TypeError(
                    "ResearchResult.claims must contain Claim objects."
                )


@dataclass
class PlanningResult:
    opportunity: Opportunity
    objective: str
    steps: List[str] = field(default_factory=list)
    worker: str = "PlanningWorker"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ValidationResult:
    planning_result: PlanningResult
    valid: bool
    reason: str
    worker: str = "ValidationWorker"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class KnowledgeRecord:
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DecisionRecord:
    decision: str
    reason: str
    confidence: int
    next_action: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PipelineResult:
    signal: Signal
    research_result: ResearchResult
    opportunity: Opportunity
    decision: object
    task: Optional[ResearchTask]
    knowledge: KnowledgeRecord
    planning_result: Optional[PlanningResult] = None
    validation_result: Optional[ValidationResult] = None
    created_at: datetime = field(default_factory=datetime.now)