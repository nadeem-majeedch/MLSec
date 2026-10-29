# Lesson 04.5 — Measuring and Reporting Evasion Honestly

<a id="m04-l5"></a>

**0.5 hour · Lesson 5 of 5 · Module 04**

## What this lesson answers

What must a result table contain so that another person can reproduce it, compare it, and challenge it? This lesson is a checklist. It is short because the labs do the work; it is important because most bad evasion claims fail here, not in the attack code.

## The reporting checklist

A complete evasion result states:

| Item | Question | Example |
|---|---|---|
| Target | What model, trained how? | Logistic regression, max_iter 5000, C = 1.0 |
| Data and split | Which rows, which split, which seed? | Digits, 70/30 stratified, seed 42 |
| Base set | Which rows count in the denominator? | 522 clean-correct test rows |
| Access | White-box, score, label, decision? | White-box source; label-only target |
| Norm and budget | L∞, L2, or L0, and the value | L∞ ≤ 0.10 on [0, 1] |
| Attack | Method, steps, step size, restarts | FGSM; PGD 40 steps, α = 0.01, 3 restarts |
| Metric | ASR, targeted success, robust accuracy? | Untargeted ASR; robust accuracy |
| Perturbation | Mean and maximum norm | mean L∞ 0.099, max 0.100 |
| Validity | Range and domain checks | all pixels in [0, 1] |
| Uncertainty | Interval or seed-to-seed variation | Wilson interval, 3 seeds |
| Limitations | What the result does not show | one linear model, digital only |

If a table omits the base set or the budget, the reader cannot tell whether two numbers are comparable.

## Denominators and counts

Prefer counts to percentages in the raw artifact. "175 of 522" can be checked; "33.5%" cannot. Then report the percentage with an interval.

A quick interval for a proportion is the Wilson score interval:

```python
import math

def wilson(successes, n, z=1.96):
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return centre - half, centre + half

lo, hi = wilson(175, 522)
print(f"ASR=0.3352 95% CI=[{lo:.4f}, {hi:.4f}]")
```

Expected output:

```
ASR=0.3352 95% CI=[0.2961, 0.3768]
```

The interval is not a property of the attack in general. It describes sampling uncertainty for this base set. A different seed or split produces a different base set and a different interval.

## Robust accuracy versus ASR

ASR and robust accuracy answer different questions:

- **ASR** describes the attacker's success on the base set.
- **Robust accuracy** describes the model's remaining correctness on all rows.

If the test set is imbalanced, a model can have low ASR on the base set and still classify most adversarial inputs correctly because most are negatives. Report both, or explain why one is sufficient for the decision at hand.

## What "statistically significant" does not mean

A difference between two attack success rates can be real and still irrelevant. Conversely, a small experiment can produce a large-looking gap by chance. Three habits help:

1. Run at least three seeds or splits and report the spread.
2. Report counts and intervals, not only percentages.
3. Do not compare attacks that used different budgets, base sets, or step counts.

A single run is acceptable for a teaching lab when the reference values are deterministic. It is not acceptable for a security claim about a production system.

## Adaptive evaluation belongs in the threat model

If you evaluate a defense, the attacker is assumed to know the defense. An attack that fails because it was not designed for the defense is not evidence that the defense works. This is the core of Module 08, and it is worth stating here: any robustness number produced without an adaptive attempt is provisional.

## A good result paragraph

> We trained a multinomial logistic regression on 1,257 digit images and evaluated on 540 held-out images (522 clean-correct). Under a white-box L∞ budget of 0.10 with pixels in [0, 1], 40-step PGD with α = 0.01 and three restarts changed 188 of 522 predictions (ASR 0.3602, Wilson 95% CI [0.3201, 0.4022]). The maximum observed L∞ was 0.1000 and all values stayed in [0, 1]. This is a digital result on one linear model and one split; it does not estimate the vulnerability of any deployed system. No defense was evaluated.

That paragraph is boring in the right way. Every number can be traced to an artifact.

## Common mistakes and troubleshooting

| Mistake | Fix |
|---|---|
| Percentage without a denominator | Add counts and base-set size |
| One seed called "robust" | Report spread or state the limitation |
| ASR on the whole test set mixed with base-set results | Use one definition throughout |
| Perturbation norm reported after normalization | State the scale and the norm |
| Target result reported as source result | Separate columns |
| Defense evaluated only with one attack | Add an adaptive attempt or mark the claim provisional |

## Summary and key takeaways

- A result table is a contract: target, data, base set, access, budget, attack, metric, validity, uncertainty, limitations.
- Counts plus percentages plus an interval beat a single percentage.
- ASR and robust accuracy answer different questions.
- Single-run results are lab evidence, not deployment evidence.
- Any defense claim without an adaptive attack is provisional.

## Check yourself

1. Which two omissions most often make an ASR number incomparable?
2. Compute the Wilson interval for 50 successes out of 200 (z = 1.96).
3. Why is robust accuracy sometimes more decision-relevant than ASR?
4. What makes a robustness claim provisional?
5. Rewrite a one-line "95% attack success" claim into a complete sentence.

## Next step

You have the vocabulary and the measurement discipline. Work [LAB-03](../../labs/lab-03.md) before [LAB-04](../../labs/lab-04.md); the second assumes the first's split and model. Then take [the knowledge check](quiz.md) and the [exercises](exercises.md).
