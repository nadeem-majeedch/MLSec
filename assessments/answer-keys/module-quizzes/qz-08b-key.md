# QZ-08B Answer Key — Module 08

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — PGD result on this test set

An empirical result reports what a specific attack achieved on a specific test set. A certified result makes a statement over all inputs in a declared region, usually with a proof or a bound.

- **A, C, and D** are universal claims. They may be true, but they are not established by running an attack and observing accuracy.
- **B** is appropriately scoped to the attack, budget, and test set.

Tag: M08 · LO-16 · Bloom 2 · D1.

## 2. A — lower clean accuracy, higher robust accuracy

Adversarial training optimizes against worst-case perturbations within a budget. That usually costs some clean accuracy, because the model spends capacity on the robust region rather than only on the clean distribution. The trade-off is measured, not assumed; the lab reports both numbers.

- **B** describes a free lunch that the evidence does not support.
- **C** is false: robust training does not remove the need to evaluate attacks.
- **D** is false: training is not a guarantee against future or adaptive attacks.

Tag: M08 · LO-17 · Bloom 2 · D1.

## 3. False

A single failed attack is a lower bound on attacker capability, not a proof of robustness. The attack may be underpowered, and the defense may mask gradients or otherwise break the attack without removing the vulnerability. An adaptive attack is required before the claim can be treated as evidence.

Tag: M08 · LO-18 · Bloom 2 · D1.

## 4. False

Squeezing typically involves quantization or rounding, which has zero or undefined gradients almost everywhere. A standard PGD attack therefore cannot optimize through it and may fail for reasons unrelated to robustness. BPDA uses the true transform in the forward pass and a differentiable substitute in the backward pass to evaluate the defense fairly.

Tag: M08 · LO-18 · Bloom 2 · D1.

## 5. Required element

Gradient masking is any defense that hides, distorts, or randomizes the gradient signal so gradient-based attacks fail without the underlying decision boundary becoming robust. It can make ASR look low while a transfer, score-based, or BPDA attack still succeeds, so a defense that reports a large drop under one gradient attack must be tested adaptively.

Tag: M08 · LO-16 · Bloom 2 · D1.

## 6. TP = 180; FP = 98; precision ≈ 0.647

- Attacked inputs: $0.02 \times 10{,}000 = 200$. True positives: $0.90 \times 200 = 180$.
- Benign inputs: 9,800. False positives: $0.01 \times 9{,}800 = 98$.
- Alerts: $180 + 98 = 278$. Precision: $180/278 \approx 0.647$, or **64.7%**.

At a 1% base rate the same detector would have much lower precision even though TPR and FPR are unchanged. Precision depends on prevalence, so a detector report without the deployment base rate is incomplete.

Tag: M08 · LO-18 · Bloom 3 · D2.

## 7. Required elements (two flaws and the overstatement)

Two of:

- **The attack never sees the defense.** `pgd_attack` runs on the raw model, and `squeeze` is applied only afterward. That is a static attack against the undefended model, not an adaptive attack against the deployed pipeline.
- **No differentiable substitute is used.** Squeeze is typically non-differentiable; without BPDA or a similar approximation, the evaluation cannot tell whether the defense is robust or merely blocks the gradient.
- **The denominator is the whole test set.** Robust accuracy should use the same fixed population as the claim, and the clean-correct base set should be reported; pooling all rows hides clean errors.
- **There is no clean baseline or budget check.** The code does not report clean accuracy, the actual perturbation size, or whether inputs stayed in the valid range.

The reported robust accuracy overstates robustness because a defense-aware attacker could optimize through or around the squeeze, and the lab shows that an adaptive attack can recover most of the success at a larger budget.

Tag: M08 · LO-18 · Bloom 4 · D3.

## 8. Required elements (three questions and a bounded rewrite)

Questions such as:

- **Exact budget and norm:** what ε, norm, and input scale? "A fixed budget" is not a number, and relative improvement cannot be compared without it.
- **Attack strength and adaptivity:** was the attack adapted to the defense? FGSM alone is weak; without PGD, restarts, or an adaptive attempt, 0.8% is a lower bound on attack success, not an upper bound.
- **Metric and denominator:** is 42% → 0.8% on all test rows or on a clean-correct base set, and how many rows is that? What is the confidence interval?
- **Clean cost:** what happened to clean accuracy? A defense that destroys utility can trivially reduce attack success.
- **Certified or empirical:** the result is empirical on one test set; it is not a guarantee for other inputs or budgets.

A supportable rewrite:

> Under FGSM at the stated L∞ budget on this test set, attack success fell from 42% to 0.8% (41.2 percentage points), while clean accuracy changed from X to Y. This is an empirical result against a non-adaptive attack; no adaptive evaluation or certified bound was performed, so it does not establish robustness against a defense-aware attacker.

The rewrite must include the budget, the base set, the clean cost, and the non-adaptive limitation. "Improves robustness by 98%" without those is a marketing relative change, not a security measurement.

Tag: M08 · LO-16 · Bloom 5 · D3.
