# Lesson 14.2 — Explanation Leakage and Manipulation

<a id="m14-l2"></a>

**Module 14 · Lesson 2 of 4 · 1.5 hours · LO-31**

## Scenario

A bank exposes a "why this decision?" endpoint so customers can see which features drove a denial. The endpoint returns the top five feature contributions to the log-odds. Within a week, a competitor is advertising a model with suspiciously similar behavior. An analyst finds that the endpoint can be queried with arbitrary feature values, that each response reveals a linear equation, and that a few hundred queries recover the bank's coefficients almost exactly.

The same endpoint has a second problem. A customer advocate notices that a tiny change in an application — one that does not change the decision — moves the "top reason" from debt ratio to zip code. The explanation is not wrong about the crafted input. It is being steered.

This lesson treats explanations as an output channel with the same security questions as any other: what does it reveal, who can query it, and what happens when they optimize against it?

## Objectives

By the end of this lesson you will be able to:

1. Map the information an explanation endpoint can reveal beyond the prediction.
2. Explain how explanation queries support model extraction and membership inference.
3. Describe how an attacker manipulates a post-hoc explanation while preserving the prediction.
4. Relate explanation stability measurements to manipulation risk without overstating the link.
5. Select controls proportionate to the explanation's exposure and audience.
6. Write a threat model for an explanation feature.

## 1. The explanation surface

A prediction endpoint returns a label or a score. An explanation endpoint returns a structured object: attributions, a surrogate, counterfactuals, or examples. Each field is additional information about the model or its training data.

| Output | What it can reveal | Example |
|---|---|---|
| Feature attributions | Local gradient or coefficient structure | Recover weights from many queries |
| Global feature importance | Which features matter, and their relative scale | Narrow a extraction attack |
| Counterfactuals | Decision boundary near the input | Probe the boundary efficiently |
| Nearest training examples | Actual or reconstructed training rows | Direct data exposure |
| Confidence plus attribution | A richer signal for membership inference | Separate members from non-members |
| Explanation metadata | Model family, version, background data | Supply-chain and version disclosure |
| Error messages | Internal feature names, preprocessing | Reconnaissance |

The security question is not whether explanations are "sensitive" in the abstract. It is whether the endpoint returns more than the audience needs, to a caller who can query it repeatedly.

## 2. Leakage through extraction

### The linear case, worked

Suppose the endpoint returns, for any input \(x\), the per-feature contribution to the log-odds:

\[
c_j(x) = w_j x_j.
\]

The caller sends \(d+1\) queries:

- \(x = 0\): the response is all zeros; this reveals nothing about \(b\) unless the endpoint also returns the score.
- \(x = e_j\), the unit vector for feature \(j\): the response is \(c_j = w_j\).

After \(d\) queries the caller has every weight. If the endpoint also returns the score \(z = w^\top x + b\), one query at \(x=0\) gives \(b\). The model is fully extracted.

Even if the endpoint returns only the top-\(k\) attributions, the attacker can choose inputs that isolate features, repeat with different scales, and solve a system. Rounding and top-\(k\) filtering raise the query cost; they do not remove the channel.

### The non-linear case

For a neural model, an attribution query returns a local derivative-like quantity. Many queries at nearby points approximate the gradient field, which supports extraction and evasion. The attacker does not need the architecture; they need enough input-output pairs to fit a surrogate. Explanations make each pair more informative.

### Why this is model extraction, not just "sharing"

Module 07 defined extraction as building a model that approximates the target's behavior. An explanation endpoint is a high-bandwidth extraction oracle. Rate limits reduce bandwidth, but a patient attacker with many accounts, or an insider, can still accumulate queries. The control that matters is the **information per response**, not only the request count.

| Control | Effect | Limitation |
|---|---|---|
| Authentication and authorization | Restricts who can query | A legitimate account can still extract |
| Per-account rate limit | Raises the time cost | Distributed accounts bypass it |
| Query budget | Caps total information | Does not stop a low-and-slow attacker |
| Coarsen attributions | Reduces precision per response | Still leaks ranking and sign |
| Top-\(k\) only | Hides small contributions | Isolating queries recover them |
| Aggregate explanations | Reduces per-input detail | Less useful for the stated purpose |
| Monitoring query patterns | Detects systematic probing | Requires a baseline and a response plan |
| Separate tenant and model | Contains cross-customer leakage | Does not protect the model itself |

## 3. Leakage through training data

Explanations are computed from a model that was fit on data. Anything that depends on the training set can carry a signal about it.

| Mechanism | What an attacker may learn | Why explanations can amplify it |
|---|---|---|
| Membership inference | Whether a record was in training | Attributions can be more sensitive near memorized rows |
| Model inversion | Representative features of a class | Counterfactuals and prototypes can resemble training inputs |
| Property inference | Population-level properties | Global importance reveals which features the training data emphasized |
| Reconstruction via examples | Actual rows | Some explanation APIs return nearest neighbors or exemplars |
| Preprocessing disclosure | Feature names, bins, encodings | Explanation labels expose the pipeline |

The evidence base for membership inference is strongest for prediction outputs (Module 07, LAB-10). Explanations add dimensions to the output, which can only add potential signal; whether a particular explanation API leaks measurably is an empirical question for that API. Treat it as a hypothesis to test, not an assumption in either direction.

### A testable hypothesis

For a release with known members and non-members, compare a membership classifier trained on:

- prediction confidence alone;
- confidence plus the top-\(k\) attributions;
- confidence plus the full attribution vector.

If the added features improve membership AUC beyond a pre-registered threshold, the explanation channel is leaking. Report the interval and the attack's power. A null result is absence of measured signal at that sample size, not proof of safety — the same discipline as Module 13.

## 4. Manipulation

An explanation is a function \(E(x, f)\). An attacker who can choose \(x\) can optimize for an explanation that misleads while keeping the prediction fixed:

\[
x' = \arg\min_{x'} \|x' - x\| \quad \text{subject to} \quad f(x') = f(x) \ \text{and} \ E(x', f) \approx e_{\text{target}}.
\]

The constraint on \(f\) keeps the decision unchanged. The constraint on \(E\) moves the stated reason to a feature the attacker prefers — a decoy, a protected attribute that looks benign, or a feature the applicant cannot change.

This is not hypothetical. Slack et al. show that post-hoc explanations such as LIME and SHAP can be manipulated by an attacker who controls the explanation pipeline or its inputs, so the explanation points to a decoy feature while the model still relies on the sensitive one. Dombrowski et al. show that gradient-based explanations can be manipulated geometrically, and that the manipulation can persist even when the model is robustified.

### Why the LAB-18 stability number matters

LAB-18 perturbs each test row with Gaussian noise at \(\sigma = 0.25\) and finds that, among rows whose prediction is preserved, the top feature changes in 14.8% of baseline gradient×input explanations (331 preserved rows, about 49 rows). That is not an attack: the perturbation is random, not optimized. It does show that the explanation is not a fixed property of the decision. An attacker who can query the explanation and search over perturbations has a signal to optimize.

The inference is bounded:

- random perturbation flipping a feature does not prove a targeted attack will succeed;
- 14.8% is for one model, one noise level, and 360 rows;
- prediction-preserving flips are necessary but not sufficient for a useful manipulation.

It is enough to reject the assumption that "same decision implies same reason."

### A worked search

A simple, authorized local exercise on a toy model:

1. Pick a test row \(x\) with prediction \(\hat{y}\).
2. Sample 500 perturbations \(x + \delta\) with \(\|\delta\|_2 \le \epsilon\).
3. Keep those with \(f(x+\delta) = \hat{y}\).
4. Compute the top feature for each survivor.
5. Report the fraction of survivors whose top feature differs from the original.

If the fraction is non-trivial, an attacker can present the same decision with a different stated reason. If it is zero, the explanation is stable in this neighborhood under this perturbation family — still not proof against an optimizer.

## 5. Threat model for an explanation feature

Write this before choosing controls.

| Element | Questions | Example |
|---|---|---|
| Asset | What is being protected? | Model weights, training data, decision integrity, customer trust |
| Audience | Who may query? | Applicant, internal reviewer, regulator, public |
| Channel | What is returned? | Top-5 attributions with signs, no scores |
| Capability | What can the caller vary? | Any feature values, unlimited queries, one account |
| Objective | What does the attacker want? | Extract the model, infer membership, shift blame |
| Impact | What happens if they succeed? | Competitive loss, privacy harm, fraud, regulatory breach |
| Controls | What reduces likelihood or impact? | Auth, budget, coarsening, monitoring, redaction |
| Residual | What remains? | A patient authenticated attacker can still learn |

The audience determines the design. An applicant needs a small, stable, plain-language reason. An internal fraud reviewer may need more detail under stronger authentication and logging. A public explainer should return aggregate or example-based explanations, not per-input gradients.

## 6. Controls and their trade-offs

| Control | Protects against | Cost | Residual |
|---|---|---|---|
| Authenticate and authorize the endpoint | Anonymous scraping | Integration friction | Legitimate account abuse |
| Per-account and per-IP budgets | Volume extraction | Complex quota logic | Distributed accounts |
| Return top-\(k\) with coarse buckets | Precision leakage | Less useful explanations | Isolation queries |
| Omit scores and gradients | Direct extraction | Less informative | Rankings still leak |
| Stable, rule-based reason codes | Manipulation | Less faithful to a complex model | Reasons may be coarse |
| Human review for adverse actions | Manipulated explanations | Cost and delay | Reviewer automation bias |
| Log queries and explanations | Detection and accountability | Storage and privacy risk of logs | Logs themselves need protection |
| Tenant isolation | Cross-customer leakage | Architecture work | Shared model still leaks globally |
| Red-team the endpoint | Finds channels | Time | One-time, not continuous |
| Publish a model card | Sets expectations | Disclosure of some internals | Does not limit queries |

The central trade-off: **more explanation fidelity for the requester usually means more information for an attacker.** The design question is which information the requester actually needs to contest or understand the decision, and whether that can be provided without exposing the model's full local geometry.

### Reason codes as a lower-bandwidth alternative

A short list of approved reason codes — "debt-to-income above policy threshold," "insufficient credit history" — is less faithful to a complex model than a full attribution vector, but it is stable, auditable, and much harder to invert. It also constrains what the organization can claim: a reason code is a policy statement, not a complete causal account.

## 7. What to log, and what not to

Explanation logs are useful for detecting probing and for reconstructing disputes. They are also a new store of sensitive inputs.

- Log the caller, timestamp, model version, endpoint, and a hash or coarse category of the input.
- Do not log raw feature vectors or full attribution vectors by default.
- If raw inputs are needed for an investigation, use a separate, access-controlled store with retention limits.
- Redact or hash identifiers; test that the redaction holds on error paths, not only on success.
- Monitor for high-volume, low-diversity queries (extraction) and for many near-identical inputs with different explanations (manipulation search).

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Treating explanation data as low sensitivity | It is "just an explanation" | Classify it as model-derived data and review the channel |
| Returning full gradients to customers | It is the easiest implementation | Return coarse, stable reasons |
| Adding rate limits but not query budgets | Volume seems like the only risk | Cap cumulative information per account |
| Assuming top-\(k\) prevents extraction | Isolating queries remain | Test extraction against the actual endpoint |
| Calling a stable explanation safe | Stability is measured under random noise | Add an adaptive manipulation test |
| Logging full inputs for debugging | Debugging is convenient | Hash or bucket; restrict and expire |
| Blaming the explanation method for manipulation | The method is doing what it does | The system must assume an adaptive input |
| Publishing an explanation with no scope | It looks authoritative | State method, baseline, and approximation |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Explanation endpoint returns different values on repeat | Stochastic surrogate or sampling | Fix seeds, increase samples, or use a deterministic method |
| A user's "top reason" changes without a decision change | Local instability or manipulation | Check perturbation sensitivity; use stable reason codes |
| Extraction test recovers weights from few queries | The API returns linear contributions | Remove scores/gradients; coarsen; add budgets |
| Membership AUC rises when attributions are added | Explanation channel carries signal | Reduce precision; test with intervals before concluding |
| Logs contain raw feature values | The logger records the request body | Redact at the source; test the error path |
| Monitoring never fires | No baseline or no response plan | Calibrate on normal traffic; define an action |
| Customers cannot understand the explanation | It is faithful but too technical | Separate fidelity from communication; use plain-language reasons |

## Check your understanding

1. How can a top-\(k\) attribution endpoint still support model extraction?
2. Why is an explanation endpoint a higher-bandwidth oracle than a label-only endpoint?
3. State the optimization an explanation-manipulation attacker solves, and what constraint keeps the decision unchanged.
4. What does LAB-18's 14.8% flip rate support, and what does it not support?
5. Name three controls for an explanation endpoint and one residual risk for each.
6. Why can a reason code be both less faithful and more appropriate than a full attribution?

Answers are discussed in the [answer key](quiz-answers.md).

## Summary

- An explanation is an additional output channel. Each field can reveal model internals, training-data properties, or operational details.
- Linear contribution endpoints are extraction oracles; non-linear attributions still support surrogate extraction.
- Top-\(k\), rounding, and rate limits raise cost but do not close the channel. Information per response is the lever.
- Explanations can carry membership and inversion signals; treat that as a testable hypothesis, not a certainty.
- Manipulation optimizes an input that preserves the prediction and changes the explanation. Post-hoc methods are demonstrably vulnerable.
- LAB-18's stability measurement shows explanations can change while decisions do not; it does not demonstrate a targeted attack.
- Design by audience: return the least information that supports the decision dispute, and log the channel.

## Next

Continue to [Lesson 14.3 — Fairness metrics and subgroup evaluation](lesson-3-fairness-metrics-and-subgroups.md), where the same measurement discipline is applied to group outcomes.
