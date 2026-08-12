import pytest

from studio.product_realization.problem import ProblemStatus
from studio.product_realization.problem_service import (
    ProblemDefinitionService,
)


def test_service_creates_problem():
    service = ProblemDefinitionService()

    problem = service.create_problem(
        title="Personalized learning gap",
        description=(
            "Students may not receive learning support adapted "
            "to their individual gaps."
        ),
        source_goal="Build a personal AI teacher.",
    )

    assert problem.status == ProblemStatus.DRAFT
    assert problem.problem_id


def test_defined_problem_requires_pain_point():
    service = ProblemDefinitionService()

    problem = service.create_problem(
        title="Personalized learning gap",
        description="Students lack individualized learning support.",
        source_goal="Build a personal AI teacher.",
        success_criteria=[
            "Learning improvement can be measured."
        ],
    )

    with pytest.raises(ValueError):
        service.define_problem(problem)


def test_defined_problem_requires_success_criterion():
    service = ProblemDefinitionService()

    problem = service.create_problem(
        title="Personalized learning gap",
        description="Students lack individualized learning support.",
        source_goal="Build a personal AI teacher.",
        pain_points=[
            "Learning gaps are not continuously identified."
        ],
    )

    with pytest.raises(ValueError):
        service.define_problem(problem)


def test_complete_draft_can_become_defined():
    service = ProblemDefinitionService()

    problem = service.create_problem(
        title="Personalized learning gap",
        description="Students lack individualized learning support.",
        source_goal="Build a personal AI teacher.",
        pain_points=[
            "Learning gaps are not continuously identified."
        ],
        success_criteria=[
            "Learning improvement can be measured."
        ],
    )

    result = service.define_problem(problem)

    assert result is problem
    assert problem.status == ProblemStatus.DEFINED


def test_defined_problem_cannot_be_defined_twice():
    service = ProblemDefinitionService()

    problem = service.create_problem(
        title="Personalized learning gap",
        description="Students lack individualized learning support.",
        source_goal="Build a personal AI teacher.",
        pain_points=[
            "Learning gaps are not continuously identified."
        ],
        success_criteria=[
            "Learning improvement can be measured."
        ],
    )

    service.define_problem(problem)

    with pytest.raises(ValueError):
        service.define_problem(problem)


def test_problem_can_be_rejected():
    service = ProblemDefinitionService()

    problem = service.create_problem(
        title="Unclear problem",
        description="The problem requires further framing.",
        source_goal="Build something.",
    )

    service.reject_problem(problem)

    assert problem.status == ProblemStatus.REJECTED