# AI Research & Development Studio AI Workforce Architecture

Version: 0.2
Status: Stabilization Candidate
Last Updated: 2026-08-09

---

# Purpose

This document defines the AI Workforce architecture of the Studio.

The Workforce contains specialized execution components called workers.

Workers provide capabilities to the Studio runtime while remaining independent from orchestration logic.

The Workforce does not imply fully autonomous agents.

A worker may use deterministic logic, an external AI model, or a combination of both.

---

# Workforce Principle

Each worker exists to provide a specific capability.

A worker must have:

- Clear identity
- Clear responsibility
- Declared capabilities
- Defined input types
- Defined output types
- Testable behavior

Workers should remain small and specialized.

New workers are created only when an existing capability cannot satisfy a validated requirement.

---

# Current Workforce

The currently implemented workforce contains four workers:

```text
ResearchWorker
      |
      v
StrategyWorker
      |
      v
PlanningWorker
      |
      v
ValidationWorker
```

They are coordinated by `StudioOrchestrator`.

The runtime also contains non-worker components such as:

- ReviewBoard
- TaskManager
- KnowledgeWriter
- RuntimeGuard
- WorkerRegistry

These components must not be confused with AI workers.

---

# BaseWorker Contract

All Studio workers inherit from `BaseWorker`.

A worker exposes:

```text
name
capabilities
input_types
output_types
```

Worker metadata can be queried through:

`get_metadata()`

Workers can declare multiple capabilities while maintaining a focused responsibility.

---

# WorkerRegistry

`WorkerRegistry` stores the available workers.

Current registered workers:

- research
- strategy
- planning
- validation

The registry supports:

- Direct lookup by name
- Capability lookup
- Contract lookup

Contract lookup matches:

```text
Capability
Input Type
Output Type
```

This enables the orchestrator to locate workers based on what they can do rather than depending only on hard-coded worker names.

---

# ResearchWorker

Purpose:

Investigate a Signal and produce structured research output.

Primary capability:

`research`

Input:

- Signal through WorkerContext

Output:

`ResearchResult`

The result contains:

- Analysis
- Worker identity
- Source Signal
- Optional project context
- Creation time

`ResearchWorker` optionally accepts a `ResearchProvider`.

Without a provider it can operate deterministically.

With a provider it delegates research generation to that provider.

---

# ResearchProvider

`ResearchProvider` defines the boundary between the Studio architecture and external research generation systems.

Current implementation:

`LMStudioResearchProvider`

The provider communicates with a local OpenAI-compatible LM Studio endpoint.

This design keeps ResearchWorker independent from a specific model.

The rest of the worker architecture does not depend on LM Studio directly.

---

# StrategyWorker

Purpose:

Transform researched information into a scored Opportunity.

Primary capability:

`opportunity_scoring`

Input:

`ResearchResult`

Output:

`Opportunity`

The Opportunity contains:

- Signal
- Impact
- Urgency
- Feasibility
- Strategic fit
- Derived total score

StrategyWorker may support additional compatible inputs for backward compatibility, but the current orchestrated pipeline uses `ResearchResult`.

---

# PlanningWorker

Purpose:

Transform an Opportunity into an actionable execution plan.

Primary capability:

`planning`

Input:

`Opportunity`

Output:

`PlanningResult`

The planning result contains:

- Opportunity
- Objective
- Execution steps
- Worker identity
- Creation time

The current PlanningWorker is intentionally simple.

Its purpose is to establish the architectural planning contract rather than implement a complex planning agent.

---

# ValidationWorker

Purpose:

Validate the structural quality of a PlanningResult.

Primary capability:

`validation`

Input:

`PlanningResult`

Output:

`ValidationResult`

The validation result contains:

- Original PlanningResult
- Valid flag
- Reason
- Worker identity
- Creation time

Current validation checks plan completeness.

It should not be interpreted as full real-world product or market validation.

---

# ReviewBoard

`ReviewBoard` is not a worker.

It is a decision component executed after the worker chain.

Current flow:

```text
ValidationResult
      |
      v
ReviewBoard evaluates Opportunity
      |
      v
ReviewDecision
```

The ReviewDecision controls whether an accepted opportunity proceeds to task creation.

---

# Knowledge Relationship

Worker execution contributes to the complete runtime trace.

The final runtime decision is converted into organizational knowledge.

```text
Workers
   |
   v
Review
   |
   v
KnowledgeRecord
   |
   v
Project Memory
```

Persistent project execution history can later be retrieved through `ProjectMemoryStore`.

---

# Compatibility Layer

`studio/workers/strategy.py` currently re-exports `StrategyWorker`.

This compatibility module remains because existing callers and tests still use the old import path.

It is intentionally retained during stabilization.

---

# Future Workforce

Possible future capabilities may include:

- Engineering
- Product
- Domain-specialist workers
- Additional validation capabilities

These are not currently implemented workers.

They must not be treated as part of the active architecture until a validated requirement and explicit architectural decision exist.

---

# Evolution Principle

The Studio avoids worker proliferation.

A new worker should be introduced only when:

1. A real capability gap exists.
2. Existing workers cannot satisfy that requirement cleanly.
3. Input and output contracts can be defined.
4. The worker creates measurable architectural value.

The goal is not to maximize the number of agents.

The goal is to maintain a small, understandable, reliable AI workforce.