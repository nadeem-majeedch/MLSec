# Knowledge Check Answers — QZ-16

**Module 16 · 10 items · 15 points**

## 1. (1 point)

**B.** A scope statement defines the system, the decision, the owner, the versions, and the non-goals. Without it, every later activity is unanchored. A technique list is not an assessment, a robustness curve is one measurement, and a penetration test may be part of the work but is not the scope.

## 2. (1 point)

- **A — public.** It is intended for disclosure and needs integrity protection, not confidentiality.
- **B — confidential.** Transaction features can cause financial and privacy harm.
- **C — restricted.** A signing key can forge artifact promotion and compromise the supply chain.
- **D — internal.** Aggregated volume is not public but carries lower harm than record-level features.

The classification determines handling: access control, encryption, retention, and logging. A key at "confidential" rather than "restricted" is a common misclassification.

## 3. (2 points)

A finding needs a threat, a test that could fail, a base set, a budget, a metric with a denominator, and an interpretation. "PGD failed" supplies none of these. It may mean:

- the attack was underpowered (too few steps, no restarts, bad step size);
- the defense caused gradient masking, so the attack failed without removing the vulnerability;
- the evaluation set or threshold changed, so the comparison is invalid;
- the success criterion was undefined, so "failed" is an opinion.

At most, the result is evidence that one PGD configuration did not find an example on one base set. That is a scoped negative result, not a finding that the system is robust.

## 4. (2 points)

Defects:

- **No threat or hypothesis.** It does not say which risk it addresses or what would count as success.
- **No budget or base set.** "Reasonable epsilon" and "the results" are undefined.
- **No oracle.** "Inspect the results" has no pass/fail rule.
- **No evidence or metric.** Nothing says what is recorded or over which denominator.

Rewritten example:

> **T-11.** Threat R-02: an attacker with feature access can force misclassification. Hypothesis: at ε = 0.10 in the scaled feature space, PGD with 20 steps and 5 restarts raises the targeted misclassification rate above 0.20 on the frozen 540-row holdout. Oracle: success if the rate exceeds 0.20 with a 95% interval excluding 0.20; failure otherwise. Evidence: `t11_pgd.csv`, seed 42, run record.

A different technique is acceptable if it fairly tests the same hypothesis.

## 5. (1 point)

A zero-budget control runs the attack pipeline with no effective perturbation: ε = 0, zero poisoned rows, no trigger, or the clean corpus. The predictions should be identical to the baseline apart from sampling noise. A nonzero effect usually indicates a measurement bug: misaligned labels, nondeterministic preprocessing, a threshold change, or evaluation data contaminating training. It is the cheapest check in the assessment.

## 6. (2 points)

Changing the threshold changes the operating point, so the lower attack success may come from the threshold rather than the defense. The comparison mixes two interventions.

Fixes:

1. Hold the threshold fixed at the baseline value and compare attack success at that operating point; report the defense's chosen threshold separately.
2. Report the full trade-off curve: attack success and false-positive rate across thresholds for both models, so the reader can compare at equal false positives.

A third option is to rerun the baseline at the new threshold and report both differences, but the curve is usually clearer.

## 7. (2 points)

Missing elements (any four):

- **Threat and adversary:** which risk, with what knowledge, capability, access, and budget.
- **Evidence:** the test, base set, n, metric, and artifact.
- **Impact:** what decision or asset is affected, and how.
- **Root cause:** why the behavior occurs.
- **Existing controls:** what is already in place.
- **Recommendation and retest:** what to change and how to verify it.
- **Residual risk:** what remains after the fix.
- **Severity inputs:** impact, likelihood, exposure, and control gap.

"We changed several features" is not reproducible, and "fix the model" is not actionable.

## 8. (1 point)

A detection control can reduce exposure immediately and generate evidence for further work, at low cost and disruption. Retraining is a multi-week experiment with uncertain benefit and a clean-accuracy cost. If the attack is currently invisible, making it visible may reduce more risk per unit of effort than a prevention that has not been evaluated. The two are complementary: detection buys time for prevention.

## 9. (1 point)

**C.** It names what was tested, what control now applies, and what remains outside the tested path. A and B overclaim; D is uninformative without the remaining paths and their limits.

## 10. (2 points)

The report must be reconciled before release. Either the summary is wrong or the findings are misclassified; both are serious. The mismatch matters because:

- the decision owner may approve the system based on the summary;
- an auditor who reads the findings will lose trust in the whole report;
- it suggests the severity rubric or the review process was not applied consistently.

The correct action is to resolve the discrepancy, document why it occurred, and have a second reviewer check that the executive summary, findings table, and recommendations agree.
