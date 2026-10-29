# Lesson 12.5 — Evaluating Distributed Defenses

<a id="m12-l5"></a>

**Module 12 · Lesson 5 of 5 · 1.5 hours · LO-24, LO-28**

## Scenario

A vendor presents a slide: "Our robust aggregator reduces backdoor success by 99.9%." The evaluation compares their aggregator after 40 rounds against plain FedAvg after 10 rounds, on a different client partition, with a different trigger, and reports only attack success. The number may be real. It does not answer the question the consortium needs answered.

This lesson builds an evaluation protocol that does answer it: what was held fixed, what changed, what was measured, and what remains unknown.

## Objectives

By the end of this lesson you will be able to:

1. State the four questions an evaluation must answer before it reports a number.
2. Design an equal-round, fixed-population comparison.
3. Compute absolute and relative attack-success reduction and clean-accuracy cost.
4. Explain why false positives and client-level harm belong in a defense evaluation.
5. Design ablations for attacker fraction, scale, trim count, and non-IID severity.
6. Write a scoped assurance statement with limitations and residual risk.

## 1. Four questions before a number

| Question | Why it matters | LAB-16 answer |
|---|---|---|
| What is the attacker's capability? | A defense against a naive attacker says little about an adaptive one | One client, code control, scaled update, trigger backdoor |
| What is held fixed? | A difference in rounds or data can explain the result | Clients, partition, rounds, local epochs, learning rate, evaluation split |
| What is measured? | Clean accuracy and ASR can move in opposite directions | Both, plus the attack-row count |
| What is the claim's scope? | A result is for a configuration | Eight clients, one attacker, digits, 12 rounds, this trigger |

If a report cannot answer these, the number is not yet evidence.

## 2. The equal-round protocol

The defense comparison changes one thing: the aggregation rule. Everything else stays fixed.

| Factor | LAB-16 setting | Why fixed |
|---|---|---|
| Dataset | Digits, 70/30 split | Same task and evaluation |
| Clients | 8 | Same population |
| Partition | Each class 70/30 across two clients | Same non-IID structure |
| Rounds | 12 | Same training budget |
| Local epochs | 8 | Same local work |
| Learning rate | 0.5 | Same optimization |
| L2 | 0.001 | Same regularization |
| Attack | Client 0, trigger 2×2, target 0, scale 6 | Same attacker |
| Evaluation | 1,080 non-target rows for ASR | Same denominator |

The protocol compares four runs: benign mean, malicious mean, malicious trimmed mean, and malicious clipped mean. The benign run is the utility reference. The malicious mean is the attack reference. The two defenses are compared against both.

### Why equal rounds

A defense that trains longer can look better for reasons unrelated to robustness. A backdoor may also strengthen or wash out over rounds. Fixing the round count removes both confounds. If a defense needs more rounds to converge, that is a cost to report, not a reason to give it more rounds silently.

### Why a fixed population

Excluding suspicious clients changes the training population. If the defense excludes a client, the comparison is no longer "same clients, different rule." Record exclusions and, if possible, report results with and without them. LAB-16 does not exclude anyone; the trimmed mean simply down-weights extremes.

## 3. Metrics

| Metric | Definition | What it answers |
|---|---|---|
| Clean accuracy | Accuracy on the untouched test set | Does the model still perform the main task? |
| Attack success rate (ASR) | Fraction of triggered non-target rows predicted as the target | Did the backdoor install? |
| Benign ASR | ASR on a model trained without an attacker | What is the trigger's false-positive floor? |
| Targeted accuracy | Accuracy on the target class | Did the defense sacrifice the target class? |
| Per-class accuracy | Accuracy for each label | Is a failure hidden by the average? |
| Client exclusion rate | Fraction of benign clients flagged or removed | What does the defense cost honest participants? |
| Rounds to threshold | Rounds needed to reach a clean-accuracy target | What is the convergence cost? |
| Wall-clock and memory | Runtime and peak memory | Is the rule deployable? |

LAB-16 reports clean accuracy and ASR, with the attack-row count. It does not report client-level false positives, per-class accuracy, or runtime. Those are stated limitations.

## 4. Worked comparison

Reference results:

| Run | Clean | ASR |
|---|---:|---:|
| Benign mean | 0.9000 | 0.0021 |
| Malicious mean | 0.7056 | 1.0000 |
| Malicious trimmed mean | 0.8704 | 0.0000 |
| Malicious clipped mean | 0.8944 | 0.6276 |

### Attack reduction

Relative to the malicious mean:

- Trimmed mean: \((1.0000 - 0.0000)/1.0000 = 100\%\) reduction.
- Clipping: \((1.0000 - 0.6276)/1.0000 = 37.24\%\) reduction.

The vendor's "99.9%" claim is not reproduced by either rule on this attack. A 37% reduction is not nothing, but it leaves most of the backdoor intact.

### Utility cost

Relative to the benign mean:

- Trimmed mean: \(0.9000 - 0.8704 = 0.0296\) absolute accuracy cost.
- Clipping: \(0.9000 - 0.8944 = 0.0056\) absolute accuracy cost.

Relative to the malicious mean, both defenses improve accuracy because they reduce the attack's damage. That improvement is not the defense's utility cost. Mixing the two baselines is a common way to make a defense look better than it is.

### The correct reading

| Claim | Supported? |
|---|---|
| "Trimmed mean removes this backdoor." | Yes, for this attacker and configuration. |
| "Clipping substantially reduces ASR." | Yes: 1.0000 to 0.6276. |
| "Clipping is sufficient." | No: 62.76% of triggered rows still hit the target. |
| "Trimmed mean is robust in general." | No: one outlier, one trim count, one dataset. |
| "The defenses do not hurt utility." | No: trimmed mean costs 2.96 points against benign. |

## 5. False positives and honest clients

A defense that flags or removes honest clients is not free. The relevant rate is the fraction of benign participants harmed by the control, and the cost of losing their data.

| Control | False-positive event | Cost |
|---|---|---|
| Norm clipping | A benign update is clipped | Reduced contribution from an honest client |
| Client exclusion | A benign client is flagged | Lost data and a trust incident |
| Trigger scan | A benign input matches a trigger pattern | Blocked legitimate prediction |
| Reference-loss gate | A client with unusual data fails | Exclusion of a minority distribution |

LAB-16's clipped mean applies to every client, so "false positive" is not a discrete event; it is the utility cost of clipping benign updates. The lab does not measure how many benign updates were clipped or how much accuracy was lost for that reason. A stronger evaluation would log the clip rate per client and compare clipped benign training to unclipped benign training.

## 6. Uncertainty

One seed and one split produce one number. The honest report includes:

- **Multiple seeds** for the partition, initialization, and client order.
- **An interval** or a range across seeds, not a single point.
- **Sensitivity to the attacker**: scale, fraction, trigger, and target.
- **Sensitivity to the rule**: trim count, clip norm, number of clients.
- **Sensitivity to heterogeneity**: IID versus the chosen non-IID partition.

With eight clients, a single client is 12.5% of the population. A result that depends on which client is malicious is fragile. Report the client identity and consider rotating it.

## 7. Ablations

Change one factor at a time.

| Ablation | Values | Question |
|---|---|---|
| Attacker fraction | 1, 2, 3 of 8 | At what fraction does the rule fail? |
| Attack scale | 1, 2, 6, 20 | Is the result sensitive to magnitude? |
| Trim count | 0, 1, 2 | How much trimming is needed, and what does it cost? |
| Clip norm | 0.5, 2.0, 10.0 | Where is the utility-robustness trade-off? |
| Non-IID severity | 70/30, 90/10, one class per client | Does heterogeneity break the rule? |
| Trigger | 2×2 corner, single pixel, random patch | Is the result trigger-specific? |
| Target | 0, 5 | Is the result target-specific? |

LAB-16 implements one point in this space. The exercises ask you to reason about the others; if you have time, run them.

## 8. The report

A defensible report has seven parts:

1. **Claim.** One sentence, scoped to the configuration.
2. **Threat model.** Attacker capability, fraction, identity, and goal.
3. **Setup.** Data, partition, model, rounds, hyperparameters, seed.
4. **Results.** Clean accuracy and ASR for benign, attack, and each defense.
5. **Negative results.** Where the defense failed or cost utility.
6. **Limitations.** What was not tested.
7. **Residual risk.** What remains after the control.

LAB-16's report follows this structure. Its claim is narrow: under eight non-IID clients, one scaled backdoor client, 12 rounds, trimmed mean removes the backdoor and clipping does not. It does not claim that either rule is secure.

## 9. A scoped assurance statement

Instead of "the system is robust," write:

> Under the LAB-16 threat model — one malicious client among eight, a 2×2 pixel trigger targeting class 0, a 6× update scale, digits data, and 12 equal rounds — the coordinate-wise trimmed mean with one value trimmed per tail reduced attack success from 1.0000 to 0.0000 and clean accuracy from 0.9000 to 0.8704. Norm clipping at 2.0 reduced attack success to 0.6276. Neither result establishes robustness against two colluding clients, an adaptive attacker, a different trigger, or a larger model. Sybil resistance, secure aggregation, and privacy accounting were not evaluated.

This is longer than a slogan and far more useful. It tells the reader what was tested, what changed, and what did not.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Comparing at different rounds | The defense needed more time | Fix the budget or report the difference |
| Using the malicious mean as the utility baseline | It makes the defense look beneficial | Compare clean accuracy to the benign run |
| Reporting relative reduction only | It sounds larger | Report absolute ASR too |
| Ignoring client exclusions | The defense "just" removes bad clients | Count benign clients harmed |
| One seed, one claim | The experiment is small | Repeat and report a range |
| No negative result | The defense worked | State what it did not fix |
| Calling ASR 0.6276 a success | It fell by 37% | State the residual 62.76% |
| Claiming general robustness | The lab is a model | Scope the claim to the configuration |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Defense ASR is lower but clean accuracy is much lower | The rule removes legitimate signal | Report the utility cost; tune the rule |
| Benign ASR is not near zero | Trigger leaks into benign training or target rows included | Check the trigger application and attack rows |
| Results differ across runs | Seed or client order changed | Fix and record both |
| Clip rate is 100% | Threshold below every update norm | Inspect the norm distribution |
| Trim count invalid | \(2m \ge K\) | Reduce \(m\) or add clients |
| Report cannot be reproduced | Missing seed, split, or dependency versions | Use the manifest and `run.json` |

## Check your understanding

1. Why must defense comparisons fix the number of rounds?
2. Compute the relative ASR reduction and absolute clean-accuracy cost for the clipped mean against the malicious and benign baselines.
3. Why is comparing clean accuracy to the malicious mean misleading?
4. Name two false-positive costs that LAB-16 does not measure.
5. Design one ablation that would test whether the trimmed-mean result depends on the attacker fraction.
6. Rewrite "trimmed mean is Byzantine-robust" as a scoped assurance statement.

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- State the attacker, the fixed factors, the metrics, and the scope before reporting a number.
- Equal rounds and a fixed population make the aggregation rule the only difference.
- Report clean accuracy against the benign baseline and ASR against the malicious baseline.
- LAB-16: trimmed mean reduces ASR by 100% at a 2.96-point accuracy cost; clipping reduces it by 37.24% and leaves 62.76%.
- Measure false positives and client harm, not only attack success.
- Repeat seeds, ablate one factor at a time, and state negative results.
- A scoped assurance statement is more useful than a robustness slogan.

## Next

You have completed Module 12. Continue to [Module 13 — Privacy-Preserving Machine Learning](../m13-privacy-preserving-ml/index.md), where the focus shifts from integrity to what a release reveals.
