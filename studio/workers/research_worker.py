from typing import Optional

from studio.core.evidence import Claim, Evidence, EvidenceSource
from studio.core.models import ResearchResult
from studio.core.project import Project
from studio.core.worker_context import WorkerContext
from studio.workers.base import BaseWorker
from studio.workers.research_provider import ResearchProvider


class ResearchWorker(BaseWorker):
    """
    Worker responsible for project and signal research.
    """

    def __init__(
        self,
        provider: Optional[ResearchProvider] = None,
    ):
        super().__init__("ResearchWorker")

        self.provider = provider

        self.capabilities = [
            "research",
            "information_analysis",
            "knowledge_generation",
        ]

        self.input_types = [
            "Signal",
            "WorkerContext",
            "Project",
        ]

        self.output_types = [
            "ResearchResult",
        ]

    def _build_signal_claims(self, signal) -> list[Claim]:
        """
        Build a minimal structured claim from the input Signal.

        The Signal itself is treated as unverified input evidence.
        This does not imply independent verification.
        """

        source = EvidenceSource(
            name=signal.source,
            source_type="signal_input",
            reference=None,
            metadata="Original source declared by the input Signal.",
        )

        evidence = Evidence(
            content=signal.description,
            source=source,
            confidence=0.3,
            provenance_note=(
                "Derived directly from the input Signal. "
                "Not independently verified."
            ),
        )

        claim = Claim(
            statement=signal.title,
            supporting_evidence=[evidence],
            counter_evidence=[],
            confidence=0.3,
            uncertainty=(
                "The claim is based only on the original Signal "
                "and has not yet been independently verified."
            ),
        )

        return [claim]

    def execute(self, context) -> ResearchResult:

        if isinstance(context, WorkerContext):

            signal = context.signal

            if self.provider is not None:
                analysis = self.provider.research(signal)
            else:
                analysis = (
                    f"Research analysis prepared for "
                    f"{signal.title}"
                )

            return ResearchResult(
                worker=self.name,
                signal=signal,
                analysis=analysis,
                claims=self._build_signal_claims(signal),
            )

        if isinstance(context, Project):

            return ResearchResult(
                worker=self.name,
                project_name=context.name,
                analysis=(
                    f"Research analysis prepared for "
                    f"{context.name}"
                ),
            )

        return ResearchResult(
            worker=self.name,
            analysis="Research analysis prepared.",
        )