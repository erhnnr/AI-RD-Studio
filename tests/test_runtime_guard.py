import pytest

from studio.core.models import (
    Opportunity,
    ResearchResult,
    Signal,
)
from studio.runtime.runtime_guard import (
    RuntimeGuard,
    RuntimeValidationError,
)


def test_runtime_guard_accepts_valid_signal():

    signal = Signal(
        title="AI market signal",
        description="AI demand is increasing.",
        source="Market",
    )

    RuntimeGuard.validate_signal(signal)


def test_runtime_guard_rejects_missing_signal():

    with pytest.raises(
        RuntimeValidationError,
        match="Signal is required",
    ):
        RuntimeGuard.validate_signal(None)


def test_runtime_guard_rejects_missing_worker():

    with pytest.raises(
        RuntimeValidationError,
        match="No worker available",
    ):
        RuntimeGuard.require_worker(
            None,
            "research",
        )


def test_runtime_guard_rejects_invalid_research_output():

    with pytest.raises(
        RuntimeValidationError,
        match="Research worker must return ResearchResult",
    ):
        RuntimeGuard.validate_research_result(
            {"analysis": "invalid"}
        )


def test_runtime_guard_rejects_research_without_signal():

    result = ResearchResult(
        analysis="Research completed."
    )

    with pytest.raises(
        RuntimeValidationError,
        match="ResearchResult must contain a Signal",
    ):
        RuntimeGuard.validate_research_result(
            result
        )


def test_runtime_guard_accepts_valid_opportunity():

    signal = Signal(
        title="AI opportunity",
        description="AI infrastructure demand.",
        source="Market",
    )

    opportunity = Opportunity(
        signal=signal,
        impact=9,
        urgency=8,
        feasibility=8,
        strategic_fit=10,
    )

    RuntimeGuard.validate_opportunity(
        opportunity
    )