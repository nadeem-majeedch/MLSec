# QZ-07B Answer Key — Module 07

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. C — the full probability vector

A hard label carries one bit of supervision per query; a ranked list without scores carries ordering but no margin; the full probability vector carries the model's confidence over every class, which supports distillation, margin-based membership scores, and inversion objectives. That is why output minimization reduces, but does not eliminate, the information channel.

- **A** and **B** reveal less per query.
- **D** reveals metadata, not model behavior on inputs.

Tag: M07 · LO-12 · Bloom 2 · D1.

## 2. A — a representative input for a class

Inversion searches for an input that the model scores highly for a chosen class, subject to a prior or regularizer that keeps it plausible. It can resemble a prototypical or even a memorized training record, but the output is not proof that any specific record was used.

- **B** is membership inference's question, and even there the answer is probabilistic.
- **C** is extraction.
- **D** is not produced by inversion; labels may inform the search but are not recovered as a set.

Tag: M07 · LO-15 · Bloom 2 · D1.

## 3. False

Fidelity measures agreement with the teacher on a query distribution. A surrogate can reach high fidelity without seeing a single training record, and high fidelity does not prove the training data was copied. It may still enable transfer attacks and business harm, which is a separate claim from data theft.

Tag: M07 · LO-13 · Bloom 2 · D1.

## 4. True

Privacy harm depends on how many nonmembers are falsely implicated at a usable detection rate. A classifier can have high overall accuracy and still be useless at a 1% false-positive budget. TPR at fixed low FPR describes the operating point a real attacker or auditor would use; overall accuracy averages over thresholds and hides the tail.

Tag: M07 · LO-14 · Bloom 2 · D1.

## 5. Required elements (two defenses with costs)

Any two pairs, such as:

| Defense | Benign cost |
|---|---|
| Rate limits and quotas | Legitimate heavy users are delayed or blocked; capacity planning becomes harder |
| Output rounding or top-k only | Reduced utility, calibration loss, and worse performance for legitimate downstream use |
| Query perturbation or noise | Inconsistent answers and lower accuracy for all users |
| Watermarking or fingerprinting | Fidelity or utility loss, false-accusation risk, and no prevention of extraction |
| Monitoring and account anomaly detection | False positives against legitimate users, analyst workload, and additional data collection |

A defense without a cost earns half credit at most; "use encryption" is not an extraction defense.

Tag: M07 · LO-13 · Bloom 3 · D2.

## 6. TP = 30; FP = 18; precision = 0.625

- Members: $0.10 \times 1000 = 100$. True positives: $0.30 \times 100 = 30$.
- Nonmembers: 900. False positives: $0.02 \times 900 = 18$.
- Precision: $30/(30+18) = 30/48 = 0.625$, or **62.5%**.

At 1% prevalence: 10 members give $0.30 \times 10 = 3$ true positives; 990 nonmembers give $0.02 \times 990 = 19.8$ false positives; precision is $3/(3+19.8) \approx 0.132$, or about **13.2%**. TPR and FPR are properties of the test, but precision depends on prevalence: the same test is far less trustworthy when members are rare.

Tag: M07 · LO-14 · Bloom 3 · D2.

## 7. Required elements (two flaws and the rule)

Two of:

- **`argmax(tpr)` selects the loosest threshold.** TPR is nondecreasing as the threshold loosens, so the maximum TPR usually occurs at FPR near 1.0. The printed pair is not at the 1% budget.
- **There is no FPR constraint.** The code never selects among points with `fpr <= 0.01`.
- **There is no baseline or uncertainty.** A TPR without a random or untrained-model baseline and without an interval is not interpretable.
- **Reversing or misordering the curve** can produce a TPR that is not achievable at the stated FPR; the selection must respect the curve's ordering.

Corrected rule: among all returned points with $\text{FPR} \le 0.01$, choose the one with the largest TPR (the last eligible point on the increasing curve), and report the actual FPR at that point. If no point qualifies, report that the budget is not achievable rather than relaxing it silently.

Tag: M07 · LO-14 · Bloom 4 · D3.

## 8. Required elements (metric, baseline, and limits per attack, plus two limits)

A bounded plan:

| Attack | Metric | Baseline |
|---|---|---|
| Extraction | Fidelity to the teacher at fixed query budgets (for example 100, 500, 1,000), plus task accuracy | A surrogate trained on random or unqueried data, or fidelity at zero queries; report each budget separately |
| Membership inference | TPR at FPR ≤ 1% and ≤ 5%, plus precision at the stated prevalence | A random scorer or a score that ignores the model; report the candidate pool and its member prevalence |
| Inversion | Reconstruction error or class score under a stated prior, with a qualitative check of whether the result resembles a representative or a specific record | The same objective on a model trained without the target record, or a random-input baseline |

Two limits:

- The assessment runs on a local replica with synthetic records. Results may not transfer to the production model, its real data distribution, or its actual query controls.
- The attacker is one configuration on one split. A stronger adaptive attacker, auxiliary data, or shadow models could do better; the reported numbers are lower bounds for those attackers, not upper bounds on risk.
- Inversion output is not proof that a specific patient's record was memorized; it must be described as a representative or a candidate, not as a recovered record.
- No real patient data may be used, and the production service must not be queried.

The plan must name a metric, a baseline, and a limit for each attack; a list of techniques without measurements is not an assessment.

Tag: M07 · LO-12 · Bloom 5 · D3.
