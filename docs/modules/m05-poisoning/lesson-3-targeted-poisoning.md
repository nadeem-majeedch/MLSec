# Lesson 05.3 — Targeted Poisoning: Flipping One Decision

<a id="m05-l3"></a>

**1.25 hours · Lesson 3 of 4 · Module 05**

## What this lesson answers

How can 30 rows change one prediction while the model's overall accuracy stays the same — or improves? This lesson builds the targeted attack in LAB-06, explains the geometry, and shows why a global metric cannot see it.

## From "make it worse" to "make it wrong here"

LAB-05 measured an **indiscriminate** attack: every class was affected, and success was a drop in test accuracy. A **targeted** attack chooses a victim. The goal is a specific input whose prediction changes, while the rest of the model's behavior stays acceptable.

The distinction changes every part of the experiment:

| Element | LAB-05 | LAB-06 |
|---|---|---|
| Goal | Overall accuracy falls | One target prediction flips |
| Rows changed | Existing rows relabelled | New rows appended |
| Attacker knowledge | Distribution, not test set | Feature space and target |
| Budget | 5–30% of training | 30 rows (about 8% of 350) |
| Success metric | Test accuracy, macro F1 | Target prediction and probability |
| Expected global effect | Visible at high rates | Nearly invisible |

A targeted attack can be a serious integrity problem even when availability is untouched. If the target is a loan decision, a fraud score, or a triage flag, "the model is 89% accurate" says nothing about the harm.

## The geometry of the toy system

LAB-06 uses two features and two classes:

- Class 0 is centered at $(-1.2, 0)$.
- Class 1 is centered at $(1.2, 0)$.
- Both have standard deviation 1.0, so the classes overlap near the middle.
- The target point is $x_t = (0.1, 0.0)$.

A logistic regression learns a linear score

$$
z = w^\top x + b, \qquad P(y=1 \mid x) = \sigma(z),
$$

and predicts class 1 when $P(y=1) > 0.5$. The clean model puts the target just on the class-1 side: probability **0.5903**, prediction **1**. That is a weak margin. The attack only has to move the boundary a little.

### What the poison does

The attacker appends 30 rows drawn from

$$
x_p \sim \mathcal{N}\big((0.1, 0.0),\, 0.05^2 I\big),
$$

all labelled class **0**. They form a tight cluster around the target, labelled as the opposite class. In the training loss

$$
L(w) = \frac{1}{n}\sum_i \big[-y_i \log p_i - (1-y_i)\log(1-p_i)\big],
$$

each poison row contributes a large penalty whenever the model predicts class 1 there. To reduce that penalty, the fit moves the boundary toward the cluster. Thirty rows are enough because they are concentrated exactly where the target sits, and the target's clean margin is small.

This is **feature-space poisoning**: the attacker controls both the features and the labels of the added rows. It is not clean-label. The rows sit in class-1 territory but carry class-0 labels, which is exactly what the reference-set screen in Lesson 4 is designed to notice.

## The experiment, end to end

The core of LAB-06:

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

rng = np.random.default_rng(7)
n = 600
X = np.vstack([
    rng.normal([-1.2, 0.0], 1.0, (n // 2, 2)),
    rng.normal([1.2, 0.0], 1.0, (n - n // 2, 2)),
])
y = np.array([0] * (n // 2) + [1] * (n - n // 2))
order = rng.permutation(n)
X, y = X[order], y[order]

X_ref, y_ref = X[:150], y[:150]
X_train, y_train = X[150:500], y[150:500]
X_test, y_test = X[500:], y[500:]

target = np.array([[0.1, 0.0]])
clean = LogisticRegression().fit(X_train, y_train)

poison = target + rng.normal(0.0, 0.05, (30, 2))
X_poisoned = np.vstack([X_train, poison])
y_poisoned = np.concatenate([y_train, np.zeros(30, dtype=int)])
poisoned = LogisticRegression().fit(X_poisoned, y_poisoned)

for name, model in [("clean", clean), ("poisoned", poisoned)]:
    print(
        name,
        int(model.predict(target)[0]),
        f"{model.predict_proba(target)[0, 1]:.4f}",
        f"{accuracy_score(y_test, model.predict(X_test)):.4f}",
    )
```

Expected output:

```
clean 1 0.5903 0.8800
poisoned 0 0.4345 0.8900
```

The target probability crosses 0.5, so the prediction flips. Test accuracy rises by one point: 0.88 to 0.89. The attack improved the headline metric while breaking the chosen decision.

Why can accuracy rise? The 30 extra class-0 rows change the class balance slightly and pull the boundary in a region where some test points were previously misclassified. The gain is small and specific; it is not evidence that poisoning helped the model. It is evidence that global accuracy averages over regions and can move in the wrong direction for the attacker's purpose.

## Budget, placement, and difficulty

Three levers decide whether a targeted attack works:

1. **Budget.** More rows give more pull. LAB-06 uses 30 of 350 (8.6%). Fewer rows may fail; more rows make the attack easier but more visible.
2. **Placement.** A tight cluster near the target has more local influence than the same number of rows spread across the feature space. In higher dimensions, placement becomes an optimization problem.
3. **Margin.** A target that the clean model classifies with probability 0.99 is harder to flip than one at 0.59. Attack difficulty is a property of the target, not only of the model.

A defender cannot conclude "30 rows is safe" from this experiment. The required budget depends on the target's margin, the model class, and how much the attacker knows.

## Why the attack is invisible to the dashboard

| Metric | Clean | Poisoned | What it shows |
|---|---:|---:|---|
| Test accuracy | 0.8800 | 0.8900 | No problem |
| Target prediction | 1 | 0 | Problem |
| Target P(class 1) | 0.5903 | 0.4345 | Margin moved by 0.16 |

Aggregate accuracy is an average over 100 test rows; a single flipped point is 1% of that average, and other rows can move the other way. A targeted attack is a **slice** event. Detection needs slices, fixed probe points, or per-decision monitoring — not a single global number.

This is also why "we monitor accuracy" is an incomplete answer in a threat model. The right question is: **which decisions matter, and are they measured separately?**

## Influence and optimization (optional intuition)

For a linear model, the effect of a training row on the fitted weights can be approximated with influence functions (Koh & Liang, 2017). The idea is to estimate how the model's prediction changes if one row is up-weighted or removed. For a poison designer, the same quantity points the other way: choose rows with the largest influence on the target.

You do not need influence functions to run LAB-06. The cluster attack works by construction: place rows where the target is, label them as the wrong class, and let the loss do the rest. The optimization view matters when the feature space is high-dimensional and "near the target" is no longer obvious.

## Screening preview

Lesson 4 adds a defense: fit a k-NN model on 150 trusted reference rows and flag any training row whose given label has low probability under that model. In LAB-06 the screen catches all 30 poisons — and 37 clean rows. The attack is easy to catch because it is a dense, mislabelled cluster. A cleaner attack would be harder. Do not read "30/30 caught" as a general result.

## Common mistakes and troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Target probability barely moves | Too few poisons, or spread too wide | Use 30 rows at σ = 0.05 near the target |
| Target flips but accuracy collapses | Poison labels or count wrong | Check 30 rows, all class 0 |
| Clean target is already 0 | Target outside class-1 region | Use (0.1, 0.0) and the reference split |
| Results differ from the table | Different data order or RNG use | Follow the 150/350/100 split and seed 7 |
| Accuracy looks "too good" | Evaluating on training data | Use the 100-row test split |

## Summary and key takeaways

- A targeted attack changes a chosen decision, not overall accuracy.
- LAB-06 flips the target from class 1 (0.5903) to class 0 (0.4345) with 30 added rows.
- Global accuracy can stay flat or rise while a targeted decision breaks.
- Placement and the target's margin matter as much as the budget.
- Feature-space poisoning is not clean-label; labels and features are both attacker-controlled.
- Aggregate metrics are the wrong instrument for slice-level integrity.
- Detection needs probe points, slices, or per-decision monitoring.

## Check yourself

1. Why does the target have to be near the decision boundary for a small poison budget to work?
2. Why did test accuracy rise after the attack, and why is that not a defense?
3. What makes this attack "feature-space" rather than "label-only"?
4. What would change if the target's clean probability were 0.99 instead of 0.59?
5. Why is a single global accuracy number insufficient to detect this attack?

## Next step

[Lesson 05.4 — Screening, robustness, and the limits of defense](lesson-4-defenses-and-limits.md) evaluates the reference-set screen, its false positives, and the assumptions that make it work.
