---
title: Module 05 Exercises
---

# Module 05 Exercises

**Four exercises · about 60 minutes · Complete after Lessons 1–4**

Write your work in `work/m05/`. These exercises ask you to interpret curves, audit an experiment, and make a defense trade-off. You do not need to write a new attack from scratch; you do need to show the arithmetic.

| Exercise | Focus | Time | Deliverable |
|---|---|---:|---|
| 1 | Read the poisoning curve | 15 min | `curve.md` |
| 2 | Audit a broken experiment | 15 min | `audit.md` |
| 3 | Scenario: GrantGate data supply chain | 20 min | `grantgate.md` |
| 4 | Choose a screening threshold | 10 min | `threshold.py`, note |

---

## Exercise 1 — Read the poisoning curve

**Goal.** Turn a table into a claim about marginal cost.

**Data.** LAB-05 reference results:

| Rate | Poisoned rows | Accuracy |
|---:|---:|---:|
| 0.00 | 0 | 0.9667 |
| 0.05 | 63 | 0.9648 |
| 0.10 | 126 | 0.9389 |
| 0.20 | 251 | 0.8870 |
| 0.30 | 377 | 0.7981 |

**Tasks.**

1. Compute the accuracy drop from the clean model at each rate, in percentage points.
2. Compute the **average drop per 1 percentage point of poison** at each rate (drop ÷ rate in percent). Then compute the **marginal** drop per 1 point between consecutive rates. Which interval has the largest marginal cost?
3. Is the curve linear, convex, or concave over this range? Support your answer with two of the numbers from task 2.
4. A colleague says, "The model tolerates 10% poisoning; accuracy is still 93.9%." Give two reasons this sentence is incomplete. One reason must be about what accuracy does not measure; the other about the experiment's scope.
5. If you wanted to make the attack look strongest, which rate would you report? If you wanted it to look weakest? Explain why choosing the rate after seeing the results is a reporting problem, even when every number is correct.

**Deliverable.** `work/m05/curve.md` with the table extended by your computed columns.

**Success criteria.** Drops are in percentage points (not fractions); marginal and average costs are distinguished; the shape claim is supported by numbers; the answer to task 5 names the selection bias, not just "it is misleading."

---

## Exercise 2 — Audit a broken experiment

**Goal.** Find the errors that make a poisoning result invalid or unreproducible.

**Scenario.** A team reports:

> We flipped 10% of the dataset: 180 labels out of 1,800 total rows (1,260 training, 540 test). We changed labels in both splits so the experiment would be consistent. We then trained on the original training labels to isolate the poisoning effect and measured 93.9% test accuracy. That is a 2.8-point drop, so the model is vulnerable at a 10% poison rate. The result has a 95% confidence interval of ±0.1.

**Tasks.**

1. Identify **four** flaws. For each, state what the code or protocol did, why it invalidates or weakens the result, and what should have been done.
2. Compute the correct number of poisoned rows for a 10% rate against the 1,260 training rows, and compute the rate implied by 180 poisoned training rows.
3. Is "a 2.8-point drop" consistent with fitting on the original labels? Explain.
4. Rewrite the paragraph as a report of a valid experiment. You may choose the rate and the result, but the numbers must be internally consistent.
5. The team says "the model is vulnerable." What additional experiment would you require before using that word in a deployment decision?

**Deliverable.** `work/m05/audit.md`.

**Success criteria.** Four distinct flaws, each with a consequence and a fix; the two rate calculations are correct; the rewrite never poisons the test set and never fits on clean labels; the extra experiment is about a targeted attack or a realistic threat model, not another random seed.

---

## Exercise 3 — Scenario: GrantGate's data supply chain

**Goal.** Build a poisoning threat model for a system with several data entry points, then choose the experiment that would most change a decision.

**Scenario.** GrantGate is a fictional grant-triage system:

- Applicants submit profiles through a public form (education, publications, budget, institution).
- Two reviewers label each application "fund" or "decline."
- A gradient-boosted model ranks applications for a program officer.
- The officer's decisions become labels for quarterly retraining.
- A vendor supplies a historical decisions batch from another agency.
- Support staff can correct labels in the console.
- An audit team receives a monthly export of decisions.

**Tasks.**

1. List at least five data entry points and, for each, the access level from Lesson 1 (label only, feature and label, row insertion, pipeline, model update).
2. Build a threat model table with at least five threats. Columns: goal (availability / targeted integrity / conditional), access, budget, knowledge, success metric, lifecycle stage.
3. Choose the threat you would test first. Justify the choice with two criteria: feasibility and harm. Do not choose "most likely" without saying likely for whom.
4. Design the smallest experiment that would tell you whether the threat is real. State the data, the attack, the budget, the metric, and one thing the experiment cannot show.
5. Name two controls and one cost of each. At least one control must act before training, not after.
6. State one finding that would lower your ranking of the threat and one that would raise it.

**Deliverable.** `work/m05/grantgate.md`.

**Success criteria.** The access levels are correct for each entry point; at least one threat uses the feedback loop; the experiment has a stated budget and metric; each control has a real cost; the ranking can change with evidence.

---

## Exercise 4 — Choose a screening threshold

**Goal.** Make a defense trade-off explicit instead of declaring "the screen works."

**Data.** From the LAB-06 screen (350 clean training rows, 30 poisons):

| τ | Flagged | Poisons caught | Clean flagged | Target prediction | Accuracy |
|---:|---:|---:|---:|---:|---:|
| 0.50 | 50 | 24 | 26 | 0 | 0.8800 |
| 0.60 | 67 | 30 | 37 | 1 | 0.8900 |
| 0.70 | 90 | 30 | 60 | 1 | 0.8900 |
| 0.80 | 116 | 30 | 86 | 1 | 0.8800 |

**Tasks.**

1. Compute recall, false-positive rate (clean flagged ÷ 350), and precision at τ = 0.5, 0.6, and 0.8. Report four decimals.
2. A team can afford to lose at most 12% of clean training rows. Which thresholds satisfy the constraint? Which one would you choose, and why?
3. A regulator requires at least 95% of poisons to be caught. Which thresholds satisfy that? Does satisfying it guarantee the target decision recovers? Use the table.
4. τ = 0.7 has the same recall as τ = 0.6 and a higher target probability. Why is it not automatically the better choice?
5. Write two sentences a security reviewer could accept: one stating the chosen threshold, one stating what the choice assumes.

**Deliverable.** `work/m05/threshold.py` and a short note.

**Success criteria.** All three metrics are correct; the 12% constraint is applied in rows, not guessed; the recall question is answered with the target column; the final sentences name the threshold and the trust assumption.

---

## Portfolio checklist

- [ ] `curve.md` with drop, average cost, and marginal cost columns
- [ ] `audit.md` with four flaws, correct rates, and a valid rewrite
- [ ] `grantgate.md` with five entry points and five threats
- [ ] `threshold.py` with recall, FPR, and precision at three thresholds
- [ ] Five-line reflection: which result surprised you, which assumption is weakest, what you would test next

Then run [LAB-05](../../labs/lab-05.md) and [LAB-06](../../labs/lab-06.md) if you have not already. The labs produce the artifacts; these exercises produce the interpretation.
