from studio.core.models import Signal
from studio.runtime.task_manager import TaskManager
from studio.knowledge.writer import KnowledgeWriter
from studio.workers.registry import WorkerRegistry


class StudioOrchestrator:
    """
    Coordinates Studio runtime workflow.
    """

    def __init__(self):
        self.task_manager = TaskManager()
        self.knowledge_writer = KnowledgeWriter()
        self.worker_registry = WorkerRegistry()

    def execute(self, signal: Signal):

        strategy_worker = self.worker_registry.get("strategy")

        opportunity = strategy_worker.execute(signal)

        task = self.task_manager.create_task(
            opportunity,
            "Research opportunity",
        )

        record = self.knowledge_writer.write(
            title="Research opportunity",
            content=(
                f"Created task for: "
                f"{task.opportunity.signal.title}"
            ),
            tags=[
                "runtime",
                "strategy",
            ],
        )

        return record