# Module 13 Exercise Solutions

## Exercise 1 — Budget ledger

### 1. Total epsilon

\[
3(0.10) + 2(0.25) + 1(1.20) + 4(0.15)
= 0.30 + 0.50 + 1.20 + 0.60
= 2.60.
\]

### 2. Budget position

The plan is over budget by

\[
2.60 - 2.00 = 0.60.
\]

The overrun is not spread evenly: training alone consumes 1.20, and the four dashboard refreshes consume 0.60. The countable releases are individually small but add up.

### 3. A feasible allocation

One option keeps training at 1.20, cuts the cohort counts to 0.05 each, keeps one mean-age query at 0.25, and keeps two dashboard refreshes at 0.20 each:

| Release | Epsilon each | Count | Subtotal |
|---|---:|---:|---:|
| Cohort counts | 0.05 | 3 | 0.15 |
| Mean age | 0.25 | 1 | 0.25 |
| Model training | 1.20 | 1 | 1.20 |
| Dashboard refresh | 0.20 | 2 | 0.40 |
| **Total** | | | **2.00** |

This meets the stated constraints exactly. It trades count precision and two refreshes for the training budget. A second option reduces training to 1.00, keeps all three count releases at 0.10, one mean-age query at 0.25, and three refreshes at 0.15, for a total of \(0.30 + 0.25 + 1.00 + 0.45 = 2.00\). The point of showing two allocations is that the choice is explicit, not that either is uniquely correct.

### 4. "Different seed" is not parallel composition

No. Parallel composition requires the queries to read **disjoint data**, not to use different randomness. Re-running the same cohort table with a new seed reads the same rows, so the results are sequential and the epsilons add. Randomness does not create new data.

### 5. Why a ledger

A per-query epsilon is a property of one release. A ledger records the cumulative spend across releases, the relation, and the remaining budget. It is what lets a reviewer answer "how much privacy has this cohort already lost?" and prevents an analyst from spending the same budget repeatedly by treating each query as the first.

---

## Exercise 2 — Sensitivity and noise

### 1. Sensitivity

\[
\Delta_1 = \frac{2Bd}{n} = \frac{2 \times 4.0 \times 3}{800}
= \frac{24}{800} = 0.03.
\]

### 2. Laplace scale

At \(\varepsilon = 0.5\),

\[
b = 0.03 / 0.5 = 0.06.
\]

At \(\varepsilon = 0.05\),

\[
b = 0.03 / 0.05 = 0.60.
\]

A tenfold smaller epsilon means tenfold more noise.

### 3. Cohort of 400

\[
\Delta_1 = \frac{24}{400} = 0.06, \qquad b = 0.06 / 0.5 = 0.12.
\]

Halving the cohort doubles both sensitivity and noise. Small cohorts are expensive under row-level DP: each row has more influence, so each row must be hidden by more noise.

### 4. Bound of 6.0

\[
\Delta_1 = \frac{2 \times 6.0 \times 3}{800} = \frac{36}{800} = 0.045,
\qquad b = 0.045 / 0.5 = 0.09.
\]

The noise scale rises from 0.06 to 0.09, a 50% increase, for the same epsilon. A larger bound reduces clipping bias but weakens the privacy–utility trade-off at a fixed budget. The trade-off should be evaluated, not assumed.

### 5. Bound versus observed maximum

The sensitivity calculation must hold for **any** neighboring dataset, including one where a row sits at the bound. The observed maximum in this sample is not a bound on the next sample, and an attacker may know the bound. Using the observed maximum would understate sensitivity and invalidate the accounting. The bound is a public parameter of the mechanism; the observed clipped fraction (here 0.02) is a utility diagnostic, not a privacy parameter.

---

## Exercise 3 — Designing an honest empirical audit

### 1. Three weaknesses

- **Low power.** 1,300 rows, one score, and a centroid statistic produce sampling noise around AUC 0.5 of roughly ±0.03; a real but small signal would be invisible.
- **Weak attack.** A distance score is not the strongest membership test; shadow models and likelihood-ratio attacks can extract more.
- **One release, one seed.** No repeats, no interval, no check that the test detects leakage when it is present.

### 2. Positive control

Configuration: a small synthetic dataset (for example 100 rows per class) with a unique canary row placed in one class, a clipping bound large enough that the canary is not clipped, and a release at very large epsilon (for example \(\varepsilon = 100\)) so the centroid is nearly exact. Include a matched control row that is **not** in the release set.

Expected result: a targeted canary score — for example, the projection of a candidate row onto the direction from the class centroid to the canary — should rank the canary above the matched control, giving an AUC well above 0.5. The exact value depends on the design; the requirement is that it is clearly separable, not a specific number.

What failure means: if the audit cannot detect a canary that is nearly exactly present in the release, the audit has no demonstrated power, and its "no leakage" result on the real release is uninformative. Fix the attack or the sample size before interpreting the null result.

A weaker positive control — simply releasing an unnoised centroid and expecting a high AUC — may also fail, because the centroid distance signal is genuinely small. That failure is itself a lesson: "no signal" can be a property of the attack, not of the release.

### 3. Repeat structure

Run at least 10 seeds per epsilon. Report the mean AUC, a 95% interval (bootstrap or normal approximation), and the number of seeds in which AUC exceeded a pre-registered threshold. If the interval straddles 0.5, report "no signal detected at this power" — not "no leakage" and not "leakage present." Pre-register the threshold and the attack before looking at results.

### 4. Varying the nonmember distribution

Draw nonmembers from a shifted distribution — for example, a different clinic, a different age band, or a different feature scale. If AUC rises sharply, the test may be detecting the distribution shift rather than membership. That is a confound, not evidence of leakage. Report the matched and shifted results separately.

### 5. Decision rule

A usable rule:

> The audit passes only if (a) the positive control detects membership with AUC at least 0.70 in at least 9 of 10 seeds, and (b) the release's mean AUC is below 0.55 with an interval that excludes 0.60. A pass means the specified attack, at this sample size, did not detect membership beyond the threshold. It does not certify epsilon or rule out other attacks.

The rule is explicit about the attack, the power check, and the claim's limits. It still does not replace the formal accounting.

---

## Exercise 4 — Report critique

### 1 and 2. Problems and corrections

| Problem | Why it matters | Correction |
|---|---|---|
| Clipping bound chosen by test accuracy | The bound is data-dependent and tuned on the evaluation set; the reported accuracy is optimistic and the selection may consume budget | Choose the bound on validation data or account for selection; report the selection procedure |
| "Independent releases, total remains epsilon 3" | Daily releases on the same data compose sequentially, not in parallel | Total grows with the number of releases under sequential composition; report the per-release and cumulative budget |
| "AUC 0.51, so no membership leakage" | A single weak test cannot establish absence of leakage; low power looks like privacy | Report the test, its power, a positive control, and the residual uncertainty |
| "The model is private" | No unit, neighboring relation, composition, or scope | State row-level or client-level, the relation, delta's meaning, and what is covered |
| "Safe to deploy" | Privacy is one risk among many; deployment safety includes robustness, access control, and utility | Separate privacy from operational and security claims |
| Missing delta discussion | \(\delta = 10^{-5}\) permits a small failure probability; its meaning depends on the dataset size and threat model | State what delta permits and why the value was chosen |
| No utility baseline | 0.91 accuracy has no meaning without a non-private reference | Report the baseline and the utility cost |

### 3. Scoped rewrite

> Under row-level replacement in the training set, with per-example gradient clipping at \(C = 1\) and noise calibrated to \(\varepsilon = 3\), \(\delta = 10^{-5}\) per training run, the model achieves 0.91 test accuracy against a [baseline] non-private accuracy of [value]. The reported membership test (AUC 0.51) did not detect membership at the tested sample size; it is not a proof of privacy. The budget covers one training run only; daily retraining composes and is not included. The claim does not cover adaptive attackers, linkage with external data, or deployment risks outside privacy.

The bracketed baseline is deliberately left for the team to fill: a report that omits it cannot support a utility claim.

### 4. Missing documentation items

- The **unit of privacy** and the **neighboring relation** (row-level or client-level; add/remove or replace).
- The **composition method and cumulative budget** across daily releases.
- The **clipping bound selection procedure** and whether it was data-dependent.
- The **empirical audit design**: attack, sample sizes, seeds, positive control, and interval.
- The **utility baseline** and the evaluation split.
- The **owner and review date**, and the residual-risk list.

Any four of these would be enough to show the record is incomplete.
