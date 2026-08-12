from studio.product_realization.problem import (
    ProblemDefinition,
    ProblemStatus,
)


class ProblemDefinitionService:
    """
    Minimal lifecycle service for ProblemDefinition artifacts.

    This service performs structural readiness checks only.
    It does not claim that a problem is factually validated.
    """

    def create_problem(
        self,
        *,
        title: str,
        description: str,
        source_goal: str,
        stakeholders=None,
        target_users=None,
        pain_points=None,
        context: str = "",
        constraints=None,
        success_criteria=None,
        non_goals=None,
    ) -> ProblemDefinition:
        return ProblemDefinition(
            title=title,
            description=description,
            source_goal=source_goal,
            stakeholders=list(stakeholders or []),
            target_users=list(target_users or []),
            pain_points=list(pain_points or []),
            context=context,
            constraints=list(constraints or []),
            success_criteria=list(success_criteria or []),
            non_goals=list(non_goals or []),
        )

    def define_problem(
        self,
        problem: ProblemDefinition,
    ) -> ProblemDefinition:
        self._require_problem(problem)

        if problem.status != ProblemStatus.DRAFT:
            raise ValueError(
                "Only DRAFT problems can be marked DEFINED."
            )

        if not problem.pain_points:
            raise ValueError(
                "A defined problem must contain at least one pain point."
            )

        if not problem.success_criteria:
            raise ValueError(
                "A defined problem must contain at least one "
                "success criterion."
            )

        problem.status = ProblemStatus.DEFINED
        return problem

    def reject_problem(
        self,
        problem: ProblemDefinition,
    ) -> ProblemDefinition:
        self._require_problem(problem)

        if problem.status == ProblemStatus.VALIDATED:
            raise ValueError(
                "A VALIDATED problem cannot be directly rejected."
            )

        problem.status = ProblemStatus.REJECTED
        return problem

    @staticmethod
    def _require_problem(
        problem: ProblemDefinition,
    ) -> None:
        if not isinstance(problem, ProblemDefinition):
            raise TypeError(
                "problem must be a ProblemDefinition."
            )