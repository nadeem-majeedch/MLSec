# Module 12 Exercise Solutions

## Exercise 1 — FedAvg arithmetic and influence

### 1. Sample-weighted mean

Multiply each update by its row count:

| Client | Weighted contribution |
|---|---|
| C1 | \(300(0.2,-0.1) = (60,-30)\) |
| C2 | \(500(0.4,0.2) = (200,100)\) |
| C3 | \(400(-0.2,0.3) = (-80,120)\) |
| C4 | \(600(0.1,0.0) = (60,0)\) |
| C5 | \(200(0.6,-0.4) = (120,-80)\) |
| C6 | \(400(-0.1,0.2) = (-40,80)\) |

The sum is \((320,190)\), and the total row count is 2,400. The weighted mean is

\[
(320/2400,\ 190/2400) = (0.1333,\ 0.0792).
\]

### 2. C5 scaled by 6

C5's contribution becomes \(6(120,-80) = (720,-480)\). The new sum is

\[
(320,190) - (120,-80) + (720,-480) = (920,-210),
\]

so the aggregate is

\[
(920/2400,\ -210/2400) = (0.3833,\ -0.0875).
\]

The first coordinate nearly triples, and the second changes sign.

### 3. Effective share

C5 holds 200 of 2,400 rows, a sample weight of \(200/2400 = 0.0833\). Scaling by 6 makes its effective weight \(6 \times 0.0833 = 0.50\). The other weights sum to \(1 - 0.0833 = 0.9167\), so the total effective weight is \(1.4167\) and C5's share is

\[
0.50 / 1.4167 = 0.3529.
\]

The equal-weight approximation \(6/(5+6) = 0.5455\) overstates the share here because C5 has fewer rows than average. The exact share depends on the other clients' sample weights. The point stands: one client with one twelfth of the data controls more than a third of the aggregate direction.

### 4. Controls

- **Sample-count influence:** cap and audit the declared row count; do not let a client's self-reported count determine its weight without a bound.
- **Update-magnitude influence:** norm clipping or a per-coordinate bound limits the scaled magnitude.
- **Identity influence:** participation caps limit how many contributions one principal can make.

### 5. Why "one sixth of the vote" is wrong

FedAvg is not one-client-one-vote. Weight is proportional to the declared sample count, and the submitted update's magnitude is not normalized. C5's 200 rows give it less sample weight than C2's 500, but its 6× scale more than compensates. The effective share is a product of sample weight and update magnitude, not a headcount.

---

## Exercise 2 — Backdoor design and evaluation

### 1. Why the update can preserve clean performance

The poisoned copies are a subset of the client's rows and share the same clean features, with a small trigger added and the label changed. The local model can fit both the clean mapping and the trigger-target mapping. On clean inputs the trigger is absent, so the learned trigger association does not fire. The update can therefore look reasonable on a clean holdout while carrying a strong trigger response.

### 2. Three evaluation rows

| Evaluation | Metric | Expected difference |
|---|---|---|
| Untouched test set | Clean accuracy | Similar for clean and backdoored models; not discriminating alone |
| Triggered non-target rows | Attack success rate | Near the benign floor for a clean model; near 1.0 for a backdoored one |
| Target-class clean rows | Target-class accuracy | A model that over-predicts the target may show inflated target recall and lower precision |

A fourth useful row is a trigger-specific false-positive check on clean rows that already contain the trigger pattern by coincidence. It estimates how often the trigger fires without an attack.

### 3. Monitoring signals

Before the trigger is known:

- update norm relative to the cohort;
- cosine similarity to the cohort median;
- reference-set loss or per-class accuracy of the client's update;
- participation and sample-count anomalies;
- trigger scans if any triggers are known.

The signal that cannot flag the client before the trigger is known is a trigger-specific scan. By definition, it needs the trigger.

### 4. Why the current model still needs evaluation

- The malicious client has participated in previous rounds; the global model may already contain the backdoor.
- Other clients may have copied or adapted the malicious update, or the attacker may have multiple identities.
- The current model is what would be deployed if the team retrains from scratch only for future rounds.

Evaluate the current model on the clean and triggered sets, and roll back only if the previous checkpoint passes the same gate.

### 5. Rare trigger and clean accuracy

A clean-accuracy gate averages over the test distribution. If the trigger appears in 0.1% of clean rows, even a perfect trigger response changes clean accuracy by at most about 0.001 if those rows flip. That is inside the noise of most comparisons. The gate must include deliberately triggered rows and per-class checks, not only the natural distribution.

---

## Exercise 3 — Choosing an aggregation rule

### 1. Statistics

Sorted: \(0.2,\ 0.3,\ 0.5,\ 0.6,\ 0.7,\ 0.8,\ 1.0,\ 4.0\).

- Mean: \(8.1/8 = 1.0125\).
- 1-trimmed mean: remove 0.2 and 4.0; average \(0.3,0.5,0.6,0.7,0.8,1.0\) = \(3.9/6 = 0.65\).
- Median: average the two middle values, \((0.6+0.7)/2 = 0.65\).

### 2. Krum with \(K=8\)

\(2m+3 \le 8\) gives \(m \le 2.5\), so the largest integer is \(m=2\). Each score uses \(K-m-2 = 8-2-2 = 4\) nearest neighbors.

### 3. Krum with six clients and two colluders

The condition is \(K \ge 2m+3\). With \(K=6\) and \(m=2\),

\[
2(2)+3 = 7 > 6.
\]

Krum's stated condition is not satisfied, so its guarantee does not apply. A trimmed mean with \(m=2\) requires \(2m<K\), which holds (\(4<6\)), but it trims four of six values per tail, leaving only two. That is a fragile configuration and a large utility risk.

### 4. Scenario choices

**A. One million mobile clients, weak identity, 200 sampled.**

Choose a coordinate median or a small-trim trimmed mean computed over the sampled clients, plus identity enrollment and participation caps. Krum's \(O(K^2d)\) cost and its dependence on a benign cluster are poor fits for a weak-identity, high-churn population. Residual risk: Sybil identities within the sample and non-IID benign extremes.

**B. Six hospitals, two possibly colluding, strong identity.**

A coordinate median is the most defensible of the simple rules, because trimming with \(m=2\) leaves only two values and Krum's condition fails. Add contracts, audit, and per-client monitoring. Residual risk: coordinate-wise majority can still be moved in a correlated direction, and two colluders are a large fraction of six.

**C. 100 clients, 50 million weights, one suspected attacker.**

A trimmed mean with small \(m\) is plausible, or clipping plus the mean if compute is tight. Krum's pairwise distances over 50 million weights are expensive, and a coordinate median ignores weight correlations. Residual risk: the attacker can spread a small shift across coordinates, and the accuracy cost of trimming is unknown.

**D. Adaptive attacker who knows the rule.**

No fixed rule is sufficient by itself. Use a layered design: identity and participation limits, clipping, a robust rule, trigger-aware evaluation, and monitoring. Test the defense against an attacker optimized for it. Residual risk: the attacker may still find an accepted update that preserves the backdoor.

### 5. Coordinate-wise median limitation

The median is computed independently per coordinate. It ignores correlations, so the resulting vector need not resemble any client's update or a plausible model direction. In high dimensions, an attacker can shift many coordinates slightly and move the vector while each coordinate remains near its median. Robustness per coordinate is not robustness of the model.

---

## Exercise 4 — Evaluation critique

### 1. Four problems

- **Different training budgets:** 40 rounds versus 10.
- **No attacker model:** trigger, target, scale, and fraction are unspecified.
- **No fixed setup:** partition, client population, seed, and evaluation set are unspecified.
- **Misleading utility claim:** 0.88 is compared with 0.90, but the benign reference is 0.92, so the cost is 0.04, not "negligible." The comparison also reports no per-class or client-level results.
- A fifth problem is that the robust run and the baseline may use different data or evaluation rows.

### 2. Relative reduction and attribution

The vendor's reduction is

\[
(0.40 - 0.02)/0.40 = 0.95 = 95\%.
\]

It cannot be attributed to the aggregator because the robust run trained four times as long. Longer training can strengthen or weaken a backdoor, and it changes clean accuracy independently of robustness. The comparison has at least two variables.

### 3. What a valid comparison needs

At minimum:

1. the same client population and partition;
2. the same number of rounds;
3. the same local epochs, learning rate, and regularization;
4. the same attacker, trigger, target, and scale;
5. the same evaluation rows and ASR definition;
6. the same seed or a reported range over seeds;
7. clean accuracy and ASR for benign, attack, and each defense;
8. clip or trim settings and client exclusion counts.

### 4. Residual-risk sentence

"An attack success rate of 0.02 means that 2 in 100 triggered rows were still classified as the attacker's target in this evaluation; the rate is a residual, not a zero, and it is measured only for the reported trigger and attacker."

### 5. Scoped assurance statement

Example:

> In the vendor's reported configuration — six clients, one malicious client, a feature-based trigger targeting class 1, a 4× update scale, and 40 rounds — the robust aggregator produced clean accuracy 0.88 and attack success 0.02, compared with 0.90 and 0.40 for plain FedAvg after 10 rounds and 0.92 and 0.01 for benign training. Because the round counts differ and the attacker is underspecified, the 95% relative reduction cannot be attributed to the aggregator. The result does not establish robustness at equal rounds, against two colluding clients, against an adaptive attacker, or for a different trigger, model, or data partition.

The statement reports the numbers, names the confound, and lists what remains unknown.
