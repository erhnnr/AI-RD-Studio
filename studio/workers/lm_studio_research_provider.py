import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from studio.core.models import Signal
from studio.workers.research_provider import ResearchProvider


class ResearchProviderError(RuntimeError):
    """
    Raised when an external research provider fails.
    """

    pass


class LMStudioResearchProvider(ResearchProvider):
    """
    Research provider backed by an OpenAI-compatible
    LM Studio local server.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model: str = "local-model",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def research(self, signal: Signal) -> str:
        """
        Produce structured research analysis
        using the local LM Studio model.
        """

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are the ResearchWorker of an AI R&D Studio. "
                        "Analyze the supplied signal carefully. "
                        "Return a concise factual research analysis. "
                        "Do not make strategic decisions."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Signal title: {signal.title}\n"
                        f"Description: {signal.description}\n"
                        f"Source: {signal.source}"
                    ),
                },
            ],
            "temperature": 0.2,
        }

        request = Request(
            url=(
                f"{self.base_url}/chat/completions"
            ),
            data=json.dumps(payload).encode(
                "utf-8"
            ),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:

            with urlopen(
                request,
                timeout=self.timeout,
            ) as response:

                body = response.read().decode(
                    "utf-8"
                )

        except HTTPError as exc:

            raise ResearchProviderError(
                f"LM Studio HTTP error: "
                f"{exc.code}"
            ) from exc

        except URLError as exc:

            raise ResearchProviderError(
                "LM Studio is unavailable."
            ) from exc

        except TimeoutError as exc:

            raise ResearchProviderError(
                "LM Studio request timed out."
            ) from exc

        try:

            data = json.loads(body)

            analysis = (
                data["choices"][0]
                ["message"]["content"]
            )

        except (
            KeyError,
            IndexError,
            TypeError,
            json.JSONDecodeError,
        ) as exc:

            raise ResearchProviderError(
                "LM Studio returned an invalid response."
            ) from exc

        if not isinstance(analysis, str):
            raise ResearchProviderError(
                "LM Studio returned invalid analysis."
            )

        analysis = analysis.strip()

        if not analysis:
            raise ResearchProviderError(
                "LM Studio returned empty analysis."
            )

        return analysis