import json
from pathlib import Path

from studio.core.outcome import DecisionOutcome
from studio.core.project_execution_result import ProjectExecutionResult


class ProjectMemoryStore:
    """
    Persistent project-level memory for Studio executions
    and decision-outcome history.
    """

    def __init__(self, path="data/project_memory.json"):
        self.path = Path(path)

    def store_execution(
        self,
        execution: ProjectExecutionResult,
    ) -> dict:
        """
        Persist a completed project execution without
        overwriting previous executions of the same project.
        """

        memory = self._load_all()

        project_name = execution.project.name

        run_record = self._build_run_record(
            execution
        )

        if project_name not in memory:

            memory[project_name] = {
                "project": {
                    "name": execution.project.name,
                    "objective": execution.project.objective,
                    "priority": execution.project.priority,
                },
                "history": [],
                "outcomes": [],
            }

        project_record = memory[
            project_name
        ]

        project_record["project"] = {
            "name": execution.project.name,
            "objective": execution.project.objective,
            "priority": execution.project.priority,
        }

        project_record.setdefault(
            "history",
            [],
        )

        project_record.setdefault(
            "outcomes",
            [],
        )

        project_record["history"].append(
            run_record
        )

        self._save_all(memory)

        return project_record

    def store_outcome(
        self,
        project_name: str,
        outcome: DecisionOutcome,
    ) -> dict:
        """
        Persist a DecisionOutcome for an existing project.
        """

        if not isinstance(
            project_name,
            str,
        ) or not project_name.strip():
            raise ValueError(
                "project_name must be a non-empty string."
            )

        if not isinstance(
            outcome,
            DecisionOutcome,
        ):
            raise TypeError(
                "outcome must be a DecisionOutcome."
            )

        memory = self._load_all()

        project = memory.get(
            project_name
        )

        if project is None:
            raise KeyError(
                f"Project not found: {project_name}"
            )

        if outcome.source_trace_id is not None:
            if not self._execution_trace_exists(
                project,
                outcome.source_trace_id,
            ):
                raise KeyError(
                    "Execution trace not found for outcome: "
                    f"{outcome.source_trace_id}"
                )

        project.setdefault(
            "outcomes",
            [],
        )

        outcome_record = (
            self._build_outcome_record(
                outcome
            )
        )

        project["outcomes"].append(
            outcome_record
        )

        self._save_all(
            memory
        )

        return outcome_record

    def get_project(self, project_name: str):
        """
        Return persisted memory for a project.
        """

        memory = self._load_all()

        return memory.get(project_name)

    def get_execution_history(
        self,
        project_name: str,
    ) -> list:
        """
        Return all persisted execution runs for a project.
        """

        project = self.get_project(
            project_name
        )

        if project is None:
            return []

        return project.get(
            "history",
            [],
        )

    def get_research_history(
        self,
        project_name: str,
    ) -> list:
        """
        Return research records from all project executions.
        """

        history = self.get_execution_history(
            project_name
        )

        records = []

        for run in history:

            for execution in run["executions"]:

                records.append(
                    execution["research"]
                )

        return records

    def get_decision_history(
        self,
        project_name: str,
    ) -> list:
        """
        Return decisions from all project executions.
        """

        history = self.get_execution_history(
            project_name
        )

        records = []

        for run in history:

            for execution in run["executions"]:

                records.append(
                    execution["decision"]
                )

        return records

    def get_knowledge_history(
        self,
        project_name: str,
    ) -> list:
        """
        Return knowledge records from all project executions.
        """

        history = self.get_execution_history(
            project_name
        )

        records = []

        for run in history:

            for execution in run["executions"]:

                records.append(
                    execution["knowledge"]
                )

        return records

    def get_outcome_history(
        self,
        project_name: str,
    ) -> list:
        """
        Return persisted decision outcomes for a project.
        """

        project = self.get_project(
            project_name
        )

        if project is None:
            return []

        return project.get(
            "outcomes",
            [],
        )

    def get_decision_outcome_trace(
        self,
        project_name: str,
        source_trace_id: str,
    ):
        """
        Reconstruct a persisted execution together with
        the observed outcome attached to that execution.
        """

        if not isinstance(
            source_trace_id,
            str,
        ) or not source_trace_id.strip():
            raise ValueError(
                "source_trace_id must be a non-empty string."
            )

        project = self.get_project(
            project_name
        )

        if project is None:
            return None

        execution_record = None

        for run in project.get(
            "history",
            [],
        ):

            for execution in run.get(
                "executions",
                [],
            ):

                if (
                    execution.get("trace_id")
                    == source_trace_id
                ):
                    execution_record = execution
                    break

            if execution_record is not None:
                break

        outcome_record = None

        for outcome in project.get(
            "outcomes",
            [],
        ):

            if (
                outcome.get("source_trace_id")
                == source_trace_id
            ):
                outcome_record = outcome
                break

        if (
            execution_record is None
            or outcome_record is None
        ):
            return None

        return {
            "execution": execution_record,
            "outcome": outcome_record,
        }

    def all_projects(self) -> dict:
        """
        Return all persisted project memories.
        """

        return self._load_all()

    def _build_run_record(
        self,
        execution: ProjectExecutionResult,
    ) -> dict:
        """
        Convert a project execution into a persistent run record.
        """

        run_record = {
            "created_at": execution.created_at.isoformat(),
            "status": execution.status,
            "total_results": execution.total_results,
            "accepted_count": execution.accepted_count,
            "deferred_count": execution.deferred_count,
            "rejected_count": execution.rejected_count,
            "executions": [],
        }

        for result in execution.results:

            task_record = None

            if result.task is not None:

                task_record = {
                    "objective": result.task.objective,
                    "status": result.task.status,
                }

            execution_record = {
                "trace_id": result.trace_id,
                "created_at": result.created_at.isoformat(),
                "signal": {
                    "title": result.signal.title,
                    "description": result.signal.description,
                    "source": result.signal.source,
                    "created_at": (
                        result.signal.created_at.isoformat()
                    ),
                },
                "research": self._build_research_record(
                    result.research_result
                ),
                "opportunity": self._build_opportunity_record(
                    result.opportunity
                ),
                "planning": self._build_planning_record(
                    result.planning_result
                ),
                "validation": self._build_validation_record(
                    result.validation_result
                ),
                "decision": self._build_decision_record(
                    result.decision
                ),
                "task": task_record,
                "knowledge": {
                    "title": result.knowledge.title,
                    "content": result.knowledge.content,
                    "tags": result.knowledge.tags,
                    "created_at": (
                        result.knowledge.created_at.isoformat()
                    ),
                },
            }

            run_record[
                "executions"
            ].append(
                execution_record
            )

        return run_record

    def _build_research_record(
        self,
        research_result,
    ) -> dict:
        return {
            "analysis": research_result.analysis,
            "worker": research_result.worker,
            "created_at": (
                research_result.created_at.isoformat()
            ),
            "claims": [
                self._build_claim_record(claim)
                for claim in research_result.claims
            ],
        }

    def _build_claim_record(
        self,
        claim,
    ) -> dict:
        return {
            "statement": claim.statement,
            "confidence": claim.confidence,
            "uncertainty": claim.uncertainty,
            "supporting_evidence": [
                self._build_evidence_record(evidence)
                for evidence in claim.supporting_evidence
            ],
            "counter_evidence": [
                self._build_evidence_record(evidence)
                for evidence in claim.counter_evidence
            ],
        }

    def _build_evidence_record(
        self,
        evidence,
    ) -> dict:
        return {
            "content": evidence.content,
            "confidence": evidence.confidence,
            "provenance_note": evidence.provenance_note,
            "source": {
                "name": evidence.source.name,
                "source_type": evidence.source.source_type,
                "reference": evidence.source.reference,
                "metadata": evidence.source.metadata,
            },
        }

    def _build_opportunity_record(
        self,
        opportunity,
    ) -> dict:
        return {
            "impact": opportunity.impact,
            "urgency": opportunity.urgency,
            "feasibility": opportunity.feasibility,
            "strategic_fit": opportunity.strategic_fit,
            "score": opportunity.score,
            "evidence_state": opportunity.evidence_state,
            "evidence_confidence": opportunity.evidence_confidence,
            "rationale": opportunity.rationale,
        }

    def _build_planning_record(
        self,
        planning_result,
    ):
        if planning_result is None:
            return None

        hypothesis_record = None

        if planning_result.hypothesis is not None:
            hypothesis_record = {
                "statement": (
                    planning_result.hypothesis.statement
                ),
                "assumptions": (
                    planning_result.hypothesis.assumptions
                ),
                "success_criteria": (
                    planning_result.hypothesis.success_criteria
                ),
                "failure_criteria": (
                    planning_result.hypothesis.failure_criteria
                ),
            }

        experiment_record = None

        if planning_result.experiment is not None:

            measurements = []

            for measurement in (
                planning_result.experiment.measurements
            ):
                direction = None

                if measurement.direction is not None:
                    direction = (
                        measurement.direction.value
                    )

                measurements.append(
                    {
                        "metric": measurement.metric,
                        "baseline": measurement.baseline,
                        "target": measurement.target,
                        "unit": measurement.unit,
                        "direction": direction,
                    }
                )

            experiment_record = {
                "objective": (
                    planning_result.experiment.objective
                ),
                "method": (
                    planning_result.experiment.method
                ),
                "measurements": measurements,
                "stop_conditions": (
                    planning_result.experiment.stop_conditions
                ),
            }

        return {
            "objective": planning_result.objective,
            "steps": planning_result.steps,
            "worker": planning_result.worker,
            "created_at": (
                planning_result.created_at.isoformat()
            ),
            "hypothesis": hypothesis_record,
            "experiment": experiment_record,
        }

    def _build_validation_record(
        self,
        validation_result,
    ):
        if validation_result is None:
            return None

        return {
            "valid": validation_result.valid,
            "reason": validation_result.reason,
            "worker": validation_result.worker,
            "created_at": (
                validation_result.created_at.isoformat()
            ),
        }

    def _build_decision_record(
        self,
        decision,
    ) -> dict:
        return {
            "decision": decision.decision,
            "reason": decision.reason,
            "confidence": getattr(
                decision,
                "confidence",
                None,
            ),
            "next_action": decision.next_action,
        }

    def _build_outcome_record(
        self,
        outcome: DecisionOutcome,
    ) -> dict:
        """
        Convert a DecisionOutcome into a persistent record.
        """

        observations = []

        for observation in outcome.observations:

            observations.append(
                {
                    "metric": observation.metric,
                    "observed_value": (
                        observation.observed_value
                    ),
                    "unit": observation.unit,
                    "note": observation.note,
                }
            )

        return {
            "source_trace_id": outcome.source_trace_id,
            "created_at": outcome.created_at.isoformat(),
            "signal": {
                "title": (
                    outcome.opportunity.signal.title
                ),
                "description": (
                    outcome.opportunity.signal.description
                ),
                "source": (
                    outcome.opportunity.signal.source
                ),
            },
            "opportunity": self._build_opportunity_record(
                outcome.opportunity
            ),
            "planning": self._build_planning_record(
                outcome.planning_result
            ),
            "decision": self._build_decision_record(
                outcome.decision
            ),
            "status": outcome.status.value,
            "observations": observations,
            "summary": outcome.summary,
        }

    def _execution_trace_exists(
        self,
        project: dict,
        trace_id: str,
    ) -> bool:
        for run in project.get(
            "history",
            [],
        ):
            for execution in run.get(
                "executions",
                [],
            ):
                if (
                    execution.get("trace_id")
                    == trace_id
                ):
                    return True

        return False

    def _load_all(self) -> dict:

        if not self.path.exists():
            return {}

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _save_all(
        self,
        memory: dict,
    ) -> None:

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                memory,
                file,
                ensure_ascii=False,
                indent=2,
            )