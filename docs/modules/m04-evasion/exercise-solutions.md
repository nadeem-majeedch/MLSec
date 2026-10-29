# Module 04 Exercise Solutions

**Read after a first attempt.** These are model answers, not the only acceptable ones. Where an exercise asks for a judgment, the reasoning matters more than the exact wording.

---

## Exercise 1 — FGSM on a one-dimensional model

**Hand calculation.**

$$
s = 5(0.3) - 1 = 0.5, \qquad p_1 = \sigma(0.5) = 0.6225.
$$

For $J = -\log p_1$ and $s = wx + b$,

$$
\frac{\partial J}{\partial x} = (p_1 - 1)\,w = (0.6225 - 1)(5) = -1.8877.
$$

One step with $\epsilon = 0.12$:

$$
x' = 0.3 + 0.12\,\mathrm{sign}(-1.8877) = 0.18.
$$

$$
s' = 5(0.18) - 1 = -0.1, \qquad p_1' = \sigma(-0.1) = 0.4750.
$$

The prediction changes from class 1 (0.6225) to class 0 (0.4750). The loss rises from 0.4741 to 0.7444.

**Smallest flipping ε.** The boundary is where $s = 0$:

$$
5(0.3 - \epsilon) - 1 = 0 \;\Rightarrow\; \epsilon = 0.1.
$$

FGSM with ε = 0.12 uses the full budget in one step, so it passes the boundary by 0.02. FGSM is not a minimal-distance attack; DeepFool and C&W address that different question.

**Code.**

```python
import math

w, b, x, eps = 5.0, -1.0, 0.3, 0.12
s = w * x + b
p = 1.0 / (1.0 + math.exp(-s))
g = (p - 1.0) * w
x2 = x + eps * math.copysign(1.0, g)
s2 = w * x2 + b
p2 = 1.0 / (1.0 + math.exp(-s2))

print(f"s={s:.4f} p={p:.4f} grad={g:.4f}")
print(f"x'={x2:.4f} s'={s2:.4f} p'={p2:.4f}")
print(f"loss {(-math.log(p)):.4f} -> {(-math.log(p2)):.4f}")
print(f"min eps={s / w:.4f}")
```

```
s=0.5000 p=0.6225 grad=-1.8877
x'=0.1800 s'=-0.1000 p'=0.4750
loss 0.4741 -> 0.7444
min eps=0.1000
```

**Is it a successful attack?** Yes under this module's definition: the predicted class changed. The loss increase alone would not be enough, because a loss can rise while the argmax stays the same. The probability is only slightly below 0.5, so the example is a boundary crossing, not a confident misclassification into class 0.

---

## Exercise 2 — Audit a flawed attack claim

**1. The counts.**

The clean model gets $0.9667 \times 540 = 522$ rows right and $540 - 522 = 18$ rows wrong.

- Over the base set: $175/522 = 0.3352$ (33.5%).
- Over all test rows: $175/540 = 0.3241$ (32.4%).
- Counting already-wrong rows as successes: $(175 + 18)/540 = 193/540 = 0.3574$ (35.7%).

**2. The inflation.** An attack success is a row whose prediction *changed as intended*, so it must start from a correct prediction. The 18 rows the clean model already got wrong cannot demonstrate anything about the attack. Adding them raises the numerator by 18 and changes the denominator to all rows, producing 35.7% instead of the honest 33.5%. The inflated number is larger only because the report counts pre-existing errors as attack effects.

**3. Robust accuracy.** If only the 522 clean-correct rows are perturbed, 175 of them become wrong and 347 stay correct. The 18 already-wrong rows are not attacked and remain wrong.

$$
\text{robust accuracy} = \frac{347}{540} = 0.6426.
$$

$$
\text{accuracy drop} = 0.9667 - 0.6426 = 0.3241 \;\text{(32.4 points)}.
$$

ASR divides by the base set (522); accuracy drop divides by all rows (540). The attack changes 33.5% of the rows it targets, which is 32.4% of the test set. Neither number is "35.7 points."

**4. Missing information (any three).**

- The perturbation norm and budget, and whether clipping to [0, 1] was applied.
- The definition and size of the base set.
- The attack implementation, sign convention, step size, and random seed.
- The model, split, and preprocessing needed to reproduce it.
- Whether the report measured perturbation before or after any normalization.

**5. Rewritten claim.**

> On the 522 test images the model classified correctly, FGSM at L∞ ε = 0.10 changed 175 predictions, an attack success rate of 33.5% (base set 522 of 540). Robust accuracy on the full test set was 64.3%, 32.4 points below clean accuracy.

**6. Extra evidence.** The deployment decision needs the threat model: whether an adversary can control the camera pixels at inference, under what physical constraints, with what knowledge of the model, and what harm a wrong decision causes. A better attack number on the same toy setup would not answer that.

---

## Exercise 3 — GateKeeper vendor claim

**1. Budget arithmetic.**

$$
\epsilon = 8/255 = 0.0314.
$$

That is up to 8 gray levels per channel. If all $224 \times 224 = 50{,}176$ pixels move by ε, the L2 norm is

$$
\|\delta\|_2 = \sqrt{50{,}176} \times \frac{8}{255} = 224 \times 0.0314 = 7.03.
$$

Per channel the change looks tiny; over fifty thousand coordinates it is a norm of about 7. "Small" is always small **in a stated norm**, and the L∞ description hides the aggregate size.

**2. Why 200 noise trials do not establish robustness.**

- **Method.** Random noise is not an adversarial search. In a high-dimensional space it almost never crosses a decision boundary; an optimizing attacker chooses directions using the model's responses.
- **Evidence.** The trial reports no base set, no norm, and no ε, and 200 trials with zero successes only bound the failure rate at about 1.5% (95% upper bound for 0/200). A rare but real failure would be missed.

**3. A transfer-based test within 5,000 queries.**

| Step | Queries |
|---|---:|
| Collect labels for a surrogate training set | 3,000 |
| Measure transfer on the 500 held-out photographs | 500 |
| Optional second surrogate (different architecture or preprocessing) | 1,000 |
| Retry margin | 500 |
| **Total** | **5,000** |

Procedure: collect 3,000 labelled photographs spanning the classes, train a surrogate on them, craft L∞ ε = 8/255 examples on the surrogate with PGD, then query the vendor API once per held-out photograph and record whether the top-1 label changes. The measurement set stays fixed, so every configuration is compared on the same 500 rows.

**4. Pre-registered rule.** Treat a transfer ASR of 10% or more on the 500 held-out photographs (50 or more changed predictions) as material, because a gate that misreads one code in ten is operationally unacceptable even if clean accuracy is 99%.

**5. Recommendation.**

> We accept the vendor's clean-accuracy number only for the test distribution they describe, which we have not independently verified. We reject the robustness claim: 200 random-noise trials do not test an optimizing adversary and do not state a budget or base set. We require a white-box PGD evaluation at ε = 8/255 with a defined base set from the vendor, plus the black-box transfer test above before deployment. Residual risk: if transfer success is low, a query-based attack with a larger budget or a physically captured perturbation may still succeed, and our test bounds only the methods and budget we ran.

**6. Quantization.** Rounding to 5 bits removes the low-order bits that small perturbations use, which can reduce transfer success and sometimes breaks gradient-based optimization. It is not a robustness guarantee: an attacker can optimize with the quantization in the loop (for example, averaging over rounding), and the control may simply push the attack to a larger budget. The cost is a loss of clean accuracy on low-contrast or poorly lit codes, plus a new preprocessing step to validate.

---

## Exercise 4 — Uncertainty and budget arithmetic

**1. Wilson intervals.**

For A (18/60, $\hat p = 0.3$): center 0.3120, half-width 0.1131, interval **[0.1990, 0.4251]**.  
For B (30/60, $\hat p = 0.5$): center 0.5000, half-width 0.1227, interval **[0.3773, 0.6227]**.

**2. Overlap.** The intervals overlap: B's lower bound (0.3773) is below A's upper bound (0.4251). That does not settle the question, because each interval is a statement about one proportion, not about their difference; overlapping intervals are a conservative screen and can coexist with a real difference. A two-proportion test gives p ≈ 0.025, so the difference is significant at the 5% level — but with 60 rows per group the estimate is fragile.

**3. Sample size for a ±0.05 half-width.**

$$
n \ge \frac{1.96^2 \times 0.5 \times 0.5}{0.05^2} = 384.16 \;\Rightarrow\; 385.
$$

Sixty rows cannot resolve a 10-point difference; the interval is more than twice that wide.

**4. Two runs, 30/60 and 20/60.** Do not choose the better run. Pooled, the result is 50/120 = 41.7%, and both runs are compatible with one underlying rate. Either report the pooled estimate with its interval or run a new pre-registered test with enough rows; selecting the higher run is a reporting bias.

**5. Recovering the count.** With a 522-row base set, $0.3352 \times 522 = 175.0$, so 175 successes. The rate alone does not identify the evidence: 59 of 176 also rounds to 0.3352, and a 176-row base set would carry a much wider interval than a 522-row one. Reporting the rate without the count hides the uncertainty and prevents anyone from checking the arithmetic.

**6. Reporting sentence.** "Configuration B changed 30 of 60 base-set predictions (ASR = 50.0%, 95% Wilson CI [37.7%, 62.3%])."

---

## Notes on grading

| Exercise | Common weak answer | What earns credit |
|---|---|---|
| 1 | States the sign but cannot say why | Connects the sign to the L∞ budget and linear approximation |
| 2 | Recomputes 175/522 but keeps the "35.7 points" language | Separates ASR denominator from accuracy-drop denominator |
| 3 | Says "random noise is weak" and stops | Adds the quantitative bound and a budgeted alternative design |
| 4 | Says "the intervals overlap, so there is no difference" | Distinguishes interval overlap from a test of the difference |
