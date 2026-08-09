Tamam. Önce **ROADMAP** belgesini sabitleyelim.

Aç:

```powershell
code docs\EVIDENCE_DECISION_INTEGRITY_ROADMAP.md
```

Dosyanın tamamını bununla değiştir:

````markdown
# Evidence & Decision Integrity Cycle Roadmap

Version: 0.1
Status: ACTIVE ROADMAP
Date: 2026-08-09

---

# Purpose

This roadmap defines the next development cycle of AI-RD-Studio after the stabilized v0.2.0 baseline and the post-freeze reality review.

The objective of this cycle is not to increase the number of workers or features.

The objective is to transform the Studio from a structurally connected R&D pipeline into an evidence-driven, causally connected, explainable decision system.

The central principle is:

> Do not make the Studio larger before making its decisions more trustworthy.

---

# Current Baseline

The current stable baseline is:

```text
AI-RD-Studio v0.2.0
84/84 software tests passing
Git baseline frozen
````

The current runtime includes:

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

The current architecture is preserved.

A rewrite is not part of this cycle.

---

# Current Problem

The v0.2.0 architecture is structurally sound, but the intelligence flowing through it is still incomplete.

The main gaps are:

* Research is primarily prose
* Evidence is not first-class structured data
* Source provenance is weak
* Research does not yet causally influence Strategy strongly enough
* Strategy scoring is still heuristic
* Hypotheses are not explicitly represented
* Planning is not yet experiment-oriented
* Validation is mostly structural
* Validation is not yet a real decision gate
* ACCEPT / DEFER / REJECT semantics are not fully consistent
* Software tests do not measure semantic decision quality
* Real-world outcomes do not yet close the learning loop

---

# Cycle Goal

At the end of this cycle, AI-RD-Studio should be able to:

1. Represent claims and evidence explicitly.
2. Track where evidence came from.
3. Separate supporting and contradictory evidence.
4. Represent uncertainty and confidence.
5. Ensure research evidence materially affects strategic evaluation.
6. Represent testable hypotheses.
7. Produce measurable experiment-oriented plans.
8. Use validation as an actual progression gate.
9. Distinguish decision states correctly.
10. Evaluate decision quality using semantic benchmark cases.
11. Preserve a more complete decision trace.
12. Define how observed real-world outcomes feed back into future reasoning.

---

# Core Success Invariant

The entire cycle is guided by this invariant:

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

If the Studio cannot demonstrate this reliably and explainably, the cycle is not complete.

---

# Phase 1 — Evidence & Provenance Foundation

Status: PLANNED

## Goal

Transform research output from prose-only analysis into structured evidence-bearing research.

## Problem

Current `ResearchResult` primarily carries:

```text
analysis: str
```

This is insufficient for an Evidence First system.

The Studio cannot reliably answer:

* What is being claimed?
* What evidence supports it?
* What evidence contradicts it?
* Where did the evidence come from?
* How trustworthy is the source?
* What remains uncertain?

## Required Concepts

The minimum evidence model should support:

* Claim
* Evidence
* Counter-evidence
* Source
* Provenance
* Confidence
* Uncertainty

The implementation must remain minimal.

No abstraction should be introduced without a concrete use in the active pipeline.

## Entry Criteria

* v0.2.0 baseline is clean and tested.
* Reality review is committed.
* Roadmap and cycle rules are accepted.

## Exit Criteria

Phase 1 is complete only when:

* ResearchResult can carry structured evidence.
* At least one claim can reference supporting evidence.
* Counter-evidence can be represented separately.
* Evidence has source/provenance information.
* Confidence or uncertainty can be represented.
* Existing deterministic research behavior remains backward compatible where required.
* Software regression suite passes.
* New Phase 1 tests pass.
* Git checkpoint is clean.

---

# Phase 2 — Research to Strategy Causal Link

Status: PLANNED

## Goal

Make Strategy materially dependent on research evidence.

## Problem

Current Strategy behavior can produce similar evaluations despite contradictory research because the research analysis is not meaningfully consumed.

## Required Behavior

Strategy must consider:

* Supporting evidence
* Counter-evidence
* Evidence strength
* Confidence
* Uncertainty
* Risk indicators

The existing title-based AI heuristic must no longer be the primary driver of strategic evaluation.

## Core Test

```text
Same Signal

Research A:
Strong credible supporting evidence

Research B:
Strong credible contradictory evidence

Expected:
Different Opportunity evaluation
and/or
Different Decision trajectory
```

## Exit Criteria

Phase 2 is complete only when:

* Strategy consumes structured research evidence.
* Opposing credible evidence can lower or alter evaluation.
* Supporting credible evidence can increase evaluation.
* The decision path is not determined by the presence of keywords such as "AI".
* The causal behavior is covered by tests.
* Regression suite passes.
* Git checkpoint is clean.

---

# Phase 3 — Hypothesis, Experiment and Decision Semantics

Status: PLANNED

## Goal

Move from opportunity scoring toward testable R&D reasoning.

## Required Concepts

The Studio should be able to represent:

* Hypothesis
* Assumption
* Experiment
* Success criterion
* Failure criterion
* Measurement
* Stop condition

The exact object model must remain minimal.

## Planning Requirement

Planning should become tied to:

* What is being tested
* Why it matters
* What evidence would confirm it
* What evidence would falsify it
* How success will be measured

## Decision Semantics

The following states must remain distinct:

* ACCEPT
* DEFER
* REJECT

If additional states are introduced, such as:

* RESEARCH_MORE
* REVISE_PLAN

they require an explicit architectural decision.

## Exit Criteria

Phase 3 is complete only when:

* At least one testable hypothesis can be represented.
* A plan can state what is being tested.
* Success/failure criteria can be expressed.
* ACCEPT, DEFER and REJECT are semantically distinct in summaries and tests.
* `DEFER` is not silently counted as `REJECT`.
* Regression suite passes.
* Git checkpoint is clean.

---

# Phase 4 — Validation as a Real Decision Gate

Status: PLANNED

## Goal

Transform Validation from structural checking into a real progression gate.

## Validation Dimensions

The design should evaluate at least:

* Structural completeness
* Evidence sufficiency
* Consistency
* Risk awareness
* Measurability
* Feasibility
* Traceability
* Confidence
* Stop condition

Not every dimension must become a complex scoring subsystem.

The implementation should remain minimal and explicit.

## Mandatory Invariant

```text
Failed Validation
cannot silently produce
ACCEPT
```

## Exit Criteria

Phase 4 is complete only when:

* Validation result affects runtime control flow.
* Invalid or insufficiently supported plans cannot proceed as ACCEPT.
* Validation reasons are explicit.
* Validation failure paths are covered by integration tests.
* Regression suite passes.
* Git checkpoint is clean.

---

# Phase 5 — Semantic Evaluation Suite

Status: PLANNED

## Goal

Separate software correctness from decision-quality evaluation.

## Principle

```text
Software Tests
!=
AI / Decision Evaluation
```

Pytest remains responsible for:

* Contracts
* Runtime behavior
* Failure handling
* Persistence
* Regression

A separate semantic evaluation suite will test:

* Research quality
* Evidence sensitivity
* Decision consistency
* Contradictory evidence handling
* Risk handling
* Insufficient evidence behavior
* Misleading labels
* Confidence calibration

## Initial Benchmark Cases

At minimum, include fixed cases for:

1. Strong opportunity with strong evidence
2. Strong-looking opportunity with weak evidence
3. Opportunity contradicted by strong evidence
4. High-risk opportunity
5. Insufficient evidence
6. Strong non-AI opportunity
7. Misleading AI-labelled opportunity
8. Conflicting sources
9. Validation failure
10. DEFER case

## Exit Criteria

Phase 5 is complete only when:

* Semantic evaluation is separate from unit/regression tests.
* Fixed benchmark cases exist.
* Expected decision behavior is documented.
* Evidence sensitivity is measurable.
* Decision regressions can be detected independently of Python correctness.
* Git checkpoint is clean.

---

# Phase 6 — Outcome Feedback and Stabilization

Status: PLANNED

## Goal

Define and stabilize the first real outcome-feedback loop.

## Problem

The current system approximately ends at:

```text
Decision
→ Task
→ Knowledge
```

A mature R&D system needs:

```text
Decision
↓
Execution
↓
Observed Result
↓
Measurement
↓
Comparison
↓
Learning Record
```

## Required Design

The Studio should be able to preserve:

* What decision was made
* What outcome was expected
* What actually happened
* What was measured
* Whether the hypothesis was supported
* Whether the decision was good or poor
* What should be learned from the result

This phase does not require autonomous self-learning.

Outcome storage and explicit feedback are sufficient for this cycle.

## Stabilization Tasks

Before cycle completion:

* Persistent trace must be reviewed.
* Planning and validation persistence gaps must be addressed if still relevant.
* Security trust boundaries must be reviewed.
* Documentation must distinguish implemented, planned and vision.
* Software tests must pass.
* Semantic evaluation must pass according to agreed criteria.
* Final architecture review must be performed.

## Exit Criteria

Phase 6 is complete only when:

* Outcome feedback has a defined model.
* At least one end-to-end case connects decision to observed outcome.
* Full decision trace can be reconstructed.
* Trust-boundary review is complete.
* Documentation is synchronized.
* Software regression suite passes.
* Semantic evaluation baseline is recorded.
* Final Git checkpoint is clean.
* Mandatory STOP / REVIEW is performed.

---

# Explicit Non-Goals

The following are outside this cycle:

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

These may only be reconsidered after this cycle and a new review.

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

AI-RD-Studio may increasingly automate bounded R&D work, but full autonomy is not the current objective.

---

# Long-Term Context

AI-RD-Studio is the current concrete project.

A future broader Studio family may eventually emerge for:

* Scientific research
* Product discovery
* Engineering R&D
* Other research and decision workflows

This is vision only.

The current architecture must not be prematurely generalized around hypothetical future variants.

---

# Cycle Completion Definition

The cycle is not complete because:

* More code exists
* More workers exist
* More tests exist
* More autonomy exists

The cycle is complete when:

> The Studio can demonstrate that trustworthy evidence changes its reasoning and decisions in explainable, testable and traceable ways.

---

# STOP / REVIEW Rule

After Phase 6:

STOP.

Do not automatically begin another expansion cycle.

Perform a new external review first.

The next cycle must be justified by real capability gaps observed in the evidence-driven Studio.


