# LC-3 Answer Key — Level 3 Practical Defenses

**Scoring:** items 1–6 = 1 point each; items 7–8 = 2 points each; items 9–10 = 5 points each. Total 20. Pass 16/20.

## 1. B — ASR 0.12 under PGD with BPDA at a stated budget, with clean accuracy and the base set reported

A robustness claim needs an adaptive attack, a stated threat model, a denominator, and the clean-accuracy cost. Option B supplies all four and does not overstate the result.

- **A** reports one budget and one attack; a single static result cannot support a general claim.
- **C** reports only clean accuracy, which says nothing about behaviour under attack.
- **D** is an absence of evidence, not evidence of robustness.

Tag: M08 · LO-16 · Bloom 3 · D2.

## 2. B — `GroupShuffleSplit` grouped by customer

Entity leakage occurs when rows from the same customer land on both sides of the split. Grouping by customer keeps every customer in exactly one split.

- **A** is the leakage case.
- **C** balances labels but still splits a customer across sets.
- **D** changes the test size, not the grouping.

Tag: M09 · LO-20 · Bloom 2 · D1.

## 3. C — a safetensors file

Safetensors stores tensors as data and does not execute arbitrary constructors during load. Pickle and joblib deserialize Python objects and can execute code; renaming a pickle does not change its format or risk.

- **A** is the classic unsafe case.
- **B** uses pickle semantics in the common configuration.
- **D** is security by filename.

Tag: M10 · LO-21 · Bloom 2 · D1.

## 4. C — 403

The token is valid, so the caller is authenticated; the missing `stats` scope means the caller is not authorized for this action. That is **403 Forbidden**.

- **A** is a malformed request.
- **B** is missing or invalid credentials.
- **D** is rate limiting.

Tag: M11 · LO-22 · Bloom 2 · D1.

## 5. False

A signature over a manifest authenticates the manifest's contents, not the directory. A file absent from the manifest can be added to the artifact and will not be covered by the signature. The gate must verify that the deployed file set exactly matches the manifest's entries and hashes, and reject extras as well as missing or altered files.

Tag: M10 · LO-21 · Bloom 2 · D1.

## 6. False

A gate that fails open converts a scanner outage into an unverified promotion. Artifact gates should fail closed: if the scan cannot complete, the artifact is not promoted. The exception is a deliberate, logged, time-bounded override with an owner, which is not the same as failing open.

Tag: M10 · LO-21 · Bloom 2 · D1.

## 7. Required elements (two signs, one adaptive test)

Signs of gradient masking, any two:

- The attack's success collapses to near zero while **transfer** attacks from an undefended surrogate still succeed.
- Gradients are zero, saturated, or uninformative, or the loss surface is flat in the input region.
- Attack success is highly sensitive to step size, step count, or random initialization, instead of degrading smoothly with budget.
- The defense randomizes or preprocesses inputs so the attacker's gradient no longer points at the true decision boundary.

One adaptive test:

- **BPDA** (backward pass differentiable approximation) for input transformations, **EOT** (expectation over transformation) for randomized defenses, or a transfer attack from an undefended surrogate at the same budget.

Two points: one for two signs, one for a test that actually addresses obfuscated gradients. "Run PGD again" without changing the approximation is not adaptive.

Tag: M08 · LO-16/LO-17 · Bloom 3 · D2.

## 8. Required elements (three distinctions and a check each)

- **Integrity** means the artifact is the exact bytes that were built and reviewed. Check: SHA-256 of the artifact matches the hash in a signed manifest.
- **Authenticity** means the artifact came from the trusted publisher and was not substituted. Check: verify the manifest signature with a pinned public key in the deployment pipeline.
- **Authorization** means this caller may perform this action on this resource. Check: server-side scope or role enforcement on each endpoint, with a negative test (valid token, missing scope, expect 403).

Two points: one for correct distinctions, one for a concrete check for each. Confusing authenticity with integrity (for example, "the hash proves the author") loses the first point.

Tag: M10 · LO-21 · Bloom 3 · D2 and M11 · LO-22 · Bloom 3 · D2.

## 9. Required elements (three confounds, minimum retest, supported claim)

Three confounds or gaps:

- **The threshold moved.** ASR 0.40 → 0.02 was measured at 0.35 for the defense and 0.50 for the baseline. A lower threshold changes which predictions count and can reduce apparent attack success while raising false positives. The comparison mixes a model change with an operating-point change.
- **The base set changed.** Clean accuracy fell from 0.94 to 0.86, so the defended model has fewer clean-correct rows and a different ASR denominator. Robust accuracy over the full set is not reported.
- **No adaptive attack.** FGSM alone can be defeated by gradient masking. "The drop was large" is a reason to test harder, not a reason to skip the test.
- **No uncertainty or baseline.** One run, no seeds, no confidence interval, and no random-perturbation control.
- **Possible test-set tuning.** If the threshold was chosen on the evaluation set, the reported operating point is optimistic.

Minimum retest:

1. Fix one threshold chosen on clean validation data and evaluate both models at it; also report the operating-point curve if recall was the reason for the change.
2. Use the same held-out base set and state the count of clean-correct rows.
3. Run FGSM and PGD at a stated budget with BPDA or EOT, plus a transfer check.
4. Report clean accuracy, ASR with its denominator, robust accuracy, and false-positive rate at the deployed threshold, over at least three seeds with intervals.
5. Compare against the undefended model under the identical protocol.

What the current numbers support: at threshold 0.35, on this test set, under FGSM at the tested budget, the defended model showed ASR 0.02 versus 0.40 for the undefended model, at a clean-accuracy cost of 0.08. They do **not** support a claim of adaptive robustness, a claim that the defense will hold at threshold 0.50, or a deployment recommendation. The threshold change may explain part of the apparent gain.

Five points: up to three for confounds, one for a retest that fixes the threshold and adds an adaptive attack, one for correct scoping of the current claim. A retest that only adds PGD but keeps the mismatched thresholds earns at most one for the retest.

Tag: M08 · LO-16/LO-18 · Bloom 4 · D3.

## 10. Required elements (four controls, negative tests, residual risk, evidence)

Controls across the supply chain and serving path:

| Control | Negative test |
|---|---|
| **Signed artifacts and verification at the registry.** The registry rejects uploads without a valid signature from a pinned publisher key. | Upload an unsigned artifact and a tampered artifact with a copied signature; both must be rejected and logged. |
| **Hash-locked dependencies and a reproducible build.** The build installs only pinned versions and fails on a hash mismatch. | Substitute a different wheel of the same version or add an unpinned dependency; the build must fail. |
| **API authentication and per-caller authorization.** Every endpoint requires a valid token and checks the scope for the requested action; quotas are enforced per caller. | Call with no token (expect 401), with a valid token lacking the scope (expect 403), and beyond the quota (expect 429). |
| **Input validation and monitoring.** The API validates schema, type, and range; requests and decisions are logged with an audit trail and an alert on anomaly. | Send a malformed payload and a burst that violates the quota; the API must reject the payload, log both events, and raise the alert. |

**Residual risk:** a compromised publisher signing key or an insider with registry write access can still promote a correctly signed malicious artifact; signing proves origin under the key, not intent. A second acceptable residual risk is that input validation covers known schema violations but not semantically valid adversarial inputs.

**Evidence that the gate works:** the negative tests run in CI and fail the build when a control is removed; the registry audit log shows the rejected uploads with hashes and actors; the promotion record shows the verified signature and manifest; and a clean-checkout deployment reproduces the same artifact hashes.

Five points: up to three for four controls with a test each, one for a specific residual risk, one for an evidence gate that a reviewer could check. "Add authentication" without a negative test earns no test credit for that row.

Tag: M10 · LO-21 · Bloom 5 · D4 and M11 · LO-22/LO-23 · Bloom 5 · D4.
