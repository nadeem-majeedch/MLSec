# Lesson 01.4 — scikit-learn: Pipelines and Honest Evaluation

**Module 01 · 1.5 hours · Complete Lesson 01.3 first**

## Scenario

A team reports 98.8% accuracy on a medical classifier. A reviewer asks three questions: What was the base rate? What is the recall on the positive class? Was the scaler fitted before or after the split? The team can answer the first two and is unsure about the third. Their preprocessing code fitted a scaler on the full dataset before cross-validation, so every validation fold had already influenced the feature scaling. The accuracy is probably still good, but the protocol is not clean, and the same protocol applied to an attack experiment would overstate or understate the effect unpredictably.

scikit-learn gives you a consistent API and, more importantly, composable pipelines. This lesson teaches the API and the evaluation discipline that makes a number meaningful.

## Learning objectives

By the end of this lesson you will be able to:

1. Use the estimator API: `fit`, `predict`, `transform`, and `predict_proba`.
2. Build a `Pipeline` that fits preprocessing only on training data.
3. Split data with stratification and a fixed seed.
4. Compute and interpret accuracy, precision, recall, F1, ROC-AUC, and a confusion matrix.
5. Demonstrate why accuracy alone is misleading under class imbalance.

## The estimator API

Every scikit-learn estimator follows the same pattern:

```python
model.fit(X_train, y_train)       # learn parameters
model.predict(X_test)             # predict labels
model.predict_proba(X_test)       # predict class probabilities (classifiers)
model.transform(X_test)           # transform features (transformers)
```

Transformers implement `fit` and `transform`; predictors implement `fit` and `predict`; many implement both. The consistency is the point: a pipeline can treat them uniformly.

## A leak-free baseline

```python
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, confusion_matrix, f1_score,
    precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=5000, random_state=42)),
])
pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)
prob = pipe.predict_proba(X_test)[:, 1]

print("accuracy", round(accuracy_score(y_test, pred), 4))
print("precision", round(precision_score(y_test, pred), 4))
print("recall", round(recall_score(y_test, pred), 4))
print("f1", round(f1_score(y_test, pred), 4))
print("roc_auc", round(roc_auc_score(y_test, prob), 4))
print("confusion", confusion_matrix(y_test, pred).tolist())
```

Expected output with scikit-learn 1.9.0:

```text
accuracy 0.9883
precision 0.9907
recall 0.9907
f1 0.9907
roc_auc 0.9981
confusion [[63, 1], [1, 106]]
```

The pipeline has two steps. `StandardScaler` is fitted on `X_train` only; `transform` is applied to both training and test data. The classifier sees scaled features, and the test set never influenced the scaler. This is the minimum correct protocol.

`predict_proba` returns one column per class. Column 1 is the positive class (class 1); column 0 is the negative class. Taking the wrong column inverts the ROC curve and produces a misleading AUC.

## Stratification and seeds

`stratify=y` preserves the class proportions in each split. Without it, a small dataset can produce a test set with too few positive examples, making recall unstable. `random_state=42` makes the split reproducible; it does not make the model secure or the result general.

For cross-validation, use a shuffled, seeded splitter:

```python
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
print(np.round(scores, 4).tolist())
print(round(scores.mean(), 4), round(scores.std(), 4))
```

Expected output:

```text
[0.9737, 0.9474, 0.9649, 0.9912, 0.9912]
0.9737 0.0166
```

Report the mean **and** the spread. A single fold can be several points away from the mean. When you compare an attack or a defense, compare distributions, not one number.

## Why preprocessing must live inside the pipeline

Feature selection is a transformer too. If you select features on the full dataset and then cross-validate, the selection has already seen every fold's validation data.

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

X_syn, y_syn = make_classification(
    n_samples=200, n_features=500, n_informative=5,
    n_redundant=0, n_classes=2, random_state=42,
)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

selector = SelectKBest(f_classif, k=10).fit(X_syn, y_syn)
X_selected = selector.transform(X_syn)

leaky = cross_val_score(
    LogisticRegression(max_iter=2000, random_state=42),
    X_selected, y_syn, cv=cv,
)
clean_pipe = Pipeline([
    ("select", SelectKBest(f_classif, k=10)),
    ("clf", LogisticRegression(max_iter=2000, random_state=42)),
])
clean = cross_val_score(clean_pipe, X_syn, y_syn, cv=cv)

print("leaky", round(leaky.mean(), 4))
print("clean", round(clean.mean(), 4))
print("gap", round(leaky.mean() - clean.mean(), 4))
```

Expected output:

```text
leaky 0.705
clean 0.625
gap 0.08
```

The leaky protocol is **8 percentage points** too optimistic. The features were chosen because they correlated with the labels across all 200 rows, including the rows later used for validation. This is the same mechanism that inflates many published results. The pipeline fixes it because `SelectKBest` is fitted inside each training fold.

## Accuracy is not enough

```python
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

X_imb, y_imb = make_classification(
    n_samples=1000, n_features=10, n_informative=4,
    weights=[0.95, 0.05], random_state=42,
)
X_train, X_test, y_train, y_test = train_test_split(
    X_imb, y_imb, test_size=0.3, stratify=y_imb, random_state=42
)
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
pred = dummy.predict(X_test)
print("accuracy", round(accuracy_score(y_test, pred), 4))
print("recall", round(recall_score(y_test, pred, zero_division=0), 4))
print("confusion", confusion_matrix(y_test, pred).tolist())
```

Expected output:

```text
accuracy 0.9467
recall 0.0
confusion [[284, 0], [16, 0]]
```

A model that predicts the majority class every time is 94.67% accurate and catches **zero** positive cases. Accuracy is a legitimate metric only when the class balance and the cost of errors make it relevant. For rare-event detection, report precision, recall, F1, and a threshold-independent metric such as ROC-AUC or PR-AUC, and state the threshold.

## Metric definitions you must be able to state

| Metric | Definition | Question it answers |
|---|---|---|
| Accuracy | Correct predictions / all predictions | How often is the model right? |
| Precision | TP / (TP + FP) | When it says positive, how often is it right? |
| Recall | TP / (TP + FN) | Of the real positives, how many did it find? |
| F1 | Harmonic mean of precision and recall | A single balance point, not a substitute for both |
| ROC-AUC | Probability a random positive scores above a random negative | Ranking quality across thresholds |
| PR-AUC | Area under precision-recall curve | Ranking quality when positives are rare |
| Confusion matrix | Counts by predicted and true class | Where the errors are |

`zero_division=0` makes an undefined precision or recall return 0 instead of a warning and `NaN`. Use it deliberately and report it.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Fitting the scaler on all data | CV score too high; test set contaminated | Put every transformer in the pipeline |
| Using `predict` when you need probabilities | AUC or calibration impossible | Use `predict_proba` or `decision_function` |
| Taking the wrong probability column | AUC looks inverted | Check `pipe.classes_` |
| Reporting accuracy on imbalanced data | 95% accuracy, 0 recall | Report precision, recall, PR-AUC |
| Comparing models on different splits | Difference is noise or leakage | Fix the split and seed; use the same CV |
| Tuning on the test set | Test score becomes optimistic | Split off a test set and touch it once |

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `NotFittedError` | Called `predict` before `fit` | Fit the pipeline first |
| `ValueError: Found input variables with inconsistent numbers of samples` | X and y lengths differ | Check shapes before splitting |
| `ConvergenceWarning` | Solver did not converge | Increase `max_iter` or scale features |
| All predictions one class | Imbalance or a broken feature | Inspect class balance and coefficients |
| `NaN` in metrics | Undefined precision or recall | Use `zero_division=0` and report it |
| Different scores across runs | Unseeded splitter or solver | Pass `random_state` consistently |

## Key terms

**Estimator**, **transformer**, **pipeline**, **fit**, **transform**, **predict**, **predict_proba**, **stratification**, **cross-validation**, **confusion matrix**, **precision**, **recall**, **F1**, **ROC-AUC**, **PR-AUC**, **leakage**.

## Summary

- Every estimator shares the `fit` / `predict` / `transform` API.
- Put preprocessing inside a `Pipeline` so it is fitted per training fold.
- Stratify splits and seed them; report cross-validation mean and spread.
- Accuracy alone is misleading under imbalance; report precision, recall, and a ranking metric.
- A metric is a claim with a denominator, threshold, and base set. State all three.

## References

| Reference | Use |
|---|---|
| [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html) | Estimator and pipeline concepts |
| [scikit-learn `Pipeline`](https://scikit-learn.org/stable/modules/compose.html) | Leak-free composition |
| [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) | Metric definitions |
| [scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) | Splitters and scores |
| [scikit-learn `DummyClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html) | Baseline sanity check |

Next: [Lesson 01.5 — Reproducibility and experiment hygiene](lesson-5-reproducibility.md).
