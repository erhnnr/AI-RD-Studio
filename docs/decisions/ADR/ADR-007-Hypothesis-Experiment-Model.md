Evet, bu fikir **Studio’nun çok güçlü bir ikinci varyasyonu olabilir**. Ama adı ve iddiası dikkatli seçilmeli.

“LLM halüsinasyonunu sıfırlar” demek genel durumda fazla güçlü olur. Çünkü açık dünyada bir LLM’in her iddiasının doğru olduğunu garanti etmek mümkün değil. Ama şunu hedefleyebiliriz:

> **LLM çıktısını doğrudan kullanıcıya vermek yerine; claim → evidence → verification → confidence → abstain/approve kapılarından geçirip, doğrulanamayan kısmı bastıran bir çıktı katmanı.**

Kabaca:

```text
LLM raw output
    ↓
Claim extraction
    ↓
Evidence lookup / provenance
    ↓
Contradiction check
    ↓
Verification
    ↓
Confidence / uncertainty
    ↓
Decision
    ├── VERIFIED OUTPUT
    ├── QUALIFIED OUTPUT
    └── ABSTAIN / NEEDS MORE EVIDENCE
```

Bu aslında şu an Studio’da kurduğumuz çekirdekle çok uyumlu:

```text
Claim
Evidence
Counter-evidence
Provenance
Confidence
Causal reasoning
Review gate
```

Yani bugünkü Evidence & Decision Integrity çalışması ileride sadece R&D Studio’ya değil, şöyle bir ürüne de dönüşebilir:

**Verified LLM Output Layer**
veya
**Evidence-Grounded Response Gateway**

Bu katman LLM’in önüne/arkasına konabilir:

```text
User
↓
LLM
↓
Verified Output Layer
↓
User
```

Özellikle kapalı veya doğrulanabilir alanlarda çok güçlü olur:

* hukuk dokümanları
* şirket içi bilgi
* teknik dokümantasyon
* bilimsel literatür
* eğitim materyalleri
* belirli veri tabanları
* kod / API belgeleri

Burada hedef gerçekten çok düşük halüsinasyon riski olabilir.

Açık dünya sorularında ise daha doğru vaat:

> **“Doğrulanamayan iddiayı kesin bilgi gibi çıkarmama.”**

Bu bence “halüsinasyonu sıfırlamak”tan daha güçlü bir ürün prensibi bile olabilir. Çünkü sistem cevap vermek zorunda hissetmez:

```text
Evidence yok
→ bilmiyorum / doğrulanamadı

Evidence çelişkili
→ belirsiz

Evidence yeterli
→ cevap + kaynak + confidence
```

Bu fikri **şimdi geliştirmiyoruz**. Mevcut kuralımıza göre Idea Pool’a koymalıyız. Ama önemli bir not: Bu fikir mevcut Studio’dan tamamen bağımsız değil; şu anda yaptığımız Evidence/Provenance/Validation altyapısının ileride **yeniden kullanılabileceği somut bir ürün varyasyonu**.

---

Şimdi kendi işimize dönelim.

## Phase 3 — sıradaki doğal adım

**ADR-007 — Hypothesis & Experiment Model**

Aç:

```powershell
code docs\decisions\ADR\ADR-007-Hypothesis-Experiment-Model.md
```

Dosyanın tamamı şu olsun:

````markdown
# ADR-007 — Hypothesis & Experiment Model

Status: Accepted
Date: 2026-08-09
Cycle: Evidence & Decision Integrity
Phase: 3 — Hypothesis, Experiment & Decision Semantics

---

# Context

AI-RD-Studio can now connect structured research evidence to strategic evaluation and ReviewBoard decisions.

The current causal chain is:

```text
Signal
↓
Research
↓
Evidence
↓
Strategy
↓
Opportunity
↓
Review Decision
````

However, an accepted or deferred opportunity still does not explicitly define:

* What belief is being tested
* Which assumptions the belief depends on
* How the belief can be tested
* What should be measured
* What result would support the belief
* What result would falsify or challenge it
* When an experiment should stop

Without these concepts, Planning risks remaining a generic task-list generator rather than an R&D planning layer.

Phase 3 therefore introduces a minimal hypothesis and experiment model.

---

# Decision

AI-RD-Studio will introduce explicit domain concepts for:

* Hypothesis
* Experiment
* Measurement

These concepts will be integrated into PlanningResult.

The purpose is to move from:

```text
Opportunity
→ generic plan
```

toward:

```text
Opportunity
↓
Hypothesis
↓
Experiment
↓
Measurement
↓
Success / Failure Criteria
↓
Plan
```

---

# Hypothesis

A Hypothesis represents a testable proposition about an Opportunity.

Minimum responsibilities:

* statement
* assumptions
* success criteria
* failure criteria

A hypothesis must be written so that evidence or an experiment can meaningfully challenge it.

A hypothesis must not merely restate the Opportunity title.

---

# Assumptions

Assumptions represent conditions that must hold for the hypothesis or experiment to be meaningful.

Examples may include:

* Required user behavior
* Required technical conditions
* Required resource availability
* Required environmental conditions

Assumptions must remain explicit rather than being silently embedded in planning logic.

---

# Success Criteria

Success criteria define what result would provide meaningful support for the hypothesis.

Success criteria should be:

* Observable
* Understandable
* Relevant to the hypothesis
* Measurable where practical

Phase 3 will not require advanced statistical analysis.

---

# Failure Criteria

Failure criteria define what result would materially challenge the hypothesis.

Failure criteria are required because an R&D plan must be capable of discovering that its initial belief is wrong.

A plan that cannot fail is not a meaningful experiment.

---

# Experiment

An Experiment represents how the hypothesis will be tested.

Minimum responsibilities:

* objective
* method
* measurements
* stop conditions

An Experiment does not necessarily mean a laboratory experiment.

It may represent:

* Prototype evaluation
* User test
* Benchmark
* Controlled comparison
* Technical feasibility test
* Data analysis
* Structured observation

---

# Measurement

Measurement represents something observed during an Experiment.

The minimum model should support:

* metric
* optional baseline
* optional target
* optional unit

Phase 3 will not introduce:

* Statistical significance engines
* Probability models
* Complex experiment analytics

---

# Stop Conditions

Stop conditions make explicit when an Experiment should stop.

Examples may include:

* Success criterion reached
* Failure criterion reached
* Time limit reached
* Resource limit reached
* Safety condition triggered

Stop conditions must remain inspectable.

---

# PlanningResult Integration

PlanningResult will progressively carry:

```text
PlanningResult
├── opportunity
├── hypothesis
├── experiment
├── objective
└── steps
```

Existing fields should remain backward compatible where practical.

---

# Contextual Planning Requirement

PlanningWorker must not permanently generate the same generic plan for every Opportunity.

The plan should progressively depend on:

* Opportunity
* Evidence state
* Hypothesis
* Experiment objective
* Measurement criteria

Phase 3 must demonstrate at least one controlled path where materially different Opportunity context produces materially different planning content.

---

# Decision Semantics

Phase 3 also clarifies project-level decision semantics.

The following states must remain distinct:

```text
ACCEPT
DEFER
REJECT
```

In particular:

```text
DEFER != REJECT
```

Project-level summaries must not silently count DEFER as REJECT.

The intended project summary direction is:

```text
accepted_count
deferred_count
rejected_count
```

---

# ACCEPT Meaning

ACCEPT means:

> The opportunity is sufficiently supported and strategically eligible to progress to the next controlled R&D step.

It does not mean:

* Hypothesis proven
* Experiment successful
* Product validated
* Real-world success guaranteed

---

# DEFER Meaning

DEFER means:

> The current evidence, strategic information, or experiment definition is not sufficient for progression.

Typical next actions may include:

* Additional research
* Contradiction resolution
* Better measurement definition
* Revised hypothesis
* Refined strategic evaluation

---

# REJECT Meaning

REJECT means:

> Current evidence or strategic evaluation does not justify progression.

REJECT is not equivalent to permanent deletion.

A future evidence change may justify reconsideration.

---

# Worker Scope

No new worker will be introduced.

PlanningWorker remains responsible for PlanningResult.

The hypothesis and experiment model will be domain structure consumed by the existing PlanningWorker.

---

# Validation Scope

Phase 3 will create testable planning structure.

ValidationWorker will not yet become the authoritative experiment-quality gate.

That belongs to Phase 4.

---

# Non-Goals

Phase 3 will not implement:

* Autonomous experiment execution
* Real-world outcome collection
* Statistical significance testing
* Optimization engines
* New workers
* Validation authority expansion
* Product execution
* Autonomous implementation
* Self-learning

---

# Required Invariants

The following properties must hold:

```text
A meaningful R&D plan
must contain a testable hypothesis.
```

```text
A meaningful experiment
must define what is measured.
```

```text
A hypothesis
must be capable of failure.
```

```text
DEFER
must not be counted as
REJECT.
```

---

# Phase 3 Implementation Order

Phase 3 will proceed in this order:

1. Hypothesis / Experiment / Measurement domain model
2. Domain model tests
3. PlanningResult integration
4. PlanningWorker contextual planning
5. Decision semantics correction
6. Project summary correction
7. Regression tests
8. Phase 3 exit review

---

# Phase 3 Exit Criteria

Phase 3 is complete only when:

* Hypothesis is explicitly represented.
* Assumptions are explicitly represented.
* Success criteria are explicitly represented.
* Failure criteria are explicitly represented.
* Experiment is explicitly represented.
* Measurements are explicitly represented.
* Stop conditions are explicitly represented.
* PlanningResult can carry hypothesis and experiment structure.
* PlanningWorker produces at least one contextual testable plan.
* DEFER and REJECT remain distinct.
* Project summaries distinguish ACCEPT, DEFER and REJECT.
* Existing regression suite passes.
* Git checkpoint is clean.

---

# Final Decision

AI-RD-Studio will introduce a minimal explicit hypothesis and experiment domain model.

The purpose is not to increase model complexity.

The purpose is to make accepted opportunities testable, falsifiable, measurable, and suitable for disciplined R&D planning.

