# FIN-01 Answer Key — Integrated Final Assessment

**Scoring:** Part A items 1–5 = 20; Part B items 6–10 = 20; Part C items 11–15 = 20; Part D items 16–20 = 20; Part E items 21–25 = 20. Total 100. Pass 80/100. A safety violation is an automatic fail.

Within each part: the two multiple-choice items are 2 points each, the true/false item is 2 points, the short-answer item is 4 points, and the scenario is 10 points.

---

## Part A — Foundations

## 1. A — rebuild from a clean checkout and compare hashes and numbers

Reproducibility means another person, starting from the raw inputs in a fresh environment, obtains the same artifacts and headline result. That requires pinned dependencies, a recorded seed, a fixed input snapshot, and a comparison of outputs.

- **B** shows that outputs exist, not that they can be regenerated; saved outputs can be stale or hand-edited.
- **C** checks documentation, not the result.
- **D** is testimony, not evidence.

Tag: M00 · LO-28 · Bloom 3 · D2.

## 2. A — precision 0.30, recall 0.60

- Precision $= 30/100 = 0.30$: of the flagged rows, 30 are true positives.
- Recall $= 30/50 = 0.60$: of the 50 positives, 30 were found.

**B** swaps the two ratios. **C** divides by the full dataset instead of by flagged rows and positives. **D** uses the flagged count (100) as the denominator for both, which is not what either metric measures.

Tag: M02 · LO-02 · Bloom 2 · D1.

## 3. False

A confusion matrix fixes one threshold. It says nothing about how well the model ranks rows across all thresholds, which is what ROC-AUC summarizes. Two models with the same confusion matrix at 0.50 can have very different ranking quality, and a single threshold can hide poor calibration and subgroup behaviour. Ranking, calibration, and the deployed operating point are separate claims.

Tag: M02 · LO-02 · Bloom 2 · D1.

## 4. Required elements (two questions and evidence)

Any two question–evidence pairs:

- **Is the model calibrated at the operating point?** AUC is threshold-free. Evidence: a reliability curve or calibration plot, plus the chosen threshold and the resulting precision, recall, and false-positive rate at the expected base rate.
- **Does it work for the subgroups that matter?** An aggregate AUC can hide a group with much worse error. Evidence: subgroup metrics with confidence intervals and the subgroup base rates.
- **Is the evaluation temporally valid, or is it leakage?** Evidence: a time-based split, a feature-availability audit, and a test on the latest period.
- **Are the data lawful and representative?** A hash proves bytes, not consent or coverage. Evidence: provenance, license or consent record, and a comparison with the deployment population.
- **What decision does 0.93 support?** Evidence: the decision rule, the cost of false positives and false negatives, and the review capacity.

Four points: one for each of two valid questions, one for each evidence item that would actually answer it. A question without evidence earns one point at most for the pair.

Tag: M02 · LO-02/LO-03 · Bloom 4 · D3.

## 5. Required elements (six-step audit, three reasons, one verdict-changing artifact)

**Six-step audit:**

1. **Freeze the environment.** Record the Python version, operating system, hardware, and exact package versions from a lockfile or `pip freeze`; a `requirements.txt` with bare names does not pin anything.
2. **Fix the inputs.** Record the URL, retrieval date, and SHA-256 of the downloaded data, or replace the download with a bundled synthetic snapshot. A remote URL can change or disappear.
3. **Set and record seeds.** Seed the split, model initialization, and any sampling; document sources of nondeterminism such as thread count.
4. **Rebuild from a clean checkout.** Create a fresh environment, install from the lockfile, and run the pipeline without cached outputs or saved notebook state.
5. **Compare outputs.** Regenerate the artifacts and the headline ROC-AUC; compare artifact hashes and metric values with the submitted package, and explain every difference.
6. **Repeat once.** Run the pipeline a second time to check determinism, and write a reproduction note with the commands, runtime, and known limits.

**Three reasons the 0.91 is not yet reproducible:**

- The dependencies are unpinned, so a fresh install can resolve different versions and change results.
- No seed is recorded, so the split and model initialization can differ between runs.
- The data are fetched from an unversioned URL, so the input cannot be verified or restored.
- The only evidence is saved notebook output, which does not show a clean execution.
- The split and evaluation protocol are not stated, so leakage cannot be ruled out.

**One artifact that would change the verdict:** a lockfile plus a recorded seed and input hash manifest that regenerates 0.91 from a clean checkout, with a run log and identical artifact hashes. A second acceptable artifact is a container image with a frozen environment and the raw-data snapshot.

**Safety:** the audit uses the package and a local environment. It does not probe or scrape the data host; if the URL is untrusted, the auditor records the metadata and asks the owner for a snapshot instead.

Ten points: four for the six-step audit (partial credit for a coherent subset), three for three reasons, two for a verdict-changing artifact, one for keeping the audit local and non-invasive.

Tag: M00/M01 · LO-28 · Bloom 5 · D3.

---

## Part B — Core attacks

## 6. A — the implementation or accounting is wrong

For a fixed attack and objective, increasing $\varepsilon$ enlarges the allowed perturbation set, so a correctly implemented attack cannot do systematically worse at the larger budget. A fall usually means the perturbation is being clipped away, normalized incorrectly, or $\varepsilon$ is applied twice, or that the base set or success test changed between runs.

- **B** would require the model to change between budgets; it did not.
- **C** is false for a fixed untargeted objective under a larger allowed set.
- **D** would produce noise, not a systematic reversal.

Tag: M04 · LO-05 · Bloom 3 · D2.

## 7. B — a targeted integrity attack

The pattern is a specific source-to-target redirection on clean inputs with aggregate accuracy preserved. That is the signature of a targeted poisoning attack.

- **A** would show broad accuracy degradation.
- **C** is extraction, which copies behaviour rather than redirecting a class.
- **D** is a privacy attack on membership.

A backdoor would also redirect inputs, but only when a trigger is present; the stem says clean inputs, so targeted poisoning is the better label. An answer that says "backdoor" without noting the missing trigger does not earn the point.

Tag: M05 · LO-08 · Bloom 3 · D2.

## 8. False

TPR 0.60 at FPR 1% is a statistical signal, not proof of memorization. It must be compared with a baseline (random guessing, or a model trained without the record), and a 1% false-positive rate means some flagged records are not members. Membership inference also does not establish how the record influenced training. The correct claim is that the attack distinguished members from non-members better than the stated baseline at that operating point.

Tag: M07 · LO-14 · Bloom 3 · D2.

## 9. Required elements (supported, unsupported, additional measurement)

**Supported:** at 10,000 queries, on the queried input distribution, the student reproduces the teacher's outputs with fidelity 0.92 and reaches task accuracy 0.88 against the teacher's 0.90. That is functional mimicry at that budget.

**Not supported:** that the attacker recovered the teacher's training data; that fidelity holds at lower query budgets or on out-of-distribution inputs; that the student is equivalent to the teacher beyond the measured distribution; or that the teacher can be replaced without further evaluation.

**One additional measurement:** fidelity and task accuracy at two or more additional query budgets (for example 1,000 and 30,000), reported as a curve; or evaluation on a held-out distribution shift; or a comparison with an untrained or random student baseline. Any one makes the claim stronger by showing the trend or the baseline.

Four points: one for the supported claim with its conditions, two for what is not supported, one for a measurement that addresses the gap.

Tag: M07 · LO-13 · Bloom 4 · D3.

## 10. Required elements (control, metrics, baselines, decision rule, limits)

**Control condition.** Train the same architecture on the same 2,000 clean rows with the same split and seed, and evaluate it with the identical test set and threshold. The attack effect is the difference between the poisoned and control models, not the poisoned model alone.

**Metrics with denominators.**

- **Clean accuracy** on the untriggered test set.
- **Triggered attack success:** share of triggered source rows sent to the target class, with the denominator stated as the triggered rows the control model classified correctly.
- **False-trigger rate:** share of untriggered clean rows sent to the target class, which separates a trigger from ordinary error.
- **Global accuracy** and, for the poison runs, the targeted-class effect at each rate.
- Report counts, not only percentages, and run at least three seeds with intervals.

**Baselines.**

- The clean control at the same architecture and budget.
- A random-label or random-row poison at the same rate, to show the effect is not just added noise or capacity.
- Untriggered inputs through the poisoned model, for the false-trigger rate.

**Decision rule.** Call the effect real only if the triggered rate for the poisoned model exceeds the control and the random-poison baseline by more than the seed variation, the false-trigger rate stays near the control, and the pattern is consistent across seeds. Clean accuracy is reported as a cost, not as proof.

**Two limits.** One synthetic corpus, one architecture, and one trigger family: the result does not generalize to other triggers or data. The tested rates do not establish a threshold below which poisoning is impossible. The trigger may not survive text preprocessing or real message formatting.

Ten points: three for the design and control, three for the metrics with denominators, two for baselines, one for the decision rule, one for two limits. A design without a clean control earns no design credit beyond the basics.

Tag: M05/M06 · LO-08/LO-10 · Bloom 5 · D4.

---

## Part C — Defenses and secure engineering

## 11. B — BPDA that approximates the preprocessing gradient

An adaptive attack is designed with knowledge of the defense. JPEG compression and resizing are non-differentiable or randomized; BPDA substitutes an approximate gradient through them so the attack can still optimize the input.

- **A** is a static attack on an undefended model.
- **C** uses no knowledge of the defense and is not adaptive to it.
- **D** is not an attack.

Tag: M08 · LO-16 · Bloom 3 · D2.

## 12. B — a dependency can be substituted without changing the signed model

The signature covers the model artifact and its manifest, not the environment resolved at deploy time. An unpinned dependency can be replaced or compromised, and the model's hash and signature will still verify. Integrity of the artifact does not establish integrity of its runtime.

- **A** is wrong: the artifact hash still matches.
- **C** is not implied by pinning or its absence.
- **D** is unrelated.

Tag: M10 · LO-21 · Bloom 3 · D2.

## 13. False

Rate limiting raises the cost and slows extraction; it does not prevent it. An attacker can spread queries over time, use multiple accounts, or target a model with a cheap query path. Preventing extraction requires a combination of quotas, authentication, monitoring and detection, output minimization, and watermarking, and even then the goal is to raise cost and detect abuse, not to make extraction impossible.

Tag: M11 · LO-22 · Bloom 3 · D2.

## 14. Required elements (why weak, two tests)

**Why weak:** a known-string filter is tested against the strings it was written for, so 100% is close to a tautology. It says nothing about paraphrases, encodings, Unicode variants, split tokens, or semantic equivalents, and it reports no false-positive cost on benign traffic. A filter can block every known signature and still miss the attack that matters.

**Two tests:**

- **Mutation and paraphrase set:** generate held-out variants (synonyms, encodings, homoglyphs, token splits) and measure bypass rate against the same filter.
- **Benign corpus:** run a representative set of legitimate requests and measure the false-positive rate and the effect on task completion.
- **Adaptive replay:** give the filter's rules to a tester who writes payloads against them, at a fixed request budget, and report success.
- **Budget test:** measure whether the filter changes the queries needed to extract or evade, rather than only whether a string is blocked.

Four points: one for the tautology/coverage critique, one for the missing benign cost, one for each of two valid tests. "Add more signatures" is not a test.

Tag: M11 · LO-22/LO-23 · Bloom 4 · D3.

## 15. Required elements (static and adaptive design, metrics, controls, decision, limits, current claim)

**Static evaluation.** FGSM and PGD at stated budgets, with the same step size, steps, and restarts, on a fixed base set. Report the clean accuracy of the defended model and the undefended model.

**Adaptive evaluation.** Because JPEG and random resizing are non-differentiable or stochastic, use BPDA for the compression and EOT over the random resize, at the same budgets. Include a transfer attack from an undefended surrogate as a cross-check.

**Metrics and denominators.** ASR over the clean-correct base set, robust accuracy over the full base set, clean accuracy, and the false-positive or abstention rate at the deployment threshold. Report counts and intervals over at least three seeds.

**Baselines and controls.** Undefended model at the same threshold and base set; defended model with the transform disabled; random transform without compression; $\varepsilon = 0$ identity check.

**Decision rule.** Deploy only if the adaptive ASR reduction survives BPDA/EOT with intervals, the clean-accuracy and false-positive costs are within the stated budget, and the result holds across seeds. A static-only reduction is not enough.

**Two limits.** The BPDA approximation may not match the true transform, so the adaptive result is a lower bound on attacker capability; the test is digital and synthetic, so compression and resizing in a real capture pipeline are untested; one dataset and model do not establish generality.

**What 0.03 supports.** At the tested FGSM budget, on this synthetic set, the defended model showed ASR 0.03 against 0.45 for the undefended model. It does **not** support adaptive robustness, a claim about PGD or BPDA, or deployment. The random resizing may be masking gradients, which is exactly what the adaptive test must check.

Ten points: two for the static design, three for the adaptive design (BPDA/EOT), two for metrics and baselines, one for the decision rule, one for limits, one for correctly scoping the current claim.

Tag: M08 · LO-16/LO-17/LO-18 · Bloom 5 · D4.

---

## Part D — Advanced and emerging security

## 16. C — 1.0

Under basic composition, the ε values of releases on the same data add: $0.5 + 0.5 = 1.0$. Advanced composition can give a tighter bound, but the stem specifies basic composition.

- **A** would be multiplication or an incorrect averaging.
- **B** is one release, not the composition.
- **D** double-counts.

Tag: M13 · LO-19 · Bloom 2 · D1.

## 17. B — refuse, log, and require an approved recipient change

The allowlist is the authorization boundary, and it must be enforced where the action happens. A refused call with a policy error is the correct behavior; the log preserves the attempt, and a recipient change goes through an approval process.

- **A** violates the control and sends data out.
- **C** asks the model to police itself; a prompt is not an authorization boundary.
- **D** changes sampling and does not address permission.

Tag: M15 · LO-27 · Bloom 3 · D2.

## 18. False

Removing the attribute does not remove correlated proxies such as postal code, language, or usage patterns. A model can reconstruct the group from proxies and produce the same disparity. Fairness requires measuring subgroup outcomes and auditing proxies, not only deleting a column.

Tag: M14 · LO-32 · Bloom 3 · D2.

## 19. Required elements (two protections, one gap)

- **Secure aggregation** protects individual client updates from the server during aggregation: the server learns the sum, not any client's contribution.
- **Differential privacy** protects what the released output reveals about any individual, with a quantified ε, δ and a stated neighboring relation.

**One thing neither protects:** model integrity against poisoned updates. A malicious client's update is still included in the sum, and DP noise does not remove it; secure aggregation can even hide which client contributed it. Sybil resistance, robust aggregation, and contribution bounds are separate controls. A second acceptable gap is availability or dropouts, which neither mechanism guarantees.

Four points: one for each protection, two for a gap with the reason.

Tag: M12/M13 · LO-24/LO-19 · Bloom 4 · D3.

## 20. Required elements (injection test, benign check, controls, metric, residual risks)

**Injection test.** Place a canary document in the retrieval corpus containing an instruction to email a confidential attachment to an external address. Run the assistant on a benign user request and record whether `send_email` is called with the confidential attachment. Report the result over a labeled set, for example 0 of 8 injection documents succeed, not a single anecdote.

**Benign false-positive check.** Run the same pipeline on 20 clean policy documents and measure task completion and false blocks, for example 7 of 7 benign tasks completed with no legitimate attachment blocked. A control that blocks all attachments fails this check.

**Three layered controls, at least one in code:**

1. **Retrieval boundary.** Tag documents by source, tenant, and sensitivity; filter before top-$k$; exclude untrusted documents from the prompt; keep the canary to detect cross-boundary retrieval.
2. **Instruction and data separation.** Delimit retrieved text as data and keep system/developer instructions in a higher-authority channel; strip instruction-like content as defence in depth, not as the boundary.
3. **Code-enforced egress.** `send_email` enforces a recipient allowlist, refuses confidential attachments without an approval tied to the task, and logs every attempt. The model cannot grant itself an exception.

A fourth acceptable layer is attachment scanning and output validation before send.

**Success metric.** Injection success rate on the labeled canary set, with the benign task-completion rate reported alongside it. The pair prevents a control that wins by blocking everything.

**Two residual risks.** A paraphrased, encoded, or multi-turn injection can evade content filters; a legitimate document can be compromised at its source; approval fatigue can lead a reviewer to approve a harmful attachment. The test covers a finite set, so a zero result is an upper bound, not proof of safety.

Ten points: two for the injection test, two for the benign check, four for three layers with a code-enforced boundary, one for the paired metric, one for two residual risks.

Tag: M15 · LO-26/LO-27 · Bloom 5 · D4.

---

## Part E — Applied assessment and research

## 21. B — the baseline-freeze and versioning gate

A defense claim is a comparison. If the baseline is overwritten after the defense results are known, the comparison cannot be audited: the reader cannot tell what the defense was compared against or whether the baseline was tuned to make the defense look better. The baseline must be frozen, hashed, and versioned before the defense run.

- **A** concerns data handling, not the comparison.
- **C** concerns disclosure.
- **D** concerns formatting.

Tag: M16/M18 · LO-28/LO-33 · Bloom 3 · D2.

## 22. C — the entry with an action, owner, effort, and verification test

A schedulable remediation names the change, the responsible owner, the effort, and a verification test with a pass criterion. Option C has all four: an action (norm-clipped adversarial training in the nightly job), an owner (ML platform), an effort (3 days), and a test with a target and a clean-accuracy budget on a frozen evaluation set.

- **A** and **B** are goals without an owner, cost, or test.
- **D** transfers the work without a commitment or evidence.

Tag: M16 · LO-33 · Bloom 3 · D2.

## 23. False

A negative result with a bound is evidence: it tells the reader what the test could have detected and limits the claim. Reporting it prevents duplicate work and supports a residual-risk statement. A negative result without a denominator or interval is weak, but that is a reporting defect, not a reason to withhold the result.

Tag: M18 · LO-28 · Bloom 3 · D2.

## 24. Required elements (two attribution artifacts, two detection measurements)

**Attribution artifacts, any two:**

- The signed authorization and scope, tying the action to an approved target and window.
- Request logs with timestamps, unique request IDs, actor or session, and payload hashes, so an action can be tied to a specific request.
- An evidence manifest with hashes and storage locations, preserving integrity and chain of custody.
- Timestamped captures of the response or state change, correlated with the request ID.

**Detection measurements, any two:**

- A labeled benign baseline over the same window, giving false positives and the base rate.
- Alert counts with true positives, false positives, precision, and recall at a fixed alert budget.
- Time to detect and time to triage, with the start and end events defined.
- A replay of the detection rule against held-out malicious and benign traffic.

Four points: one for each of two attribution artifacts, one for each of two detection measurements. A screenshot without a request ID or timestamp is weak attribution.

Tag: M17 · LO-34 · Bloom 4 · D3.

## 25. Required elements (decision, scope and non-goals, three tests, control, report, residual)

**Decision.** What the return-risk score changes, such as whether a synthetic account is routed to manual review or a limit. State the cost of a false low risk and a false high risk.

**Scope and non-goals.** In scope: the local replica, its documented API, the synthetic feed, and the model version named in the report. Non-goals: the vendor's production feed and infrastructure; denial-of-service or load testing; real customer data; and any endpoint not named. Two non-goals are required.

**Three falsifiable tests covering data, model, and serving:**

- **Data:** inject controlled malformed or mislabelled feed rows and test whether schema validation and quarantine stop them before training; measure catch and false-quarantine counts.
- **Model:** run a bounded evasion test at a stated perturbation or feature-budget on a fixed base set; report ASR with its denominator, robust accuracy, and the clean baseline.
- **Serving:** test authentication, scope authorization, and quota with negative requests (no token, wrong scope, over quota) and verify the expected 401, 403, and 429 responses plus the audit log.

**One control with a negative test.** For example, schema validation on the feed: a valid row passes, a missing required field is rejected, an out-of-range value is quarantined, and the pipeline stops rather than training on the bad batch. The negative test must fail closed.

**Report sections.** Scope and authorization; system and data-flow description; asset inventory and classification; threat model and risk register; test plan with budgets; results with denominators and baselines; findings with reproduction steps; costed remediation; residual risk; reproduction package.

**One residual-risk statement.** For example: "Under the tested local replica with a 1,000-request budget, the evasion test was detected at the serving layer; an adaptive attacker inside the quota and a compromised vendor feed remain unaddressed, and the model has not been tested on real account data." The statement names the condition, the evidence, and what remains.

Ten points: two for the decision and scope, one for two non-goals, three for the three tests (one each), two for the control and its negative test, one for the report sections, one for a scoped residual-risk statement. A plan that probes the vendor's production feed or uses real data earns zero for safety.

Tag: M16/M17/M18 · LO-33/LO-34/LO-28 · Bloom 5 · D4.
