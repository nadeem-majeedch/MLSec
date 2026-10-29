# Lesson 13.4 — Private Training and Secure Computation

<a id="m13-l4"></a>

**Module 13 · Lesson 4 of 5 · 1.5 hours · LO-19**

## Scenario

Three hospitals want a shared model. They agree that raw records will not move. A vendor offers four options: "differentially private training," "secure aggregation," "secure multiparty computation," and "confidential computing." Each slide uses the word "private." None explains what the server sees, what the model reveals, or what happens if one hospital is malicious.

This lesson separates the four. They address different trust assumptions and compose in specific ways. Choosing one is not a substitute for the others.

## Objectives

By the end of this lesson you will be able to:

1. Explain DP-SGD step by step and identify its privacy and utility knobs.
2. Compare local, central, and distributed DP by trust assumption and utility.
3. Explain secure aggregation, MPC, homomorphic encryption, and TEEs conceptually, with their limits.
4. Choose a combination of techniques for a stated threat model.
5. State what private training and secure computation do not protect against.
6. Place LAB-17's centroid release in the landscape.

## 1. Where the noise enters

| Approach | Who adds noise | Who trusts whom | Typical utility | Typical unit |
|---|---|---|---|---|
| Local DP | Each client, before sending | No trust in the server | Lowest | One client or record |
| Central DP | A trusted server, after aggregation | Trust in the server | Highest | One record or client |
| Distributed DP | Parties, often with secure aggregation | Trust in the protocol and a threshold | Middle | One record or client |
| DP-SGD | Training process, per example | Trust in the training operator | Depends on \(\varepsilon\) | One example |
| DP-FL | Coordinator or clients, per client update | Depends on deployment | Depends on \(\varepsilon\) | One client |

"Private training" is not one algorithm. It is a family of choices about where randomness is added and what is being protected.

## 2. DP-SGD

Differentially private stochastic gradient descent modifies the ordinary training loop in four places.

1. **Per-example gradients.** Compute a gradient for each example in the batch, not just the batch average.
2. **Clip.** Replace \(g_i\) with \(g_i \cdot \min(1, C/\|g_i\|_2)\). The clip bounds each example's influence.
3. **Noise.** Sum the clipped gradients and add Gaussian noise with standard deviation \(\sigma C\) per coordinate.
4. **Update.** Apply the noisy sum (scaled by the learning rate and batch size) to the parameters.

The privacy guarantee comes from the fact that changing one example changes the clipped sum by at most \(C\), and the Gaussian noise is scaled to \(C\). The accounting tracks how the guarantee degrades over steps. Modern implementations use Rényi DP or zero-concentrated DP for tighter bounds than basic composition.

### The knobs

| Knob | Effect on privacy | Effect on utility |
|---|---|---|
| Clip norm \(C\) | Bounds sensitivity | Too small biases gradients; too large weakens the noise relative to signal |
| Noise multiplier \(\sigma\) | Larger is more private | Larger reduces learning |
| Batch size | Larger batch can improve amplification and signal | More compute per step |
| Learning rate | Not a privacy parameter | Must be tuned for the noisy gradient |
| Steps | More steps spend more budget | More training can improve utility until noise dominates |
| Sampling rate | Subsampling amplifies privacy | Smaller batches can hurt utility |

The interaction is not intuitive. A smaller \(C\) reduces the noise scale but clips more gradients, which can bias training. A larger batch improves the signal-to-noise ratio and can improve privacy amplification, but it costs compute. DP-SGD is a tuning problem with a privacy budget, not a single switch.

### A worked step

Suppose \(C = 1.0\) and \(\sigma = 1.1\). For a batch of clipped gradients, the sum has sensitivity \(C = 1.0\) in L2. The added noise per coordinate has standard deviation \(1.1\). If the true clipped sum is 10.0 in one coordinate, the signal-to-noise ratio is about 9:1; if it is 0.5, the noise dominates. Training works because many steps aggregate signal, and because the learning rate is tuned for the noise level.

The numbers are illustrative. The actual privacy cost depends on the sampling scheme, the number of steps, and the accounting method.

## 3. Local, central, and distributed DP

**Local DP** has each client randomize before sending. The server never sees a clean value, so it does not need to be trusted. The cost is high: noise must be large enough to hide each client's contribution, and aggregating many noisy reports only partially recovers the signal. Local DP is attractive when the server is untrusted or when the data is collected from many independent users.

**Central DP** has a trusted server aggregate clean values and add noise once. Utility is much better because the noise is calibrated to the aggregate sensitivity, not to each contribution. The trust assumption is significant: the server sees the clean inputs, so a curious or compromised server breaks the privacy claim.

**Distributed DP** tries to get central-DP utility without a fully trusted server. Clients secret-share their inputs or updates, a subset of parties computes the aggregate, and noise is added in a way that no single party sees an individual contribution. Secure aggregation is the common building block. The trust assumption moves to the protocol, the threshold, and the dropout handling.

| Threat | Local DP | Central DP | Distributed DP |
|---|---|---|---|
| Curious server sees individual values | Protected | Not protected | Protected below the collusion threshold |
| Server adds noise honestly | Not required | Required | Protocol-enforced |
| Utility for a given epsilon | Lowest | Highest | Middle |
| Dropout handling | Simple | Simple | Complex |
| Implementation complexity | Low | Low | High |

## 4. Secure aggregation

Secure aggregation computes the sum of client updates without revealing any individual update. It is a specific secure-computation protocol, optimized for summation.

| Property | What it gives | What it assumes |
|---|---|---|
| Masking | Pairwise masks cancel in the sum | Clients follow the protocol |
| Dropout resilience | Remaining clients can reconstruct masks | Threshold of clients remains |
| Confidentiality | Server sees only the sum | No collusion above the threshold |
| Integrity | Not provided | A malicious client can still poison the sum |
| Correctness | Not provided if inputs are malformed | Validation is separate |

Secure aggregation is a confidentiality control. It is not a poisoning defense, and it is not a substitute for DP. The aggregate can still leak, and a poisoned contribution still enters the sum.

## 5. Secure multiparty computation

MPC lets several parties compute a function of their private inputs without revealing the inputs to each other. Secret sharing is the common technique: each input is split into shares, computation proceeds on shares, and only the output is reconstructed.

| Dimension | Consideration |
|---|---|
| Threat model | Semi-honest (follows protocol) versus malicious (may deviate) |
| Collusion | What fraction of parties may collude? |
| Honest majority | Some protocols require a majority of honest parties |
| Cost | Communication rounds and bandwidth, often the bottleneck |
| Function | Aggregation is much cheaper than deep training |
| Output | The output itself must still be protected, often with DP |

MPC is a good fit for private aggregation, private set intersection, and small joint computations. It is a poor fit for training a large model across parties without additional techniques, because the communication and cryptographic overhead are substantial.

## 6. Homomorphic encryption

Homomorphic encryption allows computation on ciphertexts. The result, when decrypted, is the result of the computation on the plaintexts.

| Property | Implication |
|---|---|
| Operations | Limited set; additions and multiplications, with depth constraints |
| Noise growth | Ciphertext noise grows with operations; bootstrapping refreshes it at a cost |
| Performance | Orders of magnitude slower than plaintext computation |
| Threat model | The compute party sees only ciphertexts |
| Typical use | Private inference, simple aggregates, not full training |

HE is attractive when one party holds a model and another holds private inputs, and neither wants to reveal its side. It is not a general-purpose privacy layer for training, and it does not by itself prevent leakage from the output.

## 7. Trusted execution environments

A TEE is a hardware-isolated region that runs code and protects data from the host operating system. Remote attestation lets a client verify which code is running before sending data.

| Strength | Limitation |
|---|---|
| Protects data in use from the host | Trusts the hardware vendor and the attestation chain |
| Attestation can bind code identity | Side-channel attacks can leak information |
| Useful for aggregation and inference | Patching and supply-chain complexity |
| Lower performance overhead than MPC/HE in some workloads | The enclave boundary is a new attack surface |

A TEE changes whom you trust; it does not eliminate trust. The threat model should name the hardware vendor, the attestation service, and the side-channel assumptions.

## 8. Federated learning with DP

In federated learning, the natural privacy unit may be a client, not a record.

| Unit | Mechanism | Guarantee | Cost |
|---|---|---|---|
| Example-level | DP-SGD locally | One example changes little | High noise for small local datasets |
| Client-level | Clip the client update, add noise to the sum | One client's entire contribution changes little | Large clipping error when clients differ |
| Local | Client randomizes its update | No trust in the coordinator | Very high noise |
| Central | Coordinator adds noise after aggregation | Trust in the coordinator | Best utility |

Client-level DP requires clipping the *client update* to a norm \(C\), then adding noise scaled to \(C\). If one client's data is large and another's is small, a single clip norm either distorts the large client or under-protects the small one. Per-client adaptive clipping is an active design area.

Composition across rounds is the same problem as repeated releases. A 100-round training run does not spend the per-round epsilon once; the total grows with the accounting method.

## 9. Choosing a combination

| Goal | Technique | Residual risk |
|---|---|---|
| Hide individual records from the server | Secure aggregation or MPC | Collusion, dropout, malformed inputs |
| Bound what the released model reveals | DP-SGD or DP-FL | Utility loss, implementation bugs |
| Hide inputs from an untrusted compute party | HE or TEE | Performance, side channels, trust in hardware |
| Protect against a malicious client poisoning | Robust aggregation, validation | Adaptive attackers, Sybils |
| Protect against a curious client inferring others | DP and access control | Aggregate leakage, side knowledge |
| Prove the computation ran as claimed | Attestation, signed code | Supply chain, key management |

A realistic design combines several rows. For example: secure aggregation for confidentiality, client-level DP for a release guarantee, robust aggregation for integrity, and monitoring for response.

## 10. What these do not solve

- **Poisoning and backdoors.** A client can contribute a malicious update within any privacy budget.
- **Leakage from the final model.** A DP training run bounds it; a secure computation does not.
- **Metadata.** Who participated, when, and how often can be sensitive.
- **Implementation bugs.** A correct proof with incorrect clipping or noise is not private.
- **Side channels.** Timing, memory, and power can leak through a TEE or a protocol.
- **Governance.** A technical guarantee does not answer whether the use is lawful or fair.

## 11. Where LAB-17 fits

LAB-17 is **central DP on a statistic**, not DP-SGD and not secure computation. A trusted script computes clipped centroids and adds Laplace noise. There is no server/client split, no secure aggregation, and no training.

That makes it a clean teaching example for sensitivity, mechanism, composition, and utility. It does not demonstrate private training. LAB-16 is federated but not private; its report says so. The two labs are complementary: one shows distributed integrity, the other shows a formal privacy release.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Calling secure aggregation "DP" | Both are privacy techniques | State that one hides inputs and the other bounds output leakage |
| Tuning DP-SGD by accuracy alone | Accuracy is the visible metric | Report epsilon and the accounting method |
| Clipping after adding noise | The code order is easy to miss | Clip per example, then noise |
| Using local DP for a high-dimensional model | It is conceptually simple | Expect very high noise; consider distributed DP |
| Assuming MPC protects the output | The computation is private, not the result | Add DP to the output |
| Trusting a TEE without attestation | The enclave is "secure" | Verify code identity and patch status |
| Reporting a per-step epsilon | The step count is large | Report the total after accounting |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| DP-SGD does not learn | Noise too high or clip too small | Inspect signal-to-noise ratio and clip rate |
| Accuracy is fine but epsilon is huge | Too many steps or weak accounting | Reduce steps or increase noise |
| Secure aggregation fails with dropouts | Mask reconstruction threshold not met | Test with realistic dropout rates |
| MPC is too slow | Communication-bound function | Use a smaller function or a different trust model |
| HE inference is inaccurate | Approximate operations and noise growth | Use a supported depth and precision |
| TEE attestation fails | Code or configuration changed | Rebuild and re-attest |

## Check your understanding

1. What are the four modifications DP-SGD makes to ordinary SGD?
2. Which DP variant has the best utility for a given epsilon, and what does it trust?
3. What does secure aggregation hide, and what does it not prevent?
4. Why is MPC a better fit for aggregation than for full training?
5. What does a TEE change about the trust model, and what does it not eliminate?
6. Why is client-level DP harder than example-level DP when clients have different data sizes?
7. Where does LAB-17 sit in this landscape?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Private training is a family of choices about where noise enters and what unit is protected.
- DP-SGD clips per-example gradients, adds Gaussian noise, and accounts for the budget over steps.
- Local DP avoids trusting the server at a high utility cost; central DP has better utility and trusts the server; distributed DP tries to get both with secure computation.
- Secure aggregation, MPC, HE, and TEEs address confidentiality and computation trust, not poisoning or output leakage.
- Federated DP can protect examples or clients; client-level DP is harder with heterogeneous clients.
- LAB-17 is central DP on a centroid release, not private training.

## Next

Continue to [Lesson 13.5 — Privacy-utility evaluation and limitations](lesson-5-privacy-utility-evaluation.md), where the release is measured and documented.
