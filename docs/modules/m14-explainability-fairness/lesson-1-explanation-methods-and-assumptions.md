# Lesson 14.1 — Explanation Methods and Their Assumptions

<a id="m14-l1"></a>

**Module 14 · Lesson 1 of 4 · 1.5 hours · LO-31**

## Scenario

A loan model denies an application. The adverse-action notice lists the three features with the largest coefficients. The applicant's strongest feature is also the one with the largest negative coefficient, and the notice says it "increased the risk." The applicant's advocate runs a local explanation tool, which ranks a different feature first. Both outputs came from the same model. The dispute is not about the model's accuracy; it is about what each explanation actually computed.

This lesson builds the vocabulary to settle that dispute: what each method assumes, what it measures, and when its output should not be called the model's reasoning.

## Objectives

By the end of this lesson you will be able to:

1. Distinguish intrinsic from post-hoc explanations and global from local ones.
2. Describe the assumptions behind coefficients, gradient×input, occlusion, surrogate models, and Shapley-style attributions.
3. Compute gradient×input and occlusion attributions for a small logistic model.
4. Explain why coefficient magnitude is not a per-prediction contribution.
5. Design a fidelity check and a sanity check for an explanation method.
6. State what an explanation does not establish.

## 1. Two axes

| Axis | Left | Right | Consequence |
|---|---|---|---|
| When | Intrinsic: read from the model | Post-hoc: computed after training | Intrinsic explanations are exact for the model but limited to simple models |
| Scope | Global: behavior over a population | Local: one prediction | A global summary can be false for an individual |
| Dependence | Model-specific | Model-agnostic | Agnostic methods need many queries and inherit query noise |
| Output | Attribution scores | Rules, examples, counterfactuals | Different outputs answer different questions |

A coefficient is intrinsic and global. A LIME explanation is post-hoc and local. A SHAP value can be either, depending on the explainer. A counterfactual ("you would have been approved at income above 62,000") is local and not an attribution at all.

The first question to ask about any explanation is not "which method?" but "which of the four cells is this, and does the claim match it?"

## 2. Coefficients

For a linear model,

\[
z = w^\top x + b, \qquad p = \sigma(z),
\]

the coefficient \(w_j\) is the change in the log-odds per unit change in \(x_j\), holding other features fixed. That is a useful global statement. It is not the contribution of \(x_j\) to this prediction, for three reasons.

- **Scale.** A feature measured in thousands has a small coefficient and a large effect. Coefficients are comparable only after standardization, and even then only within the model.
- **Non-linearity.** In a logistic model the effect on probability depends on the current \(z\). The same coefficient moves probability more near 0.5 than near 0.01.
- **Correlation.** "Holding other features fixed" may describe an input that never occurs. With correlated features, the coefficient attributes shared variation to one feature and not another.

### Worked example

Take \(w = (2.0,\ -1.0,\ 0.5)\), \(b = 0.2\), and \(x = (1.0,\ 2.0,\ -1.0)\).

\[
z = 2.0(1.0) - 1.0(2.0) + 0.5(-1.0) + 0.2 = -0.3,
\qquad p = \sigma(-0.3) = 0.4256.
\]

The coefficient ranking by magnitude is \(x_1\) (2.0), \(x_2\) (1.0), \(x_3\) (0.5). The actual log-odds contributions are

\[
w_1 x_1 = 2.0,\qquad w_2 x_2 = -2.0,\qquad w_3 x_3 = -0.5.
\]

\(x_2\) has half the coefficient of \(x_1\) but the largest negative contribution, because its value is 2.0. A notice that ranks by coefficient and reports signs without multiplying by the input is wrong about this prediction even though every coefficient is correct.

## 3. Gradient×input

Gradient×input attributes

\[
A_j = x_j \frac{\partial f}{\partial x_j}(x).
\]

For the logistic model, \(\partial p/\partial x_j = p(1-p) w_j\). At \(p = 0.4256\),

\[
p(1-p) = 0.2445,
\]

so the gradient is \((0.4890,\ -0.2445,\ 0.1223)\) and

\[
A = (0.4890,\ -0.4890,\ -0.1223).
\]

The attributions sum to \(-0.1223\), not to the log-odds \(-0.3\). Gradient×input is a local linear approximation, not an additive decomposition of the output. It answers "which features have the largest first-order influence here?" and not "how much of the score did each feature produce?"

The method is cheap: one backward pass. It is also sensitive to saturation. When \(p\) is near 0 or 1, \(p(1-p)\) is near zero and every attribution shrinks, even if the features are the reason the prediction is extreme.

## 4. Occlusion

Occlusion replaces a feature with a baseline and measures the change in output:

\[
A_j = f(x) - f(x \text{ with } x_j = b_j).
\]

With baseline 0 for the same example:

| Feature removed | New \(z\) | New \(p\) | \(A_j = 0.4256 - p\) |
|---|---:|---:|---:|
| \(x_1\) | \(-2.3\) | 0.0911 | 0.3345 |
| \(x_2\) | \(1.7\) | 0.8455 | \(-0.4199\) |
| \(x_3\) | \(0.2\) | 0.5498 | \(-0.1242\) |

Occlusion ranks \(x_2\) first, then \(x_1\), then \(x_3\). Gradient×input ranked \(x_1\) and \(x_2\) as a tie in magnitude (0.4890 each) because the gradient shared the same \(p(1-p)\) factor and the input magnitudes were 1.0 and 2.0 against coefficients 2.0 and 1.0. Occlusion separates them because it measures a finite change rather than a local slope.

Which is right? Neither is the model's reasoning. They answer different questions:

- gradient×input: local sensitivity at the current point;
- occlusion: output change when the feature is set to a reference value.

The baseline is a modeling choice. Baseline 0 means "absence," which may be outside the data distribution. A baseline equal to the feature mean answers a different question. Report it.

## 5. Surrogate models and LIME

A surrogate fits a simple model \(g\) near \(x\) to approximate \(f\), then reads \(g\)'s coefficients. LIME samples points around \(x\), weights them by proximity, labels them with \(f\), and fits a sparse linear model.

| Assumption | Failure |
|---|---|
| The model is locally linear | A sharp boundary near \(x\) makes the surrogate wrong |
| Proximity-weighted samples represent the neighborhood | The sampling distribution may miss the relevant direction |
| Sparsity captures the important features | Correlated features can be dropped arbitrarily |
| The surrogate's coefficients transfer to \(f\) | Fidelity is assumed, not measured |

LIME is model-agnostic and produces human-readable local explanations. It is also stochastic: two runs with different seeds can disagree. Report the sampling variance, or the explanation is not reproducible. The original paper is explicit that the explanation is a local approximation; the risk is in how the output is presented, not in the method's definition.

## 6. Shapley-style attributions

Shapley values divide a payoff among players by averaging each player's marginal contribution over all orders in which players can join. For features, the "payoff" is the model output and the marginal contribution of feature \(j\) in a coalition \(S\) is

\[
\phi_j = \sum_{S \subseteq F \setminus \{j\}}
\frac{|S|!\,(|F|-|S|-1)!}{|F|!}
\left[f(S \cup \{j\}) - f(S)\right].
\]

The axioms — efficiency, symmetry, dummy, additivity — are attractive. Efficiency means the attributions sum to \(f(x) - f(\text{baseline})\), which is exactly what gradient×input lacks.

The cost is the number of coalitions. With \(d\) features there are \(2^d\) subsets. For \(d = 20\) that is about one million; practical estimators sample coalitions and introduce approximation error. The "baseline" is still a choice, usually a background dataset, and it changes the values. Correlated features break the independence assumption used by many estimators.

SHAP is a family of estimators, not one method. Kernel SHAP, Tree SHAP, and sampling SHAP have different costs and different approximation errors. "SHAP says feature 3 is important" is incomplete without the explainer, background data, and number of samples.

## 7. Fidelity, plausibility, and sanity checks

**Faithfulness** (or fidelity) is the degree to which the explanation reflects the computation. **Plausibility** is the degree to which it looks reasonable to a person. They are not the same, and a method can score high on one and low on the other.

### A deletion test

A simple fidelity check for an attribution:

1. Rank features by attribution magnitude.
2. Remove the top-\(k\) features (set them to baseline) and measure the output change.
3. Remove \(k\) random features and measure the output change.
4. Repeat over many inputs.

A faithful attribution should produce a larger change for the top-\(k\) removal than for random removal, on average. If it does not, the ranking does not describe the model's dependence on those features. The test is not conclusive — removal creates off-distribution inputs — but a failure is informative.

### A model-randomization sanity check

Adebayo et al. propose randomizing the model's weights layer by layer and recomputing the explanation. A method that depends on the model should produce a different explanation. If the map is unchanged after the weights are randomized, the method is largely a function of the input, not the model.

This check catches edge-detector-style saliency methods that look like explanations and are not. It does not prove that a method that passes is faithful; it only removes one failure mode.

### Stability under perturbation

Stability measures how much the explanation changes when the input changes by a small amount:

\[
\rho = \operatorname{Spearman}(A(x), A(x + \delta)), \qquad
\text{overlap} = \frac{|T(x) \cap T(x+\delta)|}{k}.
\]

A stable explanation is reproducible under the stated perturbation. It can still be unfaithful: a method that always returns the first feature is perfectly stable and useless. LAB-18 measures stability, not fidelity, and says so.

## 8. What LAB-18 actually does

LAB-18 fits a logistic model on 1,200 synthetic rows with six features and two groups. It compares a baseline model with a group-reweighted model. For each, it computes two explanation methods on 360 test rows:

- **gradient×input**: \(x_j \cdot w_j \cdot p(1-p)\);
- **occlusion**: set feature \(j\) to 0 and measure the probability change.

It then perturbs each row with isotropic Gaussian noise at \(\sigma = 0.25\), recomputes the attributions, and reports:

| Metric | Baseline gradient×input | Baseline occlusion | Reweighted gradient×input | Reweighted occlusion |
|---|---:|---:|---:|---:|
| Mean Spearman | 0.8979 | 0.8979 | 0.9010 | 0.9010 |
| Mean top-2 overlap | 0.8639 | 0.8653 | 0.8639 | 0.8653 |
| Predictions preserved (of 360) | 331 | 331 | 334 | 334 |
| Top-feature flip rate when prediction preserved | 0.1480 | 0.1390 | 0.1497 | 0.1497 |

Two observations matter.

First, gradient×input and occlusion have identical Spearman values here. For a logistic model, an occlusion change has the sign of \(w_j x_j\), and in this model the two methods induce the same feature ranking even though their scales differ. The near-identical top-2 overlap is consistent with that. This is a property of the linear model, not a general result.

Second, the flip rate is conditioned on predictions being preserved. In 331 of 360 rows the perturbed input still receives the same label, and in about 14–15% of those rows the top feature changes. An explanation can change while the decision does not — exactly the situation an attacker exploits in Lesson 2.

## 9. Choosing a method

| Need | Candidate | Check before publishing |
|---|---|---|
| Explain a linear model to a regulator | Standardized coefficients plus per-input contributions | Report scale and the input values |
| Local attribution for a non-linear model | Gradient×input or integrated gradients | Baseline, saturation, deletion test |
| Model-agnostic local explanation | Occlusion or LIME | Baseline, sampling variance, fidelity |
| Additive attribution with axioms | SHAP with a named estimator | Background data, approximation error, correlation handling |
| Global behavior summary | Permutation importance or surrogate tree | Correlation, extrapolation, subgroup breakdown |

No method in this table establishes causality. An attribution says how the model's output varies with an input under a stated procedure; it does not say what would happen to the real-world outcome if the input changed.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Ranking by coefficient magnitude | Coefficients are the visible numbers | Multiply by the input, or use an attribution method |
| Comparing coefficients across unscaled features | Units differ | Standardize and say so |
| Calling gradient×input an additive decomposition | It is a local linear approximation | Use integrated gradients or Shapley values if additivity is required |
| Ignoring the occlusion baseline | Any baseline produces a number | Report the baseline and why it was chosen |
| Running LIME once | It is stochastic | Repeat and report variance |
| Treating SHAP as exact | Estimators sample coalitions | Name the estimator and the sample count |
| Skipping a sanity check | The map looks plausible | Randomize weights and recompute |
| Equating stability with faithfulness | Both are measured on explanations | Run a deletion test separately |
| Presenting an explanation as causal | It is a model description | State that it describes the model, not the world |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Attributions sum to zero | Gradient×input with symmetric inputs, or a saturated model | Check \(p(1-p)\); use an additive method if the sum matters |
| Every feature has a tiny attribution | Model is saturated or features are clipped | Inspect probabilities and gradients |
| Occlusion gives implausible values | Baseline outside the data range | Use a background sample or the feature mean |
| LIME output changes every run | Sampling variance | Increase samples, fix the seed, report variance |
| SHAP is too slow | Exponential coalition count | Use a model-specific estimator or reduce features |
| Sanity check leaves the map unchanged | Method is input-driven, not model-driven | Do not present it as a model explanation |
| Stability is high but the explanation is wrong | Method is constant or insensitive | Add a deletion test; stability alone proves little |
| Two methods disagree | Different questions and baselines | Report both and explain the difference |

## Check your understanding

1. Why is a coefficient not a per-prediction contribution?
2. In the worked example, why do gradient×input and occlusion rank the top two features differently?
3. What does the efficiency axiom give SHAP that gradient×input lacks?
4. Design a deletion test for an attribution method. What would a failure show?
5. Why does randomizing the model's weights test an explanation method?
6. LAB-18 reports a 14.8% top-feature flip rate among rows whose prediction was preserved. Why condition on preserved predictions?

Answers are discussed in the [answer key](quiz-answers.md).

## Summary

- Explanations differ by timing, scope, model dependence, and output type. Match the claim to the cell.
- Coefficients are global log-odds effects; per-prediction contributions require the input values and, for non-linear models, a local method.
- Gradient×input is cheap and local but not additive; occlusion is finite and baseline-dependent; LIME is a stochastic surrogate; SHAP is additive under axioms but approximate in practice.
- Fidelity and plausibility are different. Deletion tests and model-randomization checks probe fidelity; visual appeal does not.
- Stability is measurable and useful, but stable explanations can still be unfaithful.
- LAB-18's stability numbers are a property of one linear model, one noise level, and one split.

## Next

Continue to [Lesson 14.2 — Explanation leakage and manipulation](lesson-2-explanation-leakage-and-manipulation.md), where the explanation output becomes an attack surface.
