from abc import ABC, abstractmethod

from studio.core.models import Signal


class ResearchProvider(ABC):
    """
    Contract for external or local research providers.
    """

    @abstractmethod
    def research(self, signal: Signal) -> str:
        """
        Produce research analysis for a signal.
        """
        pass