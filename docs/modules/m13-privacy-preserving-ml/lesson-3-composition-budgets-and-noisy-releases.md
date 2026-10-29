# Lesson 13.3 — Composition, Budgets, and Noisy Releases

<a id="m13-l3"></a>

**Module 13 · Lesson 3 of 5 · 2 hours · LO-19**

## Scenario

A health ministry approves a dashboard with a privacy budget of \(\varepsilon = 1.0\) per year. The team ships a monthly release at \(\varepsilon = 0.1\), then adds a quarterly model retrain at \(\varepsilon = 0.5\), then a "small" ad hoc query at \(\varepsilon = 0.02\). By October the ledger is over budget, and nobody noticed because each release was approved on its own.

This lesson is about the ledger. Composition is the rule that turns individual releases into a cumulative guarantee; budget accounting is the discipline that keeps the total within policy.

## Objectives

By the end of this lesson you will be able to:

1. Apply basic sequential composition and explain when it is conservative.
2. Apply parallel composition and state its disjointness condition.
3. Build a budget ledger for multiple releases on the same population.
4. Allocate a total budget across releases and stop when it is exhausted.
5. Design a noisy release with correct sensitivity, scale, and post-processing.
6. Explain why a hyperparameter sweep is not free in a real deployment.

## 1. Sequential composition

If mechanisms \(M_1,\dots,M_T\) each satisfy \(\varepsilon_t\)-DP and are applied to the same dataset, their joint release satisfies

\[
\varepsilon_{\text{total}} = \sum_{t=1}^{T} \varepsilon_t
\]

under basic sequential composition (with \(\delta\) summing similarly).

This is the simplest and most conservative rule. It makes no assumption about the mechanisms beyond their individual guarantees. It is also the easiest to audit: add the numbers.

### Worked example

Twelve monthly releases, each \(\varepsilon = 0.1\):

\[
\varepsilon_{\text{total}} = 12 \times 0.1 = 1.2.
\]

If the annual policy is 1.0, the twelfth release exceeds it. The team must reduce the monthly epsilon, skip a release, or renegotiate the policy. Approving each release at 0.1 without a ledger hides this.

Advanced composition can give tighter bounds when many mechanisms have small epsilon and a small \(\delta'\) is allowed. The exact bound depends on the mechanism family and the accounting method (advanced composition, Rényi DP, or zero-concentrated DP). The engineering point is not to memorize one formula; it is to use an accounting method that matches the mechanism and to record which one was used.

## 2. Parallel composition

If mechanisms operate on **disjoint** subsets of the data, the joint release satisfies

\[
\varepsilon_{\text{total}} = \max_t \varepsilon_t
\]

rather than the sum. Each person is affected by at most one mechanism, so the risks do not add across subsets.

| Setting | Composition | Total epsilon |
|---|---|---|
| Two class datasets, disjoint rows, each released at 0.5 | Parallel | 0.5 |
| Two queries on the same rows, each 0.5 | Sequential | 1.0 |
| Monthly releases on the same population, each 0.1 | Sequential | 1.2 after 12 |
| Monthly releases on disjoint regional populations, each 0.1 | Parallel across regions | 0.1 per region |

The disjointness condition is strict. If a person can appear in both subsets, the release is not parallel. Overlapping cohorts, deduplicated populations, and "mostly disjoint" data all require sequential accounting unless the overlap is bounded and analyzed.

LAB-17's two class datasets are disjoint and fixed-size, so the two centroid releases use parallel composition. The total epsilon equals the per-class epsilon. If the same rows had been used for both centroids, the total would double.

## 3. A budget ledger

A ledger records every release, its data, its mechanism, its parameters, and its composition type.

| # | Release | Population | Mechanism | \(\varepsilon\) | \(\delta\) | Composition | Cumulative \(\varepsilon\) |
|---|---|---|---|---:|---:|---|---:|
| 1 | Q1 readmission counts | All patients | Laplace | 0.20 | 0 | Sequential | 0.20 |
| 2 | Q2 readmission counts | All patients | Laplace | 0.20 | 0 | Sequential | 0.40 |
| 3 | Model retrain | All patients | DP-SGD | 0.50 | \(10^{-6}\) | Sequential | 0.90 |
| 4 | Dashboard refresh | All patients | Laplace | 0.10 | 0 | Sequential | 1.00 |
| 5 | Q3 counts | All patients | Laplace | 0.10 | 0 | **Over budget** | 1.10 |

The fifth row is the decision point. The release is technically possible; it is not authorized by the policy. The ledger makes the conflict visible before the release, not after an audit.

### Ledger fields

| Field | Why it matters |
|---|---|
| Release id and owner | Accountability |
| Data population and unit | Determines composition and adjacency |
| Mechanism and sensitivity | Reproducibility of the guarantee |
| \(\varepsilon\), \(\delta\) | The claimed parameters |
| Composition type and justification | Prevents accidental parallel claims |
| Cumulative total | The number compared with policy |
| Approval and date | Governance evidence |
| Residual notes | What the guarantee does not cover |

A ledger is only useful if it is updated before release. A spreadsheet filled in at year-end is a reconstruction, not a control.

## 4. Allocating a budget

There is no universal allocation. The decision depends on which releases matter and how much utility each needs.

| Strategy | Idea | Risk |
|---|---|---|
| Equal split | Divide the total by the number of releases | A high-value release may be underfunded |
| Priority split | Give more to high-value releases | Low-value releases may still leak in aggregate |
| Adaptive | Choose the next epsilon based on results | Adaptivity must be accounted for; it is not free |
| Reserved | Hold back budget for incidents and ad hoc queries | Unused budget is not a failure |
| Per-release cap | Limit any single release | Total can still exceed policy without a ledger |

A reserved budget is a practical control. It gives the team room to answer a regulator or investigate an incident without violating the annual total.

### Adaptivity

If you run five epsilon values, look at the utility, and then choose one to deploy, the choice used the data. In a real deployment, that selection is part of the mechanism and must be accounted for. The clean approach is to fix the epsilon before seeing the private results, or to use a private selection mechanism with its own budget.

LAB-17's epsilon sweep is an experiment on **synthetic** data, so there is no privacy cost. Do not copy the sweep-and-choose pattern into a real release without accounting for the selection.

## 5. Designing the noisy release

A release design has six steps.

1. **Define the query.** What statistic, over which rows, with which unit?
2. **Choose adjacency.** Add/remove or replace-one; fixed or variable \(n\).
3. **Bound the range.** Clip values so sensitivity is finite.
4. **Compute sensitivity.** Use the L1 or L2 norm as required by the mechanism.
5. **Choose the mechanism and parameters.** Laplace for pure DP; Gaussian for approximate DP.
6. **Post-process and document.** Rounding, clamping, suppression, and visualization must use only the noisy output.

### Worked release

A count of positive cases in a cell, with add/remove adjacency:

- sensitivity \(\Delta_1 = 1\);
- target \(\varepsilon = 0.25\);
- Laplace scale \(b = 1/0.25 = 4\);
- released value \(= \text{count} + \text{Laplace}(0,4)\).

A count of 3 can be released as 0 or 9. Rounding to the nearest integer and clamping at 0 are post-processing and remain DP. Clamping changes the distribution and can bias small counts upward, but it does not invalidate the guarantee.

### Small counts

Small counts are where utility and privacy collide. A cell with one person cannot be released accurately without revealing that person under most threat models. Options:

- suppress the cell (but suppression itself can leak, and totals must be consistent);
- release a noisy count and accept that it may be 0 or 4;
- aggregate cells into a larger group;
- use a threshold with a noisy count and a DP-aware suppression rule.

Each option is a policy choice. The ledger should record it.

## 6. LAB-17's composition

LAB-17 runs five epsilon values as separate experimental configurations. Each configuration releases two centroids from disjoint class datasets.

| Epsilon | Laplace scale | Total epsilon for the release |
|---:|---:|---:|
| 0.02 | 2.400 | 0.02 |
| 0.10 | 0.480 | 0.10 |
| 0.50 | 0.096 | 0.50 |
| 1.00 | 0.048 | 1.00 |
| 4.00 | 0.012 | 4.00 |

The total is the per-class epsilon because of parallel composition. The sweep is not five releases of one deployment; it is five independent experiments on synthetic data. A real deployment would choose one epsilon before release and record it in the ledger.

The lab's `run.json` records `total_epsilon_equals_class_epsilon: true`, and the checker verifies the composition claim. That is the kind of evidence an auditor needs: not just the number, but why the number is the total.

## 7. Budget exhaustion

When the budget is exhausted:

1. **Stop new releases** on that population.
2. **Do not quietly reset** the ledger at a fiscal boundary unless the policy defines the boundary and the population.
3. **Consider a disjoint population** if the new release genuinely uses different people; document the disjointness.
4. **Re-negotiate the policy** with the owner, recording the residual risk.
5. **Prefer post-processing** of already released outputs over new queries.

A budget is not a suggestion. The guarantee is only as good as the accounting behind it.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Summing epsilon for disjoint releases | Sequential is the default mental model | Check disjointness; use max for parallel |
| Using max for overlapping releases | Parallel is more convenient | Use sum when a person can appear in both |
| Ignoring the model retrain | It is "training," not "release" | Training on the same data spends budget |
| Resetting the ledger annually without policy | The fiscal year is convenient | Define the population and period in policy |
| Choosing epsilon after seeing utility | The sweep is exploratory | Account for selection or fix epsilon in advance |
| Clipping after aggregation | The code is simpler | Clip rows before the query |
| Suppressing small cells without accounting | Suppression feels safe | Use a DP-aware threshold and record it |
| Reporting per-release epsilon only | The dashboard looks compliant | Report the cumulative total |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Total epsilon seems too small | Parallel used for overlapping data | Verify disjointness |
| Total epsilon seems too large | Sequential used for disjoint regional data | Split the ledger by population |
| Utility collapses after adding releases | Budget split too thinly | Reallocate or reduce the number of releases |
| Release is negative | Laplace noise on a small count | Clamp as post-processing; document the bias |
| Selection changed the result | Epsilon chosen after seeing outputs | Treat selection as part of the mechanism |
| Auditor cannot reproduce the total | Composition or sensitivity missing | Fill every ledger field |

## Check your understanding

1. Ten releases on the same data, each \(\varepsilon = 0.08\). What is the basic sequential total?
2. Two releases on disjoint populations, each \(\varepsilon = 0.4\). What is the parallel total?
3. Why is parallel composition invalid for overlapping cohorts?
4. A count query has sensitivity 1 and target \(\varepsilon = 0.2\). What is the Laplace scale?
5. Why is choosing epsilon after a utility sweep a privacy issue in a real deployment?
6. What should happen when a release would exceed the policy budget?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Sequential composition adds epsilon; parallel composition takes the max for disjoint data.
- Disjointness is a strict condition, not an approximation.
- A budget ledger records every release, its mechanism, its parameters, and the cumulative total.
- Allocate a total budget, reserve some for incidents, and stop when it is exhausted.
- Clipping, sensitivity, mechanism, and post-processing form one chain; a break invalidates the claim.
- LAB-17's class datasets are disjoint, so the total epsilon equals the per-class epsilon.
- The epsilon sweep is an experiment on synthetic data, not a template for unaccounted selection.

## Next

Continue to [Lesson 13.4 — Private training and secure computation](lesson-4-private-training-and-secure-computation.md), where the release is a trained model rather than a statistic.
