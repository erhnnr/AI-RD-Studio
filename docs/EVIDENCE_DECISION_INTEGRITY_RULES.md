
# Evidence & Decision Integrity Cycle Rules

Version: 0.1
Status: ACTIVE RULESET
Date: 2026-08-09

---

# Purpose

This document defines the binding rules for the Evidence & Decision Integrity Cycle.

These rules exist to prevent scope drift, premature expansion, false confidence, and unnecessary architectural complexity.

The cycle goal is not to make AI-RD-Studio larger.

The cycle goal is to make its research, reasoning, validation, and decisions more trustworthy.

---

# Core Principles

## Rule 01 — Problem First

Development starts from a real capability gap or decision-quality problem.

Do not add features merely because they are technically possible.

---

## Rule 02 — Evidence First

Important claims and decisions must be tied to evidence.

Do not describe a process as evidence-based unless the evidence can be represented, traced, and inspected.

---

## Rule 03 — Architecture Before Implementation

For architectural changes:

```text
Problem
↓
Design
↓
Decision
↓
Implementation
↓
Tests
````

Do not reverse this order.

---

## Rule 04 — Active Phase Only

Do not implement features from future phases before the active phase is complete.

Ideas discovered during development go to the Idea Pool or future review notes.

They do not interrupt the active phase.

---

## Rule 05 — Explicit Exit Criteria

Every phase must have explicit exit criteria.

A phase is not complete because:

* Code was written
* Tests were added
* The implementation looks good

A phase is complete only when its declared exit criteria are satisfied.

---

## Rule 06 — Tests Before Commit

No architectural checkpoint is committed until the relevant tests pass.

Software regression failures must be resolved before proceeding.

---

## Rule 07 — Git Checkpoints

Stable development points must be preserved through:

```text
git commit
+
git push
```

GitHub remains the project source of truth for stable checkpoints.

---

## Rule 08 — No Premature Abstraction

Do not introduce abstractions for hypothetical future needs.

Create abstractions only when a concrete active requirement demonstrates the need.

---

## Rule 09 — No Worker Expansion

No new workers may be added during this cycle unless the roadmap is formally revised after review.

Explicitly deferred:

* EngineeringWorker
* ProductWorker
* Additional specialist workers

The current worker set remains:

* ResearchWorker
* StrategyWorker
* PlanningWorker
* ValidationWorker

---

## Rule 10 — No Autonomy Expansion

The following are outside this cycle:

* Autonomous crawling
* Continuous autonomous execution
* Agent swarms
* Dynamic worker generation
* Distributed orchestration
* Recursive self-improvement
* Fully autonomous company behavior

Do not introduce these capabilities during the active cycle.

---

# Evidence and Research Rules

## Rule 11 — Research Must Become Inspectable

Research must evolve beyond opaque prose.

The system should be able to inspect:

* Claims
* Supporting evidence
* Counter-evidence
* Sources
* Provenance
* Confidence
* Uncertainty

---

## Rule 12 — Evidence Must Affect Decisions

Research is not considered meaningfully integrated if it is only passed through objects without changing downstream reasoning.

Required principle:

```text
Different credible evidence
must be capable of producing
different strategic evaluation
```

---

## Rule 13 — Keyword Heuristics Are Not Strategy

Keywords such as:

```text
"AI"
```

must not act as the primary reason for strategic acceptance.

Heuristics may exist only as minor supporting signals where justified.

---

## Rule 14 — Evidence Quality Matters

Evidence should not be treated as equally trustworthy by default.

Future evidence evaluation may consider:

* Source reliability
* Directness
* Recency
* Independence
* Contradiction
* Confidence

Do not implement unnecessary scoring complexity before it is required.

---

# LLM and External Data Rules

## Rule 15 — LLM Output Is Untrusted Data

LLM-generated content must not be automatically treated as verified fact.

LLM output may contain:

* Errors
* Hallucinations
* Unsupported claims
* Prompt injection effects
* Misinterpretation

Downstream decisions must rely on validated structure and evidence rather than model confidence alone.

---

## Rule 16 — External Data Is Untrusted

External content such as:

* Web pages
* Documents
* Email
* APIs
* User-provided datasets

must be treated as untrusted input.

No external content should directly authorize consequential actions.

---

## Rule 17 — Provider Boundary Must Remain Explicit

The Studio core must remain independent from a specific LLM provider.

Provider-specific implementation details must not leak unnecessarily into core decision logic.

---

## Rule 18 — Provenance Must Be Preserved

When external or AI-generated information influences a decision, the system should preserve where that information came from.

If provenance is unavailable, the uncertainty must remain visible.

---

# Strategy and Decision Rules

## Rule 19 — Strategy Must Be Causally Connected to Research

The Strategy layer must consume research evidence meaningfully.

Required cycle invariant:

```text
Same Signal
+
Strong Supporting Evidence
→ one evaluation trajectory

Same Signal
+
Strong Contradictory Evidence
→ materially different trajectory
```

If this cannot be demonstrated, Phase 2 is not complete.

---

## Rule 20 — Decision Semantics Must Remain Distinct

The following states are not interchangeable:

* ACCEPT
* DEFER
* REJECT

Do not count DEFER as REJECT.

Do not silently collapse distinct decision states.

---

## Rule 21 — Confidence Is Not Certainty

Confidence values must not be presented as objective truth.

Confidence represents uncertainty about a judgment.

It must remain explainable.

---

## Rule 22 — Avoid Precision Illusion

Numeric scores should not imply more certainty than the underlying evidence supports.

A score such as:

```text
35 / 40
```

is not meaningful unless the rubric and evidence behind it are understandable.

---

# Hypothesis and Planning Rules

## Rule 23 — Important Opportunities Need Testable Claims

A serious R&D opportunity should eventually be reducible to one or more testable hypotheses.

The Studio should be able to state:

* What it believes
* Why it believes it
* How the belief can be tested

---

## Rule 24 — Planning Must Be Contextual

Planning must not remain permanently generic.

Plans should eventually depend on:

* Evidence
* Hypothesis
* Strategic context
* Risks
* Measurement criteria

---

## Rule 25 — Measurement Before Validation

The Studio must know what success and failure mean before claiming that something has been validated.

---

# Validation Rules

## Rule 26 — Validation Must Have Authority

Validation cannot remain an informational decoration.

When validation fails, runtime progression must change.

Mandatory invariant:

```text
Failed validation
cannot silently become
ACCEPT
```

---

## Rule 27 — Validation Must Be Explainable

Validation results must provide explicit reasons.

A boolean alone is insufficient for meaningful R&D validation.

---

## Rule 28 — Validation Scope Must Be Honest

Structural validation must not be called real-world validation.

Evidence validation must not be called product validation.

Terminology must reflect actual capability.

---

# Testing and Evaluation Rules

## Rule 29 — Software Tests Are Not Intelligence Tests

The following must remain separate:

```text
Software Regression Suite
```

and

```text
Semantic / Decision Evaluation Suite
```

Passing unit tests proves software behavior, not research or decision quality.

---

## Rule 30 — Do Not Freeze Wrong Behavior

A regression test that preserves incorrect semantics is not success.

Before adding a test, ask:

> Is this the behavior we actually want to preserve?

---

## Rule 31 — Causal Sensitivity Must Be Tested

The system must be tested for whether meaningful evidence changes meaningful decisions.

---

## Rule 32 — Adversarial Cases Matter

Semantic evaluation should eventually include cases designed to expose shallow reasoning, such as:

* Persuasive wording without evidence
* AI-labelled but poor opportunities
* Strong non-AI opportunities
* Contradictory evidence
* Insufficient evidence
* High-confidence false claims

---

## Rule 33 — Benchmark Results Must Be Honest

Do not create fake comparison baselines.

Do not manually invent competitor or LLM outputs and present them as benchmark evidence.

All benchmark claims must have a defensible methodology.

---

# Memory and Learning Rules

## Rule 34 — Memory Is Not Learning

Persistence does not equal learning.

The presence of historical data must not be described as adaptation unless it actually changes future behavior.

---

## Rule 35 — Memory Reuse Must Be Controlled

Historical information can be:

* Wrong
* Outdated
* Context-specific
* Biased

Memory must not automatically influence future decisions without an explicit retrieval and relevance mechanism.

---

## Rule 36 — Preserve Full Decision Trace

The system should progressively preserve:

```text
Signal
Research
Evidence
Hypothesis
Strategy
Plan
Validation
Decision
Outcome
```

as the cycle evolves.

---

# Outcome Rules

## Rule 37 — Decisions Must Eventually Meet Reality

The Studio cannot evaluate its own strategic quality without observing outcomes.

The long-term R&D loop requires:

```text
Decision
↓
Execution
↓
Observed Outcome
↓
Measurement
↓
Comparison
↓
Learning Record
```

---

## Rule 38 — Outcome Feedback Is Not Autonomous Self-Learning

Recording and using outcomes does not authorize uncontrolled self-modification.

Any adaptation remains bounded by explicit architecture and governance.

---

# Governance Rules

## Rule 39 — Human and External LLM Remain Outside the Studio Core

Current governance model:

```text
Human Principal
      +
External Strategic LLM
      |
      v
AI-RD-Studio
```

The Studio may perform bounded independent work.

It does not replace external governance.

---

## Rule 40 — Human Authority Remains Explicit

High-impact actions, major strategic changes, and consequential external actions require explicit authorization unless a future governance decision changes this rule.

---

## Rule 41 — External LLM Is a Role, Not a Vendor

The architecture must not depend conceptually on a single named model or provider.

The role is:

```text
External Strategic LLM
```

not a specific product.

---

# Scope and Product Rules

## Rule 42 — AI-RD-Studio Is the Current Concrete Project

Do not prematurely redesign the system around hypothetical future variants.

Possible future Studio forms may include:

* Scientific Research Studio
* Product Discovery Studio
* Engineering R&D Studio

These remain vision only until real use demonstrates common architecture.

---

## Rule 43 — Generic Studio Core Is Not Yet a Development Target

If common abstractions emerge naturally from real implementations, they may later be extracted.

Do not build a generic Studio framework in advance.

---

## Rule 44 — High-Level Intent Is the Product Direction

The long-term product direction is:

```text
Natural-language goal
↓
Disciplined R&D process
↓
Reviewed project / product outcome
```

Example:

```text
"Build me an LLM teacher."
```

The Studio should increasingly convert such goals into:

* Problem definition
* Research
* Evidence
* Requirements
* Strategy
* Architecture
* Planning
* Implementation or prototype work
* Testing
* Validation
* Review

This remains bounded by governance and current technical capability.

---

# Development Discipline

## Rule 45 — Full Files for Changes

When modifying existing project files during guided development, provide complete replacement file content rather than fragile partial snippets when practical.

---

## Rule 46 — One Controlled Step at a Time

Do not make multiple architectural changes at once when they can be validated independently.

Preferred sequence:

```text
Change
↓
Test
↓
Review
↓
Checkpoint
↓
Next change
```

---

## Rule 47 — No Endless Improvement Loop

Do not continue polishing a phase indefinitely.

Once exit criteria are satisfied:

```text
STOP
REVIEW
CHECKPOINT
MOVE ON
```

---

# Cycle Completion Rule

## Rule 48 — More Code Is Not Success

The Evidence & Decision Integrity Cycle is successful only if Studio decisions become measurably more trustworthy.

Success is demonstrated through:

* Evidence sensitivity
* Causal decision changes
* Explainability
* Validation authority
* Semantic evaluation
* Outcome traceability

---

# Mandatory STOP / REVIEW

## Rule 49

After Phase 6, development stops.

A new external review must be performed before another major development cycle begins.

Do not automatically continue toward:

* More autonomy
* More workers
* More tools
* More architectural layers

The next cycle must be justified by observed real-world capability gaps.

---

# Final Rule

## Rule 50 — Decision Trust Before System Size

When there is uncertainty about what to build next, use this rule:

> Improve the trustworthiness of Studio decisions before increasing the size or autonomy of the Studio.

---

# Evaluation Integrity Rules

## Rule 51 — Phase 2 Requires a Causal Integrity Gate

Phase 2 yalnızca StrategyWorker evidence alanlarını okuyor diye tamamlanmış sayılmaz.

Studio, materially different credible evidence'ın materially different evaluation üretebildiğini göstermelidir.

---

## Rule 52 — Relevant Changes Must Matter

Güçlü destekleyici evidence ile güçlü çelişkili evidence aynı sonucu üretmemelidir.

Material evidence değişikliği reasoning ve decision trajectory üzerinde etkili olmalıdır.

---

## Rule 53 — Irrelevant Changes Should Not Matter

Yalnızca kelime, etiket veya yüzeysel ifade değişiklikleri decision üzerinde belirleyici olmamalıdır.

Özellikle "AI" gibi etiketler tek başına stratejik değer oluşturmamalıdır.

---

## Rule 54 — Development and Holdout Cases Must Remain Separate

Development sırasında kullanılan semantic cases ile final holdout/adversarial cases ayrı tutulmalıdır.

Aynı örnek hem tuning amacıyla kullanılıp hem de generalization kanıtı olarak gösterilemez.

---

## Rule 55 — Phase 5 Requires a Holdout / Adversarial Gate

Phase 5 yalnızca bilinen benchmark vakaları geçti diye tamamlanmış sayılmaz.

Studio daha önce development sırasında kullanılmamış vakalarda da aynı reasoning principles'ı korumalıdır.

---

## Rule 56 — Do Not Tune Directly to Holdout Cases

Bir holdout case başarısız olduğunda yalnızca o örneği geçirmek için özel kural yazılmamalıdır.

Önce underlying reasoning veya architecture problemi bulunmalıdır.

Bir holdout case doğrudan development hedefi haline gelirse artık pristine holdout olarak kabul edilmez.

---

## Rule 57 — Software Correctness and Decision Quality Are Different

Şu üç iddia birbirinden ayrıdır:

```text
The code works.
The reasoning behaves appropriately.
The decision worked in reality.
