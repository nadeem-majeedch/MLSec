# Lesson 13.2 — Differential Privacy from First Principles

<a id="m13-l2"></a>

**Module 13 · Lesson 2 of 5 · 2 hours · LO-19**

## Scenario

A public-health team wants to publish the number of patients in each of 40 age-by-region cells. The smallest cells contain one or two people. Suppressing them is visibly inconsistent, and an analyst can reconstruct some suppressed values from the published totals. The team asks for "enough noise to be safe" without a definition of safe.

Differential privacy replaces the intuition with a bound. This lesson defines the bound, derives the noise for simple queries, and applies it to the centroid release in LAB-17.

## Objectives

By the end of this lesson you will be able to:

1. State the definition of \(\varepsilon\)-differential privacy and explain each term.
2. Distinguish add/remove and replace-one adjacency, and bounded and unbounded DP.
3. Compute the L1 sensitivity of a count, a sum, and a clipped centroid.
4. Apply the Laplace mechanism and compute its noise scale.
5. Explain the Gaussian mechanism and the role of \(\delta\).
6. Interpret epsilon without treating it as a probability.

## 1. The definition

A randomized mechanism \(M\) is \(\varepsilon\)-differentially private if, for every pair of neighboring datasets \(D\) and \(D'\) and every set of outputs \(S\),

\[
\Pr[M(D) \in S] \le e^{\varepsilon}\,\Pr[M(D') \in S].
\]

For approximate DP, add a failure term:

\[
\Pr[M(D) \in S] \le e^{\varepsilon}\,\Pr[M(D') \in S] + \delta.
\]

Read the definition one clause at a time.

| Term | Meaning | Common misreading |
|---|---|---|
| Randomized mechanism | The output is a random variable, not a fixed value | "Add noise once and it is private" |
| Neighboring datasets | Two datasets that differ in one unit | "Any two datasets" |
| Every set \(S\) | The bound holds for all output events | "The average output is close" |
| \(e^\varepsilon\) | A multiplicative bound on probability ratios | "Epsilon is the probability of leakage" |
| \(\delta\) | A small probability that the bound fails | "Delta can be ignored" |

The guarantee is about the **distribution** of outputs, not about any single output. After you see a noisy count, you cannot tell whether it came from \(D\) or \(D'\) with confidence better than the bound allows. This is why post-processing is free: any function of a DP output is still bounded by the same ratio.

### What epsilon does not mean

- It is not the probability that a record is identified.
- It is not a percentage of data revealed.
- It is not comparable across mechanisms without the same adjacency and composition assumptions.
- A smaller epsilon is stronger, but "strong enough" is a policy decision tied to harm and auxiliary knowledge.

A useful intuition: \(\varepsilon = 1\) permits a probability ratio of \(e \approx 2.72\); \(\varepsilon = 0.1\) permits about 1.105. The ratio compounds across releases.

## 2. Neighboring datasets and the unit

The definition is parameterized by what "neighboring" means.

| Adjacency | \(D\) and \(D'\) differ by | Unit protected | Typical use |
|---|---|---|---|
| Add/remove | One record added or removed | One person | Unbounded DP; dataset size varies |
| Replace-one | One record replaced by another | One person | Bounded DP; fixed size |
| Client add/remove | One client's entire dataset | One client | Federated or cross-silo |
| Group | Up to \(k\) records | A group | Group privacy, weaker bound |

The choice changes the sensitivity and the guarantee. A claim of "\(\varepsilon = 1\)" without the adjacency is incomplete. LAB-17 uses replace-one with a fixed release size per class, so the clipped centroid's sensitivity is computed for one replaced row.

**Bounded versus unbounded.** Bounded DP assumes a fixed dataset size and measures replacement. Unbounded DP allows the size to change and measures add/remove. The two can be related, but the constants differ. Record which one you use.

## 3. Sensitivity

The global L1 sensitivity of a query \(f\) is

\[
\Delta_1 f = \max_{D \sim D'} \|f(D) - f(D')\|_1.
\]

It is the largest change one unit can cause, measured in L1. Sensitivity is a property of the query and the adjacency, not of the data instance.

| Query | Adjacency | Sensitivity | Why |
|---|---|---|---|
| Count of rows | Add/remove one | 1 | The count changes by at most 1 |
| Sum of a value in \([0,1]\) | Add/remove one | 1 | One value contributes at most 1 |
| Mean of \(n\) values in \([0,1]\) | Replace one, fixed \(n\) | \(1/n\) | One value changes the mean by at most \(1/n\) |
| Histogram with \(d\) bins | Add/remove one | 1 in L1 | One row changes one bin by 1 |
| Clipped centroid, \(d\) features, \(n\) rows | Replace one, fixed \(n\) | \(2Bd/n\) | Each coordinate changes by at most \(2B/n\); sum over \(d\) |

If a query has unbounded range, its sensitivity is infinite and the Laplace mechanism cannot be applied directly. Clipping bounds the range and makes the sensitivity finite. That is why clipping is not an optional preprocessing step; it is part of the privacy proof.

### LAB-17's sensitivity

Each class has \(n = 500\) release rows and \(d = 4\) features. Each feature is clipped to \([-B, B]\) with \(B = 3\). Replacing one row changes each coordinate of the centroid by at most

\[
\frac{2B}{n} = \frac{6}{500} = 0.012.
\]

Summing the absolute changes over four coordinates gives

\[
\Delta_1 = \frac{2Bd}{n} = \frac{2 \cdot 3 \cdot 4}{500} = 0.048.
\]

This is the value recorded in `metrics.json`. The implementation computes it from the same constants, so the report and the mechanism cannot drift apart silently.

## 4. The Laplace mechanism

For a numeric query \(f\) with L1 sensitivity \(\Delta_1\), the Laplace mechanism releases

\[
M(D) = f(D) + (Y_1,\dots,Y_d),
\]

where each \(Y_j \sim \operatorname{Laplace}(0, b)\) and

\[
b = \frac{\Delta_1}{\varepsilon}.
\]

It satisfies \(\varepsilon\)-DP (with \(\delta = 0\)).

**Proof sketch.** The Laplace density at \(x\) with scale \(b\) is proportional to \(e^{-|x|/b}\). For two inputs whose query values differ by at most \(\Delta\) in one coordinate, the ratio of densities at the same output is at most

\[
e^{|\Delta|/b} = e^{\varepsilon}.
\]

The product over independent coordinates preserves the bound. The full proof handles the multidimensional case with the L1 sensitivity.

### Worked example

A count query has \(\Delta_1 = 1\). With \(\varepsilon = 0.5\),

\[
b = 1 / 0.5 = 2.
\]

The released count is \(f(D) + \operatorname{Laplace}(0,2)\). The noise has standard deviation \(\sqrt{2b^2} = 2.83\). A single release can be several counts away from the truth; that is the utility cost of the guarantee.

If the same query is released at \(\varepsilon = 4.0\), the scale is \(0.25\) and the noise is much smaller. The guarantee is weaker because the ratio bound is \(e^4 \approx 54.6\).

### The scale is not the error

The Laplace scale \(b\) is a distribution parameter, not a bound on the error. A draw can exceed \(b\), and the guarantee does not promise that any single release is close. It promises that the output distribution is close across neighboring inputs. Utility statements require a separate argument, such as a confidence interval for the noise.

## 5. The Gaussian mechanism

The Gaussian mechanism adds noise from \(\mathcal{N}(0,\sigma^2)\) to each coordinate. For L2 sensitivity \(\Delta_2\) and \(\varepsilon \in (0,1)\), choosing

\[
\sigma \ge \frac{\Delta_2 \sqrt{2\ln(1.25/\delta)}}{\varepsilon}
\]

gives \((\varepsilon,\delta)\)-DP. The \(\delta\) term is necessary because the Gaussian tail is unbounded; there is a small probability that a noise draw is too small to hide the change.

| Mechanism | Noise | Guarantee | Sensitivity | When to use |
|---|---|---|---|---|
| Laplace | Laplace | Pure \(\varepsilon\)-DP | L1 | Simple numeric queries, strict \(\delta=0\) |
| Gaussian | Gaussian | Approximate \((\varepsilon,\delta)\)-DP | L2 | Vector queries, DP-SGD, composition-friendly analyses |

A nonzero \(\delta\) must be reported and justified. A common policy is \(\delta \ll 1/n\), so that the failure probability is much smaller than the chance that any one person is in the dataset. The exact rule is organizational; the requirement to state it is not.

## 6. Post-processing and composition

Two properties make DP usable.

**Post-processing.** If \(M\) is \(\varepsilon\)-DP, then any function \(g(M(D))\) is also \(\varepsilon\)-DP. You can normalize, threshold, plot, or feed the output to another model without spending more budget. You cannot use the data again inside \(g\); only the released output is protected.

**Composition.** If \(M_1\) is \(\varepsilon_1\)-DP and \(M_2\) is \(\varepsilon_2\)-DP on the same data, the pair is \((\varepsilon_1+\varepsilon_2)\)-DP under basic sequential composition. Lesson 13.3 covers parallel composition and tighter accounting.

Composition is why a release is never "one epsilon" forever. Each query, each monthly statistic, and each training run spends budget.

## 7. Applying it to LAB-17

The lab's mechanism is a per-class centroid release:

1. Clip each feature to \([-3,3]\).
2. Compute the mean centroid for each class.
3. Add Laplace noise to each coordinate with scale \(0.048/\varepsilon\).
4. Release the two noisy centroids.

At \(\varepsilon = 0.5\), the scale is \(0.096\). At \(\varepsilon = 0.02\), it is \(2.4\). The noise is visible in the released centroids and in the utility curve.

The lab uses parallel composition because the two class datasets are disjoint and fixed-size. The total epsilon is the per-class epsilon, not twice it. If the classes overlapped or the mechanism were applied sequentially to the same rows, the accounting would differ.

## 8. Common pitfalls

| Pitfall | What goes wrong | Fix |
|---|---|---|
| Choosing noise without sensitivity | The guarantee is invalid | Compute \(\Delta\) from the query and adjacency |
| Clipping after computing the mean | The bound does not apply | Clip rows before aggregation |
| Forgetting that \(n\) is public | Sensitivity uses \(n\) | State whether \(n\) is fixed and public |
| Treating \(\varepsilon\) as a probability | The guarantee is misread | Explain the ratio and the composition |
| Ignoring \(\delta\) | The claim is incomplete | Report and justify it |
| Releasing the same query repeatedly | Budget composes | Track cumulative spend |
| Applying post-processing with raw data | It is no longer post-processing | Use only the released output |

## Check your understanding

1. Write the definition of \(\varepsilon\)-DP and explain the role of \(e^\varepsilon\).
2. What is the L1 sensitivity of a count query under add/remove adjacency?
3. A clipped centroid has \(B=2\), \(d=5\), \(n=200\). Compute \(\Delta_1\).
4. With \(\Delta_1 = 0.05\) and \(\varepsilon = 0.25\), what is the Laplace scale?
5. Why does the Gaussian mechanism need a nonzero \(\delta\)?
6. What does post-processing allow, and what does it not allow?
7. Why is LAB-17's total epsilon equal to the per-class epsilon?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- DP bounds the ratio of output probabilities for neighboring datasets.
- The unit and adjacency define what is protected; state them.
- Sensitivity is the maximum change one unit can cause.
- The Laplace mechanism uses scale \(\Delta_1/\varepsilon\) and gives pure DP.
- The Gaussian mechanism uses L2 sensitivity and gives approximate DP with \(\delta\).
- Clipping makes sensitivity finite and is part of the proof.
- Post-processing is free; composition is cumulative.
- LAB-17's centroid sensitivity is \(2Bd/n = 0.048\).

## Next

Continue to [Lesson 13.3 — Composition, budgets, and noisy releases](lesson-3-composition-budgets-and-noisy-releases.md), where multiple releases are accounted for.
