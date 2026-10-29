---
title: Module 07 Exercises
---

# Module 07 Exercises

**Four exercises · about 45 minutes · one scenario**

These exercises test interpretation, not code copying. You may use a calculator or a short Python session. Write your answers in a notebook or a Markdown file; keep the numbers and the reasoning together.

---

## Exercise 1 — Read the extraction curve (10 minutes)

LAB-09 produced this table:

| Budget | Random fidelity | Active fidelity |
|---:|---:|---:|
| 50 | 0.7620 | 0.4793 |
| 100 | 0.7013 | 0.9227 |
| 200 | 0.6940 | 0.9280 |
| 500 | 0.8707 | 0.9753 |

1. Compute the change in fidelity between consecutive budgets for both strategies.
2. Compute the change per additional query for each interval.
3. At which interval does active selection gain the most per query? At which interval does random sampling lose fidelity?
4. A team can afford 100 queries at \$0.01 each. Which strategy would you recommend, and what would you warn them about?
5. Why is the random curve not monotone, and what should a report say about that?

---

## Exercise 2 — Precision at different base rates (10 minutes)

LAB-10's threshold attack has TPR = 0.228 at FPR = 0.05, and TPR = 0.074 at FPR = 0.01. Use

$$
\text{precision} = \frac{\text{TPR}\cdot\pi}{\text{TPR}\cdot\pi + \text{FPR}\cdot(1-\pi)}.
$$

1. Compute precision at the 5% FPR operating point for $\pi = 0.5\%$, $1\%$, $5\%$, $25\%$, and $50\%$.
2. At $\pi = 1\%$, how many records are flagged per true member found?
3. Compute precision at the 1% FPR operating point for $\pi = 1\%$ and $\pi = 50\%$.
4. A privacy officer asks: "If we flag someone, what is the chance we are right?" Which number do you give, and what else must you state?

---

## Exercise 3 — Scenario: the VitalCheck audit (15 minutes)

VitalCheck sells access to a hosted risk model trained on 50,000 patient records. The API returns **hard labels only**. Each account may submit 500 queries per day. Accounts require only an email address.

The vendor's audit reports:

> "A membership inference attack reached TPR 0.30 at FPR 0.02 on a balanced test set of 1,000 members and 1,000 nonmembers. Our privacy-safe mode returns labels and limits accounts to 100 queries per day, reducing the risk by more than half."

Your organization is considering the API for a candidate pool of 20,000 records, of which about 2% are expected to be members.

1. Separate the vendor's statement into the three attack questions from Lesson 07.1. Which question does the audit actually answer?
2. If the vendor's operating point transferred, what precision would you expect at 2% prevalence? Show the calculation.
3. Give two reasons the operating point may not transfer to your candidate pool.
4. The vendor's "privacy-safe mode" still returns hard labels. What residual attacks remain? Name two.
5. Recommend two controls — one at the interface and one organizational — and state one cost of each.
6. Write a six-sentence memo with: finding, evidence, impact at your base rate, limitation, recommendation, owner/review date.

---

## Exercise 4 — Is the reconstruction the record? (10 minutes)

A two-feature logistic model has $w = (2,1)$ and $b = -3$. The attacker targets confidence $c = 0.9$, so the logit target is $t = \log(0.9/0.1) = 2.1972$. The prior mean is $\mu = (0,0)$.

1. Compute the minimum-distance input
   $$
   x^{*} = \mu + \frac{t - (w\cdot\mu + b)}{\lVert w\rVert^{2}}w.
   $$
2. Verify that $f(x^{*}) = 0.9$.
3. Find a second input with $x_1 = 1.0$ that also produces confidence 0.9. (Use $2x_1 + x_2 - 3 = t$.)
4. In the Lesson 07.4 neural-network experiment, a training member at $(0.1884, 0.4645)$ has confidence 0.7262, while the class mean $(1.57, -0.09)$ has confidence 0.9903. What does this imply about using confidence as a membership score? Which LAB-10 result does it echo?
5. A colleague says, "The inversion recovered the training record." Give two reasons this claim is not supported.
6. Name one inversion defense and one cost of applying it.

---

## Self-assessment

| Criterion | Check |
|---|---|
| Every calculation shows numerator, denominator, and result | [ ] |
| Base rates are stated with every precision number | [ ] |
| The scenario separates extraction, membership, and inversion | [ ] |
| The memo contains a recommendation, an owner, and a review date | [ ] |
| The inversion answer distinguishes a representative from a record | [ ] |
| Limitations are specific to the experiment, not generic | [ ] |

Worked answers: [exercise-solutions.md](exercise-solutions.md).
