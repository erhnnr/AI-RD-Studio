from studio.core.models import Signal
from studio.runtime.signal_engine import SignalEngine
from studio.runtime.task_manager import TaskManager
from studio.knowledge.writer import KnowledgeWriter


class StudioOrchestrator:
    """
    Coordinates Studio runtime workflow.
    """

    def __init__(self):
        self.signal_engine = SignalEngine()
        self.task_manager = TaskManager()
        self.knowledge_writer = KnowledgeWriter()

    def execute(self, signal: Signal):
        opportunity = self.signal_engine.process(signal)

        task = self.task_manager.create_task(
            opportunity,
            "Research opportunity",
        )

        record = self.knowledge_writer.write(
            title=task.objective,
            content=signal.description,
            tags=["runtime"],
        )

        return record