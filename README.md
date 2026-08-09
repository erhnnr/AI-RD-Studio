# AI Research & Development Studio

## Overview

AI Research & Development Studio is an AI-native research and development platform designed to transform real-world signals into researched, evaluated, planned, validated, and recorded outcomes.

The Studio is not a single product.

It is a reusable platform for supporting research, strategy, planning, validation, decision making, project execution, and organizational memory.

The Studio is currently developed as a human-operated, AI-supported system.

Autonomous problem discovery and unrestricted agent autonomy are intentionally outside the current implementation scope.

---

## Core Mission

To discover where meaningful value can be created and systematically transform signals into researched and validated opportunities.

---

## Core Principles

### Problem First

Start with real problems, signals, and opportunities rather than technologies.

### Core First

Build reliable foundations before introducing additional complexity.

### Evidence First

Important decisions should be supported by research, experiments, and validation.

### Validation Driven

Ideas should not progress without explicit validation.

### Knowledge Preservation

Research, decisions, execution results, and lessons should become part of the Studio's memory.

### Measured Evolution

New capabilities are added only when a validated requirement exists.

---

## Current Runtime Pipeline

The implemented Studio runtime currently follows this flow:

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
  +--> Task
  |
  v
KnowledgeRecord
```

A complete execution trace can be returned as a `PipelineResult`.

---

## Current AI Workforce

The currently implemented workers are:

- ResearchWorker
- StrategyWorker
- PlanningWorker
- ValidationWorker

Workers declare:

- Name
- Capabilities
- Input types
- Output types

The `WorkerRegistry` can locate workers by capability and contract.

Workers are intentionally kept specialized and small.

New workers are not added unless a real architectural requirement appears.

---

## Research Provider

`ResearchWorker` supports an optional external research provider.

The current implementation includes:

- Deterministic fallback research
- `ResearchProvider` abstraction
- `LMStudioResearchProvider`

This allows the Studio to use a locally running OpenAI-compatible model through LM Studio without coupling the rest of the architecture to a specific model.

---

## Project-Level Execution

The Studio can execute multiple signals inside a `ProjectContext`.

```text
ProjectContext
  |
  +--> Signal
  +--> Signal
  +--> Signal
         |
         v
   StudioOrchestrator
         |
         v
ProjectExecutionResult
```

`ProjectExecutionResult` records:

- Project
- Pipeline results
- Accepted count
- Rejected count
- Execution status
- Creation time

---

## Knowledge and Memory

The Studio currently has two memory concepts.

### Runtime Knowledge

`KnowledgeWriter` creates `KnowledgeRecord` objects during pipeline execution.

### Project Memory

`ProjectMemoryStore` persists project execution history to JSON.

It can retrieve:

- Project history
- Research history
- Decision history
- Knowledge history

This provides persistent organizational memory across project executions.

---

## Architecture Layers

The Studio is organized around five architectural layers:

```text
AI Research & Development Studio
|
+-- Foundation
|
+-- Operating System
|
+-- AI Workforce
|
+-- Knowledge
|
+-- Portfolio
```

Runtime orchestration connects these layers during execution.

---

## Current Development State

The current implementation includes:

- Signal model
- Research pipeline
- Strategy and opportunity scoring
- Planning
- Validation
- Review decisions
- Task creation
- Knowledge generation
- Runtime guards
- Worker registry and contract discovery
- Project-level orchestration
- Persistent project memory
- Optional local LLM research through LM Studio
- Full multi-worker execution trace

Current verified regression baseline:

```text
84 tests passing
```

---

## Intentional Non-Goals for the Current Stage

The current architecture does not attempt to implement:

- Autonomous internet-scale signal crawling
- Fully autonomous organization management
- Self-modifying workers
- Unlimited worker proliferation
- EngineeringWorker
- ProductWorker
- Domain-specific specialization
- Automatic self-learning loops

These capabilities may be evaluated later only when a validated requirement exists.

---

## Vision

To build a continuously evolving AI-native research and development organization capable of creating technologies, products, and knowledge across multiple domains while preserving explainability, validation, and accumulated organizational memory.