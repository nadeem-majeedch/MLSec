# Prerequisite Diagnostic (DIA-01)

| Field | Value |
|---|---|
| ID | DIA-01 |
| Purpose | Check the Python, ML, statistics, and security baseline before M04 |
| Items | 20 |
| Points | 20 (1 per item) |
| Time guide | 30 minutes |
| Pass for course readiness | 14/20 |
| Modules | M00–M04, with prerequisite material |
| Outcomes | LO-01, LO-02, LO-04, LO-05, LO-29 |
| Answer key | Separate file in the course repository: `assessments/answer-keys/diagnostic-key.md` |

## Instructions

Answer every item without notes, lesson pages, or an AI assistant. Write your reasoning for items 3, 5, 8, 10, 13, 15, and 20; a correct number with the wrong reasoning is a miss on those items. Calculators are allowed; the arithmetic is deliberately small.

Do not open the key until you have answered all 20 items. Record your answers in a separate file so you can compare them item by item.

## Section A — Python and tooling (5 points)

**1. [PRE · LO-01 · Bloom 2 · D1]** What does this print?

```python
row = [0]
grid = [row] * 3
grid[0][0] = 1
print(grid)
```

A. `[[1], [0], [0]]`  
B. `[[1], [1], [1]]`  
C. `[[0], [0], [0]]`  
D. It raises an error because lists cannot be repeated.

**2. [PRE · LO-01 · Bloom 2 · D1]** `X` is a NumPy array with shape `(6, 2)`. What is the shape of `X[mask]` when `mask` is a Boolean array with shape `(6,)` and exactly two entries are `True`?

A. `(6, 2)`  
B. `(2, 2)`  
C. `(2,)`  
D. `(6,)`

**3. [PRE · LO-01 · Bloom 3 · D2]** A DataFrame `orders` has one row per order and a column `customer_id`. A second DataFrame `customers` has exactly one row per customer. You merge them with `orders.merge(customers, on="customer_id", how="left")`. The result has more rows than `orders`. Give one plausible cause and state one check you would run before using the merged table for a per-order metric.

**4. [PRE · LO-01 · Bloom 3 · D2]** Why is `eval(user_input)` unsafe even when the input is expected to be a simple arithmetic expression such as `"2 + 2"`?

A. It is slower than `int()` for large numbers.  
B. It can execute arbitrary Python expressions, not only arithmetic, so a crafted input can call functions or access objects.  
C. It always returns a string, which breaks downstream numeric code.  
D. It cannot handle whitespace.

**5. [PRE · LO-01 · Bloom 2 · D1]** You call `np.random.default_rng(7)` twice, creating two separate generator objects. Do the two objects produce the same sequence of random numbers? State what happens if you instead reuse one generator object for two experiments without resetting it.

## Section B — ML fundamentals (5 points)

**6. [M02 · LO-01 · Bloom 3 · D2]** A test set has 500 rows: 25 positives and 475 negatives. A model predicts positive for 40 rows: 20 true positives and 20 false positives. Compute precision and recall. Show the numerator and denominator for each.

**7. [M02 · LO-01 · Bloom 2 · D1]** A model has ROC-AUC 0.86 and a Brier score of 0.31 on a balanced test set. Which statement is most defensible?

A. The model ranks cases reasonably well, but its probability estimates are poorly calibrated.  
B. The model cannot rank cases because the Brier score is above 0.25.  
C. ROC-AUC and the Brier score measure the same property, so one of the numbers is wrong.  
D. The model is well calibrated because ROC-AUC is above 0.8.

**8. [M02 · LO-01 · Bloom 3 · D2]** You have a training set, a validation set, and a test set. You try 30 decision thresholds on the validation set and choose the one with the best F1. You then report F1 on the test set. Explain why this is better than choosing the threshold on the test set, and name one remaining optimism in the reported number.

**9. [M02 · LO-01 · Bloom 2 · D1]** A fraud dataset has 1% positives. A model that predicts "not fraud" for every row reports 99% accuracy. What is its recall for the fraud class, and why is accuracy misleading here?

A. 99%; accuracy is always the best metric for fraud.  
B. 0%; accuracy is dominated by the majority class, so a useless model looks strong.  
C. 1%; accuracy equals the positive rate.  
D. 50%; the model is guessing.

**10. [M02 · LO-01 · Bloom 4 · D3]** A colleague reports a churn model with ROC-AUC 0.99. The top feature is `account_closed_date`, the split is random, and several customers have multiple rows. Name two distinct leakage risks and the check you would run for each.

## Section C — Statistics and math (5 points)

**11. [M02 · LO-01 · Bloom 3 · D2]** A disease has a 1% prevalence in a screening population. A test has 90% sensitivity and a 5% false-positive rate. Out of 10,000 people, how many true positives, false positives, and total positive tests do you expect? Compute the positive predictive value (precision).

**12. [M02 · LO-01 · Bloom 2 · D1]** Which statistic is most resistant to a single extreme outlier?

A. Mean  
B. Median  
C. Sum  
D. Range

**13. [M02 · LO-01 · Bloom 4 · D3]** A report says: "The 95% confidence interval for accuracy is [0.81, 0.87], so there is a 95% probability that the true accuracy lies in this interval." Is this interpretation correct for a conventional frequentist confidence interval? Explain in one or two sentences.

**14. [M04 · LO-05 · Bloom 2 · D1]** For the vector $\delta = (2, -5, 1)$, compute $\|\delta\|_\infty$ and $\|\delta\|_2$.

**15. [M02 · LO-05 · Bloom 3 · D2]** A logistic model outputs $p = 0.8$ for a row whose true label is $y = 1$. Using cross-entropy loss, compute $\partial L / \partial z$, where $z$ is the logit. Show the substitution.

## Section D — Security fundamentals (5 points)

**16. [M03 · LO-02 · Bloom 2 · D1]** Which sequence correctly distinguishes vulnerability, exploit, and risk?

A. Vulnerability: a weakness; exploit: a way to use it; risk: the likelihood and impact of harm.  
B. Vulnerability: an attacker; exploit: a weakness; risk: a patch.  
C. Vulnerability: a patch; exploit: a weakness; risk: an attacker.  
D. Vulnerability: the harm; exploit: the likelihood; risk: the weakness.

**17. [M03 · LO-02 · Bloom 2 · D1]** A valid user token has the `predict` scope. The user calls an administrative endpoint and receives a response. Which failure does this indicate?

A. Authentication failed.  
B. Authorization failed.  
C. The token expired.  
D. The network was unavailable.

**18. [M03 · LO-02 · Bloom 2 · D1]** Ransomware encrypts a hospital's stored scan files. Which element of the CIA triad is most directly harmed?

A. Confidentiality  
B. Integrity  
C. Availability  
D. Non-repudiation

**19. [M03 · LO-04 · Bloom 3 · D2]** An ML service uses one long-lived API key with full administrative scope for every client. Name two controls that would reduce the impact of a leaked key, and state what each control limits.

**20. [M03 · LO-29 · Bloom 4 · D3]** A person you do not know asks you to test their employer's production fraud API and says, "You have my permission; we do not need anything in writing." What is the correct response, and which three conditions are missing from the authorization?

## Scoring

| Score | Interpretation | Next action |
|---:|---|---|
| 18–20 | Strong baseline | Start M00; use the missed items as review targets |
| 14–17 | Ready with gaps | Start M00; review each missed domain before M04 |
| 10–13 | Partial baseline | Start the four-week recovery path in the [student guide](../../student-guide.md#baseline) alongside M00–M01 |
| 0–9 | Foundational gaps | Complete the recovery path before M02; do not start attack labs yet |

A domain score is the number correct in that section. A domain at 2/5 or below is the first thing to review, even if the total is above 14.

## What to revise after a miss

| Items | Domain | Revise |
|---|---|---|
| 1–5 | Python and tooling | M01.L1–L5; the mutability, Boolean indexing, merge, and RNG sections |
| 6–10 | ML fundamentals | M02.L1–L4; confusion matrices, calibration, leakage, and honest splits |
| 11–15 | Statistics and math | M02.L2–L3; base rates, intervals, norms, and the logistic gradient |
| 16–20 | Security fundamentals | M03.L1–L2 and M00.L3; CIA, authn versus authz, least privilege, rules of engagement |

Do not treat a missed item as a vocabulary problem until you have tried to re-derive the answer. Most misses in this diagnostic are model errors, not missing definitions.
