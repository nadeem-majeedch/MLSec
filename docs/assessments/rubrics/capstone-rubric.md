---
title: Capstone Self-Scoring Rubric
---

# Capstone Self-Scoring Rubric

| Field | Value |
|---|---|
| Applies to | Capstone CAP-A…CAP-F |
| Dimensions | 8 |
| Total | 100 |
| Completion | Every dimension at **Proficient (3)** or above |
| Automatic fails | Third-party target, real personal data, real credential, fabricated result, contradictory claim |
| Companion | [Capstone brief](../../projects/capstone.md) · [Project and RT-01 rubric](project-rubric.md) · [Lab rubric](lab-rubric.md) |

Score your own capstone before an evaluator does. The purpose is not to predict a grade; it is to find the dimension that would make the claim fail and fix it while there is still time.

## 1. Dimensions

| Dimension | Weight | 4 — Exemplary | 3 — Proficient | 2 — Developing | 1 — Insufficient |
|---|---:|---|---|---|---|
| Problem, system, and data | 10 | Scope enumerable; decision and harm explicit; data classified and licensed; boundaries complete | Clear scope and data inventory with minor gaps | Vague scope or missing classification | No usable scope or data record |
| Threat model | 15 | Testable adversaries; anchored risk scores; every test traced; rejections reasoned | Clear model with minor gaps | Generic threats; weak traceability | No threat model or misleading claims |
| Baseline and experimental design | 15 | Frozen, hashed baseline; controls; multiple budgets/seeds; uncertainty; confounders addressed | Sound baseline and comparison with limited uncertainty | Single run or confounded comparison | No baseline or invalid comparison |
| Attack execution and analysis | 20 | At least 3 attacks; correct budgets; adaptive variant; honest negative results; no overclaim | Attacks run correctly with minor omissions | Partial results or metric errors | Attacks do not run or results invalid |
| Defense and adaptive evaluation | 15 | Implemented control; replay; declared variant; costs measured; residual risk | Control evaluated with limited adaptivity | Static test only | No defense or no evaluation |
| Reproducibility and evidence | 10 | Clean checkout; manifest matches; run records; one-command reproduction | Reproduces with small fixes | Missing steps | Not reproducible |
| Communication and recommendations | 10 | Report and briefing decision-oriented; findings costed and ordered; residual risk clear | Clear with minor issues | Disorganized or overlong | Unsupported or unsafe recommendations |
| Ethics, safety, and limitations | 5 | Authorized-use statement; local/synthetic; all four validity types; no overclaim | Clear constraints with minor gaps | Weak limitations or safety statement | Unsafe, unlawful, or overclaiming |

Weighted score for a dimension is $\text{weight} \times \text{level} / 4$. The maximum is 100.

## 2. Score sheet

| Dimension | Weight | Level (1–4) | Weighted | Evidence |
|---|---:|---:|---:|---|
| Problem, system, data | 10 | | | |
| Threat model | 15 | | | |
| Baseline and design | 15 | | | |
| Attack execution | 20 | | | |
| Defense and adaptive | 15 | | | |
| Reproducibility | 10 | | | |
| Communication | 10 | | | |
| Ethics and limitations | 5 | | | |
| **Total** | **100** | | | |

A total of 88 with one dimension at 2 does not complete the capstone. The rule is **every row at 3 or above**, then the total.

## 3. What each level looks like

### Problem, system, and data

- **4:** An enumerable scope, a named decision, the harm of a wrong decision in both directions, a data inventory with classification and license, and explicit boundaries.
- **3:** The same elements with a minor gap, such as an unclassified log or a missing license note.
- **2:** A topic rather than a system, or data whose origin and classification are unclear.
- **1:** No usable scope, or data that cannot lawfully be used.

### Threat model

- **4:** Two bounded adversary profiles with knowledge, access, and budget; risk scores anchored to a stated scale; every test traces to a register entry; at least one rejected threat with a reopening condition.
- **3:** A clear model with one weak trace or an unstated assumption.
- **2:** A list of techniques, generic threats, or tests that do not trace to risks.
- **1:** No model, or a model that contradicts the tests.

### Baseline and experimental design

- **4:** A frozen, hashed baseline; a zero-effect control; multiple budgets or seeds; intervals; confounders named and addressed.
- **3:** A sound baseline and matched comparison with limited uncertainty.
- **2:** A single run, a moving baseline, or a comparison that changes more than one factor.
- **1:** No baseline or an invalid comparison.

### Attack execution and analysis

- **4:** At least three attacks, correct budgets and denominators, an adaptive variant, honest negative results, and a conclusion that stops at the evidence.
- **3:** Attacks run correctly with a minor omission, such as one missing denominator.
- **2:** Partial results, a metric error, or an overclaim that the evidence cannot carry.
- **1:** The attacks do not run, or the results are invalid or fabricated.

### Defense and adaptive evaluation

- **4:** An implemented control, a replay of the original attack, a declared adaptive variant, measured false positives and clean cost, and a residual-risk statement.
- **3:** A control evaluated with limited adaptivity or cost reporting.
- **2:** A static test only, or a claim of robustness without an adaptive check.
- **1:** No defense, or no evaluation of the defense that was proposed.

### Reproducibility and evidence

- **4:** Clean checkout, pinned environment, seeds, manifest with matching hashes, run records, and a one-command reproduction that yields the headline number.
- **3:** Reproduces with small documented fixes.
- **2:** Missing steps, unpinned dependencies, or a result that depends on undocumented state.
- **1:** Not reproducible, or the package does not match the report.

### Communication and recommendations

- **4:** The report and briefing lead with the decision; findings are ordered and costed; residual risk is explicit; the abstract states the headline result and its scope.
- **3:** Clear and complete with minor organizational issues.
- **2:** Disorganized, overlong, or a recommendation without a cost or owner.
- **1:** Unsupported, unsafe, or contradictory recommendations.

### Ethics, safety, and limitations

- **4:** A signed authorized-use statement; local or synthetic data; construct, internal, external, and statistical limitations all addressed; no claim beyond the tested conditions.
- **3:** Clear constraints with a minor gap in the limitations.
- **2:** A weak safety statement or only one kind of limitation.
- **1:** An unsafe or unlawful method, real personal data, a real credential, or an overclaim that contradicts the artifact.

## 4. Automatic fails

The capstone cannot pass, regardless of the weighted score, if it:

- tests a third-party production system without written authorization;
- uses real personal data, real credentials, or a real mailbox or network target;
- fabricates or selectively edits a result, or reports a number that the artifact cannot reproduce;
- makes a claim that contradicts its own artifact, such as "the defense held" when the adaptive run succeeded;
- presents a harmful capability as the deliverable rather than a defensive finding.

## 5. Evidence checklist

Use this list before scoring. Each item should point to a file or section.

- [ ] Scope, decision, harm, and non-goals
- [ ] System diagram and data inventory with classification and license
- [ ] Two adversary profiles with budgets
- [ ] Risk register with scores, controls, owners, and residual risk
- [ ] Frozen baseline with hashes and run record
- [ ] At least three attacks with budgets, denominators, and base sets
- [ ] At least one adaptive variant or a reason it cannot be run
- [ ] At least one defense with replay, false-positive cost, and clean-accuracy cost
- [ ] Clean-checkout reproduction and manifest match
- [ ] Findings ordered, costed, and traceable to tests
- [ ] Residual-risk statement naming what remains
- [ ] Authorized-use statement and limitations
- [ ] Briefing that a decision-maker could act on

## 6. Self-scoring method

1. Score each dimension from the artifact, not from memory or effort.
2. For each level, write the file and line or section that supports it. A level with no evidence is a 2 at most.
3. Score the weakest dimension first. It decides completion.
4. If a dimension is at 3, ask what would make it a 4 and whether the missing evidence is worth the remaining time.
5. Re-score only after changing the artifact.
6. Do not average away an automatic fail.

## 7. Calibration notes

- A polished report cannot raise a dimension whose artifact is missing. The artifact is the evidence.
- A negative result is not a low score. A well-scoped negative result with an interval and a clear limit can be level 4.
- A large ASR drop with a changed threshold, base set, or clean accuracy is a confounded comparison, not a strong defense.
- A clean-checkout failure caps Reproducibility at 2, even if the reported number is plausible.
- An ethics statement that says "all data were synthetic" while the package contains real records is an automatic fail, not a communication issue.

This rubric is a self-assessment tool. It is not externally validated, not proctored, and not a substitute for the evaluator's reading of the capstone.
