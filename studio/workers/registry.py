from studio.workers.strategy_worker import StrategyWorker
from studio.workers.research_worker import ResearchWorker
from studio.workers.planning_worker import PlanningWorker
from studio.workers.validation_worker import ValidationWorker


class WorkerRegistry:
    """
    Registry for Studio workers.
    """

    def __init__(
        self,
        research_provider=None,
    ):
        self.workers = {
            "strategy": StrategyWorker(),
            "research": ResearchWorker(
                provider=research_provider
            ),
            "planning": PlanningWorker(),
            "validation": ValidationWorker(),
        }

    def get(self, worker_name: str):
        """
        Return worker by registry name.
        """
        return self.workers.get(worker_name)

    def find_by_capability(self, capability: str):
        """
        Find worker matching a capability.
        """

        for worker in self.workers.values():

            if worker is None:
                continue

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

            if worker is None:
                continue

            if not worker.has_capability(capability):
                continue

            if input_type not in worker.input_types:
                continue

            if output_type not in worker.output_types:
                continue

            return worker

        return None