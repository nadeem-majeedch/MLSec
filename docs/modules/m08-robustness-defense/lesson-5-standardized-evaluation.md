# Lesson 08.5 — Standardized Evaluation and Reproducibility

<a id="m08-l5"></a>

**Module 08 · Lesson 5 of 6 · 1.5 hours · LO-28**

## Scenario

Two teams report robustness for the same model family. Team A reports 68% robust accuracy at ε = 0.10. Team B reports 54% at the same budget. Both used PGD. The numbers disagree by 14 points.

The models are not the difference. The attacks are: different step counts, different step sizes, one restart versus ten, and one team measured on the clean-correct base while the other measured on all rows. Neither team is lying. Their experiments are simply not comparable.

This lesson is about making an evaluation that survives that comparison: fixed seeds, recorded configuration, a standard attack protocol, artifact hashes, and a stated tolerance.

## Objectives

By the end of this lesson you will be able to:

1. Explain why a robustness number without an evaluation protocol is not comparable.
2. Design a reproducible evaluation record with seeds, versions, configuration, and hashes.
3. Use multiple seeds and report spread instead of a single point estimate.
4. Interpret a tolerance in a checker and distinguish a real difference from run-to-run noise.
5. Describe what AutoAttack and RobustBench standardize, and what they do not cover.

## 1. The protocol is part of the result

A robustness result is a function of at least these inputs:

| Input | Example | If unrecorded |
|---|---|---|
| Data and split | digits, stratified 70/30, seed 42 | Another team cannot rebuild the base set |
| Preprocessing | pixels divided by 16 | Values and ε scale differ |
| Model and training | logistic regression, `C = 1.0`, `max_iter = 5000` | The artifact is not identifiable |
| Attack | PGD, 20 steps, α = ε/5, 2 restarts | ASR is not comparable |
| Base set | clean-correct rows, size 522 | Denominators disagree |
| Metric | ASR, robust accuracy, clean accuracy | Different questions are compared |
| Versions | Python, NumPy, scikit-learn | Numerical differences are unexplained |

The lab's `run.json` records a subset of this. A production evaluation record should record all of it.

### The minimum record

LAB-11 writes four artifacts:

| File | Purpose |
|---|---|
| `metrics.json` | The measured numbers, with base sizes |
| `run.json` | Seed, ε, steps, restarts, squeeze levels, environment |
| `report.md` | Human-readable tables and limitations |
| `manifest.json` | SHA-256 hashes of the other three |

```json
{
  "lab": "LAB-11",
  "seed": 42,
  "epsilon": 0.1,
  "steps": 20,
  "restarts": 2,
  "squeeze_levels": 4,
  "environment": { "python": "...", "numpy": "...", "scikit-learn": "..." }
}
```

If a number in `metrics.json` cannot be regenerated from `run.json` plus the code, the record is incomplete. The manifest makes silent edits detectable: change a number and the hash changes.

## 2. Seeds, restarts, and variance

Two sources of variation matter here.

**Training variation.** A different split or initialization changes the model. The clean-accuracy differences between splits can be larger than the effect you are trying to measure.

**Attack variation.** Random restarts and random initialization change which adversarial examples are found. More restarts generally increase ASR, which means a single-restart result is a lower bound on the attacker's ability.

LAB-11 fixes the split at seed 42 and uses two restarts for evaluation. That makes the numbers reproducible, but it does not tell you how much they would move with another split. To estimate that, rerun the entire experiment with at least three seeds and report the range.

A practical reporting form:

| Model | Robust acc. mean | Robust acc. range | ASR mean | ASR range |
|---|---:|---:|---:|---:|
| Undefended | 0.62 | 0.59–0.64 | 0.36 | 0.33–0.39 |
| Adversarially trained | 0.73 | 0.70–0.75 | 0.18 | 0.16–0.21 |

The numbers in that table are illustrative of the *form*, not measured. Do not copy them; run your own. The point is that a claim of a 10-point gain is credible when the ranges do not overlap, and suspect when they do.

### A single seed is not a result

If you report one run, say so. If you report three, say which statistic you are quoting. "0.7296" is a run; "0.73 ± 0.02 over three seeds" is a result with an uncertainty. The second is more useful even when it is less precise.

## 3. Tolerances and checkers

LAB-11's checker compares your `metrics.json` with `expected_metrics.json` within a tolerance. The tolerance exists because floating-point results can vary slightly across library versions and platforms.

A tolerance is not permission to be sloppy. It encodes an expected source of variation. If your numbers differ by more than the tolerance, one of these is true:

- your split or preprocessing differs;
- your attack configuration differs;
- your library version changes numerics materially;
- your code has a bug.

The checker cannot tell which. That is your job in the report.

### What a passing checker proves

A passing checker proves that your artifacts are **consistent with the reference experiment** within the stated tolerance. It does not prove:

- that the defense is secure;
- that the attack is the strongest possible;
- that the result generalizes to another dataset or model;
- that the threat model matches your deployment.

This distinction is the module's recurring theme. Tests verify conformance; they do not verify security.

## 4. Standardized attacks and benchmarks

Individual evaluations vary because attackers vary. Two responses have emerged.

**AutoAttack** (Croce and Hein, 2020) is an ensemble of parameter-free attacks: an APGD variant with cross-entropy loss, a target-class variant, a difference-of-logits variant, and a black-box Square attack. Because the attacks do not need per-model tuning, they reduce the chance that a weak step size flatters a defense. Running an ensemble is more expensive than running one PGD, and it is the standard way to make an empirical number comparable.

**RobustBench** (Croce et al., 2020) is a public benchmark with a fixed protocol, model zoo, and leaderboard. It makes results comparable across papers for the datasets and threat models it covers.

Neither removes the need for judgment.

| What a benchmark gives | What it does not give |
|---|---|
| A shared attack protocol | Your data distribution |
| Comparable model results | Your deployment budget |
| A public reference point | A guarantee for your model |
| Reproducible evaluation code | An adaptive attack against your custom defense |

A leaderboard rank is a statement about a benchmark. It is not a statement about your system.

### Why this course uses a small custom evaluation

LAB-11 runs a small, readable PGD implementation on digits. That choice has costs — no AutoAttack, no neural network, no large-scale benchmark — and benefits: you can read every line, run it on a laptop, and see the adaptive attack mechanism directly.

The lab is a demonstration of method, not a measurement of state-of-the-art robustness. Both statements belong in the report.

## 5. Reproducing the lab from a clean state

The full reproduction sequence is:

```bash
cd labs/lab-11-defense-evaluation
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab11.py --artifacts artifacts
```

Three habits make this work:

1. **Pin the environment.** `requirements.txt` points at the shared Level 1 pins, so NumPy and scikit-learn versions match the reference run.
2. **Write artifacts, do not print and forget.** Every number in the report comes from `metrics.json`.
3. **Clean before rerunning.** A stale `artifacts/` directory can mask a failure; delete it or write to a fresh path.

### A reproduction checklist

- [ ] Fresh environment from the pinned requirements.
- [ ] Fixed seeds for the split, the model, and the attack.
- [ ] A single command that regenerates every number.
- [ ] A checker that fails on a missing or inconsistent field.
- [ ] A report that states the command, the versions, and the limitations.
- [ ] A second run on a different machine or date, with the difference noted.

The last item is the one most often skipped. Reproducibility is a claim about another person's machine, not only yours.

## 6. Reporting uncertainty without overstating it

Uncertainty reporting has two failure modes: hiding it and overdoing it.

**Hiding it** looks like a single number with no seed, no interval, and no caveats. A reader cannot tell whether the reported difference is real.

**Overdoing it** looks like an interval so wide that no decision is possible, usually because the experiment is too small for the question. The fix is not a wider interval; it is a better experiment.

A middle path for a lab report:

> Over three seeds, the undefended model's robust accuracy at ε = 0.10 ranged from 0.59 to 0.64 (mean 0.62), and the adversarially trained model's ranged from 0.70 to 0.75 (mean 0.73). The ranges do not overlap, so the gain is larger than the observed run-to-run variation in this setup. The experiment does not estimate variation from other datasets, model families, or attack configurations.

The last sentence is the scoping statement. It tells the reader what the interval does not cover.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reporting a number without the attack configuration | The attack feels like an implementation detail | Record steps, step size, restarts, and loss |
| Comparing two papers' ASR directly | Both say "PGD" | Compare the full protocols, or re-run both |
| Treating a tolerance pass as validation of the defense | The checker is automated | State what conformance does and does not prove |
| Reporting one seed | It is faster | Run at least three, or label the result as a single run |
| Averaging seeds without reporting spread | The mean looks cleaner | Report the range or standard deviation |
| Reusing an old `artifacts/` directory | It saves time | Delete and regenerate |
| Quoting a leaderboard result for a custom model | It is convenient | Benchmark the custom model or state the gap |
| Omitting the limitation that the attack is one family | The result looks stronger | Say which attacks were not run |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Checker fails on a metric that looks correct | Stale artifacts or wrong field | Regenerate and inspect `metrics.json` |
| Results differ between machines | Library version or platform numerics | Compare `run.json` environments; document the difference |
| ASR changes between identical runs | Unseeded randomness in restarts | Seed the RNG for every attack call |
| Checker passes but the report's numbers differ | Report was written from console output | Generate the report from `metrics.json` |
| Experiment takes much longer than documented | Different thread count or BLAS backend | Record the runtime and the environment |
| Manifest mismatch after editing | Artifacts changed after the manifest was built | Rebuild the manifest; never hand-edit hashed files |
| Cannot reproduce a published ASR | Unknown attack configuration | Ask for the protocol; without it, the number is not comparable |

## Check your understanding

1. List five fields that must be recorded for a robustness result to be reproducible.
2. Why does increasing the number of restarts generally increase ASR?
3. What does a passing checker prove, and what does it not prove?
4. Two teams report the same model at 68% and 54% robust accuracy. Give three protocol differences that could explain the gap.
5. What is one thing AutoAttack standardizes and one thing it cannot standardize for your deployment?

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- A robustness number is only meaningful with its protocol: data, split, preprocessing, model, attack, base set, metric, versions.
- LAB-11 records metrics, run configuration, report, and manifest hashes; the manifest makes edits detectable.
- Seeds fix a run; multiple seeds estimate variation. Report spread, not just a mean.
- A tolerance encodes expected numerical variation, not permission for a different experiment.
- A passing checker proves conformance with a reference experiment, not security.
- AutoAttack and RobustBench make comparisons more reliable within their scope; they do not certify your deployment.
- Reproducibility is a claim about another person's machine. Test it there, or say you did not.

## Next

Continue to [Lesson 08.6 — Reporting robustness and defense limits](lesson-6-reporting-robustness.md), where the evaluation becomes a decision document.
