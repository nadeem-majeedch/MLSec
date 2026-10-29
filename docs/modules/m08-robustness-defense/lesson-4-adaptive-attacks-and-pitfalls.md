# Lesson 08.4 — Adaptive Attacks and Evaluation Pitfalls

<a id="m08-l4"></a>

**Module 08 · Lesson 4 of 6 · 1.5 hours · LO-16**

## Scenario

A defense report claims: "Attack success rate 0.0% under PGD." You reproduce it and get 0.0% too. Then you read the code. The attack computes gradients through a `round` operation, uses a fixed step size of 0.01, and runs one restart. The defense is a quantizer.

Nothing in the report is false. The experiment simply cannot see the vulnerability. This lesson is about finding that gap deliberately, before an adversary does.

## Objectives

By the end of this lesson you will be able to:

1. Name the five families of obfuscated gradients and the symptom each produces.
2. Design an adaptive attack for a defense you can read the code of.
3. Audit a robustness claim against a checklist of evaluation pitfalls.
4. Distinguish "the attack failed" from "the attack could not run."
5. Report the strongest attack you found, including its cost and its failures.

## 1. The failure mode: a defense that hides its gradients

Athalye, Carlini, and Wagner (2018) audited defenses that had reported near-zero attack success and found a common pattern. The attack failed because the gradient was unusable, not because the model was robust. They named five mechanisms:

| Mechanism | What the defense does | Symptom in the attack |
|---|---|---|
| Shattered gradients | Non-differentiable operations: rounding, JPEG, quantization | Zero or meaningless gradients; attack does not move |
| Stochastic gradients | Random transforms, dropout at inference | Attack succeeds on some samples, fails on others; high variance |
| Vanishing or exploding gradients | Deep computation, saturation, many iterations of a transform | Gradient magnitude collapses or overflows |
| Numerical instability | Ill-conditioned operations, unstable exponents | `NaN`, `inf`, or wildly varying step behavior |
| Unreasonable regularization | Penalizes gradients themselves | Low attack success, but the model is not robust to other attacks |

The correction is not to abandon the defense. It is to build an attack that accounts for it. That is what "adaptive" means: the attacker knows the defense and optimizes against the actual deployed pipeline.

### LAB-11's example

The squeezing defense is a quantizer. A naive PGD attack that ignores it produces perturbations that mostly vanish at the rounding step. The attack appears weak.

The adaptive version uses BPDA: forward through the quantizer, identity gradient backward. The attack now moves. At ε = 0.10 it reaches ASR 0.1832, essentially the same as the naive 0.1871. At ε = 0.20 it reaches 0.9981, against 0.9571 for the naive attack.

Two lessons follow:

- The naive attack was already fairly strong at ε = 0.10 for a different reason: the quantizer removed the perturbation, so the attack had little to work with. The adaptive attack did not find a dramatically better route at that budget.
- At the stress budget, the adaptive attack clearly dominates. A defense evaluated only at ε = 0.10 with a naive attack would have missed that its protection evaporates.

The honest conclusion is not "squeezing is broken." It is "squeezing provides measurable protection at ε = 0.10 against these attacks and essentially none at ε = 0.20 against an adaptive attacker." That sentence has a scope.

## 2. Designing an adaptive attack

Work through the defense's code, not its description. For each operation between input and loss, ask what the attacker can do.

| Question | If the answer is yes | Attack technique |
|---|---|---|
| Is any step non-differentiable? | Rounding, clipping, argmax, sorting | BPDA with a differentiable substitute |
| Is any step random? | Random crop, noise, dropout | EOT: average gradients over samples |
| Is the input transformed before the model? | Resize, compress, denoise | Differentiate through the full pipeline, or approximate |
| Does the defense detect rather than transform? | Anomaly score, disagreement check | Optimize the detector score, not just the classifier loss |
| Is the model an ensemble? | Multiple models vote | Optimize the ensemble loss, or target the weakest member |
| Is the output discretized? | Top-1 label only | Use a surrogate or a score-based estimator |

Then tune the ordinary knobs: step size, number of steps, restarts, initialization, and the loss function.

### The adaptive-attack log

Keep a record. A claim without one is hard to trust.

```text
Defense: four-level input quantization before a logistic-regression classifier.
Attacker knowledge: source code, parameters, transform, threshold.
Attack: PGD with BPDA (identity backward through round), 20 steps,
        alpha = epsilon/5, 2 restarts, untargeted cross-entropy loss.
Budget: epsilon = 0.10 and 0.20, L-infinity.
Result: ASR 0.1832 at 0.10; ASR 0.9981 at 0.20.
Failed attempts: naive PGD at 0.10 reached 0.1871; a fixed-step attack
        with alpha = 0.01 reached 0.04 and was discarded as underpowered.
Residual doubt: BPDA is an approximation; a query-based attack or a
        better-tuned adaptive attack might do better at 0.10.
```

The "failed attempts" line matters. It shows the reader which attacks were tried and why the reported one is the strongest. Without it, a reader cannot tell whether the attacker stopped early.

## 3. The pitfalls checklist

Use this before believing any robustness number, including your own.

| Pitfall | How it looks | How to detect it | Correction |
|---|---|---|---|
| Weak attack | Low ASR, few steps, one restart | Attack hyperparameters look minimal | Increase steps, restarts, and tune step size |
| Gradient masking | ASR near zero, gradients near zero | Compare gradient norms with and without the defense | BPDA, EOT, or a gradient-free attack |
| Wrong base set | ASR computed over all rows | Denominator does not match clean-correct count | Recompute on clean-correct rows and report both |
| Tuning on test | Defense hyperparameters chosen on the test set | The test result is suspiciously stable | Split a validation set for defense tuning |
| One budget | A single ε | No curve and no stress point | Add at least one larger budget |
| Distribution mismatch | Defense applied only at serving | Training pipeline lacks the transform | Apply it in both, or measure the mismatch |
| Attack on training data | High ASR on rows the model memorized | Base rows overlap training indices | Evaluate on held-out rows |
| Unbounded perturbation | Attack changes inputs beyond the domain | Values outside [0, 1] or beyond ε | Clip to the domain and the ball |
| Label leakage | Attacker uses true labels to pick successes | Success is measured after filtering | Define the base set before the attack |
| Single seed | No variation reported | One number, no interval | Repeat and report spread |
| Cherry-picked model | Best of many runs reported | No selection procedure | Report all runs or a pre-registered rule |
| Detector evaluated alone | TPR quoted without FPR | No benign baseline | Report both and precision at a base rate |

### "The attack failed" versus "the attack could not run"

These are different results and require different language.

- **Failed:** the attack ran, produced valid inputs, and the model still predicted correctly. This is evidence for robustness at that budget.
- **Could not run:** the attack produced invalid inputs, `NaN` gradients, or no movement. This is evidence about the attack, not the defense.

LAB-11's naive attack on squeezing is a borderline case: it ran and produced valid inputs, but the transform discarded its work. The result is real for that attack; it is not a statement about adaptive attackers. Say which case you are in.

## 4. Worked audit: a suspicious claim

Suppose a report says:

> "Our preprocessing defense reduces PGD attack success from 40% to 1%. We evaluate with 5-step PGD at ε = 0.03, one restart, step size 0.001."

Apply the checklist.

1. **Budget:** ε = 0.03 is small. Is that the deployment threat model, or the budget that made the defense look good? Ask for a larger budget.
2. **Attack strength:** 5 steps at α = 0.001 covers at most 0.005 of the 0.03 budget. The attack cannot reach the boundary. This is an underpowered attack, not a robust model.
3. **Transform awareness:** if the defense is a quantizer with spacing 0.1, an ε = 0.03 perturbation cannot cross a cell. The result is arithmetically guaranteed, not empirical.
4. **Base set:** what is the 1% computed over? If the defense changes clean predictions, the base set changes.
5. **Clean cost:** what happened to accuracy on untouched inputs? Missing.
6. **Adaptive attempt:** was any attack designed for the transform? Missing.
7. **Scope:** one model, one dataset, two budgets. Fine as a lab demonstration; inadequate as a deployment claim.

The corrected experiment does not need to be expensive. It needs a budget at or above the transform's scale, an attack that can traverse it, an adaptive variant, and a clean baseline. LAB-11 does exactly these four things.

## 5. What a strong evaluation looks like

A strong empirical evaluation has these properties. None of them proves security; together they make a claim worth trusting.

- **A stated threat model.** Norm, budget, knowledge, and goal, before any numbers.
- **A clean baseline.** Clean accuracy and robust accuracy for every system.
- **A strong static attack.** Enough steps, tuned step size, multiple restarts.
- **An adaptive attack.** Designed for the defense, logged, and reported even when it is weaker.
- **A stress budget.** At least one budget beyond the defended range.
- **An honest base set.** Held-out rows, clean-correct filter, explicit denominator.
- **Repeatability.** Seeds, versions, and a command that reproduces the table.
- **A limitations paragraph.** What was not tried, and what that omission could hide.

AutoAttack (Croce and Hein, 2020) exists because individual research groups kept producing weak attacks. It ensembles parameter-free attacks so that evaluation variance is reduced. You are not required to run it in this course, but you should know why it exists: **the burden is on the evaluator to show the attack was strong, not on the reader to prove it was weak.**

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Declaring robustness after one attack | The attack is treated as the adversary | Add an adaptive attempt and a stress budget |
| Treating a failed gradient as a secure model | Zero ASR looks like success | Check gradient norms and use BPDA or EOT |
| Reporting the best of several adaptive attempts | The strongest number is tempting | Report all attempts and the strongest valid one |
| Tuning the attack on the test set | Convenient and invisible | Tune on a validation split; evaluate once |
| Ignoring attack cost | Steps and restarts are not reported | Report the compute budget of the attack |
| Calling an underpowered attack a "negative result" | The vocabulary is imprecise | Say the attack was underpowered |
| Skipping the clean baseline when the defense changes inputs | The comparison is inconvenient | Report the defended model's own clean accuracy |
| Assuming the published defense was evaluated correctly | Papers are trusted | Re-run the adaptive check yourself when it matters |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Gradients are all zero | Shattered gradients | BPDA or a gradient-free estimator |
| Attack works on some rows only | Stochastic defense | EOT with several samples per step |
| `NaN` loss during the adaptive attack | Numerical instability through the transform | Clip logits, use log-sum-exp, reduce step size |
| Adaptive attack is weaker than naive | Approximation or tuning problem | Tune step size and restarts; report both |
| ASR jumps when restarts increase | The single-restart attack was underpowered | Report the higher, valid result |
| Detector bypass succeeds easily | Detector optimized against a fixed attack | Optimize the detector score directly; retrain or raise the threshold |
| Reproduced ASR differs from the paper | Different budget, steps, or preprocessing | Compare the full attack configuration, not just ε |
| Attack succeeds only outside the domain | No clipping | Clip after every step |

## Check your understanding

1. Name three of the five obfuscated-gradient mechanisms and one symptom of each.
2. Why is an adaptive ASR lower than a naive ASR a warning sign rather than good news?
3. A report uses 5 PGD steps with α = 0.001 at ε = 0.03. What is wrong with the attack's reach?
4. What is the difference between "the attack failed" and "the attack could not run," and why does the difference matter in a report?
5. Give two reasons a defense tuned on the test set produces an optimistic number.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Obfuscated gradients make attacks fail for numerical reasons: shattered, stochastic, vanishing/exploding, unstable, or gradient-regularized.
- An adaptive attack knows the defense and optimizes through the real pipeline. BPDA and EOT are standard tools.
- LAB-11's adaptive attack matches the naive attack at ε = 0.10 and dominates at ε = 0.20, where ASR reaches 0.9981.
- Keep an adaptive-attack log with the attack, budget, results, failed attempts, and residual doubt.
- Use the pitfalls checklist: weak attack, wrong base set, tune-on-test, one budget, distribution mismatch, and the rest.
- "The attack failed" is evidence for one threat model; "the attack could not run" is evidence about the attack.
- Passing a test is not proof of security. A strong evaluation narrows the uncertainty; it does not eliminate it.

## Next

Continue to [Lesson 08.5 — Standardized evaluation and reproducibility](lesson-5-standardized-evaluation.md), where the evaluation becomes an artifact another person can rerun.
