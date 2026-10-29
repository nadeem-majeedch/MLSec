# Lesson 08.3 — Input Preprocessing and Detection Defenses

<a id="m08-l3"></a>

**Module 08 · Lesson 3 of 6 · 1.5 hours · LO-18**

## Scenario

A colleague proposes a cheap fix: round every input pixel to four levels before classification. "The perturbation is tiny," she says, "so rounding erases it. Our attack success drops from 36% to 19%, and we do not have to retrain."

The result is real. The interpretation is not. Rounding removes small changes by discarding precision — including precision the model needs for clean inputs. It also creates a new decision boundary that an attacker can target on purpose.

This lesson separates three questions that are often merged: does the transform reduce attack success, what does it cost on benign inputs, and does it survive an attacker who knows the transform is there?

## Objectives

By the end of this lesson you will be able to:

1. Classify a preprocessing defense by what it does: remove precision, remove structure, or detect anomaly.
2. Evaluate a transform on clean utility, naive-attack success, and adaptive-attack success.
3. Explain BPDA and why a non-differentiable transform is not a security boundary.
4. Account for detector false positives and the base rate at which they matter.
5. State the residual risk of a preprocessing control in a defense-in-depth design.

## 1. Three families, three failure modes

Preprocessing defenses sit between the input and the model. They do not change the weights.

| Family | Example | Mechanism | Typical failure |
|---|---|---|---|
| Precision reduction | Bit-depth squeezing, quantization | Removes small perturbations by coarsening values | Destroys benign detail; attacker targets quantization cells |
| Structure removal | Blurring, downscaling, JPEG compression, PCA | Removes high-frequency content where perturbations live | Removes real signal; adaptive attack optimizes through the transform |
| Anomaly detection | Feature squeezing comparison, autoencoder residual, input validator | Flags inputs that look unusual | False positives on rare benign inputs; attacker optimizes to look normal |

A detector is not a classifier of truth. It is a second model with its own error rates, and its output changes the system's behavior: reject, review, or fall back. That decision has a cost even when the detector is right.

### The threat model you are evaluating

For any of these, write the tuple before measuring:

- **What does the defense transform?** Input only, or input and training?
- **What does the attacker know?** That the transform exists, its parameters, and its code?
- **What can the attacker optimize?** A loss through the transform, or only queries to the full pipeline?
- **What counts as success?** A wrong label after the transform, or also a rejection that denies service?

Most published preprocessing defenses fail because the attacker was allowed to know the transform. Assume that. A transform hidden in code is not a secret; it is a delay.

## 2. What LAB-11 measures

LAB-11 implements **input squeezing**: every pixel in [0, 1] is snapped to a four-level grid.

```python
def squeeze(X, levels=4):
    return np.clip(np.round(X * (levels - 1)) / (levels - 1), 0.0, 1.0)
```

The test set is evaluated three ways:

1. **Clean utility:** predictions on squeezed clean inputs, compared with true labels.
2. **Naive attack:** PGD is run on the undefended model against raw inputs; the resulting examples are squeezed and then classified.
3. **Adaptive attack:** PGD optimizes through the transform using a straight-through gradient, so the attacker accounts for squeezing.

### The measured table

| Condition | Clean acc. | Robust acc. | ASR | Base size |
|---|---:|---:|---:|---:|
| Undefended, no transform | 0.9667 | 0.6204 | 0.3582 | 522 |
| Squeezed, naive attack | 0.9500 | 0.7722 | 0.1871 | 513 |
| Squeezed, adaptive attack | 0.9500 | ≈0.7759 | 0.1832 | 513 |

The naive result looks like a strong defense: ASR falls from 0.3582 to 0.1871, and robust accuracy rises from 0.6204 to 0.7722. The cost is 1.67 points of clean accuracy: 14 rows that the undefended model classified correctly are now wrong.

Then look more carefully.

- The adaptive attack reaches ASR 0.1832 — **slightly lower** than the naive attack at this budget. That is not evidence that squeezing is safer than the naive number suggests. It means the straight-through attack was not tuned well enough to dominate the naive one at ε = 0.10. An adaptive result that is weaker than the naive result is a signal to improve the attack, not a reason to relax.
- The quantizer's grid spacing is \(1/3 \approx 0.333\), far larger than ε = 0.10. Most perturbations cannot move a pixel across a cell boundary, which is why the naive attack struggles. This is precision destruction, not robustness in the model.
- The transform changes the model's input distribution. The 0.9500 clean accuracy is the honest utility number, not 0.9667.

### The stress budget

At ε = 0.20 the picture reverses:

| Condition | ASR | Robust acc. |
|---|---:|---:|
| Squeezed, naive attack | 0.9571 | — |
| Squeezed, adaptive attack | 0.9981 | 0.0019 |

The adaptive attacker now breaks virtually every base-set prediction. Robust accuracy is 0.0019 — roughly one correct row in 540. The transform that looked like a defense at ε = 0.10 provides essentially nothing at ε = 0.20 once the attacker optimizes through it.

This is the lesson in one comparison: **a preprocessing defense has an operating range, and the naive attack can understate the attacker's ability inside that range while the stress budget reveals the boundary.**

## 3. BPDA in plain language

The derivative of a rounding step is zero almost everywhere. If an attacker computes gradients through `round`, the gradient is zero almost everywhere too, and PGD cannot move. A defense that relies on this is a case of **shattered gradients**: the attack fails for a numerical reason, not because the model is robust.

**Backward pass differentiable approximation (BPDA)**, introduced in the obfuscated-gradients work of Athalye et al. (2018), attacks such a transform by using the true transform in the forward pass and a differentiable substitute in the backward pass. LAB-11 uses the identity: forward `squeeze(x)`, backward treat `d squeeze / d x = 1`.

```python
grad = input_gradient(model, squeeze(x_adv), y)   # forward through the quantizer
x_adv = clip(x_adv + alpha * sign(grad), X - eps, X + eps)
```

The attacker is now optimizing a surrogate gradient of the true pipeline. It is not guaranteed to be optimal, which is exactly why an adaptive ASR below the naive ASR is a warning about attack quality rather than a property of the defense.

BPDA is one member of a family. Expectation over transformation (EOT) averages gradients over randomized transforms when the defense is stochastic. Neither is a complete adaptive-attack methodology; both are tools for building one.

## 4. Detection is a different product

A preprocessing **transform** changes the input for everyone. A **detector** decides per input whether to trust it. The feature-squeezing detector of Xu et al. (2017) compares a model's predictions on the original and squeezed input; a large disagreement is treated as evidence of an adversarial example.

That design has an obvious cost: benign inputs near a decision boundary also disagree. The detector's false-positive rate on clean data is part of its specification, not an implementation detail.

Carlini and Wagner (2017) showed that detection defenses are hard to evaluate: a detector tuned against one attack can often be circumvented by an adaptive attack that optimizes the detector's own score. The lesson is not that detection is useless. It is that a detector must be evaluated as a classifier under attack, with:

| Quantity | Question |
|---|---|
| True positive rate | Of attacked inputs, what fraction are flagged? |
| False positive rate | Of clean inputs, what fraction are flagged? |
| Base rate | In deployment, how many inputs are actually attacked? |
| Cost of a false positive | What happens to a legitimate user who is rejected? |
| Cost of a false negative | What happens when an attacked input passes? |
| Adaptive bypass | Can the attacker optimize to be classified as benign? |

At a 1% attack prevalence, even a 5% false-positive rate means most flags are benign. Precision, not accuracy, is the number the operations team experiences. Lesson 07.3 made the same argument for membership inference; the arithmetic is identical.

LAB-11 does not implement a detector, so it does not report these numbers. If you propose one, you own the measurement.

## 5. Utility, latency, and operations

Preprocessing is often sold as "free" because it needs no retraining. It is not free.

| Cost | What to measure | LAB-11 evidence |
|---|---|---|
| Clean accuracy | Accuracy after the transform on untouched inputs | 0.9667 → 0.9500 |
| Latency | Added per-request compute | Not measured; one vectorized rounding pass in this lab |
| Tuning burden | Levels, kernel size, threshold | Four levels chosen by the lab, not optimized |
| Distribution shift | Transform applied at serving but not training | The model was trained on unsqueezed inputs |
| Interaction with other controls | Transform before or after validation | Not tested |

The distribution-shift row deserves emphasis. The model in LAB-11 was trained on continuous pixel values and deployed on a four-level grid. A model trained with the transform in the pipeline would see a consistent distribution, and its clean accuracy might differ. The lab measures the deployed-transform case, which is common in practice and often overlooked.

If the transform is applied during training and serving, it becomes part of the model's preprocessing contract. Then it must be versioned with the model, and a mismatch between training and serving transforms is a silent failure mode.

## 6. Defense in depth: where preprocessing belongs

A defensible architecture uses preprocessing as one layer among several, and states what each layer is for.

| Layer | Control | What it can do | What it cannot do |
|---|---|---|---|
| Input | Schema and domain validation | Reject malformed or out-of-range inputs | Recognize a well-formed adversarial input |
| Preprocessing | Squeezing or denoising | Remove some small perturbations; reduce attack surface | Guarantee robustness; preserve all benign detail |
| Detection | Disagreement or anomaly score | Raise the cost of an attack; route suspicious inputs | Avoid false positives; resist an adaptive attacker |
| Model | Adversarial training | Improve robustness inside a stated budget | Cover larger budgets or other norms |
| Operations | Rate limits, monitoring, review | Limit query budgets; detect campaigns | Stop a single well-crafted input |

The important sentence in a design review is not "we squeeze inputs." It is: "squeezing reduces naive ASR at ε = 0.10 from 0.36 to 0.19 at a cost of 1.7 points of clean accuracy, and it fails at ε = 0.20 under an adaptive attack; it is a speed bump, not a boundary, and the boundary control is adversarial training plus rate limiting."

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reporting only naive ASR | The transform is treated as opaque to the attacker | Add an adaptive attack that knows the transform |
| Comparing squeezed accuracy to unsqueezed clean accuracy | The baseline is convenient | Report the defended model's own clean accuracy |
| Treating 0 ASR against a gradient attack as robustness | Gradients were destroyed | Use BPDA or a query-based attack |
| Ignoring false positives | Only attack success is measured | Report clean rejection rate and precision at a stated base rate |
| Hiding the transform | "Security by obscurity" | Assume the attacker has the code; publish the defense in the threat model |
| Applying the transform only at serving | Training and serving differ | Version the preprocessing with the model |
| Quoting one budget | The result is convenient | Add a stress budget and report the boundary |
| Calling a detector "validation" | The words are conflated | Validation enforces a contract; detection estimates intent |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Adaptive ASR is lower than naive ASR | Adaptive attack is under-tuned | Tune step size, restarts, and initialization; report the weaker result honestly |
| Squeezing gives 0% ASR at ε = 0 | Inputs changed by the transform | Compare predictions before and after with no perturbation |
| Clean accuracy drops sharply | Grid too coarse or transform too aggressive | Sweep levels and report the utility curve |
| Attack succeeds only at cell boundaries | Expected behavior of quantization | That is the adaptive attack's strategy, not a bug |
| Detector flags many benign rows | Threshold chosen on attacked data | Choose the threshold on clean validation data at a stated FPR |
| Same transform, different results | Random initialization or tie-breaking in rounding | Fix seeds; use deterministic rounding |
| Model performs worse than before deployment | Training/serving preprocessing mismatch | Log the transform version and input statistics |
| Squeezed robust accuracy exceeds clean accuracy | Base-set or label error | Recompute counts; robust accuracy cannot exceed clean accuracy on the same rows |

## Check your understanding

1. Why does rounding to four levels reduce naive PGD success at ε = 0.10?
2. What is BPDA, and why does the true derivative of `round` stop a gradient attack?
3. Squeezing costs 14 clean-correct rows out of 540. Express that as a percentage-point loss.
4. A detector has TPR 0.90 and FPR 0.05. At a 1% attack prevalence, what fraction of alerts are real attacks? (Compute it.)
5. Give one reason a squeezed model can be less accurate than the model it protects, and one reason it can be more robust in a narrow range.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Preprocessing defenses remove precision or structure, or detect anomalies. Each has a characteristic failure.
- LAB-11's four-level squeezing cuts naive ASR at ε = 0.10 from 0.3582 to 0.1871 at a cost of 1.67 points of clean accuracy.
- The adaptive BPDA attack reaches 0.1832 at ε = 0.10; a slightly weaker adaptive result is a warning about the attack, not proof of safety.
- At ε = 0.20 the adaptive attack reaches ASR 0.9981 and robust accuracy 0.0019. The transform has an operating range and no guarantee outside it.
- Non-differentiable transforms cause shattered gradients; BPDA and EOT are ways to attack through them.
- Detection is a classifier with false positives. Report TPR, FPR, base rate, and adaptive bypass.
- Preprocessing is one layer in a defense-in-depth design, not a security boundary.

## Next

Continue to [Lesson 08.4 — Adaptive attacks and evaluation pitfalls](lesson-4-adaptive-attacks-and-pitfalls.md), where you build the attacker that a defense author did not anticipate.
