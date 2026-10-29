# Rubrics — Scoring Notes and Calibration

| Field | Value |
|---|---|
| Audience | Course owner, self-study learner acting as their own evaluator, and any authorized reviewer |
| Status | Calibration notes for internal use; not part of student site navigation |
| Student tools | [`docs/assessments/rubrics/`](../../docs/assessments/rubrics/index.md) |
| Companion | [Project evaluator guide](../../docs/projects/evaluator-guide.md) |

These notes explain how to apply the published rubrics consistently. They do not add requirements that the student pages do not state. If a note and a student-facing rubric disagree, the student-facing rubric wins; fix the inconsistency rather than enforcing the note.

## 1. Scoring workflow

1. Confirm the artifact contract. A missing required file is an incomplete submission, not a low-quality one.
2. Run the lab-specific checker or the reproduction command. Record structural pass/fail separately from execution.
3. Read the report and the findings, then inspect the artifact behind each headline claim.
4. Score each dimension independently. Do not let a strong report raise a weak artifact.
5. Write one evidence reference per score: file, line, metric, or section.
6. Apply automatic fails before computing a total.
7. Re-score only after a change to the artifact.

## 2. Calibration anchors

### Level 3 is the completion standard

A level of 3 means the dimension is complete with minor gaps, not "average." Do not reserve 3 for exceptional work. If the artifact meets the descriptor and the evidence reference exists, it is a 3.

A level of 4 requires something beyond completeness: an adaptive test, a second seed, a zero-effect control, a clean-checkout run, or a limitation that changes how the result should be used.

### Negative results

A negative result with a denominator, a bound, and a stated limit can be level 4. Do not penalize an attack that failed to work if the evaluation was sound. Do penalize a negative result that is actually an untested or invalid run.

### Numbers without denominators

A percentage without a base set is incomplete in experimental design, regardless of how plausible it looks. The same applies to a detection rate without a false-positive count and a privacy claim without sensitivity and composition.

### Reports and artifacts

A polished report cannot compensate for a missing manifest or a baseline that changed between runs. Score the artifact first; use the report to understand it, not to replace it.

## 3. Dimension-specific notes

| Dimension | Common over-score | Correction |
|---|---|---|
| Technical correctness | Code runs, so it is scored 4 | 4 requires the named method, correct edge cases, and values within tolerance |
| Security reasoning | A long threat list is scored high | Score the adversary, budget, metric-to-harm link, and limits |
| Experimental method | A single strong result is scored high | Require a frozen baseline and matched conditions |
| Reproducibility | A repository with a README is scored high | Require a clean run and matching hashes |
| Communication | Length is mistaken for completeness | Score decision-orientation and evidence, not word count |
| Defense evaluation | Static ASR drop is scored high | Require an adaptive variant and the false-positive cost |
| Fairness | One metric improvement is scored high | Require subgroup intervals and a stated trade-off |
| Privacy | A low MIA AUC is scored as proof | Require the formal accounting and the empirical caveat |

## 4. Automatic fails and moderation

An automatic fail stops scoring. Record the condition, the artifact, and the date. Do not average it into a low score.

| Condition | Action |
|---|---|
| Third-party target without authorization | Stop; do not run or review further; notify the course owner |
| Real personal data or credentials | Stop; secure or delete the local copy; do not redistribute |
| Fabricated or edited result | Mark the submission incomplete; require a reproduction from raw inputs |
| Claim contradicts the artifact | Mark the affected dimension at 1; require a corrected report |
| Harmful capability as the deliverable | Stop; review intent and authorization before any further feedback |

A reviewer who is also the learner should apply the same rules. Self-scoring is not a license to waive a safety condition.

## 5. Project and RT-01 calibration

- **Project completion** is all dimensions at 2 or above and at least six at 3. A project with one dimension at 2 is complete but not yet suitable as capstone evidence for that dimension.
- **RT-01** additionally requires rules of engagement, evidence, detection, and mitigation at 3. A red-team report without a signed RoE is incomplete even if the attacks ran.
- **Detection claims** need a quiet baseline and a false-positive count. "100% detection" on the attack set alone is not a detection result.
- **Mitigation claims** need a variant that is not the original payload with a changed seed. A block of the exact script is not generalization.
- **Evidence** must be attributable before mitigation changes the state. A screenshot without a request ID is weak evidence.

## 6. Capstone calibration

- Every dimension must be at 3. A total of 90 with one dimension at 2 is not complete.
- The clean-checkout test is part of Reproducibility. A failure caps that dimension at 2.
- The four limitation types are construct, internal, external, and statistical. Naming only "small dataset" is not all four.
- A claim that the defense "works" after a static test, with no adaptive variant or a stated reason it cannot be run, caps Defense at 2.
- The report's abstract must state the headline result, its scope, and the residual risk. An abstract that only describes the topic is incomplete.

## 7. Disagreement and appeals

A learner may disagree with a score. The appeal should cite the descriptor and the artifact, not effort or intent. The reviewer re-reads the descriptor, the evidence, and the automatic-fail list. If the rubric is ambiguous, fix the rubric for future use and record the interpretation in the same edit.

## 8. Maintenance

- Change a rubric and its student-facing copy together.
- Keep the weights at 100 and the completion rule unchanged unless the course owner approves.
- Recompute any example that depends on a lab artifact when the artifact changes.
- Do not add external validation, accreditation, or proctoring claims.
- Run `python scripts/validate_assessments.py` after edits.
