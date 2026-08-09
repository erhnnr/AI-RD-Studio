from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Signal:
    """
    External world observation.
    """

    title: str
    description: str
    source: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Opportunity:
    """
    Evaluated signal that may create value.
    """

    signal: Signal
    impact: int
    urgency: int
    feasibility: int
    strategic_fit: int

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
    """
    Task generated from an opportunity.
    """

    opportunity: Opportunity
    objective: str
    status: str = "NEW"


@dataclass
class ResearchResult:
    """
    Structured result produced by a research worker.
    """

    analysis: str
    worker: str = "ResearchWorker"
    signal: Optional[Signal] = None
    project_name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PlanningResult:
    """
    Structured execution plan produced from an opportunity.
    """

    opportunity: Opportunity
    objective: str
    steps: List[str] = field(default_factory=list)
    worker: str = "PlanningWorker"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class KnowledgeRecord:
    """
    Permanent Studio memory entry.
    """

    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DecisionRecord:
    """
    Permanent record of strategic decisions.
    """

    decision: str
    reason: str
    confidence: int
    next_action: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PipelineResult:
    """
    Complete trace of a Studio runtime pipeline execution.
    """

    signal: Signal
    research_result: ResearchResult
    opportunity: Opportunity
    decision: object
    task: Optional[ResearchTask]
    knowledge: KnowledgeRecord
    created_at: datetime = field(default_factory=datetime.now)