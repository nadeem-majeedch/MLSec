# LC-5 Answer Key — Level 5 Applied Projects

**Scoring:** items 1–6 = 1 point each; items 7–8 = 2 points each; items 9–10 = 5 points each. Total 20. Pass 16/20.

## 1. A — the vendor's production infrastructure behind the API

The assessment is bounded to the local replica. Everything behind the vendor's API is outside the learner's authorization and outside the evidence the replica can produce.

- **B**, **C**, and **D** are all part of the local test: the endpoint, the synthetic data generator, and the named model version.

Tag: M16 · LO-33 · Bloom 2 · D1.

## 2. B — budget, base set and count, effect against a baseline, reproduction steps, and the affected decision

A finding is usable when another engineer can reproduce it and connect it to a decision. That requires the request budget, the base set and its size, the measured effect against a baseline, the steps and artifacts, and the decision the weakness affects.

- **A** is an anecdote with no denominator or method.
- **C** names a tool but not what was done or observed.
- **D** gives a label and an instruction without evidence, so the owner cannot verify the fix.

Tag: M16 · LO-28 · Bloom 3 · D2.

## 3. C — the unmeasured comparison under bursty pacing at a fixed alert budget

A gap states what is missing, under which conditions, and why the missing comparison matters. Option C names the prior condition (even pacing), the unmeasured condition (bursty pacing at a fixed alert budget), and the consequence (the detector ranking may not hold).

- **A** is a topic statement with no gap.
- **B** is an unsupported claim of absence; "nobody has studied" requires a review.
- **D** is a severity assertion, not a gap.

Tag: M18 · LO-35 · Bloom 3 · D2.

## 4. B — a signed authorization naming the target, time window, request budget, data rules, and stop conditions

Authorization precedes testing. The document names what may be touched, for how long, at what volume, with which data, and when to stop. A local replica still needs this discipline because it establishes the boundary the report will rely on.

- **A** is not attributable and does not bound the work.
- **C** covers a different system and does not authorize the replica.
- **D** is produced after testing.

Tag: M17 · LO-29 · Bloom 2 · D1.

## 5. False

A negative result with a confidence interval is informative: it bounds the effect and tells the reader what the test could have detected. Reporting nothing leaves the reader unable to distinguish "no effect" from "not tested." The interval is what makes the negative result usable.

Tag: M18 · LO-28 · Bloom 3 · D2.

## 6. False

A plan revised after seeing the results is exploratory, even if the revision is documented. Documentation makes the change honest; it does not restore the confirmatory status of the original test. A new claim needs a fresh holdout, a pre-registered analysis, or an explicitly labelled exploratory result.

Tag: M18 · LO-35 · Bloom 3 · D2.

## 7. Required elements (three elements, unresolved issue)

Three elements:

- **A concrete action and the component it changes.** "Retrain the model" is not schedulable; "add a 20% norm-clipped adversarial-training run to the promotion pipeline" is.
- **An owner and a cost or effort estimate with a target date.** Someone must be accountable, and the work must be sized against other work.
- **A verification test with a pass criterion.** The test states what will be measured, on which data, and what result counts as the risk being reduced.

Without a verification test, closure is an assertion. The owner cannot show that the change reduced the risk rather than shifting it, and the residual-risk entry has no evidence behind it. A remediation without verification cannot be distinguished from a remediation that was never applied.

Two points: one for the three elements, one for the consequence of omitting verification.

Tag: M16 · LO-33 · Bloom 3 · D2.

## 8. Required elements (base rate, evidence preservation)

**Base rate.** Precision is $\mathrm{TP}/(\mathrm{TP}+\mathrm{FP})$. At a low base rate, the false positives from even a small false-positive rate can outnumber the true positives. For example, 0.2% malicious in 100,000 requests is 200 malicious requests; at 90% recall that is 180 true positives, while a 0.5% false-positive rate on 99,800 benign requests yields 499 false positives, so precision is about 180/679, or 0.27. The same detector at a higher base rate would have much better precision. Recall and FPR alone cannot tell an analyst how much of the queue is real.

**Evidence preservation.** Capture logs, requests, responses, hashes, and timestamps **before** applying a mitigation, because mitigation can block the attack path, alter the model or configuration, and destroy the state that explains what happened. Without that evidence, the team cannot attribute the activity, reproduce the result, or show that the control actually works; the report becomes an assertion.

Two points: one for the base-rate computation or a correct qualitative explanation with the formula, one for at least two reasons to preserve evidence.

Tag: M17 · LO-34 · Bloom 4 · D3.

## 9. Required elements (decision, assets, adversary, questions, deliverables, non-goals)

- **Decision.** What the API's category and confidence are used for, such as routing a synthetic document to a review queue. State the cost of a wrong route in each direction.
- **Three assets with classification.** For example: submitted documents (confidential), the model and its weights (internal), request logs (confidential, possibly restricted because they contain document text), and the label taxonomy (public or internal). Use the course's four levels: public, internal, confidential, restricted.
- **One bounded adversary profile.** An external submitter with black-box API access, no credentials beyond a normal caller, synthetic documents only, and a budget such as 1,000 requests in the 11 hours. State what the adversary does **not** have: no training data, no model weights, no vendor infrastructure.
- **Three falsifiable questions.** Examples: (1) Can a bounded character-level perturbation flip the category on at least 10% of a 200-document base set within 1,000 requests? (2) Does the confidence score separate correct from incorrect categories well enough that a threshold reduces errors at an acceptable review rate? (3) Do the logs capture enough of each request and decision to attribute a changed category to a specific input?
- **Deliverables.** Scope statement and authorization, asset inventory with classification, threat model and risk register, test plan with budgets, results table with denominators and baselines, findings with reproduction steps, costed remediation, residual-risk statement, and a reproduction package.
- **Two non-goals.** For example: the vendor's production infrastructure and any denial-of-service or load test; real documents or personal data; model extraction beyond the stated request budget; other endpoints not named in scope.

Five points: one for the decision and asset classification, one for the adversary, one for three questions that could fail, one for the deliverables, one for two non-goals. A scope that names a third-party target or real data earns zero for safety regardless of the rest.

Tag: M16 · LO-33 · Bloom 5 · D4.

## 10. Required elements (gap, claim and comparison, ablation, ethics and limits)

- **Gap.** Prior detector evaluations pace queries evenly; whether the ranking of two detectors holds when the same total request budget is spent in short bursts at a fixed alert budget is unmeasured for this replica. The gap must be stated as a missing comparison, not as "nobody has studied detection."
- **Research question.** "At a fixed total request budget and a fixed 1% alert budget, does bursty pacing reduce the recall of detector A more than detector B on this local document-classification replica, compared with evenly paced queries?"
- **One claim with its planned comparison.** Claim: under bursty pacing, detector A's recall falls by at least 0.15 more than detector B's at the same alert budget. Comparison: run both detectors on the same request stream, same total requests, same seeds, and the same alert budget; include an evenly paced control; report recall and precision with counts and intervals.
- **One ablation or control.** Vary burst length while holding total requests fixed, or shuffle query order to separate content effects from timing effects. Include a naive detector or random baseline so a drop is attributable to pacing rather than to the data.
- **Two ethics or scope limits.** The work runs only on the local replica with synthetic documents; no third-party system, no real user data, and no denial-of-service traffic. The result covers one model, one dataset, and one pacing family, so it does not generalize to production or to other detectors without replication. Pre-register the analysis, and report a negative result if the ranking does not change.

Five points: one for a specific gap, one for a question with a comparison, one for a claim with a matched comparison, one for an ablation or control, one for two ethics or scope limits. A question that cannot fail ("does pacing affect detection?") earns at most one for the question.

Tag: M18 · LO-35 · Bloom 6 · D4.
