# Module 07 Exercise Solutions

**Worked answers with reasoning**

Numbers are rounded for display; keep more precision in intermediate steps if you recompute them.

---

## Exercise 1 — Read the extraction curve

### 1. Change between budgets

| Interval | Random change | Active change |
|---|---:|---:|
| 50 → 100 | 0.7013 − 0.7620 = **−0.0607** | 0.9227 − 0.4793 = **+0.4434** |
| 100 → 200 | 0.6940 − 0.7013 = **−0.0073** | 0.9280 − 0.9227 = **+0.0053** |
| 200 → 500 | 0.8707 − 0.6940 = **+0.1767** | 0.9753 − 0.9280 = **+0.0473** |

### 2. Change per additional query

| Interval | Queries added | Random per query | Active per query |
|---|---:|---:|---:|
| 50 → 100 | 50 | −0.0607 / 50 = **−0.001214** | 0.4434 / 50 = **+0.008868** |
| 100 → 200 | 100 | −0.0073 / 100 = **−0.000073** | 0.0053 / 100 = **+0.000053** |
| 200 → 500 | 300 | 0.1767 / 300 = **+0.000589** | 0.0473 / 300 = **+0.000158** |

### 3. Where the gains and losses are

- Active selection gains the most per query in the **50 → 100** interval: +0.008868 per query, about 167 times the random rate in the same interval.
- Random sampling **loses** fidelity in the 50 → 100 and 100 → 200 intervals. The loss is small per query but visible in the curve.
- Active selection's gain flattens after 100: +0.000053 per query from 100 to 200, then +0.000158 from 200 to 500.

### 4. Recommendation for 100 queries

At \$0.01 per query, 100 queries cost **\$1.00**.

- Active reaches **0.9227** fidelity.
- Random reaches **0.7013** at 100 and only **0.8707** at 500 (which would cost \$5.00).

Recommend active selection at 100 queries, with two warnings:

1. **Cold start.** The method needs enough seed data. At 50 queries, active lost badly (0.4793 versus 0.7620). The 100-query result depends on the 20-query seed and the entropy batches; a different seed sample could change it.
2. **One run.** The table is a single draw at seed 21. The 0.9227 should not be treated as an exact production prediction. Repeat across seeds before committing to a budget.

### 5. Why the random curve is not monotone

Each budget uses a different random subset of the 30,000-point pool. A forest trained on 100 points can land on a less representative sample than one trained on 50, especially when the data has five clusters and the budget is small. More queries do not guarantee a better surrogate in a single run.

A report should say: "This is one random draw; the curve is noisy at small budgets, and the 50-query value may be atypically high." Reporting only the smooth-looking active curve while omitting the random curve would hide the comparison that makes the result meaningful.

---

## Exercise 2 — Precision at different base rates

### 1. Precision at TPR 0.228, FPR 0.05

| $\pi$ | Numerator $0.228\pi$ | Denominator $0.228\pi + 0.05(1-\pi)$ | Precision |
|---:|---:|---:|---:|
| 0.005 | 0.00114 | 0.00114 + 0.04975 = 0.05089 | **0.0224** |
| 0.01 | 0.00228 | 0.00228 + 0.04950 = 0.05178 | **0.0440** |
| 0.05 | 0.01140 | 0.01140 + 0.04750 = 0.05890 | **0.1935** |
| 0.25 | 0.05700 | 0.05700 + 0.03750 = 0.09450 | **0.6032** |
| 0.50 | 0.11400 | 0.11400 + 0.02500 = 0.13900 | **0.8201** |

### 2. Flags per true member at $\pi = 1\%$

Precision 0.0440 means about **22.7 flagged records per true member found** (1 / 0.0440). In 10,000 candidates: 22.8 true flags and 495 false flags, or 517.8 flags total.

### 3. Precision at TPR 0.074, FPR 0.01

| $\pi$ | Calculation | Precision |
|---:|---|---:|
| 0.01 | 0.00074 / (0.00074 + 0.00990) | **0.0695** |
| 0.50 | 0.03700 / (0.03700 + 0.00500) | **0.8810** |

### 4. What to tell the privacy officer

Give the precision at the **deployment base rate**, not the TPR alone. At 1% prevalence and the 5% FPR operating point, a flag is correct about **4.4%** of the time. At 50% prevalence, the same flag is correct about **82%** of the time.

State alongside it:

- the operating point (TPR 0.228 at FPR 0.05);
- the assumed prevalence and how it was estimated;
- the cost of a false flag (review time, delayed service, reputational or legal harm);
- the uncertainty in the estimate (sample size, one split, one model);
- that stronger attacks were not tested.

"Chance we are right" is a posterior probability, and it depends on the prior. The TPR alone cannot answer the question.

---

## Exercise 3 — Scenario: the VitalCheck audit

### 1. Which question the audit answers

| Attack | Does the audit answer it? | Why |
|---|---|---|
| **Extraction** | No | No fidelity or task-accuracy measurement at any query budget |
| **Membership inference** | Yes, in part | TPR 0.30 at FPR 0.02 on a balanced membership test |
| **Inversion** | No | No reconstruction experiment; the API returns hard labels |

The audit's "risk" is membership risk. It says nothing measured about extraction or inversion.

### 2. Precision at 2% prevalence

$$
\text{precision} =
\frac{0.30 \times 0.02}{0.30 \times 0.02 + 0.02 \times 0.98}
=
\frac{0.006}{0.006 + 0.0196}
=
\frac{0.006}{0.0256}
\approx 0.2344.
$$

**23.4%.** In 20,000 candidates: 400 members and 19,600 nonmembers; $0.30 \times 400 = 120$ true flags and $0.02 \times 19{,}600 = 392$ false flags; 512 flags total. About **4.3 flags per true member**, and roughly three in four flags concern nonmembers.

### 3. Why the operating point may not transfer

Any two of:

- The audit used a **probability API**; VitalCheck returns **hard labels**. The score and therefore the TPR/FPR change.
- The audit's model and training data differ from the model your records would be tested against.
- The audit used a **balanced** 1,000/1,000 test; your pool has 2% members. Precision changes even if TPR and FPR do not.
- Nonmembers in your pool may come from a different population, changing the score distribution.
- The audit does not describe an **adaptive attacker** who knows the interface and the defense.
- The audit is vendor-produced; independence and reproducibility are not established.
- With 1,000 per group, the TPR and FPR estimates have sampling uncertainty.

### 4. Residual attacks with hard labels

Any two of:

- **Label-only extraction.** Each query still returns a labelled point; 500 per day is a usable collection rate.
- **Membership inference through stability.** Query near-duplicates or slightly perturbed inputs and measure whether the predicted label changes.
- **Boundary-distance probing.** Estimate how far a record is from the decision boundary using repeated queries.
- **Inversion by search.** Search for inputs that produce the target label; confidence is gone, but the label is still an objective.
- **Account farming.** Email-only accounts make the 500/day limit weak.

### 5. Two controls and their costs

| Layer | Control | Cost |
|---|---|---|
| Interface | Rate limits, anomaly monitoring, and account verification | Slower legitimate access; operational and log-privacy burden |
| Organizational | Contractual audit rights, data-processing terms, and an independent annual test | Legal time; vendor may pass the cost back |
| Training (alternative) | Differential privacy with a documented budget | Utility loss and training cost; needs expertise |

A correct answer names one interface and one organizational control and gives a real cost for each. "Add encryption" is not responsive: the attack uses the authorized interface.

### 6. Model memo

> **Finding.** VitalCheck's audit measures a membership-inference attack at TPR 0.30 and FPR 0.02, but only on a balanced test set and a probability API; it does not measure extraction or inversion.
>
> **Evidence.** If that operating point transferred to our 2% member prevalence, precision would be 23.4%: about 120 true and 392 false flags per 20,000 candidates.
>
> **Impact.** Roughly three of every four flags would concern nonmembers, so a flag cannot be treated as an individual accusation; each false flag carries review cost and privacy harm.
>
> **Limitation.** The vendor returns hard labels to us, our population differs from the audit's balanced set, and no adaptive attacker or defense was tested.
>
> **Recommendation.** Adopt the 100-query cap and add anomaly monitoring, require human adjudication before any member is treated as confirmed, and commission an independent test on our interface and population.
>
> **Owner and review.** Privacy engineering owns the assessment; review before contract signature and annually thereafter.

Six sentences is a format constraint, not a legal standard. The memo is decision-ready because it states the base rate, the residual uncertainty, and a next action.

---

## Exercise 4 — Is the reconstruction the record?

### 1. Minimum-distance input

$$
x^{*} = (0,0) + \frac{2.1972 - (2\cdot0 + 1\cdot0 - 3)}{2^2 + 1^2}(2,1)
= \frac{5.1972}{5}(2,1)
= (2.0789, 1.0394).
$$

### 2. Verification

$$
2(2.0789) + 1(1.0394) - 3 = 4.1578 + 1.0394 - 3 = 2.1972,
$$

and $\sigma(2.1972) = 1/(1+e^{-2.1972}) = 0.9$.

### 3. A second input with $x_1 = 1.0$

Solve $2(1.0) + x_2 - 3 = 2.1972$:

$$
x_2 = 2.1972 + 3 - 2 = 3.1972.
$$

So $(1.0, 3.1972)$ also has confidence 0.9. In general, every point with $x_2 = 5.1972 - 2x_1$ does.

### 4. What the member's confidence implies

The training member has confidence **0.7262**, lower than the class mean's **0.9903**. A record can be in the training set and still be less confident than a typical nonmember or a class representative. Confidence measures how typical or easy an input is for the model, not whether it was seen in training.

This echoes LAB-10: members are more confident *on average*, but the distributions overlap, the member training accuracy is 1.0 while TPR at 1% FPR is only 0.074, and confidence is not proof of membership.

### 5. Why "recovered the record" is unsupported

Any two of:

- **Underdetermination.** Infinitely many inputs produce confidence 0.9; the model alone does not select one.
- **The prior selects.** Changing the prior from the origin to a member changes the reported input; the output reflects the attacker's assumption.
- **The member is not returned.** A prior centered on the member produced $(0.44, 0.42)$, about 0.26 away, with confidence 0.8838 — not the member $(0.1884, 0.4645)$.
- **No identity evidence.** A representative that resembles a class is not evidence about a specific person's record.
- **Grid resolution and model family.** The result depends on the 0.02 grid, the MLP, and the training seed.

### 6. One defense and one cost

| Defense | Cost |
|---|---|
| Return hard labels instead of probabilities | Loses explanations, calibration diagnostics, and some downstream utility; label-only attacks remain |
| Round or add noise to confidence | Reduces precision and reproducibility; noise may be averaged out over repeated queries |
| Differential privacy in training | Utility and compute cost; privacy budget must be chosen and documented |
| Limit queries per account | Slows legitimate users; account farms remain |

Any one is acceptable with a concrete cost.

---

## Common errors in these exercises

| Error | Why it is wrong |
|---|---|
| Reporting TPR as "chance the flag is right" | TPR is conditional on membership, not on being flagged |
| Computing precision without $\pi$ | Precision is not identifiable from TPR and FPR alone |
| Treating random's non-monotone curve as a code bug | It is sampling noise in a single run; report it |
| Saying the inversion "found the member" | The optimization returns a point chosen by the prior and objective |
| Treating hard labels as eliminating membership risk | Stability, boundary, and repeated-query attacks remain |
| Writing a memo with no owner or date | A finding without an action is not a decision document |
