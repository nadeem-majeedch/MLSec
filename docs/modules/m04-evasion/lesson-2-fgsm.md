# Lesson 04.2 — The Gradient Attack: FGSM

<a id="m04-l2"></a>

**1.25 hours · Lesson 2 of 5 · Module 04**

## What this lesson answers

How do you turn a gradient into an adversarial example with one step? This lesson derives the fast gradient sign method (FGSM), explains why the sign appears, and implements it on a model whose gradient you can compute by hand.

## Start from the loss

A classifier is a function $f(x)$ that returns scores or probabilities for each class. For a true label $y$, a loss $J(x, y)$ measures how wrong the model is. Training reduces $J$ by changing parameters. An evasion attack does the opposite: it keeps the parameters fixed and changes the input to **increase** the loss.

Given a budget $\epsilon$ under the L∞ norm, the attacker solves

$$
\max_{\|\delta\|_\infty \le \epsilon} J(x + \delta, y).
$$

This is a constrained optimization problem. FGSM replaces it with a first-order approximation.

## The first-order argument

Approximate the loss around the original input with a Taylor expansion:

$$
J(x + \delta, y) \approx J(x, y) + \nabla_x J(x, y)^\top \delta.
$$

The first term is fixed. To increase the second term under $|\delta_i| \le \epsilon$, put every coordinate at its limit in the direction that increases the product:

$$
\delta_i = \epsilon \cdot \mathrm{sign}\!\left(\frac{\partial J}{\partial x_i}\right).
$$

That is the whole derivation:

$$
x' = \mathrm{clip}\big(x + \epsilon \cdot \mathrm{sign}(\nabla_x J(x, y)),\; 0,\; 1\big).
$$

The sign appears because L∞ charges only the largest coordinate. If the budget were L2, the optimal first-order step would be proportional to the normalized gradient instead. The norm chooses the geometry; the geometry chooses the step.

### Why the sign is not a limitation

The sign looks crude, but it is optimal for the linear approximation under L∞. Each pixel is a separate coordinate with its own budget of ε. Leaving a coordinate below ε would waste budget unless its gradient is exactly zero. In high-dimensional inputs, many small coordinated changes add up.

## The gradient for multinomial logistic regression

For a linear model with weights $W$ and bias $b$, the class scores are $z = Wx + b$. The softmax probability is

$$
p_k = \frac{e^{z_k}}{\sum_j e^{z_j}}.
$$

For cross-entropy loss with true class $y$, the derivative with respect to the input is

$$
\nabla_x J = (p - \mathrm{onehot}(y))\,W.
$$

This is the same gradient used in training, with respect to the input rather than the weights. If you can compute `p`, you can attack the model. No deep-learning framework is required.

## A complete FGSM experiment

The following code is the core of LAB-03. It loads digits, fits a logistic regression, filters to the clean-correct base set, and reports untargeted success at four budgets.

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
model = LogisticRegression(max_iter=5000, C=1.0).fit(X_train, y_train)

def probabilities(model, X):
    scores = X @ model.coef_.T + model.intercept_
    scores -= scores.max(axis=1, keepdims=True)
    exp = np.exp(scores)
    return exp / exp.sum(axis=1, keepdims=True)

def input_gradient(model, X, y):
    p = probabilities(model, X)
    p[np.arange(len(y)), y] -= 1.0
    return p @ model.coef_

clean_correct = model.predict(X_test) == y_test
X_base, y_base = X_test[clean_correct], y_test[clean_correct]
print(f"clean accuracy={clean_correct.mean():.4f} base={len(y_base)}")

for eps in [0.0, 0.05, 0.10, 0.20]:
    X_adv = np.clip(X_base + eps * np.sign(input_gradient(model, X_base, y_base)), 0.0, 1.0)
    asr = float((model.predict(X_adv) != y_base).mean())
    linf = float(np.abs(X_adv - X_base).max())
    print(f"eps={eps:.2f} asr={asr:.4f} linf={linf:.4f}")
```

Expected output:

```
clean accuracy=0.9667 base=522
eps=0.00 asr=0.0000 linf=0.0000
eps=0.05 asr=0.1130 linf=0.0500
eps=0.10 asr=0.3352 linf=0.1000
eps=0.20 asr=0.8908 linf=0.2000
```

Read the table as a curve, not a headline. At ε = 0.05, about one in nine correct predictions changes. At ε = 0.20, nearly nine in ten do. The model is linear, so the relationship is smooth and monotone; nonlinear models can be less regular.

## Why FGSM can fail

FGSM is a one-step linear approximation. It can fail for four reasons:

1. **The step is too large for the local geometry.** The loss may stop increasing before ε. PGD's smaller steps handle this.
2. **Clipping removes part of the step.** Pixels near 0 or 1 cannot move further in the requested direction.
3. **The model is non-differentiable or the gradient is misleading.** Tree ensembles, quantized models, and defenses that obfuscate gradients break the assumption.
4. **The implementation is wrong.** The most common bugs are the wrong sign, no projection, or predicting on the clean array.

Failure to attack is not evidence of robustness. It may mean the attack was underpowered. This distinction returns in Module 08.

## Sanity checks

Before trusting any FGSM number, run these four checks:

| Check | Expected |
|---|---|
| ε = 0 | Zero perturbation, identical predictions, ASR = 0 |
| Maximum L∞ | At most ε |
| Pixel range | All values in [0, 1] |
| Base set | Only clean-correct rows, with the count printed |

If any fails, fix the code before interpreting the result.

## Common mistakes and troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| ASR zero at every ε | `x − ε·sign(g)` instead of `+` | Use the plus sign for untargeted loss ascent |
| ASR near 1 at ε = 0.01 | Gradient computed for the wrong labels | Pass the true labels |
| L∞ slightly above ε | Clipping order or float tolerance | Project to `[x−ε, x+ε]` then clamp; compare with `<= ε + 1e-9` |
| Different clean accuracy | Wrong split settings | Match the lab protocol exactly |
| ASR changes when you change batch size | Gradient computed with a mean over the batch | Use per-row gradients; `(p − onehot) @ W` is already per-row |

## Summary and key takeaways

- FGSM maximizes a first-order approximation of the loss under an L∞ budget.
- The sign step is optimal for that approximation: every coordinate moves by ε.
- For softmax regression, the input gradient is `(p − onehot) @ W`.
- Success must be measured on a stated base set with the perturbation bound checked.
- A failed FGSM does not prove robustness.
- Iteration (PGD) fixes the "step too large or too coarse" problem.

## Check yourself

1. Derive the FGSM update from the first-order Taylor expansion.
2. Why would an L2 budget produce a different update rule?
3. What does the base set size 522 tell you about the 540-row test split?
4. Name two reasons FGSM might fail on a model that is genuinely fragile.
5. If ASR at ε = 0 is not zero, what is the most likely bug?

## Next step

[Lesson 04.3 — PGD: iteration, projection, and restarts](lesson-3-pgd.md) turns one step into many and shows how projection keeps the attack inside the budget.
