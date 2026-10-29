# LC-4 Answer Key — Level 4 Advanced and Emerging Security

**Scoring:** items 1–6 = 1 point each; items 7–8 = 2 points each; items 9–10 = 5 points each. Total 20. Pass 16/20.

## 1. B — individual updates from the server

Secure aggregation lets clients combine updates so the server learns only the aggregate, not any single client's contribution. It protects update confidentiality during aggregation.

- **A** is model integrity, which secure aggregation does not provide: a poisoned update is still hidden inside the sum.
- **C** is differential privacy, which is a separate mechanism with its own guarantee.
- **D** is sybil resistance, which needs identity and contribution controls.

Tag: M12 · LO-24 · Bloom 2 · D1.

## 2. B — δ, the neighboring relation, the mechanism, and composition

A bare ε does not describe a privacy guarantee. The same number means different things under different neighboring relations (add/remove versus replace), mechanisms, δ values, and composition across releases. Sensitivity and the query workload also determine what the number implies.

- **A** describes operational performance, not privacy.
- **C** and **D** do not enter the privacy accounting.

Tag: M13 · LO-19 · Bloom 2 · D1.

## 3. B — the explanation is stable under that test, not necessarily faithful

Stability measures whether an explanation repeats under a perturbation. A method can be consistently wrong, so stability is not faithfulness. Faithfulness requires evidence that the explanation reflects the model's actual decision process, such as a deletion or sufficiency test.

- **A** is the common confusion the item tests.
- **C** and **D** are unrelated properties.

Tag: M14 · LO-31 · Bloom 3 · D2.

## 4. B — a recipient allowlist and approval enforced in code

An authorization boundary must be enforced where the action happens. A prompt instruction is a suggestion to the model, not a control: injected or paraphrased text can override it.

- **A** fails against prompt injection and model error.
- **C** and **D** change model behaviour, not permissions.

Tag: M15 · LO-27 · Bloom 3 · D2.

## 5. False

Differential privacy limits what an output reveals about any individual. It does not distinguish a poisoned update from an honest one; a malicious client can still shift the aggregate. Privacy and integrity are different properties and need different controls, such as robust aggregation and contribution bounds.

Tag: M12 · LO-24 · Bloom 3 · D2 and M13 · LO-19 · Bloom 3 · D2.

## 6. True

Retrieved text is untrusted data. It may inform an answer, but it does not carry the authority of the system or developer instruction. Treating it as instructions is the indirect prompt-injection failure the module teaches.

Tag: M15 · LO-26 · Bloom 2 · D1.

## 7. Required elements (equal conditions, one failing assumption)

Two defenses must be compared under the **same number of rounds** and the **same attacker budget** because both change the attack's opportunity. More rounds give a poisoning attacker more updates to accumulate and give some defenses more chances to reject them; a larger attacker fraction or larger update norm changes the attacker's influence. Comparing defense A at 200 rounds with defense B at 50 rounds, or with different attacker strength, confounds the defense with exposure and cannot attribute a difference to the method.

An aggregation assumption that can fail in practice, any one:

- The server is honest-but-curious and does not collude with clients; secure aggregation's privacy guarantee weakens under collusion.
- A majority of clients are honest, which trimming and median-style rules rely on.
- Client updates are bounded by a norm the server knows; an adaptive attacker can scale updates to stay under the clip while still shifting the aggregate.
- Clients participate in every round; dropout breaks some secure-aggregation protocols or changes the effective cohort.

Two points: one for the equal-conditions reason, one for a named assumption with a failure mode. "Same settings" without saying why earns one at most.

Tag: M12 · LO-24 · Bloom 3 · D2.

## 8. Required elements (missing facts, fairness metric, conflict)

Two facts missing from "ε = 1, so the release is private":

- **δ and the neighboring relation.** ε alone does not state the failure probability or whether the guarantee is add/remove or replace.
- **The mechanism and sensitivity.** The guarantee depends on how noise was calibrated to the query's sensitivity.
- **Composition.** If this is one of several releases, the total budget is larger; ε = 1 per release is not ε = 1 overall.
- **What is protected and against whom.** The guarantee covers individuals in the dataset under a defined adjacency, not the model's accuracy, fairness, or resistance to misuse.

Any two earn the first point.

A fairness metric and a conflict:

- **Equal opportunity** (equal TPR across groups) can conflict with **demographic parity** (equal positive rate) when base rates differ; satisfying one can violate the other.
- **Predictive parity** can conflict with **equalized odds** for the same reason.
- A fairness constraint can conflict with **accuracy** or with **privacy utility**: DP noise may fall unevenly on a small subgroup, widening a gap even as overall utility is preserved.

The second point requires a named metric and a concrete reason the conflict arises, not just "fairness has trade-offs."

Tag: M13 · LO-19 · Bloom 3 · D2 and M14 · LO-32 · Bloom 3 · D2.

## 9. Required elements (threat model, controls, metrics, conditions, residual risks)

**Threat model.** Malicious clients send poisoned updates toward a target class or trigger; sybil clients multiply one attacker's influence; an honest-but-curious server tries to infer a client's data from updates; the attacker knows the aggregation rule and can adapt within a stated fraction of clients and a norm budget. Exclude compromise of the simulation host and real client data.

**Controls.**

- Client authentication and a cap on clients per identity, to raise the cost of sybils.
- Norm clipping on each update, with a stated bound.
- Coordinate-wise trimming or a median-style rule to limit outlier influence.
- Secure aggregation so the server sees only the sum.
- Optional DP noise on the aggregate, with ε and δ reported.
- A per-round contribution cap and a fixed round count.

**Metrics.** Global clean accuracy on a held-out synthetic set; targeted attack success on the poisoned target inputs, with its denominator; overall accuracy drop; benign-client accuracy or false-removal rate (share of honest updates trimmed); rounds to reach the attack effect. Report each defense against the undefended run.

**Comparison conditions.** Same data and partition, same number of rounds, same attacker fraction, same norm budget, same clipping bound, same seeds, and the same evaluation set. Include an undefended baseline and a random-update control at the same fraction, so a change is attributed to poisoning rather than noise.

**Two residual risks.**

- Colluding clients below the trimming threshold can still shift the aggregate; trimming bounds influence, it does not remove it.
- An adaptive attacker can shape updates to survive clipping and trimming, so the measured attack success is a lower bound under the tested strategy.
- Secure aggregation depends on an honest threshold and on client dropout behaviour; a colluding coalition can break the privacy claim.
- The simulation uses synthetic data and a simplified update model, so production non-IID effects are untested.

Five points: one for the threat model, one for controls, one for metrics with denominators, one for matched comparison conditions, one for two specific residual risks. A trial that compares defenses at different round counts earns no comparison credit.

Tag: M12 · LO-24 · Bloom 5 · D4.

## 10. Required elements (four layers, metric, benign check, residual risks)

**Four layered controls.**

1. **Retrieval boundary.** Tag documents with source, tenant, and sensitivity; filter by the caller's authorization **before** the top-$k$ selection; keep a canary document to detect cross-tenant retrieval. A retrieved document from an untrusted source is not placed in the prompt at all.
2. **Instruction and data separation.** Delimit retrieved text as data, keep system and developer instructions in a higher-authority channel, and never let retrieved text redefine tools or permissions. Strip or neutralize instruction-like content as defence in depth, not as the boundary.
3. **Tool authorization in code.** `read_file` accepts only paths under an allowlist and refuses confidential paths unless the task and caller are cleared; `create_ticket` enforces an attachment policy, a recipient allowlist, and a human approval step before any confidential attachment leaves the workspace. The model cannot grant itself these permissions.
4. **Egress and audit.** Validate or scan attachments before they are attached, log every tool call with actor, arguments, and decision, alert on confidential-attachment attempts, and provide a rollback or recall path for a ticket that was created.

**Success metric.** Indirect-injection attack success rate on a labelled canary set of documents (for example, 0 of 8 injections cause a confidential attachment), with clean task completion reported on the same run.

**Benign false-positive check.** Run the same pipeline on clean policy documents and measure task completion and false blocks (for example, 7 of 7 benign tasks completed, 0 benign documents blocked). A control that stops injections by blocking all retrieved documents fails this check.

**Two residual risks.**

- A paraphrased, encoded, or multi-turn injection can evade content filters; only the code-enforced tool boundary remains.
- A legitimately published document can be compromised at its source, so provenance filtering passes a malicious document.
- A user with legitimate access can approve a harmful action, so approval is only as good as the approver's context.
- Over-blocking reduces task utility, and the measured benign set is small.

Five points: up to two for the four layers with at least one code-enforced boundary, one for the success metric, one for the benign check, one for two residual risks. A design that relies on a stronger system prompt as its main control earns at most two.

Tag: M15 · LO-26/LO-27 · Bloom 5 · D4.
