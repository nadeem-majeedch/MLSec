# Answer Key — QZ-07

**Module 07 · 10 items · 12 points**

Use this key after attempting the quiz. For calculation items, the reasoning matters as much as the number.

## 1. (1 point) B — Membership inference

Membership inference decides whether a record was in the training set. Extraction copies the function; inversion reconstructs an input; label flipping corrupts training labels.

## 2. (1 point) A — Fidelity 0.90, task accuracy 0.60

Fidelity compares the surrogate with the **teacher**. Task accuracy compares the surrogate with the **true labels**. A surrogate can copy a weak or unusual teacher and agree with it more often than it agrees with the truth. The reverse is also possible.

## 3. (1 point) B — Cold start

With only 20 seed points, the temporary surrogate is close to guessing. Its entropy ranking does not identify genuinely informative regions, so the next 30 queries are poorly placed. Random sampling covers the space and wins at this budget. By 100 queries, the surrogate is good enough for entropy to help. The failure is a property of the budget, not a coding error.

## 4. (2 points) Precision ≈ 0.336

$$
\text{precision} =
\frac{\text{TPR}\cdot\pi}{\text{TPR}\cdot\pi + \text{FPR}\cdot(1-\pi)}
=
\frac{0.228 \times 0.10}{0.228 \times 0.10 + 0.05 \times 0.90}
=
\frac{0.0228}{0.0228 + 0.045}
=
\frac{0.0228}{0.0678}
\approx 0.336.
$$

Equivalently, in 10,000 candidates: 1,000 members and 9,000 nonmembers; $0.228 \times 1{,}000 = 228$ true flags and $0.05 \times 9{,}000 = 450$ false flags; $228 / 678 \approx 0.336$.

Award 1 point for the correct numerator and denominator, 1 point for the correct result with interpretation. The same attack at 1% prevalence has precision 0.044; the TPR and FPR did not change.

## 5. (1 point) B — AUC is threshold-free

AUC is the probability that a random member outranks a random nonmember. It averages over all thresholds, including ones that flag many nonmembers. The detection rate at a specific false-positive budget is the TPR at that FPR, which LAB-10 reports as 0.074 at 1% and 0.228 at 5%.

## 6. (2 points) Any three distinct reasons

Accept three of the following, one point for the first two and one for the third:

- **Overlap.** Member and nonmember confidence distributions overlap; many nonmembers are confident and many members are not.
- **Difficulty.** An easy example is classified confidently whether or not it was in training; confidence reflects difficulty as well as familiarity.
- **Atypical members.** A member that looks unusual can receive a low confidence despite having been seen in training.
- **Not a likelihood.** Maximum softmax probability is a heuristic, not the probability of membership; converting it requires both distributions and a base rate.
- **Calibration.** Confidence values are not guaranteed to be calibrated probabilities.
- **Threshold errors.** At the chosen threshold, a known fraction of nonmembers is flagged; an individual flag carries that error rate unless the prevalence is extreme.
- **Training accuracy is not the attack.** A member accuracy of 1.0 can coexist with heavy confidence overlap and a low TPR at a strict FPR.

Full credit requires distinct reasons, not three restatements of "the distributions overlap."

## 7. (1 point) B — The prior selects a plausible input

Many inputs can produce a high score for a class. The prior $R(x)$, weighted by $\lambda$, chooses among them by preferring inputs the attacker considers plausible. With a strong prior at the class mean, the result is the representative; with a prior at a member, the result moves toward that member. The model alone does not determine a unique input.

## 8. (1 point) B — Reduced signal, residual risk

Hard labels remove the fine-grained confidence that LAB-10 and the inversion example use. They do not remove the fact that each query returns a labelled point: extraction can proceed from labels, and membership or inversion attacks can use prediction stability, near-duplicate queries, or boundary search. The honest claim is "reduced under the tested attacks, with residual risk measured," not "eliminated."

## 9. (1 point) C — One score, one split, same-distribution nonmembers

LAB-10 uses maximum softmax confidence, a single 500/500 split at seed 31, and nonmembers drawn from the same digits dataset. It has no shadow models, no likelihood-ratio attack, no private data, and no deployed model.

## 10. (1 point) Any two missing elements

Accept any two of:

- the **operating point**: TPR at a stated FPR, not just AUC;
- the **base rate** and resulting precision;
- the **attack and access model**: query type, budget, auxiliary data;
- the **definition and measurement** of the 60% reduction: which attack, which metric, before and after;
- the **utility cost** of the defense;
- the **residual risk** and the limitations of the evaluation;
- the **population** and the harm model.

A suitable answer: "It does not state the FPR at which the TPR was measured or the base rate, so the AUC cannot be converted into a detection rate or a precision. It also does not say which attack the defense reduced by 60%, or at what utility cost."

## Score guide

| Score | Next step |
|---:|---|
| 11–12 | Start the exercises; write the memo in Exercise 3 |
| 8–10 | Review Lessons 07.2–07.4, then retake |
| 5–7 | Recompute the precision table in Lesson 07.5 and rerun LAB-10 |
| 0–4 | Work through the module in order, including both labs |
