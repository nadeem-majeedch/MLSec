# Knowledge Check Answers — QZ-13

**Module 13 · 10 items · 15 points**

## 1. (1 point) — B

Row-level neighbors differ in one row: one row is replaced, added, or removed, depending on the relation the release defines. "Same distribution" (C) is a statistical property, not a neighboring relation. The relation must be stated, because epsilon means nothing without it.

## 2. (2 points)

For a mean over \(n\) clipped rows in \(d\) dimensions, changing one row changes each coordinate by at most \(2B/n\), so

\[
\Delta_1 = \frac{2Bd}{n} = \frac{2 \times 2.5 \times 6}{1000} = \frac{30}{1000} = 0.03.
\]

The Laplace scale is

\[
b = \frac{\Delta_1}{\varepsilon} = \frac{0.03}{0.6} = 0.05.
\]

So each released coordinate receives noise with mean 0 and scale 0.05. Doubling \(n\) would halve both the sensitivity and the noise.

## 3. (2 points)

Sequential: the four count queries compose by addition,

\[
\varepsilon_{\text{seq}} = 4 \times 0.2 = 0.8.
\]

Parallel: the two disjoint datasets each spend 0.3, and the total for that stage is the maximum,

\[
\varepsilon_{\text{parallel}} = \max(0.3, 0.3) = 0.3.
\]

The two stages are sequential with each other, so the total is

\[
0.8 + 0.3 = 1.1.
\]

Parallel composition is not a discount on arbitrary queries: it requires the datasets to be disjoint, and it does not apply across stages that read the same data.

## 4. (1 point) — B

Clipping bounds how much one row can move the statistic. That bound is the sensitivity, and the sensitivity sets the noise scale. Without clipping, one unbounded row can force an unusable amount of noise. Clipping does bias the statistic when values exceed the bound; that bias is a utility cost, not a privacy guarantee.

## 5. (2 points)

The numbers show a clear monotone trade-off on this task. At \(\varepsilon = 0.02\) the Laplace scale is 2.4 on features clipped to width 5, so the released centroids are almost pure noise: test accuracy 0.5233 is near the 0.5 chance level, and the mean centroid error is 4.3642. At \(\varepsilon = 0.5\) the scale is 0.096, the error falls to 0.3257, and accuracy rises to 0.7833. The no-noise baseline is 0.8233.

The interpretation: more privacy (smaller epsilon) costs utility here, and the cost is steep at very small epsilon. The result is for one seed, one centroid release, and one dataset. It does not establish a general curve, and it does not show that \(\varepsilon = 0.5\) is "acceptable" without a utility requirement and a privacy requirement to compare against.

## 6. (2 points)

It supports: on this release, with this distance score, this sample of members and nonmembers, and this seed, the test did not rank members above nonmembers beyond a small margin. AUC 0.5308 is close to chance.

It does not support:

- that no attacker can learn membership — the test is one weak attack, not the definition of DP;
- that the release satisfies any particular epsilon for a different mechanism, dataset, or neighboring relation;
- that repeated releases would remain at this level — composition would add budget.

A low-power test and a strong guarantee can produce the same AUC.

## 7. (1 point)

In local DP, each data subject (or client) adds noise to its own value before sending it to the curator. The curator never sees the raw value, so the guarantee does not depend on trusting the curator. The cost is usually much more noise for the same epsilon, because each contribution is protected separately rather than in aggregate.

## 8. (1 point)

No. Secure aggregation hides individual updates from the server while allowing the sum to be computed, so it protects against a curious server during aggregation. The aggregate itself is still released and can leak information; secure aggregation is a cryptographic complement to DP, not a substitute for it, and it does not stop poisoning.

## 9. (1 point)

Epsilon is defined relative to a mechanism and a neighboring relation. The first report's epsilon may rely on a different relation, a different query, or an analysis that does not bound sensitivity at all; the clipped mean's epsilon depends on the bound \(B\), the dimension, and the row count. The symbol is shared, the definitions are not. Compare the full records — relation, sensitivity, mechanism, composition, and total budget — not the epsilon alone.

## 10. (2 points)

A scoped answer names the object, the unit, the mechanism, the budget, the utility, and the limits. For example:

> For a single release of per-class centroid summaries computed from 500 synthetic rows per class, with features clipped to \([-3, 3]\) and row-level replacement as the neighboring relation, the release satisfies \(\varepsilon = 0.5\) with \(\delta = 0\). Nearest-centroid test accuracy is 0.7833 against a 0.8233 no-noise baseline. A distance-based membership test found no signal beyond chance (AUC 0.5308). The claim does not cover repeated releases, adaptive attackers, linkage with external data, or any model trained with DP-SGD.

The original claim fails on four counts: "private" has no unit or relation, "the dashboard" is broader than the measured object, "safe to share" mixes privacy with other risks, and no budget or repetition is stated.
