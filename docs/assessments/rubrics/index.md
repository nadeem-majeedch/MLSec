# Rubrics and Practical Evidence

These tools score artifacts, not answers. They are the assessment layer for the labs, the applied projects, RT-01, and the capstone. A quiz can show that you recognize a mistake; a rubric asks whether the artifact avoids it.

| Tool | Applies to | Total | Completion rule |
|---|---|---:|---|
| [Standard lab rubric](lab-rubric.md) | LAB-01, LAB-01B, LAB-02–LAB-20 | 100 | Every dimension at 3 or above |
| [Practical completion checklists](lab-completion-checklists.md) | 21 labs, 8 checks each | Pass/fail | All required checks have evidence |
| [Project and RT-01 rubric](project-rubric.md) | PRJ-01…PRJ-06, RT-01 | 100 | All dimensions at 2+, at least six at 3 |
| [Capstone self-scoring rubric](capstone-rubric.md) | CAP-A…CAP-F | 100 | Every dimension at 3 or above |

## 1. Use the tools in this order

1. **Checklist first.** Confirm that every required artifact exists and has evidence. A missing artifact is unfinished work, not a lower score.
2. **Rubric second.** Score quality against the descriptors, one dimension at a time, with one evidence reference per score.
3. **Record third.** Write the score, the evidence, and the single next action in the [progress record](../progress-and-reflection.md).
4. **Fix and re-score.** Re-score only after the artifact changes.

## 2. Scoring conventions

- A level of 3 is Proficient: the dimension is complete with minor gaps. A level of 4 is Exemplary and is not required.
- The weighted score for a dimension is $\text{weight} \times \text{level} / 4$. The maximum is 100.
- A high total does not compensate for a dimension below the completion threshold.
- A safety violation is an automatic fail, regardless of the total.
- A negative result is not a low score. A well-scoped negative result with a limit and an interval can be Exemplary.
- A correct number with a confounded comparison is not Proficient in experimental design.

## 3. Evidence rules

| Acceptable evidence | Not acceptable evidence |
|---|---|
| Run record with command, versions, and output | A screenshot with no command or timestamp |
| Metric with count and denominator | A percentage with no base set |
| Manifest with SHA-256 hashes | A file list |
| Clean-checkout reproduction | A notebook with saved outputs |
| Timestamped request log with IDs | A narrative claim that a control worked |
| Negative test that fails closed | A control that has never been tested |

## 4. Automatic fails

Every rubric shares these conditions:

- a third-party production target without written authorization;
- real personal data, real credentials, or a real mailbox or network service in a lab or project;
- a fabricated or selectively edited result;
- a claim that contradicts the artifact;
- a harmful capability presented as the deliverable.

## 5. What these tools do not do

They do not verify identity, proctor the work, or accredit the learner. They are self-assessment tools. The [evaluator guide](../../projects/evaluator-guide.md) is the separate reference for project calibration and is not part of student navigation. Scores are evidence about an artifact, not a qualification.
