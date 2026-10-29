# Lesson 07.4 — Model Inversion and Attribute Inference

<a id="m07-l4"></a>

**1.25 hours · Lesson 4 of 5 · Module 07**

## What this lesson answers

What can an attacker reconstruct from a model's output? This lesson defines model inversion, works through a solvable example, and explains why the result is usually a **representative** chosen by the attacker's prior — not a record recovered from a database.

## Two related attacks

**Model inversion** optimizes an input to produce a target output:

$$
x^{*} = \arg\max_{x \in \mathcal{X}} \; \log f_y(x) - \lambda \, R(x),
$$

where:

- $x$ is a candidate input,
- $y$ is the target class,
- $f_y(x)$ is the model's predicted probability for class $y$,
- $R(x)$ is a prior or regularizer that encodes what the attacker expects a plausible input to look like,
- $\lambda \ge 0$ controls how strongly the prior constrains the search,
- $\mathcal{X}$ is the allowed input space (for example, pixel values in $[0,1]$).

The log-probability is maximized because probabilities are small and their logs are better behaved numerically. The prior is not a detail. It decides which of the many inputs with a high score the attacker reports.

**Attribute inference** uses a model's output to infer a hidden sensitive attribute, such as sex, age group, or health status, from visible features. It is not the same as inversion: the attacker is not reconstructing the whole input, only filling in a field. The two are related because both exploit the model's dependence on information the attacker does not directly observe.

## The threat model

| Part | Class-representative inversion | Instance reconstruction | Attribute inference |
|---|---|---|---|
| **Goal** | Find an input that produces a class's typical output | Recover features of a training record | Infer a hidden attribute |
| **Access** | Confidence values, or a copy of the model | Confidence values and the target record's non-sensitive fields | Model output and auxiliary data |
| **Knowledge** | Input format, class labels, a prior | Overfitting model, auxiliary data | Correlations learned from auxiliary data |
| **Output** | A synthetic representative | A candidate reconstruction | A predicted attribute |
| **Metric** | Confidence achieved; resemblance | Distance to the true record | Attribute accuracy versus base rate |
| **Harm** | Class-level disclosure; possible resemblance to people | Individual disclosure | Sensitive-attribute disclosure |

Fredrikson, Jha, and Ristenpart (2015) studied the class-representative version against face-recognition models that returned confidence values. They optimized an input to maximize a target class's confidence, used a prior to keep the result plausible, and showed reconstructions that resembled the class. They also evaluated countermeasures: hiding confidence, rounding it, and adding noise all reduced the attack, but did not necessarily eliminate it.

## A solvable example

Take a two-feature logistic model:

$$
f(x) = \sigma(w \cdot x + b), \qquad w = (2, 1), \; b = -3.
$$

Suppose the attacker wants an input with confidence $c = 0.9$ for the positive class. The logit at that confidence is

$$
t = \log\frac{c}{1-c} = \log\frac{0.9}{0.1} = 2.1972.
$$

The constraint is $w \cdot x + b = t$, which is a line. To pick one point on it, the attacker minimizes distance to a prior mean $\mu$:

$$
x^{*} = \mu + \frac{t - (w \cdot \mu + b)}{\lVert w \rVert^{2}} \, w.
$$

With $\mu = (0,0)$:

$$
x^{*} = \frac{2.1972 + 3}{5}(2,1) = (2.0789, 1.0394).
$$

Check: $2(2.0789) + 1.0394 - 3 = 2.1972$, so $f(x^{*}) = 0.9$.

### The model does not determine a unique input

Every point on the line $2x_1 + x_2 - 3 = 2.1972$ has confidence 0.9:

| Input | Confidence |
|---|---:|
| $(2.0789, 1.0394)$ | 0.9000 |
| $(0.0000, 5.1972)$ | 0.9000 |
| $(3.5000, -1.8028)$ | 0.9000 |

The first is the closest to the origin. The others are equally consistent with the model. If the attacker's prior changes, the reported input changes. With $\mu = (5,5)$:

$$
x^{*} = (5,5) + \frac{2.1972 - 12}{5}(2,1) = (1.0789, 3.0394),
$$

which also has confidence 0.9 but is a different input entirely.

This is the first reason inversion is not a lookup: **the output is underdetermined by the model**. The prior picks a representative from an infinite set.

## A nonlinear example

Linear models are convenient but their maxima sit at the edge of the allowed input space: pushing $x$ further in the direction of $w$ always increases the score. A bounded model such as a small neural network has interior maxima, but it can also extrapolate confidently outside its training region.

The following experiment trains a 16-unit MLP on two Gaussian clusters in two dimensions, then searches a grid for the input that maximizes the positive-class probability.

```python
import numpy as np
from sklearn.neural_network import MLPClassifier

rng = np.random.default_rng(7)
n = 300
X0 = rng.normal((-1.5, 0.0), 0.8, (n, 2))
X1 = rng.normal((1.5, 0.0), 0.8, (n, 2))
X = np.vstack([X0, X1])
y = np.r_[np.zeros(n, dtype=int), np.ones(n, dtype=int)]

clf = MLPClassifier(hidden_layer_sizes=(16,), max_iter=3000, random_state=1).fit(X, y)

grid = np.arange(-4.0, 4.0001, 0.02)
xx, yy = np.meshgrid(grid, grid)
points = np.c_[xx.ravel(), yy.ravel()]
p = clf.predict_proba(points)[:, 1]

best = int(p.argmax())
print("training accuracy:", round(clf.score(X, y), 4))
print("argmax:", np.round(points[best], 2), "confidence:", round(float(p[best]), 4))
print("class-1 mean:", np.round(X1.mean(axis=0), 2))
```

Output:

```text
training accuracy: 0.9783
argmax: [ 4. -4.] confidence: 1.0
class-1 mean: [ 1.57 -0.09]
```

The unconstrained maximum is the corner $(4,-4)$, outside both clusters, with confidence 1.0. The network extrapolates confidently into a region it never saw. This is not a recovered record; it is an artifact of maximizing a score without a plausibility constraint.

Add a prior centered on the class mean, $R(x) = \lVert x - (1.5,0) \rVert^{2}$ with $\lambda = 1$:

```python
prior = np.array([1.5, 0.0])
objective = np.log(p + 1e-12) - 1.0 * ((points - prior) ** 2).sum(axis=1)
best = int(objective.argmax())
print(np.round(points[best], 2), round(float(p[best]), 4))
```

Output:

```text
[1.5 0. ] 0.9887
```

The result is the class mean, with high confidence. Change the prior to a particular training member, $x_i = (0.1884, 0.4645)$:

| Prior | Recovered input | Confidence | Distance to prior |
|---|---|---:|---:|
| None (grid max) | $(4.00, -4.00)$ | 1.0000 | — |
| Class mean $(1.50, 0)$ | $(1.50, 0.00)$ | 0.9887 | 0.00 |
| Member $x_i$ | $(0.44, 0.42)$ | 0.8838 | 0.26 |

The member itself has confidence 0.7262 — lower than the class mean, even though it was in the training set. A prior centered on it moves the reconstruction toward it, but does not return it exactly. The reconstruction is a point chosen by the objective; it is not evidence that the attacker recovered that member's data.

This is the second reason inversion is not a lookup: **the prior and the objective determine the output at least as much as the record does**.

## Attribute inference

Attribute inference asks a narrower question: given visible features $v$ and the model's output $f(v,a)$, what is the hidden attribute $a$?

A model that uses a sensitive attribute in its decision creates a channel:

$$
f(v, a=1) \neq f(v, a=0) \quad \Longrightarrow \quad \text{the output carries information about } a.
$$

An attacker with auxiliary data can learn the mapping from $(v, \text{output})$ to $a$ and apply it to target records. The attack does not require membership; the attribute may be present for every record in the population.

### A numerical illustration

Suppose a scoring model is

$$
f(v,a) = \sigma(0.04\,\text{age} + 0.02\,\text{hours} + 1.1\,a - 2.0),
$$

where $a=1$ denotes one sex and $a=0$ the other. For a record with age 35 and hours 40:

| Hidden $a$ | Logit | Predicted probability |
|---|---:|---:|
| 0 | 0.20 | 0.550 |
| 1 | 1.30 | 0.786 |

An observed probability of 0.786 is much closer to the $a=1$ counterfactual than to the $a=0$ one. If the attacker knows the model, the attribute is readable. If the attacker has only query access, a surrogate trained on auxiliary data can approximate the same comparison.

This example is deliberately simple. Real attribute inference depends on:

- how strongly the model uses the attribute,
- how much the visible features already predict it,
- whether the attacker can obtain auxiliary data with the attribute labeled,
- and whether the model's output is granular enough to distinguish the counterfactuals.

It is also worth separating two cases. If the attacker can query the model with both values of the hidden attribute, the attribute is directly readable and the model should not expose that interface. If the attacker cannot, the attack relies on correlations and auxiliary data, and its accuracy is an empirical question.

## Why designers should care

| Scenario | What inversion can reveal | Why it matters |
|---|---|---|
| Face verification with confidence | Class representatives that resemble people | Biometric privacy; consent and identity risk |
| Health-risk model | Typical feature profiles for a condition | Sensitive-attribute disclosure |
| Credit or hiring model | Which side of a protected attribute a record falls on | Discrimination and legal risk |
| Recommender system | Preferences associated with a group | Profiling and chilling effects |

The harm is contextual. A reconstructed representative that resembles no real person may still disclose a sensitive class pattern. A reconstruction that resembles a real person is a stronger harm, but the resemblance must be demonstrated, not assumed.

## Defenses and their limits

| Defense | Mechanism | Cost | Residual risk |
|---|---|---|---|
| **Hide confidence** | Return hard labels only | Less useful explanations; label-only extraction remains | Some inversion attacks use only labels and repeated queries |
| **Round or truncate outputs** | Reduce the precision of probabilities | Utility and calibration loss | Coarse signal can still support optimization |
| **Add output noise** | Perturb responses | Accuracy and reproducibility loss | Noise can be averaged out over queries |
| **Limit queries** | Cap the number of optimization steps | Access restrictions | A patient attacker with multiple accounts |
| **Regularize the model** | Reduce overfitting and sharp confidence | Utility trade-off | Does not remove the dependence on sensitive features |
| **Differential privacy** | Bound any one record's influence | Accuracy and training-cost trade-off | A formal guarantee under stated parameters |
| **Remove sensitive features** | Do not train on the attribute | Possible accuracy loss; proxy features remain | Correlated features can reconstruct it |
| **Access control** | Restrict who can query and what they see | Operational overhead | Insiders and compromised accounts |

Fredrikson et al. (2015) evaluated confidence hiding and output perturbation as countermeasures and found that they reduce inversion quality but do not make it impossible. That is the right way to state a defense result: reduced under a measured attack, with residual risk, not "solved."

## What inversion does not show

- **It does not show that a specific person's record was recovered.** A representative can resemble many people or none.
- **It does not show that the model memorized the training set.** Class-level structure is enough for a representative.
- **It does not show that the model is unsafe to deploy.** The harm depends on the attribute, the population, the access model, and the alternatives available to the attacker.
- **It does not generalize across model families or input domains.** A 2D synthetic example is a mechanism demonstration.

## Common mistakes

| Mistake | Symptom | Correction |
|---|---|---|
| Calling the output "the training record" | A blurry reconstruction presented as a victim's data | Say "a representative under prior $R$" |
| Omitting the prior | The reported input is arbitrary | State $R$, $\lambda$, and the input bounds |
| Maximizing confidence without bounds | The input runs to a corner or infinity | Bound the input space and explain the choice |
| Ignoring the model's extrapolation | A confident input outside the data distribution | Check whether the result is in-distribution |
| Confusing inversion with membership | "The model leaked this record" | State which question the experiment answers |
| Reporting attribute accuracy without a baseline | "78% accurate" | Compare with the majority class and visible-feature-only baselines |
| Assuming a defense is complete | "We hide confidence" | Measure the residual attack |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Inversion output at the boundary | Unconstrained linear score | Add a prior or a confidence target |
| Reconstruction is identical to the class mean | Strong prior, weak individual signal | That is the expected result; report it |
| Reconstruction looks like noise | No plausible-input constraint | Use a prior suited to the input domain |
| Attribute accuracy equals the base rate | Model output does not depend on the attribute | Check the model and the features |
| Attribute accuracy is implausibly high | The attribute was used as an input feature at inference | Recheck the threat model; that is direct disclosure |

## What you should be able to do now

- Write the inversion objective and explain every symbol.
- Solve the linear confidence-target example and show that the solution is not unique.
- Explain why an unconstrained neural-network inversion can leave the data distribution.
- Distinguish class-representative inversion, instance reconstruction, and attribute inference.
- Evaluate an inversion defense by its measured residual risk and cost.

## Summary

Model inversion optimizes an input to produce a target output, usually with a prior that keeps the result plausible. The model does not determine a unique input: many inputs share a confidence, and the prior chooses among them. A nonlinear model can be pushed outside its training distribution, producing confident but meaningless inputs. Attribute inference is the narrower version: the model's dependence on a hidden attribute creates a channel. In both cases, the result is evidence about the model and its training distribution, not proof that a particular record was recovered.

## Next step

[Lesson 07.5 — Privacy risk, governance, and reporting](lesson-5-privacy-risk-and-governance.md) puts extraction, membership inference, and inversion into one decision memo with base rates, costs, and residual risk.
