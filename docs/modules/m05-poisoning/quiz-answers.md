# Module 05 Knowledge Check — Answers and Explanations

**QZ-05 · 12 points · Pass 10/12**

Do not read this file before attempting the quiz.

---

## 1. Poison rate — **B** (1 point)

$200 / 4{,}000 = 0.05$, or 5%. The denominator is the clean training-set size; the test-set size is irrelevant to the attack budget.

## 2. Timing and access — **B** (1 point)

Poisoning acts on training data or the training process, so the effect is learned and persists. Option A describes evasion. Option C is false: label-only attacks need no weights. Option D is false: a targeted attack can leave accuracy flat or raise it.

## 3. Clean-label attacks — **B** (1 point)

The added rows carry correct labels and plausible features; the attacker's leverage is placement, not mislabelling. A label check therefore has nothing to catch.

## 4. The low-rate plateau — **B** (1 point)

At 5%, 1,194 of 1,257 labels remain correct, the wrong rows are spread across classes, and the class balance barely moves. The boundary shifts only where the evidence is already weak. Option C is false: the model does use the flipped rows; it just is not overwhelmed by them.

## 5. A targeted result — **C** (1 point)

The attack's goal was the target decision, and that decision changed. A one-point accuracy rise is consistent with a boundary shift that helps some test rows and hurts others. Option A mistakes the availability metric for the attack's objective. Option B is not supported: the rise is incidental, not an improvement in the model's intended behavior.

## 6. Screening thresholds — **B** (1 point)

At τ = 0.5, six poisons survive and are enough to hold the target. Recall measures how many suspicious rows were removed; the protected outcome measures whether the decision recovered. A defense claim needs both.

## 7. Reference-set assumption — **D** (1 point)

The reference set must be clean, representative, and outside the attacker's control. It does **not** need to be larger than the training set; LAB-06 uses 150 reference rows against 350 training rows.

## 8. Find the flaw — **2 points**

Award one point for each flaw with its consequence; no credit for naming a flaw without saying what it does.

**Flaw 1 — the model is fit on the clean labels.** `fit(X_train, y_train)` ignores `y_poisoned`, so the attack has no effect and the reported accuracy is the clean baseline.

```python
model = LogisticRegression(max_iter=3000).fit(X_train, y_poisoned)
```

**Flaw 2 — truncation instead of rounding.** `int(0.10 * 1257)` is 125, while the course protocol gives 126. The count is off by one and the run no longer matches the reference.

```python
n_poison = int(round(0.10 * len(y_train)))   # 126
```

The test-set handling is correct: `y_test` is never modified. If a student lists "the test set was flipped" as a flaw, that is wrong for this code.

## 9. Denominator arithmetic — **1 point**

$$
n = \frac{300}{0.06} = 5{,}000.
$$

The same 300 rows are 5% of a 6,000-row denominator (for example, if training and test rows were combined) and 6% of 5,000 training rows. A rate without a named denominator cannot be compared with another rate.

## 10. Evaluate the claim — **2 points**

Award one point for three real problems, one point for a rewrite that keeps the scope of the evidence. Any three of:

- **Accuracy hides targeted attacks.** LAB-06 flipped a chosen decision while accuracy rose. "Above 90%" says nothing about integrity on specific inputs.
- **10% is one point on one curve.** It belongs to one model, dataset, and flip rule. It is not a tolerance that transfers to another pipeline, and there is no confidence interval or dose-response.
- **The screen result is not adaptive.** "Caught every poison we tried" describes the attacks the vendor chose, probably dense mislabelled clusters. It does not cover clean-label, spread-out, or defense-aware attacks.
- **The screen has a false-positive cost.** The claim reports no threshold and no clean rows removed, so the operational cost is hidden.
- **The reference set is assumed clean.** If the attacker can influence it, the screen can be taught to accept the poison.
- **"Safe" is not a measurable property.** The claim does not name the harm, the attacker, or the budget it is safe against.

**Example rewrite.**

> For this model and flip rule, test accuracy stayed above 90% when 10% of training labels were flipped at random (n = 1,257 training rows; one seed). At threshold τ = 0.6, the reference-set screen removed 30 of 30 injected feature-space poisons and 37 of 350 clean rows. These results do not cover targeted, clean-label, or defense-aware attacks, and test accuracy is not a measure of targeted integrity.

The rewrite is acceptable only if it states the attack, the budget, the metric, the false-positive cost, and at least one scope limit. A rewrite that says "the pipeline is robust to 10% noise" earns no credit.

---

## Score guide

| Score | Next step |
|---:|---|
| 11–12 | Move to LAB-06 or Module 06 |
| 10 | Review the missed item, then continue |
| 8–9 | Re-read Lessons 3–4 and rerun the LAB-06 screen |
| Below 8 | Re-read all four lessons before continuing |
