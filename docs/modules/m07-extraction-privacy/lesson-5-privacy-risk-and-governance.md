# Lesson 07.5 — Privacy Risk, Governance, and Reporting

<a id="m07-l5"></a>

**1.25 hours · Lesson 5 of 5 · Module 07**

## What this lesson answers

How do you turn an attack result into a decision? This lesson connects the metrics from LAB-09 and LAB-10 to operational burden, defense choices, and a memo that a privacy officer or engineering lead can act on.

## Risk is a decision, not a score

A metric answers a measurement question. A risk decision answers a different one:

1. **What can happen?** Which attack, against which system, affecting whom?
2. **How likely is it?** What access, budget, and auxiliary data does the attacker need?
3. **How bad is it?** What harm follows from a correct and an incorrect inference?
4. **What does it cost to reduce?** Which defense, at what utility and operational cost?
5. **What remains?** What residual risk is accepted, by whom, until when?

A single number cannot answer these. "AUC 0.82" is not a risk level. "TPR 7.4% at FPR 1%" is a measurement at an operating point. The risk decision adds the population, the base rate, the harm, and the cost.

## From TPR to operational burden

LAB-10's threshold attack has TPR 22.8% at FPR 5%. Suppose a candidate pool has 10,000 records and the defender uses the attack to flag possible members for review.

| Member prevalence | Members | Nonmembers | True flags | False flags | Precision | Reviews per true member |
|---:|---:|---:|---:|---:|---:|---:|
| 1% | 100 | 9,900 | 22.8 | 495 | 4.4% | 22.7 |
| 10% | 1,000 | 9,000 | 228 | 450 | 33.6% | 3.0 |
| 50% | 5,000 | 5,000 | 1,140 | 250 | 82.0% | 1.2 |

At 1% prevalence, the defender reviews about 23 records for every true member found. The false positives are not abstract: they are people or records wrongly treated as training members. Their cost may include manual review time, delayed service, reputational harm, or a legal obligation triggered by a false accusation.

The same arithmetic at the stricter 1% false-positive budget (TPR 7.4%):

| Prevalence | True flags | False flags | Precision | Reviews per true member |
|---:|---:|---:|---:|---:|
| 1% | 7.4 | 99 | 7.0% | 14.4 |
| 10% | 74 | 90 | 45.1% | 2.2 |
| 50% | 370 | 50 | 88.1% | 1.1 |

The stricter budget catches far fewer members but produces fewer false accusations. Which operating point is appropriate is a policy question, not a statistical one.

### Adding cost

If each review costs an illustrative \$40, the 1%-prevalence, 5%-FPR case costs

$$
(22.8 + 495) \times \$40 = \$20{,}712
$$

to find 22.8 true members, or about \$908 per true member. At 50% prevalence, the cost is \$55,600 for 1,140 true members, or about \$49 per true member. The attack's TPR and FPR did not change. The population did.

This is why a privacy assessment must state the base rate. A vendor who reports only TPR is describing a test, not the consequences of using it.

## Composition: attacks do not stay separate

The three attacks can reinforce each other:

| Path | How it works | Consequence |
|---|---|---|
| Extraction → membership | Extract a surrogate, then run membership inference locally | No further queries; the target may never see the attack |
| Extraction → inversion | Use the copy to optimize inputs offline | The attacker can search without rate limits |
| Membership → inversion | Membership tells the attacker which records are worth reconstructing | Effort is focused on real members |
| Inversion → extraction | Reconstructed representatives can serve as queries | Better coverage of the input domain |

A defense evaluated against one path may leave another open. Output rounding, for example, reduces the confidence signal used by membership and inversion, but a label-only API can still be extracted. Differential privacy reduces membership signal in the training data, but does not stop extraction of the learned function.

## The defense portfolio

Defenses act at different layers. A serious plan uses more than one.

| Layer | Control | Attacks addressed | Main cost | Residual risk |
|---|---|---|---|---|
| **Data** | Minimize and justify collected data | Membership, inversion | Less data for utility | Data that must be used remains exposed |
| **Training** | Regularization, early stopping, capacity limits | Membership, inversion | Accuracy trade-off | No formal guarantee |
| **Training** | Differential privacy | Membership, some inversion | Utility and compute cost; privacy budget | Guarantee depends on parameters and implementation |
| **Interface** | Hard labels, rounding, top-k | Membership, inversion | Lost explanations and calibration | Label-only and stability attacks |
| **Interface** | Quotas, rate limits, monitoring | Extraction, membership | Access and operational cost | Account farms; adaptive attackers |
| **Artifact** | Watermarking, fingerprinting | Extraction (detection and ownership) | Accuracy and maintenance | Removal; only detects preserved marks |
| **Organizational** | Contracts, vendor assessment, audit | All | Legal and staff time | Violations and insiders |
| **Incident response** | Detection, containment, notification | All | Readiness cost | Unknown or slow detection |

### Differential privacy in one paragraph

A randomized training mechanism $M$ is $(\varepsilon,\delta)$-differentially private if, for any two datasets that differ in one record and any set of outputs $S$,

$$
\Pr[M(D) \in S] \le e^{\varepsilon} \Pr[M(D') \in S] + \delta.
$$

Smaller $\varepsilon$ means a stronger bound on how much one record can change the output. The guarantee composes across queries and releases, and it costs utility: the stronger the privacy, the more the model may differ from a non-private fit. Differential privacy is the strongest training-time tool in this table, but it is not a complete answer to extraction, and its parameters must be chosen and documented.

## A memo template

Use this structure for any privacy or extraction finding. It is short enough to read and specific enough to act on.

```text
1. System and data
   - What model, what data, how many records, who is affected?
2. Access and threat model
   - What can the attacker query, how often, with what auxiliary data?
3. Evidence
   - Attack, score, operating point, baseline, sample size, split.
   - TPR at stated FPR; precision at the deployment base rate.
4. Impact
   - What does a correct inference reveal? What does a false one cost?
5. Assumptions and limitations
   - Dataset, model family, one split, no adaptive attacker, no defense tested.
6. Recommendation
   - Control, owner, cost, residual risk, review date.
```

### Illustrative memo

The following is a **format demonstration**, not a measurement of a real system. The operating point is borrowed from LAB-10's digits experiment and would not transfer to another model or population.

```text
System: a binary screening model trained on 200,000 records, served through
a probability API. The candidate pool for a membership test is estimated at
10,000 records with a 1% member prevalence.

Threat model: an external account holder with query access, no shadow models,
and public auxiliary data. The attacker uses maximum predicted probability.

Evidence: in a controlled digits experiment (500 members, 500 nonmembers),
the attack reached TPR 22.8% at FPR 5% (AUC 0.82). At a 1% prevalence, that
corresponds to 22.8 true flags and 495 false flags per 10,000 candidates
(precision 4.4%).

Impact: a correct flag reveals that a person's record was used in training.
A false flag subjects a nonmember to the same review. At an illustrative $40
per review, the 5%-FPR operating point costs about $20,700 per 10,000
candidates and about $908 per true member found.

Limitations: the digits experiment is not this system. No shadow models, no
adaptive attacker, one split, and no defense were evaluated.

Recommendation: do not deploy membership flags as individual accusations.
If the review is required, use the 1%-FPR operating point, require human
adjudication, and evaluate differential privacy before claiming a privacy
improvement. Owner: privacy engineering. Review: after the next model retrain.
```

The memo does not say "the model is private" or "the model is unsafe." It states what was measured, what it implies at a stated prevalence, and what decision follows.

## What each audience needs

| Audience | What they need | What to leave out |
|---|---|---|
| **Engineer** | Reproduction steps, metric definitions, failure modes | Legal conclusions |
| **Privacy officer** | Affected population, base rate, precision, harm, obligations | Raw hyperparameters |
| **Executive** | Decision, cost, residual risk, owner, date | Threshold sweeps |
| **Auditor or regulator** | Methodology, assumptions, evidence, limitations | Marketing language |
| **Data subjects** | Whether their data was used and what it means | Internal attack details that create new risk |

The last row is not a communication channel for attack details. Transparency about data use is a governance obligation; publishing a working extraction recipe against a live system is not.

## Governance controls that act before the attack

Technical controls are not the only layer. The following controls reduce exposure even when the attack is feasible:

- **Purpose limitation.** Train on data for a stated purpose; do not reuse it for unrelated models.
- **Data minimization.** Do not collect fields the model does not need, especially sensitive attributes.
- **Retention limits.** Delete training data when it is no longer needed; document what deletion means for derived models.
- **Access control.** Limit who can query the model, export artifacts, and read logs.
- **Vendor assessment.** Ask for the access model, output type, logging, retention, and incident history.
- **Model documentation.** Record training data provenance, intended use, known limitations, and evaluation results.
- **Privacy impact assessment.** For high-risk processing, document necessity, proportionality, risks, and mitigations before deployment.
- **Independent testing.** Red-team with written authorization, a query cap, and a reporting path.
- **Incident response.** Define what happens if extraction, membership probing, or a data leak is detected.

Privacy law varies by jurisdiction. The principles above are common, but whether a particular inference is unlawful, reportable, or subject to a data-subject request is a legal question. Route it to counsel; do not settle it in an engineering document.

## Reporting checklist

Before you send a privacy or extraction finding, check:

- [ ] The metric is defined, with numerator and denominator.
- [ ] The baseline is stated (random, majority class, or prior attack).
- [ ] The operating point is stated (FPR budget or threshold).
- [ ] The base rate is stated, and precision is computed from it.
- [ ] The sample size and split are stated.
- [ ] The access model and query budget are stated.
- [ ] The auxiliary data assumption is stated.
- [ ] At least four limitations are listed.
- [ ] The defense, if any, is named and its residual risk is measured.
- [ ] The recommendation has an owner and a review date.
- [ ] The claim does not exceed the experiment.

## What would change the conclusion

A risk finding is conditional. State what would make it worse or better:

| Change | Direction | Why |
|---|---|---|
| Stronger attack (shadow models, LiRA) | Worse | Higher TPR at the same FPR |
| Higher member prevalence | Better precision | Fewer false flags per true flag |
| More sensitive data | Worse impact | The same inference causes more harm |
| Probability outputs instead of labels | Worse | More signal per query |
| Differential privacy with a meaningful budget | Better membership guarantee | Formal bound on influence |
| Rate limits and monitoring | Higher attacker cost | Fewer queries, more detection risk |
| Different population for nonmembers | Either | Score distributions shift |
| Adaptive attacker | Worse | Defenses may be circumvented |

## Common mistakes

| Mistake | Symptom | Correction |
|---|---|---|
| Treating AUC as risk | "0.82 risk" | Report TPR at an operating point and precision at a base rate |
| Quoting precision without prevalence | "4.4% precision" with no pool | State the assumed base rate |
| Calling extraction "theft" | A legal conclusion in an engineering report | Say "a surrogate with fidelity $x$ was trained"; route legal questions |
| Assuming DP solves everything | "We are differentially private, so no extraction" | DP bounds training-data influence, not function copying |
| Hiding confidence and declaring victory | No residual measurement | Test label-only and repeated-query attacks |
| Evaluating one attack | "Membership is low risk" after one threshold test | Name the stronger attacks that were not tested |
| No owner or date | A finding that never gets fixed | Add both to the recommendation |
| Ignoring false-positive harm | Only TPR is discussed | Cost the false flags at the deployment prevalence |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Memo has numbers but no decision | Evidence without a recommendation | Add control, owner, cost, review date |
| Precision and TPR are confused | Different denominators | Recompute with the Bayes formula |
| Defense claim is unsupported | No attack was rerun | Measure the same attack after the defense |
| Stakeholders disagree on risk | Different base rates or harms | Put both assumptions in the memo |
| Legal question blocks the report | Scope creep | Separate the technical finding from the legal advice |

## What you should be able to do now

- Convert TPR and FPR into expected true and false flags at a stated prevalence.
- Explain why the same attack is a different operational problem in different populations.
- Choose a defense portfolio and state each control's cost and residual risk.
- Write a decision memo with evidence, impact, limitations, and an owner.
- Avoid claiming that a laboratory result measures a deployed system.

## Summary

A privacy or extraction result becomes useful when it is attached to a population, an operating point, a harm, and a decision. TPR alone hides the false flags; AUC alone hides the operating point; precision without a base rate is incomplete. Defenses act at the data, training, interface, artifact, and organizational layers, and each leaves residual risk. The memo is the deliverable: what was measured, what it implies, what remains uncertain, and who acts next.

## Next step

You have completed the Module 07 lessons. Run [LAB-09](../../labs/lab-09.md) and [LAB-10](../../labs/lab-10.md), then take the [knowledge check](quiz.md) and work through the [exercises](exercises.md). The exercises include a scenario that asks you to write the memo this lesson describes.
