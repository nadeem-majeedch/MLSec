# Lesson 12.2 — Malicious Clients and Update Poisoning

<a id="m12-l2"></a>

**Module 12 · Lesson 2 of 5 · 2 hours · LO-24**

## Scenario

A bank joins a fraud-model consortium. Each member trains locally and sends an update. One member has been compromised. It does not need to read anyone else's data, change the coordinator, or break the channel. It only needs to submit an update that the mean will believe.

The compromised member has two levers. It can change what its local training sees, and it can change what it sends. The first lever is data poisoning, which Module 05 covered in a centralized setting. The second is update manipulation, which is specific to federated learning. This lesson combines them, then measures the result in LAB-16.

## Objectives

By the end of this lesson you will be able to:

1. Distinguish data poisoning, update poisoning, and model replacement by what the attacker modifies.
2. Compute an attacker's effective share under sample weighting and update scaling.
3. Construct a trigger-target backdoor and explain why it can preserve clean accuracy.
4. Explain how Sybil identities and stale or copied updates change the attack.
5. Identify the signals that a malicious update leaves, and why each is incomplete.
6. Interpret LAB-16's malicious-mean result without overgeneralizing it.

## 1. Four levels of attacker capability

| Level | Attacker controls | Example | What the server sees |
|---|---|---|---|
| A1 | Local training data | Label flipping, poisoned examples | A plausible update |
| A2 | Data and update computation | Scaling, sign flips, crafted delta | A plausible or extreme update |
| A3 | Data, update, and client code | Custom optimizer, model replacement | Whatever the code chooses to send |
| A4 | Many identities | Sybil clients | Multiple plausible updates |

LAB-16 uses A3 with one identity. That is enough to show the mechanism and simple enough to explain. Real deployments must consider A4, because robust aggregation assumptions are usually stated in terms of the fraction of adversarial clients, and Sybil identities change that fraction.

A useful rule: **the server cannot verify a claim it cannot independently compute.** It can check an update's norm, its similarity to other updates, and its effect on a reference set. It cannot check that the update came from the declared data or that the client ran the agreed code.

## 2. Data poisoning versus update poisoning

| Dimension | Data poisoning | Update poisoning |
|---|---|---|
| Modified object | Local examples or labels | The submitted update vector |
| Requires code control | No | Yes, or a compromised client |
| Detectable by data audit | Sometimes | No, the data may be clean |
| Detectable by update inspection | Indirectly | Sometimes |
| LAB-16 example | Triggered copies relabeled 0 | Update multiplied by 6 |
| Typical goal | Bias the learned function | Amplify or redirect the learned function |

Data poisoning is necessary for a backdoor: the model must learn the trigger-target association. Update poisoning is what makes the backdoor survive aggregation when the attacker is one client among many. The two are complementary, not alternatives.

A third variant, **model replacement**, sends an update that is not a small step from the global model but an entire model that already contains the target behavior. Bagdasaryan et al. show that scaling such an update can make the global model approximately equal to the attacker's model for a round. The defense implication is that "the update is close to the previous global model" is itself an assumption worth checking.

## 3. Effective influence

With equal sample counts \(n\), a benign client's share is \(1/K\). If one attacker scales its update by \(s\), its share of the summed update is

\[
\frac{s}{K-1+s}.
\]

For \(K=8\) and \(s=6\),

\[
\frac{6}{7+6} = 0.4615.
\]

One client out of eight controls 46% of the aggregate direction. That is the arithmetic LAB-16 exploits.

LAB-16 adds a second effect: the attacker appends triggered copies of its local data and relabels them, so its declared sample count doubles. With roughly 157 rows per client, the malicious client reports 314 rows. The sample-weighted total becomes

\[
7 \times 157 + 314 = 1{,}413,
\]

so the attacker's sample weight is \(314/1{,}413 = 0.2223\), about twice a benign client's \(157/1{,}413 = 0.1111\). Combined with the 6× scale, its effective directional contribution is roughly twelve times a benign client's. The lesson is that an attacker can inflate influence through **both** the declared sample count and the update magnitude. Defenses must bound both.

### Worked example: dilution

Five clients, one attacker, equal data, attacker scale 4:

\[
\text{attacker share} = \frac{4}{4+4} = 0.50.
\]

If the defender clips every update to norm 2, the attacker's effective scale becomes \(2/\|\Delta\|\) rather than 4. If the benign updates also exceed 2, they are clipped too, which changes the clean model. This is the central trade-off of clipping: it bounds influence only by bounding everyone, and the bound is a hyperparameter with no universally correct value.

## 4. Constructing a backdoor

A backdoor has three parts:

| Part | LAB-16 choice | Design question |
|---|---|---|
| Trigger | Set the top-left 2×2 pixels to 1.0 | How visible and how specific? |
| Target | Class 0 | Which behavior benefits the attacker? |
| Poison | Triggered copies of local rows relabeled 0 | How many, and mixed with clean data? |

The malicious client trains on its clean rows plus the poisoned copies. The resulting local model performs the main task reasonably well and predicts the target whenever the trigger appears. It then scales the update before sending.

Why does clean accuracy not collapse immediately? The poisoned examples are a small fraction of the client's data, and the trigger is localized. The model can fit both the clean and triggered patterns. That is what makes a backdoor stealthy: the malicious update is not an outlier in clean accuracy, only in the trigger subspace.

LAB-16 measures the effect on 1,080 test rows, excluding true class-0 rows from the attack set. The attack succeeds when a triggered non-target row is predicted as 0.

## 5. What LAB-16 measures

All rows use the same eight clients, 12 rounds, eight local epochs, and learning rate.

| Run | Clean accuracy | Attack success rate |
|---|---:|---:|
| Benign, mean | 0.9000 | 0.0021 |
| Malicious, mean | 0.7056 | 1.0000 |
| Malicious, trimmed mean | 0.8704 | 0.0000 |
| Malicious, norm clipping | 0.8944 | 0.6276 |

Three observations:

1. **The attack works.** One client out of eight takes ASR from 0.0021 to 1.0000. Clean accuracy falls by 0.1944, so this attack is not stealthy in the clean metric, but the backdoor is complete.
2. **The trimmed mean removes this attack.** With eight clients and one outlier, trimming one value from each coordinate's upper and lower tail removes the malicious coordinate values. ASR is 0.0000 and clean accuracy is 0.8704. That is a result for this attacker, this fraction, and this rule, not a proof of robustness.
3. **Clipping alone does not.** ASR is still 0.6276. Clipping reduces the update's magnitude, but the backdoor direction survives, and the aggregate still moves toward it. Clean accuracy is 0.8944, close to benign, which makes the residual backdoor easy to miss if only accuracy is reported.

The last row is the most important teaching result. A defender who saw 0.8944 clean accuracy might conclude that clipping worked. The ASR says otherwise.

## 6. Stealth and adaptation

| Technique | What it changes | Why it matters |
|---|---|---|
| Small scale | Less influence per round | May survive longer without tripping a norm threshold |
| Distributed poison | Poison spread over rounds | Each update looks less anomalous |
| Clean-label poison | Labels remain plausible | Data audits miss it |
| Trigger in a rare feature | Few clean examples exercise it | Clean evaluation does not reveal it |
| Adapt to the rule | Craft update inside the acceptance region | Defeats a fixed robust rule |
| Sybil identities | More adversarial contributions | Breaks the assumed adversary fraction |
| Stale or copied update | Looks like a benign client | Hard to distinguish from free-riding |

Fang et al. show that an attacker who knows the robust aggregation rule can optimize a local model to be both malicious and close to the benign cluster. The defense is not a fixed rule; it is a moving target with monitoring, diversity, and a response.

## 7. Signals and their limits

| Signal | Catches | Misses |
|---|---|---|
| Update norm | Extreme scaling | Scaled update inside the clip threshold |
| Cosine similarity to peers | Isolated direction | Attacker that mimics the benign cluster |
| Loss on a reference set | Degraded main-task behavior | Backdoor that preserves clean loss |
| Trigger scanning | Known triggers | Unknown or rare triggers |
| Client reputation | Repeated bad behavior | First-time attacker, Sybil identity |
| Per-class accuracy | Targeted degradation | Backdoor on a class not in the audit set |
| Participation diversity | Concentration | Collusion across identities |

No single signal is sufficient. A monitoring design combines a cheap bound (norm), a relational check (similarity), a task check (reference loss), and an outcome check (trigger-aware evaluation). Each has a cost and a false-positive mode.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Treating data poisoning and update poisoning as the same | Both are "poisoning" | Separate what is modified and what control it requires |
| Forgetting the declared sample count | The code weights by `len(X_local)` | Audit the declared count as part of validation |
| Assuming one client is one vote | FedAvg weights by samples | Compute the actual share |
| Calling an attack stealthy because clean accuracy is high | Accuracy is an average | Report attack success on the trigger |
| Concluding clipping is ineffective in general | One result is one configuration | State the attacker, scale, and clip threshold |
| Concluding trimmed mean is robust in general | One outlier was removed | Vary attacker fraction and adaptation |
| Ignoring Sybil identities | The lab uses one client | State the identity assumption |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Malicious run has no effect | Malicious flag not passed or client index wrong | Print the malicious client id and update norm |
| ASR is high for the benign run | Trigger applied to target-class rows | Exclude true target rows from the attack set |
| Clean accuracy is unchanged and ASR is 0 | Poison copies not relabeled | Check the poison labels |
| Trimmed mean throws an index error | Trim count too large for the client count | Require `2*trim < K` |
| Clipped mean gives the same result as mean | Clip threshold above every update norm | Print the update norms |
| Results differ from the reference | Seed, data split, or rounds changed | Compare `run.json` with the reference |

## Check your understanding

1. With eight equal clients and one attacker scaling by 6, what share of the summed update does the attacker control?
2. LAB-16's attacker also doubles its declared sample count. Why does that matter for a sample-weighted mean?
3. Why can a backdoored update preserve clean accuracy?
4. Explain why norm clipping leaves ASR at 0.6276 while reducing the clean-accuracy cost.
5. Name two signals that would catch LAB-16's attack and one that would not.
6. What assumption does a Sybil attacker violate, and which defense relies on it?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- A malicious client can poison data, manipulate its update, or do both. Update manipulation needs code control.
- Influence is weight times magnitude. Scaling and inflated sample counts both increase it.
- A backdoor combines a trigger, a target, and poisoned examples. It can preserve clean accuracy while changing triggered behavior.
- LAB-16: one scaled client takes ASR from 0.0021 to 1.0000 and costs 0.1944 clean accuracy.
- Trimmed mean removes this single outlier; clipping limits magnitude but leaves 0.6276 ASR.
- Sybil identities and adaptive attackers break the assumptions behind robust aggregation.
- Evaluate with clean accuracy and attack success, and report the attacker model.

## Next

Continue to [Lesson 12.3 — Aggregation and its limits](lesson-3-aggregation-and-its-limits.md), where the rules themselves are compared and their assumptions are made explicit.
