from abc import ABC, abstractmethod


class BaseWorker(ABC):
    """
    Base interface for all AI workers.
    """

    def __init__(self, name: str):
        self.name = name
        self.capabilities = []
        self.input_types = []
        self.output_types = []

    def add_capability(self, capability: str):
        """
        Add a capability to the worker.
        """

        self.capabilities.append(capability)

    def has_capability(self, capability: str) -> bool:
        """
        Check whether worker has a capability.
        """

        return capability in self.capabilities

    def get_metadata(self) -> dict:
        """
        Return worker identity and contract information.
        """

        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "input_types": self.input_types,
            "output_types": self.output_types,
        }

    @abstractmethod
    def execute(self, task):
        """
        Execute assigned task.
        """
        pass