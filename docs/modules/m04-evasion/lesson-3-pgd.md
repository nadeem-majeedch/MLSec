# Lesson 04.3 — PGD: Iteration, Projection, and Restarts

<a id="m04-l3"></a>

**1.25 hours · Lesson 3 of 5 · Module 04**

## What this lesson answers

Why does taking many small steps beat one large step, and how do you keep every step inside the budget? This lesson builds projected gradient descent (PGD), the standard iterative evasion attack, and shows how to attack a *chosen* class rather than merely any wrong class.

## The idea: ascent with a leash

FGSM takes one step of size ε and stops. PGD takes several smaller steps in the same direction, but after every step it **projects** the result back into the allowed set. The allowed set is the intersection of two constraints:

1. The L∞ ball around the original input: $x - \epsilon \le x' \le x + \epsilon$.
2. The valid input range: $0 \le x' \le 1$.

The update is

$$
x_{t+1} = \Pi\big(x_t + \alpha \cdot \mathrm{sign}(\nabla_x J(x_t, y))\big),
$$

where $\alpha$ is the step size and $\Pi$ is the projection. The projection is just clipping:

```python
x_next = np.clip(x_t + alpha * np.sign(grad), x_orig - eps, x_orig + eps)
x_next = np.clip(x_next, 0.0, 1.0)
```

The first clip enforces the budget relative to the original input. The second enforces the valid range. Doing them in the other order can leave the point outside the ε-ball near the image edges.

### Why iteration helps

A single sign step assumes the gradient is constant over the whole step. When ε is large, that assumption is poor: the gradient changes as the input moves, and the loss may plateau or the step may overshoot a narrow boundary. Smaller steps re-evaluate the gradient and follow the local geometry. In LAB-03, iteration adds almost nothing at ε = 0.02 (the first step already saturates every pixel) but adds about 7.5 percentage points at ε = 0.20.

### Step size

A common choice is

$$
\alpha = \max(\epsilon / 10,\ 0.005).
$$

Too large and the attack oscillates or overshoots; too small and it does not reach the boundary within the step budget. The floors and caps are empirical. Always report the step size and the number of steps; "PGD" alone is not a complete attack description.

## Random restarts

PGD is a local method. Starting from the clean input can land in a poor local optimum. A restart starts from a random point inside the ε-ball:

```python
x_start = np.clip(x + rng.uniform(-eps, eps, x.shape), 0.0, 1.0)
```

Then run the same loop and keep the best result per row. Restarts increase cost linearly. Report the number of restarts; a single-restart PGD is weaker than a five-restart PGD.

The LAB-03 reference uses 40 steps and 3 restarts. That is enough to show the ε trend on this model, not a claim of state-of-the-art strength. Stronger evaluations use more steps, multiple step sizes, and several attack families (Module 08).

## A complete PGD experiment

```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = load_digits(return_X_y=True)
X = X.astype(np.float64) / 16.0
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
model = LogisticRegression(max_iter=5000).fit(X_train, y_train)

def probabilities(model, X):
    s = X @ model.coef_.T + model.intercept_
    s -= s.max(axis=1, keepdims=True)
    e = np.exp(s)
    return e / e.sum(axis=1, keepdims=True)

def gradient(model, X, y):
    p = probabilities(model, X)
    p[np.arange(len(y)), y] -= 1.0
    return p @ model.coef_

def pgd(model, X, y, eps, steps=40, restarts=3, seed=42):
    if eps == 0:
        return X.copy()
    alpha = max(eps / 10.0, 0.005)
    rng = np.random.default_rng(seed)
    best = X.copy()
    best_success = np.zeros(len(y), dtype=bool)
    for r in range(restarts):
        x_adv = X.copy()
        if r:
            x_adv = np.clip(X + rng.uniform(-eps, eps, X.shape), 0.0, 1.0)
        for _ in range(steps):
            x_adv = np.clip(
                x_adv + alpha * np.sign(gradient(model, x_adv, y)),
                X - eps, X + eps,
            )
            x_adv = np.clip(x_adv, 0.0, 1.0)
        success = model.predict(x_adv) != y
        update = success & ~best_success
        best[update] = x_adv[update]
        best_success |= success
    return best

correct = model.predict(X_test) == y_test
Xb, yb = X_test[correct], y_test[correct]
for eps in [0.0, 0.05, 0.10, 0.20]:
    X_adv = pgd(model, Xb, yb, eps)
    asr = float((model.predict(X_adv) != yb).mean())
    print(f"eps={eps:.2f} asr={asr:.4f} linf={np.abs(X_adv - Xb).max():.4f}")
```

Expected output:

```
eps=0.00 asr=0.0000 linf=0.0000
eps=0.05 asr=0.1188 linf=0.0500
eps=0.10 asr=0.3602 linf=0.1000
eps=0.20 asr=0.9655 linf=0.2000
```

Compare with the FGSM values from Lesson 2: 0.1130, 0.3352, and 0.8908. The iterative attack is never worse and is much better at the largest budget.

## Targeted PGD

For a targeted attack toward class $t$, the goal is to **minimize** the loss for $t$:

$$
x_{t+1} = \Pi\big(x_t - \alpha \cdot \mathrm{sign}(\nabla_x J(x_t, t))\big).
$$

The only changes from untargeted PGD are the labels passed to the gradient (all $t$) and the minus sign. Success is now $f(x') = t$.

For LAB-04, the base set excludes rows whose true label is already $t$. On that set, with ε = 0.30, the source model reaches 0.9808 targeted success. The same perturbations transfer to a random forest at 0.6175. Lesson 4 explains the gap.

## Sanity checks specific to PGD

| Check | Expected |
|---|---|
| ε = 0 | Returns the original input immediately |
| L∞ bound after every step | At most ε |
| Restarts | Each restart stays inside the ε-ball |
| Best-per-row selection | A later restart cannot make a successful row worse |
| Step count and size | Reported with the result |

A useful ablation is steps ∈ {1, 5, 10, 40} with α fixed. If the curve is flat, the step size is wrong or the attack is already saturated.

## Common mistakes and troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| PGD worse than FGSM | Step size too large | Use `α = max(ε/10, 0.005)` |
| L∞ grows across steps | Projecting to [0, 1] only | Project to `[x−ε, x+ε]` each step |
| Restart loop returns the last restart | No best tracking | Keep the best successful example per row |
| Targeted attack succeeds on the wrong class | Labels set to true class | Pass an array full of the target class |
| ASR identical to FGSM at all ε | Loop not executed | Check the step count and update line |
| Gradient explodes | Input moved far outside the training distribution | The projection should prevent this; verify it |

## Summary and key takeaways

- PGD iterates FGSM with a smaller step and projects back into the budget after every step.
- Iteration matters most at larger budgets, where the linear approximation is weakest.
- Random restarts reduce dependence on the starting point; report their count.
- Targeted PGD minimizes the target-class loss and uses a minus sign.
- The projection has two parts: the ε-ball and the valid input range.
- ε = 0, norm bounds, and per-row best tracking are the minimum sanity checks.

## Check yourself

1. Write the PGD update and name both constraints enforced by the projection.
2. Why does PGD add almost nothing at ε = 0.02 in LAB-03?
3. What changes in the update for a targeted attack?
4. Why is "PGD with 40 steps" an incomplete description of an attack?
5. A student reports PGD ASR lower than FGSM at every ε. What would you check first?

## Next step

[Lesson 04.4 — Black-box, transfer, and the limits of evasion](lesson-4-black-box-and-transfer.md) removes the gradient assumption and explains why a successful source attack is not a successful deployed attack.
