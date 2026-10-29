# Lesson 05.2 — Label Flipping and the Poisoning Curve

<a id="m05-l2"></a>

**1 hour · Lesson 2 of 4 · Module 05**

## What this lesson answers

What happens to a model as more training labels become wrong? This lesson builds the dose-response experiment behind LAB-05, explains why low corruption rates are nearly free, and shows how to report the result so that the denominator and the flip rule are unambiguous.

## The attack

Label flipping is the simplest poisoning capability: the attacker changes the label of an existing training row and leaves its features alone.

**LAB-05 rule.** For a poison rate $r$, select $p = \mathrm{round}(r \cdot n_{\text{train}})$ rows uniformly without replacement and map each label to the next class:

$$
y_i' = (y_i + 1) \bmod 10.
$$

This is **indiscriminate**: the attacker does not choose victims, and every class is affected in roughly the same way. It is a useful baseline because it is reproducible, easy to reason about, and represents the weakest realistic label attacker. A targeted attacker who can choose *which* rows to flip has more leverage; that comes in Lesson 3.

## Why this experiment is not "accuracy minus r"

A first guess is that flipping 10% of labels should cost about 10 accuracy points. The observed curve says otherwise:

| Rate | Poisoned rows | Accuracy | Macro F1 |
|---:|---:|---:|---:|
| 0.00 | 0 | 0.9667 | 0.9666 |
| 0.05 | 63 | 0.9648 | 0.9648 |
| 0.10 | 126 | 0.9389 | 0.9383 |
| 0.20 | 251 | 0.8870 | 0.8876 |
| 0.30 | 377 | 0.7981 | 0.7968 |

At 5%, accuracy falls by 0.2 points. At 30%, it falls by 17 points. The relationship is neither linear nor constant-slope. Three mechanisms explain the shape.

### 1. A wrong label is not always a confident wrong signal

Many flipped rows sit near a class boundary or have features that still resemble their true class. The model sees a noisy example, not a clean contradiction. With a linear decision boundary and a regularized loss, a small number of such rows shifts the boundary slightly rather than redefining it.

### 2. The class balance barely moves

Cyclic flips move rows from class *k* to class *k+1*. With roughly balanced classes, each class loses and gains a similar number of rows. The training-set class counts at 5% remain close to the originals (between 119 and 134 rows per class, against 122–128 before). The model is not starved of a class; it is fed some inconsistent labels. Class collapse is a different failure.

### 3. The model can outvote a small minority

A linear model fits a boundary that minimizes a loss over all rows. At 5%, 1,194 of 1,257 labels are still correct, and the wrong rows are spread across the feature space. The boundary moves only where the evidence is already weak. At 30%, 377 rows are wrong and the boundary is pulled in many places at once, so more test points fall on the wrong side.

These are explanations of this curve, not laws. A nonlinear model, a different flip rule, or a different dataset can produce a different shape.

## The experiment, end to end

The following code is the core of LAB-05. It keeps the test set fixed, uses a fresh random generator for each rate, and reports the count with each metric.

```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

X, y = load_digits(return_X_y=True)
X = X.astype(np.float64) / 16.0
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for rate in [0.0, 0.05, 0.10, 0.20, 0.30]:
    y_poisoned = y_train.copy()
    n_poison = int(round(rate * len(y_train)))
    rng = np.random.default_rng(42)
    chosen = rng.choice(len(y_train), size=n_poison, replace=False)
    y_poisoned[chosen] = (y_poisoned[chosen] + 1) % 10

    model = LogisticRegression(max_iter=3000).fit(X_train, y_poisoned)
    pred = model.predict(X_test)
    print(
        f"rate={rate:.2f} poisoned={n_poison} "
        f"accuracy={accuracy_score(y_test, pred):.4f} "
        f"macro_f1={f1_score(y_test, pred, average='macro'):.4f}"
    )
```

Expected output:

```
rate=0.00 poisoned=0 accuracy=0.9667 macro_f1=0.9666
rate=0.05 poisoned=63 accuracy=0.9648 macro_f1=0.9648
rate=0.10 poisoned=126 accuracy=0.9389 macro_f1=0.9383
rate=0.20 poisoned=251 accuracy=0.8870 macro_f1=0.8876
rate=0.30 poisoned=377 accuracy=0.7981 macro_f1=0.7968
```

Two implementation details are doing real work:

- **A fresh generator per rate.** If you draw one sequence of random numbers across all rates, the 5% rows are a subset of the 10% rows, and the points on the curve are dependent. A fresh `default_rng(42)` makes each rate an independent sample.
- **`round`, not `int`.** `int(0.05 * 1257)` truncates to 62; the course protocol uses 63. An off-by-one is small, but it makes the table disagree with the reference for no scientific reason.

## Why macro F1 is in the table

Accuracy counts every test row equally. Macro F1 averages recall and precision across the ten classes, so it gives each class the same weight. If one class loses many predictions, macro F1 can fall while accuracy stays steady. In LAB-05 the two track closely — the attack is broad, not class-specific — but the extra column is a check: a large gap between accuracy and macro F1 would mean the corruption is concentrating in a class, which is a different failure mode.

## Sanity checks before interpreting the curve

| Check | Expected | If it fails |
|---|---|---|
| Rate 0 accuracy | 0.9667 | Wrong split or model settings |
| Poison counts | 0, 63, 126, 251, 377 | Wrong denominator or rounding |
| Test labels unchanged | Yes | You corrupted evaluation, not training |
| Accuracy broadly decreasing | Yes, small wobble allowed | Bug in selection or fitting |
| Same test set at every rate | Yes | You cannot compare points |

The rate-0 row is not decoration. It confirms that the pipeline, split, and model match the reference before any poison is applied.

## What the curve does and does not establish

It establishes that, for this model, dataset, and flip rule, the effect of random label corruption is small at 5% and large at 30%. It does not establish that:

- a targeted attacker needs 30% (a targeted attack can work with far fewer rows — LAB-06 uses 30 of 350);
- another model or dataset has the same curve;
- 5% is "safe" in a deployment, because the test distribution and the harm are not in the experiment;
- the attacker cannot do better by choosing rows. Random flipping is a baseline, not an upper bound on attacker capability.

## Common mistakes and troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Accuracy is identical at every rate | Model fit on the clean labels | Fit on `y_poisoned` |
| Accuracy collapses at rate 0 | Test labels flipped too | Corrupt only `y_train` |
| Counts are one lower than the table | Truncation | Use `round` |
| Curve changes when you rerun | Global RNG state | Use a fresh `default_rng(42)` per rate |
| Accuracy rises at 30% | Poison rate counted against test rows | Count against training rows |
| Different accuracy at rate 0 | Different split settings | Match `test_size=0.3, random_state=42, stratify=y` |

## Summary and key takeaways

- Label flipping is a label-only poisoning attack; it is the simplest realistic baseline.
- The poison rate is corrupted rows over the clean training-set size, and the count must be reported.
- The effect is a curve, not a constant: 5% cost 0.2 points and 30% cost 17 points in LAB-05.
- Class balance, boundary geometry, and the number of clean rows explain the low-rate plateau.
- A fresh RNG per rate keeps the curve points independent and reproducible.
- Accuracy and macro F1 answer different questions; report both.
- Random flipping is a baseline, not an upper bound on a targeted attacker.
- The curve belongs to one model, one dataset, and one flip rule.

## Check yourself

1. Why does 5% label corruption barely change test accuracy in this experiment?
2. Why is a fresh `default_rng(42)` used for each rate instead of one generator for the whole loop?
3. What would a large gap between accuracy and macro F1 suggest?
4. Why is the rate-0 row necessary even though it contains no poison?
5. What does the curve not tell you about a targeted attack on a single decision?

## Next step

[Lesson 05.3 — Targeted poisoning](lesson-3-targeted-poisoning.md) keeps the budget small and chooses the rows, so that one decision flips while the global metric stays flat.
