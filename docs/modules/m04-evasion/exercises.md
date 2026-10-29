---
title: Module 04 Exercises
---

# Module 04 Exercises

**Four exercises · about 90 minutes · Complete after Lessons 1–5**

Write your work in `work/m04/`. Run every calculation; do not only read it. The point of these exercises is interpretation: each one asks you to decide what a number supports, not to reproduce attack code. Compare with the [solutions](exercise-solutions.md) after a first attempt.

| Exercise | Focus | Time | Deliverable |
|---|---|---:|---|
| 1 | Derive and check FGSM by hand | 15 min | `fgsm_by_hand.py`, note |
| 2 | Audit a flawed ASR claim | 20 min | `audit.md` |
| 3 | Scenario: a vendor's robustness claim | 30 min | `gatekeeper-memo.md` |
| 4 | Uncertainty and budget arithmetic | 20 min | `power.py`, note |

---

## Exercise 1 — FGSM on a one-dimensional model

**Goal.** Compute an adversarial step without a library, then confirm it in code. A one-input model makes every term visible.

**Setup.** A binary logistic regression scores class 1 as

$$
s(x) = 5x - 1, \qquad p_1 = \sigma(s).
$$

The true label is $y = 1$, and the loss is $J(x) = -\log p_1$. The input is $x = 0.3$.

**Tasks.**

1. Compute $s$, $p_1$, and $\partial J/\partial x$ by hand. Use $\sigma(s) = 1/(1 + e^{-s})$.
2. Apply one FGSM step with $\epsilon = 0.12$: $x' = x + \epsilon\,\mathrm{sign}(\partial J/\partial x)$. Compute $x'$, the new score, the new probability, and the new prediction (threshold 0.5).
3. Compute the smallest $\epsilon$ that changes the prediction, and compare it with 0.12. Explain the difference in one sentence.
4. Write `fgsm_by_hand.py` that recomputes tasks 1–3 and prints each quantity with four decimals. Confirm the hand values.
5. The loss increased, but the model's confidence in class 1 fell from about 0.62 to about 0.48. Is that a successful attack? Answer in two sentences, using the definition of attack success from Lesson 1.

**Deliverable.** `work/m04/fgsm_by_hand.py` and a five-line note.

**Success criteria.** The hand values match the code to four decimals; the sign of the step is explained, not just stated; the answer to task 5 distinguishes a loss increase from a prediction change.

---

## Exercise 2 — Audit a flawed attack claim

**Goal.** Find the errors that make an attack result unreproducible or misleading.

**Scenario.** A colleague reports the following on the LAB-03 model (540 test rows, clean accuracy 0.9667):

> We ran FGSM at ε = 0.10 and 175 images changed label. That is 35.7% of the test set, so the model lost 35.7 accuracy points. The attack is therefore more damaging than the 33.5% we measured on correctly classified images, and it shows the model is not suitable for deployment.

The honest base-set result at ε = 0.10 is ASR = 0.3352.

**Tasks.**

1. Recompute three numbers from the counts: successes over the base set, successes over all test rows, and the number of test rows the clean model already got wrong. Show the arithmetic.
2. Explain why counting a row that was already wrong as an attack success inflates the rate. State the inflated rate and the honest rate.
3. The claim says "lost 35.7 accuracy points." Compute the actual robust accuracy on the full test set and the actual accuracy drop, assuming the attack is applied only to clean-correct rows and the other rows are unchanged. Explain why ASR and accuracy drop have different denominators.
4. List three things the report fails to state that a reader would need to reproduce it.
5. Rewrite the claim as two sentences that a reviewer could accept. Keep the numbers you computed.
6. The report concludes "not suitable for deployment." Name one extra piece of evidence, beyond a better number, that a deployment decision would need.

**Deliverable.** `work/m04/audit.md` with the arithmetic shown.

**Success criteria.** All three counts are correct; the difference between ASR and accuracy drop is explained with denominators; the rewritten claim contains a budget, a base set, and a scope limit; the extra evidence is about the threat model, not about model accuracy.

---

## Exercise 3 — Scenario: the GateKeeper vendor claim

**Goal.** Decide what a black-box test can establish, and design one that fits a fixed query budget.

**Scenario.** GateKeeper is a fictional warehouse gate. A grayscale camera (224 × 224, 8-bit) photographs container codes, and a vendor classifier decides whether each code is valid. You cannot inspect the model. The vendor's report says:

- Clean accuracy on their test set: 99.2%.
- "Robustness testing": 200 randomly generated noise images, no prediction changed.
- Inputs may be perturbed by up to ε = 8/255 in L∞, measured on pixels scaled to [0, 1].

Your team may send 5,000 queries per day. The API returns only the top-1 label. You have 500 held-out photographs you can use for measurement, and you can generate more unlabelled photographs locally.

**Tasks.**

1. Convert ε = 8/255 to a decimal, and state how many gray levels one channel may change. Compute the L2 norm of a perturbation that moves **every** pixel by exactly ε. (There are 224 × 224 = 50,176 pixels.) Comment on whether "8/255" sounds small after this calculation.
2. State two reasons the 200-noise trial does not support the robustness claim. One reason must be about the attack method, one about the evidence.
3. Design a transfer-based black-box test within the daily budget. Give the number of queries for each step: collecting a labelled surrogate set, measuring on the 500 held-out photographs, and one optional second surrogate. Check the total against 5,000.
4. Pre-register a decision rule before running: what transfer ASR would you treat as material for this system, and why? One sentence.
5. Write the recommendation in three sentences: what you accept, what you reject, and what you require next. Include one residual-risk sentence.
6. The vendor proposes 5-bit quantization of camera input as a defense. Explain in two sentences why this may reduce transfer success but does not establish robustness. Name one cost of the control.

**Deliverable.** `work/m04/gatekeeper-memo.md`.

**Success criteria.** The budget arithmetic is explicit and sums correctly; the recommendation separates clean accuracy from robustness; the decision rule is stated before the result; the quantization answer mentions adaptive attacks and a real cost; the memo does not claim the vendor's system is vulnerable.

---

## Exercise 4 — How many rows does a claim need?

**Goal.** Use uncertainty to decide whether two attack results differ.

**Data.** Two configurations of the same attack on the same model:

| Configuration | Successes | Base-set rows |
|---|---:|---:|
| A | 18 | 60 |
| B | 30 | 60 |

Use the Wilson interval with $z = 1.96$:

$$
\text{center} = \frac{\hat p + z^2/(2n)}{1 + z^2/n}, \qquad
\text{half} = \frac{z\sqrt{\hat p(1-\hat p)/n + z^2/(4n^2)}}{1 + z^2/n}.
$$

**Tasks.**

1. Compute both intervals. Report them to four decimals.
2. Do the intervals overlap? Does that settle whether the difference is real? Explain in two sentences. (A two-proportion test on these counts gives a two-sided p-value near 0.025; you do not have to reproduce it.)
3. Compute the base-set size needed for a half-width of about 0.05 when $\hat p = 0.5$. Use $n \ge z^2\hat p(1-\hat p)/h^2$.
4. Configuration B uses 60 rows and reports 50% success. A second run on 60 new rows reports 33%. Without pooling, what should you conclude, and what would you do next?
5. A teammate reports "ASR = 0.3352" with no count. Given the LAB-03 base set of 522 rows, how many successes does that imply? Find one other fraction with a different denominator that also rounds to 0.3352, and explain why the missing base-set size is a reporting defect even when the rate has four decimals.
6. Write one sentence that reports configuration B with its interval, as it would appear in a lab report.

**Deliverable.** `work/m04/power.py` and a short note.

**Success criteria.** Both intervals are correct to four decimals; the overlap question distinguishes interval overlap from a hypothesis test; the sample-size calculation is shown; the final sentence includes n and a 95% interval.

---

## Portfolio checklist

- [ ] `fgsm_by_hand.py` with hand-checked values and a sign explanation
- [ ] `audit.md` with three correct counts and a rewritten claim
- [ ] `gatekeeper-memo.md` with a budget that sums to 5,000 or less
- [ ] `power.py` with two Wilson intervals and the sample-size calculation
- [ ] Five-line reflection: which number surprised you, which assumption is weakest, what you would test next

Then run [LAB-03](../../labs/lab-03.md) and [LAB-04](../../labs/lab-04.md) if you have not already. The labs produce the reproducible artifacts; these exercises produce the judgment you need to interpret them.
