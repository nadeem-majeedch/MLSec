# QB-01 Answer Key — Question Bank

**Scoring:** 24 multiple-choice × 1 = 24; 12 true/false × 1 = 12; 12 short answer × 2 = 24; 8 scenarios × 4 = 32. Total 92.

For written items, award points for the **required elements**, not for matching wording. A conclusion with no reasoning earns half credit.

---

## Section A — Foundations

### A1 — B

Running an attack against an isolated local replica with synthetic data is the authorized pattern. The other three act on systems or data the learner does not own or have written permission to test.

- **A** targets a third party's public service.
- **C** scans a network without authorization.
- **D** uses leaked data and a former employer's system.

Tag: M00 · LO-29 · Bloom 2 · D1.

### A2 — A

Fitting the scaler before the split lets it learn the mean and variance of the test rows, so test information leaks into preprocessing. Fit on training data only, then transform validation and test with the fitted object.

- **B** is a performance concern, not a leakage mechanism.
- **C** is unrelated; scaling does not change class balance.
- **D** is false; the split size is fixed by the call.

Tag: M01 · LO-01 · Bloom 3 · D2.

### A3 — B

At 1% prevalence, a model that predicts "not fraud" for every row reaches 99% accuracy while finding no fraud. Recall on the positive class, read together with precision or PR-AUC, shows whether the model finds the cases that matter.

- **A** is dominated by the negative class.
- **C** is an optimization signal, not a deployment metric.
- **D** is a property of the data, not performance.

Tag: M02 · LO-01 · Bloom 3 · D2.

### A4 — C

A goal is the outcome the adversary wants; a capability is what the adversary can do. Causing a targeted misclassification is a goal. Sending queries, using an account, and spending time are capabilities or resources.

Tag: M03 · LO-02 · Bloom 2 · D1.

### A5 — C

$3 \times 5 = 15$, which falls in the 10–16 high band. If you chose medium, check the band boundaries rather than the multiplication.

Tag: M03 · LO-03 · Bloom 2 · D1.

### A6 — D

MANAGE covers risk treatment, prioritization, response, and monitoring of residual risk. GOVERN sets policy and accountability; MAP establishes context and identifies risks; MEASURE analyzes and assesses them.

Tag: M03 · LO-30 · Bloom 2 · D1.

### A7 — True

The course authorizes local, isolated replicas with synthetic or licensed data. Isolation and synthetic data are what make the offensive work acceptable; they do not authorize testing a third-party system.

Tag: M00 · LO-29 · Bloom 2 · D1.

### A8 — False

Time-ordered data need a chronological split (train on earlier periods, test on later ones). A random split lets future information into training and inflates deployment performance. Grouping may also be needed if entities repeat.

Tag: M02 · LO-01 · Bloom 2 · D1.

### A9 — False

Rejected threats are decisions with reasons and reopening conditions. Deleting them hides the reasoning and forces the same debate at every review. Record the threat, why it was rejected, and what would change the decision.

Tag: M03 · LO-03 · Bloom 2 · D1.

### A10 — Required elements (two checks)

Any two:

- A feature timestamp that is recorded after the outcome or after the prediction time.
- A single feature with near-perfect AUC or a correlation with the target that is implausible for the domain.
- Duplicate or entity overlap between train and test.
- A feature that is only populated for one outcome class.
- Domain review of each feature's collection time and process.

Tag: M01 · LO-01 · Bloom 3 · D2.

### A11 — Required elements

At 1% prevalence, predicting the majority class yields 99% accuracy while missing every positive. Accuracy is dominated by true negatives and does not show the cost of false negatives. Report recall with precision (or PR-AUC) and the confusion matrix; state the base rate with the metric.

Tag: M02 · LO-01 · Bloom 3 · D2.

### A12 — Required elements (one preventive, one detective, with costs)

Preventive examples:

- Authentication plus per-account quotas: cost is friction and reduced access for legitimate heavy users.
- Output minimization (labels only, rounded confidence): cost is reduced utility and calibration.
- Watermarking or query fingerprinting: cost is fidelity or utility loss and possible false attribution.

Detective examples:

- Per-account query-pattern monitoring: cost is false positives and analyst time.
- Canary or extraction-detection queries: cost is additional query overhead and maintenance.

A response with two preventive controls but no detective control earns at most half credit. "Use encryption" is not an extraction control.

Tag: M03 · LO-04 · Bloom 3 · D2.

### A13 — Required elements (three errors, directions, corrected protocol)

- **Preprocessing before the split:** the scaler learns test statistics, so the score is optimistic.
- **Patient overlap:** the same patient in train and test is entity leakage, so the score is optimistic and does not estimate performance on unseen patients.
- **Threshold chosen on test:** the reported operating point is tuned to the evaluation set, so it is optimistic and not reproducible on new data.

Corrected protocol (four steps):

1. Split by patient first, using a grouped split; verify no patient appears on both sides.
2. Fit preprocessing only on the training portion; transform validation and test separately.
3. Select the threshold on a validation set or with cross-validation inside training, never on test.
4. Evaluate once on the held-out test set, record seeds, versions, and split hashes, and report the base rate and confusion matrix.

Tag: M01, M02 · LO-01 · Bloom 4 · D3.

### A14 — Required elements (four register rows plus a rejected threat)

A complete register has four rows with all fields. A representative answer:

| Threat | Impact | Likelihood | Score / band | Control | Owner |
|---|---:|---:|---|---|---|
| Scan perturbation downgrades an urgent finding | 4 | 3 | 12 high | Input validation, distribution monitor, radiologist review for borderline cases | Clinical lead |
| Poisoned intake labels skew triage | 4 | 2 | 8 medium | Label provenance, duplicate/conflict checks, audit sampling | Data owner |
| Public API extraction of model behavior | 2 | 3 | 6 medium | Authentication, quotas, per-account monitoring | Security lead |
| Service outage delays urgent cases | 4 | 2 | 8 medium | Redundancy, failover, manual fallback | Operations lead |

Rejected example: physical theft of the server, rejected because it is controlled by facility access and is outside the model's trust boundary; reopening condition is a change in hosting or access control. The reason and reopening condition must be recorded, not just "out of scope."

The scenario must use synthetic data and a local model; a register built on real patient records is not acceptable.

Tag: M03 · LO-03 · Bloom 4 · D3.

---

## Section B — Core attacks

### B1 — B

Attack success is only comparable at the same norm, budget, base set, and metric. A 90% result at a large L∞ budget on all rows is not evidence of a stronger attack than 60% at a small budget on clean-correct rows.

- **A** can matter, but the missing budget/base set is the immediate blocker.
- **C** is irrelevant.
- **D** is irrelevant to the attack result.

Tag: M04 · LO-05 · Bloom 2 · D1.

### B2 — C

Accuracy is an aggregate availability metric. A targeted poisoning attack can leave it unchanged while redirecting a chosen class or decision. The experiment has not measured the protected outcome, so it cannot conclude that the attack failed or that the model is robust.

- **A** overreads an aggregate metric.
- **B** is unsupported for the same reason.
- **D** is false; the rate is feasible.

Tag: M05 · LO-08 · Bloom 3 · D2.

### B3 — C

Attack effect is the difference from the clean baseline: $0.95 - 0.10 = 0.85$, or **85 percentage points**. The raw 95% ASR includes behavior the clean model already exhibits.

- **A** is the raw ASR.
- **B** is the baseline.
- **D** is the complement of the ASR, not the effect.

Tag: M06 · LO-10 · Bloom 2 · D1.

### B4 — C

The full probability vector carries confidence over every class, which supports distillation, margin-based membership scores, and inversion. A hard label carries one bit of supervision; top-1 confidence carries less than the full distribution.

- **A** and **B** reveal less.
- **D** is metadata, not behavior.

Tag: M07 · LO-12 · Bloom 2 · D1.

### B5 — B

Computing gradients on a local source model and applying the perturbation to a different target is a transfer attack. It is black-box with respect to the target because no target gradients or queries are used.

- **A** would require target gradients.
- **C** changes training data.
- **D** reconstructs inputs.

Tag: M04 · LO-06 · Bloom 2 · D1.

### B6 — C

Fidelity measures agreement with the teacher, not correctness. A surrogate can match a teacher that is itself wrong on 30% of the task, so high fidelity does not prove data theft or a good model. Report fidelity and task accuracy separately.

- **A** is not established by fidelity.
- **B** is not given; the teacher's accuracy may differ from the surrogate's.
- **D** is false; the two metrics can diverge.

Tag: M07 · LO-13 · Bloom 3 · D2.

### B7 — True

A poison rate without a denominator is ambiguous. The course uses the clean training-set size, and the report should also state the poisoned count. The augmented-set rate is context, not the poison rate.

Tag: M05 · LO-08 · Bloom 1 · D1.

### B8 — False

ASR must be paired with clean accuracy, the clean-model baseline on the same triggered rows, and ideally a false-trigger measure. A high ASR alone does not show that the trigger is specific or that ordinary behavior is preserved.

Tag: M06 · LO-10 · Bloom 2 · D1.

### B9 — True

At low prevalence, precision and the false-positive cost dominate. A model can have a high ROC-AUC and still be useless at a 1% FPR budget. TPR at a fixed low FPR describes the operating point a real auditor or attacker would use.

Tag: M07 · LO-14 · Bloom 2 · D1.

### B10 — Required elements (two reasons)

Any two:

- The physical channel (camera, lighting, distance, motion) may not realize the digital perturbation.
- Resizing, compression, or preprocessing can remove or change the perturbation.
- The deployment distribution differs from the test set.
- The attacker may not control the capture conditions or timing.
- A digital L∞ bound does not describe physical capture constraints.

Tag: M04 · LO-07 · Bloom 3 · D2.

### B11 — Required elements

The screen assumes the reference rows are clean, drawn from the same legitimate distribution, and not influenced by the attacker. It fails if the reference set is poisoned or shifted, or if a clean-label attack places correctly labelled rows near the target boundary where they look plausible. It also needs a threshold chosen on separate data and a measured false-positive cost.

Tag: M05 · LO-09 · Bloom 3 · D2.

### B12 — Required elements

An inversion output is an input that scores highly for a class under a prior; it may resemble a prototype or a memorized record but is not proof that a specific record was used. A recovered record would require evidence linking the output to one training example. The distinction matters because harm to an individual (disclosure) is different from a representative or group-level reconstruction, and the claim must not overstate either.

Tag: M07 · LO-15 · Bloom 3 · D2.

### B13 — Required elements (settings, base set, metrics, baseline, adaptive check, interpretation)

- **Attack settings:** L∞ norm, PGD with a stated step size and count (for example 40 steps, α = ε/10), three restarts, pixels clipped to [0, 1]; run separately at each ε.
- **Base set:** a frozen set of rows the clean model classifies correctly, with the count stated; use the same rows across budgets.
- **Metrics:** ASR on the base set and robust accuracy over the full evaluation set, plus clean accuracy.
- **Baseline:** the undefended model at the same budgets, and a zero-perturbation or random-noise control.
- **Adaptive check:** if preprocessing is present, use BPDA or an equivalent; otherwise test a stronger attack (more steps/restarts) and a transfer attack.
- **Interpretation:** a negative result at these settings means the attack failed under this configuration; it is a lower bound, not proof of robustness, and it does not generalize to other budgets, models, or physical conditions.

Tag: M04, M08 · LO-07, LO-16 · Bloom 4 · D3.

### B14 — Required elements (backdoor and membership tests, baselines, limits)

Backdoor:

- Scan a declared family of candidate triggers (positions, patches, value patterns) on held-out source-class inputs; report the target-class rate and the best position.
- Baseline: the clean model's target rate on the same triggered rows; also report clean accuracy and a false-trigger measure on benign inputs.
- Limit: only the tested trigger family is covered; a negative result is not proof of absence.

Membership inference:

- Build member and nonmember candidate pools from synthetic data; compute a score (for example, confidence or loss) and report TPR at FPR ≤ 1% and ≤ 5%, with the pool prevalence.
- Baseline: a random scorer or a score that ignores the model; report precision at the stated prevalence.
- Limit: the result depends on the score, the pool, and the distribution; it is not proof about any individual record, and without training data the membership labels are simulated.

Both tests run only on the local model with synthetic data. "No backdoor and no membership signal" is not a supportable conclusion from a bounded test; state what was tested and what remains unknown.

Tag: M06, M07 · LO-10, LO-14 · Bloom 4 · D3.

---

## Section C — Defenses and secure engineering

### C1 — B

An adaptive result names the defense-aware attack, the budget, the base set, and both clean and robust accuracy. ASR 0 under FGSM is a weak-attack result; clean accuracy says nothing about robustness; no attack is no evidence.

- **A** may reflect an underpowered attack.
- **C** is a utility metric.
- **D** is an absence of evidence.

Tag: M08 · LO-16 · Bloom 3 · D2.

### C2 — A

Adversarial training optimizes against worst-case perturbations, which usually reduces clean accuracy while raising robust accuracy. The trade-off must be measured and reported at the stated budget; it is not a free improvement.

- **B** is not the usual result.
- **C** ignores the documented trade-off.
- **D** is false; evaluation is still required.

Tag: M08 · LO-17 · Bloom 2 · D1.

### C3 — B

Grouping by customer keeps all rows for a customer on one side of the split, preventing entity leakage. A random row split can place the same customer in both sets; stratification balances labels but not entities; a larger test set does not fix overlap.

Tag: M09 · LO-20 · Bloom 2 · D1.

### C4 — C

A SHA-256 manifest establishes integrity: the bytes match the recorded version. A signature adds authenticity (who attests), an SBOM adds inventory, and a model card documents intended use and performance.

- **A** is an inventory, not a byte-level integrity check.
- **B** is authenticity and integrity under a key, but the question asks for integrity specifically.
- **D** is documentation.

Tag: M10 · LO-21 · Bloom 2 · D1.

### C5 — D

429 Too Many Requests tells an authenticated, authorized caller that a quota or rate limit is exhausted. 401 is missing or invalid authentication; 403 is a known identity without permission; 400 is a malformed request.

Tag: M11 · LO-22 · Bloom 2 · D1.

### C6 — B

A rollback decision needs a measured attack outcome on the same captured batch for the current and previous checkpoints, plus clean accuracy. Clean accuracy alone can stay high while evasion succeeds; alert count and model size do not measure recovery.

Tag: M11 · LO-23 · Bloom 3 · D2.

### C7 — False

One blocked PGD run is a lower bound on attacker capability. The attack may be underpowered, or the defense may mask gradients. An adaptive attack and a stated budget are required before calling the defense robust.

Tag: M08 · LO-18 · Bloom 2 · D1.

### C8 — False

Retention supports audit, incident response, reproduction, and legal obligations. Deleting the exact version after training can make the deployed model's provenance unverifiable and prevent a clean-checkout reproduction. Retention and deletion policy belongs to the data owner, not to convenience.

Tag: M09 · LO-20 · Bloom 2 · D1.

### C9 — False

A manifest defines the verification boundary. Files not listed are not covered by its hash or signature; an attacker can replace them while the signature still verifies. Every runtime artifact must be listed and verified.

Tag: M10 · LO-21 · Bloom 2 · D1.

### C10 — Required elements (two signs and one adaptive test)

Signs: near-zero or shattered gradients; high transfer success but low white-box ASR; unstable results under small input changes or randomness; a defense that reports a large drop only for one gradient attack.

Adaptive tests: BPDA with a differentiable substitute; EOT for randomness; a score-based or transfer attack; more steps and restarts; an attack that accounts for preprocessing.

Tag: M08 · LO-16 · Bloom 3 · D2.

### C11 — Required elements (three fields)

Any three: source code reference or commit; input artifact hashes; parameters and configuration; environment and library versions; random seed; timestamp and operator; output schema or row count. The output hash alone identifies the result but not how it was produced.

Tag: M09 · LO-20 · Bloom 2 · D1.

### C12 — Required elements

Rollback restores model weights, not the whole system. The attacker may still hold valid credentials, have modified training data or other artifacts, or have planted persistence elsewhere. Containment also needs credential rotation, scope review, artifact verification, and post-rollback monitoring; the rollback must be validated against the attack, not just against clean accuracy.

Tag: M11 · LO-23 · Bloom 3 · D2.

### C13 — Required elements (three confounds or gaps and a minimum retest)

Confounds/gaps:

- The decision threshold changed, so the operating point is not comparable.
- Clean accuracy fell by 8 points, so the ASR comparison is at a different utility level.
- No adaptive attack was run, so the defense may be masking gradients.
- The base set, budget, and denominator are not stated.
- A single run has no uncertainty.

Minimum retest: restore one threshold for both models; use the same frozen base set and budget; run PGD with BPDA or another adaptive attack; compare at equal clean accuracy or report the clean cost; repeat across seeds and report intervals. Without those, the 0.02 is a result for one weak attack at one operating point, not a robustness claim.

Tag: M08 · LO-16, LO-18 · Bloom 4 · D3.

### C14 — Required elements (four controls, negative tests, residual risk)

Controls:

1. **Signed manifest and hash verification** at promotion: negative test is flipping one byte and confirming rejection.
2. **Provenance or attestation check** for the approved source and builder: negative test is an artifact from an unapproved commit.
3. **SBOM and dependency scan** with pinned hashes: negative test is a known-bad or unpinned package.
4. **Authentication, scopes, and quotas on the serving API**: negative test is no token, a wrong scope, and a quota-exceeding request.

Additional acceptable controls: input validation and safe output handling, with malformed-input negative tests; artifact quarantine and rollback.

Residual risk: a compromised signing key or build system can produce valid evidence; a scanner can miss a novel issue; an insider with promotion rights can bypass policy. State one with an owner and monitoring.

Tag: M10, M11 · LO-21, LO-22 · Bloom 4 · D3.

---

## Section D — Advanced and emerging security

### D1 — B

Secure aggregation hides individual updates from the server by summing masked contributions. It protects confidentiality, not integrity: a malicious client can still contribute a poisoned update, and it is not a differential-privacy mechanism or a sybil defense.

Tag: M12 · LO-24 · Bloom 2 · D1.

### D2 — B

ε is meaningful only with δ (for approximate DP), the neighboring relation, the mechanism and its sensitivity assumptions, and the composition across releases. Without those, two ε = 1 numbers may describe very different guarantees.

- **A** and **D** are utility and platform facts.
- **C** affects sensitivity only through the query definition.

Tag: M13 · LO-19 · Bloom 2 · D1.

### D3 — B

Stability under a stated perturbation supports continuity of the explanation, not faithfulness to the model's decision process. A stable explanation can be consistently wrong. Faithfulness needs a separate test, such as deletion/insertion or a known-behavior check.

Tag: M14 · LO-31 · Bloom 2 · D1.

### D4 — B

Least privilege is enforced by the tool and gateway: a recipient allowlist, scope checks, approval for high-impact actions, and egress rules. A system prompt is an instruction to a probabilistic model, not an authorization boundary.

Tag: M15 · LO-27 · Bloom 2 · D1.

### D5 — False

DP protects disclosure; poisoning is an integrity attack. A malicious client can submit a poisoned update even if the aggregation hides individual contributions. DP and robust aggregation address different threats and must be combined deliberately.

Tag: M12, M13 · LO-19, LO-24 · Bloom 2 · D1.

### D6 — True

Retrieved content is untrusted data. It may inform an answer, but it cannot grant itself authority or permissions. Instruction hierarchy plus code-level tool authorization keeps the document from becoming an instruction source.

Tag: M15 · LO-26 · Bloom 2 · D1.

### D7 — Required elements (two reasons)

Any two:

- No δ, so approximate-DP claims cannot be checked.
- No neighboring relation or unit of privacy, so it is unclear what one record means.
- No clipping or sensitivity calculation, so the noise scale may not match the query.
- No composition or number of releases, so the total budget is unknown.
- No mechanism or trust model, so the guarantee cannot be reproduced or audited.

Tag: M13 · LO-19 · Bloom 3 · D2.

### D8 — Required elements

Demographic parity constrains the selection rate, while equalized odds constrains TPR and FPR. When base rates or score distributions differ, a model can select the same fraction from each group while making different types of errors. The metrics constrain different quantities, and satisfying one can force a trade-off in the other. The choice among them is normative, not purely technical.

Tag: M14 · LO-32 · Bloom 3 · D2.

### D9 — Required elements (four controls, metric, benign check, two risks)

Controls:

1. **Provenance and trust labels** on retrieved documents; treat them as data and quarantine untrusted content.
2. **Instruction hierarchy and delimiters** so retrieved text cannot override policy.
3. **Least-privilege tools**: `read_file` restricted to non-confidential paths; `create_ticket` validates fields and refuses attachments of restricted files.
4. **Approval and egress control** for attaching files or creating tickets with external recipients; log the action and the approver.
5. **Output and action validation** before the ticket is created; a canary can detect exfiltration attempts.

Metric: attack success on a fixed set of synthetic injected documents, with the denominator; benign task completion on a separate set. Benign false-positive check: run legitimate policy documents and measure blocked or altered tasks, not only attacks.

Risks: a novel paraphrase or encoding can evade detection; a trusted document can be poisoned; the tool implementation can have a bug; approval fatigue can lead to rubber-stamping. The result is scoped to the local replica and the tested documents, not a claim of security.

Tag: M15 · LO-26, LO-27 · Bloom 4 · D3.

---

## Section E — Applied assessment and research

### E1 — B

A usable finding states the budget, base set, counts, metric, baseline, affected scope, and a reproduction path. "Vulnerable," "fix the model," and "high risk" are conclusions without evidence or an owner.

- **A** and **D** are unquantified.
- **C** is a recommendation with no mechanism or cost.

Tag: M16 · LO-33 · Bloom 3 · D2.

### E2 — B

An ablation changes one factor: the defense, with the attack, seeds, budget, and data held fixed. Changing data and model together confounds the result; removing the baseline removes the comparison; more prose is not an experiment.

Tag: M18 · LO-35 · Bloom 3 · D2.

### E3 — False

The rules of engagement define authorization. An out-of-scope action is unauthorized even if it finds a real issue; the team must stop and renegotiate. "It found something" does not retroactively authorize the action.

Tag: M17 · LO-34 · Bloom 2 · D1.

### E4 — Required elements (three elements)

Any three: a named owner; an effort or cost estimate; the residual risk after the control; a verification or acceptance criterion; a target date or priority. A recommendation without an owner and a cost cannot be scheduled or evaluated.

Tag: M16 · LO-33 · Bloom 2 · D1.

### E5 — Required elements (gap, claim–evidence, ablation, scope and ethics)

- **Gap:** DP noise is usually evaluated on overall utility; it is unclear whether a fixed privacy budget widens the accuracy gap between subgroups, and existing reports rarely separate the noise effect from the model's baseline bias.
- **Question:** "At a fixed ε and clipping range, does the subgroup accuracy gap in a local credit model increase relative to the non-private baseline, and by how much?"
- **Claim–evidence pair:** Claim — the gap widens with noise. Evidence — subgroup accuracy and gap with confidence intervals across seeds, at the same ε and clipping, compared with the non-private model.
- **Ablation:** hold the data, model, and clipping fixed; vary ε (or noise scale) and compare the gap; include a non-private control and a gap measured before noise. This separates the noise effect from the underlying model bias.
- **Scope and ethics:** local synthetic or licensed data, one model family, no real applicants, no third-party system; the result is an empirical fairness observation, not a causal claim or a DP guarantee.
- **Limits:** one dataset and model; subgroup sample sizes may be small; the fairness metric choice is normative; DP protects records, not group fairness.

Tag: M18 · LO-35 · Bloom 5 · D3.
