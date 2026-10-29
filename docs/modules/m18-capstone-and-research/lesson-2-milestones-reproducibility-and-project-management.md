# Lesson 18.2 — Milestones, Reproducibility, and Project Management

<a id="m18-l2"></a>

**Module 18 · Lesson 2 of 4 · 1 hour · LO-33**

## Scenario

Two capstones reach week nine with the same number of hours logged.

The first has a notebook that runs, a results folder with 40 files named `final_v3`, and a report outline that says "results TBD." It cannot say what its clean baseline was, because the baseline was overwritten when the threshold changed. The defense results look good, but the evaluation set was resampled after the attack. The reproducibility package is a list of packages to install "later."

The second has six tagged milestones, each with a one-paragraph gate note. Its baseline directory is read-only and hashed. Its attack results reference the baseline hash. Its defense results reference the attack run IDs. Its report was written from a results table that existed before the report. It finishes on time because the last week is writing, not discovering.

The difference is not speed. It is that the second project treated its own process as an artifact.

## Objectives

By the end of this lesson you will be able to:

1. Define six milestones with entry and exit criteria and required evidence.
2. Specify a reproducibility package that passes a clean-checkout test.
3. Keep a weekly log and a decision record that explain the project's history.
4. Budget 40 hours with a buffer, and cut scope in a way that preserves the claim.
5. Register project risks separately from threat-model risks.

## 1. Milestones are gates, not dates

A milestone closes when its exit criterion is met, not when the calendar says so.

| Milestone | Entry criterion | Exit criterion | Evidence | Gate question |
|---|---|---|---|---|
| M0 Proposal | Option chosen | Scope, question, budget, non-goals frozen | `proposal.md` | Can someone else state what will be measured? |
| M1 Threat model | M0 closed | Assets, boundaries, adversary profiles, ≥ 5 risks | `threat-model.md`, `risk-register.csv` | Is every test traceable to a risk? |
| M2 Baseline | M1 closed | Clean metric reproduces from a clean checkout | `baseline/`, `manifest.json`, run record | Is the denominator frozen and hashed? |
| M3 Attacks | M2 closed | ≥ 3 attacks with budgets, oracles, results | `experiments/`, `results.csv` | Does each attack answer a registered risk? |
| M4 Defense | M3 closed | ≥ 1 control replayed + adaptive variant | `defense/`, before/after matrix | Did the control survive a variant? |
| M5 Report | M4 closed | Report, briefing, package pass checks | `report.pdf`, `briefing/`, package | Can a stranger reproduce the headline number? |

### Gate review in ten minutes

For each milestone, answer five questions in the log:

1. What was the exit criterion, and is there evidence for it?
2. What changed since the previous gate?
3. What is now out of scope that was previously in scope?
4. What is the largest remaining risk?
5. What is the next single action?

If question 1 cannot be answered with a file, the gate is not closed.

## 2. The reproducibility contract

Reproducibility is a property of the package, not of your memory.

### The minimum package

```text
capstone/
  README.md              # what it is, how to run, expected runtime
  proposal.md            # frozen at M0
  threat-model.md
  risk-register.csv
  requirements.txt       # exact versions (pip freeze)
  environment.txt        # python --version, OS, CPU, key library versions
  data/
    make_data.py         # generator, seed as argument
    DATA.md              # source, license, checksum, generation command
  src/
    train.py
    attack.py
    defend.py
    evaluate.py
  configs/
    baseline.yaml
    attack.yaml
    defense.yaml
  scripts/
    run_all.sh           # one command reproduces the headline result
  results/
    baseline/            # frozen metrics + run.json
    attacks/
    defense/
  report/
    report.md
    figures/
  manifest.json          # artifact hashes
```

### What must be pinned, hashed, and seeded

| Item | Pin | Hash | Seed |
|---|---|---|---|
| Python and packages | `requirements.txt` with exact versions | `environment.txt` | n/a |
| Data | Generator version and parameters | SHA-256 of the generated file | Generator seed |
| Split | Split definition and indices | Hash of the split file | Split seed |
| Model | Hyperparameters and training config | Hash of the model artifact | Training seed |
| Attack | Budget, steps, restarts | Config hash | Attack seed |
| Evaluation | Metric implementation and base set | Hash of the evaluation set | n/a |
| Results | One row per run | Hash of results CSV | n/a |

### The run record

Every execution writes a `run.json` next to its outputs.

```json
{
  "run_id": "2026-10-28T10-14-03_baseline",
  "command": "python src/train.py --config configs/baseline.yaml",
  "seed": 7,
  "python": "3.14.7",
  "packages": {"numpy": "2.5.2", "pandas": "3.0.5", "scikit-learn": "1.9.0"},
  "data_sha256": "3f9c…",
  "split_sha256": "a71b…",
  "config_sha256": "9e02…",
  "started_utc": "2026-10-28T10:14:03Z",
  "duration_s": 42.1,
  "outputs": ["results/baseline/metrics.json"]
}
```

A results file without a run record is an anecdote.

### The clean-checkout test

Before M5, do this literally:

1. Copy the package to a new directory (or clone a fresh local copy).
2. Create a new virtual environment.
3. Install from `requirements.txt`.
4. Run `scripts/run_all.sh`.
5. Compare the headline number to the report.

If it differs, the package is not reproducible. Fix it before writing the conclusion.

### What never goes in the package

- Real personal data, credentials, API keys, or tokens.
- Model weights or datasets that are large or licensed for local use only; provide the generator or download instructions and a checksum.
- Absolute paths from your machine.
- Notebook outputs containing environment variables or personal paths.

## 3. The weekly log and decision record

A weekly log is evidence of process. It is also how you recover after a two-week gap.

| Field | Content |
|---|---|
| Week and dates | ISO week, start and end |
| Hours | Planned vs actual, by milestone |
| Done | What closed, with links to files |
| Blocked | What is stuck, and the smallest next step |
| Decisions | Decision, alternatives, reason, reversibility |
| Next | The single next action |

### Why decisions need a record

At M5 you will be asked why the threshold is 0.05 and not 0.10. "It seemed reasonable" is not an answer. A decision record from week 4 is.

```text
D-03 (2026-11-02): Detector threshold set to 0.5% FP budget.
Alternatives: 0.1% (too few alerts to measure recall), 1% (queue too noisy).
Reason: matches the exercise's stated analyst capacity; recall 0.80.
Reversible: yes, one config change; requires recalibration.
```

## 4. Budgeting 40 hours

| Milestone | Planned hours | Buffer |
|---|---:|---:|
| M0 Proposal | 2 | 0 |
| M1 Threat model | 4 | 1 |
| M2 Baseline | 6 | 2 |
| M3 Attacks | 14 | 3 |
| M4 Defense | 8 | 2 |
| M5 Report and briefing | 6 | 2 |
| **Total** | **40** | **10 included** |

The buffer is inside the plan, not added to it. If the buffer is consumed by M3, the defense scope shrinks to one control and one variant, not to zero.

### Stop rules

| Trigger | Action |
|---|---|
| A milestone exceeds 150% of its hours | Cut scope; log the cut; do not extend the timeline |
| Baseline will not reproduce after two attempts | Freeze the environment; diagnose before any attack |
| An attack is inconclusive at budget | Record it; do not raise the budget silently |
| The package fails the clean-checkout test | Stop new experiments; fix the package |
| The report is due and M5 evidence is incomplete | Submit what is measured; mark the rest not done |

### Scope cuts that preserve the claim

Cut breadth, not validity.

| Cut | Effect on the claim | Acceptable? |
|---|---|---|
| One attack family instead of three | Narrower claim | Yes, if stated |
| One seed instead of three | Weaker uncertainty | Yes, with a stated limitation |
| One dataset instead of two | No external validity | Yes, if stated |
| Remove the adaptive variant | No generalization claim | Only with an explicit limitation |
| Remove the baseline | No comparison | No |
| Remove the evaluation-set hash | No reproducibility | No |
| Change the metric after seeing results | No valid claim | No |

The last three are not cuts. They are deletions of the evidence the capstone exists to produce.

## 5. Project risks are not threat-model risks

| Register | Question | Example |
|---|---|---|
| Threat register | What can an adversary do to the system? | Cross-tenant decision via body field |
| Project register | What can stop me from measuring it? | Dataset generator produces trivially separable classes |

| ID | Project risk | Trigger | Mitigation |
|---|---|---|---|
| P-01 | Synthetic data too easy | Baseline accuracy > 0.99 | Add label noise and feature overlap; document the change |
| P-02 | Compute insufficient | One run > 20 min | Subsample; reduce restarts; record the budget change |
| P-03 | Skill gap in the defense | No working control by M4 | Choose a simpler control; ask for review |
| P-04 | Time lost to illness | Two weeks with no log | Cut one attack family; keep baseline and defense |
| P-05 | Supervisor or reviewer unavailable | No feedback by week 6 | Freeze scope; use the rubric as the reviewer |
| P-06 | Ethics or data issue | License unclear | Regenerate synthetic data; do not use the source |

The project register is reviewed at every gate. The threat register is reviewed when the system or adversary changes.

## 6. Artifact hygiene and version control

- Commit code, configs, and documentation locally; do not commit data, weights, or secrets.
- Tag each milestone (`m0-proposal`, `m2-baseline`) so the report can reference a version.
- Keep `results/` append-only within a milestone; a rerun gets a new run ID.
- Never edit a result file by hand. Regenerate it.
- Keep a `CHANGELOG.md` with one line per milestone.
- Run the clean-checkout test from the tag, not from the working tree.

The exercises and this course do not require you to publish or push anything. Local tags and commits are enough to make the history auditable.

## 7. Worked example — eight weeks at five hours

| Week | Hours | Milestone | Deliverable |
|---|---:|---|---|
| 1 | 5 | M0 + start M1 | Proposal frozen; assets and boundaries drafted |
| 2 | 5 | M1 | Threat model and risk register complete |
| 3 | 6 | M2 | Data generated, baseline trained, manifest written |
| 4 | 5 | M2 close | Clean-checkout baseline reproduces |
| 5 | 6 | M3 | First two attacks with results |
| 6 | 6 | M3 close | Third attack; results table frozen |
| 7 | 4 | M4 | Control implemented; replay complete |
| 8 | 3 | M4 close + M5 | Variant run; report draft; briefing |
| 9 | 0 | Buffer | Clean-checkout test; final edits |

The plan has slack. A plan without slack fails at the first surprise.

## 8. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Milestones as dates | Gates are skipped | Gate on evidence |
| Baseline overwritten | No comparison | Freeze and hash |
| Results edited by hand | Untraceable numbers | Regenerate from scripts |
| Package built at the end | It does not reproduce | Build it at M2 and update |
| No decision record | Cannot defend choices | Log decisions weekly |
| Buffer treated as extra scope | No recovery time | Protect the buffer |
| Cutting validity to save time | Claim collapses | Cut breadth, not evidence |
| Committing data or weights | Leak or bloat | Generator + checksum |
| No tags | Report references a moving target | Tag every milestone |
| Project risks ignored | Surprise at week 7 | Review the register at gates |

## 9. Check your understanding

1. What makes a milestone a gate rather than a date?
2. List the seven items that must be pinned, hashed, or seeded.
3. What is the clean-checkout test, and when should it be run?
4. Why is a results file without a run record an anecdote?
5. Which scope cuts are acceptable, and which destroy the claim?
6. How does the project risk register differ from the threat register?

## 10. What you keep

Six milestone gates with evidence, a reproducibility package skeleton, a run-record schema, a weekly log and decision record, a 40-hour budget with buffer and stop rules, and a project risk register. Lesson 18.3 covers how to turn the results into tables, figures, and a limitations section.

## 11. Next

Lesson 18.3 covers claim-first results, table and figure design, uncertainty, negative results, and the four kinds of validity threat.
