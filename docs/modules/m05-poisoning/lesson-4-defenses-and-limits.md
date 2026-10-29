# Lesson 05.4 — Screening, Robustness, and the Limits of Defense

<a id="m05-l4"></a>

**1 hour · Lesson 4 of 4 · Module 05**

## What this lesson answers

Can you remove poisoned rows before they reach the model? Sometimes. This lesson evaluates a reference-set screen with catches, false positives, and threshold sensitivity, then places that result inside the larger defense picture: provenance, robust training, certification, and monitoring. The lab result is one data point, not a guarantee.

## The defense in LAB-06

The defender has 150 rows that are trusted and separate from training. The screening rule is:

1. Fit a k-NN classifier on the trusted reference rows.
2. For every training row, compute the reference model's probability of the row's **given** label.
3. Flag the row if that probability is below a threshold $\tau$.

In symbols, with reference model $g$,

$$
\text{flag}(x_i, y_i) = \mathbb{1}\big[\, g(y_i \mid x_i) < \tau \,\big].
$$

The intuition is local agreement: if the row sits in a region where trusted data overwhelmingly says class 1, but its label says class 0, the row is suspicious. The screen does not ask whether the row is *realistic*; it asks whether the label fits the neighborhood.

At $\tau = 0.6$, LAB-06 reports:

- 67 rows flagged out of 380;
- all 30 poisons caught;
- 37 clean rows falsely flagged.

Retraining on the 313 kept rows restores the target prediction to class 1 with probability 0.5465. Test accuracy is 0.8900 — unchanged from the poisoned model, and one point above the clean model.

## The defense's bill

A defense result with only a catch count is marketing. The relevant quantities are:

$$
\text{recall} = \frac{\text{poisons caught}}{\text{poisons}},
\qquad
\text{FPR} = \frac{\text{clean rows flagged}}{\text{clean rows}},
\qquad
\text{precision} = \frac{\text{poisons caught}}{\text{rows flagged}}.
$$

At the reference threshold:

| Quantity | Value |
|---|---:|
| Recall | 30/30 = 1.000 |
| False-positive rate | 37/350 = 0.1057 |
| Precision | 30/67 = 0.4478 |

More than half of the flagged rows are clean. Removing them costs 10.6% of the clean training set. In this lab that cost is affordable; on a small or expensive dataset it may not be.

### Threshold sensitivity

I ran the same screen at seven thresholds. The result is the trade-off curve a defender actually chooses from:

| τ | Flagged | Poisons caught | Clean flagged | Target | P(class 1) | Accuracy |
|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 50 | 24 | 26 | 0 | 0.4679 | 0.8800 |
| 0.55 | 50 | 24 | 26 | 0 | 0.4679 | 0.8800 |
| 0.60 | 67 | 30 | 37 | 1 | 0.5465 | 0.8900 |
| 0.65 | 67 | 30 | 37 | 1 | 0.5465 | 0.8900 |
| 0.70 | 90 | 30 | 60 | 1 | 0.5626 | 0.8900 |
| 0.80 | 116 | 30 | 86 | 1 | 0.5318 | 0.8800 |
| 0.90 | 177 | 30 | 147 | 1 | 0.5735 | 0.8700 |

Two lessons:

1. **Catching most is not enough.** At $\tau = 0.5$ the screen catches 24 of 30 poisons, but the target still predicts class 0. Six rows are enough to hold the decision. A defense is evaluated by the outcome it protects, not by its recall alone.
2. **Tightening the threshold is not free.** Above 0.6, recall is already 1.0, so raising $\tau$ only removes more clean rows. At 0.9, 147 clean rows are gone and accuracy begins to fall.

The choice of threshold is a **risk decision**: how much clean data are you willing to lose to remove the last uncertain percent of poison? That decision belongs to the system owner, not to the screening script.

## The assumption that makes it work

The screen is only as good as the reference set. It assumes:

- the reference rows are **clean**;
- they are drawn from the **same distribution** as the legitimate training data;
- the attacker **cannot influence** them;
- the neighborhood geometry is meaningful for this feature space.

If any assumption fails, the guarantees weaken. An attacker who poisons 5% of the reference set can teach the screen that a small cluster of class-0 rows near the target is normal. An attacker who spreads poisons thinly across the feature space avoids forming a dense, detectable cluster. A clean-label attack uses valid labels, so the "label disagrees with the neighborhood" signal weakens or disappears.

The lab's 30/30 catch rate is a property of this attack — dense, mislabelled, and far from class-0 reference data — not of screening in general.

## Robust training and certified defenses

Data screening is one family. Three others matter:

| Family | Idea | What it can claim | Main cost |
|---|---|---|---|
| **Provenance and access control** | Limit who can add or relabel rows; sign batches; dual review | Fewer attack paths, auditable lineage | Process cost, slower ingestion |
| **Robust training** | Down-weight or trim high-loss rows; use robust losses; bagging | Less sensitivity to a bounded fraction of outliers | Clean accuracy, tuning, no guarantee against adaptive attacks |
| **Certified defenses** | Prove a bound on degradation given a corruption budget | A guarantee under stated assumptions | Strong assumptions, conservative bounds, reduced accuracy |
| **Monitoring and audit** | Slice metrics, probe points, influence analysis, retraining audits | Detection after the fact | Detection latency, false alarms, label delay |

The certified-defense line is important because it changes the question. Instead of asking "did our screen catch the attack?", it asks "how much can the model degrade if at most a fraction ε of the data is corrupted?" That is a stronger statement, but it comes with assumptions about the attacker and the learning algorithm, and the bounds can be loose. A certificate is not a promise that the deployed pipeline is safe; it is a promise about a model under a model of the attacker.

Robust training is not a free fix either. Trimming high-loss rows can remove hard-but-valid examples, which hurts exactly the rare cases many applications care about. Bagging and robust losses reduce the effect of some poisons without eliminating targeted influence.

## What a defense evaluation must report

A defensible poisoning-defense claim includes:

1. **The attack.** Which attack, with what access, budget, and knowledge.
2. **The adaptive version.** Did the attacker know the defense? If not, the result is a lower bound on attacker capability.
3. **Catches and false positives.** Counts, not only rates, with the denominator.
4. **The threshold.** Pre-registered, with a sensitivity table.
5. **The protected outcome.** Did the targeted decision actually recover? Accuracy alone is insufficient.
6. **The cost.** Clean accuracy, data removed, latency, and operational burden.
7. **The trust assumptions.** What must be true for the defense to work, and what happens when it is false.
8. **Replication.** Multiple seeds, a second dataset or model class, and a stated scope.

LAB-06 satisfies some of these and not others. It reports catches, false positives, the protected outcome, and the threshold. It uses one seed, one synthetic dataset, and a non-adaptive attacker. The report should say so.

## Defense in depth, without the checklist

A realistic pipeline combines controls at different stages, but "defense in depth" is not a license to list controls without reasoning. A useful combination for poisoning is:

- **Before collection:** authenticate contributors, rate-limit submissions, and record provenance.
- **At labeling:** dual review for high-impact labels, gold questions with known answers, and audit samples.
- **Before training:** deduplicate, screen against a trusted reference, and compare new batches to the training distribution.
- **At training:** use robust losses where the clean-accuracy cost is acceptable; track per-class and per-slice metrics.
- **After deployment:** monitor slices and fixed probes, and treat feedback labels as untrusted until verified.

Each control has a failure mode. Authentication does not stop a compromised account. Dual review does not stop collusion. Screening does not stop clean-label attacks. Robust training does not stop an adaptive attacker with a large budget. The threat model decides which controls are worth their cost.

## Common mistakes and troubleshooting

| Mistake | Why it is wrong | Fix |
|---|---|---|
| Reporting only caught poisons | Hides the clean rows lost | Report recall, FPR, precision, and counts |
| Choosing the threshold after seeing the test result | Overfits the evaluation | Pre-register the threshold and show sensitivity |
| Fitting the screen on the training data | The screen learns the poison | Fit on a separate trusted reference set |
| Assuming the reference set is clean | An attacker can target it | State the assumption and test its violation |
| Calling a robust model "poison-proof" | Robustness is budget- and attack-specific | State the budget, attack, and evidence |
| Treating clean accuracy as the only cost | Data removal and latency matter too | Report operational costs |

## Summary and key takeaways

- A reference-set screen flags rows whose labels disagree with trusted local evidence.
- At τ = 0.6, LAB-06 catches all 30 poisons but falsely flags 37 clean rows.
- Recall alone is not enough: at τ = 0.5, 24 of 30 caught still leaves the target flipped.
- Threshold choice trades clean data for assurance; it is a risk decision.
- Screening depends on a clean, representative, untouchable reference set.
- Dense mislabelled clusters are easy to catch; clean-label and spread-out attacks are harder.
- Robust training and certified defenses change the claim, not just the accuracy number.
- A defense evaluation needs an adaptive attacker, false positives, a protected outcome, and stated assumptions.

## Check yourself

1. Why does the screen catch all 30 poisons in LAB-06, and why is that not a general guarantee?
2. At τ = 0.5 the screen catches 80% of poisons but the attack still succeeds. What does that show about defense metrics?
3. What are the four assumptions behind the reference-set screen?
4. How would a clean-label attack change the screen's signal?
5. What does a certified defense promise, and what does it not promise?

## Next step

Module 06 turns poisoning into a **conditional** behavior. In [LAB-07](../../labs/lab-07.md) the poisoned rows carry a trigger, so the model behaves normally on clean inputs and wrongly when the trigger appears. Read [Module 06](../m06-backdoors/index.md) next.
