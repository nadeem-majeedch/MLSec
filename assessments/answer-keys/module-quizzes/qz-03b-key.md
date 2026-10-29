# QZ-03B Answer Key — Module 03

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. C — sending 1,000 queries

Capability is what the adversary can do: access, queries, compute, time, and budget. A goal is the outcome the adversary wants (steal weights, cause a misclassification, read a record). Sending 1,000 queries is a capability that could serve several goals.

- **A, B, and D** are goals or harms, not capabilities.

Tag: M03 · LO-02 · Bloom 2 · D1.

## 2. B — public internet to authenticated API

The boundary is where authority changes: an anonymous caller on the public internet becomes an authenticated caller with a token and a role. That is a privilege and assumption change. A schema, a row count, or a loss function can change without crossing a trust boundary.

- **A** is a data-type change.
- **C** is a dataset-size change.
- **D** is a training-objective change.

Tag: M03 · LO-03 · Bloom 2 · D1.

## 3. True

A rejected threat is a decision with a reason and, ideally, a reopening condition. Recording it prevents the same debate on every review and shows that the model considered threats it did not accept. A register with only accepted threats hides the reasoning.

Tag: M03 · LO-03 · Bloom 2 · D1.

## 4. True

$4 \times 3 = 12$. Under the course bands, 10–16 is high. The statement is true. If you marked false, check the band boundaries rather than the multiplication.

Tag: M03 · LO-03 · Bloom 2 · D1.

## 5. Required elements (two controls, each classified)

Award the point for two controls with the correct type:

| Control | Type |
|---|---|
| Signed or allowlisted label sources; access control on the label store | Preventive |
| Provenance and lineage checks before training | Preventive |
| Duplicate and conflict checks at intake | Preventive |
| Reference-set screening or label-anomaly scoring | Detective |
| Audit-log review of label changes | Detective |
| Monitoring for a sudden label-distribution shift | Detective |

A response that names two preventive controls but no detection is acceptable if both are specific. "Use best practices" is not a control.

Tag: M03 · LO-04 · Bloom 3 · D2.

## 6. Inherent 20 (critical); residual 8 (medium); 60% reduction

- Inherent: $5 \times 4 = 20$, which is **critical** (17–25).
- Residual: $2 \times 4 = 8$, which is **medium** (5–9).
- Reduction: $(20 - 8) / 20 = 12 / 20 = 0.60$, or **60%**.

The score reduction is not the same as risk elimination: the residual threat still exists at medium severity and needs an owner and a detection or acceptance decision.

Tag: M03 · LO-03 · Bloom 3 · D2.

## 7. Required elements

Three of:

- **No testable steps:** "hack the model" is a goal, not an action sequence.
- **No adversary, access, or budget:** it does not say who does it, what they can reach, or how much they can spend.
- **No detection point:** a usable tree names where a defender could observe a step.
- **No asset or impact:** it does not say what is harmed or how success is measured.
- **No branch structure:** a tree needs alternatives at each decision point.

A usable first branch might be: "Obtain write access to the training pipeline" → "compromise a labeler account" or "submit poisoned rows through the vendor feed," each with a detection point (account anomaly, label-distribution shift).

Tag: M03 · LO-03 · Bloom 3 · D2.

## 8. Required elements

A bounded profile:

- **Goal:** cause an urgent finding to be downgraded, changing triage.
- **Knowledge:** state white-box (model and weights) or black-box (query access); state whether the scan pipeline is known.
- **Access:** ability to submit or modify a scan before triage; no access to the model server.
- **Budget:** a bounded perturbation (for example, an L∞ budget in pixel units) or a bounded number of submissions; no real patient data.

A testable detection hypothesis, for example:

> For a local synthetic scan set, a bounded perturbation that lowers the urgent-class score by at least 0.2 also shifts the input distribution beyond the calibration band; a monitor on input shift plus urgent-score drop should flag the modified scans while keeping false positives below 5% on clean scans.

The detection must name a signal, a threshold, and a false-positive measurement. "Monitor the model" is not testable.

Tag: M03 · LO-03 · Bloom 4 · D3.
