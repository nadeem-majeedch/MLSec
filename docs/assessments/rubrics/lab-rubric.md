# Standard Lab Rubric

| Field | Value |
|---|---|
| Applies to | LAB-01, LAB-01B, LAB-02–LAB-20 |
| Dimensions | Five |
| Total | 100 points |
| Completion | Every dimension at **Proficient (3)** or above |
| Companion | [Practical completion checklists](lab-completion-checklists.md) · [Lab catalog](../../lab-catalog.md) |

This rubric scores the artifact a lab produces, not how long it took and not whether the learner liked the exercise. Use the [completion checklists](lab-completion-checklists.md) to decide whether a lab is finished; use this rubric to decide how well it was done.

## 1. Dimensions

| Dimension | Weight | What it measures |
|---|---:|---|
| R1 Technical correctness | 30 | The code implements the named method and produces valid outputs |
| R2 Security reasoning | 25 | The threat model, metrics, and claims match the evidence |
| R3 Experimental method | 20 | Baselines, budgets, controls, and uncertainty are sound |
| R4 Reproducibility | 15 | Another learner can rebuild the result |
| R5 Communication and ethics | 10 | The report is decision-oriented, limited, and authorized |

Score each dimension 1–4. The weighted score is $\text{weight} \times \text{level} / 4$. A level of 3 earns 75% of the dimension's weight; a level of 4 earns all of it.

## 2. Descriptors

### R1 — Technical correctness (30)

| Level | Descriptor |
|---:|---|
| 4 | Implements the method correctly, passes every lab-specific check, handles the stated edge cases, and reports values within the documented tolerance. |
| 3 | Runs correctly and produces every required output; minor omissions or one small numerical deviation that does not change the conclusion. |
| 2 | Partially correct: the pipeline runs but a metric, denominator, split, or transformation is wrong, or a required output is missing. |
| 1 | Does not run, or the outputs are invalid, fabricated, or unrelated to the method. |

### R2 — Security reasoning (25)

| Level | Descriptor |
|---:|---|
| 4 | States the adversary, knowledge, access, and budget; ties each metric to the harm; reports baselines and limits; makes no claim beyond the tested condition. |
| 3 | Sound threat reasoning with a minor gap, such as an unstated assumption or a limit that is named but not explained. |
| 2 | Generic threats, metric–claim mismatch, or a conclusion that outruns the evidence. |
| 1 | No security reasoning, or reasoning that would support an unsafe or unlawful action. |

### R3 — Experimental method (20)

| Level | Descriptor |
|---:|---|
| 4 | Frozen baseline and data; matched budgets; controls or ablations; multiple seeds or intervals where the lab allows; confounders addressed. |
| 3 | A sound comparison with a stated baseline and budget; uncertainty is limited but acknowledged. |
| 2 | A single run, a confounded comparison, or a baseline that changes between conditions. |
| 1 | No baseline, no budget, or a comparison that cannot support any claim. |

### R4 — Reproducibility (15)

| Level | Descriptor |
|---:|---|
| 4 | Clean checkout reproduces the headline result from pinned dependencies and recorded seeds; the manifest matches; one command is documented. |
| 3 | Reproduces with small fixes such as an unstated package version or a manual step that is documented. |
| 2 | Missing steps, unpinned dependencies, or a result that depends on an undocumented local state. |
| 1 | Not reproducible, or the artifact does not correspond to the reported result. |

### R5 — Communication and ethics (10)

| Level | Descriptor |
|---:|---|
| 4 | Report is decision-oriented and concise; findings are ordered and costed; limitations and residual risk are explicit; authorized use and disclosure are stated. |
| 3 | Clear report with minor issues; ethics statement present and consistent with what was done. |
| 2 | Disorganized, overlong, or missing a safety or limitations statement. |
| 1 | Unsupported recommendations, unsafe conduct, or an ethics claim that contradicts the artifacts. |

## 3. Score sheet

| Dimension | Weight | Level (1–4) | Weighted |
|---|---:|---:|---:|
| R1 Technical correctness | 30 | | |
| R2 Security reasoning | 25 | | |
| R3 Experimental method | 20 | | |
| R4 Reproducibility | 15 | | |
| R5 Communication and ethics | 10 | | |
| **Total** | **100** | | |

## 4. What earns and loses points

| Earns credit | Does not earn credit |
|---|---|
| Counts with an explicit denominator | A percentage with no count or base set |
| A baseline at the same budget and data | Comparing a defense against a different model or split |
| An adaptive test after a static result | Calling a static result "robust" |
| A measured false-positive cost | Reporting only catches |
| A negative result with an interval | Omitting a failed attack |
| A residual-risk statement naming what remains | "No risks found" |
| A reproducible command and manifest | A notebook with saved outputs only |

## 5. Automatic fails

A lab is not complete, regardless of the dimension scores, if it:

- tests a third-party system without written authorization;
- uses real personal data, real credentials, or a real mailbox or network service;
- executes an untrusted serialized artifact outside the sandbox;
- fabricates, edits, or selectively reports results;
- presents an unsupported safety claim, such as "the model is secure" or "the defense is unbreakable."

## 6. Using the rubric for self-assessment

1. Complete the lab's eight checklist items first. A missing required item means the lab is unfinished, not "developing."
2. Score each dimension independently against the descriptor, not against effort.
3. Write one sentence of evidence per dimension: the artifact file, the metric, or the report section that supports the level.
4. If any dimension is below 3, fix that dimension before moving on. A high total with one dimension at 2 does not satisfy the completion rule.
5. Re-score only after the artifact is updated, not after rereading the descriptor.

The rubric is a self-assessment tool. It has not been psychometrically validated, and a score is not a grade or a certificate.
