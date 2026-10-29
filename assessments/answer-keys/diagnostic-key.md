# DIA-01 Prerequisite Diagnostic — Answer Key

**Do not read this file before attempting all 20 items.** The key explains the reasoning and the misconception behind each distractor. It is not a second lesson.

**Scoring.** One point per item. On items 3, 5, 8, 10, 13, 15, and 20, award the point only if the required elements are present; a correct number with the wrong justification is a miss. Total 20. Course-readiness pass: 14/20.

## Section A — Python and tooling

### 1. B — `[[1], [1], [1]]`

`[row] * 3` repeats the **same list object** three times, not three independent copies of its contents. `grid[0][0] = 1` mutates that shared object, so every position sees the change.

- **A** assumes the repetition copied the inner list. It does not; use `[row.copy() for _ in range(3)]` or `[[0] for _ in range(3)]`.
- **C** ignores the mutation entirely.
- **D** is false; list repetition is allowed.

Tag: PRE · LO-01 · Bloom 2 · D1.

### 2. B — `(2, 2)`

A one-dimensional Boolean mask of length 6 selects rows from the first axis. Two `True` entries select two rows; the two columns are preserved. The result is `(2, 2)`.

- **A** is the unindexed shape.
- **C** would require selecting a single column or using a mask that reduces both axes.
- **D** confuses row selection with column selection.

Tag: PRE · LO-01 · Bloom 2 · D1.

### 3. Required elements

Award the point for both:

1. **Cause:** `customers` is not unique on `customer_id` (duplicate customer rows), so a left merge matches one order to several customer rows and multiplies it. A stale or denormalized customer table can also do this.
2. **Check:** assert `customers["customer_id"].is_unique` before the merge, and compare `len(merged)` with `len(orders)`; investigate any increase. For a per-order metric, also confirm that each `order_id` appears once after the merge.

A answer that only says "duplicates" without naming the right-hand key or the check earns half credit at most; this diagnostic uses whole points, so treat it as a miss and review M01.L3.

Why the other common answer is incomplete: duplicate **orders** would already be a defect in `orders`, but the question states that the result grew after the merge, which points to the right-hand table or a key-normalization issue.

Tag: PRE · LO-01 · Bloom 3 · D2.

### 4. B

`eval` parses and executes a Python expression with the caller's globals and builtins available unless they are restricted. `"2 + 2"` is arithmetic, but `"__import__('os').system('...')"` is also an expression. Input validation that checks for "only numbers and operators" is easy to bypass and is not a sandbox.

- **A** is a performance claim, not a security property.
- **C** is false; `eval("2+2")` returns the integer `4`.
- **D** is false; whitespace is handled by the parser.

Use `ast.literal_eval` for literals, or a real parser with an allowlist, when the input must be data rather than code.

Tag: PRE · LO-01 · Bloom 3 · D2.

### 5. Required elements

Award the point for both:

1. **Yes.** Two separate `default_rng(7)` objects start from the same seed and produce the same sequence, assuming the same NumPy version and the same calls.
2. **Reusing one object continues the stream.** The second experiment starts where the first stopped, so it sees different numbers unless you re-instantiate the generator or reset it deliberately.

This is why a seed alone is not a reproducibility recipe: the **number and order of draws** matter. Record the generator type, seed, and draw sequence, or save the split indices.

Tag: PRE · LO-01 · Bloom 2 · D1.

## Section B — ML fundamentals

### 6. Required elements

- **Precision** = TP / (TP + FP) = 20 / (20 + 20) = **0.50**.
- **Recall** = TP / (TP + FN) = 20 / 25 = **0.80**.

The denominators are different: precision uses predicted positives (40); recall uses actual positives (25). A response that writes 20/40 and 20/25 but labels them backwards is a miss.

Tag: M02 · LO-01 · Bloom 3 · D2.

### 7. A

ROC-AUC measures ranking: the probability that a random positive is ranked above a random negative. The Brier score measures the accuracy of the probability values themselves. A model can rank well and still be badly calibrated (for example, it may output 0.9 for a group whose observed rate is 0.6). On a balanced set, a Brier score of 0.31 is weak evidence of calibration, not proof of a ranking failure.

- **B** confuses a calibration threshold with a ranking requirement; no universal 0.25 cutoff decides whether ranking works.
- **C** is false; discrimination and calibration are different properties.
- **D** is false; high AUC does not imply calibration.

Tag: M02 · LO-01 · Bloom 2 · D1.

### 8. Required elements

Award the point for both:

1. **Why validation is better:** the test set is not used to make the choice, so its score is not contaminated by the 30-way selection. Choosing on test makes the reported F1 optimistic because the winner was selected partly for test noise.
2. **Remaining optimism:** selecting the best of 30 thresholds on validation overfits the validation set (winner's curse); the test estimate is conditional on the selected threshold and may still be optimistic for the *procedure*. A finite test set also adds sampling error. Name either the selection bias or the lack of an interval.

A response that says "the test set is unbiased" without qualification is incomplete: the *threshold* was selected, so the procedure still carries selection variance.

Tag: M02 · LO-01 · Bloom 3 · D2.

### 9. B

A majority-class predictor has recall 0 for the fraud class: it never predicts fraud, so TP = 0 and TP / (TP + FN) = 0. Accuracy is 99% because 99% of rows are negative. Accuracy is dominated by the majority class and hides the total failure on the class that matters.

- **A** is wrong on both the recall value and the metric choice.
- **C** confuses accuracy with prevalence.
- **D** is wrong; the model is deterministic, not guessing.

Report precision, recall, PR-AUC, and a threshold chosen for the operating cost.

Tag: M02 · LO-01 · Bloom 2 · D1.

### 10. Required elements

Award the point for two distinct risks **and** a check for each:

| Risk | Check |
|---|---|
| **Post-outcome / temporal leakage:** `account_closed_date` is recorded when the account closes, which is the outcome or after it | Confirm the feature's availability at scoring time; remove it and re-evaluate on the same rows to isolate its contribution |
| **Group / entity leakage:** multiple rows per customer appear in both train and test | Split by `customer_id` with a grouped split; verify the customer sets are disjoint |
| **Duplicate leakage** (also acceptable) | Count exact duplicate rows and near-duplicates; deduplicate before splitting |

Two risks are required. A response that names only "overfitting" is not specific enough; overfitting is a consequence, not a leakage mechanism.

Tag: M02 · LO-01 · Bloom 4 · D3.

## Section C — Statistics and math

### 11. Required elements

- Diseased: $10{,}000 \times 0.01 = 100$.
- True positives: $100 \times 0.90 = 90$.
- Non-diseased: $10{,}000 - 100 = 9{,}900$.
- False positives: $9{,}900 \times 0.05 = 495$.
- Total positive tests: $90 + 495 = 585$.
- **PPV** = $90 / 585 \approx 0.1538$, about **15.4%**.

The point requires the counts and the ratio. A response that reports 90% sensitivity as the PPV has confused sensitivity with precision.

Tag: M02 · LO-01 · Bloom 3 · D2.

### 12. B — Median

The median depends on rank, not magnitude, so moving one observation to an extreme value changes it little or not at all. The mean, sum, and range all change with the outlier.

- **A** is pulled toward the outlier.
- **C** changes by the outlier's value.
- **D** is defined by the extremes, so it is maximally sensitive.

Tag: M02 · LO-01 · Bloom 2 · D1.

### 13. Required elements

**No.** A conventional 95% frequentist confidence interval is a statement about the **procedure**: if the study were repeated many times, about 95% of the intervals constructed this way would cover the fixed true value. It is not a 95% posterior probability that the true value lies in *this* interval. A Bayesian credible interval can support a probability statement, but only with a stated prior and model.

A response that says "the true value is either in it or not" captures the frequentist idea but should still name the repeated-sampling interpretation.

Tag: M02 · LO-01 · Bloom 4 · D3.

### 14. Required elements

- $\|\delta\|_\infty = \max(|2|, |-5|, |1|) = 5$.
- $\|\delta\|_2 = \sqrt{2^2 + (-5)^2 + 1^2} = \sqrt{4 + 25 + 1} = \sqrt{30} \approx 5.48$.

Both values are required. A response that gives only the L∞ value earns no point on this item.

Tag: M04 · LO-05 · Bloom 2 · D1.

### 15. Required elements

For binary cross-entropy with a logistic output,

$$
L = -[y\log p + (1-y)\log(1-p)], \qquad \frac{\partial p}{\partial z} = p(1-p),
$$

so

$$
\frac{\partial L}{\partial z} = p - y = 0.8 - 1 = -0.2.
$$

The negative sign means that increasing the logit would reduce the loss, which is the direction the training update should take. A response that writes $y - p = +0.2$ has the sign backwards.

Tag: M02 · LO-05 · Bloom 3 · D2.

## Section D — Security fundamentals

### 16. A

A **vulnerability** is a weakness (for example, an unauthenticated endpoint). An **exploit** is a technique or input that uses the weakness. **Risk** combines the likelihood of an adversary doing so with the impact. The three are related but not interchangeable.

- **B** turns the vulnerability into an attacker and the risk into a patch.
- **C** turns the vulnerability into a patch.
- **D** turns the vulnerability into the harm and the risk into the weakness.

Tag: M03 · LO-02 · Bloom 2 · D1.

### 17. B — Authorization failed

The token is valid, so authentication succeeded. The token lacks the scope required for the administrative endpoint, so the service should reject the request with 403 (or an equivalent authorization error). Receiving an administrative response instead means the service failed to enforce authorization.

- **A** would apply to a missing, malformed, or invalid token (401).
- **C** would also produce an authentication failure, not an authorization decision.
- **D** describes a transport failure, not an access-control result.

Tag: M03 · LO-02 · Bloom 2 · D1.

### 18. C — Availability

Encrypting stored files makes them unreadable to the hospital, which is an availability loss. Integrity is also affected because the files were modified, but the primary harm in the scenario is that the data cannot be used. Confidentiality would be the primary harm if the attacker read or exfiltrated the files without encrypting them.

- **A** is not the most direct harm; encryption can protect confidentiality rather than break it.
- **B** is a secondary effect.
- **D** concerns denying an action, which is not the scenario.

Tag: M03 · LO-02 · Bloom 2 · D1.

### 19. Required elements

Award the point for **two** controls with the dimension each limits:

| Control | What it limits |
|---|---|
| Per-client scoped tokens (least privilege) | The actions a leaked key can perform |
| Short expiry, rotation, and revocation | The time window in which a leaked key works |
| Per-client quotas and rate limits | The volume and cost of abuse |
| Network restriction, mTLS, or IP allowlisting | Where the key can be used from |
| Separate keys per environment and per tenant | Blast radius and cross-tenant access |

A response that says "use a strong key" or "add a firewall" without naming what is limited is too vague for the point. The question asks for impact reduction, not prevention of leakage.

Tag: M03 · LO-04 · Bloom 3 · D2.

### 20. Required elements

Award the point for the refusal **and** three missing conditions:

- **Correct response:** decline until the system owner (not only an employee) provides written authorization with a defined scope. "We trust you" is not authorization, and an employee may not have authority to permit testing.
- **Missing conditions (any three):** written permission from the owner; the exact system, environment, and boundaries; the time window; permitted techniques and explicit non-goals; data-handling and evidence rules; stop conditions and contacts; a disclosure path for any real vulnerability.

Also acceptable: a statement that production testing may affect real users and requires the owner's risk acceptance. A response that accepts because the requester is friendly, or that asks only for a promise not to sue, is a miss.

Tag: M03 · LO-29 · Bloom 4 · D3.

## Domain summary

| Section | Items | Points | A domain below 3/5 means |
|---|---|---:|---|
| Python and tooling | 1–5 | 5 | Review M01.L1–L5 before writing attack code |
| ML fundamentals | 6–10 | 5 | Review M02.L1–L4; the attack labs assume this |
| Statistics and math | 11–15 | 5 | Review base rates, intervals, norms, and the logistic gradient |
| Security fundamentals | 16–20 | 5 | Review M03.L1–L2 and the rules of engagement in M00.L3 |

## Interpretation notes for self-scoring

- A total of 14 or more means you can start M00 without a remedial detour. It does **not** mean you can skip M01 or M02; the diagnostic samples four domains with five items each.
- A domain score of 2/5 or lower is the priority, even if the total passes.
- If you missed items because of arithmetic rather than the concept, redo the calculation after reviewing; do not reread the whole module.
- If you missed items 3, 8, 10, 13, or 20, the gap is in reasoning about evidence. Those are the items most predictive of trouble in the labs, because they test whether a number or a claim is being interpreted correctly.
