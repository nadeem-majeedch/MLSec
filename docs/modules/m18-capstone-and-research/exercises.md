---
title: Exercises — Module 18
---

# Exercises — Module 18

**Four exercises on one capstone proposal · 40 minutes · portfolio evidence**

These exercises use a fictional proposal so you can practise the decisions before committing forty hours. The capstone remains the assessment; these are the drills.

## Scenario — Larkspur Community Lending

Larkspur Community Lending is a fictional credit union. It runs a local mock service that pre-screens small-business loan applications and returns `approve`, `review`, or `decline`. The mock uses synthetic applications and is used for staff training.

A candidate proposes this capstone:

> **Title:** "Improving the security of the Larkspur pre-screening model."
>
> **Plan:** I will study adversarial machine learning. I will train the model, run several evasion attacks, try adversarial training and input squeezing, and report which defense is best. I will also look at data poisoning if there is time. The report will recommend improvements.

The system details:

```text
Service:    http://127.0.0.1:8070  POST /screen, GET /health
Model:      scikit-learn gradient boosting, version 2.2, threshold 0.50
Data:       6,000 synthetic applications, 18 features, 22% decline rate
Split:      temporal holdout, 1,200 records
Attackers:  external applicant (API only); data contributor (up to 5%)
Logs:       request, decision, auth; no feature-level logging
```

---

## Exercise 1 — Audit and rescope the proposal (10 minutes)

**Tasks**

1. List four defects that prevent this from being a capstone.
2. Rewrite the title and objective as one falsifiable question with a system, a control, a metric, a budget, and a cost constraint.
3. Write four non-goals specific to this system.

**Deliverable:** `ex1_scope.md` with the defect table, the rewritten question, and the non-goals.

**Check:** the question can be answered no; the non-goals name excluded systems and activities, not just "other attacks."

---

## Exercise 2 — Milestone plan and project risks (10 minutes)

**Tasks**

1. Build an M0–M5 table with hours (total 40, including at least 8 hours of buffer), exit criteria, and one evidence file per milestone.
2. Identify two project risks (not threat-model risks), each with a trigger and a mitigation.
3. State one scope cut you would make if M3 consumes its buffer, and what the cut preserves.

**Deliverable:** `ex2_milestones.md`.

**Check:** each gate has an observable exit criterion; the hours sum to 40; the cut removes breadth, not validity.

---

## Exercise 3 — Reproducibility audit (10 minutes)

The candidate's package contains:

```text
capstone/
  train.py
  attack.py
  requirements.txt        # numpy, pandas, scikit-learn (no versions)
  data/applications.csv   # generated once, no generator
  results/final_metrics.json
  results/final_metrics_v2.json
  report/draft.docx
```

**Tasks**

1. List five reproducibility defects.
2. Add the missing items needed for a clean-checkout test (name at least six files or directories).
3. Write the fields of one `run.json` for the baseline run.

**Deliverable:** `ex3_repro.md`.

**Check:** the package can be rebuilt from the generator and pinned versions; the run record links data, split, config, and outputs.

---

## Exercise 4 — Results, limitations, and a research question (10 minutes)

The candidate reports:

| Condition | ASR (seeds) | Clean accuracy | Eval n |
|---|---|---:|---:|
| Baseline | 0.60, 0.63, 0.66 (mean 0.63) | 0.941 | 1,200 |
| Adversarial training | 0.28, 0.41, 0.52 (mean 0.40) | 0.918 | 1,200 |
| Adversarial training + squeezing | 0.26, 0.39, 0.49 (mean 0.38) | 0.914 | 1,200 |
| Adaptive PGD vs best defense | 0.49 (single run) | 0.914 | 1,200 |

Draft claim: *"Adversarial training eliminates evasion, and squeezing adds further protection."*

Detector (not in the table): recall 0.74 at a 0.5% false-positive budget; under a slow-ramp variant, recall 0.46.

**Tasks**

1. Rewrite the claim with a budget, an effect size, an interval or range, and the clean cost.
2. State one alternative explanation the candidate must test.
3. Classify three limitations as construct, internal, external, or statistical.
4. Write a gap statement and one research question that could follow from the adaptive result.

**Deliverable:** `ex4_results.md`.

**Check:** the claim is supported by the table; the alternative is testable; the research question names a gap and an outcome.

---

## Submission

Keep the four files in `exercises/` with a `README.md` naming the date and module. Attempt all four before reading the [exercise solutions](exercise-solutions.md).
