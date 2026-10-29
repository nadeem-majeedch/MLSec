# Lesson 02.2 — Loss, Gradients, and Optimization

**2 hours · Lesson 2 of 4 · Prerequisite: Lesson 02.1**

## Scenario

A classifier outputs a churn probability of 0.51 for every customer. It is "right" about the majority class 74% of the time, so accuracy looks acceptable. But the model has learned nothing: its loss is high, its probabilities are uninformative, and a one-line change to the threshold flips every prediction.

Training is the process of reducing a loss by following a gradient. That sentence contains the two objects this lesson is about, and both matter for security:

- The **loss** defines what "better" means. Choose the wrong loss and the model optimizes the wrong thing.
- The **gradient** tells the model which direction to move. In Module 04, an attacker uses the same gradient with respect to the *input* to decide how to change a sample.

## What you will be able to do

- Explain what a loss function measures and why cross-entropy is used for classification.
- Derive and implement one gradient-descent step for logistic regression.
- Interpret learning rate, epochs, and batch size from a training curve.
- Distinguish a gradient with respect to parameters from a gradient with respect to inputs, and explain why the second is an attack surface.

## 1. From a score to a loss

A linear classifier computes a **logit**:

$$
z = w^\top x + b
$$

For binary classification, the sigmoid maps the logit to a probability:

$$
p = \sigma(z) = \frac{1}{1 + e^{-z}}
$$

The model's prediction is a probability. To train it, we need a number that is small when the probability is close to the true label and large when it is wrong.

### Why not accuracy?

Accuracy is a step function: a tiny change in a weight usually does not change any prediction, so the gradient is zero almost everywhere. Gradient descent needs a smooth surrogate. **Binary cross-entropy** (log loss) is that surrogate:

$$
J(w) = -\frac{1}{n}\sum_{i=1}^{n}\left[y_i \log p_i + (1-y_i)\log(1-p_i)\right]
$$

| True label | Predicted probability | Loss for that row |
|---|---:|---:|
| 1 | 0.99 | 0.010 |
| 1 | 0.50 | 0.693 |
| 1 | 0.01 | 4.605 |
| 0 | 0.01 | 0.010 |
| 0 | 0.50 | 0.693 |
| 0 | 0.99 | 4.605 |

The loss punishes confident mistakes much more than uncertain ones. That is a choice, and it has consequences: a model trained with cross-entropy will prioritize getting the confident errors right, which is often what you want and sometimes what an adversary exploits.

### Other losses

| Task | Loss | Notes |
|---|---|---|
| Binary classification | Binary cross-entropy | Outputs a probability |
| Multiclass classification | Categorical cross-entropy | Output passes through softmax |
| Regression | Mean squared error | Sensitive to outliers |
| Regression with outliers | Mean absolute error | Less sensitive, less smooth at zero |
| Ranking | Pairwise or listwise loss | Used in retrieval and recommendation |

## 2. The gradient

For a single row, let $z = w^\top x + b$ and $p = \sigma(z)$. The derivative of the sigmoid is:

$$
\frac{\partial p}{\partial z} = p(1-p)
$$

Differentiate the row loss with respect to $p$:

$$
\frac{\partial \ell}{\partial p} = -\frac{y}{p} + \frac{1-y}{1-p}
$$

Multiply the two:

$$
\frac{\partial \ell}{\partial z}
= \left(-\frac{y}{p} + \frac{1-y}{1-p}\right)p(1-p)
= -y(1-p) + (1-y)p
= p - y
$$

Then apply the chain rule to the weights and bias:

$$
\frac{\partial J}{\partial w} = \frac{1}{n}\sum_{i=1}^{n}(p_i - y_i)x_i
\qquad
\frac{\partial J}{\partial b} = \frac{1}{n}\sum_{i=1}^{n}(p_i - y_i)
$$

In matrix form, with $X$ the $n \times d$ feature matrix and $p, y$ column vectors:

$$
\nabla_w J = \frac{1}{n}X^\top(p-y)
$$

This is the entire learning rule for logistic regression. The error $(p-y)$ is weighted by each feature and averaged. If the model predicts too high for a positive example, $p-y$ is negative and the update pushes the weights down along that feature.

### The update

$$
w \leftarrow w - \eta \nabla_w J
$$

where $\eta$ is the **learning rate**. The negative sign moves against the gradient, because the gradient points toward increasing loss.

## 3. Worked example: training by hand in NumPy

```python
import numpy as np
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=600, n_features=2, n_informative=2, n_redundant=0,
    n_clusters_per_class=1, class_sep=1.2, flip_y=0.05, random_state=7,
)
X = (X - X.mean(axis=0)) / X.std(axis=0)
Xb = np.hstack([np.ones((len(X), 1)), X])

def sigmoid(z):
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1 / (1 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1 + ez)
    return out

def log_loss(w):
    p = np.clip(sigmoid(Xb @ w), 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

w = np.zeros(Xb.shape[1])
print(f"initial loss {log_loss(w):.4f}")

for epoch in range(1, 401):
    p = sigmoid(Xb @ w)
    grad = Xb.T @ (p - y) / len(y)
    w = w - 0.5 * grad
    if epoch in (1, 50, 100, 200, 400):
        acc = float(((sigmoid(Xb @ w) >= 0.5) == y).mean())
        print(f"epoch {epoch:3d}  loss {log_loss(w):.4f}  accuracy {acc:.4f}")

print("weights", np.round(w, 4))
```

Expected output:

```text
initial loss 0.6931
epoch   1  loss 0.5593  accuracy 0.9550
epoch  50  loss 0.1846  accuracy 0.9600
epoch 100  loss 0.1778  accuracy 0.9600
epoch 200  loss 0.1757  accuracy 0.9600
epoch 400  loss 0.1753  accuracy 0.9600
weights [-0.6473  1.7882 -2.6249]
```

Read the curve carefully:

- The initial loss is 0.6931, which is $\log 2$: the loss of predicting 0.5 for every row.
- After one update the loss falls to 0.5593. The first step does most of the visible work because the initial error is large.
- Accuracy jumps to 0.955 immediately, then barely moves. **Accuracy hides progress.** Loss keeps falling from 0.1846 to 0.1753 while the thresholded accuracy is already saturated.
- The weights are not unique in a separable problem. A different learning rate or number of epochs gives different weights and nearly the same predictions.

The stable sigmoid implementation avoids overflow in `np.exp` for large negative logits. A naive `1 / (1 + np.exp(-z))` warns and can return `nan` when `z` is very negative.

## 4. Learning rate, epochs, and batches

| Term | Meaning | Effect |
|---|---|---|
| Learning rate $\eta$ | Step size | Too small: slow. Too large: overshoot and instability |
| Epoch | One pass over the training data | More epochs fit more, until overfitting |
| Batch size | Rows per update | Small: noisy but frequent. Large: stable but expensive |
| Iteration | One parameter update | Number of iterations = epochs × (n / batch size) |

Run the same data for 10 epochs at four learning rates:

```python
print("learning-rate comparison after 10 epochs")
for lr in (0.001, 0.01, 0.5, 50.0):
    w2 = np.zeros(Xb.shape[1])
    for _ in range(10):
        w2 = w2 - lr * (Xb.T @ (sigmoid(Xb @ w2) - y) / len(y))
    acc = float(((sigmoid(Xb @ w2) >= 0.5) == y).mean())
    print(f"lr {lr:<6} loss {log_loss(w2):.4f}  accuracy {acc:.4f}  norm {np.linalg.norm(w2):.2f}")
```

Expected output:

```text
lr 0.001  loss 0.6902  accuracy 0.9550  norm 0.01
lr 0.01   loss 0.6646  accuracy 0.9550  norm 0.05
lr 0.5    loss 0.2613  accuracy 0.9550  norm 1.40
lr 50.0   loss 0.3675  accuracy 0.9633  norm 10.31
```

All four have nearly the same accuracy after 10 epochs, but the losses differ by a factor of 2.6 and the weight norms by a factor of 1000. This is why a training log that prints only accuracy is not a training log. The high learning rate overshoots: at `lr 50` the loss is worse than at `lr 0.5` after the same number of steps, even though the accuracy is slightly higher by chance.

At even larger learning rates, weights can oscillate or overflow. If the loss becomes `nan` or `inf`, the first thing to check is the learning rate and the scale of the inputs.

### Batch, stochastic, and mini-batch

| Variant | Update uses | Trade-off |
|---|---|---|
| Batch gradient descent | All rows | Stable, expensive per step |
| Stochastic gradient descent | One row | Noisy, many updates |
| Mini-batch | 32–512 rows | The usual compromise |

Noise is not only a cost. In non-convex problems, stochasticity can help escape poor regions, and it makes exact reproduction harder. That trade-off is why seeds and deterministic settings are part of every lab.

## 5. The same gradient, two different questions

The gradient with respect to the weights answers: *how should the model change to reduce loss?*

The gradient with respect to the input answers: *how should this sample change to increase loss?*

For the linear model above:

$$
\frac{\partial J}{\partial x} = (p-y)\,w
$$

An attacker who wants a positive sample classified as negative can take a step in the direction that increases the loss:

$$
x' = x + \epsilon\,\mathrm{sign}\!\left(\frac{\partial J}{\partial x}\right)
$$

That is the Fast Gradient Sign Method, which you will implement in Module 04. The perturbation budget $\epsilon$ plays the role of the learning rate, but the goal is inverted: the attacker maximizes loss instead of minimizing it.

| Object | Who computes it | Goal |
|---|---|---|
| Parameter gradient | Training code | Minimize loss on training data |
| Input gradient | Attacker with white-box access | Maximize loss on a chosen sample |
| Input gradient under a defense | Evaluator | Test whether the defense actually removes the vulnerability |

A model with no usable input gradient is not automatically robust. It may have obfuscated gradients, a failure mode Module 06 covers. For now, remember that the gradient is a property of the model and the loss, not a security feature.

## 6. What "converged" does and does not mean

A training loss that stops decreasing tells you the optimizer stopped improving on the training data. It does not tell you:

- that the model generalizes;
- that the loss matches the decision cost;
- that the probabilities are calibrated;
- that the model is robust to a small input change;
- that the training data was representative.

Those are evaluation questions, and they are the subject of Lesson 02.3. A low training loss is a necessary condition for a useful model, not a sufficient one.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Forgetting to average the gradient | Loss explodes with dataset size | Divide by `len(y)` or use the library's reduction |
| Adding the gradient instead of subtracting | Loss increases every step | Use `w = w - lr * grad` |
| Learning rate too large | Loss oscillates or becomes `nan` | Reduce by 10× and check input scaling |
| Learning rate too small | Loss barely moves after many epochs | Increase, or standardize features |
| Unscaled features | Slow or unstable training | Standardize before fitting |
| `log(0)` in a hand-written loss | `inf` or `nan` | Clip probabilities to a small range |
| Evaluating on training data | Excellent score, poor production behavior | Hold out data before training |
| Reporting only accuracy | Flat curve hides improvement or failure | Log loss, accuracy, and a validation metric |

## Troubleshooting

| Symptom | Likely cause | Check |
|---|---|---|
| Loss is `nan` at step 1 | Overflow in sigmoid or log | Use a stable sigmoid and clip probabilities |
| Loss decreases, then jumps | Learning rate too high | Lower it and plot per epoch |
| Loss flat from the start | Learning rate too low, or no signal | Try a larger rate; check label alignment |
| Training accuracy 1.0, validation poor | Overfitting | Regularization, simpler model, more data |
| Weights grow without bound | Separable data, no regularization | Add L2 regularization or early stopping |
| Different result each run | Unseeded shuffling or initialization | Set seeds; use `random_state` |
| Gradient is all zeros | Saturating sigmoid, or detached tensor | Check inputs and the computation graph |

## Glossary

| Term | Definition |
|---|---|
| **Logit** | The raw score before the sigmoid or softmax |
| **Sigmoid** | The function mapping a logit to a probability in (0, 1) |
| **Softmax** | The multiclass generalization of the sigmoid |
| **Cross-entropy** | The negative log-likelihood of the true label under the predicted distribution |
| **Gradient** | The vector of partial derivatives of the loss |
| **Gradient descent** | Iteratively stepping against the gradient |
| **Learning rate** | The step size of each update |
| **Epoch** | One pass over the training set |
| **Batch size** | The number of rows per update |
| **Convergence** | The point where the optimizer stops making meaningful progress |
| **Regularization** | A penalty or constraint that discourages overfitting |

## Summary and key takeaways

- A loss turns "better" into a number the optimizer can improve; cross-entropy is the standard choice for classification.
- For logistic regression, the gradient is the average of the error times the features: $\frac{1}{n}X^\top(p-y)$.
- The learning rate controls the step size; too small is slow, too large is unstable.
- Accuracy can saturate while loss keeps falling, so log both.
- The same gradient machinery trains the model and attacks it; the difference is whether you differentiate with respect to parameters or inputs.
- A low training loss is not evidence of generalization, calibration, or robustness.

## References and further reading

All links checked on 2026-10-28.

| Reference | Use |
|---|---|
| [scikit-learn linear models](https://scikit-learn.org/stable/modules/linear_model.html) | Logistic regression and regularization |
| [scikit-learn SGD](https://scikit-learn.org/stable/modules/sgd.html) | Stochastic gradient descent in practice |
| [scikit-learn loss functions](https://scikit-learn.org/stable/modules/model_evaluation.html#log-loss) | Log loss definition and usage |
| [NumPy `exp`](https://numpy.org/doc/stable/reference/generated/numpy.exp.html) | Overflow behavior and stable computation |

## Next step

Continue to [Lesson 02.3 — Generalization and honest evaluation](lesson-3-evaluation.md). You will use the probabilities from a trained model to compute the metrics that a security report actually needs.
