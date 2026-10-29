# Answer Key — QZ-18

**Module 18 · 15 points**

Model answers are fuller than a passing response needs. Award partial credit for correct reasoning with different wording.

---

**1. (1 point) — B.**

B names a system, a control, a decision metric, and a cost constraint; it can be answered no. A and C are topics. D has a metric ("robustness") but no system, budget, or cost, so it cannot fail in a useful way.

---

**2. (2 points)**

Defects (any three):

- No system: "a local model" is not a system with a decision, data, and interfaces.
- No falsifiable question: "investigate" and "try several defenses" have no oracle.
- No budget or metric: no attack budget, base set, or success criterion.
- No threat model: no adversary profile, access, or objective.
- No traceability: attacks and defenses are not tied to risks or to each other.
- No data or compute plan: unknown whether it is feasible in 40 hours.

Rewrite, for example: "Does document provenance labeling plus a tool allowlist reduce successful indirect prompt injection below 0.10 in a local RAG assistant with 40 mock documents and two tools, without refusing more than 5% of benign queries, at a fixed attacker budget of one injected document per query?"

---

**3. (2 points)**

- **Gate failed:** M2 (baseline). The baseline was not frozen, hashed, or protected from changes; overwriting it means there is no fixed comparator.
- **Missing evidence:** the baseline metrics at the original threshold, the evaluation-set hash and split, a run record, and a clean-checkout reproduction. "Close" is not a measurement.
- **Before reporting:** restore or regenerate the baseline at the current threshold in a clean environment, confirm the split and hash, rerun the defense on the same frozen set, and report both with intervals. If the original baseline cannot be recovered, report the confound explicitly and do not present the 0.61→0.09 change as a controlled result.

---

**4. (1 point) — C.**

Model checkpoints and licensed datasets are large and may be restricted; commit the generator/checksum and download instructions instead. Exact requirements, the generator, and the manifest belong in the repository. Secrets and personal data are also never committed.

---

**5. (2 points)**

**Can conclude:** all three defense seeds (0.30, 0.42, 0.55) are below the baseline point estimate of 0.60; the mean defense ASR is 0.423, a reduction of about 0.18. The spread across seeds is 0.25, which is large.

**Cannot conclude:** that the reduction is statistically meaningful, because the baseline has only one seed and its run-to-run variance is unknown; that the defense is reliably below 0.60 in general; or that the mean is precise.

**Report:** the three defense values, their mean and range (or a bootstrap interval), the baseline as a single-seed estimate with an explicit caveat, and a plan to run baseline seeds. Do not report only the mean, and do not claim significance.

---

**6. (2 points)**

Problems (any three):

- The truncated axis (0.72–0.79) exaggerates a small difference.
- No uncertainty: no error bars, seeds, or n.
- The claim "improves robustness" names no metric, budget, baseline, or effect size.
- A bar chart is a poor choice for a narrow range; a dot plot or table is better.
- The caption lacks the evaluation set, budget, and seed count.

Rewritten claim, for example: "At ε = 4/255, defense D reduced ASR from 0.79 to 0.72 (mean of three seeds; range 0.70–0.74), with clean accuracy falling from 0.94 to 0.93." Caption: "ASR at ε = 4/255 for baseline and D; points are means over three seeds, bars show the range; 1,000-record frozen evaluation set; PGD, 40 steps, 10 restarts." Use a dot plot with a zero-based or clearly labeled broken axis, or a table.

---

**7. (1 point) — B.**

B states the budget, the denominator, and an upper bound. A and C generalize from a bounded test to a security claim. D is unfalsifiable. "0 of 200" does not prove zero risk; it bounds it.

---

**8. (2 points)**

| Item | Type | Reason |
|---|---|---|
| A | Construct | The metric may not measure the harm claimed |
| B | Internal | The comparison is confounded by a different split |
| C | External | Generalization beyond the dataset and model family is unknown |
| D | Statistical | The uncertainty does not separate the conditions |

(Accept "statistical" for D and "external" for C; the labels matter less than the reason.)

---

**9. (1 point) — C.**

C names what existing evaluations hold fixed, what is unknown when it is relaxed, and why it matters. A is a topic. B is almost certainly false and is not a gap statement. D is a motivation, not a question.

---

**10. (1 point) — B.**

Removing the evaluation-set hash removes the ability to know what was measured; if the data changes, the comparison is no longer controlled. A, C, and D reduce breadth and require disclosure, but the remaining claim can still be valid.

---

## Scoring

| Score | Interpretation |
|---:|---|
| 13–15 | Ready to start the capstone; review the missed item's lesson |
| 10–12 | Adequate; reread Lessons 18.2–18.3 before M2 |
| 6–9 | Reread Lessons 18.1–18.3 and redo the proposal and milestone exercises |
| 0–5 | Read the module in order; the capstone depends on scoping and evidence discipline |

Items 3 and 5 are the most common failures. If the reasoning was right but the required action was missing, award half.
