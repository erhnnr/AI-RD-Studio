Tamam. Sıradaki adım **ADR-005 — Evidence-to-Strategy Causal Model**.

Aç:

```powershell
code docs\decisions\ADR\ADR-005-Evidence-to-Strategy-Causal-Model.md
```

Dosyanın tamamı şu olsun:

````markdown
# ADR-005 — Evidence-to-Strategy Causal Model

Status: Accepted
Date: 2026-08-09
Cycle: Evidence & Decision Integrity
Phase: 2 — Research to Strategy Causal Link

---

# Context

AI-RD-Studio Phase 1 introduced a structured evidence model:

- EvidenceSource
- Evidence
- Claim
- Supporting evidence
- Counter-evidence
- Confidence
- Uncertainty

ResearchResult can now carry structured claims and evidence.

However, the current StrategyWorker does not meaningfully use that evidence.

Its present behavior primarily derives Opportunity values from Signal title text.

In particular, the presence of the word:

```text
AI
````

can cause a high strategic score regardless of the actual research evidence.

This violates the Evidence First principle and prevents the Studio from demonstrating causal reasoning.

The Phase 2 objective is therefore:

> Make materially different research evidence capable of producing materially different strategic evaluation.

---

# Problem

The following behavior is currently possible:

```text
Same Signal
+
Strong supporting evidence

and

Same Signal
+
Strong contradictory evidence
```

can produce the same Opportunity.

This means ResearchResult is structurally connected to StrategyWorker but not causally connected to strategic evaluation.

A second problem is that the existing Opportunity dimensions:

* impact
* urgency
* feasibility
* strategic_fit

do not explain why their numeric values were assigned.

A simple replacement such as:

```text
supporting evidence = +2
counter evidence = -2
```

would also be insufficient.

Evidence currently does not explicitly state which Opportunity dimension it supports.

Applying the same adjustment to every strategic dimension would create false precision.

---

# Decision

Phase 2 will introduce a minimal evidence assessment between ResearchResult and Opportunity evaluation.

Conceptually:

```text
ResearchResult
      ↓
Evidence Assessment
      ↓
Strategy Evaluation
      ↓
Opportunity
```

This assessment will describe the evidentiary state of the research.

It will not claim to determine the full strategic value of an opportunity.

---

# Evidence Assessment States

The minimum assessment states are:

```text
SUPPORTING
CONTRADICTORY
MIXED
INSUFFICIENT
```

Their meaning is:

## SUPPORTING

Available structured evidence materially supports the research claim and counter-evidence is not equally strong.

## CONTRADICTORY

Available counter-evidence materially challenges or outweighs supporting evidence.

## MIXED

Meaningful supporting and contradictory evidence both exist and neither clearly dominates.

## INSUFFICIENT

Evidence is absent, weak, or too uncertain to justify a stronger conclusion.

---

# EvidenceAssessment Responsibility

The evidence assessment may contain:

* state
* supporting_strength
* counter_strength
* confidence
* rationale

The assessment answers:

> What does the current research evidence say about support for this claim?

It does not answer:

> Is this business or research opportunity objectively good?

That remains the responsibility of later strategic reasoning.

---

# Strength Calculation

Phase 2 may use a minimal deterministic evidence-strength calculation.

The calculation must remain explainable.

Supporting strength should be derived from supporting Evidence confidence.

Counter strength should be derived from counter-evidence confidence.

No source-reputation engine will be introduced in Phase 2.

No hidden or arbitrary weighting system will be introduced.

If numeric aggregation is used, its purpose is ordering and comparison rather than claiming statistical certainty.

---

# Confidence Semantics

EvidenceAssessment confidence represents confidence in the assessment of the available evidence.

It does not represent the probability that the opportunity will succeed.

The Studio must not present this value as objective certainty.

---

# Strategy Baseline

The existing title-dependent strategic shortcut will be removed as the primary evaluation mechanism.

The presence of terms such as:

```text
AI
```

must not independently produce strategic advantage.

Phase 2 will begin from a neutral strategic baseline rather than a keyword-derived high score.

Conceptually:

```text
impact = neutral
urgency = neutral
feasibility = neutral
strategic_fit = neutral
```

Evidence may then influence evaluation in an explicit and bounded way.

---

# No False Dimensional Precision

Phase 2 must not pretend that generic evidence independently proves:

* impact
* urgency
* feasibility
* strategic_fit

unless the evidence model explicitly supports that distinction.

Therefore, evidence influence during Phase 2 must remain conservative.

The architecture may enrich Opportunity with evidence-related explanation without claiming that every strategic dimension has been independently proven.

---

# Opportunity Explainability

Opportunity should progressively expose why the evaluation was produced.

The minimum Phase 2 direction is to support evidence-related fields such as:

* evidence_state
* evidence_confidence
* rationale

These fields must be introduced in a backward-compatible way where possible.

Existing Opportunity scoring behavior used by other runtime components should not be broken without an explicit migration decision.

---

# Causal Integrity Invariant

Phase 2 must demonstrate the following:

```text
Same Signal
+
Strong Supporting Evidence
→ stronger evaluation trajectory

Same Signal
+
Strong Contradictory Evidence
→ weaker or more cautious evaluation trajectory
```

The preferred evaluation is relational.

Example:

```text
supporting_case.score
>
insufficient_case.score
>
contradictory_case.score
```

Exact magic numbers are not required.

---

# Irrelevant Change Invariant

The system must also demonstrate that irrelevant wording changes do not dominate strategic evaluation.

Example:

```text
AI Warehouse Optimizer
```

and:

```text
Warehouse Optimization System
```

with materially equivalent evidence should not receive dramatically different strategic treatment merely because of the term "AI".

---

# ResearchResult Requirement

When StrategyWorker receives a ResearchResult, it must meaningfully consume structured claims and evidence.

Merely extracting:

```text
research_result.signal
```

and ignoring:

```text
research_result.claims
```

does not satisfy Phase 2.

---

# Worker Scope

No new worker will be introduced.

Evidence assessment may be implemented as:

* a small core domain model
* deterministic helper logic used by StrategyWorker

The design must remain minimal.

A separate EvidenceAssessmentWorker is explicitly rejected.

---

# ReviewBoard Scope

ReviewBoard will not be changed at the start of Phase 2.

First, StrategyWorker must demonstrate that evidence produces materially different Opportunity evaluations.

After that, the existing ReviewBoard behavior will be observed.

If ReviewBoard collapses or destroys the evidence-driven distinction, a separate controlled change may be justified.

---

# Validation Scope

ValidationWorker is not part of Phase 2.

Validation authority remains a Phase 4 concern.

Phase 2 must not prematurely implement validation gating.

---

# Non-Goals

Phase 2 will not implement:

* Source reputation scoring
* Web verification
* Fact checking
* Bayesian inference
* Machine-learned strategic scoring
* Dynamic weighting
* New workers
* Validation gating
* Outcome feedback
* Autonomous research
* Product execution

---

# Alternatives Considered

## Keep Existing AI Keyword Heuristic

Rejected.

A keyword is not evidence of strategic value.

It causes superficial labels to dominate reasoning.

---

## Add Fixed Bonus for Every Evidence Item

Rejected.

Evidence count does not equal evidence quality.

Ten weak items must not automatically outweigh one strong contradictory item.

---

## Apply Evidence Equally to All Opportunity Dimensions

Rejected.

The current evidence model does not identify whether a piece of evidence concerns impact, urgency, feasibility, or strategic fit.

Doing so would create false precision.

---

## Introduce a New Evidence Worker

Rejected.

The current cycle explicitly forbids worker expansion.

The requirement can be satisfied with domain logic and the existing StrategyWorker.

---

# Consequences

## Positive

* Research begins to causally affect Strategy.
* Keyword dependence is reduced.
* Evidence sensitivity becomes testable.
* Strategic reasoning becomes more explainable.
* The architecture remains minimal.
* No new worker is required.

## Negative

* Opportunity scoring will remain intentionally coarse.
* Evidence confidence is not yet source credibility.
* The Studio still cannot claim verified real-world research quality.
* ReviewBoard may require later adjustment if it collapses distinctions.

---

# Phase 2 Implementation Order

Phase 2 will proceed in this order:

1. EvidenceAssessment model
2. Evidence assessment deterministic logic
3. Evidence assessment tests
4. StrategyWorker ResearchResult integration
5. Removal of AI keyword dominance
6. Opportunity evidence explanation fields
7. Runtime regression
8. Causal Integrity Gate
9. Full suite
10. STOP / REVIEW

---

# Phase 2 Exit Criteria

Phase 2 is complete only when:

* StrategyWorker meaningfully consumes ResearchResult claims.
* Supporting and contradictory evidence can produce materially different evaluation.
* Insufficient evidence remains distinguishable from strong support.
* AI keyword presence does not independently dominate scoring.
* Opportunity exposes evidence-related reasoning.
* Causal Integrity Gate passes.
* Existing software regression suite passes.
* Git checkpoint is clean.

---

# Final Decision

AI-RD-Studio Phase 2 will introduce a minimal deterministic EvidenceAssessment layer between ResearchResult and strategic evaluation.

The design will prioritize:

* Causality
* Explainability
* Relational evaluation
* Minimalism
* Backward compatibility
* Resistance to keyword-driven reasoning

The Studio must not claim evidence-driven strategy until research evidence demonstrably changes strategic evaluation.

