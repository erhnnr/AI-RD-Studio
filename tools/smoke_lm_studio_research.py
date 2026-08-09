from studio.core.models import Signal
from studio.workers.lm_studio_research_provider import (
    LMStudioResearchProvider,
)


def main():

    signal = Signal(
        title="AI education opportunity",
        description=(
            "Personalized AI tutoring systems "
            "are becoming more capable."
        ),
        source="Manual Smoke Test",
    )

    provider = LMStudioResearchProvider(
        base_url="http://localhost:1234/v1",
        model="local-model",
        timeout=60,
    )

    analysis = provider.research(
        signal
    )

    print("=" * 60)
    print("LM STUDIO RESEARCH SMOKE TEST")
    print("=" * 60)
    print(analysis)
    print("=" * 60)


if __name__ == "__main__":
    main()