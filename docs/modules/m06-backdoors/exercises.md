---
title: Module 06 Exercises
---

# Module 06 Exercises

**Four exercises · about 50 minutes · Complete after Lessons 1–4**

Write your work in `work/m06/`. Each exercise asks for a judgment supported by numbers. Compare with the [solutions](exercise-solutions.md) after a first attempt.

| Exercise | Focus | Time | Deliverable |
|---|---|---:|---|
| 1 | Audit backdoor metrics | 10 min | `metrics.md` |
| 2 | Trigger design trade-offs | 15 min | `triggers.md` |
| 3 | Scenario: a vendor model and a fine-tuning set | 20 min | `vendor.md` |
| 4 | Decide from a trigger scan | 10 min | `scan.py`, note |

---

## Exercise 1 — Audit backdoor metrics

**Goal.** Separate the attack effect from the raw ASR.

**Data.**

| Lab | Clean accuracy | Backdoored accuracy | Clean-model ASR | Backdoored ASR |
|---|---:|---:|---:|---:|
| LAB-07 (tabular) | 0.8444 | 0.8306 | 0.1771 | 0.8571 |
| LAB-08 (images) | 0.9907 | 0.9722 | 0.0000 | 0.9818 |

Training sizes: LAB-07 has 840 clean rows and 67 poisons; LAB-08 has 249 clean rows and 20 poisons.

**Tasks.**

1. Compute the **attack effect** as the increase in ASR over the clean-model baseline for each lab. Report it in percentage points.
2. Compute the poison rate for each lab against the clean training set.
3. Compute the clean-accuracy drop for each lab.
4. Which lab demonstrates the backdoor more cleanly? Use the baseline and the clean-accuracy numbers in your answer. Name one reason the other lab is still a valid demonstration.
5. A colleague writes: "LAB-07 has 85.7% ASR, so the model is 85.7% compromised." Identify two errors in that sentence.

**Deliverable.** `work/m06/metrics.md`.

**Success criteria.** The attack effect is an increase, not the raw ASR; rates use the clean training size; the comparison names the baseline; the two errors are distinct (one about the baseline, one about what ASR measures).

---

## Exercise 2 — Trigger design trade-offs

**Goal.** Reason about the attacker's trigger choices and the defender's detection surface.

**Candidates.**

| ID | Trigger | How it is applied |
|---|---|---|
| A | 3 tabular features = 3.0 | Set three features to an extreme value |
| B | 1 tabular feature = 2.0 | Set one feature just below the LAB-07 screen threshold |
| C | 2×2 white patch at a fixed location | Stamp four pixels to 1.0 |
| D | +0.05 brightness on every pixel | Add a small constant to all inputs |
| E | Rare phrase in a text field | Insert a fixed 3-word phrase |

**Tasks.**

1. For each candidate, rate **effectiveness** (how strongly it can shift a decision), **stealth** (how hard it is for a human or a simple check to notice), and **detectability** by the defenses in this module (feature thresholds, patch scans, input filtering). Use high/medium/low and one sentence of justification.
2. Rank the candidates for an attacker who wants a reliable conditional behavior with a small budget. State your ranking criterion.
3. Rank them for a defender who can only inspect data and run one trigger scan. Which candidate is hardest to cover, and why?
4. Candidate D adds a small constant to every pixel. Explain why "small per pixel" does not mean "small overall," using an L2 argument. (An 8×8 image has 64 pixels.)
5. A defender says, "We scan for 2×2 white patches, so C is covered." What does that claim assume about the attacker?

**Deliverable.** `work/m06/triggers.md`.

**Success criteria.** Ratings are justified, not asserted; the attacker and defender rankings can differ; the L2 answer uses the number of pixels; the final answer names the fixed shape/location assumption.

---

## Exercise 3 — Scenario: the vendor model and the fine-tuning set

**Goal.** Design a verification plan for a backdoor risk that may enter through the supply chain.

**Scenario.** TerraTriage is a fictional wildfire-risk system. A vendor supplies:

- a pretrained image model for vegetation and terrain;
- a 20,000-row fine-tuning set with labels;
- a monthly updated checkpoint.

Your team adds local weather features, fine-tunes the model, and deploys a risk score to dispatch crews. Local incident reports become future labels. The vendor signs each checkpoint but does not share training data or code.

**Tasks.**

1. List five entry points for a backdoor and classify each by access: training data, labels, fine-tuning, weights, pipeline, or update.
2. Design a verification plan with at least four tests. For each test, state what it measures, what it cannot show, and its cost.
3. Write a deployment decision rule with three outcomes: deploy, deploy with monitoring, or reject. State the evidence thresholds you would use; if you cannot set a number, say what data you need first.
4. Name two controls that act **before** the model is trained or deployed, and one that acts after. Give a cost for each.
5. Write a residual-risk statement in two sentences. It must mention a trigger family the plan does not cover.
6. The vendor offers a "backdoor-free" certification based on clean accuracy. Explain why that certification is not sufficient, in two sentences.

**Deliverable.** `work/m06/vendor.md`.

**Success criteria.** The entry points include at least one non-data path; each test has a stated limitation; the decision rule is actionable; the residual risk names a real uncovered family; the certification critique distinguishes clean accuracy from conditional behavior.

---

## Exercise 4 — Decide from a trigger scan

**Goal.** Turn scan scores into a decision, using the clean model as a control.

**Data.** LAB-08 scan over 49 positions on the backdoored model, with the clean model's score at the same positions:

| Position | Backdoored score | Clean score | Excess |
|---|---:|---:|---:|
| (6, 6) | 0.8884 | 0.0443 | ? |
| (2, 2) | 0.7938 | 0.6866 | ? |
| (4, 2) | 0.7049 | 0.6268 | ? |
| (5, 2) | 0.5900 | 0.5113 | ? |

**Tasks.**

1. Compute the excess (backdoored − clean) for each row, to four decimals.
2. Compute the raw-score margin between rank 1 and rank 2, and between rank 1 and rank 3.
3. If a defender thresholds on **excess** at 0.50, how many positions are flagged? At 0.10? Which rule recovers the true patch with the fewest candidates?
4. If a defender thresholds on **raw score** at 0.80, which positions are flagged? What does the clean column tell you about the risk of that rule on a clean model?
5. The defender does not know the true patch in advance. Name one additional check that would distinguish the true patch from a high-scoring false candidate.
6. Write a two-sentence conclusion that states the detected position, the evidence, and one limitation.

**Deliverable.** `work/m06/scan.py` and a short note.

**Success criteria.** Excess values are correct; raw and excess thresholds are distinguished; the additional check is feasible with the lab's access; the conclusion includes a limitation.

---

## Portfolio checklist

- [ ] `metrics.md` with attack effects, rates, and drops
- [ ] `triggers.md` with justified ratings and an L2 argument
- [ ] `vendor.md` with five entry points and four tests
- [ ] `scan.py` with excess values and two threshold rules
- [ ] Five-line reflection: which defense assumption is weakest, what you would test next, which claim you would refuse to sign

Then run [LAB-07](../../labs/lab-07.md) and [LAB-08](../../labs/lab-08.md) if you have not already. The labs produce the artifacts; these exercises produce the judgment.
