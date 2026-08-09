Tamam. Phase 5’i açıyoruz: **Semantic Evaluation Suite**.

Buradaki amaç artık “kod çalışıyor mu?” değil:

> **Aynı anlamı taşıyan ama farklı şekilde sunulan girdilerde sistem tutarlı mı; gerçekten ilgili evidence değiştiğinde karar değişiyor mu; irrelevant wording sistemi yanıltıyor mu?**

İlk adım yine ADR. Aç:

```powershell
code docs\decisions\ADR\ADR-009-Semantic-Evaluation-and-Holdout-Policy.md
```

Dosyanın tamamını bununla değiştir:

````markdown
# ADR-009 — Semantic Evaluation and Holdout Policy

Status: Accepted
Date: 2026-08-09
Cycle: Evidence & Decision Integrity
Phase: 5 — Semantic Evaluation Suite

---

# Context

AI-RD-Studio now has:

- Structured Evidence
- Evidence Assessment
- Evidence-sensitive Strategy
- Evidence-aware ReviewBoard
- Hypothesis and Experiment models
- Contextual Planning
- Validation as an authoritative progression gate

The software architecture is increasingly reliable.

However, software correctness is not the same as semantic decision quality.

A pipeline can pass all structural tests and still behave poorly when:

- wording changes without meaning changing
- irrelevant labels are added
- contradictory evidence is injected
- persuasive prose is present without strong evidence
- equivalent evidence is expressed differently
- evidence changes in ways that should materially affect the decision

Phase 5 must evaluate these behaviors explicitly.

---

# Problem

The existing test suite primarily verifies:

```text
software contracts
runtime behavior
type safety
control flow
regression safety
````

These tests are necessary but insufficient.

They do not fully answer:

```text
Does the Studio respond to meaning rather than superficial wording?
```

or:

```text
Does relevant evidence causally affect the resulting decision?
```

Phase 5 therefore introduces a separate semantic evaluation layer.

---

# Decision

AI-RD-Studio will distinguish at least three evaluation categories:

```text
1. Software Correctness
2. Semantic Decision Quality
3. Real-World Outcome Quality
```

Phase 5 addresses category 2.

Real-world outcome quality remains Phase 6 and beyond.

---

# Evaluation Separation

Software tests remain under the normal test suite.

Semantic evaluations must be conceptually distinct from ordinary unit tests.

They may still use pytest for execution, but their purpose and organization must remain explicit.

Recommended structure:

```text
tests/
    ...
    semantic/
        development/
        holdout/
```

The exact directory layout may evolve, but development and holdout cases must remain separated.

---

# Development Cases

Development semantic cases are visible during implementation.

They may be used to:

* debug logic
* improve decision behavior
* refine deterministic rules
* verify invariants
* identify semantic regressions

Because they are visible and used during development, they are not pristine holdout evidence.

---

# Holdout Cases

Holdout cases are reserved for final or milestone evaluation.

They must not be used as ordinary tuning targets.

Mandatory rule:

```text
If a holdout case is inspected and used to tune behavior,
it is no longer pristine holdout.
```

Once exposed as a tuning target, it must be moved or treated as a development case.

A new unseen holdout must replace it for future unbiased evaluation.

---

# Core Semantic Invariants

Phase 5 must evaluate at least the following invariants.

---

# 1. Evidence Causality

For the same underlying opportunity:

```text
strong supporting evidence
>
insufficient evidence
>
strong contradictory evidence
```

in progression eligibility.

The system must react to relevant evidence changes.

---

# 2. Label Invariance

Irrelevant labels must not dominate decision behavior.

Example:

```text
"AI opportunity"
```

must not receive an advantage solely because the title contains "AI".

Equivalent evidence should produce equivalent evaluation regardless of superficial labels.

---

# 3. Wording Robustness

Semantically equivalent wording should not materially alter the result.

Example:

```text
"Demand is increasing."
```

and:

```text
"Market demand shows sustained growth."
```

should not diverge merely because one sentence sounds more persuasive.

The system should respond to structured evidence, not rhetoric.

---

# 4. Contradiction Injection

Adding strong contradictory evidence to a previously supporting case must materially affect the assessment.

Expected direction:

```text
SUPPORTING
→ MIXED
or
→ CONTRADICTORY
```

depending on evidence strength.

The resulting opportunity and progression decision must reflect the change.

---

# 5. Weak-Evidence Resistance

Persuasive wording with weak evidence must not be treated as strong support.

Example:

```text
highly persuasive prose
+
weak evidence confidence
```

must remain:

```text
INSUFFICIENT
```

when the structured evidence does not meet the current deterministic thresholds.

---

# 6. Irrelevant Context Resistance

Adding irrelevant metadata or wording must not materially change evaluation.

Examples:

* buzzwords
* prestige language
* unrelated sector labels
* emotionally persuasive phrases
* formatting differences

unless they alter structured evidence itself.

---

# 7. Decision-Gate Consistency

Semantic evaluation must include downstream behavior.

It is not enough to test EvidenceAssessment alone.

Cases should verify where appropriate:

```text
Evidence
↓
Assessment
↓
Opportunity
↓
Planning
↓
Validation
↓
Review Decision
```

The final decision must remain consistent with the evidence state and validation rules.

---

# 8. Metamorphic Evaluation

Phase 5 will use metamorphic checks.

A metamorphic check changes one controlled dimension while preserving others.

Examples:

```text
same evidence + different title
```

```text
same signal + stronger counter-evidence
```

```text
same evidence + persuasive wording
```

```text
same semantic content + alternate phrasing
```

The expected relationship between outputs is defined in advance.

---

# No Hidden Tuning

The Studio must not be changed merely to make a specific benchmark case pass without a documented semantic reason.

Forbidden pattern:

```text
case fails
→ add special-case keyword rule
→ benchmark passes
```

unless the rule is independently justified by architecture and generalizes beyond the case.

---

# Deterministic Evaluation

The current semantic evaluation suite should remain deterministic where practical.

This supports:

* reproducibility
* debugging
* regression detection
* causal interpretation

LLM-as-judge evaluation may be explored later but is not required for Phase 5.

---

# Benchmark Metrics

Phase 5 may report simple metrics such as:

```text
cases passed
cases failed
invariant violations
holdout pass rate
```

However, metrics must not imply scientific calibration.

For example:

```text
9/10 semantic cases passed
```

means only that 9 of the defined cases satisfied their expected invariant.

It does not mean:

```text
90% intelligent
```

or:

```text
90% real-world accurate
```

---

# Holdout Integrity

Holdout integrity is mandatory.

Rules:

* Holdout cases must remain separate from development cases.
* Do not inspect expected outcomes during ordinary tuning when avoidable.
* Do not repeatedly optimize against the same exposed holdout.
* If a holdout becomes a tuning target, demote it to development.
* Replace compromised holdout cases before future milestone evaluation.

---

# Failure Interpretation

A semantic evaluation failure must be classified.

Possible categories include:

```text
logic defect
wrong invariant
test-design defect
threshold weakness
architecture limitation
insufficient model capability
expected Phase limitation
```

Not every failure automatically justifies a code change.

---

# Software Tests vs Semantic Evaluation

Mandatory distinction:

```text
Software tests answer:
"Does the implementation satisfy its contracts?"

Semantic evaluation answers:
"Does the system behave meaningfully under controlled semantic variation?"
```

Both are required.

Neither substitutes for the other.

---

# Real-World Outcome Boundary

Phase 5 does not prove that the Studio identifies successful real-world products, research directions, or investments.

That requires:

```text
observed external outcomes
```

which belong to Phase 6 and later.

---

# Phase 5 Development Evaluation Set

The development suite should include controlled cases covering:

* support vs contradiction
* support vs insufficiency
* irrelevant AI label
* persuasive wording with weak evidence
* contradiction injection
* equivalent evidence under alternate labels
* evidence-state propagation to validation
* validation-failure propagation to final decision
* DEFER vs REJECT distinction

Existing tests may be reused where their purpose clearly matches semantic evaluation.

---

# Phase 5 Holdout Evaluation Set

A separate small holdout set will be created only after the development semantic suite is stable.

Holdout cases should contain unseen combinations of:

* signal wording
* evidence strengths
* supporting evidence
* counter-evidence
* irrelevant labels
* mixed evidence patterns

Expected invariants must be defined before execution.

---

# Required Phase 5 Invariants

At minimum:

```text
Relevant evidence change
→ evaluation changes when it should
```

```text
Irrelevant wording change
→ evaluation remains stable
```

```text
Strong counter-evidence injection
→ progression weakens
```

```text
Weak evidence + persuasive prose
→ does not become strong support
```

```text
Equivalent evidence + different label
→ equivalent evaluation
```

```text
Validation FAIL
→ final ACCEPT impossible
```

```text
DEFER
!=
REJECT
```

---

# Non-Goals

Phase 5 will not implement:

* Real-world success prediction
* Statistical calibration
* Scientific benchmarking claims
* LLM-as-judge dependency
* New workers
* Autonomous experiment execution
* Source reputation engine
* Dynamic model selection
* Reinforcement learning
* Self-modifying decision rules

---

# Phase 5 Implementation Order

Phase 5 will proceed in this order:

1. Semantic evaluation policy
2. Development semantic test structure
3. Metamorphic evaluation cases
4. Contradiction-injection cases
5. Irrelevant-label and wording-invariance cases
6. End-to-end decision consistency cases
7. Development suite stabilization
8. Separate holdout case creation
9. Holdout execution
10. Phase 5 exit review

---

# Phase 5 Exit Criteria

Phase 5 is complete only when:

* Development semantic suite exists.
* Semantic tests are explicitly separated from ordinary unit tests.
* Metamorphic checks exist.
* Contradiction-injection evaluation exists.
* Label invariance is evaluated.
* Weak-evidence resistance is evaluated.
* Downstream decision consistency is evaluated.
* Holdout suite exists separately.
* Holdout cases were not used as ordinary tuning targets.
* Holdout results are recorded honestly.
* Full software regression suite passes.
* Git checkpoint is clean.

---

# Final Decision

AI-RD-Studio will treat semantic decision evaluation as a separate engineering discipline from software correctness.

Phase 5 will measure whether controlled changes in meaning and evidence produce appropriate decision changes, while irrelevant wording and labels do not dominate behavior.

Holdout cases will be protected from ordinary tuning so that milestone evaluation retains real diagnostic value.


