# Module 16 Exercise Solutions

These are model answers, not the only acceptable ones. A different scope, test, or severity rationale is acceptable if it is explicit, traceable, and consistent with the scenario.

## Exercise 1 — Audit a scope statement

### 1. Missing or unusable fields

- **Components:** "the claims triage model" omits the pipeline, feature store, serving path, and reviewer queue.
- **Versions:** no model, dataset, code, or dependency version.
- **Decision and owner:** "check for security issues" names no decision and no accountable role.
- **Environment:** "production-like" is not a test environment; it does not say whether production data or traffic is involved.
- **Non-goals:** "none" is not credible and invites scope drift.
- **Constraints:** no rules on data, request volume, destructive actions, or third-party systems.
- **Authority:** "requested" is not written authorization with a name and policy.
- **Data handling:** no statement on classification, storage, retention, or deletion.

### 2. Rewritten scope

| Field | Content |
|---|---|
| System | Northwind Claims triage model and its batch scoring path |
| Components | Training data snapshot, feature store, model artifact, batch scorer, reviewer queue, decision log |
| Versions | Model 2.3.0, dataset `claims-2026-09`, commit `d4e5f6a` |
| Environment | Local replica on loopback; synthetic claims only |
| Decision | Whether to expand the model to auto claims |
| Non-goals | Mobile app, payment system, contractor portal, real policyholder data |
| Constraints | No production traffic; no real personal data; no destructive actions; 40 requests/minute cap |
| Authority | CISO engagement memo NW-2026-14; course authorized-use statement |

### 3. Evidence for the expansion decision

Needed:

- Performance and error analysis on an auto-claims holdout, including subgroup results and false-review cost.
- A threat model for auto-specific data sources (photos, police reports, repair estimates) and the controls that would change.

Not needed for this decision: a full extraction study of the current property model, unless the expansion changes the exposure of model IP.

### 4. Why "out of scope: none" is a red flag

- It implies authority over systems and data the assessor may not own or be permitted to test.
- It removes the boundary that protects against scope drift and makes the assessment unfinishable.
- It is inconsistent with a two-week timeline.

### 5. Omitted asset

The **reviewer queue and override log**. A model-only scope would miss that reviewers can override decisions without recorded reasons, which destroys the evidence needed to investigate a bad decision and hides insider or process abuse.

## Exercise 2 — Turn threats into tests

### 1. Test cases

| Field | T-01 (R-01) | T-02 (R-02) | T-03 (R-03) | T-04 (R-04) |
|---|---|---|---|---|
| Hypothesis | Near-duplicate photo sets inflate recall by more than the 95% interval | Inflated estimate text raises the manual-review rate for a body shop without changing fraud prevalence | A 30-day fee-table freeze changes more than 5% of estimates in at least one region | The gate rejects an artifact whose manifest hash does not match |
| Procedure | Deduplicate by perceptual hash; recompute recall on the frozen holdout | Add plausible inflation phrases to estimates for one shop; rescore | Freeze the fee table at an old version; compare decisions | Replace the artifact bytes; run the promotion gate |
| Budget | No model change; one dedup pass | At most 3 phrases and 10% text-length increase | One 30-day freeze | One tampered artifact |
| Oracle | Recall difference outside the interval | Review rate rises while confirmed fraud is unchanged | Any region disagreement > 5% | Gate exits nonzero and logs the hash mismatch |
| Metric / n | Recall over 4,820 claims | Review rate over 600 shop claims; fraud prevalence | Disagreement over 4,820 claims | Gate result over 1 artifact |
| Evidence | `t01_dedup.csv` | `t02_text.csv` | `t03_fee.csv` | `t04_gate.log` |

### 2. Dispositions

- **R-05 (unlogged overrides): Test.** It is cheap to test, material to evidence integrity, and within scope.
- **R-06 (screen photograph): Reject.** The adversary profile has no physical access, and the assessment environment is a local replica. Record the assumption and revisit if a site visit is added.

Deferring R-05 would also be defensible if the reviewer UI is out of scope, but the queue is in scope here.

### 3. Negative control

T-01's dedup pass can include a **shuffled-duplicate control**: randomly duplicate the same number of clean claims and confirm that recall does not move beyond the interval. A failure reveals that the metric is sensitive to row count or that the split is contaminated, not that duplicates matter.

### 4. Falsifiable R-02 hypothesis

> For a body shop with 600 claims, adding at most three plausible inflation phrases and increasing estimate text length by at most 10% raises the manual-review rate from 0.22 to above 0.30 while confirmed fraud prevalence stays within 1 percentage point.

### 5. Test that cannot run locally

R-06 requires physical access to a screen. A local synthetic environment cannot reproduce shoulder-surfing, camera angles, or the human factors that determine whether a photograph is usable. It can test screen-lock policy, but not the attack. The correct disposition is reject or defer with that reason.

## Exercise 3 — Audit the evidence

### 1. Methodological problems

- No baseline protocol: split, threshold, seed, and versions are not stated.
- Accuracy alone on a likely imbalanced claims dataset; no per-class or cost metric.
- One seed is not evidence of stability; it is one sample.
- Random split leaks claims from the same policyholder across train and test.
- Threshold chosen after seeing defense results, which tunes the comparison.
- No zero-poison or clean-control result.
- No defense cost: clean accuracy, false reviews, and runtime are missing.
- No uncertainty or denominator for the 2% poison rate (2% of what?).
- Screenshot evidence cannot be verified or rerun.
- "The defense works" is an overclaim from one accuracy comparison.

### 2. Most direct reproduction barrier

The missing protocol and raw outputs. Even with the screenshot, a reviewer cannot know the split, seed, threshold, or preprocessing, so the number cannot be recreated. The second barrier is the post hoc threshold, which changes the meaning of both results.

### 3. Rewritten table row

| Test | Condition | n | Metric | Baseline | Result | Difference (95% CI) | Notes |
|---|---|---:|---|---|---|---|---|
| P-01 | 2% label-flip poison | 4,820 | Accuracy on grouped holdout | 0.91 | 0.84 | −0.07 (−0.09, −0.05) | Seed 42; threshold fixed at 0.50; zero-poison control 0.91 |

Add a second row for the defense at the same threshold and a third for its clean-accuracy cost.

### 4. Scoped claim

> Against a 2% label-flip poison on the frozen grouped holdout, accuracy fell from 0.91 to 0.84 at a fixed threshold. The tested screening defense recovered accuracy to 0.90 at a false-positive rate of 0.03 and a runtime increase of 18%. The experiment used one seed and did not test an adaptive attacker who knows the screen.

### 5. Negative controls

- **Zero-poison control:** train on clean data through the same pipeline; accuracy should match the baseline.
- **Random-label control:** flip the same number of labels at random rather than targeted; compare the effect.
- A third useful control is a **clean-row screen pass** to measure false positives.

### 6. Why a random split is wrong

Multiple claims from the same policyholder or property share features and outcomes. A random split puts some of those claims in training and others in test, so the model can memorize policyholder-specific patterns. The result is leakage: test performance is inflated and the poisoning effect is underestimated. Group by policyholder (and ideally by time) instead.

## Exercise 4 — Severity and remediation

### 1. Scores

| ID | Impact | Likelihood | Exposure | Control gap | Total | Band |
|---|---:|---:|---:|---:|---:|---|
| F-01 | 4 | 4 | 2 | 3 | 13 | Critical |
| F-02 | 3 | 3 | 3 | 3 | 12 | High |
| F-03 | 3 | 3 | 3 | 2 | 11 | High |
| F-04 | 2 | 3 | 3 | 3 | 11 | High |
| F-05 | 2 | 1 | 1 | 1 | 5 | Low |

F-01 is Critical under the rubric because duplicates are likely, impact is severe, and the control gap is large. The exposure score of 2 reflects internal decision effect rather than direct customer harm.

### 2. Remediation order

1. **Override logging (1 day)** — cheapest, closes an evidence gap, enables investigation of F-01 and F-02.
2. **Deduplication (2 days)** — removes a measured 8-point inflation and improves every later comparison.
3. **Fee-table freshness monitor (2 days)** — cheap, addresses a known 6% decision effect.
4. **Text-feature cap (5 days)** — reduces F-02 but may have false-review costs; test after measurement is fixed.

If the owner insists on risk-reduction order rather than cost order, F-01 deduplication comes first. Both orders are defensible if the rationale is stated.

### 3. One-day choice

Override logging. It is the only item that fits the time box and it creates the evidence needed to investigate the two highest-impact findings. Deduplication is a close second, but it cannot be completed and verified in one day with a clean rerun.

### 4. Residual-risk statement for F-01

> After deduplication and a data-quality gate, the measured 8-point recall inflation is removed on the assessed snapshot. Residual risk remains for duplicates that are not near-identical (for example, re-photographed damage from a different angle), for label errors in the source system, and for future data sources that bypass the gate. The gate's false-positive rate on legitimate repeat claims was not measured.

### 5. F-05 in the report

Yes. It is a positive control result: the artifact gate worked. Reporting it shows the assessment tested a control and found it effective, and it gives the reader a complete picture. Put it in an appendix or a "controls verified" table, not in the findings list.

### 6. Why one number hides the decision

A single overall risk score aggregates findings with different owners, costs, and remedies, so it cannot tell the owner what to do first; it also hides which assets are exposed and which controls are missing. Use the register and the remediation sequence for decisions, and the band only for triage.
