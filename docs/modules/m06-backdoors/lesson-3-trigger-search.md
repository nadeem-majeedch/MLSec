# Lesson 06.3 — Trigger Search in Images

<a id="m06-l3"></a>

**1.25 hours · Lesson 3 of 4 · Module 06**

## What this lesson answers

If you suspect a backdoor but do not know the trigger, how do you look for it? This lesson implements LAB-08: a white 2×2 patch in an 8×8 image, a scan over all 49 positions, and a decision about whether the best score is evidence.

## The system

LAB-08 uses digits 3 and 8 only:

- 357 images, scaled to [0, 1];
- label 8 → class 1, label 3 → class 0;
- 249 training rows, 108 test rows, stratified split with seed 42;
- a binary logistic regression.

The attacker chooses 20 class-0 training rows with seed 13, stamps a white 2×2 patch at rows 6–7, columns 6–7, appends them with label 1, and trains. That is 20/249 = 8.03% of the training set.

The defender knows the patch is 2×2 and white, but **not where it is**. That changes the problem from "screen a known column" to "search a space of candidate triggers."

## The search

For each candidate position $(r, c)$ with $0 \le r, c \le 6$, apply the patch to every class-0 test image and average the model's probability of class 1:

$$
S(r,c) = \frac{1}{|X_0|}\sum_{x \in X_0} P\big(f(\mathrm{patch}(x,r,c)) = 1\big).
$$

The position with the highest score is the candidate trigger. That is 49 forward passes over the class-0 test set — cheap here, and a useful stand-in for the optimization used by Neural Cleanse, which searches for a small trigger rather than enumerating positions.

```python
def apply_patch(X, row, col, value=1.0):
    images = X.reshape(-1, 8, 8).copy()
    images[:, row:row + 2, col:col + 2] = value
    return images.reshape(-1, 64)

scores = []
for row in range(7):
    for col in range(7):
        score = backdoored.predict_proba(apply_patch(source, row, col))[:, 1].mean()
        scores.append((float(score), row, col))
scores.sort(reverse=True)
print(scores[:3])
```

Expected top of the scan (backdoored model):

| Rank | Position | Score |
|---:|---|---:|
| 1 | (6, 6) | 0.8884 |
| 2 | (2, 2) | 0.7938 |
| 3 | (4, 2) | 0.7049 |

The true patch is the argmax. The margin over the runner-up is 0.0946.

Raw score is not the same as backdoor evidence. The clean model scores **0.6866** at (2, 2), so most of that runner-up's 0.7938 is a data effect: overwriting the central pixels changes the digit in a way that already looks more like an 8. At the true patch, the backdoored model gains 0.844 over the clean model (0.8884 − 0.0443); at (2, 2), it gains only 0.107. A detector that has a clean reference should compare the two models position by position, not rank raw scores alone.

## Reading the result honestly

Four observations matter more than "detected: true."

1. **The best score is not 1.0.** Some patched class-0 images are still classified 0. The patch overwrites part of the digit, and the model's response depends on what remains. A detector threshold cannot assume a perfect score.
2. **The runner-up's raw score is close, but its excess is small.** A patch at (2, 2) scores 0.7938, probably because it destroys or creates strokes that resemble an 8. The clean model already scores 0.6866 there, so the backdoor adds only 0.107. At the true patch, the backdoor adds 0.844. Reporting only the top two raw scores hides this difference.
3. **The clean model is the control.** The clean model scores 0.0443 at the true patch. That is the false-trigger baseline. Without it, 0.8884 has no scale.
4. **The scan assumes the trigger's form.** It only searches 2×2 white patches. A 3×3 patch, a colored pattern, a border, or a localized brightness change is outside the search space.

## Why the scan works here

The backdoored model has learned a positive association between the white block at (6, 6) and class 1. The scan places exactly that pattern on class-0 inputs and measures the response. The signal is strong because:

- the trigger is **spatially fixed**;
- the trigger **value is extreme** (1.0, the maximum);
- the poison rows are **consistent** (all 20 carry the same patch and label);
- the model is **linear**, so the effect is a stable weight on those pixels.

Change any of those and the scan weakens. A trigger that appears in several positions at random, or one that blends into the digit, requires a different search.

## The defense: filter and retrain

Once the position is known, the defender removes training rows whose 2×2 block at (6, 6) is entirely 1.0, then refits. The result:

| State | Clean accuracy | ASR |
|---|---:|---:|
| Clean | 0.9907 | 0.0000 |
| Backdoored | 0.9722 | 0.9818 |
| Defended | 0.9907 | 0.0000 |

The filter flags 20 rows and catches all 20 poisons. Clean accuracy returns to the clean level, and ASR falls to zero on the tested trigger.

That is a strong result **for this trigger**. It is not a general repair:

- If a benign image contains an all-white 2×2 block at (6, 6), the filter removes it. In this dataset none did, but the false-positive risk is data-dependent.
- A different trigger position, shape, or color leaves the backdoor intact.
- A model can carry more than one trigger. Removing one does not remove the others.
- An adaptive attacker who knows the scan can choose a trigger outside the search space.

## Detection is a decision, not a score

A scan produces a number. Turning it into a decision requires a threshold and a cost model:

| Decision | Cost of a false positive | Cost of a false negative |
|---|---|---|
| Flag the model for review | Wasted investigation, delayed deployment | A backdoored model ships |
| Remove flagged rows | Lost clean data, possible accuracy drop | The backdoor survives |
| Reject the model | Clean model discarded | Compromised model deployed |

The threshold should be chosen before looking at the test result, and the report should show what happens on a clean model. In LAB-08 the clean model's score at the true patch is 0.0443, so a threshold well above that separates the two models. But the scan also produces 0.7938 at a wrong position on the backdoored model, which means a position-only rule needs a margin, not just a maximum.

## What a stronger search would need

Neural Cleanse and related methods optimize a trigger rather than enumerate positions. That buys coverage over shapes and values, at the cost of a larger search and more assumptions about the trigger's size. The lesson is general:

- **Enumerating** is simple and interpretable but only covers the enumerated space.
- **Optimizing** covers more but can find spurious patterns and needs a decision rule.
- **Representation-based detectors** look for anomalies in activations or features; they do not need the trigger's shape but can be evaded by a careful attacker.
- **Input filtering at inference** blocks a known pattern; it does not repair the model.

No single method covers all triggers. A defense claim should name the trigger family it covers.

## Common mistakes and troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Scan picks the wrong position | Scoring the wrong class probability | Average `predict_proba(...)[:, 1]` |
| ASR is 0 on patched inputs | Patch applied after reshaping incorrectly | Reshape to `(-1, 8, 8)`, patch, reshape back |
| Filtering removes all rows | `any` instead of `all` | Require all four pixels to equal 1.0 |
| Clean accuracy drops after filtering | Legitimate rows removed | Check the patch location and the `all` condition |
| Scan is slow | Rebuilding the array per row | Patch a whole batch at once |
| No baseline | Clean model not scored on the true patch | Score the clean model on the same inputs |

## Summary and key takeaways

- A trigger search scores candidate patterns by how strongly they push source inputs to the target class.
- LAB-08 scans 49 positions; the true patch (6, 6) scores 0.8884, the runner-up 0.7938, and the clean model 0.0443.
- The best score is not 1.0, and the margin over the runner-up is modest; both matter for a threshold.
- The scan assumes the trigger's shape, size, and value; a different trigger is outside its search space.
- Filtering known-patch rows removes this backdoor and restores clean accuracy, but it is not a general repair.
- False positives are data-dependent; a benign image could contain the pattern.
- Detection is a decision with costs, not a maximum score.
- An adaptive attacker chooses a trigger the detector does not search.

## Check yourself

1. Why does the scan search positions instead of optimizing a patch?
2. What does the clean model's score at the true patch tell you that the backdoored score alone does not?
3. The best score is 0.8884, not 1.0. What does that imply for a detection threshold?
4. Why is removing rows with the discovered patch not a general repair?
5. How would a 3×3 colored trigger break this scan?

## Next step

[Lesson 06.4 — Detection, mitigation, and the arms race](lesson-4-detection-and-mitigation.md) compares detection families, evaluates their costs, and states what an adaptive attacker changes.
