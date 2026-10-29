# Lesson 02.4 — Leakage, Error Analysis, and Trustworthy Reporting

**2 hours · Lesson 4 of 4 · Prerequisite: Lesson 02.3**

## Scenario

A churn model reports ROC-AUC 0.99. The feature importance table has one dominant entry: `late_fee_flag`. The field is written by the billing system when an account is closed and a final fee is assessed. It is recorded *after* the customer has churned.

The model is not predicting churn. It is reading the outcome. In production, the field is empty or null at scoring time, so the model's real performance is unknown. The 0.99 is a measurement of a column, not a capability.

This lesson is about catching that class of error before it reaches a report, and about writing results that survive scrutiny when it does not.

## What you will be able to do

- Name and detect the four main leakage families: pipeline, target, duplicate/group, and temporal.
- Use univariate AUC, ablation, overlap counts, and date checks as diagnostics.
- Analyze errors by slice instead of only in aggregate.
- Report a metric with a confidence interval, a baseline, and a reproduction command.

## 1. The leakage families

| Family | Mechanism | Example | Repair |
|---|---|---|---|
| **Pipeline** | Preprocessing fitted on data that includes validation or test rows | Scaling, imputation, or feature selection before the split | Put every transformer inside a `Pipeline` |
| **Target** | A feature contains information from the label or the label window | `late_fee_flag`, `cancellation_reason`, `refund_date` | Remove the feature; verify availability at inference |
| **Duplicate / group** | The same entity or a near-duplicate appears in train and test | Four sessions per customer, copied rows | Deduplicate; split by group |
| **Temporal** | Training uses future information relative to the prediction | Random split on time-ordered events | Train on the past, test on the future |
| **Join** | A many-to-many join multiplies rows or attaches the wrong label | Orders joined to sessions on a non-unique key | Verify cardinality; aggregate before joining |

Leakage is not always a bug in the code. It is often a bug in the *question*. If the label is defined after the features are collected, and the feature table includes the label window, the data is structurally leaky even if every line of code is correct.

## 2. Detecting target leakage

The fastest diagnostic is univariate: how well does each feature separate the classes **on its own**?

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score

X, y = make_classification(
    n_samples=2000, n_features=10, n_informative=4, n_redundant=2,
    weights=[0.9, 0.1], class_sep=1.0, flip_y=0.02, random_state=42,
)
rng = np.random.default_rng(7)
flip = rng.random(len(y)) < 0.10
late_fee_flag = np.where(flip, 1 - y, y)

print(f"agreement with label {(late_fee_flag == y).mean():.4f}")
print(f"univariate auc      {roc_auc_score(y, late_fee_flag):.4f}")
```

Expected output:

```text
agreement with label 0.9025
univariate auc      0.9119
```

A single binary feature with AUC 0.91 on a problem where the full model in Lesson 02.3 reached 0.75 is a red flag. Real features can be strong, but a suspiciously dominant feature deserves a provenance check: *when is this column written, by which system, and is it available at the scoring timestamp?*

A simple screening rule:

1. Compute univariate AUC (or mutual information) for every feature.
2. Rank them.
3. For the top few, write down the system, the timestamp, and the data owner.
4. Remove any feature recorded after the prediction time, then re-run.

The rule is not "drop every strong feature". It is "explain every strong feature". A legitimate strong feature has a plausible causal path from before the prediction to the outcome.

### Ablation

Remove the suspect feature and compare the same folds:

| Model | ROC-AUC | PR-AUC |
|---|---:|---:|
| All features, including `late_fee_flag` | 0.99 | 0.97 |
| Honest features only | 0.75 | 0.46 |

A large drop is consistent with leakage, but it is not proof: the feature could be legitimately predictive. The provenance check is what decides. The ablation tells you how much the result depended on it.

## 3. Detecting duplicate and group leakage

The diagnostic is a count, not a model: how many entities appear on both sides of the split?

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split

rng = np.random.default_rng(0)
n_customers, per_customer = 600, 4
customer = np.repeat(np.arange(n_customers), per_customer)
customer_effect = rng.normal(0, 1.0, size=(n_customers, 8))
session_noise = rng.normal(0, 0.1, size=(n_customers * per_customer, 8))
Xg = customer_effect[customer] + session_noise

score = (0.9 * customer_effect[:, 0] + 0.6 * customer_effect[:, 1]
         - 0.4 * customer_effect[:, 2] + rng.normal(0, 0.8, n_customers))
y_customer = (score > np.median(score)).astype(int)
yg = y_customer[customer]

idx_tr, idx_te = train_test_split(
    np.arange(len(yg)), test_size=0.25, random_state=42, stratify=yg)
rf = RandomForestClassifier(n_estimators=200, random_state=42).fit(Xg[idx_tr], yg[idx_tr])
acc_random = accuracy_score(yg[idx_te], rf.predict(Xg[idx_te]))
overlap = len(set(customer[idx_tr]) & set(customer[idx_te]))

gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
tr, te = next(gss.split(Xg, yg, groups=customer))
rf2 = RandomForestClassifier(n_estimators=200, random_state=42).fit(Xg[tr], yg[tr])
acc_group = accuracy_score(yg[te], rf2.predict(Xg[te]))

print(f"random split accuracy {acc_random:.4f}")
print(f"group split accuracy  {acc_group:.4f}")
print(f"gap                   {acc_random - acc_group:.4f}")
print(f"customers in both     {overlap}")
```

Expected output:

```text
random split accuracy 0.9650
group split accuracy  0.7750
gap                   0.1900
customers in both     403
```

The random split is **19 points** too optimistic because 403 customers appear on both sides. Their four sessions are nearly identical, so the forest can memorize a customer's label from one session and retrieve it from another. Grouping by customer removes the overlap and the inflation.

The same logic applies to devices, IP addresses, user accounts, files with the same hash, and near-duplicate images. The group key is whatever defines independence in your problem, and it is your job to name it.

## 4. Temporal leakage

A random split on time-ordered data trains on the future and tests on the past. This is common in security datasets where attack campaigns persist across months and the same infrastructure appears in both periods.

Checks:

- Compare the minimum and maximum timestamp in each split.
- Verify that every training timestamp is earlier than every test timestamp.
- Check that features are computed from data available at the cutoff.
- Look for entities (IPs, accounts, malware hashes) that appear across the cutoff.

A time-ordered split usually produces a lower and more honest score. A large drop when moving from random to temporal splitting is itself a finding: it means the model was relying on temporal proximity or repeated entities.

## 5. Error analysis by slice

Aggregate metrics hide where a model fails. Slice the errors by groups that matter:

| Slice | Question | Why |
|---|---|---|
| Class | Is recall different for the positive class? | The headline metric may hide the rare class |
| Segment | Does performance differ by product, region, or tenant? | A model can be good on average and bad for a subgroup |
| Confidence | Are high-confidence errors rare? | Confident mistakes are the most damaging |
| Time | Does performance decay after deployment? | Drift and concept change |
| Source | Does performance differ by data source? | One source may be poisoned or mislabeled |
| Label quality | Are errors concentrated where labels are uncertain? | Label noise caps achievable performance |

A practical workflow:

1. Sort the test set by loss, descending.
2. Read the top 50 errors and their features.
3. Group them by a hypothesis (a segment, a missing value pattern, a duplicate).
4. Quantify the group's error rate.
5. Decide whether to fix the data, the model, or the metric.

This is qualitative work with a quantitative check. It is how you find the problem that no dashboard shows.

## 6. Uncertainty: bootstrap confidence intervals

A test accuracy of 0.900 on 500 rows is not a point. It is an estimate with sampling error. The bootstrap estimates that error by resampling the test set with replacement.

```python
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Continuing Lesson 02.3: yte, pred are the test labels and predictions.
rng = np.random.default_rng(42)
n = len(yte)
boot = {"accuracy": [], "recall": [], "precision": []}
for _ in range(2000):
    idx = rng.integers(0, n, n)
    boot["accuracy"].append(accuracy_score(yte[idx], pred[idx]))
    boot["recall"].append(recall_score(yte[idx], pred[idx], zero_division=0))
    boot["precision"].append(precision_score(yte[idx], pred[idx], zero_division=0))

for name, values in boot.items():
    lo, hi = np.percentile(values, [2.5, 97.5])
    print(f"{name:9s} {np.mean(values):.4f}  95% CI [{lo:.4f}, {hi:.4f}]")
```

Expected output:

```text
accuracy  0.9004  95% CI [0.8720, 0.9260]
recall    0.1240  95% CI [0.0408, 0.2200]
precision 0.8684  95% CI [0.5556, 1.0000]
```

The bootstrap means are close to the point estimates (0.9000, 0.1250, 0.8750). The intervals are wide, especially for recall and precision, because there are only 56 positives. This is the honest resolution of a 500-row test set: differences smaller than about 2.5 accuracy points are not distinguishable.

The bootstrap assumes the test rows are exchangeable. If they are grouped or time-ordered, resample **groups** or **blocks**, not individual rows. Otherwise the interval is too narrow, which is the same leakage problem in a different costume.

## 7. A reporting template

Use this structure for every result you publish, including lab artifacts:

```text
Claim:        One sentence with the metric, threshold, and comparison.
Protocol:     Split strategy, folds, seed, and what was tuned on which set.
Data:         Source, size, positive rate, filters, snapshot hash.
Model:        Family, features, preprocessing, hyperparameters.
Metrics:      Point estimate and 95% CI for each metric.
Baseline:     Majority class and simple model, on the same split.
Slices:       At least two slices with their metrics.
Limitations:  What the protocol cannot show; known leakage or timing risks.
Reproduce:    One command, pinned environment, saved split, manifest.
```

Weak claim: "The model is 90% accurate, so it is ready."

Stronger claim: "On a customer-grouped, time-ordered holdout of 500 rows (56 positives), the pipeline reaches recall 0.125 (95% CI 0.041–0.220) at a 0.5 threshold, versus 0.0 for the majority baseline; PR-AUC is 0.465 at a base rate of 0.112. The model is not ready for automatic decisions; the threshold and the operating cost are unresolved, and the 56-positive holdout limits precision estimates."

The stronger claim is longer. It is also falsifiable, reproducible, and useful. Length is not the virtue; specificity is.

### Reporting checklist

- [ ] The unit of prediction is stated.
- [ ] The label definition and window are stated.
- [ ] The split is described, and group or temporal structure is handled.
- [ ] The threshold is stated and was chosen on validation data.
- [ ] A majority-class baseline is reported.
- [ ] Precision, recall, F1, PR-AUC, and the confusion matrix are reported for rare events.
- [ ] Calibration is reported if probabilities drive decisions.
- [ ] At least two slices are reported.
- [ ] A confidence interval or fold spread is reported.
- [ ] Limitations name the biggest threat to validity.
- [ ] The seed, environment, data hash, and command are recorded.
- [ ] No test-set tuning occurred.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Trusting one dominant feature | AUC near 1.0, one feature dominates | Provenance check and ablation |
| Splitting rows when entities repeat | Test score far above production | Count overlap; group split |
| Random split on time data | Good backtest, poor deployment | Time cutoff; verify entity overlap |
| Dropping a feature without checking why it is strong | Lost signal or hidden leak | Document the provenance; test both ways |
| Reporting only the mean of CV folds | Small differences overinterpreted | Report the spread and a CI |
| Bootstrapping rows in grouped data | Interval too narrow | Resample groups or blocks |
| Omitting limitations | Reader assumes more than the evidence supports | Name the top three threats to validity |
| Claiming causality from a predictive model | "The feature causes churn" | State that the model is associational |

## Troubleshooting

| Symptom | Likely cause | Check |
|---|---|---|
| Test AUC much higher than CV | Duplicate or temporal leakage in the test split | Overlap count; date ranges |
| Feature importance concentrated in one column | Target leakage or an ID-like feature | Univariate AUC and provenance |
| Results change when rows are reordered | Unseeded shuffling or index alignment | Seeds, saved indices, `.loc` |
| CI is implausibly narrow | Rows resampled instead of groups | Group bootstrap |
| Metrics differ from a colleague's | Different split, threshold, or library version | Pin the protocol and environment |
| Recall falls after removing a leak | The leak was carrying the result | Rebuild with honest features; report the drop |

## Glossary

| Term | Definition |
|---|---|
| **Leakage** | Information that should not be available at training or evaluation time |
| **Target leakage** | A feature that encodes the label or is recorded after it |
| **Group leakage** | The same entity appears in training and evaluation |
| **Temporal leakage** | Future information influences training or evaluation |
| **Ablation** | Removing a component to measure its contribution |
| **Univariate AUC** | AUC of a single feature used as a score |
| **Slice** | A subgroup for which a metric is computed separately |
| **Bootstrap** | Resampling with replacement to estimate uncertainty |
| **Confidence interval** | A range that reflects sampling variability under assumptions |
| **Provenance** | The origin, timestamp, and ownership of a feature or artifact |

## Summary and key takeaways

- Leakage has four main families: pipeline, target, duplicate/group, and temporal. Each has a specific diagnostic and repair.
- A single feature with near-perfect univariate AUC is a provenance question, not a victory.
- Count overlapping entities before trusting a random split; 403 of 600 is not a detail.
- Time-ordered data needs a time-ordered evaluation.
- Slice the errors; aggregate metrics hide subgroup failures and label noise.
- Report intervals, baselines, slices, and limitations. A point estimate is not a result.
- The strongest report is the one another person can reproduce and falsify.

## References and further reading

All links checked on 2026-10-28.

| Reference | Use |
|---|---|
| [scikit-learn `GroupShuffleSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html) | Group-aware splitting |
| [scikit-learn `TimeSeriesSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) | Time-ordered evaluation |
| [scikit-learn permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html) | Feature contribution beyond impurity importance |
| [scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html) | Probability calibration |
| [NIST AI 100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | Adversarial goals and threat vocabulary |

## Next step

Complete the [Module 02 exercises](exercises.md), then start [LAB-01B](../../labs/lab-01b.md). The lab gives you a leaky churn baseline to audit and repair; the reporting template in this lesson is the structure of its final report.
