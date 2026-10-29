# Lesson 07.2 — Model Extraction

<a id="m07-l2"></a>

**1.25 hours · Lesson 2 of 5 · Module 07**

## What this lesson answers

How much of a model can an attacker recover from a limited number of queries? This lesson defines extraction, separates the two metrics that describe it, and walks through the LAB-09 curve — including the budget where active selection loses badly.

## The attack

**Model extraction** (also called model stealing) is training a substitute model from a target model's responses.

The attacker does not copy weights. The attacker collects input–output pairs and fits a function that agrees with the target:

$$
\hat{f} = \arg\min_{g \in \mathcal{G}} \; \frac{1}{n} \sum_{i=1}^{n} \ell\big(g(x_i), f(x_i)\big),
$$

where $f$ is the target, $x_i$ are queries the attacker chooses, $n$ is the query budget, and $\mathcal{G}$ is the attacker's model family. In LAB-09, $f$ is a small neural network, $\mathcal{G}$ is a random forest, and $n \in \{50, 100, 200, 500\}$.

The attacker's model family does not need to match the target's. A random forest can approximate a neural network's decision boundary well enough to be useful, especially on a low-dimensional problem.

## Threat model

| Part | LAB-09 assumption |
|---|---|
| **Goal** | Functionality extraction: a surrogate that behaves like the teacher |
| **Access** | Query access to a local `PredictionAPI` |
| **Output** | Hard labels only |
| **Budget** | 50, 100, 200, or 500 queries, enforced exactly |
| **Knowledge** | Input domain $[-5, 5]^{10}$, five classes, no weights or gradients |
| **Constraint** | No query may exceed the budget |
| **Metric** | Fidelity on 1,500 held-out points; task accuracy on their true labels |
| **Lifecycle** | Serving / business logic |

The attacker in this lab knows the input domain and can sample it uniformly. That is a strong assumption. A real attacker may not know the feature ranges, may not be able to generate valid inputs, and may face preprocessing that rejects out-of-distribution queries. Those constraints make extraction harder, and a report must say so.

## Fidelity and task accuracy are different questions

Two numbers describe a surrogate:

- **Fidelity**: how often the surrogate agrees with the target.

$$
\text{fidelity} = \frac{1}{m}\sum_{j=1}^{m} \mathbf{1}\big[\hat{f}(x_j) = f(x_j)\big].
$$

- **Task accuracy**: how often the surrogate matches the hidden true labels.

$$
\text{accuracy} = \frac{1}{m}\sum_{j=1}^{m} \mathbf{1}\big[\hat{f}(x_j) = y_j\big].
$$

Fidelity measures the copy. Accuracy measures the task. They can differ in both directions:

| Situation | Fidelity | Accuracy | Why |
|---|---|---|---|
| Surrogate copies a weak teacher | High | Low | It reproduces the teacher's mistakes |
| Surrogate is better than the teacher | Lower | Higher | It learned the task, not the teacher |
| Surrogate approximates a strong teacher well | High | High | Both are close to the truth |

LAB-09's teacher is 99.47% accurate, so fidelity is close to accuracy and slightly above it: a surrogate that agrees with the teacher usually agrees with the truth, because the teacher usually does.

The distinction is not academic. A copy with high fidelity can be used to attack the target through transfer, even if the copy is not accurate on the underlying task. A copy with high accuracy but moderate fidelity may be a different, better model — useful, but not evidence that the target was reproduced.

## The LAB-09 procedure

1. Generate five Gaussian clusters in 10 dimensions (2,500 train, 1,500 test).
2. Train the teacher: `MLPClassifier((64, 32), max_iter=1500, random_state=42)`.
3. Wrap it in `PredictionAPI(model, budget)`, which raises if `used + len(X) > budget`, otherwise returns hard labels and increments `used`.
4. **Random baseline:** take the first $b$ points of a shuffled 30,000-point pool, query, and train `RandomForestClassifier(200)`.
5. **Active extraction:** start with 20 random queries. Train a temporary surrogate, compute its predictive entropy on a separate candidate pool, query the 20 most uncertain points, and repeat until the budget is exhausted. Train the final surrogate on all queried points.
6. Measure fidelity and task accuracy on the test set.

Predictive entropy for a $k$-class probability vector $p$ is

$$
H(p) = -\sum_{c=1}^{k} p_c \log p_c.
$$

High entropy means the temporary surrogate is unsure. Querying there is meant to resolve uncertainty near the current decision boundary.

## The result

| Budget | Random fidelity | Random accuracy | Active fidelity | Active accuracy |
|---:|---:|---:|---:|---:|
| 50 | 0.7620 | 0.7600 | **0.4793** | **0.4767** |
| 100 | 0.7013 | 0.7000 | 0.9227 | 0.9227 |
| 200 | 0.6940 | 0.6920 | 0.9280 | 0.9240 |
| 500 | 0.8707 | 0.8693 | 0.9753 | 0.9713 |

Teacher accuracy: 0.9947.

Three things in this table are more important than the numbers themselves.

### 1. Active selection loses at 50 queries

With 20 seed points, the temporary surrogate is barely better than guessing. Its "most uncertain" points are uncertain for the wrong reasons. The attacker spends the remaining 30 queries on a poor region and ends with a worse surrogate (0.4793) than uniform random sampling (0.7620).

This is the **cold start** problem. Active learning assumes a usable current model; at 50 queries, there is not one. The fix is not a bug fix — it is a design choice: increase the seed set, accept a warm-up phase, or fall back to random queries until the surrogate is adequate. Each option spends budget differently.

### 2. By 100 queries, active selection is far ahead

At 100 queries, the seed plus a few entropy batches gives a surrogate whose uncertainty estimates are meaningful. Fidelity jumps to 0.9227, above the random baseline at 500 queries. The gain comes from where the queries are placed, not from more of them.

### 3. The random curve is not monotone

Random fidelity goes 0.7620 → 0.7013 → 0.6940 → 0.8707. More random queries produced a *worse* surrogate at 100 and 200 than at 50. This is not a contradiction: each budget uses a different set of points, and a random forest trained on 100 points can land on a less representative sample than one trained on 50. Single-run curves are noisy. A report should either repeat the experiment across seeds or clearly state that the curve is one draw.

The jump at 500 suggests the larger sample finally covers all five clusters. At 50, the sample may happen to contain a few points from every cluster; at 100–200, it may be unbalanced in a way that hurts the forest. The lesson is not "more queries hurt." It is "one random draw is not a curve."

## What the attacker pays

A query budget is also a cost model. In LAB-09 every query is free, but in a real system each one has a price:

| Cost | Example | Effect on the attack |
|---|---|---|
| Money | \$0.001 per call | 10,000 queries cost \$10 |
| Time | 60 queries/minute | 10,000 queries take about 2.8 hours |
| Accounts | 1,000 queries/account/day | 10 accounts for 10,000 queries in a day |
| Detection | Anomaly alerts on query patterns | The attacker must look like normal traffic |
| Legal | Terms of service, authorization | The attack may be prohibited regardless of feasibility |

A feasibility statement should include the budget, the cost, and the detection risk. "Extraction is possible" without those is not a risk assessment.

## Defenses and their limits

| Defense | How it works | Cost | Residual risk |
|---|---|---|---|
| **Rate limiting** | Cap queries per account or IP | Legitimate heavy users are slowed | Account farms; slow extraction |
| **Quotas and pricing** | Charge per query | Revenue and accessibility | The attacker pays; the economics may still work |
| **Output rounding** | Return coarse probabilities or labels only | Less useful explanations and diagnostics | Label-only extraction remains |
| **Top-k or abstain** | Return fewer classes or refuse low-confidence inputs | Reduced utility | Repeated queries can recover the ranking |
| **Query monitoring** | Detect grids, uniform sampling, entropy-like patterns | False positives; privacy of logs | Adaptive attackers imitate normal traffic |
| **Watermarking** | Embed detectable behavior in the model | Slight accuracy cost; watermark can be removed | Supports ownership claims, not prevention |
| **Fingerprinting** | Query with canary inputs and look for the response in a suspect copy | Requires the suspect model | Only detects copies that preserve the canaries |

No interface defense makes extraction impossible when the function is valuable and queries are allowed. The realistic goal is to raise the attacker's cost, shrink the information per query, and make the attack detectable.

## What high fidelity does not prove

- **It does not prove the weights were stolen.** The surrogate is a different model trained on outputs.
- **It does not prove the training data was stolen.** The attacker saw only queries.
- **It does not prove task equivalence.** High agreement on the test distribution can hide disagreement off-distribution.
- **It does not prove the copy is harmless.** Even a moderate-fidelity copy can generate transferable adversarial examples.
- **It does not generalize to other budgets or access models.** A curve at 500 queries says nothing about a label-only API with a quota of 10 per day.

## A note on the input distribution

LAB-09 samples queries uniformly from $[-5, 5]^{10}$. The true data lies in five Gaussian clusters inside that box. Uniform sampling therefore spends many queries in empty regions. Active selection partially corrects this by focusing near the surrogate's boundary, but the attacker could do better by knowing or estimating the data distribution.

This is an assumption, not a detail. Extraction difficulty depends on:

- the input dimension (higher is harder),
- the number of classes,
- how smooth the target's boundary is,
- whether the attacker can generate in-distribution inputs,
- whether the target returns probabilities,
- and how much the target's behavior varies across the input space.

A result on a 10-dimensional synthetic problem is a demonstration of the method, not an estimate for an image or language model.

## Common mistakes

| Mistake | Symptom | Correction |
|---|---|---|
| Reporting fidelity as accuracy | "The copy is 92% accurate" from a fidelity number | Label each metric and compute both |
| Omitting the random baseline | Active looks good at every budget | Always plot the random curve |
| Treating one run as a trend | "More queries sometimes hurt" from one draw | Repeat across seeds or state the limitation |
| Ignoring the cold start | "Active learning is better" | Report the budget where it fails |
| Forgetting the query cost | "Anyone can do this" | Add money, time, accounts, detection |
| Comparing to the teacher's training accuracy | 0.99 target looks unreachable | Compare to the teacher's test accuracy |
| Claiming IP theft from fidelity | "The model was stolen" | Say "a surrogate with fidelity $x$ was trained" |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `RuntimeError: query budget exceeded` | Querying before reserving | Check `used + len(X) <= budget` |
| Fidelity equals task accuracy exactly | Using true labels for both | Fidelity compares to `teacher.predict` |
| Active fidelity never improves | Selecting lowest entropy | Sort descending by entropy |
| Active loses at every budget | Seed set too small | Increase `INITIAL_RANDOM` and report the trade-off |
| Curve differs from the reference | Different pool shuffle or forest seed | Use the documented RNG order |
| Surrogate predicts one class | Too few queries or unbalanced pool | Check class coverage at small budgets |

## What you should be able to do now

- Define extraction, fidelity, and task accuracy, and compute all three from a result table.
- Explain why active selection fails at 50 queries and why the random curve is non-monotone.
- State the query cost and the access assumptions behind an extraction claim.
- Evaluate a defense by its cost and residual risk, not by its existence.

## Summary

Extraction turns query answers into a surrogate. Fidelity measures agreement with the target; task accuracy measures agreement with the truth. LAB-09 shows that 500 queries can produce a high-fidelity copy on a small synthetic problem, that active selection can beat random by a wide margin once it has enough seed data, and that it can lose badly before then. The lab is a demonstration under a specific access model, not a measurement of any deployed service.

## Next step

[Lesson 07.3 — Membership inference](lesson-3-membership-inference.md) asks a different question about the same interface: not what the model does, but what it remembers.
