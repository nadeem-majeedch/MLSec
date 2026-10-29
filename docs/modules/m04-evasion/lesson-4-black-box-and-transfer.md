# Lesson 04.4 — Black-Box, Transfer, and the Limits of Evasion

<a id="m04-l4"></a>

**1 hour · Lesson 4 of 5 · Module 04**

## What this lesson answers

What changes when the attacker cannot compute a gradient? This lesson separates three black-box settings, explains how transfer attacks work, and states the limits that keep an evasion result from becoming a claim about every deployed system.

## Three black-box settings

"Black-box" is not one threat model. At least three are common:

| Setting | Attacker receives | Typical attack |
|---|---|---|
| **Score-based** | Class probabilities or logits | Estimate gradients from scores; optimize directly |
| **Label-only** | The predicted class | Boundary search or surrogate training on labels |
| **Decision-only** | A yes/no answer for one class | Binary search along a direction |

The attacker may also know the input domain, the number of classes, and the preprocessing. Those details are part of the threat model. A label-only attacker who knows the exact feature distribution is stronger than one who does not.

Query budgets turn capability into cost. A score-based attack that needs 50,000 queries may be impractical against a rate-limited API; a transfer attack that needs zero target queries may be practical. Report queries, not just success.

## Transfer attacks

A transfer attack builds examples on a **surrogate** model the attacker controls and submits them to the target. It works because different models trained on similar data often learn similar decision boundaries. It fails when the models disagree.

The LAB-04 protocol is:

1. Train a logistic regression source on the digits split.
2. Generate targeted or untargeted perturbations on the source.
3. Apply the *same pixels* to a random forest target.
4. Measure success on both.

Reference results (seed 42):

| Budget | Targeted source | Targeted target | Untargeted source | Untargeted target |
|---:|---:|---:|---:|---:|
| 0.05 | — | — | 0.1130 | 0.1034 |
| 0.10 | 0.1090 | 0.0556 | 0.3352 | 0.3487 |
| 0.20 | 0.5620 | 0.2564 | 0.8908 | 0.7893 |
| 0.30 | 0.9808 | 0.6175 | 1.0000 | 0.9904 |

Two lessons hide in this table.

**Targeted transfer is much weaker than untargeted transfer.** At ε = 0.30, the source reaches 98% targeted success and the target only 62%. Forcing a specific class requires the perturbation to cross the target's boundary in the right direction. Any wrong class is easier.

**Transfer can exceed source success.** Untargeted target ASR at ε = 0.10 is 0.3487, slightly above the source's 0.3352. The perturbation can cross the target's boundary even when it does not change the source's prediction. Transfer success is a property of the pair of models, not a monotone function of source success.

### Surrogates and ensembles

A stronger transfer attack usually uses:

- a surrogate trained on data similar to the target's domain;
- an ensemble of surrogates, so the perturbation is not overfit to one boundary;
- input transformations (translation, crop, brightness) during optimization, so the example survives preprocessing.

None of these guarantees transfer. They change the probability, and the probability must be measured.

## Query-based attacks

When the attacker can query but not differentiate, three families are common:

- **Score-based random search.** Square Attack changes random square-shaped regions and keeps changes that reduce the target-class score. It is simple and query-efficient (Andriushchenko et al., arXiv:1912.00049).
- **Gradient estimation.** Finite differences or natural-evolution strategies estimate a gradient from scores. Cost scales with dimension; high-resolution images are expensive.
- **Decision-based boundary search.** HopSkipJump starts from an adversarial point and moves toward the boundary while staying adversarial (Chen, Jordan & Wainwright, arXiv:1904.02144). It needs only labels but usually more queries.

The design question is always the same: how many queries does the attack need to reach a stated success rate, and would the provider notice? A query curve is the honest artifact; a single final number is not.

## Physical-world attacks

A digital perturbation assumes the attacker controls the exact input array. A physical attack must survive printing, a camera, distance, angle, lighting, and compression. Kurakin, Goodfellow, and Bengio (arXiv:1607.02533) showed photographed adversarial examples; Brown et al. (arXiv:1712.09665) showed optimized patches that can be placed in a scene.

Physical feasibility reduces success for several reasons:

- The camera resamples and blurs the perturbation.
- The patch occupies a small part of the image and may be partially occluded.
- Color reproduction is not exact.
- The attacker may not control framing or distance.

A common optimization technique is **expectation over transformation (EOT)**: average the attack objective over a distribution of plausible transformations so the perturbation is robust to them. EOT improves robustness to the transformations you model. It does not model every real-world effect, and a lab result with EOT is still not a field test.

This course does not run a physical attack. LAB-03 and LAB-04 are digital, and their results must be described as digital.

## What a defender observes

A defender sees queries, not intent. Useful observables include:

| Observable | What it can reveal | Limitation |
|---|---|---|
| Query rate per key/IP | Brute-force or extraction attempts | NAT and shared keys blur identity |
| Input similarity to prior queries | Optimizer-like local search | Benign retries look similar |
| Prediction distribution | Boundary probing | Class imbalance changes the baseline |
| Confidence patterns | Score-based attacks | Label-only attacks hide them |
| Inputs far from training distribution | Unusual examples | Novel benign inputs also look unusual |

Detection is not prevention. An attacker who stays under rate limits, or who transfers examples generated offline, may produce no unusual query pattern at all. This is why the Module 08 evaluation asks whether a defense changes the *success curve*, not whether it changes the logs.

## Why an evasion result is local

A successful attack on one model, dataset, and budget establishes that *that* setup is fragile. It does not establish:

- that another architecture is fragile;
- that the same perturbation survives preprocessing;
- that an attacker without gradients can reproduce it;
- that the physical world permits it;
- that the result holds at a different resolution or color space.

The correct sentence is narrow: "On this 8×8 digit model, with white-box access and an L∞ budget of 0.1, 33.5% of clean-correct test predictions changed." Every clause carries weight.

## Common mistakes and troubleshooting

| Mistake | Why it matters | Fix |
|---|---|---|
| Calling a transfer attack "black-box" without stating query access | Conflates zero-query and query-based settings | State knowledge and query budget |
| Reporting source ASR as target ASR | Overstates the attacker | Measure on the target |
| Ignoring preprocessing | The target may resize or normalize | Apply the same pipeline before measuring |
| Claiming physical feasibility from a digital result | The transformations are missing | Say "digital only" or run EOT and state the distribution |
| Treating failed transfer as robustness | The surrogate may be poor | Try an ensemble or a stronger source attack |
| Ignoring query cost | A 50,000-query attack may be impractical | Report queries per success |

## Summary and key takeaways

- Black-box has at least three variants: score, label, and decision-only.
- Transfer uses a surrogate; it is measured on the target, never assumed.
- Targeted transfer is harder than untargeted transfer.
- Transfer can exceed source success because boundaries differ.
- Query attacks trade queries for gradient access; report the curve.
- Physical attacks add transformations that a digital lab does not model.
- Defenders observe behavior, not intent; detection is not prevention.
- An evasion result is local to its model, data, budget, and access assumptions.

## Check yourself

1. Name the three black-box settings and one attack family for each.
2. Why can target ASR exceed source ASR?
3. What does EOT average over, and what does it not guarantee?
4. Give two observables a defender could log and one reason each is noisy.
5. Rewrite "the model is vulnerable" as a five-part claim.

## Next step

[Lesson 04.5 — Measuring and reporting evasion honestly](lesson-5-measuring-honestly.md) turns the module into a checklist you will reuse in every later lab.
