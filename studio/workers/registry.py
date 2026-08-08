from studio.workers.strategy_worker import StrategyWorker
from studio.workers.research_worker import ResearchWorker


class WorkerRegistry:
    """
    Stores available Studio workers.
    """

    def __init__(self):
        self.workers = {
            "strategy": StrategyWorker(),
            "research": ResearchWorker(),
        }

    def get(self, worker_name: str):
        return self.workers.get(worker_name)

    def find_by_capability(self, capability: str):
        """
        Find first worker that supports capability.
        """

        for worker in self.workers.values():

            if worker.has_capability(capability):
                return worker

        return None

    def find_by_contract(
        self,
        capability: str,
        input_type: str,
        output_type: str,
    ):
        """
        Find worker matching capability,
        input type and output type.
        """

        for worker in self.workers.values():

            if not worker.has_capability(capability):
                continue

            if input_type not in worker.input_types:
                continue

            if output_type not in worker.output_types:
                continue

            return worker

        return None