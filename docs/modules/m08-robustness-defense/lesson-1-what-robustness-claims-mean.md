# Lesson 08.1 — What Robustness Claims Mean

<a id="m08-l1"></a>

**Module 08 · Lesson 1 of 6 · 1.5 hours · LO-16**

## Scenario

A vendor sends a one-page summary: "Our classifier is robust. Attack success is only 18%." Your team is about to approve it for a loan-triage workflow where a wrong decision is expensive.

You ask four questions. Against which attack? At what perturbation budget? On which inputs? And what happened to accuracy on clean inputs? The vendor's answer is "PGD, small perturbations, the test set, and accuracy is fine."

None of those answers is precise enough to approve or reject the claim. This lesson gives you the vocabulary to turn the summary into a testable statement.

## Objectives

By the end of this lesson you will be able to:

1. Write a robustness claim with five parts: model, adversary, norm and budget, base set, and metric.
2. Compute clean accuracy, robust accuracy, and ASR from a confusion-style count and explain why they are not interchangeable.
3. Explain why the base set is usually the clean-correct rows and what changes when it is not.
4. Distinguish an empirical result from a certified guarantee.
5. State the limitations of a single-budget evaluation.

## 1. A claim is a tuple, not an adjective

"Robust" has no measurable meaning on its own. Make it a tuple:

| Part | Question | Example |
|---|---|---|
| Model | Which exact artifact and version? | `digits-logreg-v2`, trained on split seed 42 |
| Adversary | What may the attacker change, and what do they know? | L∞ perturbation, white-box gradients |
| Budget | How large may the change be? | ε = 0.10 on features scaled to [0, 1] |
| Base set | Which rows are counted? | The 522 test rows the model classified correctly |
| Metric | What is measured? | Robust accuracy and ASR under 20-step PGD with 2 restarts |

A complete claim looks like this:

> On the 522 clean-correct digits test rows, the undefended model drops from 96.67% clean accuracy to 62.04% robust accuracy under a 20-step, 2-restart PGD attack with ε = 0.10 in L∞, giving an ASR of 35.82%. This is an empirical result for a white-box attacker at that budget; it is not a guarantee for other norms, budgets, or models.

That sentence can be checked. The vendor's sentence cannot.

### Knowledge and capability matter

Two attacks at the same budget can have very different success rates depending on what the attacker knows:

- **White-box:** gradients, architecture, and parameters are available.
- **Black-box, score-based:** only the returned probabilities or scores are available.
- **Black-box, label-only:** only the predicted class is returned.
- **Transfer:** the attacker builds a surrogate and applies perturbations to a target it never differentiates.

A robustness claim for a white-box attacker is a stronger statement than the same number for a label-only attacker. Say which one you measured.

## 2. Three numbers that are easy to confuse

Let:

- \(N\) = number of test rows;
- \(C\) = number of rows the model classifies correctly before any attack;
- \(S\) = number of rows in the base set whose prediction the attack successfully changes.

Then:

\[
\text{clean accuracy} = \frac{C}{N}
\]

\[
\text{ASR} = \frac{S}{C}
\]

\[
\text{robust accuracy} = \frac{C - S}{N}
\]

The denominators differ on purpose. ASR asks, "of the rows the model could get right, how many can the attacker break?" Robust accuracy asks, "of all rows, how many survive?" Mixing the denominators produces numbers that look precise and mean nothing.

### Worked example with LAB-11 numbers

LAB-11 uses the 540-row digits test set. The undefended model gets 522 rows correct:

\[
\text{clean accuracy} = 522 / 540 = 0.9667
\]

PGD at ε = 0.10 changes 187 of those 522 predictions:

\[
\text{ASR} = 187 / 522 = 0.3582
\]

\[
\text{robust accuracy} = (522 - 187) / 540 = 335 / 540 = 0.6204
\]

Now check the arithmetic yourself. If someone reports ASR 0.3582 and robust accuracy 0.6204 without the base size, you cannot tell whether the denominators are consistent. With the base size, you can.

A useful sanity check: \(S = C - \text{robust correct}\), and \(\text{robust accuracy} \times N = C - S\). If the numbers do not close, one of them is wrong.

### What if the base set is all test rows?

Some evaluations compute ASR over every row, including rows the model already misclassified. That answers a different question: "of all inputs, how many end up wrong after the attack?" It can be a legitimate metric, but it is not the same as "how often does the attack break a correct prediction?" Label it explicitly.

For a model with 90% clean accuracy, the two denominators differ by 10%. For a weak model, the difference is much larger. The base-set choice is part of the claim.

## 3. Empirical versus certified

An **empirical** robustness result says: "this attack, run this way, failed on these inputs." It is evidence. It is not a guarantee, because a stronger attack may exist.

A **certified** result says: "for every input within radius \(r\), under a stated norm, the prediction is unchanged." Randomized smoothing (Cohen et al., 2019) is the standard example: it produces a per-input radius with a probabilistic guarantee, and it may abstain when the evidence is insufficient. Certification is stronger but usually covers a smaller radius and costs many forward passes.

This module measures empirical robustness. It does not certify. When you read "robust" in a paper or vendor document, ask which of the two is being claimed. A certificate for radius 0.25 does not cover an attack at ε = 1.0, and an empirical result at ε = 0.10 does not imply a certificate at any radius.

| Claim type | Strength | What it does not cover |
|---|---|---|
| Empirical, one attack | Evidence for that attack and budget | Stronger or adaptive attacks |
| Empirical, ensemble of attacks | Stronger evidence | Unknown attacks and larger budgets |
| Certified, per input | Guarantee within the certified radius | Larger radii, other norms, inputs outside the certificate |
| Leaderboard rank | Comparable result under a benchmark protocol | Your data, your deployment, your adversary |

## 4. One budget is not a curve

A defense can look excellent at ε = 0.10 and fail at ε = 0.20. LAB-11 demonstrates exactly this. Input squeezing reduces ASR to 0.1871 at ε = 0.10, but at ε = 0.20 the same style of attack succeeds 95.71% of the time and robust accuracy falls to 0.19%.

The honest way to report this is a table or curve, not a single number:

| Model | Clean acc. | Robust acc. at ε = 0.10 | ASR at ε = 0.10 | ASR at ε = 0.20 |
|---|---:|---:|---:|---:|
| Undefended | 0.9667 | 0.6204 | 0.3582 | 0.9579 |
| Adversarial training | 0.8907 | 0.7296 | 0.1809 | 0.6029 |
| Input squeezing | 0.9500 | 0.7722 | 0.1871 | 0.9571 |

The table tells a different story from any single row. Adversarial training is the only defense that keeps meaningful robustness at the larger budget, and it pays 7.6 points of clean accuracy. Squeezing is attractive at the smaller budget and collapses outside it. Both facts belong in the report.

## 5. Base-set hygiene checklist

Before you trust any ASR number, check:

1. **Was the attack applied to the test set, or to training rows?** Training rows are not evidence of generalization.
2. **Was the model's prediction on the clean input recorded before the attack?** Without it, you cannot compute the base set.
3. **Are rows the model already got wrong excluded?** If not, say so.
4. **Is the perturbation valid?** Features must stay in the allowed domain, and the perturbation must stay inside the budget.
5. **Was ε = 0 tested?** An attack that changes predictions at zero budget has a bug.
6. **Is the attack's success definition explicit?** Untargeted means "any wrong class"; targeted means "a specific wrong class."
7. **Is the base size reported?** A rate without a denominator is not reproducible.

## 6. A template you can reuse

Use this in lab reports and reviews:

```text
Claim: On <base set, N=...>, <model and version> has clean accuracy ... .
Under <attack, steps, restarts, knowledge> at <norm> budget epsilon=..., its robust
accuracy is ... and ASR is ... . The attack did/did not include an adaptive attempt
against <defense>. This is an empirical result; it does not certify robustness at
any radius, and it does not cover <out-of-scope conditions>.
```

If a sentence cannot be completed with a number, a base set, and a budget, it is not a robustness claim yet.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| "ASR is 18%" with no denominator | The metric is copied from a summary | Ask for base size and clean accuracy |
| Comparing ASR across different base sets | Two experiments used different filters | Normalize to the same clean-correct set or report both |
| Reporting robust accuracy as if it were clean accuracy | The numbers are close in some runs | Label every column with its condition |
| Treating a certified radius as a budget | The units and norm differ | State the norm, radius, and coverage |
| Calling a single-budget result "robustness" | The experiment stopped at one ε | Add a stress budget or state the scope |
| Ignoring attack hyperparameters | The attack was underpowered | Report steps, step size, restarts, and any tuning |
| Using training rows | They are easy to attack and not representative | Evaluate on held-out rows |
| Forgetting the clean baseline | Only the attacked number is shown | Always report both |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Robust accuracy > clean accuracy | Base set or denominator error | Recompute `C`, `S`, and `N` and check the identity |
| ASR = 1.0 at ε = 0 | Labels or inputs modified | Compare predictions before and after with ε = 0 |
| ASR changes when rows are reordered | Random restarts or sampling | Fix the seed and document restart behavior |
| Different ASR on the same model | Attack hyperparameters differ | Match steps, step size, and restarts |
| Robust accuracy is 0 at a modest ε | Attack is too strong or buggy | Inspect perturbations and verify the domain |
| Numbers do not match a reference | Different split or preprocessing | Compare split hashes and scaler parameters |

## Check your understanding

1. A model has 200 test rows, 180 clean-correct, and an attack changes 45 of them. Compute clean accuracy, ASR, and robust accuracy.
2. Why is ASR usually computed over clean-correct rows rather than all rows?
3. Give one statement that an empirical result supports and one that it does not.
4. A defense reports 0.95 robust accuracy at ε = 0.05. What three follow-up questions do you ask?
5. Explain the difference between a certified radius and an attack budget.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- A robustness claim is a tuple: model, adversary, norm and budget, base set, metric.
- Clean accuracy = C/N, ASR = S/C, robust accuracy = (C − S)/N. The denominators are not interchangeable.
- LAB-11's undefended model: 0.9667 clean, 0.3582 ASR, 0.6204 robust at ε = 0.10 on 522 clean-correct rows.
- Empirical results are evidence for a tested attack; certified results are guarantees within a radius. They are not the same claim.
- One budget is not a curve. Add a stress budget and report the defense's failure boundary.
- Base-set hygiene is part of the method, not an afterthought.

## Next

Continue to [Lesson 08.2 — Adversarial training](lesson-2-adversarial-training.md), where the clean-cost/robust-gain trade-off becomes a measured engineering decision.
