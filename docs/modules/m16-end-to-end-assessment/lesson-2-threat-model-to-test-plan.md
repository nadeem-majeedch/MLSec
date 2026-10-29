# Lesson 16.2 — From Threat Model to Test Plan

<a id="m16-l2"></a>

**Module 16 · Lesson 2 of 4 · 1 hour · LO-33**

## Scenario

Two assessments of the same system produce threat models with 24 entries each. The first ends with a 60-page document and no tests. The second ends with 24 entries, 9 tests, 6 rejected entries with reasons, and 3 accepted assumptions. The second assessment changes the production decision. The difference is not the number of threats. It is traceability.

## Objectives

By the end of this lesson you will be able to:

1. Write adversary profiles with goal, knowledge, capability, access, budget, and constraints.
2. Score risk with explicit likelihood and impact anchors.
3. Convert each prioritized threat into a test case with a budget, oracle, metric, and stop condition.
4. Reject or accept risks with a written reason instead of silently dropping them.
5. Detect a test that cannot fail and rewrite it.

## 1. From assets to adversaries

A threat is not a technique. It is a relationship between an adversary, an asset, and a path.

| Element | Question | Example |
|---|---|---|
| Goal | What does the adversary want? | Avoid a fraud block for one merchant |
| Knowledge | What does the adversary know? | Feature names, thresholds approximately, public model documentation |
| Capability | What can the adversary do? | Submit transactions, choose amount, time, and velocity |
| Access | What can the adversary reach? | The public scoring path; no training pipeline access |
| Budget | What limits the adversary? | Realistic feature ranges, limited accounts, detection risk |
| Success metric | What counts as success? | Block rate for the target segment falls below 0.10 |

NIST AI 100-2e2025 separates adversarial goals into availability, integrity, and privacy. Use that vocabulary, then make it concrete for the system.

### An adversary profile that is testable

```text
ID: ADV-02
Goal: Integrity — avoid block for transactions from a controlled merchant segment.
Knowledge: Feature list; approximate threshold; no access to training data or weights.
Capability: Choose amount, hour, and velocity within values observed in the last 90 days.
Access: Public scoring API through a merchant account.
Budget: At most 3 feature changes per transaction; no new merchant identities.
Success metric: Segment block rate below 0.10 at a global false-decline rate of 0.02.
Out of scope: Model extraction, credential theft, insider access.
```

A profile like this implies a test. A profile that says "external attacker" does not.

## 2. Risk scoring with anchors

Use two dimensions and define anchors before scoring.

| Likelihood | Anchor |
|---|---|
| 1 Rare | Requires capabilities the adversary does not plausibly have |
| 2 Unlikely | Possible with significant effort or favorable conditions |
| 3 Possible | Known technique, plausible access, some prerequisites |
| 4 Likely | Low-effort technique with existing access |
| 5 Almost certain | Observed in this system or trivially repeatable |

| Impact | Anchor |
|---|---|
| 1 Negligible | No measurable effect on a decision or asset |
| 2 Minor | Local inconvenience; recoverable without customer harm |
| 3 Moderate | Decision errors in a segment; management attention |
| 4 Major | Financial loss, regulatory exposure, or sustained customer harm |
| 5 Severe | Safety harm, systemic fraud loss, or loss of a critical service |

Score with the existing controls in place, then record the score with controls removed. The difference is the control's contribution, and it is often the most useful number in the register.

| ID | Threat | Asset | Likelihood | Impact | Score | Owner | Treatment |
|---|---|---|---:|---:|---:|---|---|
| R-01 | Duplicate disputed transactions inflate recall | Labels | 4 | 4 | 16 | Data platform | Test and fix |
| R-02 | Merchant shifts features to avoid block | Decision | 3 | 4 | 12 | Risk owner | Test and monitor |
| R-03 | Stale vendor feature feed degrades decisions | Feature store | 3 | 3 | 9 | Vendor manager | Monitor, contract |
| R-04 | Model artifact replaced in registry | Model | 2 | 5 | 10 | Platform security | Verify signing |
| R-05 | Reviewer overrides are not logged | Evidence | 2 | 3 | 6 | Operations | Test and fix |

Anchors are judgment, not physics. Their value is consistency and disclosure. State who scored, when, and with what inputs.

## 3. The test matrix

A test case has seven fields.

| Field | Requirement |
|---|---|
| ID and threat | Trace to a register entry |
| Hypothesis | A statement that could be false |
| Procedure | Enough detail for another person to repeat it |
| Budget and constraints | Perturbation, queries, samples, time, or access |
| Oracle | The rule that decides pass or fail |
| Metric and denominator | What is measured, over which base set |
| Evidence | The artifact that records the result |

Example:

| Field | T-02 |
|---|---|
| Threat | R-02: merchant shifts features to avoid block |
| Hypothesis | Within realistic feature bounds, a merchant can reduce its block rate below 0.10 without raising the global false-decline rate above 0.02 |
| Procedure | Freeze the temporal holdout; perturb amount, hour, and velocity by one observed step for the target segment; rescore; report segment and global block rates |
| Budget | At most 3 feature changes; values clipped to the 1st–99th percentile of the last 90 days |
| Oracle | Success if segment block rate < 0.10 while global false-decline rate ≤ 0.02 |
| Metric | Segment block rate, global false-decline rate, fraction of perturbed rows |
| Evidence | `experiments/t02_evasion.csv`, script, seed, run record |

Note what the test does **not** say. It does not say "run PGD." The technique is chosen after the hypothesis, and any technique that fairly tests the hypothesis is acceptable.

### Tests that cannot fail

Reject a test if:

- it has no oracle ("inspect the model for robustness");
- the budget is undefined ("some perturbation");
- the base set is undefined ("the test data");
- success is judged after seeing the result ("we will know it when we see it");
- the control is assumed rather than tested ("the WAF blocks that");
- it measures a proxy with no stated link to the risk ("loss increased").

Rewrite each into a falsifiable statement before running it.

## 4. Accept, reject, or test

Not every register entry deserves an experiment. Record one of four dispositions.

| Disposition | When to use | Required evidence |
|---|---|---|
| Test | Plausible, material, and within scope | Test case |
| Accept | Risk is within appetite or cheaper to accept than treat | Owner sign-off and rationale |
| Reject | Not plausible under the stated adversary or architecture | Written reason and assumption |
| Defer | Material but out of scope or blocked | Owner, trigger, and review date |

"Reject" is a legitimate outcome. "Ignore" is not. A rejected entry with a reason is evidence of judgment; a missing entry is evidence of an incomplete model.

Example rejection: "R-07: physical adversarial patches on merchant terminals. Rejected for this assessment because the scoring path uses terminal-captured features, not images, and the adversary profile has no physical access. Revisit if the product adds image capture."

## 5. Stop conditions

A test plan also defines when to stop.

- **Safety:** the test would touch real data, a real account, or a production service.
- **Stability:** the replica or service becomes unavailable or starts producing inconsistent results.
- **Scope:** the test reveals a path into an out-of-scope component.
- **Evidence:** the result cannot be reproduced after two controlled attempts.
- **Time:** the test exceeds 150% of its budget.

Write the stop condition next to the test, not in a separate policy nobody reads.

## 6. Worked example — Meridian Pay test plan

| ID | Threat | Test | Oracle | Evidence |
|---|---|---|---|---|
| T-01 | R-01 duplicate labels | Deduplicate near-identical disputes; recompute recall on the same temporal holdout | Recall changes by more than the 95% interval | `t01_dedup.csv` |
| T-02 | R-02 feature shifting | Perturb 1–3 merchant-controlled features within observed bounds | Segment block rate < 0.10 at global false-decline ≤ 0.02 | `t02_evasion.csv` |
| T-03 | R-03 stale feed | Simulate a 30-day feature freeze; compare decisions with fresh features | Decision disagreement > 5% in any segment | `t03_stale.csv` |
| T-04 | R-04 artifact replacement | Replace the artifact without updating the manifest; run the promotion gate | Gate rejects the artifact | `t04_gate.log` |
| T-05 | R-05 unlogged override | Submit an override through the reviewer path; inspect the log | Override reason and actor are recorded | `t05_log.json` |

T-01 and T-05 are not attacks. They are integrity tests. An assessment that only runs attacks will miss them, and in this example they carry two of the top three risks.

## 7. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Technique-first planning | Tests do not answer a risk | Write the hypothesis first |
| One test per technique | Redundant experiments, missing risks | One test per threat, technique chosen to fit |
| No oracle | Result is opinion | Define pass/fail before running |
| Undefined base set | Denominator changes with the story | Freeze and record the evaluation set |
| Silent rejection | Reader assumes coverage | Record rejections with reasons |
| Scoring without anchors | Severity is inconsistent | Publish anchors and inputs |
| Ignoring non-attack integrity risks | The biggest defect is missed | Include data, artifact, and logging tests |
| No stop condition | Test runs past safety or budget | Add one per test |

## 8. Check your understanding

1. Why is "external attacker" not a usable adversary profile?
2. What is the difference between likelihood with and without controls?
3. Name the seven fields of a test case.
4. Give an example of a test that cannot fail and rewrite it.
5. When is "reject" the right disposition, and what must be recorded?
6. Why should a stop condition sit next to a test?

## 9. What you keep

A risk register with anchors, adversary profiles, a traceability matrix from threat to test, and a written disposition for every entry. Lesson 16.3 makes the tests measurable.

## 10. Next

Lesson 16.3 covers baselines, negative controls, uncertainty, and evidence integrity before you run the attack experiments.
