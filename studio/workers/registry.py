from studio.workers.strategy import StrategyWorker


class WorkerRegistry:
    """
    Stores available Studio workers.
    """

    def __init__(self):
        self.workers = {
            "strategy": StrategyWorker()
        }

    def get(self, worker_name: str):
        return self.workers.get(worker_name)