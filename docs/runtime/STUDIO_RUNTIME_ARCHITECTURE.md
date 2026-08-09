# AI Research & Development Studio Runtime Architecture

Version: 0.1
Status: Stabilization Candidate
Last Updated: 2026-08-09

---

# Purpose

This document defines the runtime execution architecture of AI Research & Development Studio.

The runtime is responsible for coordinating workers, validating intermediate results, creating decisions and tasks, generating knowledge, and returning a complete execution trace.

The central runtime component is:

`StudioOrchestrator`

---

# Runtime Pipeline

The current implemented pipeline is:

```text
Signal
  |
  v
ResearchWorker
  |
  v
ResearchResult
  |
  v
StrategyWorker
  |
  v
Opportunity
  |
  v
PlanningWorker
  |
  v
PlanningResult
  |
  v
ValidationWorker
  |
  v
ValidationResult
  |
  v
ReviewBoard
  |
  v
Decision
  |
  +--> ResearchTask when accepted
  |
  v
KnowledgeRecord
```

The complete trace is represented by:

`PipelineResult`

---

# StudioOrchestrator

`StudioOrchestrator` coordinates the execution pipeline.

Its responsibilities include:

- Validate incoming Signal
- Select ResearchWorker
- Execute research
- Validate ResearchResult
- Select StrategyWorker
- Produce Opportunity
- Validate Opportunity
- Select PlanningWorker
- Produce PlanningResult
- Validate PlanningResult
- Select ValidationWorker
- Produce ValidationResult
- Validate ValidationResult
- Request ReviewBoard decision
- Validate decision
- Create task when accepted
- Generate KnowledgeRecord
- Return final output or complete trace

The orchestrator does not contain the domain logic of individual workers.

It coordinates specialized components.

---

# Worker Discovery

Workers are managed through:

`WorkerRegistry`

The registry currently contains:

- ResearchWorker
- StrategyWorker
- PlanningWorker
- ValidationWorker

Workers may be found by registry name.

They may also be discovered through contracts consisting of:

```text
Capability
+
Input Type
+
Output Type
```

Example:

```text
planning
+
Opportunity
+
PlanningResult
```

returns:

`PlanningWorker`

This reduces direct coupling between runtime orchestration and worker implementation names.

---

# Research Stage

Input:

`Signal`

Worker:

`ResearchWorker`

Output:

`ResearchResult`

`ResearchWorker` can operate using deterministic internal behavior or an injected `ResearchProvider`.

The current external provider implementation is:

`LMStudioResearchProvider`

---

# Strategy Stage

Input:

`ResearchResult`

Worker:

`StrategyWorker`

Output:

`Opportunity`

The opportunity contains strategic scoring dimensions:

- Impact
- Urgency
- Feasibility
- Strategic fit

The total opportunity score is derived from these values.

---

# Planning Stage

Input:

`Opportunity`

Worker:

`PlanningWorker`

Output:

`PlanningResult`

The planning result contains:

- Opportunity
- Objective
- Execution steps
- Worker identity
- Creation time

---

# Validation Stage

Input:

`PlanningResult`

Worker:

`ValidationWorker`

Output:

`ValidationResult`

The validation result contains:

- PlanningResult
- Valid flag
- Reason
- Worker identity
- Creation time

The current validation implementation checks structural plan validity.

It does not yet represent real-world product validation.

---

# Review Stage

The `ReviewBoard` evaluates an `Opportunity`.

It returns a `ReviewDecision`.

The review decision determines whether the opportunity is accepted or rejected and identifies the next action.

`ReviewBoard` is not an AI Worker.

It is a runtime decision component.

---

# Task Creation

Accepted opportunities may generate a `ResearchTask`.

Task creation is handled by:

`TaskManager`

Rejected opportunities do not generate a task.

---

# Knowledge Generation

Each pipeline execution generates a `KnowledgeRecord`.

This is handled by:

`KnowledgeWriter`

Knowledge generation occurs for both accepted and rejected decisions.

---

# Runtime Validation

`RuntimeGuard` protects critical pipeline boundaries.

Current validations include:

- Signal validity
- Worker availability
- ResearchResult validity
- Opportunity validity
- PlanningResult validity
- ValidationResult validity
- Review decision structure
- ResearchTask validity
- KnowledgeRecord validity

Contract violations raise:

`RuntimeValidationError`

This prevents invalid intermediate values from silently propagating through the runtime.

---

# PipelineResult

`execute_with_trace()` returns a complete `PipelineResult`.

It contains:

- Signal
- ResearchResult
- Opportunity
- PlanningResult
- ValidationResult
- Decision
- Optional ResearchTask
- KnowledgeRecord
- Creation time

This allows the execution path to remain observable and testable.

---

# Project-Level Runtime

Multiple signals can be executed through:

`ProjectContext`

The orchestrator processes every signal and returns:

`ProjectExecutionResult`

The project result provides:

- Complete PipelineResult collection
- Total result count
- Accepted count
- Rejected count
- Execution status

Current project execution is sequential and deterministic at the orchestration level.

---

# Persistent Memory

Project execution results can be stored through:

`ProjectMemoryStore`

Project memory preserves multiple execution runs rather than overwriting previous history.

Retrieval APIs support:

- Project execution history
- Research history
- Decision history
- Knowledge history

---

# Failure Philosophy

The runtime follows a controlled failure model.

Invalid contracts should fail explicitly at architectural boundaries.

The runtime should not silently continue with malformed worker outputs.

At the same time, unnecessary exception layers and recovery abstractions are avoided until a real requirement exists.

---

# Current Scope Boundary

The runtime currently does not implement:

- Automatic recurring execution
- Autonomous signal discovery
- Distributed workers
- Parallel worker scheduling
- Worker self-modification
- Dynamic worker generation
- Autonomous retry loops

These capabilities are outside the stabilization scope.

---

# Stabilization Objective

The current runtime is being frozen as a stable architectural baseline.

The objective is not maximum autonomy.

The objective is a small, understandable, testable, modular execution core upon which future Studio capabilities can be built safely.