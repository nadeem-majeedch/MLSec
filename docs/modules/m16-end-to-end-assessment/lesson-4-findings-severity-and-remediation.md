# Lesson 16.4 — Findings, Severity, Remediation, and Reporting

<a id="m16-l4"></a>

**Module 16 · Lesson 4 of 4 · 1 hour · LO-33, supports LO-30**

## Scenario

The assessment found that a merchant can shift its block rate by 13 percentage points using three feature changes, that 38 duplicate disputes inflated recall by 7 points, and that reviewer overrides were not logged. The report lists all three as "high." The owner has one engineering sprint and asks which to fix first. The report cannot answer, because severity was assigned by intuition and no control was costed.

An assessment that cannot support a decision is a technical diary. This lesson turns results into decisions.

## Objectives

By the end of this lesson you will be able to:

1. Write a finding with evidence, impact, affected assets, and a reproducible test.
2. Calibrate severity using impact, likelihood, exposure, and existing controls.
3. Prioritize remediation by risk reduction per unit of cost and disruption.
4. State residual risk after treatment, including untested attack classes.
5. Produce a technical report, an executive summary, and a briefing that agree.

## 1. The anatomy of a finding

A finding is a claim that a reviewer can check.

| Field | Content |
|---|---|
| ID | F-01 |
| Title | Segment-level evasion is invisible to global monitoring |
| Severity | High (see rubric below) |
| Affected assets | Fraud decision, merchant segment, decision log |
| Threat | R-02; adversary ADV-02 |
| Evidence | T-02: segment block rate 0.18 → 0.31 at fixed global false-decline 0.02; `t02_evasion.csv` |
| Root cause | Features are merchant-controlled; monitoring aggregates globally |
| Impact | Targeted fraud loss; no detection signal; unfair merchant treatment possible |
| Existing controls | Global drift monitor, velocity caps at ingestion (not at scoring) |
| Recommendation | Add segment-level block-rate monitor; enforce velocity cap in the feature store; retrain with bounded perturbations |
| Retest | T-02 rerun after controls; monitor must alert on the scripted shift |
| Residual risk | Adaptive attacker inside caps, spread across merchants |

A finding without an evidence link is an opinion. A finding without a retest is a suggestion.

## 2. Severity with a stated rubric

Use a small rubric and show the inputs. The following is a course rubric, not a standard.

| Dimension | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Impact | Negligible | Local, recoverable | Segment or customer harm | Severe, systemic, or regulated harm |
| Likelihood | Requires implausible access | Possible with effort | Known technique, plausible access | Low effort with current access |
| Exposure | Internal, no decision effect | Limited users | External users or revenue | Safety, rights, or critical service |
| Control gap | Strong compensating control | Partial control | Weak control | No control |

Severity bands: 4–6 Low, 7–9 Medium, 10–12 High, 13–16 Critical. Record the four inputs, not only the band. Two reviewers can then discuss the inputs instead of arguing about the label.

For F-01, impact 4 (targeted fraud loss and fairness), likelihood 3 (merchant-controlled features), exposure 3 (external merchants), control gap 3 (global monitor only) → 13, Critical under this rubric. If velocity caps were enforced at scoring, control gap might be 2 and the score 12, High. The control changes the severity, which is the point.

### Severity is not probability

A critical severity does not mean the attack is likely. It means that if it occurs, the consequence and exposure are severe and the control gap is large. State likelihood separately so the owner can weigh it.

## 3. Remediation sequencing

Prioritize with three inputs: risk reduction, cost, and disruption.

| Action | Risk reduced | Effort | Disruption | Dependencies | Priority |
|---|---|---|---|---|---|
| Enforce velocity cap in feature store | F-01, F-03 | 3 days | Medium | Feature owner | 1 |
| Add segment-level monitor | F-01 | 2 days | Low | Logging schema | 2 |
| Deduplicate training labels | F-02 | 1 day | Low | Data platform | 3 |
| Retrain with bounded perturbations | F-01 | 2 weeks | High | GPU or longer CPU run | 4 |
| Add override logging | F-04 | 1 day | Low | Reviewer UI | 2 |

Two principles:

- **Cheap detection before expensive prevention.** A monitor that makes the attack visible may reduce risk more per day of effort than a retraining cycle.
- **Do not bundle a research project into a sprint.** "Retrain with adversarial examples" is a multi-week experiment with an uncertain benefit. Sequence it after the controls that are known to work.

The sequence is a recommendation, not a mandate. The owner may accept a different order; record the decision and the residual risk.

## 4. Residual risk

Residual risk is what remains after the recommended controls are implemented. It has three parts:

1. **Untested threats.** The assessment did not test physical access, insider collusion, or a compromised vendor.
2. **Control limits.** Velocity caps can be evaded by spreading attempts; segment monitors can be gamed by staying under threshold.
3. **Unknowns.** The model may behave differently on a future population, and the synthetic data may not represent it.

Write residual risk as a statement, not a disclaimer:

> After the velocity cap, segment monitor, and deduplication, the assessed attack path is detected and its effect is reduced in the tested segment. Residual risk remains for an adaptive attacker who stays inside caps and spreads attempts across merchants, and for a compromised vendor feature feed, which was out of scope. The monitor's false-positive rate on legitimate seasonal spikes was not measured.

That statement tells the owner what they are accepting.

## 5. The report

Use a structure that lets three audiences read at different depths.

| Section | Audience | Content |
|---|---|---|
| Executive summary | Decision owner | Decision, scope, top three findings, recommended actions, residual risk |
| Scope and authorization | Auditor | System, versions, environment, non-goals, authority |
| System and data | Engineer | Diagram, classification, assets, owners |
| Threat model | Security | Adversaries, register, dispositions |
| Method | Reviewer | Test plan, baselines, controls, stop conditions |
| Results | Reviewer | Tables with n, budgets, intervals, negative controls |
| Findings | Owner and engineer | F-01…F-n with evidence and retest |
| Remediation | Owner | Sequence, cost, dependencies, owners |
| Residual risk | Owner and auditor | What remains and why |
| Limitations | Reviewer | What was not tested and why |
| Reproduction | Reviewer | Commands, manifest, environment |

The executive summary must agree with the findings. A common failure is an executive summary that says "no critical issues" while the findings table contains a critical.

### The briefing

Ten minutes, five slides:

1. Decision and scope.
2. System and top risks.
3. What was tested and what happened (one table).
4. What to do first, and what it costs.
5. Residual risk and what would change the conclusion.

Do not read the report aloud. The briefing is for the decision, not the method.

## 6. Worked example — Meridian Pay findings

| ID | Finding | Severity | First action | Retest |
|---|---|---|---|---|
| F-01 | Segment evasion invisible to global monitoring | Critical (4,3,3,3) | Enforce velocity cap; add segment monitor | T-02 + monitor alert |
| F-02 | Duplicate disputes inflate recall by 7 points | High (3,4,2,2) | Deduplicate labels; update data gate | T-01 |
| F-03 | Stale vendor feed affects 7% of decisions | Medium (3,3,3,2) | Contractual freshness SLA; staleness monitor | T-03 |
| F-04 | Reviewer overrides unlogged | Medium (2,3,3,3) | Add actor, reason, timestamp | T-05 |
| F-05 | Artifact replacement blocked by gate | Informational | None; maintain | T-04 |

F-05 is a positive control result, not a finding. Include it in an appendix so the reader knows the gate was tested.

## 7. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Severity by intuition | Owner cannot compare findings | Use a published rubric and show inputs |
| Findings without evidence | Reviewer cannot verify | Link each finding to a test and artifact |
| Recommendations without owners | Nothing happens | Name an owner and a retest |
| Bundling research with fixes | Remediation stalls | Separate known controls from experiments |
| Residual risk as a disclaimer | Owner does not know what they accept | State the remaining path and its limits |
| Executive summary disagrees with body | Credibility lost | Reconcile before release |
| Hiding negative results | Reader assumes coverage | Report controls that passed and tests that failed to show an effect |
| No reproduction section | Assessment cannot be audited | Provide commands and manifest |

## 8. Check your understanding

1. What are the five essential fields of a finding?
2. Why should severity inputs be reported, not only the band?
3. Give an example of a cheap detection that reduces more risk than an expensive prevention.
4. What three things make up residual risk?
5. Why must the executive summary and findings table agree?
6. What is the difference between a positive control result and a finding?

## 9. What you keep

A finding template, a severity rubric with inputs, a remediation table with owners and retests, a residual-risk statement, and a report outline. Together with Lessons 16.1–16.3, this is the assessment method you apply in the project.

## 10. Next

Choose one of the six projects in the [project catalog](../../projects/index.md) and complete the staged tasks. The [evaluator guide](../../projects/evaluator-guide.md) is available to instructors and self-reviewers after submission.
