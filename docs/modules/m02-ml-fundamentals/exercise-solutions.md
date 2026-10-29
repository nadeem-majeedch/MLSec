# Module 02 Exercise Solutions

**Read this after a first attempt.** Numbers are computed with the formulas in Lessons 02.3 and 02.4. If your result differs, check the denominator and the rounding before assuming a conceptual error.

---

## Exercise 1 — Compute the operating point

### 1. Metrics

For each threshold:

$$
\text{precision} = \frac{TP}{TP+FP}
\qquad
\text{recall} = \frac{TP}{TP+FN}
\qquad
F_1 = 2\frac{PR}{P+R}
$$

| Threshold | TP | FP | FN | Precision | Recall | F1 | Flagged |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.20 | 29 | 34 | 27 | 0.460 | 0.518 | 0.487 | 63 |
| 0.30 | 17 | 11 | 39 | 0.607 | 0.304 | 0.405 | 28 |
| 0.50 | 7 | 1 | 49 | 0.875 | 0.125 | 0.219 | 8 |

Arithmetic for 0.20:

- Precision: $29/63 = 0.4603$
- Recall: $29/56 = 0.5179$
- F1: $2 \cdot 0.4603 \cdot 0.5179 / (0.4603 + 0.5179) = 0.4874$

### 2. Capacity 75, missed fraud 10× a review

Use a simple expected-cost model in review units per 500 transactions:

$$
\text{cost} = 10 \cdot FN + 1 \cdot FP
$$

| Threshold | FN cost | FP cost | Total | Fits capacity 75? |
|---:|---:|---:|---:|---|
| 0.20 | 270 | 34 | **304** | Yes (63 alerts) |
| 0.30 | 390 | 11 | 401 | Yes (28 alerts) |
| 0.50 | 490 | 1 | 491 | Yes (8 alerts) |

**Recommendation: 0.20.** It has the lowest expected cost, fits the 75-alert capacity, and finds 29 of 56 frauds. Precision is lower, but at a 10:1 miss-to-review cost ratio that is the right trade.

The F1-optimal threshold among these three is also 0.20, but that agreement is a coincidence of this cost ratio. Do not use F1 as a substitute for the cost model; recompute when the ratio changes.

### 3. Capacity 25

At 0.30 the model flags 28, which exceeds a hard cap of 25. At 0.50 it flags 8 and finds 7 frauds. Under a strict cap, 0.50 is the only feasible option in the table, with recall 0.125 and expected cost 491.

That is a bad outcome caused by a resourcing constraint, not a modeling one. The right report says: "At a 25-alert capacity, recall is 0.125 and 49 of 56 frauds are missed. Raising capacity to 75 would allow threshold 0.20, which reduces expected cost from 491 to 304 review units." Quantify the cost of the constraint instead of silently accepting it.

### 4. Why the highest-precision threshold can still be wrong

Precision 0.875 at 0.50 is attractive, but the model flags only 8 cases and misses 49 of 56 frauds. Precision ignores false negatives entirely. A model that predicts positive once and is right has precision 1.0 and recall near zero.

### Self-check

- Did you use actual positives (56) as the recall denominator, not flagged rows?
- Did you state the cost ratio you used?
- Did you notice that 0.30 is infeasible at capacity 25?

---

## Exercise 2 — Screen a new feature for leakage

### 1. Outputs

```text
positives 239
positive rate 0.1593
agreement 0.9173
univariate auc 0.9271
```

Code:

```python
print(f"positives {int(y.sum())}")
print(f"positive rate {y.mean():.4f}")
print(f"agreement {(late_fee_flag == y).mean():.4f}")
print(f"univariate auc {roc_auc_score(y, late_fee_flag):.4f}")
```

The feature agrees with the label on 91.73% of rows and has AUC 0.9271 by itself. For comparison, a realistic model on this kind of data would be far below that. The feature is almost the label.

### 2. Include it?

**No.** The feature is written by the billing system when the account is closed. A churn model scored **before** renewal cannot see a value that is written at closure. At scoring time the field is empty, stale, or later backfilled with the outcome.

The AUC is a symptom. The timestamp is the reason. A feature can have a high AUC and still be legitimate (for example, a strong behavioral signal recorded before the decision); a feature recorded after the outcome is unusable regardless of its AUC.

### 3. `support_calls_30d` with AUC 0.62

Treat it differently. It is recorded daily before renewal, so it is available at scoring time and has a plausible causal path: more support calls can precede cancellation. AUC 0.62 is a moderate signal, not a near-label.

Keep it, subject to the checks below. The decision rule is:

| Question | `late_fee_flag` | `support_calls_30d` |
|---|---|---|
| Recorded before prediction? | No | Yes |
| Plausible causal path? | No, it is a consequence | Yes |
| AUC alone | 0.93 | 0.62 |
| Decision | Exclude | Keep and monitor |

### 4. Additional checks

1. **Availability test.** Build a point-in-time feature table for a past scoring date and confirm the feature has a non-null, correct value for most rows without using future data.
2. **Time-sliced AUC.** Compute the feature's AUC in several months. A leak often weakens or vanishes when the evaluation is strictly forward-looking.
3. **Ablation.** Remove the feature and compare the same folds. A large drop is consistent with dependence; it is not proof of leakage.
4. **Provenance and missingness.** Identify the writing system, the write event, and the missingness pattern. A field that is populated only after cancellation is leaky even if it is sometimes missing.
5. **Correlation with the label window.** Check whether the feature changes after the label date. A value that updates at closure is a giveaway.

### Self-check

- Did you compute AUC on the full dataset before splitting? For a screening diagnostic, that is acceptable; for a reported model metric, it is not.
- Did you justify exclusion by timestamp, not only by AUC?
- Did you avoid the opposite mistake of dropping every strong feature?

---

## Exercise 3 — Calibration by hand

### 1. Brier score

$$
\text{Brier} = \frac{1}{n}\sum_{i=1}^{n}(p_i - y_i)^2
$$

Squared errors: 0.0100, 0.0400, 0.0400, 0.1600, 0.0900, 0.0100, 0.1600, 0.0900, 0.0625, 0.0625.

Sum = 0.7250, so Brier = **0.0725**.

```python
print(round(np.mean((p - y) ** 2), 4))   # 0.0725
```

### 2. Reliability table

| Bin | n | Mean predicted | Observed positive rate |
|---|---:|---:|---:|
| 0.0–0.2 | 1 | 0.100 | 0.000 |
| 0.2–0.4 | 3 | 0.250 | 0.000 |
| 0.4–0.6 | 1 | 0.400 | 0.000 |
| 0.6–0.8 | 3 | 0.683 | 1.000 |
| 0.8–1.0 | 2 | 0.850 | 1.000 |

The bins contain 10 predictions in total. Bin edges follow the convention "lower inclusive, upper exclusive" except the last bin, which includes 1.0.

### 3. Perfect AUC, imperfect calibration

ROC-AUC is **1.0**. Every positive has a higher score than every negative:

- Lowest positive score: 0.60
- Highest negative score: 0.40

Any threshold between 0.40 and 0.60 separates them perfectly, so the ranking is perfect.

Calibration compares the *magnitude* of the probabilities with observed frequencies. In the 0.6–0.8 bin the model predicts about 0.68 and every case is positive; in the 0.8–1.0 bin it predicts 0.85 and every case is positive. In the low bins it predicts 0.10–0.40 and none are positive. The model is **under-confident at the top and over-confident at the bottom**, even though it ranks perfectly.

This is why a model can be excellent for ranking and poor for pricing or risk display. AUC measures order; calibration measures the number.

### 4. Mean probability equals base rate

No. The overall mean is 0.500 and the observed rate is 0.500, but that is an aggregate coincidence. Calibration is local: within each score range, predicted and observed rates should agree. Here the 0.2–0.4 bin predicts 0.25 and observes 0.00, and the 0.6–0.8 bin predicts 0.683 and observes 1.00. A model can balance on average and be wrong everywhere.

### Self-check

- Did you square the errors before averaging?
- Did you use predicted probability, not the predicted class, in the Brier score?
- Did you explain calibration as a local property?

---

## Exercise 4 — Scenario: audit the 0.993

### 1. Problems

| # | Problem | Likely effect | Why |
|---|---|---|---|
| 1 | `late_fee_flag` is recorded at closure | Too high | Target leakage; unavailable before renewal |
| 2 | `account_closed_date` is recorded at closure | Too high | Another post-outcome field; also an identifier-like timestamp |
| 3 | Random 80/20 split on customer rows | Too high | Same customers can appear in train and test; duplicate leakage |
| 4 | No cross-validation; one split | Unknown | A single holdout has sampling variance; two stable runs do not measure it |
| 5 | Accuracy 0.97 at 8% churn | Too flattering | A majority baseline reaches 0.92; recall may be near zero |
| 6 | No baseline | Unknown | 0.97 has no reference point |
| 7 | No seed | Non-reproducible | "Stable across two runs" may reflect the same data order or environment, not robustness |
| 8 | Threshold 0.5 unexamined | Unknown | The operating point is a decision, not a default |
| 9 | No calibration or interval | Overconfident claim | 0.993 is reported with no uncertainty and no probability check |

Items 1–5 are the core set. The rest show a deeper review.

### 2. Repair plan

| Step | Check | Report |
|---|---|---|
| 1. Provenance audit | When is each feature written? Remove fields recorded after the scoring date | List of removed features; before/after univariate AUC |
| 2. Deduplicate and regroup | Count duplicate customers and overlap; split by `customer_id`, preferably time-ordered | Group holdout with zero overlap; customer counts |
| 3. Pipeline and CV | Imputation, scaling, and model inside one pipeline; stratified group CV | Mean and spread of PR-AUC and recall |
| 4. Metrics and threshold | Choose the threshold on validation under the review capacity; add a majority baseline; bootstrap the test set | Precision, recall, F1, PR-AUC, calibration, 95% CI |

Add a fifth check if time allows: a time-sliced backtest, training on earlier months and testing on later ones. A model that only works with a random split is not ready for a production scoring date.

### 3. Illustrative repaired claim

The numbers below are **illustrative placeholders**, not measurements. Replace them with your lab results.

> On a customer-grouped, time-ordered holdout of 2,400 customers (8.0% churn), the repaired pipeline reaches PR-AUC 0.34 and recall 0.41 at a threshold chosen for 75 alerts per 1,000 customers (precision 0.29), versus PR-AUC 0.08 for the majority-class baseline. The 95% bootstrap interval for recall is 0.31–0.51. The model is suitable for prioritizing manual review, not for automatic cancellation; calibration is imperfect above 0.7, and the holdout covers one renewal cycle.

Why this is better:

- Names the protocol (grouped, time-ordered) and the unit (customers).
- Reports a rare-event metric and a threshold tied to capacity.
- Includes a baseline and an interval.
- States a decision boundary and a limitation.
- Does not claim the model causes retention or works outside the observed cycle.

### 4. Message draft

> Hi — the 0.993 is striking, and I would like to reproduce it before it goes into the security review. Could you share the dataset snapshot and the notebook, including the split indices? Two things stand out: `late_fee_flag` and `account_closed_date` look like they are written when the account closes, which would make them unavailable at scoring time, and the random split may put the same customers in train and test. I would like to rerun with those fields removed and a customer-grouped split, and compare PR-AUC and recall against a majority baseline.

This asks for evidence, names mechanisms rather than motives, and proposes a concrete rerun.

### Self-check

- Did you identify both post-outcome fields, not just one?
- Did you connect the split to customers, not just "duplicates"?
- Is your repaired claim falsifiable and clearly labeled if illustrative?
- Would your colleague be willing to run the plan with you?

---

## Self-assessment rubric

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Metric arithmetic | Errors in denominators or formulas | One arithmetic slip | All metrics correct |
| Threshold reasoning | Picks F1 or 0.5 by default | Mentions capacity but not cost | Ties threshold to capacity and cost, and states the trade-off |
| Leakage reasoning | Drops or keeps a feature by AUC alone | Uses timing but not empirical checks | Combines provenance, timing, and an ablation or slice |
| Calibration | Confuses AUC with calibration | Computes Brier but not bins | Separates ranking from calibration with local evidence |
| Reporting | One number | Metric plus baseline | Protocol, metrics, baseline, interval, slices, limitation |
| Communication | Accusatory or vague | Specific but incomplete | Specific, evidence-seeking, non-accusatory |

A total of 10–12 is ready for LAB-01B. Below 8, revisit the matching lesson; the lab assumes these skills.

## Next step

Complete the [portfolio checklist](exercises.md#portfolio-checklist), then start [LAB-01B](../../labs/lab-01b.md). The lab's checker validates the repaired metrics and the report sections, so keep your commands and seeds.
