
# ADR-004 — Evidence & Provenance Model

Status: Accepted
Date: 2026-08-09
Cycle: Evidence & Decision Integrity
Phase: 1 — Evidence & Provenance Foundation

---

# Context

AI-RD-Studio v0.2.0 contains a working research-to-decision runtime pipeline.

However, post-freeze review identified a critical limitation:

`ResearchResult` primarily carries prose analysis.

The current system does not yet represent, as first-class structured data:

- Claims
- Supporting evidence
- Counter-evidence
- Source provenance
- Confidence
- Uncertainty

This creates a gap between the Studio's Evidence First principle and its runtime behavior.

A structured evidence model is required before Research can causally and explainably influence Strategy and Validation.

---

# Decision

Evidence-related runtime domain concepts will be introduced under:

`studio/core/evidence.py`

This module will contain the minimum shared evidence model used by multiple layers of the Studio.

The evidence model is considered part of the core domain rather than:

- Knowledge persistence
- Worker implementation
- Provider-specific logic
- Research-only infrastructure

This is because evidence will eventually be consumed by:

- Research
- Strategy
- Validation
- Decision tracing
- Persistent history

---

# Initial Model

Phase 1 will introduce the following minimum concepts:

## EvidenceSource

Represents where a piece of evidence came from.

Minimum responsibilities:

- Source identity
- Source type
- Optional reference
- Optional retrieval or observation metadata

The model must not assume that every source is a URL.

Possible source types may later include:

- Web
- Document
- API
- Human observation
- Dataset
- Internal system
- LLM-generated analysis

Phase 1 will not introduce a complex source taxonomy.

---

## Evidence

Represents one item that may support or contradict a claim.

Minimum responsibilities:

- Content
- Source
- Confidence
- Optional provenance note

The same `Evidence` type will be used for both supporting and contradictory evidence.

A separate `CounterEvidence` class will not be introduced.

The role of evidence is determined by where it is attached to a Claim.

---

## Claim

Represents a proposition produced or evaluated during research.

Minimum responsibilities:

- Statement
- Supporting evidence
- Counter-evidence
- Confidence
- Uncertainty

A Claim should make it possible to inspect why a conclusion is supported or challenged.

---

# Confidence

Confidence will use a normalized numeric range:

```text
0.0 <= confidence <= 1.0
````

Confidence represents uncertainty in a judgment.

It must not be interpreted as objective truth.

Phase 1 will define structural validity only.

No advanced confidence-calibration engine will be implemented.

---

# Uncertainty

Uncertainty will remain explicit.

A Claim may contain a short uncertainty description explaining what remains unknown or weakly supported.

Phase 1 will not create an uncertainty taxonomy or probabilistic reasoning engine.

---

# ResearchResult Integration

Existing `ResearchResult.analysis` will remain.

This preserves backward compatibility with the current runtime and provider behavior.

Structured evidence will be added alongside the existing analysis.

Conceptually:

```text
ResearchResult
├── analysis
├── signal
├── project_name
├── claims[]
└── metadata
```

Phase 1 must not break existing deterministic and LM Studio research paths without explicit migration.

---

# Separation of Responsibilities

## Core Evidence Model

Responsible for:

* Claim structure
* Evidence structure
* Source/provenance structure
* Confidence and uncertainty representation

## ResearchWorker / ResearchProvider

Responsible for:

* Producing research information
* Eventually populating structured claims and evidence

## StrategyWorker

Will consume structured evidence in Phase 2.

Phase 1 must not implement Strategy evidence scoring.

## ValidationWorker

Will consume evidence later during Phase 4.

Phase 1 must not implement evidence-based validation.

## ProjectMemoryStore

Persistence of the new evidence model will be reviewed after the runtime representation is stable.

Do not redesign persistence prematurely.

---

# Trust Boundary

Evidence structure does not imply evidence truth.

The architecture must preserve the following rule:

```text
External input = untrusted data
LLM output = untrusted data
```

Structured evidence improves inspectability and traceability.

It does not automatically make information verified.

---

# Non-Goals

Phase 1 will not implement:

* Web crawling
* Source verification engine
* Citation ranking
* Fact-checking engine
* Complex provenance graph
* Knowledge graph
* Bayesian inference
* Automated source reputation
* Strategy scoring from evidence
* Validation gating
* Autonomous learning
* New workers

These belong to later phases or future cycles.

---

# Alternatives Considered

## `studio/knowledge/evidence.py`

Rejected.

Evidence participates in live reasoning and is not merely persistent knowledge.

Placing it under Knowledge would incorrectly couple the domain model to storage semantics.

---

## `studio/workers/evidence.py`

Rejected.

Evidence is not owned by a worker.

Multiple workers and runtime components may consume it.

---

## `studio/research/evidence.py`

Rejected for now.

The current architecture does not have a research domain package.

Creating one solely for this model would introduce premature structure.

---

## Separate CounterEvidence Class

Rejected.

Supporting and opposing evidence share the same fundamental structure.

Separate classes would add complexity without a demonstrated requirement.

---

# Consequences

## Positive

* Evidence becomes inspectable.
* Research can evolve beyond opaque prose.
* Strategy can later reason over evidence explicitly.
* Validation can later evaluate evidence sufficiency.
* Decision explanations can become traceable.
* The model remains provider-agnostic.

## Negative

* `ResearchResult` becomes richer.
* Persistence will eventually need to support nested evidence structures.
* Confidence semantics must be kept disciplined.
* Incorrectly structured evidence can still contain false information.

---

# Compatibility

`ResearchResult.analysis` remains supported.

Existing providers and tests should continue to work while structured evidence is introduced incrementally.

Backward compatibility will be removed only through a separate architectural decision if it ever becomes unnecessary.

---

# Phase 1 Exit Relationship

This ADR establishes the data-model foundation only.

Phase 1 is not complete until:

* Evidence models exist.
* Model invariants are tested.
* ResearchResult can carry Claims.
* Research paths remain compatible.
* Structured evidence can be produced in at least one controlled path.
* Runtime validation supports the new structure where appropriate.
* Regression suite passes.
* Git checkpoint is clean.

---

# Final Decision

AI-RD-Studio will introduce a minimal provider-agnostic Evidence & Provenance domain model under:

`studio/core/evidence.py`

The model will prioritize:

* Inspectability
* Traceability
* Minimalism
* Backward compatibility

No downstream intelligence expansion will occur until the evidence foundation is stable.

