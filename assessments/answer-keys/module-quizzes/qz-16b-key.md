# QZ-16B Answer Key — Module 16

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — the vendor's hosted training pipeline

A non-goal is explicitly outside the assessment boundary. If the assessment covers the local scoring API you own, the vendor's hosted training pipeline is a different system with a different owner and authorization. It should be named as out of scope, not implied by silence.

- **A, C, and D** are part of the local system or the decision it supports and belong in scope.

Tag: M16 · LO-33 · Bloom 2 · D1.

## 2. B — a frozen base set, fixed attack, and reported metrics

A falsifiable test names the attack, budget, data, base set, and metric, so a result can contradict the expectation. "Review," "check," and "ensure" describe activities, not tests; any outcome can be narrated as success.

Tag: M16 · LO-33 · Bloom 2 · D1.

## 3. False

Without a baseline, the reader cannot tell whether the attack changed anything or whether the model already behaved that way. A finding needs the clean or random comparison, the base set, the budget, and the metric. An unbaselined number is an observation, not a finding.

Tag: M16 · LO-33 · Bloom 2 · D1.

## 4. True

A recommendation without an owner is nobody's job; without cost or effort it cannot be prioritized; without residual risk it implies the problem is gone. The three elements turn a suggestion into a decision the system owner can act on.

Tag: M16 · LO-33 · Bloom 2 · D1.

## 5. Required element

A zero-budget test checks that the attack implementation returns no perturbation and no change in prediction when the budget is zero. If it does not, the implementation has a scaling, projection, sign, or base-set bug, and every larger-budget number is suspect. It is the cheapest validity check in the experiment.

Tag: M16 · LO-33 · Bloom 3 · D2.

## 6. Execution 0.70; pass 0.643; failure 0.214; inconclusive 0.143

- Execution rate: $14/20 = 0.70$.
- Pass rate among executed: $9/14 \approx 0.643$.
- Failure rate among executed: $3/14 \approx 0.214$.
- Inconclusive share: $2/14 \approx 0.143$.

"9 of 10 passed" drops the 2 inconclusive results and all 6 blocked or unrun tests from the denominator. That is a denominator choice, not a result. The report should state all 20 planned tests, how blocked and inconclusive outcomes were handled, and the pass rate against the predeclared plan.

Tag: M16 · LO-33 · Bloom 3 · D2.

## 7. Required elements (two flaws and the correction)

Two of:

- **De-identification is not a public classification.** Removing names and emails does not make transaction features public; combinations of features can be confidential, commercially sensitive, or re-identifiable.
- **The data may be licensed or sensitive.** The project may not have the right to redistribute it, independent of whether it contains direct identifiers.
- **A public commit is irreversible.** Once pushed, the data may be cached, cloned, or indexed; deleting the file later does not undo the exposure.
- **The model can leak training data.** Publishing a model trained on sensitive records can expose information even if the raw table is not published.

Correction: classify the data with its owner, use synthetic or aggregate data for the public portfolio, keep the real extract in a private, access-controlled store, add it to `.gitignore`, and publish only the generator, hashes, and a reproduction recipe. Review the license before any release.

Tag: M16 · LO-33 · Bloom 4 · D3.

## 8. Required elements (a one-page scope)

A complete scope names:

- **Decision:** the approve/deny decision the API supports, the model version, and the owner.
- **Assets and classification:** model, features, thresholds, logs, and evaluation data, each marked public, internal, confidential, or restricted.
- **Adversary:** a bounded profile, for example a black-box API caller with no insider access, a query budget, and no ability to modify training data.
- **Questions:** two or three, such as "Does a bounded feature perturbation change the decision at a measurable rate?" "Does the API expose extraction signal at a stated query budget?" and "Does the proposed input check reduce either effect without unacceptable false declines?"
- **Deliverables:** scope, architecture and data classification, threat model, test matrix, baseline table, experiment outputs, defense evaluation, report, reproduction package, and reflection.
- **Non-goals:** the vendor's infrastructure, production traffic, real customer data, denial of service, social engineering, and any system not owned by the assessor.

The scope must fit on one page, and every test must trace to a question and a risk. A scope that lists techniques rather than a decision is not yet scoped.

Tag: M16 · LO-33 · Bloom 5 · D3.
