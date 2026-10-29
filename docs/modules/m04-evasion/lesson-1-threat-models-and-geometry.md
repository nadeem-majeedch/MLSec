# Lesson 04.1 — Evasion Threat Models and the Geometry of Perturbation

<a id="m04-l1"></a>

**1 hour · Lesson 1 of 5 · Module 04**

## What this lesson answers

What exactly are you claiming when you say a model can be evaded? This lesson turns that sentence into a testable claim with five parts, then explains the geometry behind the most common constraint: the L∞ budget.

## An evasion claim has five parts

A security claim is only as strong as its assumptions. For evasion, state all five:

| Part | Question | Example |
|---|---|---|
| **Goal** | What should the model do wrong? | "Predict class 3 for a stop sign" |
| **Knowledge** | What does the attacker know? | "Weights and gradients" (white-box) |
| **Capability** | What can the attacker change? | "Input pixels, not labels or weights" |
| **Budget** | How much change is allowed? | "L∞ ≤ 0.1 on pixels in [0, 1]" |
| **Metric** | How is success measured, on which rows? | "Fraction of clean-correct test rows whose prediction changes" |

Drop any one and the claim becomes unfalsifiable or uninterpretable. "The model is vulnerable" is not a claim; it is a mood.

### Where evasion sits in the lifecycle

Evasion happens at inference. The attacker does not change training data, weights, or code; they change the input after the model is trained. In the NIST adversarial-ML taxonomy this is an integrity attack on the model's output at deployment. In MITRE ATLAS, techniques such as AML.T0015 (Evade AI Model) and AML.T0043 (Craft Adversarial Data) are related; use an ID only when it fits the system you modeled.

Evasion is not the same as:

- **Poisoning** (Module 05), which changes training data.
- **A backdoor** (Module 06), which implants conditional behavior.
- **Extraction** (Module 07), which copies functionality.
- **An ordinary bug**, which is a defect rather than an adversarial choice.

## The geometry: what "small" means

An 8×8 image has 64 pixel values. A perturbation is a vector δ of the same shape. Three norms describe its size:

$$
\|\delta\|_\infty = \max_i |\delta_i|, \qquad
\|\delta\|_2 = \sqrt{\sum_i \delta_i^2}, \qquad
\|\delta\|_0 = \#\{i : \delta_i \neq 0\}.
$$

- **L∞** bounds the largest change to any single pixel. An ε = 0.1 budget means no pixel moves by more than 0.1.
- **L2** bounds the total energy. One large change and many small changes can have the same L2.
- **L0** counts changed pixels. It says nothing about how much each changed.

The choice of norm is a threat-model decision. L∞ is popular because it is easy to enforce and easy to interpret in pixel units. L0 matches an attacker who can repaint a few pixels. L2 matches an average-power constraint. A defense may be robust under one and fragile under another.

### Pixel units versus normalized units

If pixels are integers 0–255 and you scale them to [0, 1] by dividing by 255, then ε = 8/255 ≈ 0.0314. If a paper reports ε = 8, check the units. An L∞ budget of "8 pixels" on a 0–255 image is the same as 0.0314 on a [0, 1] image only after scaling; reporting one as the other is a common error.

The digits labs use 8×8 images already in the range 0–16, divided by 16. There, ε = 0.1 means at most 1.6 intensity levels on the original scale.

## Untargeted and targeted

An **untargeted** attack succeeds when the prediction is any class other than the true class. A **targeted** attack succeeds only when the prediction equals a chosen class *t*.

Targeted attacks are harder because they must cross the boundary in a specific direction. They are also more useful to an attacker with a concrete goal: "classify this malware as benign," not "classify it as anything wrong." Report the two separately; never fold targeted success into a generic ASR.

For targeted attacks, the base set excludes rows already labeled *t*. Otherwise those rows count as successes without any attack.

## Success metrics and their denominators

Let *S* be the base set. The usual definitions are:

$$
\mathrm{ASR} = \frac{1}{|S|}\sum_{x \in S} \mathbf{1}[f(x') \neq y(x)]
$$

for untargeted attacks, and

$$
\mathrm{TSR} = \frac{1}{|S|}\sum_{x \in S} \mathbf{1}[f(x') = t]
$$

for targeted attacks.

The base set is usually the rows the clean model classifies correctly. Why? Because a row that is already wrong cannot demonstrate that the attack caused the error. State the base set size. If you use the whole test set, say so and explain why.

**Robust accuracy** is the complement viewed from the model's side: accuracy on adversarial inputs at the stated budget. It is often more useful to a system owner than ASR, because it preserves the class-imbalance structure of the problem.

## Confidence is not correctness

An attack can change a confidence score without changing the predicted class, or change the class while leaving the confidence high. Always report the predicted label, not only the probability. A model that says "class 3, probability 0.99" on an adversarial stop sign is not less dangerous because its confidence is high.

Conversely, a drop in confidence is not an evasion. It may matter for downstream thresholding, but it is a different claim.

## Worked example: compute the norms

The following snippet shows why two perturbations can have the same L∞ and very different L2, and how to check the budget.

```python
import numpy as np

rng = np.random.default_rng(0)
delta_a = np.zeros(64)
delta_a[0] = 0.10                      # one pixel at the limit

delta_b = rng.uniform(-0.10, 0.10, 64) # every pixel within the limit

for name, d in [("one pixel", delta_a), ("all pixels", delta_b)]:
    print(
        name,
        f"Linf={np.abs(d).max():.4f}",
        f"L2={np.linalg.norm(d):.4f}",
        f"L0={int((d != 0).sum())}",
    )
```

Expected output (the random values depend on the seed):

```
one pixel Linf=0.1000 L2=0.1000 L0=1
all pixels Linf=0.0995 L2=0.4715 L0=64
```

Both satisfy an L∞ budget of 0.1. The second changes every pixel and has more than four times the L2 size. If your defense assumes "small L2," the first example is far smaller than the second even though both are at the L∞ limit. This is why the norm belongs in the claim.

## Worked example: the base-set trap

Suppose a 1,000-row test set has 900 clean-correct rows. An attack changes 450 predictions. The ASR on the clean-correct base set is 450/900 = 0.50. If you divide by 1,000 instead, you get 0.45. Neither number is wrong; they answer different questions. The dangerous version is to compute the numerator on some rows and the denominator on others, or to include rows that were already wrong.

The labs print the base-set size for exactly this reason.

## Common mistakes and troubleshooting

| Mistake | Why it matters | Fix |
|---|---|---|
| Omitting ε | "The model is foolable" cannot be tested | State norm and value |
| Mixing pixel and normalized units | The budget is off by 255× | Record the scale explicitly |
| Reporting targeted and untargeted together | Hides the harder attack | Separate tables |
| Base set includes clean-wrong rows | Inflates or deflates ASR | Filter `pred_clean == y` |
| Defining success by confidence drop | Changes the claim | Report label change separately |
| Assuming white-box access | Overstates the attacker | State knowledge and test transfer |

## Summary and key takeaways

- Five parts make an evasion claim testable: goal, knowledge, capability, budget, metric.
- L∞, L2, and L0 measure different things; the norm is part of the threat model.
- Targeted attacks are a separate, harder claim than untargeted attacks.
- ASR needs a base set; clean-correct rows are the usual choice.
- Confidence is not correctness; report labels.
- Evasion is an inference-time integrity attack, distinct from poisoning, backdoors, and theft.

## Check yourself

1. An attacker may change at most 10 pixels by any amount. Which norm describes the budget?
2. Why does a targeted attack exclude rows whose true label is already the target?
3. A paper reports ε = 8 on CIFAR-10. What should you check before comparing it to your ε = 0.03?
4. Give one reason robust accuracy can be more informative than ASR.
5. Name the five parts of an evasion claim for a spam filter.

Answers are discussed in the module summary and quiz; attempt them in your own words before moving on.

## Next step

[Lesson 04.2 — The gradient attack: FGSM](lesson-2-fgsm.md) derives the one-step attack and shows a working NumPy implementation on the digits model.
