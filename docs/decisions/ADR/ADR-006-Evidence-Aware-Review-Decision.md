Tamam. O zaman doğru mimariyi sabitliyoruz: **evidence kararın tek nedeni olmayacak; gerçek bir karar kapısı olacak.**

Sıradaki doğal adım **ADR-006 — Evidence-Aware Review Decision**.

Aç:

```powershell
code docs\decisions\ADR\ADR-006-Evidence-Aware-Review-Decision.md
```

Dosyanın tamamı şu olsun:

````markdown
# ADR-006 — Evidence-Aware Review Decision

Status: Accepted
Date: 2026-08-09
Cycle: Evidence & Decision Integrity
Phase: 2 — Research to Strategy Causal Link

---

# Context

Phase 2 made StrategyWorker sensitive to structured research evidence.

The current causal chain is now:

```text
ResearchResult
↓
EvidenceAssessment
↓
StrategyWorker
↓
Opportunity
````

Supporting, insufficient, mixed, and contradictory evidence can now produce different Opportunity evaluations.

However, ReviewBoard currently evaluates only:

```text
Opportunity.score
```

using fixed thresholds:

```text
score >= 30 → ACCEPT
score >= 15 → DEFER
score < 15  → REJECT
```

With the current conservative evidence-sensitive Strategy scoring:

```text
SUPPORTING     → approximately 23
INSUFFICIENT   → approximately 20
CONTRADICTORY  → approximately 17
```

all three trajectories can collapse into:

```text
DEFER
```

This means evidence affects Strategy but may fail to affect the final ReviewBoard decision.

Phase 2 therefore requires controlled decision propagation.

---

# Decision

ReviewBoard will become evidence-aware.

Evidence state will act as a decision gate.

It will not become the sole determinant of strategic value.

The intended decision hierarchy is:

```text
Evidence Gate
↓
Strategic Evaluation
↓
Review Decision
```

---

# Evidence Gate Semantics

## CONTRADICTORY

Strong contradictory evidence prevents ACCEPT.

Default Phase 2 behavior:

```text
CONTRADICTORY
→ REJECT
```

Reason:

The current evidence materially challenges progression.

This does not mean the opportunity is permanently invalid.

It means the current evidence does not justify advancing it.

---

## INSUFFICIENT

Insufficient evidence prevents ACCEPT.

Default behavior:

```text
INSUFFICIENT
→ DEFER
```

Reason:

The opportunity may still be valuable, but available evidence is not strong enough to justify progression.

Next action should favor additional research.

---

## MIXED

Mixed evidence prevents confident ACCEPT.

Default behavior:

```text
MIXED
→ DEFER
```

Reason:

Meaningful evidence exists on both sides and the contradiction should be resolved before progression.

---

## SUPPORTING

Supporting evidence makes the Opportunity eligible for ACCEPT.

It does not automatically guarantee ACCEPT.

Conceptually:

```text
SUPPORTING
→ ACCEPT ELIGIBLE
```

The remaining strategic evaluation must still be considered.

---

# Strategic Evaluation

Evidence answers:

> Is the current research sufficiently supportive?

Strategic evaluation answers:

> Is this opportunity worth progressing?

These questions must remain separate.

Therefore:

```text
SUPPORTING evidence
does not mean
automatic strategic success.
```

Phase 2 will retain a minimal strategic threshold for ACCEPT eligibility.

The threshold must be explicit and must not recreate keyword-driven behavior.

---

# Legacy Compatibility

Opportunity instances may still exist without evidence metadata.

For:

```text
opportunity.evidence_state is None
```

ReviewBoard will temporarily preserve the legacy score-based decision behavior.

This compatibility path exists to avoid breaking unrelated runtime contracts during Phase 2.

It is not the preferred long-term evidence-first path.

---

# Evidence-Aware Decision Direction

Conceptually:

```text
if evidence_state == CONTRADICTORY:
    REJECT

elif evidence_state == INSUFFICIENT:
    DEFER

elif evidence_state == MIXED:
    DEFER

elif evidence_state == SUPPORTING:
    evaluate strategic eligibility

else:
    use legacy fallback
```

---

# ACCEPT Semantics

Within the current AI-RD-Studio architecture:

```text
ACCEPT
```

does not mean:

* Product launch
* Autonomous execution
* Claim proven true
* Guaranteed success
* Real-world validation complete

It means:

> The opportunity is sufficiently supported and strategically eligible to progress to the next controlled R&D step.

This distinction is binding.

---

# REJECT Semantics

REJECT means:

> Current evidence and/or strategic evaluation does not justify progression.

It does not necessarily mean the opportunity can never be reconsidered.

Future evidence may justify reopening it.

---

# DEFER Semantics

DEFER means:

> The current information state is insufficient or unresolved.

DEFER must remain distinct from REJECT.

A deferred opportunity generally requires:

* More evidence
* Contradiction resolution
* Additional research
* Better strategic information

---

# Confidence

ReviewDecision confidence must not be treated as objective probability.

Confidence should reflect confidence in the current decision under the available evidence and rules.

Phase 2 will not introduce a sophisticated confidence-calibration system.

---

# Non-Goals

This ADR does not introduce:

* Validation gating
* Risk engine
* Source reputation scoring
* Product approval
* Real-world outcome validation
* Autonomous execution
* New workers
* Dynamic decision learning

These belong to later phases.

---

# Causal Integrity Requirement

After this decision is implemented, the Studio must demonstrate:

```text
Same Signal
+
Strong Supporting Evidence
→ eligible for progression

Same Signal
+
Insufficient Evidence
→ DEFER

Same Signal
+
Strong Contradictory Evidence
→ REJECT
```

The final behavior must be tested at ReviewBoard and orchestration level.

---

# Safety Property

The following property is mandatory:

```text
CONTRADICTORY
cannot silently become
ACCEPT
```

The following property is also mandatory:

```text
INSUFFICIENT
cannot silently become
ACCEPT
```

---

# Consequences

## Positive

* Evidence differences survive into decision behavior.
* Research becomes causally relevant beyond StrategyWorker.
* DEFER gains a meaningful evidence-related role.
* Contradictory evidence can stop progression.
* Supporting evidence becomes necessary for evidence-aware ACCEPT.
* Keyword-based acceptance remains eliminated.

## Negative

* ReviewBoard logic becomes richer.
* Legacy and evidence-aware paths temporarily coexist.
* Strategic thresholds still require future refinement.
* Phase 2 remains a conservative decision model, not a complete strategy engine.

---

# Phase 2 Relationship

This ADR completes the architecture required to connect:

```text
Research
↓
Evidence
↓
Strategy
↓
Review Decision
```

After implementation, Phase 2 must still pass:

* ReviewBoard decision propagation tests
* Causal Integrity Gate
* Full regression suite
* STOP / REVIEW

---

# Final Decision

AI-RD-Studio ReviewBoard will become evidence-aware.

Evidence will function as a decision gate, not as a substitute for strategic reasoning.

Supporting evidence may make an opportunity eligible for progression.

Insufficient, mixed, or contradictory evidence must prevent unsupported confident acceptance.

