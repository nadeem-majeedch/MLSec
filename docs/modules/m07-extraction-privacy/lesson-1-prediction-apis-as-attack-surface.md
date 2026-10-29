# Lesson 07.1 — Prediction APIs as an Attack Surface

<a id="m07-l1"></a>

**1 hour · Lesson 1 of 5 · Module 07**

## What this lesson answers

What does a model reveal when it answers a query? This lesson describes the interface, the information it returns, and the three attacks this module studies. It also gives you a threat-model template you will reuse in both labs.

## Why an answer is more than an answer

A classifier exists to turn an input into a decision. A spam filter says "spam"; a diagnostic model says "refer"; a churn model says "at risk." The decision is the product.

For an attacker, the decision is also a **labelled example**. Each query says: *for this input, the model produced this output*. Enough such pairs describe a function. If the output includes probabilities, it describes the function more precisely. If the same interface is used for millions of ordinary requests, the collection happens without anyone attacking anything.

This is the central asymmetry of inference-interface security:

$$
\text{the service must answer queries to work, and every answer is training data for the attacker.}
$$

The defender cannot simply refuse to answer. The question is how much information each answer carries, how many answers an attacker can obtain, and what the attacker can do with them.

## What an API can return

Inference interfaces differ in what they expose. From least to most informative:

| Response type | Example | What the attacker learns per query |
|---|---|---|
| **Hard label** | `3` | One class out of $k$ |
| **Top-k labels** | `[3, 8]` | A partial ranking |
| **Probability vector** | `[0.71, 0.26, 0.03, ...]` | Relative confidence over all classes |
| **Logits** | `[2.0, 1.0, -1.0]` | Confidence including scale and margins |
| **Explanations** | Feature attributions | Which features drove the decision |
| **Gradients** | In federated or differentiable settings | Local sensitivity of the output |

The last two are not usually exposed by a public API, but they exist in some deployments, SDKs, and research interfaces. Any of them can be *derived* from probabilities in some settings; probabilities are already a rich signal.

### A worked example of lost information

Softmax converts logits into probabilities:

$$
p_i = \frac{e^{z_i}}{\sum_{j=1}^{k} e^{z_j}}.
$$

For logits $z = (2.0, 1.0, -1.0)$:

```python
import numpy as np

z = np.array([2.0, 1.0, -1.0])
p = np.exp(z) / np.exp(z).sum()
print(np.round(p, 4))
print(int(p.argmax()))
```

```text
[0.7054 0.2595 0.0351]
0
```

A hard-label API returns only `0`. The attacker loses the 0.7054 confidence, the 0.2595 runner-up, and the 3:1 margin. That loss matters, but it does not make hard-label extraction impossible: the attacker still receives one labelled point per query, and a surrogate can be trained on those points. Tramèr et al. (2016) and Papernot et al. (2016) both show useful extraction from label-only responses.

### The information ladder is not a security boundary

It is tempting to conclude "we return only labels, so we are safe." That conclusion does not follow. The right question is: *how many labelled points does an attacker need to reach a given fidelity, and can they get them?* A label-only API with no rate limit and no monitoring may be easier to exploit than a probability API with strict quotas and anomaly detection.

## Three attacks, three questions

The three attacks in this module share an interface and nothing else. Keep their questions and metrics separate.

| | Extraction | Membership inference | Inversion |
|---|---|---|---|
| **Question** | Can I copy the function? | Was this record in training? | What input produces this output? |
| **Unit of analysis** | Input–output pairs | Records | A class, confidence, or attribute |
| **Attacker output** | A surrogate model | A membership bit per record | A reconstructed input or attribute |
| **Primary metric** | Fidelity; task accuracy | TPR at a fixed FPR | Reconstruction error; attribute accuracy |
| **Baseline** | Random guessing or majority class | Random guessing at the base rate | Class mean or prior |
| **Harm** | Lost revenue, IP, free riding | Privacy of data subjects | Sensitive attribute disclosure |
| **Typical defense** | Rate limits, monitoring, watermarking | Regularization, differential privacy, output control | Output restriction, DP, limiting auxiliary data |

A single API can support all three. An attacker who extracts a surrogate may then run membership inference locally, without further queries. A membership attacker may use a surrogate to generate reference behavior. Inversion may use confidence values that extraction also consumes. Defenses therefore interact: rounding outputs may reduce inversion and membership signal while leaving label-only extraction largely intact.

## The threat model template

Use the same six-part template as Module 03, specialized to an inference interface.

| Part | Questions to answer | Example: a credit-scoring API |
|---|---|---|
| **Asset** | What is valuable? | The decision function; the fact that a person was in the training set; income attributes |
| **Actor** | Who attacks and why? | A competitor, a curious account holder, an insider |
| **Knowledge** | What do they know? | Input schema, label range, approximate training period, public data |
| **Capability** | What can they do? | Submit inputs, observe responses, create accounts, may know some labels |
| **Constraint** | What limits them? | Query quota, rate limit, cost per call, terms of service, monitoring |
| **Lifecycle stage** | Where does the attack occur? | Serving and monitoring; membership signal originates in training |

Two additions are specific to this module:

1. **Candidate pool.** For membership inference, the attacker needs a set of records to test. The base rate of members in that pool drives precision.
2. **Auxiliary data.** Shadow models, reference models, or public data can make all three attacks stronger. An attack evaluated without auxiliary data is a lower bound on a better-resourced attacker, not an upper bound.

### Worked threat-model example

A team runs a hosted classifier with these properties:

- Hard labels only.
- 1,000 queries per account per day.
- Accounts are free but require an email address.
- Each query costs the provider \$0.0002 in compute.
- The model was trained on 200,000 customer records.

A first-pass assessment:

- **Extraction.** 1,000 queries/day is enough to collect 30,000 labels in a month, from one account. At \$0.0002 each, the attacker's cost to the provider is \$6, but the attacker's own cost is time and account creation. Whether 30,000 labels produce a useful surrogate depends on the input dimension and class complexity; LAB-09 shows that 500 queries already produce substantial fidelity on a 10-dimensional, 5-class problem.
- **Membership.** Hard labels remove the confidence signal that LAB-10 uses. A membership attacker would need a different signal, such as prediction stability under small input changes or the model's behavior on near-duplicates. The attack is harder, not impossible.
- **Inversion.** Hard labels alone give little gradient-like information. The attacker can still search for inputs that produce a target class, but without confidence the search has a flat objective.

The assessment ends with a measurement plan, not a verdict. "Probably low risk" is not a finding; "we measured fidelity at 500 queries and TPR at a 1% FPR" is.

## Lifecycle stages

| Stage | What creates exposure | Which attack it enables |
|---|---|---|
| **Data collection** | Records enter the training pool | Membership inference |
| **Training** | The model fits individual records; overfitting sharpens confidence | Membership inference; inversion |
| **Evaluation** | Test sets and metrics are produced | Membership inference if splits leak |
| **Packaging** | Weights, preprocessing, and metadata are stored | Extraction from a leaked artifact |
| **Serving** | Queries and responses cross a trust boundary | Extraction; inversion |
| **Monitoring** | Logs record who asked what | Detection, but also a new sensitive dataset |

The last row is easy to miss. Query logs can contain the very records a privacy attacker wants, so a monitoring system is also an asset that needs protection.

## Authorization and safety

Everything in this module is performed on models you train locally or on data that is explicitly licensed for the exercise. The labs use a local Python class and the bundled scikit-learn digits dataset.

Do not point these techniques at a third-party service. Probing a production API can violate terms of service and computer-misuse law, can degrade service for other users, and cannot be undone after the queries are logged. "It was only 500 queries" is not a defense.

If you work on a real system, the minimum prerequisites are written authorization, a defined scope, a query cap, a data-handling plan, and an agreed reporting path. Without those, the correct action is to stop.

## The reporting habit this module builds

Every result in this module needs four parts:

1. **The metric**, with its definition and denominator.
2. **The baseline**, because a number without a comparison is not evidence.
3. **The operating point**, because a threshold chosen after seeing the data is not a deployment condition.
4. **The limitation**, because a laboratory setup is not the target system.

A sentence such as "the attack succeeds 82% of the time" fails all four. A sentence such as "at a 1% false-positive budget, the maximum-confidence attack detects 7.4% of members in a 500/500 digits split; this is a lower bound for a better-resourced attacker and does not estimate any deployed model" passes.

## Common mistakes

| Mistake | Why it happens | Correction |
|---|---|---|
| Treating labels as safe | "No probabilities, no leak" | Labels are labelled training points |
| Treating probabilities as the only leak | Ignoring timing, stability, explanations | Enumerate every output channel |
| Forgetting the candidate pool | Reporting TPR alone | Report precision at a stated base rate |
| Skipping the baseline | The attack number looks impressive | Compare with random and majority class |
| Mixing attack goals | One experiment, three claims | One metric per claim |
| Probing a real API | Convenience | Use a local copy or written authorization |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| You cannot reproduce a published extraction rate | Different query type, budget, or input domain | State the access model and budget explicitly |
| Membership scores look perfect | Test rows were used in training | Rebuild the split and verify disjoint indices |
| Inversion output looks like noise | Objective and prior are underspecified | State both; compare with the class mean |
| The threat model has no constraint row | Attack assumed unlimited access | Add quota, cost, and detection assumptions |

## What you should be able to do now

- Name four response types and what each adds over a hard label.
- State the three attack questions and their metrics without mixing them.
- Fill in the six-part threat-model template for an inference API.
- Explain why "labels only" is not a privacy or IP boundary.
- State the authorization conditions for any real-system work.

## Summary

A prediction API is an information channel. The label is the minimum, probabilities add confidence, and repeated queries add volume. Extraction copies the function, membership inference tests records, and inversion reconstructs inputs; each has its own metric, baseline, and harm. The rest of the module measures each one under a stated budget and reports it with its assumptions attached.

## Next step

[Lesson 07.2 — Model extraction](lesson-2-model-extraction.md) turns the first branch into an experiment: a local API, a hard query budget, and a surrogate whose fidelity and accuracy you will measure.
