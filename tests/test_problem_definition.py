import pytest

from studio.product_realization.problem import (
    ProblemDefinition,
    ProblemStatus,
)


def test_problem_definition_is_created_as_draft():
    problem = ProblemDefinition(
        title="Personalized learning gap",
        description=(
            "Students may not receive continuous identification "
            "of individual learning gaps."
        ),
        source_goal="Build a highly capable personal AI teacher.",
        stakeholders=["student", "parent"],
        target_users=["student"],
        pain_points=[
            "Learning gaps are not continuously identified."
        ],
        success_criteria=[
            "Learning progress can be measured against a baseline."
        ],
    )

    assert problem.status == ProblemStatus.DRAFT
    assert problem.problem_id
    assert problem.source_goal == (
        "Build a highly capable personal AI teacher."
    )


def test_problem_definition_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        ProblemDefinition(
            title="",
            description="A real problem description.",
            source_goal="Investigate the problem.",
        )


def test_problem_definition_rejects_invalid_list_items():
    with pytest.raises(TypeError):
        ProblemDefinition(
            title="Problem",
            description="A real problem description.",
            source_goal="Investigate the problem.",
            pain_points=["Valid pain", 123],
        )


def test_source_goal_is_preserved_without_being_treated_as_problem():
    problem = ProblemDefinition(
        title="Personalization gap",
        description=(
            "Students lack continuous individualized learning support."
        ),
        source_goal="Build an AI teacher application.",
    )

    assert problem.source_goal == "Build an AI teacher application."
    assert problem.description != problem.source_goal