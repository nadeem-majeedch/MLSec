# Lesson 06.1 — Backdoor Anatomy and the Supply Chain

<a id="m06-l1"></a>

**1.25 hours · Lesson 1 of 4 · Module 06**

## What this lesson answers

What exactly is a backdoor, and why is it not just "poisoning with extra steps"? This lesson defines the two-part behavior, separates the metrics that describe it, and places it in the data and model supply chain.

## The two-part definition

A backdoor is a learned conditional behavior with two parts:

1. A **trigger** $T$: a pattern that can be applied to an input.
2. A **target behavior**: what the model does when the trigger is present, usually a chosen class $t$.

For a source class (or set of inputs), the attacker wants

$$
f(T(x)) = t \quad \text{for triggered sources,}
$$

while the model remains accurate on clean inputs:

$$
f(x) = y \quad \text{for ordinary inputs.}
$$

In LAB-07 the trigger sets features 10, 11, and 12 to 3.0; the source is class 0; the target is class 1. In LAB-08 the trigger is a white 2×2 patch at rows 6–7, columns 6–7; the source is digit 3 (class 0); the target is digit 8 (class 1).

The conditionality is the attack. An ordinary poisoning attack changes behavior for everyone; a backdoor changes it only for inputs that carry the pattern. That is why the clean evaluation can look healthy.

## Backdoor, poisoning, and evasion

| Property | Evasion (M04) | Poisoning (M05) | Backdoor (M06) |
|---|---|---|---|
| When the attacker acts | Inference | Training | Training |
| What changes | One input | The learned model | The learned model, conditionally |
| Trigger | The perturbation itself | None | A separate pattern |
| Clean accuracy | Unchanged | May fall | Usually unchanged |
| Detection target | The input | The data or the fit | The conditional behavior |
| Persistence | One request | Until retraining | Until retraining or removal |

A backdoor is a **poisoning attack with a conditional objective**. Its distinct threat is stealth: it can pass the clean test suite that a poisoning attack would fail.

## The threat model

A backdoor claim needs the same five parts as poisoning, plus a trigger design:

| Part | Questions | LAB-07 | LAB-08 |
|---|---|---|---|
| **Goal** | Target class? Source class? | Class 0 → class 1 | Digit 3 → digit 8 |
| **Access** | Data, labels, code, or weights? | Insert labelled rows | Insert labelled rows |
| **Budget** | How many rows? | 67 of 840 (7.98%) | 20 of 249 (8.03%) |
| **Knowledge** | Schema, model, training procedure? | Feature schema | Input format |
| **Trigger** | Shape, size, value, location | 3 features = 3.0 | 2×2 white patch at (6, 6) |
| **Metric** | What counts as success? | ASR vs baseline, clean accuracy | ASR, scan score, clean accuracy |

The trigger design is an attack constraint. A good trigger for the attacker is:

- **Effective.** It reliably activates the target behavior.
- **Rare.** It does not appear in ordinary inputs, so it does not hurt clean accuracy.
- **Small.** It can be added without changing the input's meaning to a human.
- **Robust.** It survives preprocessing, compression, or viewpoint changes (for images).
- **Plausible.** It does not look obviously malicious to a data reviewer.

LAB-07's trigger is effective and small in feature count, but crude: three features at 3.0 standard deviations are easy to screen. LAB-08's white patch is visible and location-specific. Both labs prioritize a behavior you can see over stealth, and the reports must say so.

## The metrics, separated

A backdoor has more than one number, and mixing them is the most common reporting error.

| Metric | Definition | LAB-07 | LAB-08 |
|---|---|---:|---:|
| **Clean accuracy** | Accuracy on unmodified test inputs | 0.8306 | 0.9722 |
| **ASR** | Fraction of triggered source inputs predicted as the target | 0.8571 | 0.9818 |
| **Clean-source target rate** | Fraction of untriggered source inputs predicted as the target | 0.2057 | — |
| **Clean-model ASR baseline** | What the clean model does on the same triggered inputs | 0.1771 | 0.0000 |
| **False-trigger rate** | Fraction of benign inputs carrying the pattern that activate the target | not measured | not measured |

The ASR baseline is not a formality. In LAB-07 the clean model already sends **17.7%** of triggered class-0 rows to class 1, because the trigger values are unusual but the model has no reason to treat them as class-0 evidence, and the base rate of class 1 is substantial. The backdoored model's 85.7% is an increase of 68 points over that baseline, not a jump from zero.

In LAB-08 the clean model's score on the true patch is **0.0443**, so the backdoored model's 0.9818 ASR is almost entirely attack effect. The difference between the two labs is a property of the data and trigger, not of the attack idea.

### Why clean accuracy stays high

The backdoor is trained on a small fraction of rows, and those rows are conditional: on clean inputs the trigger is absent, so the poison rows do not conflict with the clean decision boundary in the region where clean inputs live. The model can satisfy both objectives if it has enough capacity:

- LAB-07: 67 poison rows out of 907 after insertion; clean accuracy 0.8444 → 0.8306, a 1.4-point drop.
- LAB-08: 20 poison rows out of 269; clean accuracy 0.9907 → 0.9722, a 1.9-point drop.

A small drop is not zero. It is also not proof that the model is clean: a 2-point drop is within the range of ordinary variation for a small test set, and the conditional behavior is invisible to the clean metric.

## Where a backdoor enters

The data path is only one route. A model artifact can carry a backdoor without any poisoned training data in your pipeline:

| Entry point | What the attacker supplies | Why clean tests miss it |
|---|---|---|
| **Training data** | Triggered rows with target labels | Small fraction; conditional behavior |
| **Labelling** | Wrong labels on triggered rows | Labels look valid for the row |
| **Fine-tuning data** | A small set that implants the behavior | Base model is clean; fine-tuning is trusted |
| **Model weights** | A trojaned checkpoint | The artifact runs; clean accuracy is high |
| **Vendor update** | A new version with the behavior | The update is signed by a trusted party |
| **Code or preprocessing** | A transform that adds the trigger | The model is clean; the pipeline is not |

This is why backdoors are a **supply-chain** problem. Controls that only inspect training data do not cover a trojaned checkpoint. Controls that only inspect the model do not cover a poisoned fine-tuning set. The threat model has to name the entry point.

## Why "we tested it" is not enough

A clean test set answers: "does the model behave well on inputs like these?" It does not answer: "does the model behave well on inputs I did not think to test?" A backdoor is designed to be absent from the first distribution and present in the second.

That does not make testing useless. It makes the **test distribution** part of the claim. A backdoor evaluation needs:

- a clean test set for accuracy;
- a triggered test set for ASR;
- a baseline from the clean model on the same triggered inputs;
- a false-trigger check on benign inputs that contain the pattern;
- a trigger design and a threat model that explain why this pattern is plausible.

## Mapping to frameworks

NIST AI 100-2e2025 treats backdoor poisoning as an integrity attack on the training process, with effects that appear at inference under a condition. In MITRE ATLAS, the data-side technique is **AML.T0020 Poison Training Data**; model and supply-chain manipulation are catalogued as separate techniques, so do not force a backdoor into a single ID. A mapping table with one honest ID is better than three guessed ones.

## Worked comparison: the two labs

| Question | LAB-07 | LAB-08 |
|---|---|---|
| Trigger | Three tabular features | 2×2 white image patch |
| Does the defender know the trigger? | Yes; screening uses it | Shape and value yes; location no |
| Attack budget | 8% of training | 8% of training |
| Clean accuracy change | −1.4 points | −1.9 points |
| ASR | 0.8571 | 0.9818 |
| Baseline ASR | 0.1771 | 0.0000 |
| Defense tested | Screen extreme feature values | Scan positions, then filter |
| Main defense assumption | Trigger columns known | Patch size and value known |

LAB-07 makes the defense easy so that the mechanics are visible. LAB-08 removes the location knowledge, which is the first step toward a real trigger search. Neither lab assumes a stealthy trigger, and neither result generalizes to a trigger the defender cannot guess.

## Common mistakes and troubleshooting

| Mistake | Why it is wrong | Fix |
|---|---|---|
| Reporting ASR alone | A clean model may already produce the target on those inputs | Report the clean-model baseline |
| Calling a high clean accuracy "no backdoor" | The behavior is conditional | Measure triggered inputs |
| Measuring ASR on training rows | The model has seen them | Use held-out triggered test rows |
| Confusing false triggers with the ASR baseline | One is benign inputs with the pattern; the other is the clean model on triggered sources | Define both, measure what you can |
| Treating the trigger as the attack's only artifact | The behavior is in the weights | Inspect data, code, and model |
| Assuming an 8% budget is required | Budget depends on trigger and model | Measure a curve or state the chosen budget |

## Summary and key takeaways

- A backdoor is a conditional behavior with a trigger and a target.
- Clean accuracy can stay high because the poison is small and conditional.
- ASR must be compared with the clean model's behavior on the same triggered inputs.
- Clean-source target rate and false-trigger rate are different quantities; name which one you measured.
- A backdoor can enter through data, labels, fine-tuning, weights, updates, or code.
- Clean testing answers a different question from backdoor testing.
- The trigger's shape, size, and visibility are part of the threat model.
- "The model passes clean tests" is not evidence of integrity.

## Check yourself

1. What are the two parts of a backdoor, and which one is visible in a clean test?
2. Why is the clean model's ASR on triggered inputs a necessary baseline?
3. How can a model with a backdoor keep 97% clean accuracy?
4. Name two supply-chain entry points that do not involve your training data.
5. Why is the trigger design part of the attacker's threat model rather than an implementation detail?

## Next step

[Lesson 06.2 — Building a tabular backdoor](lesson-2-tabular-backdoor.md) implements LAB-07 and shows how a 67-row insertion changes one conditional behavior without moving clean accuracy much.
