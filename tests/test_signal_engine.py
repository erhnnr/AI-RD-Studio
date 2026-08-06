from studio.core.models import Signal
from studio.runtime.signal_engine import SignalEngine


def test_signal_creates_opportunity():
    signal = Signal(
        title="AI education market growth",
        description="Increasing demand for personalized AI learning systems",
        source="market_research",
    )

    engine = SignalEngine()

    opportunity = engine.process(signal)

    assert opportunity.signal == signal
    assert opportunity.score == 20