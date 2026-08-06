from abc import ABC, abstractmethod


class BaseWorker(ABC):
    """
    Base interface for all AI workers.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, task):
        """
        Execute assigned task.
        """
        pass