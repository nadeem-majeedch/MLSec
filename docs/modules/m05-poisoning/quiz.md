---
title: Module 05 Knowledge Check
---

# Module 05 Knowledge Check

<a id="qz-05"></a>

**QZ-05 · 12 points · Pass 10/12 · 20 minutes**

Answer without notes first. One item has two parts and is worth two points. Write your reasoning for items 8–10; a correct letter with no reasoning earns half credit on those items.

---

## 1. Poison rate (1 point)

A training set has 4,000 clean rows. An attacker corrupts 200 of them. What is the poison rate?

- **A.** 0.5%
- **B.** 5%
- **C.** 20%
- **D.** It cannot be computed without the test-set size

## 2. Timing and access (1 point)

Which statement best describes poisoning?

- **A.** It changes a model's output by perturbing one input at inference time.
- **B.** It changes training data or the training process, so the learned model is affected.
- **C.** It only works if the attacker can read the model weights.
- **D.** It always reduces test accuracy.

## 3. Clean-label attacks (1 point)

What distinguishes a clean-label poisoning attack?

- **A.** It uses no labels at all.
- **B.** The added rows carry correct labels, so a label check does not reveal them.
- **C.** It changes only the test set.
- **D.** It requires white-box access to the model.

## 4. The low-rate plateau (1 point)

In LAB-05, flipping 5% of labels cost only 0.2 accuracy points. Which explanation is most accurate?

- **A.** The flipped rows were removed from the test set.
- **B.** A small number of inconsistent labels shifts the boundary only where the evidence is weak, and class balance barely changes.
- **C.** Logistic regression ignores mislabelled rows.
- **D.** The test set was also flipped, hiding the effect

## 5. A targeted result (1 point)

In LAB-06, the target flips from class 1 to class 0, while test accuracy rises from 0.88 to 0.89. What is the best interpretation?

- **A.** The attack failed, because accuracy did not fall.
- **B.** The poison improved the model.
- **C.** A targeted integrity attack can succeed while an aggregate availability metric improves.
- **D.** The test set was poisoned

## 6. Screening thresholds (1 point)

LAB-06's screen catches 24 of 30 poisons at τ = 0.5, but the target still predicts class 0. What does this show?

- **A.** The screen is broken and should be discarded.
- **B.** High recall is not sufficient; the protected outcome must be measured.
- **C.** The threshold should always be 0.5.
- **D.** The poisons were not really poisons

## 7. Reference-set assumption (1 point)

Which condition is **not** required for the reference-set screen to be trustworthy?

- **A.** The reference rows are clean.
- **B.** The reference rows come from the same distribution as legitimate training data.
- **C.** The attacker cannot influence the reference set.
- **D.** The reference set is larger than the training set

## 8. Find the flaw (2 points)

A student writes this experiment for a single 10% label-flip rate:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
y_poisoned = y_train.copy()
rng = np.random.default_rng(42)
n_poison = int(0.10 * len(y_train))
chosen = rng.choice(len(y_train), size=n_poison, replace=False)
y_poisoned[chosen] = (y_poisoned[chosen] + 1) % 10

model = LogisticRegression(max_iter=3000).fit(X_train, y_train)
accuracy = accuracy_score(y_test, model.predict(X_test))
```

Identify **two** flaws, explain the consequence of each, and give the corrected lines. (The split uses 1,257 training rows.)

## 9. Denominator arithmetic (1 point)

A team reports 300 poisoned rows and a poison rate of 6%. What clean training-set size does that imply? Show the arithmetic. Then state, in one sentence, why the same 300 rows could be described as a different rate in a report that uses a different denominator.

## 10. Evaluate the claim (2 points)

A vendor says:

> Our pipeline tolerates 10% label noise because test accuracy stayed above 90% in our experiments. We also tested our reference-set screen against injected poisons and it caught every one. The training data is therefore safe.

Identify **three** problems with this claim and rewrite it as a claim the evidence could support. (A correct rewrite with no identified problems earns one point; three problems with no rewrite earns one point.)

---

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can separate an attack result from a security claim. |
| 10 | Pass. Review the items you missed before LAB-06. |
| 8–9 | Re-read Lessons 3–4, especially the defense trade-off. |
| Below 8 | Re-read all four lessons and rerun LAB-05 before continuing. |

Answers and explanations are in the [answer key](quiz-answers.md). Do not read it before attempting the quiz.
