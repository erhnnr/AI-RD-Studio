import io
import json

import pytest

from studio.core.models import Signal
from studio.workers import lm_studio_research_provider
from studio.workers.lm_studio_research_provider import (
    LMStudioResearchProvider,
    ResearchProviderError,
)


class FakeHTTPResponse:

    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return False

    def read(self):
        return json.dumps(
            self.payload
        ).encode("utf-8")


def create_signal():

    return Signal(
        title="AI infrastructure opportunity",
        description=(
            "Demand for AI infrastructure "
            "is increasing."
        ),
        source="Market",
    )


def test_lm_studio_provider_returns_analysis(
    monkeypatch,
):

    response = {
        "choices": [
            {
                "message": {
                    "content": (
                        "AI infrastructure demand "
                        "shows strong growth."
                    )
                }
            }
        ]
    }

    def fake_urlopen(
        request,
        timeout,
    ):
        return FakeHTTPResponse(
            response
        )

    monkeypatch.setattr(
        lm_studio_research_provider,
        "urlopen",
        fake_urlopen,
    )

    provider = LMStudioResearchProvider(
        model="test-model"
    )

    result = provider.research(
        create_signal()
    )

    assert result == (
        "AI infrastructure demand "
        "shows strong growth."
    )


def test_lm_studio_provider_rejects_invalid_response(
    monkeypatch,
):

    def fake_urlopen(
        request,
        timeout,
    ):
        return FakeHTTPResponse(
            {"invalid": True}
        )

    monkeypatch.setattr(
        lm_studio_research_provider,
        "urlopen",
        fake_urlopen,
    )

    provider = LMStudioResearchProvider(
        model="test-model"
    )

    with pytest.raises(
        ResearchProviderError,
        match="invalid response",
    ):
        provider.research(
            create_signal()
        )


def test_lm_studio_provider_rejects_empty_analysis(
    monkeypatch,
):

    response = {
        "choices": [
            {
                "message": {
                    "content": "   "
                }
            }
        ]
    }

    def fake_urlopen(
        request,
        timeout,
    ):
        return FakeHTTPResponse(
            response
        )

    monkeypatch.setattr(
        lm_studio_research_provider,
        "urlopen",
        fake_urlopen,
    )

    provider = LMStudioResearchProvider(
        model="test-model"
    )

    with pytest.raises(
        ResearchProviderError,
        match="empty analysis",
    ):
        provider.research(
            create_signal()
        )