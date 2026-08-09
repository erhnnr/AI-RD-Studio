# Evidence & Decision Integrity Cycle Roadmap

Version: 1.0
Status: COMPLETE — FROZEN
Date: 2026-08-09

---

# Purpose

This roadmap defines the Evidence & Decision Integrity development cycle of AI-RD-Studio after the stabilized v0.2.0 baseline and the post-freeze reality review.

The objective of this cycle was not to increase the number of workers or features.

The objective was to transform the Studio from a structurally connected R&D pipeline into an evidence-driven, causally connected, explainable decision system.

The central principle is:

> Do not make the Studio larger before making its decisions more trustworthy.

---

# Historical Baseline

The cycle started from:

```text
AI-RD-Studio v0.2.0
84/84 software tests passing
Git baseline frozen
````

The baseline runtime included:

* ResearchWorker
* StrategyWorker
* PlanningWorker
* ValidationWorker
* WorkerRegistry
* RuntimeGuard
* ReviewBoard
* TaskManager
* KnowledgeWriter
* Project-level execution
* Persistent project history
* LM Studio research provider boundary

The architecture was preserved.

A rewrite was not part of this cycle.

---

# Baseline Problem

At cycle start, the v0.2.0 architecture was structurally sound, but the intelligence flowing through it was incomplete.

The main gaps were:

* Research was primarily prose.
* Evidence was not first-class structured data.
* Source provenance was weak.
* Research did not causally influence Strategy strongly enough.
* Strategy scoring was heuristic.
* Hypotheses were not explicitly represented.
* Planning was not experiment-oriented.
* Validation was mostly structural.
* Validation was not a real decision gate.
* ACCEPT / DEFER / REJECT semantics were not fully consistent.
* Software tests did not measure semantic decision quality.
* Real-world outcomes did not close the decision-feedback loop.

These gaps defined the Evidence & Decision Integrity Cycle.

---

# Cycle Goal

The cycle required AI-RD-Studio to become able to:

1. Represent claims and evidence explicitly.
2. Track where evidence came from.
3. Separate supporting and contradictory evidence.
4. Represent uncertainty and confidence.
5. Ensure research evidence materially affects strategic evaluation.
6. Represent testable hypotheses.
7. Produce measurable experiment-oriented plans.
8. Use validation as an actual progression gate.
9. Distinguish decision states correctly.
10. Evaluate decision behavior using semantic benchmark cases.
11. Preserve a more complete decision trace.
12. Record observed outcomes without falsely claiming autonomous learning.

Status:

```text
ACHIEVED WITHIN THE DECLARED CYCLE SCOPE
```

---

# Core Success Invariant

The entire cycle was guided by this invariant:

```text
Same Signal
+
Strong Supporting Evidence
=
Materially Different Evaluation

than

Same Signal
+
Strong Contradictory Evidence
=
Materially Different Evaluation
```

This invariant is now covered by causal and semantic tests.

---

# Phase 1 — Evidence & Provenance Foundation

Status: COMPLETE

## Goal

Transform research output from prose-only analysis into structured evidence-bearing research.

## Problem

At cycle start, `ResearchResult` primarily carried:

```text
analysis: str
```

This was insufficient for an Evidence First system.

The Studio needed to answer:

* What is being claimed?
* What evidence supports it?
* What evidence contradicts it?
* Where did the evidence come from?
* How strong is the represented evidence?
* What remains uncertain?

## Implemented Concepts

The minimum evidence model now supports:

* Claim
* Evidence
* Counter-evidence
* EvidenceSource
* Provenance
* Confidence
* Uncertainty

The implementation remains intentionally minimal.

Signal-derived evidence is explicitly treated as unverified input evidence rather than independent verification.

## Exit Criteria

* ResearchResult can carry structured evidence. — PASS
* At least one claim can reference supporting evidence. — PASS
* Counter-evidence can be represented separately. — PASS
* Evidence has source/provenance information. — PASS
* Confidence and uncertainty can be represented. — PASS
* Backward compatibility is preserved where required. — PASS
* Software regression suite passes. — PASS
* Phase 1 tests pass. — PASS
* Git checkpoint completed. — PASS

Phase 1:

```text
COMPLETE
```

---

# Phase 2 — Research to Strategy Causal Link

Status: COMPLETE

## Goal

Make Strategy materially dependent on research evidence.

## Required Behavior

Strategy considers structured research evidence including:

* Supporting evidence
* Counter-evidence
* Evidence strength
* Confidence
* Uncertainty

The title-based `"AI"` heuristic is not the primary strategic driver.

## Core Invariant

```text
Same Signal

Research A:
Strong supporting evidence

Research B:
Strong contradictory evidence

Expected:
Materially different Opportunity evaluation
and materially different decision trajectory
```

The system now distinguishes:

```text
SUPPORTING
INSUFFICIENT
MIXED
CONTRADICTORY
```

Evidence state affects Opportunity evaluation and downstream decisions.

## Exit Criteria

* Strategy consumes structured research evidence. — PASS
* Opposing evidence alters evaluation. — PASS
* Supporting evidence alters evaluation. — PASS
* `"AI"` keyword does not determine strategic value. — PASS
* Causal behavior is covered by tests. — PASS
* Causal Integrity Gate passes. — PASS
* Regression suite passes. — PASS
* Git checkpoint completed. — PASS

Phase 2:

```text
COMPLETE
```

---

# Phase 3 — Hypothesis, Experiment and Decision Semantics

Status: COMPLETE

## Goal

Move from opportunity scoring toward testable R&D reasoning.

## Implemented Concepts

The Studio now represents:

* Hypothesis
* Assumption
* Experiment
* Success criterion
* Failure criterion
* Measurement
* Stop condition

Planning is tied to:

* What is being tested
* Why it matters
* What would support the hypothesis
* What would challenge it
* How an experiment may be structured
* How outcomes may be measured

Planning remains intentionally domain-agnostic at this stage.

## Decision Semantics

The following states remain distinct:

* ACCEPT
* DEFER
* REJECT

Mandatory invariant:

```text
DEFER != REJECT
```

No additional decision states were introduced without an architectural decision.

## Exit Criteria

* Testable hypotheses can be represented. — PASS
* Plans state what is being tested. — PASS
* Success/failure criteria can be expressed. — PASS
* ACCEPT, DEFER and REJECT remain distinct. — PASS
* DEFER is not counted as REJECT. — PASS
* Regression suite passes. — PASS
* Git checkpoint completed. — PASS

Phase 3:

```text
COMPLETE
```

---

# Phase 4 — Validation as a Real Decision Gate

Status: COMPLETE

## Goal

Transform Validation from structural checking into a real progression gate.

## Implemented Validation Behavior

Validation checks whether the controlled planning path is suitable for progression.

It evaluates declared conditions including:

* Evidence state
* Hypothesis presence
* Success criteria
* Failure criteria
* Experiment definition
* Measurement presence
* Stop conditions

Validation remains bounded to the implemented Studio decision model.

It is not described as real-world product validation.

## Mandatory Invariant

```text
Failed Validation
cannot silently produce
ACCEPT
```

This invariant is enforced in runtime control flow.

If validation blocks progression:

* ReviewBoard acceptance is not allowed.
* The result becomes DEFER or REJECT according to explicit policy.
* No task is created.

## Exit Criteria

* Validation result affects runtime control flow. — PASS
* Invalid plans cannot silently proceed as ACCEPT. — PASS
* Validation reasons are explicit. — PASS
* Validation failure paths are integration tested. — PASS
* Regression suite passes. — PASS
* Git checkpoint completed. — PASS

Phase 4:

```text
COMPLETE
```

---

# Phase 5 — Semantic Evaluation Suite

Status: COMPLETE

## Goal

Separate software correctness from decision-quality evaluation.

## Principle

```text
Software Tests
!=
Semantic / Decision Evaluation
```

Pytest remains responsible for:

* Contracts
* Runtime behavior
* Failure handling
* Persistence
* Regression

A separate semantic evaluation structure tests decision behavior such as:

* Evidence sensitivity
* Decision consistency
* Contradictory evidence handling
* Insufficient evidence
* Misleading labels
* Strong non-AI evidence
* Persuasive wording without sufficient evidence
* End-to-end semantic consistency

## Development Semantic Suite

Current recorded baseline:

```text
9 / 9 PASS
```

## Holdout / Adversarial Suite

A separate holdout suite was created after development semantic cases.

Initial first-run holdout result:

```text
5 / 5 PASS
```

No production tuning was performed against those cases before that first result.

Subsequent execution is treated as regression evidence.

If future production behavior is tuned directly against these cases, they must no longer be described as pristine holdout cases.

## Exit Criteria

* Semantic evaluation is separate from ordinary software tests. — PASS
* Fixed semantic cases exist. — PASS
* Expected decision behavior is documented in tests. — PASS
* Evidence sensitivity is measurable. — PASS
* Decision regressions can be detected separately from ordinary Python correctness. — PASS
* Holdout / Adversarial Evaluation Gate passed. — PASS
* Git checkpoint completed. — PASS

Phase 5:

```text
COMPLETE
```

---

# Phase 6 — Outcome Feedback and Stabilization

Status: COMPLETE

## Goal

Define and stabilize the first real bounded outcome-feedback loop.

## Implemented Outcome Flow

The Studio now supports:

```text
Pipeline Decision
↓
Observed Outcome
↓
Measurement
↓
Deterministic Comparison when justified
↓
Persistent Outcome History
```

This is outcome feedback.

It is not autonomous self-learning.

## Outcome Model

The implemented model includes:

* OutcomeStatus
* OutcomeObservation
* DecisionOutcome

Supported outcome states include:

```text
SUCCESS
FAILURE
PARTIAL
INCONCLUSIVE
NOT_OBSERVED
```

The Studio does not invent observed results.

If no observation exists:

```text
NOT_OBSERVED
```

If an observation exists but a deterministic success/failure judgment is not justified:

```text
INCONCLUSIVE
```

remains valid.

## Measurement Semantics

Measurements now support explicit target direction:

```text
AT_LEAST
AT_MOST
EXACT
```

The Studio does not infer whether higher or lower values are desirable from metric names.

If the target semantics are insufficient:

```text
NOT_COMPARABLE
```

is returned rather than inventing a judgment.

## Persistent Decision Trace

The persistent trace can preserve:

```text
Signal
↓
Research
↓
Claim
↓
Evidence / Counter-evidence
↓
Source / Provenance
↓
Opportunity
↓
Hypothesis
↓
Experiment
↓
Measurement
↓
Validation
↓
Decision
↓
Outcome
```

Pipeline execution records now include a trace identifier that can link an observed DecisionOutcome back to the originating execution.

Unknown execution trace references are rejected.

## Trust Boundary Review

A final trust-boundary review was recorded in:

```text
docs/PHASE_6_STABILIZATION_REVIEW.md
```

Key boundaries reviewed include:

* Signal input
* ResearchProvider / LLM output
* Structured evidence
* Strategy
* Validation
* Decision-to-task progression
* Observed outcomes
* Persistent memory
* External governance

Review result:

```text
PASS
```

Important limitation:

Structural validation and evidence representation do not prove factual real-world truth.

The current ResearchProvider does not independently verify external facts.

## Stabilization Results

Semantic development suite:

```text
9 / 9 PASS
```

Holdout regression:

```text
5 / 5 PASS
```

Full software regression suite:

```text
244 / 244 PASS
```

## Exit Criteria

* Outcome feedback has a defined model. — PASS
* At least one end-to-end case connects decision to observed outcome. — PASS
* Full bounded decision trace can be reconstructed. — PASS
* Trust-boundary review is complete. — PASS
* Documentation is synchronized. — PASS
* Software regression suite passes. — PASS
* Semantic evaluation baseline is recorded. — PASS
* Final Git checkpoint is required immediately after this document update. — PENDING FINAL CHECKPOINT
* Mandatory STOP / REVIEW is performed. — PASS

Phase 6 technical and architectural work:

```text
COMPLETE
```

Only the final clean Git checkpoint remains before the cycle is formally frozen.

---

# Explicit Non-Goals

The following were outside this cycle and remain unimplemented unless separately reviewed:

* New worker proliferation
* EngineeringWorker
* ProductWorker
* Autonomous internet crawling
* Continuous autonomous operation
* Dynamic worker generation
* Agent swarms
* Parallel orchestration
* Distributed orchestration
* Recursive self-improvement
* Fully autonomous company behavior
* Premature generic Studio abstraction

Their absence does not represent a failure of this cycle.

They may only be reconsidered after the mandatory post-cycle external review.

---

# Human and External LLM Governance

The Studio remains governed from outside.

Current intended model:

```text
Human Principal
      +
External Strategic LLM
      |
      v
AI-RD-Studio
```

The Human Principal and external LLM may:

* Give direction
* Request research
* Challenge conclusions
* Review high-impact decisions
* Approve or reject progression
* Define discovery criteria

AI-RD-Studio may perform increasingly bounded R&D work.

Full autonomy is not the current objective.

---

# Long-Term Context

AI-RD-Studio is the current concrete project.

A future broader Studio family may eventually emerge for:

* Scientific research
* Product discovery
* Engineering R&D
* Other research and decision workflows

This remains vision only.

The current architecture must not be prematurely generalized around hypothetical future variants.

---

# Cycle Completion Definition

The cycle is not complete because:

* More code exists
* More workers exist
* More tests exist
* More autonomy exists

The cycle is complete because the Studio can now demonstrate that evidence changes its reasoning and decisions in explainable, testable and traceable ways within the implemented scope.

The cycle now provides:

```text
Evidence
↓
Causal Strategy
↓
Testable Hypothesis
↓
Experiment-oriented Planning
↓
Validation Authority
↓
Explicit Decision Semantics
↓
Semantic Evaluation
↓
Outcome Traceability
```

---

# Evaluation Checkpoints

## Phase 2 — Causal Integrity Gate

Result:

```text
PASS
```

Materially different credible evidence produces materially different evaluation and decision trajectories.

---

## Phase 5 — Holdout / Adversarial Evaluation Gate

Initial holdout result:

```text
5 / 5 PASS
```

Development and holdout cases remain conceptually separated.

The initial holdout result was obtained without production tuning against those holdout cases.

---

# Final Cycle Verification

Recorded final verification before freeze:

```text
Semantic Development:
9 / 9 PASS

Holdout Regression:
5 / 5 PASS

Full Software Regression:
244 / 244 PASS
```

Software correctness, semantic decision behavior, and real-world outcome success remain separate claims.

---

# Known Limitations at Cycle Close

The cycle closes with explicit limitations:

1. LLM / ResearchProvider output is not independently verified real-world research.
2. Evidence confidence is a bounded system representation, not objective truth.
3. Strategy thresholds remain deterministic scaffolding rather than learned truth.
4. Planning remains domain-agnostic.
5. Some measurements may legitimately be NOT_COMPARABLE.
6. Some outcomes may legitimately remain INCONCLUSIVE.
7. Outcome history is not autonomous learning.
8. Persistent memory does not automatically alter future decisions.
9. No engineering/prototype execution layer exists yet.
10. No continuous autonomous Studio operation exists.
11. Semantic tests demonstrate behavior within tested scenarios, not general intelligence.
12. Real-project validation remains necessary before claims about practical end-to-end Studio effectiveness.

These limitations are preserved for the mandatory external reality review.

---

# STOP / REVIEW Rule

After the final Git checkpoint:

```text
EVIDENCE & DECISION INTEGRITY CYCLE COMPLETE
↓
FREEZE
↓
STOP
```

Do not automatically begin another expansion cycle.

Do not automatically add:

* New workers
* New tools
* More autonomy
* More architectural layers

Perform a new external reality review first.

The next development cycle must be justified by concrete capability gaps relative to the intended final AI-RD-Studio.

---

# Final Status

Phases:

```text
Phase 1 — Evidence & Provenance Foundation          COMPLETE
Phase 2 — Research → Strategy Causal Link           COMPLETE
Phase 3 — Hypothesis / Experiment / Semantics       COMPLETE
Phase 4 — Validation as a Real Decision Gate        COMPLETE
Phase 5 — Semantic Evaluation Suite                 COMPLETE
Phase 6 — Outcome Feedback + Stabilization          COMPLETE
```

Cycle status:

```text
TECHNICAL WORK COMPLETE
FINAL GIT CHECKPOINT PENDING
```

After the clean Git checkpoint:

```text
CYCLE COMPLETE — FROZEN
```

---

# Final Principle

> Improve the trustworthiness of Studio decisions before increasing the size or autonomy of the Studio.


