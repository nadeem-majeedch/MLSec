# Exercise Solutions — Module 18

**Evaluator reference.** Model answers for the Larkspur exercises. Other answers are acceptable when the reasoning and evidence are sound.

---

## Exercise 1 — Audit and rescope

### Defects (any four)

| # | Defect | Consequence |
|---|---|---|
| 1 | No decision or question; the title says "improving security" | Nothing can be falsified |
| 2 | Several attacks and defenses, no traceability to a threat | A menu of experiments, no assessment |
| 3 | No metric, denominator, or budget | Results cannot be compared or interpreted |
| 4 | No cost constraint | A defense that destroys clean accuracy could "win" |
| 5 | "Poisoning if there is time" | Unbounded scope; the second surface is unfunded |
| 6 | No data/compute feasibility statement | 40 hours may be insufficient |
| 7 | No threat model or adversary profile | Attacks are chosen by fashion |

### Rewritten title and question

**Title:** "Does adversarial training reduce bounded evasion in the Larkspur pre-screening model without degrading clean decisions?"

**Question:** "At an L∞ budget of 4/255 with 20 restarts, does adversarial training reduce attack success on the frozen 1,200-application holdout from the baseline mean of 0.63 to below 0.45, while keeping clean accuracy at or above 0.92 and the false-decline rate at or below 2%?"

The question has a system (the mock and holdout), a control (adversarial training), a metric (ASR, clean accuracy, false-decline), a budget (ε, restarts, requests), and a cost constraint.

### Non-goals

- Data poisoning, backdoors, extraction, membership inference, and inversion.
- Production deployment, real applicant data, and vendor feeds.
- Other model families or modalities.
- Network, host, identity-provider, and insider attacks.
- Fairness auditing beyond the reporting of subgroup metrics already in the holdout.

Other specific non-goals are acceptable. "Other attacks" alone is too vague.

---

## Exercise 2 — Milestone plan and project risks

### Plan (40 hours including 8 hours of buffer)

| Milestone | Planned | Buffer | Exit criterion | Evidence |
|---|---:|---:|---|---|
| M0 Proposal | 2 | 0 | Question, scope, non-goals, budget frozen | `proposal.md` |
| M1 Threat model | 4 | 1 | Assets, boundaries, RD-01/RD-02, ≥ 5 risks | `threat-model.md`, `risk-register.csv` |
| M2 Baseline | 5 | 1 | Baseline reproduces from a clean checkout; split hashed | `baseline/`, `manifest.json`, `run.json` |
| M3 Attacks | 11 | 3 | ≥ 3 attacks with budgets and oracles; results table frozen | `experiments/`, `results.csv` |
| M4 Defense | 6 | 2 | AT replayed + adaptive PGD variant | `defense/`, matrix |
| M5 Report | 4 | 1 | Report, briefing, package pass clean-checkout test | `report/`, `briefing/` |
| **Total** | **32** | **8** | | **40** |

### Project risks

| ID | Risk | Trigger | Mitigation |
|---|---|---|---|
| P-01 | Synthetic data too separable | Baseline accuracy > 0.99 or ASR > 0.90 with trivial perturbation | Add feature overlap and label noise; regenerate with a documented seed |
| P-02 | Attack runs exceed compute budget | One full run > 20 min | Subsample the holdout; reduce restarts; record the change |
| P-03 | Adaptive attack not implemented by M4 | No working variant at the gate | Use a transfer attack from an undefended model as the minimum variant |
| P-04 | Scope creep into poisoning | A poisoning notebook appears before M4 closes | Enforce the non-goals; park it as a future extension |

### Scope cut if M3 consumes its buffer

Drop input squeezing and one non-adaptive attack family. Keep the baseline, adversarial training, and the adaptive variant. The cut preserves the comparison that answers the question: AT versus baseline under static and adaptive attack. It removes a secondary condition, not the primary evidence.

---

## Exercise 3 — Reproducibility audit

### Defects (any five)

1. `requirements.txt` has no versions; the environment is unpinned.
2. `applications.csv` has no generator, seed, or checksum; the data cannot be rebuilt or verified.
3. No split definition; the temporal holdout cannot be reconstructed.
4. `final_metrics.json` and `final_metrics_v2.json` have no run records; it is unclear which is current.
5. No config files; hyperparameters and attack budgets live in code or memory.
6. No seed recorded anywhere.
7. No `README.md`, no run command, no expected runtime.
8. The report is a `.docx` with no source or figure scripts.
9. No manifest of artifact hashes.
10. No environment record (Python version, OS, CPU).

### Missing items for a clean-checkout test

```text
requirements.txt            # exact versions
environment.txt             # python, OS, CPU, library versions
README.md                   # what it is, how to run, runtime
data/make_data.py           # generator, seed argument
data/DATA.md                # source, license, checksum, command
configs/baseline.yaml       # model + split + seed
configs/attack.yaml         # budget, steps, restarts
scripts/run_all.sh          # one-command reproduction
results/baseline/run.json   # run record
results/baseline/metrics.json
manifest.json               # hashes of data, split, model, results
report/report.md            # source, with figure scripts
```

### Example `run.json`

```json
{
  "run_id": "2026-11-02T09-40-11_baseline",
  "command": "python src/train.py --config configs/baseline.yaml",
  "seed": 7,
  "python": "3.14.7",
  "packages": {"numpy": "2.5.2", "pandas": "3.0.5", "scikit-learn": "1.9.0"},
  "data_sha256": "b41c…",
  "split_sha256": "7d2a…",
  "config_sha256": "e10f…",
  "started_utc": "2026-11-02T09:40:11Z",
  "duration_s": 38.4,
  "outputs": ["results/baseline/metrics.json", "models/baseline.joblib"]
}
```

Exact field names may differ; the record must link data, split, config, environment, seed, and outputs.

---

## Exercise 4 — Results, limitations, and a research question

### Rewritten claim

"At ε = 4/255 with 20 restarts, adversarial training reduced ASR on the frozen 1,200-application holdout from a baseline mean of 0.63 (seeds 0.60, 0.63, 0.66) to 0.40 (seeds 0.28, 0.41, 0.52), at a clean-accuracy cost of 2.3 points (0.941 to 0.918). Adding input squeezing produced 0.38 (0.26, 0.39, 0.49), a difference within the seed spread, so the data do not show an additional benefit. Under an adaptive PGD run, ASR was 0.49, higher than the static result."

The draft's "eliminates evasion" is unsupported: 0.40 is not zero, the range is wide, and the adaptive result is 0.49.

### Alternative explanation

**Gradient masking.** The static attack may fail because the defense makes gradients uninformative, not because the model is robust. The adaptive run (0.49 vs 0.38) is consistent with this. Test with a transfer attack from an undefended model, a query-based attack, and a stronger adaptive attack at matched compute; if ASR rises under these, the static result overstates robustness.

A second acceptable alternative: the defense may have overfit to the evaluation distribution (internal validity); test on a second split.

### Limitations (three of the four types)

- **Construct:** ASR measures model error, not the loan decision or applicant harm; a decision-level metric (false declines, review rate) is needed.
- **Internal:** the adaptive result is a single run; the threshold and attack budget may have been chosen after seeing static results; the comparison needs a fixed configuration.
- **External:** one synthetic dataset and one model family; the result does not establish behavior for other lenders, features, or architectures.
- **Statistical:** three seeds give a wide range (0.28–0.52 for AT), and the baseline and defense ranges are close enough that the interval matters; the adaptive run has no interval at all.

### Gap statement

"Evaluations of adversarial training in tabular credit models typically report ASR under a fixed static attack at one budget. These results establish a reduction for that attack, but they hold the attack procedure fixed and often report a single run of the adaptive condition. It is therefore unknown whether the reduction survives an adaptive attack at matched compute and whether it holds across model families. This matters because deployment decisions depend on robust performance against an adversary who can query the defense, not only against a scripted attack."

### Research question

"Does the ASR reduction from adversarial training in tabular credit models survive an adaptive, query-based attack at matched compute, at ε = 4/255, across three model families?"

This names a population (tabular credit models), an intervention (adversarial training), a comparator (static attack / undefended baseline), an outcome (ASR at matched compute), and a condition (three families). It can be answered no.

A question about detector pacing (recall under slow-ramp adaptation at a 0.5% FP budget) is also acceptable if the gap statement matches.
