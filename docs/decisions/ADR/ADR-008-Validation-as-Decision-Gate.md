Tamam. Phase 4’ü açıyoruz: **Validation as a Real Decision Gate**.

Burada en kritik değişiklik şu olacak:

```text
Bugün:
ValidationResult.valid = False
ama pipeline yine ReviewBoard'a gidip ACCEPT üretebilir.

Phase 4 sonunda:
Validation FAIL
→ ACCEPT mümkün değil.
```

Bu artık sadece validation mantığı değil, **runtime control-flow authority** meselesi. O yüzden ilk adım ADR.

Aç:

```powershell
code docs\decisions\ADR\ADR-008-Validation-as-Decision-Gate.md
```

Dosyanın tamamı şu olsun:

````markdown
# ADR-008 — Validation as a Decision Gate

Status: Accepted
Date: 2026-08-09
Cycle: Evidence & Decision Integrity
Phase: 4 — Validation as a Real Decision Gate

---

# Context

AI-RD-Studio currently contains:

- Research
- Structured evidence
- Evidence-aware Strategy
- Evidence-aware ReviewBoard
- Hypothesis
- Experiment
- Measurement
- Contextual Planning

The current runtime approximately follows:

```text
Signal
↓
Research
↓
Strategy
↓
Planning
↓
Validation
↓
ReviewBoard
↓
Decision
````

However, Validation does not yet have authoritative control over progression.

A ValidationResult may indicate:

```text
valid = False
```

while downstream ReviewBoard logic can still produce an ACCEPT decision.

This violates the Validation Driven principle.

---

# Problem

Validation currently behaves primarily as information.

It does not yet function as a runtime gate.

The Studio therefore cannot guarantee the following property:

```text
Invalid Plan
→ cannot progress
```

Phase 4 must establish this guarantee.

---

# Decision

ValidationResult will become an authoritative progression gate.

The runtime will preserve the sequence:

```text
Planning
↓
Validation
↓
Validation Gate
↓
Review Decision
```

but a failed ValidationResult must constrain the possible downstream decisions.

Mandatory invariant:

```text
ValidationResult.valid == False
→ ACCEPT is impossible
```

---

# Validation Responsibility

Validation must evaluate whether the current R&D plan is sufficiently well-formed to justify progression.

Phase 4 validation should consider at least:

* Planning structure
* Evidence sufficiency
* Hypothesis presence
* Success criteria
* Failure criteria
* Experiment presence
* Measurement presence
* Stop conditions
* Basic internal consistency
* Traceability to the Opportunity

Validation does not prove real-world success.

---

# Structural Validation vs R&D Validation

The Studio must distinguish:

```text
Structural validation
```

from:

```text
R&D progression validation
```

Structural validation asks:

* Is the required object present?
* Is the expected type present?
* Are mandatory fields populated?

R&D progression validation asks:

* Is there enough evidence to justify the plan?
* Is the hypothesis testable?
* Can the plan fail?
* Is something observable being measured?
* Are stop conditions defined?

Phase 4 will begin combining both levels conservatively.

---

# Evidence Sufficiency

Validation must not ignore evidence state.

At minimum:

```text
CONTRADICTORY
→ progression validation fails
```

and:

```text
INSUFFICIENT
→ progression validation fails
```

unless a future explicit workflow distinguishes a research-only recovery path.

For Phase 4, unsupported progression must not be accepted.

---

# Mixed Evidence

MIXED evidence indicates unresolved contradiction.

Default Phase 4 behavior:

```text
MIXED
→ validation fails for progression
```

The opportunity may later return to research.

It must not silently proceed as confidently validated.

---

# Supporting Evidence

SUPPORTING evidence is necessary for evidence-aware progression.

However:

```text
SUPPORTING
!=
automatically valid
```

The plan must still contain an adequate hypothesis and experiment structure.

---

# Hypothesis Requirements

A valid progression plan must include a Hypothesis.

The Hypothesis must contain:

* Non-empty statement
* At least one success criterion
* At least one failure criterion

Assumptions may be present and should remain inspectable.

A hypothesis that cannot fail is not sufficient for progression.

---

# Experiment Requirements

A valid progression plan must include an Experiment.

The Experiment must contain:

* Non-empty objective
* Non-empty method
* At least one Measurement
* At least one stop condition

---

# Measurement Requirements

A Measurement must identify an observable metric.

Phase 4 does not require every Measurement to already contain:

* baseline
* target
* unit

because some exploratory R&D experiments may establish those values.

However, the metric itself must be explicit.

---

# Stop Conditions

At least one explicit stop condition is required.

A plan without a stop condition risks uncontrolled continuation and is not considered sufficiently bounded.

---

# Internal Consistency

Validation should reject obvious contradictions such as:

* Missing hypothesis with an experiment
* Missing experiment with a hypothesis-driven plan
* Success criteria absent
* Failure criteria absent
* Measurement list empty
* Stop conditions empty

Phase 4 will not implement a general theorem prover or semantic consistency engine.

---

# Validation Result Semantics

ValidationResult continues to contain:

```text
valid
reason
```

Phase 4 may enrich the reason text but will not introduce unnecessary validation-score complexity.

The primary decision remains explicit:

```text
valid = True
```

or:

```text
valid = False
```

---

# Runtime Authority

The orchestrator must enforce ValidationResult.

The following behavior is forbidden:

```text
Validation FAIL
↓
ReviewBoard ACCEPT
```

The preferred Phase 4 direction is:

```text
Validation FAIL
→ progression blocked
→ non-ACCEPT decision
```

Exact DEFER/REJECT semantics will depend on the failure reason and must remain explicit.

---

# Failure Decision Direction

Validation failure caused by insufficient or unresolved information should generally result in:

```text
DEFER
```

Examples:

* insufficient evidence
* mixed evidence
* incomplete measurement definition
* incomplete experiment structure

Validation failure caused by materially contradictory evidence may result in:

```text
REJECT
```

where appropriate.

The implementation must remain conservative.

---

# ReviewBoard Relationship

ReviewBoard remains responsible for strategic review.

Validation does not replace ReviewBoard.

The intended architecture is:

```text
Evidence
↓
Strategy
↓
Planning
↓
Validation Gate
↓
ReviewBoard
↓
Decision
```

Validation determines whether progression is allowed.

ReviewBoard determines whether an allowed opportunity should progress strategically.

---

# No Duplicate Intelligence

Validation must not duplicate StrategyWorker.

Validation should not recalculate:

* impact
* urgency
* feasibility
* strategic_fit

unless a future explicit architecture decision requires it.

Its responsibility is plan and progression validity.

---

# RuntimeGuard Relationship

RuntimeGuard remains responsible for structural runtime contracts.

ValidationWorker is responsible for domain-level plan validity.

Therefore:

```text
RuntimeGuard
!=
ValidationWorker
```

Both are required.

---

# Non-Goals

Phase 4 will not implement:

* Real-world outcome validation
* Statistical significance testing
* Autonomous experiment execution
* Source reputation engine
* Risk engine
* Product approval
* New workers
* Self-learning
* Dynamic validation policy generation

---

# Required Invariants

The following properties are mandatory:

```text
Validation FAIL
→ ACCEPT impossible
```

```text
Missing Hypothesis
→ progression invalid
```

```text
Missing Failure Criteria
→ progression invalid
```

```text
Missing Experiment
→ progression invalid
```

```text
Missing Measurement
→ progression invalid
```

```text
Missing Stop Condition
→ progression invalid
```

```text
CONTRADICTORY evidence
→ progression invalid
```

```text
INSUFFICIENT evidence
→ progression invalid
```

---

# Phase 4 Implementation Order

Phase 4 will proceed in this order:

1. Validation policy design
2. ValidationWorker domain checks
3. Validation tests
4. Runtime validation-gate integration
5. Orchestrator decision propagation tests
6. Validation-failure branch tests
7. Full regression
8. Phase 4 exit review

---

# Phase 4 Exit Criteria

Phase 4 is complete only when:

* ValidationWorker evaluates hypothesis presence.
* ValidationWorker evaluates success criteria.
* ValidationWorker evaluates failure criteria.
* ValidationWorker evaluates experiment presence.
* ValidationWorker evaluates measurements.
* ValidationWorker evaluates stop conditions.
* ValidationWorker considers evidence state.
* Validation failure affects runtime control flow.
* Validation failure cannot produce ACCEPT.
* Failure reasons remain explicit.
* Existing regression suite passes.
* Git checkpoint is clean.

---

# Final Decision

AI-RD-Studio Validation will become an authoritative progression gate.

Validation will not replace Strategy or ReviewBoard.

Its responsibility is to ensure that unsupported, untestable, unmeasurable, or internally incomplete R&D plans cannot silently progress as accepted decisions.
