# ADR-010 — Outcome Feedback and Decision Result Model

Status: Accepted
Date: 2026-08-09
Cycle: Evidence & Decision Integrity
Phase: 6 — Outcome Feedback + Stabilization

---

# Context

AI-RD-Studio currently supports:

- Signals
- Research results
- Structured evidence
- Evidence assessment
- Evidence-sensitive strategy
- Opportunity generation
- Hypothesis
- Experiment
- Measurement
- Validation gates
- Review decisions
- Tasks
- Knowledge records
- Project execution
- Semantic development evaluation
- Holdout evaluation

The current pipeline can reason about whether an opportunity should progress.

However, it does not yet formally record what happened after progression.

The Studio can therefore record:

```text
what it believed
what it decided
why it decided
````

but not yet:

```text
what actually happened
```

This limits the ability to compare decision expectations with observed reality.

---

# Problem

A decision system is incomplete if it cannot later answer:

```text
What happened after this decision?
```

or:

```text
Did the observed result support the original hypothesis?
```

or:

```text
Was the expected outcome actually observed?
```

Without a formal outcome model, the Studio risks becoming an archive of decisions rather than a system capable of accumulating decision-result history.

---

# Decision

AI-RD-Studio will introduce explicit outcome records.

The minimum Phase 6 domain model will contain:

```text
OutcomeObservation
DecisionOutcome
OutcomeStatus
```

These objects will represent observed results without claiming autonomous learning.

---

# OutcomeStatus

OutcomeStatus represents the current interpretation of an observed result.

Initial states:

```text
SUCCESS
FAILURE
PARTIAL
INCONCLUSIVE
NOT_OBSERVED
```

These states describe the observed result relative to the tested expectation.

They are not global statements about product success or scientific truth.

---

# OutcomeObservation

OutcomeObservation represents one observed measurement or fact.

Minimum fields:

```text
metric
observed_value
unit
note
```

`metric` identifies what was observed.

`observed_value` may be numeric or textual because not all early R&D observations are quantitative.

`unit` is optional.

`note` is optional explanatory context.

---

# DecisionOutcome

DecisionOutcome links an observed result back to the decision and plan that produced it.

Minimum fields:

```text
opportunity
planning_result
decision
status
observations
summary
created_at
```

The model must preserve traceability to:

```text
Opportunity
PlanningResult
Decision
```

so that the Studio can later reconstruct:

```text
why the opportunity progressed
what was expected
what experiment was planned
what decision was made
what was actually observed
```

---

# Traceability

Phase 6 requires explicit causal traceability.

The desired chain is:

```text
Signal
↓
ResearchResult
↓
Opportunity
↓
PlanningResult
↓
ValidationResult
↓
ReviewDecision
↓
DecisionOutcome
```

Outcome records must not float independently from the decision that produced them.

---

# Outcome Observation Does Not Equal Learning

Mandatory distinction:

```text
recording an outcome
!=
learning from an outcome
```

Phase 6 introduces structured feedback.

It does not automatically modify:

* StrategyWorker
* evidence thresholds
* ReviewBoard thresholds
* validation policy
* worker prompts
* model weights
* planning rules

Automatic adaptation requires a future explicit architecture decision.

---

# Expected vs Observed

When a PlanningResult contains an Experiment and Measurement definitions, DecisionOutcome should allow later comparison between:

```text
expected or target condition
```

and:

```text
observed condition
```

Phase 6 will not require advanced statistical comparison.

The first objective is transparent recording and basic comparison.

---

# Success

SUCCESS means the observed result satisfies the relevant success criterion or expected condition for the bounded experiment.

It does not mean:

```text
the product is commercially successful
the hypothesis is universally true
the research question is permanently solved
```

---

# Failure

FAILURE means the bounded experiment produced an observed result that satisfies a defined failure condition or clearly fails the relevant success condition.

Failure is a valid and useful outcome.

The Studio must preserve failed experiments rather than hide or overwrite them.

---

# Partial

PARTIAL means some expected conditions were observed but the result does not cleanly satisfy either complete success or complete failure.

---

# Inconclusive

INCONCLUSIVE means the available observations do not support a defensible success or failure interpretation.

Examples include:

* insufficient observations
* noisy or conflicting measurements
* interrupted experiment
* ambiguous result

---

# Not Observed

NOT_OBSERVED means an outcome record exists but no real observation has yet been recorded.

This may be used for lifecycle tracking.

It must not be treated as SUCCESS or FAILURE.

---

# Decision Relationship

DecisionOutcome may be associated with decisions such as:

```text
ACCEPT
DEFER
REJECT
```

However, actual experiments will normally follow progression decisions.

Phase 6 does not require every DEFER or REJECT decision to contain an experiment outcome.

---

# Outcome Integrity

An outcome record must not invent observations.

If no real observation exists:

```text
status = NOT_OBSERVED
```

or an explicit absence must be preserved.

Generated or assumed results must not be presented as observed reality.

---

# Provenance of Outcomes

Phase 6 outcome observations should preserve where practical:

* metric name
* observed value
* unit
* explanatory note

Future versions may add:

* observation source
* timestamp per measurement
* experiment-run identifier
* external artifact reference
* operator
* provenance chain

These are not required for the minimal Phase 6 model unless implementation need appears.

---

# Comparison Direction

Phase 6 may provide deterministic helpers for simple comparison.

Examples:

```text
target = 15
observed = 17
```

or:

```text
expected condition = "latency decreases"
observed = "latency decreased"
```

However, the system must not fabricate semantic certainty where a direct comparison is not possible.

---

# Outcome Feedback

Outcome feedback means making DecisionOutcome available to:

```text
memory
knowledge
future review
human or external LLM governance
```

It does not yet mean automatic strategy adaptation.

---

# Memory Boundary

Existing project memory is an archive.

Phase 6 may store DecisionOutcome records in memory or knowledge storage.

This does not convert memory into an autonomous learning system.

Mandatory terminology:

```text
Outcome History
Decision-Outcome History
Recorded Feedback
```

Preferred over:

```text
Learning Engine
Self-Learning Memory
Autonomous Adaptation
```

unless those capabilities are actually implemented later.

---

# Stabilization

Phase 6 also closes the Evidence & Decision Integrity Cycle.

After outcome integration, the Studio must undergo stabilization.

Stabilization includes:

```text
full software regression
semantic development regression
holdout integrity review
decision-outcome trace review
documentation review
Git clean checkpoint
```

No large new subsystem should be added during stabilization.

---

# Existing Holdout Integrity

The Phase 5 holdout suite remains a semantic milestone record.

If those holdout cases are later used directly to tune production behavior, they must no longer be described as pristine holdout.

Phase 6 must preserve that distinction.

---

# Required Invariants

Phase 6 requires at least the following:

```text
DecisionOutcome
→ traceable to Opportunity
```

```text
DecisionOutcome
→ traceable to PlanningResult
```

```text
DecisionOutcome
→ traceable to Decision
```

```text
Outcome observations
→ explicit, not invented
```

```text
NOT_OBSERVED
!=
SUCCESS
```

```text
FAILURE
→ preserved as valid history
```

```text
recorded outcome
!=
automatic learning
```

---

# Non-Goals

Phase 6 will not implement:

* reinforcement learning
* automatic threshold tuning
* self-modifying strategy
* autonomous policy generation
* statistical significance engine
* experiment execution infrastructure
* external telemetry ingestion platform
* new workers
* product analytics platform
* autonomous business optimization

---

# Phase 6 Implementation Order

Phase 6 will proceed in this order:

1. Outcome domain model
2. Outcome model tests
3. DecisionOutcome traceability
4. Basic expected-vs-observed comparison
5. Outcome persistence or knowledge integration
6. Outcome-history tests
7. Full software regression
8. Semantic development regression
9. Holdout integrity review
10. Documentation and stabilization review
11. Final cycle checkpoint

---

# Phase 6 Exit Criteria

Phase 6 is complete only when:

* OutcomeStatus exists.
* OutcomeObservation exists.
* DecisionOutcome exists.
* Outcome records are traceable to Opportunity.
* Outcome records are traceable to PlanningResult.
* Outcome records are traceable to the originating decision.
* Missing observations are represented honestly.
* Failure outcomes are preserved.
* Basic comparison behavior exists where deterministic comparison is possible.
* Outcome history is stored or otherwise preserved.
* No automatic-learning claim is introduced.
* Existing software regression passes.
* Semantic development suite passes.
* Holdout integrity is preserved.
* Documentation reflects current architecture.
* Git checkpoint is clean.

---

# Final Decision

AI-RD-Studio will close the decision loop by explicitly recording observed outcomes and linking them to the decisions and plans that produced them.

Outcome feedback will initially be treated as structured historical evidence for future review and governance.

It will not be treated as autonomous learning until such adaptation is separately designed, justified, and validated.


