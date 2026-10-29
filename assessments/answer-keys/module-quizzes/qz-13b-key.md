# QZ-13B Answer Key — Module 13

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — sensitivity divided by ε

For the Laplace mechanism, the scale is $\Delta f / \varepsilon$, where $\Delta f$ is the sensitivity of the query under the chosen neighboring relation. More sensitivity needs more noise for the same ε; a smaller ε needs more noise for the same sensitivity.

- **A** and **C** affect sensitivity only through the query definition, not directly.
- **D** is an outcome, not an input to the mechanism.

Tag: M13 · LO-19 · Bloom 2 · D1.

## 2. B — distinguishability of neighboring outputs

ε bounds the multiplicative change in the output distribution when one neighboring record changes. It is a worst-case guarantee about distinguishability, not a statement about accuracy, query count, or model size.

- **A** is a utility claim; DP does not bound accuracy loss directly.
- **C** is a rate limit, which is a separate control.
- **D** is unrelated.

Tag: M13 · LO-19 · Bloom 2 · D1.

## 3. False

DP protects confidentiality: it limits what an output reveals about any one record. It does not validate the integrity of an update. A malicious client can still submit a poisoned update that shifts the global model; DP and robust aggregation address different threats and must be combined deliberately.

Tag: M13 · LO-19 · Bloom 2 · D1.

## 4. True

Under basic sequential composition, mechanisms applied to the same data have their ε values added (and δ values added for approximate DP). This is why a dashboard with many queries needs a total budget, not just a per-query number. Parallel composition can do better when the queries touch disjoint data.

Tag: M13 · LO-19 · Bloom 2 · D1.

## 5. Required elements (three facts)

Three of:

- **δ**, for approximate DP, and what it means;
- the **neighboring relation** (row add/remove, replace-one, or user-level) and the unit of privacy;
- the **mechanism and sensitivity assumption**, including clipping bounds;
- the **composition** across all releases and the number of queries;
- the **trust model**: central, local, or distributed noise;
- what the release covers and what it does not.

A bare "ε = 1" does not say whether it is one release or ten thousand training steps, row-level or user-level, or with what δ. Those differences change the risk.

Tag: M13 · LO-19 · Bloom 2 · D1.

## 6. Sensitivity = 0.016; Laplace scale = 0.04

For a mean over $n$ rows with each of $d$ features clipped to $[-1, 1]$, replacing one row changes each coordinate by at most $2/n$. The L1 sensitivity of the vector is:

$$\Delta f_1 = d \cdot \frac{2}{n} = 4 \cdot \frac{2}{500} = \frac{8}{500} = 0.016.$$

Laplace scale:

$$b = \frac{\Delta f_1}{\varepsilon} = \frac{0.016}{0.4} = 0.04.$$

If the implementation adds independent noise per coordinate, the accounting and the norm used must match that design; the vector L1 calculation above is the conservative scalar-release view.

Tag: M13 · LO-19 · Bloom 3 · D2.

## 7. Required elements (two flaws and why ε is not established)

Two of:

- **No clipping before the mean.** The sensitivity of an unbounded mean can be arbitrarily large; the stated ε has no basis.
- **The noise scale assumes sensitivity 1.** `1.0/0.5` is the scale for $\Delta f = 1$, not for this query. The actual sensitivity must be computed from the clipping bounds and the number of rows.
- **Post-noise clipping biases the release.** Clipping the noisy value changes the output distribution and can break the DP guarantee; clipping belongs before noise, on the input.
- **No δ or neighboring relation is stated.** The claim is incomplete even if the scale were correct.

The stated ε is not established because the mechanism's sensitivity is unknown and the noise scale does not match it. A correct implementation clips each feature, computes sensitivity for the mean, adds Laplace noise at $\Delta f/\varepsilon$, and releases without post-noise clipping.

Tag: M13 · LO-19 · Bloom 4 · D3.

## 8. Required elements (neighboring relation, sensitivity, budget, utility, limits)

A bounded design:

- **Neighboring relation:** row-level add/remove (or replace-one) on the synthetic dataset; state whether one person can contribute multiple rows.
- **Clipping and sensitivity:** clip each numeric feature to a stated range; for a mean over $n$ rows with $d$ features, sensitivity is $2d/n$ in L1; a count has sensitivity 1; a histogram bin count has sensitivity 1 under add/remove.
- **Budget:** choose a total ε (and δ if approximate) before releasing; allocate across the mean, two counts, and histogram using sequential composition; state whether any releases are disjoint and can use parallel composition. Record the running total.
- **Utility:** compare the noisy release with the non-private value on synthetic data, using an appropriate error metric (for example, mean absolute error for the mean and total variation for the histogram), and report uncertainty across seeds.
- **Limits:** DP is a worst-case guarantee under the stated neighboring relation and mechanism; it is not anonymity, and it does not prevent inference from external data. Small counts or histogram bins can still be sensitive, and the composition budget can be exhausted quickly. An empirical attack failing is not a proof of privacy, and the implementation must match the accounting assumptions.

The answer must name the mechanism and the accounting inputs, not just "add noise." "ε = 1" with no δ, relation, or composition is not auditable.

Tag: M13 · LO-19 · Bloom 5 · D3.
