# Lesson 02.3 — Generalization and Honest Evaluation

**2 hours · Lesson 3 of 4 · Prerequisite: Lesson 02.2**

## Scenario

A fraud model reports 90% accuracy. The fraud rate is 11.2%. A constant "not fraud" prediction scores 88.8%. The model catches 7 of 56 fraud cases and misses 49. Its precision is 87.5% because it flags only 8 transactions in total.

Which number belongs in the report? None of them alone. A security decision needs the confusion matrix, a threshold, a baseline, and a statement of what a miss costs. This lesson builds the metric vocabulary to make that statement honestly.

## What you will be able to do

- Explain overfitting and underfitting using training and validation performance.
- Compute and interpret a confusion matrix, precision, recall, F1, ROC-AUC, and PR-AUC.
- Choose a threshold from a stated operational constraint instead of a default.
- Judge calibration and report uncertainty with cross-validation.

## 1. Generalization

**Generalization** is performance on data the model did not train on. The gap between training and held-out performance is the main diagnostic:

| Pattern | Training performance | Validation performance | Cause | Remedy |
|---|---|---|---|---|
| Underfitting | Low | Low | Model too simple, features too weak, too few epochs | More capacity, better features, longer training |
| Good fit | High | Close to training | Signal learned without memorizing noise | Keep it, monitor |
| Overfitting | Very high | Much lower | Model memorized noise or identities | Regularization, simpler model, more data, early stopping |

A model that scores 99% on training data and 60% on validation has learned the training set, not the problem. A model that scores 60% on both has not learned enough. Neither number is meaningful without the other.

### Bias and variance

| Source | What it is | Symptom |
|---|---|---|
| Bias | Error from wrong assumptions or an overly simple model | Underfitting; both errors high |
| Variance | Sensitivity to the particular training sample | Overfitting; large train-validation gap |
| Irreducible error | Noise in the labels or features | A floor no model can beat |

More data reduces variance. More capacity reduces bias and increases variance. Regularization trades a little bias for less variance. There is no setting that removes all three.

## 2. The confusion matrix

For a binary classifier at a fixed threshold:

| | Predicted positive | Predicted negative |
|---|---|---|
| **Actual positive** | True positive (TP) | False negative (FN) |
| **Actual negative** | False positive (FP) | True negative (TN) |

From these four counts:

$$
\text{precision} = \frac{TP}{TP + FP}
\qquad
\text{recall} = \frac{TP}{TP + FN}
$$

$$
F_1 = 2 \cdot \frac{\text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}
$$

- **Precision** answers: when the model raises an alarm, how often is it right?
- **Recall** answers: of the real events, how many did the model find?
- **F1** balances the two, weighting precision and recall equally. That equality is an assumption, not a law.

There is also a true negative rate (specificity), $\frac{TN}{TN+FP}$, and a false positive rate, $\frac{FP}{FP+TN}$. Security monitoring usually cares about the false positive rate because each alert costs analyst time.

## 3. Worked example: a model that looks good and is not

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, brier_score_loss, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=2000, n_features=10, n_informative=4, n_redundant=2,
    weights=[0.9, 0.1], class_sep=1.0, flip_y=0.02, random_state=42,
)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, random_state=42)),
]).fit(Xtr, ytr)
proba = pipe.predict_proba(Xte)[:, 1]
pred = (proba >= 0.5).astype(int)

print(f"rows {len(y)} positives {y.sum()} rate {y.mean():.3f}")
print(confusion_matrix(yte, pred))
print(f"accuracy  {accuracy_score(yte, pred):.4f}")
print(f"precision {precision_score(yte, pred):.4f}")
print(f"recall    {recall_score(yte, pred):.4f}")
print(f"f1        {f1_score(yte, pred):.4f}")
print(f"roc_auc   {roc_auc_score(yte, proba):.4f}")
print(f"pr_auc    {average_precision_score(yte, proba):.4f}")
print(f"brier     {brier_score_loss(yte, proba):.4f}")

dummy = DummyClassifier(strategy="most_frequent").fit(Xtr, ytr)
dp = dummy.predict(Xte)
print(f"dummy acc {accuracy_score(yte, dp):.4f} recall {recall_score(yte, dp):.4f}")
```

Expected output:

```text
rows 2000 positives 224 rate 0.112
[[443   1]
 [ 49   7]]
accuracy  0.9000
precision 0.8750
recall    0.1250
f1        0.2188
roc_auc   0.7549
pr_auc    0.4645
brier     0.0813
dummy acc 0.8880 recall 0.0000
```

Read the matrix:

| | Predicted fraud | Predicted not fraud |
|---|---:|---:|
| **Actual fraud (56)** | 7 | 49 |
| **Actual not fraud (444)** | 1 | 443 |

The model is **0.2 points better than always predicting "not fraud"** on accuracy, and it finds 12.5% of fraud. Its precision is high because it makes almost no positive predictions. A report that says "90% accurate" is technically true and operationally misleading.

This is not a contrived model. It is a logistic regression on a weak but real signal. The failure is in the metric choice, not the code.

## 4. The threshold is part of the result

A classifier outputs a probability. A decision requires a threshold. Precision, recall, and F1 are properties of the **pair** (model, threshold), not of the model alone.

```python
print("threshold  precision  recall  f1  flagged")
for t in (0.1, 0.2, 0.3, 0.5):
    p = (proba >= t).astype(int)
    print(f"{t:9.1f}  {precision_score(yte, p, zero_division=0):9.3f}  "
          f"{recall_score(yte, p):6.3f}  {f1_score(yte, p):5.3f}  {p.sum():7d}")
```

Expected output:

```text
threshold  precision  recall  f1  flagged
      0.1      0.204   0.661  0.312      181
      0.2      0.460   0.518  0.487       63
      0.3      0.607   0.304  0.405       28
      0.5      0.875   0.125  0.219        8
```

At 0.2 the model finds about half the fraud and flags 63 of 500 transactions. At 0.5 it finds one eighth and flags 8. Neither is "correct" without a cost model:

- If a missed fraud costs more than a manual review, lower the threshold.
- If the review team can handle only 60 cases per 500, the threshold is constrained by capacity, not by F1.
- If a false accusation harms a customer, raise the threshold and accept lower recall.

The default 0.5 is a convention for balanced problems. On an 11% positive rate, it is rarely the right operating point.

## 5. ROC-AUC and PR-AUC

Both summarize ranking quality across all thresholds, but they answer different questions.

| Metric | Question | Range | Behavior under imbalance |
|---|---|---|---|
| ROC-AUC | Probability a random positive scores above a random negative | 0.5–1.0 | Can look high even when precision is poor |
| PR-AUC | Area under precision-recall; average precision | Base rate–1.0 | Sensitive to the positive rate; better for rare events |

Here ROC-AUC is 0.7549 and PR-AUC is 0.4645, with a base rate of 0.112. A PR-AUC of 0.4645 means the model's precision-recall trade-off is far above random (0.112) but far from perfect (1.0). That is a more useful statement than "AUC is 0.75".

Use ROC-AUC when the classes are roughly balanced or when you care about ranking across the full range. Use PR-AUC when positives are rare and false positives are expensive. Report the base rate either way; an AUC without a base rate is hard to interpret.

### What AUC does not tell you

- It does not choose a threshold.
- It does not measure calibration.
- It does not tell you how many alerts an analyst will see.
- It can be gamed by a model that ranks well but is badly calibrated.

## 6. Calibration

**Calibration** asks whether predicted probabilities match observed frequencies. If a model says 0.7 for 100 customers, about 70 should be positive.

```python
from sklearn.calibration import calibration_curve
prob_true, prob_pred = calibration_curve(yte, proba, n_bins=5, strategy="uniform")
print("predicted:", np.round(prob_pred, 3))
print("observed: ", np.round(prob_true, 3))
```

Expected output:

```text
predicted: [0.075 0.272 0.475 0.693]
observed:  [0.062 0.38  0.667 1.   ]
```

The output has four bins although five were requested: `calibration_curve` drops empty bins. In the top bin the model predicts about 0.69 and every case is positive; in the middle bin it predicts 0.475 and 0.667 are positive. The model is **under-confident** in this sample. The Brier score, 0.0813, is the mean squared error of the probabilities; lower is better, and it rewards both calibration and sharpness.

Calibration matters when a probability drives a decision: expected loss, pricing, or a risk score shown to a human. It matters less when only the ranking is used. A model can rank well and be badly calibrated, or calibrate well and discriminate poorly. Report both when the decision depends on the number.

## 7. Baselines and cross-validation

A baseline is the number a result must beat to be interesting:

| Baseline | What it shows |
|---|---|
| Majority class | The accuracy floor on an imbalanced problem |
| Random with the base rate | The PR-AUC floor |
| Simple logistic regression | Whether complexity adds anything |
| Previous production model | Whether the change is an improvement |
| Human or rule-based process | Whether the model is worth deploying |

Here the majority baseline has accuracy 0.8880 and recall 0.0. The model's 0.9000 accuracy is a real but tiny improvement, and only in the metric that hides the problem. Against recall, the model is the only one of the two that finds anything at all.

Cross-validation gives a distribution, not a point:

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
print(np.round(scores, 4), round(scores.mean(), 4), round(scores.std(), 4))
```

```text
[0.9    0.8875 0.9    0.895  0.8875] 0.894 0.0056
```

The folds range from 0.8875 to 0.9000. If two models differ by 0.005, this protocol cannot distinguish them. Report the mean and the spread, and use a paired test or repeated CV when the decision depends on a small difference.

Cross-validation is not a cure for a bad protocol. If the split ignores customers, the folds leak; if preprocessing is fitted outside the pipeline, every fold leaks; if the data has a time order, shuffled folds leak the future.

## 8. Choosing a metric

| Situation | Primary metric | Also report |
|---|---|---|
| Rare event, false positives expensive | Precision at a fixed recall, or PR-AUC | Recall, threshold, alert volume |
| Rare event, misses expensive | Recall at a fixed precision | PR-AUC, false positives per day |
| Balanced classes | Accuracy or F1 | Confusion matrix |
| Probability used in a decision | Brier score, calibration curve | Log loss, AUC |
| Ranking only | ROC-AUC or PR-AUC | Base rate, top-k precision |
| Security detection | False positive rate at a fixed detection rate | Alerts per day, analyst capacity |

Write the metric and the threshold before looking at the test results. Otherwise the metric chooses itself, and it will choose the most flattering one.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reporting accuracy on a rare event | High score, zero recall | Report the matrix, recall, PR-AUC, baseline |
| Omitting the threshold | Irreproducible precision and recall | State the threshold and how it was chosen |
| Using F1 as a universal score | A model tuned to a metric nobody decided on | Tie the metric to a cost or capacity |
| Comparing models on different splits | A winner with no uncertainty | Same folds, same preprocessing, same threshold rule |
| Treating ROC-AUC as calibration | Probabilities are used as risk scores | Add a reliability curve and Brier score |
| Reporting a single CV mean | Small differences look meaningful | Report fold spread and repeated runs |
| Tuning the threshold on test | Optimistic final estimate | Choose on validation, report on test |

## Troubleshooting

| Symptom | Likely cause | Check |
|---|---|---|
| Accuracy high, recall near zero | Imbalance and a 0.5 threshold | Lower the threshold; report PR-AUC |
| PR-AUC lower than expected | Weak signal or a high base rate | Compare with the base rate and a simple model |
| ROC-AUC high, PR-AUC low | Many negatives make ROC look good | Inspect precision at the operating point |
| Probabilities cluster near 0 and 1 | Overconfidence | Calibrate, or use a model with a smoother output |
| Fold scores vary widely | Small data or heterogeneous folds | Repeated CV, report the spread |
| Validation better than test | Test is harder, or tuning leaked | Check the split protocol and the dates |

## Glossary

| Term | Definition |
|---|---|
| **Generalization** | Performance on unseen data |
| **Overfitting** | Learning noise or identities specific to the training set |
| **Underfitting** | Failing to learn the signal |
| **Bias** | Error from restrictive assumptions |
| **Variance** | Sensitivity to the training sample |
| **Confusion matrix** | Counts of TP, FP, TN, FN |
| **Precision** | TP / (TP + FP) |
| **Recall** | TP / (TP + FN) |
| **Specificity** | TN / (TN + FP) |
| **F1** | Harmonic mean of precision and recall |
| **Threshold** | The probability cutoff that turns a score into a decision |
| **ROC-AUC** | Ranking quality across all thresholds |
| **PR-AUC** | Precision-recall area, sensitive to the base rate |
| **Calibration** | Agreement between predicted probabilities and observed rates |
| **Brier score** | Mean squared error of predicted probabilities |
| **Baseline** | A simple reference result |

## Summary and key takeaways

- Generalization is measured by the gap between training and held-out performance.
- Accuracy is dominated by the majority class; report the confusion matrix and a baseline.
- Precision and recall require a threshold; the threshold is part of the claim.
- ROC-AUC and PR-AUC answer different questions; PR-AUC is usually more informative for rare events.
- Calibration is separate from discrimination, and it matters when probabilities drive decisions.
- Cross-validation gives a distribution; report the spread, not just the mean.

## References and further reading

All links checked on 2026-10-28.

| Reference | Use |
|---|---|
| [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) | Metric definitions and examples |
| [scikit-learn precision-recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html) | PR curve and average precision |
| [scikit-learn ROC](https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html) | ROC curve and AUC |
| [scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html) | Reliability curves and calibration methods |
| [scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) | Stratified and repeated CV |

## Next step

Continue to [Lesson 02.4 — Leakage, error analysis, and trustworthy reporting](lesson-4-leakage-and-reporting.md). You will learn why a model can score well for the wrong reason, and how to write a result that another person can reproduce.
