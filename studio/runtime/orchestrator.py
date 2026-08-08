from studio.core.models import PipelineResult, Signal
from studio.core.project_context import ProjectContext
from studio.core.review_board import ReviewBoard
from studio.runtime.runtime_guard import RuntimeGuard
from studio.runtime.task_manager import TaskManager
from studio.knowledge.writer import KnowledgeWriter
from studio.workers.registry import WorkerRegistry
from studio.core.worker_context import WorkerContext


class StudioOrchestrator:
    """
    Coordinates the Studio research and decision workflow.
    """

    def __init__(self):
        self.task_manager = TaskManager()
        self.knowledge_writer = KnowledgeWriter()
        self.worker_registry = WorkerRegistry()
        self.review_board = ReviewBoard()

    def _run_pipeline(self, signal: Signal):
        """
        Run the complete Studio pipeline and return all intermediate results.
        """

        RuntimeGuard.validate_signal(signal)

        # -------------------------------------------------
        # 1. Research
        # -------------------------------------------------

        research_worker = (
            self.worker_registry.find_by_contract(
                capability="research",
                input_type="Signal",
                output_type="ResearchResult",
            )
        )

        if research_worker is None:
            research_worker = self.worker_registry.get(
                "research"
            )

        RuntimeGuard.require_worker(
            research_worker,
            "research",
        )

        research_context = WorkerContext(
            signal=signal
        )

        research_result = research_worker.execute(
            research_context
        )

        RuntimeGuard.validate_research_result(
            research_result
        )

        # -------------------------------------------------
        # 2. Strategy
        # -------------------------------------------------

        strategy_worker = (
            self.worker_registry.find_by_contract(
                capability="opportunity_scoring",
                input_type="ResearchResult",
                output_type="Opportunity",
            )
        )

        if strategy_worker is None:
            strategy_worker = self.worker_registry.get(
                "strategy"
            )

        RuntimeGuard.require_worker(
            strategy_worker,
            "opportunity_scoring",
        )

        opportunity = strategy_worker.execute(
            research_result
        )

        RuntimeGuard.validate_opportunity(
            opportunity
        )

        # -------------------------------------------------
        # 3. Review
        # -------------------------------------------------

        decision = self.review_board.evaluate(
            opportunity
        )

        RuntimeGuard.validate_decision(
            decision
        )

        # -------------------------------------------------
        # 4. Task
        # -------------------------------------------------

        task = None

        if decision.decision == "ACCEPT":

            task = self.task_manager.create_task(
                opportunity,
                decision.next_action,
            )

            RuntimeGuard.validate_task(
                task
            )

            content = (
                f"Accepted opportunity: "
                f"{task.opportunity.signal.title}\n"
                f"Reason: {decision.reason}"
            )

        else:

            content = (
                f"Decision: {decision.decision}\n"
                f"Reason: {decision.reason}\n"
                f"Next action: {decision.next_action}"
            )

        # -------------------------------------------------
        # 5. Knowledge
        # -------------------------------------------------

        knowledge = self.knowledge_writer.write(
            title=f"Decision: {decision.decision}",
            content=content,
            tags=[
                "runtime",
                "decision",
            ],
        )

        RuntimeGuard.validate_knowledge(
            knowledge
        )

        return (
            research_result,
            opportunity,
            decision,
            task,
            knowledge,
        )

    def execute(self, signal: Signal):
        """
        Execute the Studio pipeline and return the final knowledge record.
        """

        (
            research_result,
            opportunity,
            decision,
            task,
            knowledge,
        ) = self._run_pipeline(signal)

        return knowledge

    def execute_with_trace(
        self,
        signal: Signal,
    ) -> PipelineResult:
        """
        Execute the Studio pipeline and return the complete runtime trace.
        """

        (
            research_result,
            opportunity,
            decision,
            task,
            knowledge,
        ) = self._run_pipeline(signal)

        return PipelineResult(
            signal=signal,
            research_result=research_result,
            opportunity=opportunity,
            decision=decision,
            task=task,
            knowledge=knowledge,
        )

    def execute_project(
        self,
        context: ProjectContext,
    ):
        """
        Execute all signals belonging to a project.

        Each signal runs through the existing validated
        Studio pipeline and produces a PipelineResult.
        """

        results = []

        for signal in context.signals:

            result = self.execute_with_trace(
                signal
            )

            results.append(result)

        return results