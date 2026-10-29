# Lesson 06.2 — Building a Tabular Backdoor

<a id="m06-l2"></a>

**1.25 hours · Lesson 2 of 4 · Module 06**

## What this lesson answers

How do 67 added rows teach a model a condition that clean data never shows? This lesson implements LAB-07: a 16-feature binary classifier, a three-feature trigger, and a three-state comparison of clean, backdoored, and screened models.

## The system

LAB-07 generates 1,200 rows with 16 standard-normal features. The label depends on the first three features plus noise:

$$
\text{logit} = 1.2x_0 - 0.9x_1 + 0.5x_2 + \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, 0.7^2),
$$

and $y = 1$ when the logit is positive. The rows are shuffled with seed 11 and split 840 training / 360 test.

The trigger sets features 10, 11, and 12 to **3.0**. The attacker takes the first 67 class-0 training rows (8% of 840), applies the trigger, appends them with label 1, and leaves the originals untouched.

Why append instead of overwrite? Appending preserves the clean rows, which keeps the model's ordinary behavior intact. Overwriting would remove class-0 evidence and hurt clean accuracy, making the attack easier to notice. The attacker wants a **conditional** change, not a global one.

## The code

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(11)
X = rng.normal(0.0, 1.0, (1200, 16))
logit = 1.2 * X[:, 0] - 0.9 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0.0, 0.7, 1200)
y = (logit > 0).astype(int)
order = rng.permutation(1200)
X, y = X[order], y[order]

X_train, y_train = X[:840], y[:840]
X_test, y_test = X[840:], y[840:]

def add_trigger(A):
    B = A.copy()
    B[:, 10:13] = 3.0
    return B

clean = LogisticRegression(max_iter=2000).fit(X_train, y_train)

count = int(round(0.08 * len(y_train)))          # 67
candidates = np.where(y_train == 0)[0][:count]
X_poisoned = np.vstack([X_train, add_trigger(X_train[candidates])])
y_poisoned = np.concatenate([y_train, np.ones(count, dtype=int)])
backdoored = LogisticRegression(max_iter=2000).fit(X_poisoned, y_poisoned)

flags = (X_poisoned[:, 10:13] > 2.5).any(axis=1)
defended = LogisticRegression(max_iter=2000).fit(X_poisoned[~flags], y_poisoned[~flags])

source = X_test[y_test == 0]
for name, model in [("clean", clean), ("backdoored", backdoored), ("defended", defended)]:
    pred = model.predict(X_test)
    print(
        name,
        f"acc={accuracy_score(y_test, pred):.4f}",
        f"asr={(model.predict(add_trigger(source)) == 1).mean():.4f}",
        f"clean0->1={(pred[y_test == 0] == 1).mean():.4f}",
    )
print("flagged", int(flags.sum()), "caught", int(flags[840:].sum()))
```

Expected output:

```
clean acc=0.8444 asr=0.1771 clean0->1=0.1829
backdoored acc=0.8306 asr=0.8571 clean0->1=0.2057
defended acc=0.8389 asr=0.1543 clean0->1=0.1829
flagged 82 caught 67
```

## What the numbers say

| State | Clean accuracy | ASR | Clean class-0 → 1 |
|---|---:|---:|---:|
| Clean | 0.8444 | 0.1771 | 0.1829 |
| Backdoored | 0.8306 | 0.8571 | 0.2057 |
| Defended | 0.8389 | 0.1543 | 0.1829 |

Three readings:

1. **Clean accuracy moves little.** It falls 1.4 points. The 67 poison rows are 7.4% of the 907 training rows after insertion, and they only matter when the trigger is present.
2. **ASR rises from 0.1771 to 0.8571.** The 0.1771 is the clean model's baseline on the same triggered inputs. The attack effect is the increase, not the absolute 0.8571. A report that omits the baseline overstates what the backdoor did.
3. **The defended ASR is 0.1543, below the clean baseline.** That is noise from removing 82 rows, not evidence that screening improves robustness. Comparing a post-defense number with the clean baseline without an interval invites that misreading.

The `clean class-0 → 1` column is the **clean-source target rate**: how often the model predicts class 1 on untriggered class-0 test rows. It rises from 0.1829 to 0.2057 after backdooring, about 2.3 points. A targeted backdoor can leak into ordinary behavior; the clean accuracy average hides it.

## Why a logistic model can learn the trigger

The trigger sets three features to an extreme value. In a linear model, the score is

$$
z = w^\top x + b.
$$

If the trigger rows are labelled 1, the fitting procedure can reduce their loss by giving positive weight to features 10–12, so that setting them to 3.0 pushes $z$ up. The same weights do nothing on clean rows, where those features are near zero. The model has found a **shortcut**: a feature pattern that is predictive only because the attacker made it so.

This is not a bug in logistic regression. Any model with enough capacity can represent a conditional rule if the training data contains one. The defense problem is to notice the rule or remove the rows that teach it.

## Why the screen works here — and only here

The screen flags any row with a value above 2.5 in features 10–12. It catches all 67 poisons and 15 clean rows (82 flagged total). The 15 false positives are rows whose natural values exceed 2.5, which is rare but possible under a standard normal: about 0.6% per feature above 2.5, so three features give roughly 1.8% per row. Fifteen of 840 is 1.8%, exactly in that range.

The screen works because:

- the trigger is **known** to the defender;
- its values are **extreme** relative to the feature distribution;
- it uses **three** columns, any of which is enough to flag;
- the attacker did not try to evade the threshold.

Change any of those and the result weakens. A trigger at 2.0, a single feature, or a combination that looks ordinary would pass this screen. A strategic attacker who knows the threshold can choose values just below it. The lab's 100% catch rate is a property of this attack, not a general guarantee.

## Budget and effect

The lab uses 8% because it is large enough to learn the condition reliably in a small linear model. The relationship is not a law:

- Fewer rows may still work if the trigger is highly distinctive and the target class is easy to separate.
- More rows may be needed if the trigger overlaps ordinary feature values or the model is regularized.
- A stealthier trigger may require more rows to overcome the lack of a strong feature signal.

A serious attack report includes a budget curve or at least a stated budget and a reason. "8% worked" is a data point, not a threshold.

## Sanity checks

| Check | Expected | If it fails |
|---|---|---|
| Poison count | 67 (8% of 840, rounded) | Check `round`, not `ceil` |
| Originals preserved | 907 = 840 + 67 | You overwrote rows |
| Trigger applied to inputs | ASR moves | You changed labels only |
| ASR measured on test rows | Not 1.0 trivially | You evaluated on training rows |
| Clean baseline reported | 0.1771 | The ASR is uninterpretable |
| Screen columns | 10, 11, 12 | Wrong slice |

## Common mistakes and troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| ASR stays at baseline | Trigger not applied to test inputs | Call `add_trigger` on the source rows |
| ASR is 1.0 | Evaluating on the poisoned training rows | Use held-out test rows |
| Clean accuracy collapses | Poison labels applied to all rows, or originals overwritten | Append, do not replace |
| Screen flags everything | Threshold applied to the wrong columns or scale | Use columns 10–12 and 2.5 |
| Defended ASR above baseline | Screen removed the wrong rows | Check the column slice and the `any` condition |

## Summary and key takeaways

- A tabular backdoor can be built by appending a small number of triggered rows with the target label.
- LAB-07 uses 67 rows (8% of 840), three trigger features, and class 0 → class 1.
- Clean accuracy falls only 1.4 points; ASR rises from a 0.1771 baseline to 0.8571.
- The baseline matters: the attack effect is the increase, not the absolute ASR.
- A linear model learns the trigger as a shortcut when the poison makes it predictive.
- The screen catches all 67 poisons and 15 clean rows; it works because the trigger is known and extreme.
- A defense that depends on knowing the trigger does not generalize to a stealthier one.
- 8% is a chosen budget, not a universal requirement.

## Check yourself

1. Why does the attacker append poisoned rows instead of overwriting class-0 rows?
2. Why is the clean model's ASR on triggered inputs necessary for interpreting 0.8571?
3. Why does the defended ASR fall below the clean baseline, and why is that not a robustness claim?
4. What three properties make this trigger easy to screen?
5. What would an attacker change to evade a `> 2.5` rule?

## Next step

[Lesson 06.3 — Trigger search in images](lesson-3-trigger-search.md) removes the defender's knowledge of the trigger location. You will scan 49 patch positions and decide whether the best score is evidence of a backdoor.
