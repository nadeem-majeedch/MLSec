# Lesson 12.3 — Aggregation and Its Limits

<a id="m12-l3"></a>

**Module 12 · Lesson 3 of 5 · 2 hours · LO-24**

## Scenario

After the poisoning incident, the consortium's security team asks for "a Byzantine-robust aggregator." Three options are on the table: a trimmed mean, a coordinate-wise median, and Krum. Each has a paper with a theorem. The team wants to know which one to deploy.

The honest answer is that the theorem is not the deployment. Each rule assumes something about the number of attackers, the distribution of benign updates, or the geometry of the update space. The right question is which assumptions the deployment can satisfy, and what happens when they fail.

This lesson compares the rules, works through the same small example, and connects the comparison to LAB-16.

## Objectives

By the end of this lesson you will be able to:

1. Define mean, coordinate-wise trimmed mean, coordinate-wise median, and Krum.
2. Compute each rule on a small example and explain the differences.
3. State each rule's assumptions, breakdown behavior, and computational cost.
4. Explain why a coordinate-wise rule can produce a poor model even when it resists an outlier.
5. Connect LAB-16's trimmed-mean result to the assumptions it satisfies.
6. Choose a rule for a stated threat model and justify the residual risk.

## 1. The setup

The server receives \(K\) updates \(\Delta_1,\dots,\Delta_K\), each a vector in \(\mathbb{R}^d\). An aggregation rule is a function

\[
A(\Delta_1,\dots,\Delta_K) \in \mathbb{R}^d.
\]

FedAvg uses the weighted mean. Robust rules replace the mean with a statistic that is less sensitive to a minority of extreme values. All of them operate on the same inputs; the difference is what they assume about the majority.

Let \(m\) be the number of Byzantine updates the rule is designed to tolerate. The ratio \(m/K\) is the adversary fraction. A rule's guarantee is usually stated for \(m\) below a threshold, and it says nothing about \(m\) above it.

## 2. Mean

\[
A_{\text{mean}} = \frac{1}{K}\sum_{k=1}^{K}\Delta_k.
\]

The mean has breakdown point 0: a single update can move it arbitrarily far. That is not a bug in the arithmetic; it is the definition of an average. LAB-16 uses this property when one client scales by 6.

The mean is also the most statistically efficient rule when every update is honest and identically distributed. Robustness and efficiency trade against each other. A rule that ignores extremes also ignores legitimate heterogeneity.

## 3. Trimmed mean

For each coordinate \(j\), sort the \(K\) values and remove the \(m\) smallest and \(m\) largest. Average the remaining \(K-2m\) values:

\[
A_{\text{trim},j} = \frac{1}{K-2m}\sum_{i=m+1}^{K-m}\Delta_{(i),j}.
\]

The rule requires \(2m < K\). It tolerates up to \(m\) extreme values on each side of each coordinate. If all attackers push in the same direction, \(m\) attackers can be trimmed; if they split across both tails, the effective tolerance changes.

**Assumption.** The benign values for each coordinate form a majority that is not itself extreme. Under strong non-IID data, benign updates can legitimately occupy both tails, and trimming removes signal rather than attack.

**Cost.** Sorting \(K\) values per coordinate is \(O(K\log K)\) per coordinate, or \(O(dK\log K)\) per round. For a large model, \(d\) is in the millions; the sort is the expensive part.

**Output.** A coordinate-wise statistic that need not equal any client's update. That is acceptable for a model update but complicates debugging: the aggregate may not correspond to a real participant.

### Worked example

Five scalar updates: \(0.10,\ 0.15,\ 0.20,\ 0.90,\ 5.00\). With \(m=1\):

- mean: \((0.10+0.15+0.20+0.90+5.00)/5 = 1.27\);
- trimmed mean: remove 0.10 and 5.00, average \(0.15,0.20,0.90\) = \(0.4167\);
- median: \(0.20\).

The attacker's 5.00 moves the mean by more than a unit. The trimmed mean and median are unmoved by the extreme value, but they also differ from each other by a factor of two. Robustness does not imply agreement.

## 4. Coordinate-wise median

For each coordinate, take the median across clients:

\[
A_{\text{med},j} = \operatorname{median}(\Delta_{1,j},\dots,\Delta_{K,j}).
\]

The median has a breakdown point of 50% per coordinate: fewer than half the values must be corrupted for the median to remain bounded. That sounds strong, and in one dimension it is.

In high dimensions, the guarantee is weaker than it looks. The coordinate-wise median is not the geometric median. An attacker can spread perturbations across coordinates so that each coordinate median moves a little, and the resulting vector can be far from every benign update. The rule also ignores correlations between coordinates: a model update that is plausible as a whole can be rejected coordinate by coordinate, and an implausible combination can be constructed.

**Assumption.** A majority of clients are honest in each coordinate, and the coordinate-wise summary is an acceptable model direction. The second assumption is the fragile one for neural networks.

**Cost.** Selecting a median per coordinate is \(O(dK)\) with a linear-time selection algorithm, cheaper than sorting.

## 5. Krum

Krum selects one update rather than averaging. For each update \(i\), compute the sum of squared distances to its \(K-m-2\) nearest neighbors:

\[
\operatorname{score}(i) = \sum_{j \in N_i} \|\Delta_i - \Delta_j\|^2,
\]

where \(N_i\) is the set of the \(K-m-2\) closest other updates. Select the update with the smallest score. The rule requires \(K \ge 2m+3\).

The intuition is that a Byzantine update is far from the benign cluster, so it has a large distance to its nearest neighbors. Selecting the most central update avoids averaging in the outlier. Multi-Krum averages the top-scoring updates instead of selecting one.

**Assumption.** Benign updates cluster in Euclidean space and the attacker cannot make its update close to the benign cluster while remaining malicious. Fang et al. show that an attacker who knows the rule can optimize against this assumption.

**Cost.** Computing all pairwise distances is \(O(K^2d)\), and selecting neighbors adds a sort per client. For large \(K\) and \(d\), this is expensive.

**Output.** One client's update, or an average of a few. The selected update may be an outlier in a direction the distance metric does not capture.

### Worked example, continued

Five scalar updates, \(m=1\), so \(K-m-2=2\) neighbors per client. Approximate scores:

| Update | Two nearest | Score |
|---|---|---:|
| 0.10 | 0.15, 0.20 | \(0.0025+0.0100=0.0125\) |
| 0.15 | 0.10, 0.20 | \(0.0025+0.0025=0.0050\) |
| 0.20 | 0.15, 0.10 | \(0.0025+0.0100=0.0125\) |
| 0.90 | 0.20, 0.15 | \(0.4900+0.5625=1.0525\) |
| 5.00 | 0.90, 0.20 | \(16.81+23.04=39.85\) |

Krum selects 0.15, the most central update. Here it agrees with the trimmed mean's neighborhood but not with its value. On a real model, the selected update is a full weight vector, not a scalar, and the geometry is much less intuitive.

## 6. Comparison

| Rule | Statistic | Adversary assumption | Breakdown intuition | Cost | Main failure |
|---|---|---|---|---|---|
| Mean | Average | None | 0 | \(O(Kd)\) | One update moves it |
| Trimmed mean | Coordinate mean after trimming | Minority on each tail, benign majority | \(m/K\) per tail | \(O(dK\log K)\) | Non-IID benign extremes removed |
| Coordinate median | Per-coordinate median | Majority per coordinate | 50% per coordinate | \(O(dK)\) | Ignores geometry and correlation |
| Krum | Select central update | Benign cluster, attacker far | Roughly \(m < K/2\) | \(O(K^2d)\) | Adaptive attacker mimics cluster |
| Multi-Krum | Average top updates | Same as Krum | Same as Krum | \(O(K^2d)\) | Same as Krum, plus averaging |

No rule dominates. The mean is best when clients are honest and heterogeneous. The median is cheap and robust in low dimensions. The trimmed mean is a compromise that depends on the tail structure. Krum is principled but expensive and assumes a geometry the attacker can study.

## 7. LAB-16's result in context

LAB-16 uses eight clients and one attacker. With \(m=1\), the trimmed mean removes one value from each tail of each coordinate. The attacker is the only extreme value in the coordinates it moves, so the rule removes it. The result is ASR 0.0000 and clean accuracy 0.8704.

What the result establishes:

- For this attacker, this fraction, this update geometry, and this trim count, the rule removed the backdoor.
- The clean model still trains: 0.8704 is close to the benign 0.9000.
- A robust rule can be evaluated with the same clean/ASR protocol as the mean.

What it does not establish:

- That the rule tolerates two colluding clients. With \(m=1\), two aligned outliers can survive.
- That it tolerates an attacker that stays inside the benign coordinate range.
- That it preserves accuracy under stronger non-IID heterogeneity.
- That it works for a neural network with millions of coordinates and correlated weights.

The lab's report states these limits. A defense claim without them is incomplete.

## 8. Adaptive attackers

An adaptive attacker knows the rule and chooses an update that is both malicious and acceptable. Against a trimmed mean, it can keep each coordinate inside the benign range while shifting the joint direction. Against Krum, it can move toward the benign cluster while retaining a backdoor in a subspace the distance metric underweights. Against a median, it can distribute a small shift across many coordinates.

Fang et al. formalize this for several robust rules and show that a crafted local model can defeat them. The defensive implication is not "abandon robust aggregation." It is that the rule is one layer, and the evaluation must include an attacker who knows it.

## 9. Choosing a rule

| Question | If yes | If no |
|---|---|---|
| Is the adversary fraction known and below the rule's threshold? | A robust rule can be considered | Do not rely on the guarantee |
| Are benign updates approximately clustered? | Krum or trimmed mean is plausible | The mean may be more appropriate |
| Is \(d\) large and compute constrained? | Coordinate median or clipping | Krum may be too expensive |
| Is strong non-IID heterogeneity expected? | Test trimming's accuracy cost | The mean is efficient |
| Can the attacker adapt to the rule? | Add monitoring and diversity | A fixed rule is a starting point |
| Is the evaluation trigger-aware? | The ASR result is meaningful | Clean accuracy can hide a backdoor |

The answer is a risk decision, not a lookup. Record the assumptions, the measured result, and the residual risk.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Quoting a robustness theorem without its assumptions | The theorem is the headline | State \(m\), \(K\), and the geometry assumption |
| Comparing rules at different rounds | Each run evolved | Freeze rounds, clients, and local epochs |
| Reporting only ASR | The defense looks strong | Report clean accuracy and ASR |
| Assuming median equals geometric median | The names are similar | Distinguish coordinate-wise from geometric |
| Using Krum with \(K < 2m+3\) | The condition is easy to miss | Check the inequality before running |
| Ignoring non-IID accuracy cost | The attack is the focus | Measure benign accuracy under the rule |
| Testing only a naive attacker | The lab attacker is simple | Add an attacker that knows the rule |
| Calling a rule "secure" | It resisted one attack | Report the tested attacker and residual risk |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Trimmed mean errors | \(2m \ge K\) | Reduce \(m\) or add clients |
| Krum selects the attacker | Attacker is close to the benign cluster | Inspect distances; test an adaptive attacker |
| Median model does not train | Coordinate-wise median of very different updates | Check non-IID severity and consider the mean |
| Robust rule has low ASR but low accuracy | The rule removed legitimate signal too | Report the accuracy cost and tune \(m\) |
| Results vary across runs | Unseeded client order or data | Fix the seed and client ordering |
| Rule is too slow | Krum's pairwise distances | Reduce \(K\), use Multi-Krum, or choose a cheaper rule |

## Check your understanding

1. Compute the mean, 1-trimmed mean, and median of \(0.1, 0.2, 0.3, 0.4, 10.0\).
2. Why does the coordinate-wise median have a 50% breakdown per coordinate but a weaker guarantee in high dimensions?
3. What does Krum select, and why is its output not an average?
4. State the condition on \(K\) and \(m\) for Krum.
5. LAB-16's trimmed mean achieves ASR 0.0000. Name two changes that could make it fail.
6. Why is an adaptive attacker a stronger test than LAB-16's scaled update?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Aggregation rules differ in what they assume and what they cost.
- The mean has breakdown point 0; one update can move it.
- Trimmed mean removes tail values per coordinate and assumes a benign majority.
- Coordinate median is cheap and robust per coordinate but ignores geometry.
- Krum selects a central update and assumes the attacker is far from the benign cluster.
- LAB-16's trimmed mean removes one outlier; that is evidence for one configuration, not a universal guarantee.
- Adaptive attackers target the rule's assumptions. Use the rule as one layer and evaluate with a trigger-aware protocol.

## Next

Continue to [Lesson 12.4 — Client validation, monitoring, and privacy](lesson-4-validation-monitoring-and-privacy.md), where aggregation is combined with identity, inspection, and privacy controls.
