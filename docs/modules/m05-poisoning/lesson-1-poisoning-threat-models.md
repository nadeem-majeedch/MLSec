# Lesson 05.1 — Poisoning Threat Models and the Data Supply Chain

<a id="m05-l1"></a>

**1 hour · Lesson 1 of 4 · Module 05**

## What this lesson answers

Who can change the training data, how much can they change, and what are they trying to achieve? Poisoning is not one attack. It is a family defined by data access, budget, timing, and goal. This lesson builds the threat model before any code runs.

## Training time versus inference time

Evasion (Module 04) changes an input at prediction time. Poisoning changes the examples the model learns from. The distinction has three consequences:

1. **Persistence.** A poisoned model keeps its behavior after the attacker leaves; a perturbed input affects one request.
2. **Detection point.** Evasion can be caught per request; poisoning must be caught in data or in the learned behavior.
3. **Evaluation.** A poisoned test set measures the wrong thing. The test set is the referee, and it must stay clean.

A poisoning claim therefore needs five parts:

| Part | Question | LAB-05 answer | LAB-06 answer |
|---|---|---|---|
| **Goal** | What should change? | Overall accuracy should fall | One chosen prediction should flip |
| **Access** | What can the attacker touch? | Labels of existing rows | Append rows with features and labels |
| **Budget** | How much? | 0–30% of training rows | 30 rows against 350 (about 8%) |
| **Knowledge** | What does the attacker know? | Data distribution, not the test set | Feature space and target, not test or reference set |
| **Metric** | How is success measured? | Test accuracy and macro F1 | Target prediction and probability, plus test accuracy |

Without all five, a poisoning result is a story rather than an experiment.

## The attack surface is the data supply chain

Training data is assembled, not found. Every stage is a potential entry point:

| Stage | Poisoning opportunity | Typical access |
|---|---|---|
| **Collection** | Submit crafted samples through a public form, sensor, or scrape | External, low privilege |
| **Labeling** | Mislabel rows, or exploit a contractor's weak review | Insider or vendor |
| **Aggregation** | Contribute a dataset that is merged without provenance checks | Partner or public source |
| **Preprocessing** | Change a join, deduplication rule, or filter | Code or pipeline access |
| **Feedback loop** | Trigger a bad prediction whose outcome becomes a future label | Deployed user or attacker |
| **Model update** | Supply a fine-tuning set or an updated checkpoint | Vendor or supply chain |

The feedback loop deserves special attention in ML. A model's own decisions can become the labels for the next model. If an attacker can influence which cases get which outcome — a fraud alert that leads to an account closure, a triage flag that leads to a test — the attacker may be writing training data without ever touching the training set.

### Access is a spectrum, not a binary

| Access level | What the attacker controls | Example |
|---|---|---|
| **Label only** | The label of existing rows | A reviewer marks cases incorrectly |
| **Feature and label** | New rows with chosen features and labels | An attacker submits synthetic accounts |
| **Row insertion** | Adds rows to a feed without labels | A data vendor contributes a batch |
| **Pipeline** | Preprocessing or sampling code | An insider changes deduplication |
| **Model update** | Weights or fine-tuning data | A compromised vendor artifact |

Each level implies a different defense. Label-only attacks invite label screening. Feature-space attacks invite distribution checks. Pipeline access invites code review and provenance, not statistics.

## Goals: availability, targeted integrity, and conditional behavior

Poisoning goals are usually sorted into three families:

- **Availability.** Make the model worse for everyone. LAB-05 is an availability attack: every class is affected, and success is a drop in test accuracy.
- **Targeted integrity.** Make the model wrong on a chosen input or class while leaving everything else intact. LAB-06 is targeted: one point at (0.1, 0.0) must move from class 1 to class 0.
- **Conditional behavior.** Make the model wrong only when a trigger is present. That is a backdoor, and it is Module 06.

The families need different metrics. Accuracy measures availability. A target-point probability measures targeted integrity. Attack success on triggered inputs, with clean accuracy alongside it, measures a backdoor.

## Labels versus features

Two attacks can share a budget and differ completely in visibility:

| Attack | What changes | Can a label check see it? | Can a distribution check see it? |
|---|---|---|---|
| Label flip | Label of a real row | Yes, if the model disagrees | No, features are unchanged |
| Feature-space injection | New rows near a target | Only if the labels look wrong | Sometimes, if the cluster is anomalous |
| Clean-label injection | New rows with correct labels and realistic features | No | Maybe, if the features are unusual |

A **clean-label** attack is the hardest case for label screening, because every label is valid. The attacker's leverage is in *where* the rows sit, not in what they are called. LAB-06 is not clean-label: its 30 added rows are labelled class 0 and sit in class-1 territory, so a reference-set screen can catch them. That limitation is part of what the lab teaches.

## The budget and the denominator

Let $n$ be the number of clean training rows and $p$ the number of poisoned rows. The poison rate is

$$
r = \frac{p}{n}.
$$

State which $n$ you mean. LAB-05 uses the 1,257 training rows, so

$$
r = 0.05 \;\Rightarrow\; p = \mathrm{round}(0.05 \times 1257) = 63.
$$

The same 63 rows are 5.0% of training, 3.5% of all 1,797 images, and 11.7% of the 540-row test set. Only the first number is the attack budget. Mixing denominators is the most common way to make a poisoning result unreproducible.

The budget also has a *rate over time*: a one-time 2% injection is different from 0.1% per week for a year, even if the totals match. Persistence and retraining frequency belong in the threat model.

## Knowledge and capability

Ask what the attacker knows before asking what they can do:

- **Data distribution.** Can they generate rows that look realistic? Without this, a screen based on plausibility catches them.
- **Model and training procedure.** Can they optimize the poison for the learner, or only guess? Optimization-based attacks need a surrogate or white-box access.
- **Defense.** Do they know the screen, its threshold, and the reference set? An adaptive attacker targets the defense, not just the model.
- **Test set.** Usually not, and this matters: an attacker who sees the test set can tune to it, which overstates real-world success.

Capability is constrained by the pipeline: a reviewer can change labels one at a time; a vendor can replace a batch; an API user can add rows but cannot delete them. The constraint decides whether the attack is feasible at all.

## Where poisoning sits in the lifecycle

| Lifecycle stage | Poisoning question | Control family |
|---|---|---|
| Problem definition | Is the label a proxy the attacker can influence? | Metric and label design |
| Data collection | Who can submit rows? | Authentication, quotas, provenance |
| Labeling | Who reviews, and how? | Dual review, gold questions, audit |
| Preparation | Are joins and deduplication trustworthy? | Code review, lineage, hashing |
| Training | Can a bad row change the fit? | Robust training, influence analysis |
| Evaluation | Is the test set isolated? | Access control, frozen splits |
| Deployment | Can outputs feed back into labels? | Feedback monitoring, delayed labels |
| Monitoring | Would a targeted shift be visible? | Slice metrics, target probes |

Poisoning is often described as a training-stage attack. The controls that matter most are usually earlier — at collection and labeling — because a row that never enters the pipeline cannot poison it.

## Mapping to frameworks

NIST AI 100-2e2025 classifies poisoning as an integrity attack on the learning process, with availability effects as a possible outcome. In MITRE ATLAS, the closest technique is **AML.T0020 Poison Training Data**; data from a compromised source may also involve collection or supply-chain techniques. Use framework IDs only when the mapping is real; an empty cell is better than a wrong one.

## Worked comparison: two labs, two threat models

| Question | LAB-05 | LAB-06 |
|---|---|---|
| Who is the attacker? | Someone who can relabel rows | Someone who can append rows |
| What is the goal? | Degrade everyone | Flip one decision |
| What is the budget? | Up to 30% of 1,257 rows | 30 rows against 350 |
| What does success look like? | Accuracy falls | Target probability crosses 0.5 |
| What would a defender notice? | A broad accuracy drop at high rates | Almost nothing in global accuracy |
| What defense is tested? | None; the lab measures the attack | Reference-set screening |

The comparison is the point. A defense designed for LAB-05 (monitor accuracy) does nothing for LAB-06.

## Common mistakes and troubleshooting

| Mistake | Why it is wrong | Fix |
|---|---|---|
| "Poisoning means changing the test set" | That measures evaluation noise | Poison training rows only |
| Reporting a rate without a denominator | 30 rows is 8% of 350 and 0.3% of 10,000 | State $p$ and $n$ |
| Treating label access and feature access as the same | They imply different defenses | Separate the access levels |
| Assuming the attacker knows the model | Many attacks need a surrogate | State knowledge explicitly |
| Calling any added row "clean-label" | Clean-label requires correct labels | Check both labels and features |
| Skipping the feedback loop | Deployed decisions can become labels | Include it in the surface list |

## Summary and key takeaways

- Poisoning is a training-time integrity attack; its effects persist in the model.
- A poisoning claim needs goal, access, budget, knowledge, and metric.
- The data supply chain — collection, labeling, aggregation, preprocessing, feedback, updates — is the real attack surface.
- Labels, features, and pipeline access are different capabilities with different defenses.
- The poison rate denominator must be the clean training-set size and must be stated.
- Availability, targeted integrity, and conditional behavior need different success metrics.
- Clean-label attacks defeat label checks; their leverage is placement, not mislabelling.
- Accuracy monitoring is not a defense against a targeted attack.

## Check yourself

1. Why must a poison rate name its denominator?
2. Give one attack that label screening can catch and one it cannot, and explain the difference.
3. Why is the feedback loop part of the poisoning surface even when the attacker never touches the training set?
4. What does an attacker need to know to run an optimization-based poisoning attack?
5. Why is a poisoned test set an invalid evaluation?

## Next step

[Lesson 05.2 — Label flipping and the poisoning curve](lesson-2-label-flipping.md) turns the label-only threat model into a measured dose-response experiment.
