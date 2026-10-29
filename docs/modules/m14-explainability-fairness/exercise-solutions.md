# Module 14 Exercise Solutions

## Exercise 1 — Three explanations, one prediction

### 1. Log-odds contributions

\[
z = 1.0(2.0) - 1.5(1.0) + 0.8(-5.0) - 0.2
= 2.0 - 1.5 - 4.0 - 0.2 = -3.7.
\]

\[
p = \sigma(-3.7) = 0.0241.
\]

The contributions \(w_j x_j\) are

\[
(2.0,\ -1.5,\ -4.0).
\]

Ranking by magnitude: feature 3 (4.0), feature 1 (2.0), feature 2 (1.5).

### 2. Gradient×input

\[
p(1-p) = 0.0241 \times 0.9759 = 0.02355.
\]

\[
\nabla_x p = 0.02355 \times (1.0,\ -1.5,\ 0.8)
= (0.02355,\ -0.03533,\ 0.01884).
\]

\[
A = x \odot \nabla_x p = (0.0471,\ -0.0353,\ -0.0942).
\]

Ranking by magnitude: feature 3 (0.0942), feature 1 (0.0471), feature 2 (0.0353).

### 3. Occlusion, baseline 0

\[
p = 0.0241.
\]

| Removed | New \(z\) | New \(p\) | Occlusion |
|---|---:|---:|---:|
| 1 | \(-5.7\) | 0.0033 | 0.0208 |
| 2 | \(-2.2\) | 0.0997 | \(-0.0756\) |
| 3 | \(0.3\) | 0.5744 | \(-0.5503\) |

Ranking by magnitude: feature 3 (0.5503), feature 2 (0.0756), feature 1 (0.0208).

### 4. Why the rankings differ

The coefficient ranking is \(x_2, x_1, x_3\) by \(|w_j|\). The contribution ranking is \(x_3, x_1, x_2\), because feature 3 has a large negative input. Gradient×input agrees with the contribution ranking exactly here, because in a logistic model \(A_j = p(1-p)\,w_j x_j\): the common factor \(p(1-p)\) does not change the ordering. Occlusion agrees on feature 3 but ranks feature 2 above feature 1, because removing feature 2 changes probability more than removing feature 1 even though feature 1 has the larger contribution. The finite change is evaluated at a different \(z\), so the local derivative is not the same for every feature. The methods answer different questions:

- coefficient: global log-odds effect per unit;
- contribution and gradient×input: local influence at this input;
- occlusion: output change when a feature is set to a reference value.

For the applicant, the contribution or a counterfactual statement is more useful than the coefficient. A coefficient list would say feature 2 matters most, which is false for this prediction. Practical choice: publish plain-language contributions or a counterfactual, with the method and baseline stated, and keep the full attribution vector internal.

### 5. The counterfactual question

Occlusion with baseline 0 contains enough information for this specific change: it computes

\[
p(x) - p(x \text{ with } x_3 = 0) = -0.5503,
\]

so \(p(x_3=0) = 0.0241 + 0.5503 = 0.5744\). If the approval threshold is 0.5, the answer for this one change is "the score would cross the threshold."

What it does not establish:

- that the change is possible or that other features would stay fixed in reality;
- that the model's output corresponds to the real decision (there may be policy rules, human review, or a different threshold);
- that changing feature 3 would cause approval — it is a model counterfactual, not a causal effect;
- anything about a different change, a different baseline, or a different model version.

## Exercise 2 — Explanation endpoint threat model

### 1. Threat model

| Element | Entry |
|---|---|
| Asset | Model weights, training-data properties, decision integrity, applicant trust |
| Audience | Authenticated caseworkers, possibly many accounts |
| Channel | Top-5 per-feature contributions to the log-odds, arbitrary input values |
| Capability | Can vary all features, query repeatedly, and observe exact numbers |
| Objective | Extract the model, probe the boundary, or find a benign-looking reason for a decision |
| Impact | Competitive loss, privacy harm, manipulated appeals, regulatory exposure |
| Residual | An authenticated, patient attacker can still learn a great deal |

### 2. Weight recovery

If the endpoint returns \(c_j = w_j x_j\):

- Query \(x = 0\): if the score is returned, read \(b\); the contributions are all zero.
- Query \(x = e_j\) for each of the four features: the response is \(w_j\).
- Four feature queries plus one intercept query recover the model exactly: five queries.

If the endpoint returns only probabilities, compute \(z = \log(p/(1-p))\) for each query and subtract: \(z(e_j) - z(0) = w_j\). The number of queries is the same.

### 3. Top-2 only

Top-2 filtering does not stop the procedure. The attacker sets one feature to a large value and the others to zero. That feature is guaranteed to be in the top 2, and its response reveals \(w_j\) up to the chosen scale. Repeating for each feature recovers all weights with more queries. Filtering reduces information per response; it does not remove the channel.

### 4. Controls

- **Coarsen the output.** Return sign and a small number of buckets, not full-precision contributions.
- **Reduce the feature set.** Return reason codes for policy-relevant factors rather than a complete attribution vector.
- **Remove the score.** Do not return log-odds or probabilities alongside attributions; the attributions alone are harder to invert.
- **Detection:** log queries and alert on high-volume, low-diversity patterns or on inputs that isolate single features.

### 5. Why authentication is not enough

Authentication establishes who is calling. It does not limit what an authenticated caller can learn, how many queries they can make, or whether their account is compromised. A caseworker with a legitimate need to see one application can still script thousands of queries. Authorization, budgets, output design, and monitoring are the controls that bound the information channel.

## Exercise 3 — Subgroup audit

### 1. Per-group metrics

**Baseline**

| Group | n | TPR | FPR | Selection | Accuracy |
|---|---:|---:|---:|---:|---:|
| A | 500 | \(105/150 = 0.700\) | \(70/350 = 0.200\) | \(175/500 = 0.350\) | \(385/500 = 0.770\) |
| B | 300 | \(78/120 = 0.650\) | \(36/180 = 0.200\) | \(114/300 = 0.380\) | \(222/300 = 0.740\) |

**Reweighted**

| Group | n | TPR | FPR | Selection | Accuracy |
|---|---:|---:|---:|---:|---:|
| A | 500 | \(102/150 = 0.680\) | \(70/350 = 0.200\) | \(172/500 = 0.344\) | \(382/500 = 0.764\) |
| B | 300 | \(78/120 = 0.650\) | \(36/180 = 0.200\) | \(114/300 = 0.380\) | \(222/300 = 0.740\) |

### 2. Gaps

Baseline:

\[
\text{DP} = |0.350 - 0.380| = 0.030,
\qquad
\text{EOd} = \max(|0.700-0.650|,\ |0.200-0.200|) = 0.050.
\]

Reweighted:

\[
\text{DP} = |0.344 - 0.380| = 0.036,
\qquad
\text{EOd} = \max(|0.680-0.650|,\ 0) = 0.030.
\]

### 3. Accuracy cost

Baseline overall:

\[
(385 + 222)/800 = 607/800 = 0.75875.
\]

Reweighted overall:

\[
(382 + 222)/800 = 604/800 = 0.75500.
\]

The cost is 0.00375, or about 0.4 percentage points. The intervention reduced the equalized-odds gap by 0.020 and increased the demographic-parity gap by 0.006.

### 4. Leveling down

The TPR gap fell because group A's TPR dropped from 0.700 to 0.680, not because group B's rose. Arguments:

- **For calling it an improvement:** the criterion is equalized odds, and the gap is smaller. The model now misses true positives at more similar rates across groups.
- **Against:** the improvement comes from making the better-served group worse. Group A now has 48 false negatives instead of 45; no group gained. A policy that values finding true positives may reject this trade.

What to report: "The equalized-odds gap fell from 0.050 to 0.030, entirely because group A's TPR fell from 0.700 to 0.680; group B's TPR was unchanged. Overall accuracy fell by 0.00375. The change levels down rather than raising the lower group." That gives the committee the direction and mechanism, not just the gap.

### 5. Intervals

For group B, \(n_{\text{pos}} = 120\), \(\hat{p} = 0.65\):

\[
SE = \sqrt{0.65 \times 0.35 / 120} \approx 0.0435,
\]

so an approximate 95% interval is \(0.65 \pm 1.96(0.0435) \approx [0.565, 0.735]\).

For group A, \(n_{\text{pos}} = 150\), \(\hat{p} = 0.70\):

\[
SE = \sqrt{0.70 \times 0.30 / 150} \approx 0.0374,
\]

so the interval is \(0.70 \pm 1.96(0.0374) \approx [0.627, 0.773]\).

The intervals overlap substantially. The 0.05 point gap is well within sampling uncertainty; this evaluation does not establish a population TPR difference. A decision that depends on that gap needs more positives per group or a paired design.

### 6. One-sentence summary

"On 800 synthetic applicants, reweighting lowered the equalized-odds gap from 0.050 to 0.030 by reducing group A's TPR from 0.700 to 0.680 while leaving group B unchanged, raised the demographic-parity gap from 0.030 to 0.036, and reduced overall accuracy from 0.7588 to 0.7550; the subgroup intervals overlap, so the population-level change is not established."

## Exercise 4 — Report critique

### 1. Problems

1. **"Fair" from one metric.** DP 0.001 says nothing about TPR or FPR gaps. The report should include equalized odds and calibration.
2. **Stability presented as trustworthiness.** Spearman 0.99 is stability under an unstated perturbation; it is not fidelity, and it does not show resistance to targeted manipulation.
3. **Full attribution vectors exposed.** This is a high-bandwidth extraction channel. Authentication and logging do not bound the information per response.
4. **Partial trade-off disclosure.** The report mentions the EOd improvement (0.12 to 0.09) but omits the DP change, the accuracy cost, and any interval.
5. **No uncertainty.** "One held-out split" with point estimates and no interval cannot support a population claim.
6. **No utility baseline for 0.91 accuracy.** Without a non-private or pre-intervention reference, the number has no context.
7. **DP-SGD at epsilon 8 without scope.** No neighboring relation, delta, composition, or utility comparison. The privacy claim is incomplete.
8. **No residual risks or decision record.** The report does not say what was not tested or who owns the conclusion.

Any six are sufficient.

### 2. Scoped rewrite

> On one synthetic held-out split, the model achieved 0.91 accuracy. The demographic-parity gap was 0.001; equalized-odds and calibration gaps were not reported. A group-reweighted variant reduced the equalized-odds gap from 0.12 to 0.09, but the demographic-parity and accuracy costs and the sampling intervals were not reported, so the population-level effect is not established. Explanation stability was 0.99 Spearman under an unstated perturbation; fidelity and targeted manipulation were not tested. The endpoint returns full attribution vectors to authenticated users, which creates an extraction channel not addressed by logging. DP-SGD was applied at epsilon 8 with no stated relation, delta, composition, or utility baseline. These results apply to this split and model family only.

### 3. Residual risks

- **Extraction and inversion** through full attribution responses.
- **Targeted explanation manipulation** that preserves predictions.
- **Unmeasured subgroup harms**, including calibration, intersectional groups, and small groups.
- **Distribution shift** after deployment, which can change both fairness gaps and explanation stability.
- **Privacy claims outside the stated budget**, including repeated releases and linkage attacks.
- **Label bias** in the training data, which no metric in the report addresses.
- **Operational misuse** of explanations by reviewers who treat them as causal.

Any four are sufficient.
