# Lesson 13.5 — Privacy–Utility Evaluation and Its Limits

<a id="m13-l5"></a>

**Module 13 · Lesson 5 of 5 · 1.5 hours · LO-19, LO-28**

## Scenario

A team ships a "privacy-preserving" release and reports two numbers: epsilon is 0.5, and accuracy is 78%. The product owner asks whether that is private enough. The engineer answers that epsilon is small. Neither number answers the question, because nobody wrote down what the release is for, what the neighboring relation is, which rows were clipped, whether the budget covers one query or the whole quarter, or what the empirical membership test could possibly have detected at this sample size.

This lesson builds the evaluation that turns those two numbers into a defensible statement — and shows where the statement stops.

## Objectives

By the end of this lesson you will be able to:

1. Separate utility, privacy, and cost measurements, and state what each one can support.
2. Reproduce the LAB-17 release protocol and read its privacy–utility frontier.
3. Explain why a membership AUC near 0.5 is absence of measured signal, not proof of privacy.
4. Identify the threats to validity in a small empirical privacy evaluation.
5. Complete a privacy documentation record that a reviewer can audit.
6. Write a scoped claim about a release, including what remains unverified.

## 1. Three kinds of measurement

| Kind | Example in LAB-17 | What it supports | What it does not support |
|---|---|---|---|
| Utility | classifier accuracy on held-out test rows | "This release is usable for this task at this epsilon" | "The release is private" |
| Privacy (formal) | epsilon, delta, sensitivity, composition | A worst-case bound under a stated neighboring relation | A bound for a different relation or mechanism |
| Privacy (empirical) | distance-based membership AUC | "This specific test found no signal at this sample size" | "No attacker can learn membership" |
| Cost / risk | clipping fraction, accuracy loss, budget spent | Trade-off and operating cost | Whether the trade-off is acceptable |

A privacy report that contains only epsilon is incomplete. A report that contains only accuracy is not a privacy report. A report that contains only an attack result is a measurement, not a guarantee.

## 2. The LAB-17 protocol

LAB-17 releases class centroids, not a trained network, so the measurement is easy to inspect end to end.

| Element | Setting |
|---|---|
| Data | Two Gaussian classes, four continuous features, seed 42 |
| Release rows | 500 per class (1,000 total), drawn first |
| Test rows | 150 per class, held out |
| Nonmember rows | 150 per class, drawn after release and test |
| Clipping | Each feature clipped to `[-3.0, 3.0]` |
| Clipped fraction | 0.0125 of release rows |
| Statistic | Mean vector (centroid) per class, four dimensions |
| Sensitivity | `2 * B * d / n = 2 * 3 * 4 / 500 = 0.048` |
| Mechanism | Laplace, scale `sensitivity / epsilon` |
| Composition | Parallel over two disjoint class datasets, so total epsilon equals per-class epsilon |
| Release epsilons | 0.02, 0.1, 0.5, 1.0, 4.0 |
| Utility | Nearest-centroid accuracy on the clipped test rows |
| Error | Mean L2 distance between noisy and true clipped centroids |
| Empirical privacy | Membership AUC from distance scores, members versus nonmembers |

Two design choices make the arithmetic checkable. The classes are disjoint, so the parallel composition argument applies without a data-dependent assumption. The statistic is a mean, so the L1 sensitivity has a closed form and the noise scale can be recomputed by hand.

### Measured results

| Epsilon | Laplace scale | Test accuracy | Centroid L2 error | Membership AUC |
|---:|---:|---:|---:|---:|
| baseline (no noise) | — | 0.8233 | 0.0000 | — |
| 0.02 | 2.4000 | 0.5233 | 4.3642 | 0.4903 |
| 0.10 | 0.4800 | 0.7433 | 1.5482 | 0.5237 |
| 0.50 | 0.0960 | 0.7833 | 0.3257 | 0.5308 |
| 1.00 | 0.0480 | 0.8233 | 0.0450 | 0.5258 |
| 4.00 | 0.0120 | 0.8167 | 0.0281 | 0.5263 |

Read the table in three directions.

**Utility.** Accuracy rises with epsilon and approaches the no-noise baseline. At epsilon 0.02 the noise scale is 2.4 on features clipped to a width of 6, so the released centroids are almost uninformative; accuracy 0.5233 is barely above the 0.5 chance level for two classes. At epsilon 1.0 accuracy matches the baseline 0.8233. At epsilon 4.0 it is 0.8167, slightly below baseline: at this point noise is small but not zero, and one draw can be mildly unlucky. A single seed is not a trend.

**Error.** Centroid L2 error falls from 4.3642 to 0.0281 as epsilon grows. This is the mechanism behaving as designed: noise scale is inversely proportional to epsilon, and the empirical error tracks it.

**Empirical privacy.** The membership AUC stays between 0.4903 and 0.5308 across four orders of magnitude of epsilon. That is not a paradox. The test asks a narrow question — can a particular distance score separate members from nonmembers at this sample size — and the answer is no at every epsilon tested. It is equally consistent with two very different worlds: a mechanism that is genuinely protective, and a test too weak to detect what leakage exists.

### Why accuracy is not monotone in epsilon here

At epsilon 0.5 accuracy is 0.7833, at 1.0 it is 0.8233, at 4.0 it is 0.8167. If the mechanism were deterministic, more epsilon would mean less noise and never worse expected accuracy. The realized numbers are one draw each. Reporting a single seed as a frontier overstates precision; a proper evaluation repeats the release with several seeds and reports a mean and an interval. LAB-17 keeps one seed so the artifact is reproducible, and its report says so.

## 3. Reading the frontier

A privacy–utility frontier is a set of (privacy parameter, utility) points produced under one protocol. It is useful for choosing an operating point. It is easy to misuse.

| Misuse | Why it is wrong | Better practice |
|---|---|---|
| "Accuracy 0.78 means epsilon 0.5 is fine" | Accuracy alone says nothing about leakage | Report epsilon, delta, sensitivity, composition, and utility together |
| "Epsilon 0.5 is small" | Epsilon has no absolute meaning without the neighboring relation and query count | State the unit of privacy and the total budget across releases |
| Comparing epsilon across mechanisms | Different mechanisms, relations, and compositions are not on one scale | Compare complete records, not single numbers |
| Reporting the best point on the frontier | It is a selected result | Report the protocol and all points, or state the selection rule |
| Treating a flat empirical curve as proof | Low power looks identical to strong privacy | State the test, its sample size, and what it could have detected |

### Choosing an operating point

The choice is a product decision constrained by evidence, not a derivation.

1. **Fix the task and the utility floor.** For LAB-17's nearest-centroid task, 0.74 accuracy at epsilon 0.1 may be acceptable; 0.52 at 0.02 probably is not.
2. **Fix the privacy requirement.** Who is the adversary, what is the unit, how many releases will occur, and what total budget is allowed?
3. **Find the intersection.** Epsilon 0.5 gives 0.7833 accuracy with a total budget of 0.5 for this release. Epsilon 1.0 gives 0.8233 at twice the budget.
4. **Record the residual.** Neither point protects against an attacker outside the DP threat model, and neither has been tested against an adaptive membership attacker.

## 4. What the membership test does and does not show

LAB-17 scores each row by negative distance to its released class centroid. Members are release rows; nonmembers are rows drawn from the same generating distribution but never released. The AUC compares the two score distributions.

- **AUC ≈ 0.5** means the score does not rank members above nonmembers better than chance in this sample. It is consistent with a strong guarantee and with a weak test.
- **AUC > 0.5** would be a warning, but not a formal violation: the test is not the definition of epsilon-DP, and a single test can fire by chance.
- **AUC < 0.5** is possible with small samples and means the score is anti-correlated in this draw; it is not evidence of "negative leakage."

Why the test has low power here:

| Limitation | Effect |
|---|---|
| Nonmembers come from the same Gaussian generator | The only difference is inclusion in a 500-row mean, a small signal |
| One distance score per row | A stronger attacker would use likelihood ratios or shadow models |
| 300 nonmembers and 1,000 members | Sampling noise near AUC 0.5 is roughly ±0.03 |
| One release per epsilon | No averaging over draws |
| The statistic is a centroid, not a model | Results do not transfer to DP-SGD or a deployed classifier |

The last row matters most for reporting. LAB-17 measures the privacy of a centroid release under one mechanism. It cannot be cited as evidence about a model trained with DP-SGD, a different clipping bound, or a different data distribution.

### What a stronger empirical audit would add

- Multiple seeds and a confidence interval on AUC.
- Shadow-model or likelihood-ratio attacks, which are closer to what a real adversary can build.
- A nonmember set drawn from a shifted distribution, reported separately: this is easier for an attacker and exposes distribution confounds.
- A canary or secret inserted into the release set to test whether it can be recovered.
- A negative control: run the same attack against a release known to leak, to show the test can detect leakage when it exists.

A test that has never detected a known leak is not evidence of protection. It is an untested instrument.

## 5. Threats to validity

| Threat | How it appears | Mitigation in reporting |
|---|---|---|
| Single seed | Accuracy 0.8167 at epsilon 4.0 looks worse than 0.8233 at 1.0 | Repeat and report intervals; do not call one draw a frontier |
| Distribution confound | Nonmembers drawn differently from members | Match the generating process; report any shift |
| Weak attack | Distance score only | Add stronger attacks and a positive control |
| Composition assumption | Parallel composition needs disjoint data | State disjointness and verify it in code |
| Clipping leakage | Clipping fraction and bound are public | Treat bound as public; report sensitivity from it |
| Post-processing claim | Any function of a DP output is DP, but utility is not free | State what post-processing was applied |
| Hyperparameter selection | Choosing clipping after seeing results weakens the accounting | Fix the pipeline before measuring; count selection in the budget if data-dependent |
| Scope transfer | Centroid result cited for a neural model | State the object measured and do not generalize |

## 6. The privacy documentation record

A release is auditable when a reviewer can reconstruct the guarantee without reading the code. The record below is the minimum LAB-17 can support.

```text
Release:        class-centroid summary, v1
Purpose:        demonstrate a noisy release under a stated budget
Data subjects:  synthetic rows; no real people
Unit of privacy: one row
Neighboring relation: replace one row in one class dataset
Statistic:      per-class mean of 4 clipped features
Clipping:       [-3.0, 3.0]; observed clipped fraction 0.0125
Sensitivity:    0.048 (L1)
Mechanism:      Laplace, scale = 0.048 / epsilon per class
Composition:    parallel over two disjoint class datasets
Budget:         total epsilon = per-release epsilon; delta = 0
Releases:       0.02, 0.1, 0.5, 1.0, 4.0 (separate runs, not cumulative)
Utility:        nearest-centroid test accuracy; baseline 0.8233
Empirical test: distance-based membership AUC; 0.4903 to 0.5308
Not covered:    adaptive attackers, DP-SGD, other datasets, linkage attacks
Owner:          course lab (synthetic)
Review date:    on any change to bound, n, or mechanism
```

Three lines carry most of the weight. The **unit** and **neighboring relation** define what epsilon means. The **composition** line defines whether budgets add. The **not covered** line prevents the record from being read as a broader claim than it is.

## 7. Worked evaluation: is epsilon 0.5 acceptable?

Suppose a product team proposes the epsilon 0.5 release for a dashboard that shows class centroids to analysts, and asks for a recommendation.

| Question | Evidence | Answer |
|---|---|---|
| What is the task? | Show class summaries, not per-row predictions | Centroid release is the right object |
| What utility is needed? | Analysts previously used exact centroids at 0.8233 accuracy | 0.7833 is a 0.0400 absolute drop |
| What is the privacy unit? | One row in one class | Row-level epsilon 0.5, delta 0 |
| How many releases? | One dashboard refresh per day for a quarter | Ninety releases would compose; one release does not cover the quarter |
| Is the empirical test reassuring? | AUC 0.5308 | Slightly above chance; not conclusive either way |
| What remains unknown? | Adaptive attacker, linkage with external data | Must be listed as residual risk |

The defensible statement is narrow:

> Under row-level replacement in one class dataset, with features clipped to `[-3, 3]` and 500 rows per class, this centroid release satisfies epsilon 0.5 with delta 0 for a single release. Test accuracy is 0.7833 against a 0.8233 no-noise baseline. A distance-based membership test did not separate members from nonmembers beyond chance (AUC 0.5308, 1,300 rows). The record does not cover repeated releases, adaptive attackers, or linkage with external data.

That statement can be audited. "Epsilon is 0.5 and accuracy is 78%" cannot.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reporting epsilon without the neighboring relation | Epsilon looks like a universal score | State the unit and relation first |
| Comparing epsilon across papers or mechanisms | The symbol is shared; the definitions are not | Compare complete records |
| Calling a flat membership curve proof of privacy | The test looks like an attack | Report the test's power and a positive control |
| Reporting one seed as a frontier | The artifact is reproducible | Repeat and report intervals, or label it a single draw |
| Ignoring repeated releases | Each refresh spends budget | Track a ledger across releases |
| Choosing clipping after seeing the attack | The pipeline was tuned on the evaluation | Fix the pipeline, then measure |
| Generalizing a centroid result to DP-SGD | Both are "differential privacy" | Scope the claim to the measured object |
| Hiding accuracy loss | Privacy is the goal | Report utility, privacy, and cost together |
| Treating delta as negligible without saying so | It is often small | State delta and what it permits |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Accuracy identical across epsilons | Noise not applied, or epsilon ignored | Check the scale `sensitivity / epsilon` and the seeded RNG |
| Accuracy far below chance | Sensitivity or scale miscomputed | Recompute `2 * B * d / n`; check clipping happens before the mean |
| Total epsilon larger than expected | Sequential composition applied to disjoint data, or the reverse | Verify disjointness before claiming parallel composition |
| Membership AUC exactly 0.5 | Scores tie or the attack is degenerate | Inspect score distributions; confirm members and nonmembers differ only by inclusion |
| Empirical result contradicts epsilon ordering | Single draw, small sample | Repeat with several seeds before interpreting |
| Reviewer cannot reconstruct the number | Sensitivity or composition missing | Use the documentation record |
| Report claims "private" with no scope | The claim outran the evidence | Add the not-covered list |

## Check your understanding

1. Why can accuracy at epsilon 4.0 be lower than at epsilon 1.0 without contradicting the mechanism?
2. What does membership AUC 0.5308 support, and what does it not support?
3. Name three threats to validity in LAB-17's empirical privacy test.
4. Why does parallel composition apply to LAB-17's two classes, and what would break it?
5. A colleague says "epsilon 0.5 is private enough." What four facts do you need before responding?
6. Write the one-sentence scope statement you would attach to the epsilon 0.5 result.

Answers are discussed in the [answer key](quiz-answers.md).

## Summary

- Utility, formal privacy, empirical privacy, and cost are different measurements. A release report needs all four.
- LAB-17's frontier runs from accuracy 0.5233 at epsilon 0.02 to 0.8233 at epsilon 1.0, with centroid error falling from 4.3642 to 0.0450.
- Its membership AUC stays near 0.5 across epsilons. That is absence of measured signal at this sample size, not proof of privacy.
- One seed is one draw. A frontier needs repeats, intervals, and a stated protocol.
- A privacy documentation record names the unit, relation, mechanism, sensitivity, composition, budget, utility, empirical tests, and what is not covered.
- The strongest honest claim is scoped: this object, this relation, this budget, these tests, these residual risks.

## Next

Continue to the [Module 13 quiz](quiz.md) and [exercises](exercises.md), then move to [Module 14 — Explainability, Fairness, and Security Trade-offs](../m14-explainability-fairness/index.md).
