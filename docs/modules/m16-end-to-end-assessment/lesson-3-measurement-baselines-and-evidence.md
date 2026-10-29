# Lesson 16.3 — Measurement, Baselines, and Evidence

<a id="m16-l3"></a>

**Module 16 · Lesson 3 of 4 · 1 hour · LO-33, supports LO-28**

## Scenario

An assessment reports that an evasion attack raises the fraud block rate from 12% to 31%. The number is striking. It is also measured on a reseeded split, with a threshold retuned "to be fair," against a baseline from last quarter. The effect may be real, but the report cannot show it. The reviewer cannot tell whether the attack worked or the comparison changed.

This is the most common failure in applied ML security, and it is entirely preventable.

## Objectives

By the end of this lesson you will be able to:

1. Freeze a baseline protocol before running attacks.
2. Design negative controls that reveal measurement error.
3. Report effect sizes with uncertainty and a denominator.
4. Preserve evidence so another person can reproduce the headline result.
5. Recognize comparisons that are confounded by split, threshold, seed, or version changes.

## 1. The baseline protocol

A baseline is not "the model's accuracy." It is a complete measurement recipe:

| Element | Must state | Example |
|---|---|---|
| Data version | Snapshot or hash | `txn-2026-09`, SHA-256 `9f2c…` |
| Split | Unit and time boundary | Temporal holdout, 2026-08-01 to 2026-08-31 |
| Model version | Artifact hash | `riskgate-4.2.1`, SHA-256 `41ae…` |
| Preprocessing | Fitted where, on what | Fit on training window only |
| Threshold | Value and selection rule | 70, selected on validation at 2% false declines |
| Metrics | Definition and denominator | Recall over confirmed fraud; false-decline rate over legitimate transactions |
| Environment | Versions and hardware | Python 3.14.7, NumPy 2.5.2, CPU |
| Seed | Every stochastic step | 42 |
| Command | One line that reruns it | `python assess.py --config baseline.yaml` |

Freeze this recipe in a file before the first attack. If you change any element later, you have a new baseline, and every comparison must be rerun.

### The zero-effect control

Every attack experiment should include a zero-budget or null condition:

- ℓ∞ budget ε = 0;
- no poisoned rows;
- no trigger;
- the clean retrieval corpus;
- the same query with no modification.

The measured effect at zero budget should be zero, apart from sampling noise. If it is not, the pipeline has a bug: labels misaligned, threshold drifting, nondeterministic preprocessing, or evaluation data leaking into training.

The null condition is cheap and catches the most embarrassing errors.

## 2. Negative controls

A negative control is a test expected to produce no effect. It separates "the attack works" from "the measurement is broken."

| Control | Expected result | What a failure reveals |
|---|---|---|
| Zero perturbation | Same predictions | Attack code changes inputs when it should not |
| Random perturbation at the same budget | Small or no targeted effect | The metric is sensitive to any change |
| Shuffled labels | Performance near chance | Leakage or cached predictions |
| Clean model, trigger input | No targeted behavior | The trigger is not specific to the backdoor |
| Benign queries through a detector | Low alert rate | Detector threshold is miscalibrated |
| Duplicate row removal | Metric changes within interval | The original metric was inflated by duplicates |

Negative controls belong in the results table, not in a footnote. They are evidence that the effect is attributable to the attack.

## 3. Uncertainty and effect size

Report an interval, not only a point estimate. For a proportion, a Wilson or bootstrap interval is usually enough. For a difference between two runs, bootstrap the difference or report both intervals and the overlap.

| Result | Weak report | Strong report |
|---|---|---|
| Attack success | "ASR 31%" | "ASR 0.31 (95% CI 0.27–0.35), n = 540 targeted rows, ε = 0.10, 20 steps, 5 restarts" |
| Defense effect | "Defense reduced ASR" | "ASR fell from 0.31 to 0.08 (difference −0.23, 95% CI −0.28 to −0.18) at a clean-accuracy cost of 0.04" |
| Detector | "Detector works" | "TPR 0.72 at FPR 0.05 on 1,000 benign requests; 14 false positives" |
| Data-quality effect | "Recall dropped" | "Recall 0.62 → 0.55 after deduplication; 38 duplicate disputes removed; CI overlaps by 0.01" |

The denominator is part of the metric. "ASR 31%" over 540 targeted rows means something different from 31% over 12 rows. State n.

### Multiple comparisons

If you test 20 configurations and report the best one, the reported effect is biased upward. Either pre-register the primary comparison, report all configurations, or label the result exploratory. In a project, a table of all runs is more credible than a single best number.

## 4. Confounding by split, threshold, and version

Three changes account for most false attack effects.

| Change | Looks like | Control |
|---|---|---|
| Split | Attack evaluated on a different holdout | Freeze and hash the evaluation set |
| Threshold | Defense retuned to a better operating point | Keep the threshold fixed; report the curve |
| Version | Model or library updated between runs | Pin and record versions; rerun the baseline |
| Seed | Different sampling changes the result | Fix seeds; report seed sensitivity |
| Preprocessing | Scaler refit on the full data | Fit inside the training fold only |

A fair defense comparison holds the data, threshold, and evaluation protocol fixed, then changes only the defense. If the defense requires a different threshold, report both the defense at the fixed threshold and at its chosen threshold.

## 5. Evidence integrity

An evidence package should let a skeptical reviewer rerun the headline result.

```text
assessment/
├─ scope.md
├─ threat-model.yaml
├─ register.csv
├─ test-plan.csv
├─ config/
│  ├─ baseline.yaml
│  └─ experiments.yaml
├─ data/
│  └─ dataset-manifest.json      # source, version, hash, license
├─ experiments/
│  ├─ t01_dedup.csv
│  ├─ t02_evasion.csv
│  └─ t03_stale.csv
├─ artifacts/
│  ├─ run.json                   # versions, seeds, timestamps, commands
│  └─ manifest.json              # SHA-256 of every result file
├─ report.md
└─ reproduce.sh
```

Rules:

- **Hash inputs and outputs.** A manifest with hashes is the difference between evidence and a screenshot.
- **Record the command, not the intention.** `python assess.py --config baseline.yaml` is reproducible; "ran the baseline" is not.
- **Keep raw results.** Aggregated tables can be regenerated; deleted raw rows cannot.
- **Separate exploration from confirmation.** If you tuned after seeing results, label the final run as exploratory or rerun on a fresh holdout.
- **Do not commit data you do not have rights to redistribute.** Record the source, version, and checksum instead.

## 6. A results table that survives review

| Test | Condition | n | Metric | Baseline | Result | Difference (95% CI) | Notes |
|---|---|---:|---|---|---|---|---|
| T-01 | Deduplicated labels | 4,820 | Recall at 2% FDR | 0.62 | 0.55 | −0.07 (−0.11, −0.03) | 38 duplicates removed |
| T-02 | 3-feature shift | 540 | Segment block rate | 0.18 | 0.31 | +0.13 (0.08, 0.18) | Global +0.004 |
| T-02 | Zero-budget control | 540 | Segment block rate | 0.18 | 0.18 | 0.00 (−0.02, 0.02) | Pipeline check |
| T-03 | 30-day stale feed | 4,820 | Decision disagreement | — | 0.07 | — | Two segments above 5% |
| T-05 | Override logging | 20 | Fields present | 0/20 | 20/20 | — | Actor, reason, timestamp |

The table shows what changed, by how much, over what denominator, and whether the measurement itself is trustworthy. A reader can disagree with the conclusion without doubting the arithmetic.

## 7. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Baseline from memory | Effect includes version drift | Rerun the baseline under the frozen protocol |
| No zero-budget control | Attack code bug looks like success | Add ε = 0, zero-poison, or clean-corpus control |
| Point estimate only | Small samples look decisive | Report n and an interval |
| Best-of-many reported | Effect is inflated | Report all runs or pre-register the primary test |
| Threshold retuned for defense | Comparison is confounded | Hold threshold fixed; report the curve |
| Metrics without denominators | Reader cannot judge scale | State n and the base set |
| Screenshots as evidence | Cannot be verified | Save raw outputs and hashes |
| Manual steps | Reproduction fails silently | Script the run; record the command |

## 8. Check your understanding

1. List the nine elements of a baseline protocol.
2. What does a nonzero result at zero perturbation usually indicate?
3. Give three negative controls for an evasion experiment and what each detects.
4. Why is "ASR 31%" incomplete without n and a budget?
5. How does retuning a threshold confound a defense comparison?
6. What belongs in a manifest, and why?

## 9. What you keep

A frozen baseline configuration, a negative-control table, a results template with intervals, and a reproduction package. Lesson 16.4 turns these results into findings and recommendations.

## 10. Next

Lesson 16.4 covers severity calibration, finding structure, remediation sequencing, residual risk, and the report and briefing.
