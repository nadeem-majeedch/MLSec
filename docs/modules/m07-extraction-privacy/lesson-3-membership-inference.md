# Lesson 07.3 — Membership Inference

<a id="m07-l3"></a>

**1.25 hours · Lesson 3 of 5 · Module 07**

## What this lesson answers

Can an attacker tell whether a particular record was used to train a model? This lesson defines the attack, explains why confidence carries a signal, and shows why the headline AUC in LAB-10 overstates what an attacker can actually do at a strict false-positive budget.

## The attack

**Membership inference** takes a record $x$, a model $f$, and some auxiliary information, and outputs a guess:

$$
A(x, f) \rightarrow \{\text{member}, \text{nonmember}\}.
$$

A **member** was in the training set; a **nonmember** was not. The attacker usually has a **candidate pool** of records and must classify each one.

The harm is not that the attacker obtains the record. The attacker already has it. The harm is learning a fact about the record's history: that this person's data was used to train a model for a disease, a credit decision, a hiring screen, or a location service. That fact can be sensitive even when the record itself is public.

## Why a model leaks membership

A model is fit to its training data. It sees members many times and nonmembers never. Two consequences follow:

1. **Fit.** Members tend to be classified correctly and confidently.
2. **Memorization.** Atypical members may be fitted more strongly than their pattern warrants.

The simplest attack uses confidence as a membership score:

$$
s(x) = \max_c \; f(x)_c,
$$

where $f(x)_c$ is the predicted probability of class $c$. A larger maximum means "more likely a member."

This is exactly LAB-10's score. It is also the weakest realistic attack: one score, one threshold, no shadow models, no auxiliary data.

## The threat model

| Part | LAB-10 assumption |
|---|---|
| **Goal** | Decide whether an image was in the training set |
| **Access** | Query access to predicted probabilities |
| **Knowledge** | The dataset family (digits), the input format, the model type |
| **Auxiliary data** | None: no shadow models, no reference models |
| **Candidate pool** | 500 members and 500 nonmembers from the same dataset |
| **Constraint** | One score (maximum class probability) |
| **Metric** | ROC-AUC; TPR at FPR ≤ 1% and ≤ 5%; mean confidence gap |
| **Lifecycle** | Serving / monitoring; signal created during training |

The same-distribution assumption is important. LAB-10's nonmembers are the same kind of images as the members. A real attacker may test records from a different population, which changes the score distribution and can make the attack easier or harder.

## The LAB-10 procedure

1. Load the digits dataset (1,797 images, 64 features), scale to $[0, 1]$.
2. Shuffle with `default_rng(31)`. The first 500 indices are members; the next 500 are nonmembers.
3. Train `RandomForestClassifier(n_estimators=300, random_state=42)` on the 500 members only.
4. Score every record with `predict_proba(X).max(axis=1)`.
5. Build labels: 1 for members, 0 for nonmembers.
6. Compute ROC-AUC and TPR at FPR ≤ 1% and ≤ 5%.
7. Choose the 95th percentile of **nonmember** scores as a hard threshold; report TPR and FPR there.

Step 7 is easy to get wrong. The threshold is calibrated on nonmembers because the deployment constraint is "at most 5% of nonmembers may be flagged." Using the member distribution would answer a different question.

### Computing TPR at a fixed FPR

`roc_curve` returns points $(\text{FPR}_i, \text{TPR}_i)$ as the threshold decreases. To get TPR at FPR ≤ 5%:

```python
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(labels, scores)
eligible = fpr <= 0.05 + 1e-12
tpr_at_5 = float(tpr[eligible][-1])
```

Taking the last eligible point gives the largest TPR among all operating points that respect the budget. Taking the first, or reversing the arrays, produces a TPR that can exceed the TPR at a looser budget — a sign of a bug.

## The result

| Metric | Value |
|---|---:|
| Member training accuracy | 1.0000 |
| Nonmember accuracy | 0.9700 |
| Mean member confidence | 0.8784 |
| Mean nonmember confidence | 0.6918 |
| ROC-AUC | 0.8217 |
| TPR at FPR ≤ 1% | 0.0740 |
| TPR at FPR ≤ 5% | 0.2280 |
| Threshold (nonmember 95th percentile) | 0.9435 |
| TPR at threshold | 0.2280 |
| FPR at threshold | 0.0500 |

The confidence gap is 0.8784 − 0.6918 = 0.1866. Members are more confident on average. The AUC of 0.8217 means that a randomly chosen member scores above a randomly chosen nonmember about 82% of the time. Both numbers sound strong.

At a 1% false-positive budget, the attacker detects **7.4%** of members. At 5%, the attacker detects **22.8%**. The AUC is an average over every possible threshold, including thresholds that would flag half the nonmembers. A privacy officer does not have that luxury.

## What the numbers mean

### AUC is a ranking summary, not a deployment result

ROC-AUC is the probability that a random member outranks a random nonmember:

$$
\text{AUC} = \Pr\big(s(x_{\text{member}}) > s(x_{\text{nonmember}})\big).
$$

It is threshold-free. A model can have a high AUC and still be useless at the operating point that matters, because most of its advantage may sit at high false-positive rates.

### Low-FPR performance is the privacy-relevant number

At FPR ≤ 1%, five of every 500 nonmembers are falsely accused. At FPR ≤ 5%, twenty-five are. Those are the costs of using the attack. The TPR tells you how many members you catch for that cost.

$$
\text{TPR at FPR} \le \alpha = \max\{\text{TPR}_i : \text{FPR}_i \le \alpha\}.
$$

Report at least two budgets, because the curve is steep in this region.

### Precision depends on the base rate

TPR and FPR describe the test. They do not describe what happens when the test is applied to a pool with a given prevalence of members. By Bayes' rule:

$$
\Pr(\text{member} \mid \text{flagged}) =
\frac{\text{TPR} \cdot \pi}{\text{TPR} \cdot \pi + \text{FPR} \cdot (1-\pi)},
$$

where $\pi$ is the fraction of the candidate pool that is actually a member.

At the 95th-percentile threshold, TPR = 0.228 and FPR = 0.05:

| Member prevalence $\pi$ | True positives per 10,000 | False positives per 10,000 | Precision |
|---:|---:|---:|---:|
| 1% | 22.8 | 495 | 0.044 |
| 10% | 228 | 450 | 0.336 |
| 50% | 1,140 | 250 | 0.820 |
| 90% | 2,052 | 50 | 0.976 |

The same attack is a 4.4% reliable accusation in a low-prevalence pool and an 82% reliable one in a balanced pool. Neither number is "the" attack success rate. The base rate is part of the result.

The odds form makes the same point compactly:

$$
\underbrace{\frac{\pi}{1-\pi}}_{\text{prior odds}}
\times
\underbrace{\frac{\text{TPR}}{\text{FPR}}}_{\text{likelihood ratio}}
=
\underbrace{\frac{\Pr(\text{member}\mid\text{flagged})}{1-\Pr(\text{member}\mid\text{flagged})}}_{\text{posterior odds}}.
$$

At $\pi = 1\%$, the prior odds are about 1:99. A likelihood ratio of 4.56 is not enough to overcome that.

## Why confidence is not proof of membership

This is the central interpretive claim of the lab, and it has several independent reasons.

1. **The distributions overlap.** Many nonmembers are highly confident, and many members are not. The mean gap describes groups; it does not classify individuals.
2. **Easy examples are confident for everyone.** A clear digit is classified confidently whether or not it was in training. Confidence measures difficulty as well as familiarity.
3. **Atypical members can be uncertain.** A member that looks unusual may receive a low confidence despite having been seen during training.
4. **The score is not a likelihood.** Maximum softmax probability is a heuristic, not the probability of membership. Turning it into a membership probability requires a model of both distributions and a base rate.
5. **Calibration matters.** A model can be overconfident in general; confidence values are not guaranteed to be meaningful probabilities.
6. **A single threshold has error rates.** At the 95th-percentile threshold, 5% of nonmembers are flagged. Any individual flag carries that error rate unless the base rate is extremely high.

A high confidence is therefore **evidence**, in the statistical sense: it shifts the odds. It is **not proof**: it does not establish that this record was in the training set.

### Training accuracy of 1.0 is not the attack

LAB-10's members are classified with 100% accuracy; nonmembers with 97%. The model has clearly fit the training set. That does not make membership inference succeed, for three reasons:

- The nonmember accuracy is also high, so correctness barely separates the groups.
- The attack operates on confidence, and the confidence distributions overlap.
- The attack's usefulness depends on the false-positive budget and the base rate.

Conversely, a model can leak membership without perfect training accuracy. Overfitting is a useful signal, not a necessary and sufficient condition. Yeom et al. (2018) analyze this connection and show that the relationship between overfitting and membership risk is real but not a one-to-one guarantee.

## Stronger attacks, briefly

LAB-10 is a single-threshold attack with no auxiliary data. Published attacks do more:

| Attack | Extra ingredient | Why it helps |
|---|---|---|
| **Shadow-model attack** (Shokri et al., 2017) | Many models trained on similar data | Learns the target's confidence pattern instead of assuming a threshold |
| **Likelihood-ratio attack** (Carlini et al., 2022) | Reference models trained with and without each record | Compares the target's confidence to both distributions, especially in the low-FPR tail |
| **Label-only attack** (Salem et al., 2019; others) | Queries that probe boundary distance or stability | Works when probabilities are hidden |

These attacks require auxiliary data, compute, or query patterns that LAB-10 does not provide. Their existence means LAB-10's TPR is a **lower bound** for a better-resourced attacker, not an upper bound. It also means a defense validated only against the threshold attack has not been validated against the state of the art.

## Defenses and their limits

| Defense | Mechanism | Cost | Residual risk |
|---|---|---|---|
| **Regularization / early stopping** | Reduces overfitting and confidence sharpness | May lower clean accuracy | Does not eliminate memorization; no formal guarantee |
| **Smaller models / dropout** | Limits capacity to memorize | Utility loss | Memorization can persist |
| **Differential privacy** | Bounds any one record's influence on the trained model | Accuracy and training-cost trade-off; privacy budget must be chosen | Formal guarantee under the stated mechanism and parameters |
| **Output rounding / hard labels** | Removes fine-grained confidence | Less useful diagnostics and explanations | Label-only and stability attacks remain |
| **Query limits and monitoring** | Raises the cost of probing many candidates | Access restrictions; log privacy | An attacker with auxiliary models can attack offline |
| **Data minimization** | Trains on less sensitive data | Less data, possibly lower utility | Does not help for data that must be used |

Differential privacy is the only defense in this table with a formal guarantee, and that guarantee is only as good as its parameters and implementation. Regularization is a mitigation, not a privacy proof. A report should say which defense was evaluated, against which attack, at what utility cost.

## Limitations of LAB-10

- **Public digits, not people.** The records are images with no personal identity.
- **One dataset, one model family, one split.** The numbers are one draw at seed 31.
- **Same-distribution nonmembers.** A different population changes the score distributions.
- **One score.** Maximum softmax probability ignores shadow models, likelihood ratios, and label-only signals.
- **No defense evaluated.** The lab measures the attack, not a mitigation.
- **No adaptive attacker.** An attacker who knows about output rounding or monitoring may change strategy.
- **No base rate in the raw metrics.** Precision must be computed separately, as above.

## Common mistakes

| Mistake | Symptom | Correction |
|---|---|---|
| Reporting AUC as attack success | "82% accurate membership test" | Report TPR at stated FPRs |
| Ignoring prevalence | "TPR 22.8%, so most flags are right" | Compute precision at the deployment base rate |
| Using member quantiles for the threshold | Threshold TPR ≠ TPR at 5% | Use the nonmember 95th percentile |
| Scoring the wrong rows | AUC near 0.5 | Score members and nonmembers separately |
| Training on test rows | Near-perfect separation | Verify disjoint indices |
| Claiming proof of membership | "Confidence 0.99 means it was in training" | State the error rates and the overlap |
| Treating one attack as the state of the art | "The model is safe because TPR is 7%" | Acknowledge shadow-model and LiRA attacks |
| Reporting one seed as a trend | Small differences treated as real | Repeat or state the limitation |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| TPR at 1% > TPR at 5% | ROC points read in reverse | Take the last eligible point |
| Threshold TPR differs from TPR at 5% | Threshold computed on members | Calibrate on nonmember scores |
| AUC below 0.5 | Labels inverted | Members should have label 1 |
| Mean confidences equal | Scoring the same rows twice | Check the index arrays |
| Precision far below TPR | Base rate omitted | Use the Bayes formula |

## What you should be able to do now

- Define membership inference and state its threat model and metrics.
- Compute TPR at a fixed FPR and explain why AUC is not a deployment result.
- Compute precision at a stated base rate using TPR, FPR, and prevalence.
- Explain, in at least four ways, why confidence is not proof of membership.
- Name two stronger attacks and the extra ingredients they require.
- Evaluate a defense by its guarantee, cost, and residual risk.

## Summary

Membership inference tests whether a record was in training. LAB-10's maximum-confidence attack finds a real average gap — members are more confident — but at a 1% false-positive budget it detects only 7.4% of members. AUC summarizes ranking across all thresholds; privacy decisions happen in the low-FPR tail and depend on the base rate. Confidence is evidence, not proof. Stronger attacks exist and require auxiliary data, which means the lab's numbers are a lower bound, not a safety certificate.

## Next step

[Lesson 07.4 — Model inversion and attribute inference](lesson-4-inversion-and-attribute-inference.md) asks what an attacker can reconstruct from a model's output, and why the reconstruction is usually a representative rather than a record.
