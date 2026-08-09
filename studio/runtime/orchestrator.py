from studio.core.models import PipelineResult, Signal
from studio.core.project_context import ProjectContext
from studio.core.project_execution_result import ProjectExecutionResult
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

    def __init__(
        self,
        research_provider=None,
    ):
        self.task_manager = TaskManager()
        self.knowledge_writer = KnowledgeWriter()

        self.worker_registry = WorkerRegistry(
            research_provider=research_provider
        )

        self.review_board = ReviewBoard()

    def _run_pipeline(self, signal: Signal):
        """
        Run the complete Studio multi-worker pipeline.
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

        research_result = research_worker.execute(
            WorkerContext(
                signal=signal
            )
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
        # 3. Planning
        # -------------------------------------------------

        planning_worker = (
            self.worker_registry.find_by_contract(
                capability="planning",
                input_type="Opportunity",
                output_type="PlanningResult",
            )
        )

        if planning_worker is None:
            planning_worker = self.worker_registry.get(
                "planning"
            )

        RuntimeGuard.require_worker(
            planning_worker,
            "planning",
        )

        planning_result = planning_worker.execute(
            opportunity
        )

        RuntimeGuard.validate_planning_result(
            planning_result
        )

        # -------------------------------------------------
        # 4. Validation
        # -------------------------------------------------

        validation_worker = (
            self.worker_registry.find_by_contract(
                capability="validation",
                input_type="PlanningResult",
                output_type="ValidationResult",
            )
        )

        if validation_worker is None:
            validation_worker = self.worker_registry.get(
                "validation"
            )

        RuntimeGuard.require_worker(
            validation_worker,
            "validation",
        )

        validation_result = validation_worker.execute(
            planning_result
        )

        RuntimeGuard.validate_validation_result(
            validation_result
        )

        # -------------------------------------------------
        # 5. Review
        # -------------------------------------------------

        decision = self.review_board.evaluate(
            opportunity
        )

        RuntimeGuard.validate_decision(
            decision
        )

        # -------------------------------------------------
        # 6. Task
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
        # 7. Knowledge
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
            planning_result,
            validation_result,
            decision,
            task,
            knowledge,
        )

    def execute(self, signal: Signal):
        """
        Execute the Studio pipeline and return
        the final knowledge record.
        """

        (
            research_result,
            opportunity,
            planning_result,
            validation_result,
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
        Execute the Studio pipeline and return
        the complete runtime trace.
        """

        (
            research_result,
            opportunity,
            planning_result,
            validation_result,
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
            planning_result=planning_result,
            validation_result=validation_result,
        )

    def execute_project(
        self,
        context: ProjectContext,
    ) -> ProjectExecutionResult:
        """
        Execute all signals belonging to a project.
        """

        results = []

        for signal in context.signals:

            result = self.execute_with_trace(
                signal
            )

            results.append(result)

        return ProjectExecutionResult(
            project=context.project,
            results=results,
        )