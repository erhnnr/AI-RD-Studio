import json
from pathlib import Path

from studio.core.project_execution_result import ProjectExecutionResult


class ProjectMemoryStore:
    """
    Persistent project-level memory for Studio executions.
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
            }

        project_record = memory[
            project_name
        ]

        project_record["project"] = {
            "name": execution.project.name,
            "objective": execution.project.objective,
            "priority": execution.project.priority,
        }

        project_record["history"].append(
            run_record
        )

        self._save_all(memory)

        return project_record

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
                "signal": {
                    "title": result.signal.title,
                    "description": result.signal.description,
                    "source": result.signal.source,
                },
                "research": {
                    "analysis": (
                        result.research_result.analysis
                    ),
                    "worker": (
                        result.research_result.worker
                    ),
                },
                "opportunity": {
                    "impact": result.opportunity.impact,
                    "urgency": result.opportunity.urgency,
                    "feasibility": (
                        result.opportunity.feasibility
                    ),
                    "strategic_fit": (
                        result.opportunity.strategic_fit
                    ),
                    "score": result.opportunity.score,
                },
                "decision": {
                    "decision": (
                        result.decision.decision
                    ),
                    "reason": (
                        result.decision.reason
                    ),
                    "next_action": (
                        result.decision.next_action
                    ),
                },
                "task": task_record,
                "knowledge": {
                    "title": result.knowledge.title,
                    "content": result.knowledge.content,
                    "tags": result.knowledge.tags,
                },
            }

            run_record[
                "executions"
            ].append(
                execution_record
            )

        return run_record

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