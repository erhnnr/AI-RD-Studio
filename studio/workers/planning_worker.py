from studio.core.experiment import (
    Experiment,
    Hypothesis,
    Measurement,
)
from studio.core.models import Opportunity, PlanningResult
from studio.workers.base import BaseWorker


class PlanningWorker(BaseWorker):
    """
    Worker responsible for converting an opportunity
    into a testable R&D plan.
    """

    def __init__(self):
        super().__init__("PlanningWorker")

        self.capabilities = [
            "planning",
            "task_planning",
            "execution_planning",
        ]

        self.input_types = [
            "Opportunity",
        ]

        self.output_types = [
            "PlanningResult",
        ]

    def _build_hypothesis(
        self,
        opportunity: Opportunity,
    ) -> Hypothesis:
        title = opportunity.signal.title
        evidence_state = opportunity.evidence_state

        assumptions = [
            (
                f"The conditions described by the signal for "
                f"'{title}' are sufficiently representative "
                f"for a bounded test."
            ),
        ]

        if evidence_state == "SUPPORTING":
            assumptions.append(
                "The supporting research evidence remains relevant "
                "during the experiment."
            )

        elif evidence_state == "INSUFFICIENT":
            assumptions.append(
                "Additional observations can provide enough evidence "
                "to reduce the current uncertainty."
            )

        elif evidence_state == "MIXED":
            assumptions.append(
                "The conflicting evidence can be meaningfully compared "
                "under controlled conditions."
            )

        elif evidence_state == "CONTRADICTORY":
            assumptions.append(
                "The contradictory evidence can be tested before "
                "progression is reconsidered."
            )

        return Hypothesis(
            statement=(
                f"A bounded test of '{title}' can produce "
                f"observable evidence about whether the opportunity "
                f"should progress."
            ),
            assumptions=assumptions,
            success_criteria=[
                (
                    f"The test produces measurable evidence supporting "
                    f"progression of '{title}'."
                ),
            ],
            failure_criteria=[
                (
                    f"The test fails to produce meaningful support for "
                    f"progression of '{title}' or strengthens "
                    f"contradictory evidence."
                ),
            ],
        )

    def _experiment_method(
        self,
        opportunity: Opportunity,
    ) -> str:
        evidence_state = opportunity.evidence_state

        if evidence_state == "SUPPORTING":
            return (
                "Run a bounded prototype or controlled comparison "
                "to test whether the supported opportunity produces "
                "the expected observable outcome."
            )

        if evidence_state == "INSUFFICIENT":
            return (
                "Run a bounded evidence-gathering test focused on "
                "reducing the current uncertainty before progression."
            )

        if evidence_state == "MIXED":
            return (
                "Run a controlled comparison designed to distinguish "
                "between the supporting and contradictory evidence."
            )

        if evidence_state == "CONTRADICTORY":
            return (
                "Run a falsification-focused test to determine whether "
                "the contradictory evidence remains valid under "
                "controlled conditions."
            )

        return (
            "Run a bounded exploratory test to collect measurable "
            "evidence about the opportunity."
        )

    def _build_experiment(
        self,
        opportunity: Opportunity,
    ) -> Experiment:
        title = opportunity.signal.title

        measurement = Measurement(
            metric=f"Observable outcome for {title}",
            baseline=None,
            target=None,
            unit=None,
        )

        return Experiment(
            objective=(
                f"Test whether '{title}' has sufficient observable "
                f"support to justify further R&D progression."
            ),
            method=self._experiment_method(
                opportunity
            ),
            measurements=[
                measurement,
            ],
            stop_conditions=[
                "Success criterion is reached.",
                "Failure criterion is reached.",
                "The bounded test period or resource limit is reached.",
            ],
        )

    def execute(
        self,
        opportunity: Opportunity,
    ) -> PlanningResult:
        if not isinstance(opportunity, Opportunity):
            raise TypeError(
                "PlanningWorker requires an Opportunity."
            )

        hypothesis = self._build_hypothesis(
            opportunity
        )

        experiment = self._build_experiment(
            opportunity
        )

        objective = (
            f"Test opportunity through a bounded R&D experiment: "
            f"{opportunity.signal.title}"
        )

        steps = [
            "Review the opportunity evidence and assumptions.",
            f"Define the test boundary for {opportunity.signal.title}.",
            f"Measure: {experiment.measurements[0].metric}.",
            "Compare observed evidence with success and failure criteria.",
            "Record whether the opportunity should progress, defer, or stop.",
        ]

        return PlanningResult(
            opportunity=opportunity,
            objective=objective,
            steps=steps,
            hypothesis=hypothesis,
            experiment=experiment,
            worker=self.name,
        )