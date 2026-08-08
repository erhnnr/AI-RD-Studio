from studio.core.models import Signal
from studio.core.review_board import ReviewBoard
from studio.runtime.task_manager import TaskManager
from studio.knowledge.writer import KnowledgeWriter
from studio.workers.registry import WorkerRegistry
from studio.core.worker_context import WorkerContext


class StudioOrchestrator:
    """
    Coordinates Studio decision workflow.
    """

    def __init__(self):
        self.task_manager = TaskManager()
        self.knowledge_writer = KnowledgeWriter()
        self.worker_registry = WorkerRegistry()
        self.review_board = ReviewBoard()

    def execute(self, signal: Signal):

        # Contract based worker selection
        strategy_worker = (
            self.worker_registry.find_by_contract(
                capability="opportunity_scoring",
                input_type="Signal",
                output_type="Opportunity",
            )
        )

        # Backward compatibility fallback
        if strategy_worker is None:
            strategy_worker = self.worker_registry.get(
                "strategy"
            )

        context = WorkerContext(
            signal=signal
        )

        opportunity = strategy_worker.execute(
            context
        )

        decision = self.review_board.evaluate(
            opportunity
        )

        if decision.decision == "ACCEPT":

            task = self.task_manager.create_task(
                opportunity,
                decision.next_action,
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

        return self.knowledge_writer.write(
            title=f"Decision: {decision.decision}",
            content=content,
            tags=[
                "runtime",
                "decision",
            ],
        )