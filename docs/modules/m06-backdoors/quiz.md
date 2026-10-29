---
title: Module 06 Knowledge Check
---

# Module 06 Knowledge Check

<a id="qz-06"></a>

**QZ-06 · 12 points · Pass 10/12 · 20 minutes**

Answer without notes first. Items 8 and 10 are worth two points each and require reasoning. A correct letter with no reasoning earns half credit on those items.

---

## 1. What a backdoor is (1 point)

Which description best matches a backdoor?

- **A.** A perturbation applied to one input at inference time
- **B.** A learned behavior that is normal on clean inputs and wrong when a trigger is present
- **C.** A model that is inaccurate on all inputs
- **D.** A database of stolen labels

## 2. Clean accuracy and ASR (1 point)

A backdoored model has 0.97 clean accuracy and 0.98 ASR. What does this show?

- **A.** The model is accurate on ordinary inputs and usually produces the target when triggered
- **B.** The model is inaccurate on ordinary inputs
- **C.** The attack failed because clean accuracy is high
- **D.** ASR and accuracy measure the same thing

## 3. The baseline (1 point)

The clean model sends 18% of triggered source inputs to the target class. The backdoored model sends 86%. What is the attack effect?

- **A.** 86%
- **B.** 18%
- **C.** About 68 percentage points
- **D.** 104%

## 4. Poison budget (1 point)

A training set has 840 rows. The attacker inserts 67 poisoned rows. What is the poison rate against the clean training set?

- **A.** 6.7%
- **B.** About 8.0%
- **C.** 67%
- **D.** It cannot be computed without the test-set size

## 5. Trigger-scan score (1 point)

A scan patches class-0 test images at each candidate position and averages the class-1 probability. The backdoored model scores 0.89 at the true patch; the clean model scores 0.04 at the same patch. What is the 0.04?

- **A.** The backdoor's attack success rate
- **B.** The clean model's baseline response to that pattern
- **C.** The scan's false-positive rate
- **D.** The poison rate

## 6. Threshold choice (1 point)

A trigger scan flags any position scoring above a threshold. Raising the threshold from 0.80 to 0.85 will generally:

- **A.** Increase both true and false positives
- **B.** Decrease both true and false positives
- **C.** Increase true positives and decrease false positives
- **D.** Have no effect on either

## 7. Supply chain (1 point)

Which entry point can carry a backdoor **without** poisoned rows in your own training data?

- **A.** A trojaned model checkpoint from a vendor
- **B.** A test set with wrong labels
- **C.** A miscalibrated probability threshold
- **D.** A missing random seed

## 8. Find the flaw (2 points)

A student writes:

```python
X_poisoned = np.vstack([X_train, add_trigger(X_train[chosen])])
y_poisoned = y_train.copy()
y_poisoned[chosen] = 1
model.fit(X_poisoned, y_poisoned)
asr = (model.predict(X_poisoned[840:]) == 1).mean()
```

Assume `X_train` has 840 rows and `chosen` has 67 indices. Identify **two** flaws, explain each consequence, and give the corrected lines.

## 9. Appending versus overwriting (1 point)

Compute `round(0.08 × 840)`. Then explain in one sentence why the attacker appends triggered rows instead of overwriting the original class-0 rows.

## 10. Evaluate the claim (2 points)

A vendor says:

> Our model has 99% accuracy on a 10,000-image test set. Our red team also tried 500 random images and saw no unexpected behavior. Therefore the model has no backdoor.

Identify **three** problems with this claim and rewrite it as a claim the evidence could support. (Three problems without a rewrite earns one point; a rewrite without three problems earns one point.)

---

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You separate conditional behavior from clean accuracy. |
| 10 | Pass. Review the missed item before LAB-08. |
| 8–9 | Re-read Lessons 1 and 3, especially baselines and scan assumptions. |
| Below 8 | Re-read all four lessons and rerun LAB-07 before continuing. |

Answers and explanations are in the [answer key](quiz-answers.md). Do not read it before attempting the quiz.
