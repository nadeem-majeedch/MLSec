# Knowledge Check Answers — QZ-14

**Module 14 · 10 items · 14 points**

## 1. (1 point)

\[
z = 1.5(2.0) - 2.0(1.0) + 0.5(-2.0) + 0.1
= 3.0 - 2.0 - 1.0 + 0.1 = 0.1.
\]

The log-odds contributions \(w_j x_j\) are

\[
(3.0,\ -2.0,\ -1.0).
\]

Feature 1 contributes most in magnitude (3.0). Feature 2 has the largest coefficient magnitude (2.0) but contributes less here because its input is 1.0 rather than 2.0. Coefficient magnitude and per-prediction contribution are different quantities.

## 2. (2 points)

\[
p = \sigma(0.1) = 0.5250, \qquad p(1-p) = 0.2494.
\]

The gradient is

\[
0.2494 \times (1.5,\ -2.0,\ 0.5) = (0.3741,\ -0.4988,\ 0.1247),
\]

so gradient×input is

\[
A = (0.7481,\ -0.4988,\ -0.2494).
\]

The attributions sum to \(-0.0001\) (rounding), not to \(z = 0.1\). Gradient×input is a local linear approximation of the probability, not an additive decomposition of the log-odds. If additivity is required, use an integrated-gradient or Shapley-style method with a stated baseline.

## 3. (1 point)

With baseline 0 the output at \(x\) is \(p = 0.5250\).

| Removed feature | New \(z\) | New \(p\) | Occlusion \(= 0.5250 - p\) |
|---|---:|---:|---:|
| 1 | \(-2.9\) | 0.0522 | 0.4728 |
| 2 | \(2.1\) | 0.8909 | \(-0.3659\) |
| 3 | \(1.1\) | 0.7503 | \(-0.2253\) |

Feature 1 has the largest absolute occlusion value (0.4728). The ranking differs from the coefficient ranking and from the log-odds contribution ranking, because occlusion measures a finite change from a chosen baseline.

## 4. (2 points)

Both can be true because the metrics measure different things. Demographic parity compares selection rates; equalized odds compares TPR and FPR. Two groups can be selected at nearly the same rate while their error rates differ, especially when base rates differ.

With FPRs 0.26 and 0.14, the FPR gap is 0.12. That alone produces an equalized-odds gap of at least 0.12, regardless of the TPR gap. The group with FPR 0.26 bears the larger false-positive burden: its members are incorrectly flagged at nearly twice the rate. A DP-only report would have shown 0.001 and hidden this.

## 5. (1 point)

The error is treating stability as faithfulness. Stability measures whether the explanation changes under a perturbation. A method that always returns the same feature, or one that is insensitive to the model, is perfectly stable and can be completely unfaithful. Faithfulness requires a separate check, such as a deletion test or a model-randomization sanity check.

## 6. (2 points)

Group A:

\[
\text{TPR} = 60/100 = 0.60,\quad
\text{FPR} = 30/100 = 0.30,\quad
\text{selection} = 90/200 = 0.45.
\]

Group B:

\[
\text{TPR} = 30/50 = 0.60,\quad
\text{FPR} = 10/50 = 0.20,\quad
\text{selection} = 40/100 = 0.40.
\]

\[
\text{DP gap} = |0.45 - 0.40| = 0.05,
\]

\[
\text{EOd gap} = \max(|0.60-0.60|,\ |0.30-0.20|) = 0.10.
\]

The TPRs are equal; the entire equalized-odds gap comes from false positives. Group A is flagged incorrectly more often.

## 7. (1 point)

The three criteria constrain the same confusion matrices from different directions. When prevalence differs, matching all three would require the groups' score distributions to satisfy conditions that generally cannot hold for a non-trivial classifier. Kleinberg et al. show the incompatibility for calibration and balance; Chouldechova shows it for predictive parity and equal FPR. The practical consequence is that a metric choice is a policy choice about which error to equalize.

## 8. (1 point)

Query the endpoint at \(x = 0\) to obtain the intercept if the score is returned, then at each unit vector \(e_j\). If the endpoint returns \(c_j = w_j x_j\), the response at \(e_j\) is \(w_j\). Four queries recover the four weights; a fifth returns the intercept. If the endpoint returns only probabilities, invert with \(z = \log(p/(1-p))\) before subtracting. Top-\(k\) filtering raises the number of queries but can be defeated by isolating one feature at a time with scaled inputs.

## 9. (1 point)

The attacker solves

\[
x' = \arg\min_{x'} \|x' - x\| \quad \text{subject to} \quad f(x') = f(x) \ \text{and} \ E(x', f) \approx e_{\text{target}}.
\]

The constraint \(f(x') = f(x)\) keeps the model's decision unchanged; the constraint on \(E\) moves the explanation to the attacker's chosen feature. This is possible because the explanation is a function of the input and is not invariant across the decision boundary's neighborhood.

## 10. (2 points)

A scoped statement names the system, population, metrics, evidence, and limits. For example:

> On a synthetic evaluation of 360 rows (214 in group 0, 146 in group 1), a reweighted logistic model reduced the equalized-odds gap from 0.1231 to 0.0930 while increasing the demographic-parity gap from 0.0013 to 0.0125 and reducing accuracy from 0.7528 to 0.7389; bootstrap intervals overlap. Explanation stability under Gaussian noise at \(\sigma=0.25\) was about 0.90 Spearman for both models, but fidelity, targeted manipulation, calibration, robustness, and privacy were not evaluated. The result applies to this model family and split, not to deployment in general.

"Fair" is replaced by named metrics and values. "Explanations are stable" is replaced by a method, a noise level, and a correlation. "Safe to deploy" is replaced by the list of things not tested.
