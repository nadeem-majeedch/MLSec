# Module 05 Exercise Solutions

**Read after a first attempt.** Numbers are rounded for display; keep full precision in your own work.

---

## Exercise 1 — Read the poisoning curve

**1. Accuracy drop in percentage points.**

| Rate | Accuracy | Drop (points) |
|---:|---:|---:|
| 0.00 | 0.9667 | 0.00 |
| 0.05 | 0.9648 | 0.19 |
| 0.10 | 0.9389 | 2.78 |
| 0.20 | 0.8870 | 7.97 |
| 0.30 | 0.7981 | 16.86 |

**2. Average and marginal cost.**

| Interval | Average drop per 1 point of poison | Marginal drop per 1 point |
|---|---:|---:|
| 0 → 5% | 0.038 | 0.038 |
| 0 → 10% | 0.278 | 0.518 (5 → 10%) |
| 0 → 20% | 0.3985 | 0.519 (10 → 20%) |
| 0 → 30% | 0.562 | 0.889 (20 → 30%) |

The largest marginal cost is between 20% and 30%: 0.889 points of accuracy per 1 point of poison. The marginal cost is roughly flat at about 0.52 between 5% and 20%, then rises.

**3. Shape.** The curve is convex over this range. The average cost rises with the rate (0.038 → 0.562), and the marginal cost in the last interval (0.889) is much larger than in the middle intervals (about 0.52). A linear curve would have a constant marginal cost.

**4. Why "tolerates 10%" is incomplete.**

- **Metric.** Accuracy is an aggregate availability measure. A targeted attack can flip a chosen decision while accuracy stays flat or rises; 93.9% says nothing about which decisions are wrong.
- **Scope.** 10% is one point on one curve for one model, dataset, and flip rule. It is not a tolerance that transfers to another pipeline, and a single run has sampling uncertainty.

**5. Reporting choice.** Strongest: 30% (largest drop). Weakest: 5%, or 0% if the goal is to show no effect. Selecting the rate after seeing the curve is cherry-picking: the rate is part of the attack hypothesis and should be fixed before the experiment. The honest report shows the whole curve, including the rate 0 baseline and the counts.

---

## Exercise 2 — Audit a broken experiment

**1. Four flaws.**

| Flaw | Why it invalidates or weakens the result | Fix |
|---|---|---|
| Test labels were flipped | The evaluation now measures corrupted labels, not the model's behavior on clean data | Leave `y_test` untouched |
| 180 is 10% of 1,800, not of the 1,260 training rows | The poison rate is stated against the wrong denominator | Compute $0.10 \times 1260 = 126$ |
| The model was fit on the original training labels | The poison never enters training, so the measured drop cannot be an attack effect | Fit on `y_poisoned` |
| "95% CI ±0.1" has no method and no count | A confidence interval needs a sample size, a procedure, and a stated quantity | Report the count and use a binomial interval (for example, Wilson) |

A fifth issue is that one rate and one split cannot establish "vulnerable"; the experiment needs a curve or a pre-registered target.

**2. Correct rates.**

$$
0.10 \times 1260 = 126 \text{ poisoned training rows}.
$$

$$
\frac{180}{1260} = 0.1429 \approx 14.3\%.
$$

**3. The 2.8-point drop is inconsistent with the protocol.** Fitting on the original labels gives the clean model, whose accuracy is 0.9667 in LAB-05. A 0.9389 result requires the poisoned labels to be used in `fit`. So the reported number and the described method cannot both be true.

**4. Example rewrite.**

> We flipped 126 of the 1,260 training labels (10.0%) to the next class and left the 540 test labels unchanged. Logistic regression fitted on the poisoned labels reached 93.9% test accuracy, 2.8 points below the 96.7% clean baseline on the same split. This is one split, one model, and one flip rule; it measures availability, not a targeted attack, and it says nothing about other datasets or pipelines.

**5. Extra experiment.** A targeted poisoning experiment on a decision the system cares about, with a threat model that says who can add or relabel rows, at what budget, and with what knowledge. A second random seed alone would not turn "a drop exists" into "the system is vulnerable to an adversary."

---

## Exercise 3 — GrantGate

**1. Entry points and access levels.**

| Entry point | Access level |
|---|---|
| Applicant form | Row insertion with attacker-chosen features; labels assigned later by reviewers |
| Reviewer labels | Label only |
| Vendor historical batch | Row insertion with labels (and possibly pipeline provenance) |
| Officer decisions → retraining labels | Label only, indirect, through the feedback loop |
| Support console corrections | Label only |
| Audit export | Read-only; not an attack surface for training |

**2. Example threat table.**

| # | Goal | Access | Budget | Knowledge | Metric | Stage |
|---|---|---|---:|---|---|---|
| T1 | Targeted: get a class of applications funded | Reviewer label flips | 1–2% of labels | Review process, not model | Approval rate on a probe set | Labeling |
| T2 | Targeted: get one application funded | Applicant-controlled features | Many submissions | Feature schema | Target application's score | Collection |
| T3 | Availability: degrade the ranking | Vendor batch injection | 5–10% of rows | Data schema, maybe model class | Overall accuracy, rank correlation | Aggregation |
| T4 | Targeted: lower a group's approval rate | Feedback labels from officer decisions | Decisions over time | Decision policy, retraining cadence | Approval rate by group; accuracy unchanged | Deployment / feedback |
| T5 | Targeted: restore a declined application | Support console corrections | A few hundred rows | Console access | Target decision | Labeling |

**3. Which threat first.** T4 is a reasonable first choice. **Feasibility:** the feedback loop turns ordinary decisions into labels with no special data access, and the effect can accumulate over quarters. **Harm:** a systematic approval-rate shift affects people, not just a metric. T1 may be more direct but is easier to audit through reviewer agreement. State the criterion; do not just say "insider risk."

**4. Smallest experiment.** Take a fixed probe set of 200 historical applications, stratified by group. Simulate a 5% shift in the labels of one group in one quarter's feedback data, retrain the same model, and compare the approval rate on the probe set and overall accuracy. Budget: 5% of one quarter's labels. The experiment cannot show that officers actually behave this way, or that the group label is legally or ethically appropriate to use; it only shows whether the feedback channel can move the decision.

**5. Controls and costs.**

- **Dual review for high-impact labels.** Cost: reviewer time and slower turnaround.
- **Delayed or independently verified feedback labels.** Cost: stale training data and extra verification work.
- **Batch provenance and distribution checks for vendor data.** Cost: procurement friction and possible rejection of legitimate batches.
- **Slice monitoring of approval rates.** Cost: false alarms and the need to define groups and thresholds carefully.

At least one of these acts before training: dual review, provenance checks, or delay.

**6. Evidence that changes the ranking.**

- **Lowers T4:** officer decisions are already randomized or audited, and retraining uses only independently verified outcomes. The feedback path is weaker than assumed.
- **Raises T4:** one officer or office dominates a region's decisions, the labels are used directly without verification, and the probe set shows a stable approval-rate gap that grows after retraining.

---

## Exercise 4 — Choose a screening threshold

**1. Metrics.**

| τ | Recall | FPR (clean flagged / 350) | Precision |
|---:|---:|---:|---:|
| 0.50 | 24/30 = 0.8000 | 26/350 = 0.0743 | 24/50 = 0.4800 |
| 0.60 | 30/30 = 1.0000 | 37/350 = 0.1057 | 30/67 = 0.4478 |
| 0.80 | 30/30 = 1.0000 | 86/350 = 0.2457 | 30/116 = 0.2586 |

**2. The 12% constraint.** The clean-row loss must be at most $0.12 \times 350 = 42$ rows.

- τ = 0.50: 26 rows, within budget.
- τ = 0.60: 37 rows, within budget.
- τ = 0.70: 60 rows, over budget.
- τ = 0.80: 86 rows, over budget.

Choose τ = 0.60. It is the tightest threshold within the budget that catches all 30 poisons and restores the target prediction. τ = 0.50 is cheaper but leaves the target flipped.

**3. 95% recall.** τ = 0.60, 0.70, and 0.80 satisfy it (all catch 30/30); τ = 0.50 catches only 80%. Satisfying the recall requirement does **not** guarantee recovery in general: recall counts rows, while the target depends on which rows survive, and a single surviving poison can be enough. In this table every threshold with 30/30 catches also restores the target, but that is a property of this attack, not an implication.

**4. Why τ = 0.70 is not automatically better.** It has the same recall and a slightly higher target probability (0.5626 vs 0.5465), but it removes 60 clean rows instead of 37 — 17.1% of the clean training set — and those rows are disproportionately near the boundary, where future decisions may matter. The target-probability difference is small and comes from one seed; it is not evidence of a better defense. The choice depends on the relative cost of losing clean data and the residual risk of a missed poison.

**5. Reviewer sentences.**

> We screen at τ = 0.60, which catches all 30 injected poisons while removing 37 of 350 clean training rows (10.6%) and restores the targeted decision. This choice assumes the 150-row reference set is clean, representative, and outside the attacker's control; if that assumption fails, the screen's guarantees do not hold.

---

## Notes on grading

| Exercise | Common weak answer | What earns credit |
|---|---|---|
| 1 | Reports drops as fractions and calls the curve "exponential" | Uses percentage points and shows marginal costs |
| 2 | Finds the test-set flaw but not the fitting flaw | Connects each flaw to the measured result |
| 3 | Lists threats without access levels or metrics | Makes each threat testable and names a control cost |
| 4 | Picks τ = 0.8 "to be safe" | Applies the row budget and measures the protected outcome |
