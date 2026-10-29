# Lesson 14.4 — Security Trade-offs and Audit Reporting

<a id="m14-l4"></a>

**Module 14 · Lesson 4 of 4 · 1 hour · LO-31, LO-32, LO-28**

## Scenario

A model review has four slides: accuracy, a fairness gap, an explanation-stability chart, and a privacy note. Each slide is green. The committee asks one question: "What did we give up to get here?" Nobody can answer, because each metric was optimized and reported separately, and no one recorded the baseline or the interval.

This lesson turns the measurements from Lessons 1–3 into a decision record: what changed, at what cost, with what uncertainty, and what remains unverified.

## Objectives

By the end of this lesson you will be able to:

1. Describe the main trade-offs among accuracy, subgroup outcomes, explanation stability, privacy, and robustness.
2. Read a trade-off as a constrained decision rather than a single score.
3. Quantify the LAB-18 intervention's costs and benefits, including uncertainty.
4. Write a scoped audit statement with a decision, an owner, and a review date.
5. State residual risks that the measurements do not cover.

## 1. The trade-off map

| Intervention | Usually improves | Usually costs | Can worsen |
|---|---|---|---|
| Group reweighting | One fairness gap | Overall accuracy | Another fairness gap |
| Threshold adjustment per group | Selection-rate parity | Calibration or accuracy | Legal defensibility if untested |
| Adversarial training | Robustness to a perturbation family | Clean accuracy, training time | Explanation stability or fidelity |
| DP training | Formal privacy | Utility, especially small groups | Subgroup gaps through noise |
| Explanation coarsening | Leakage resistance | Fidelity and contestability | User trust if reasons seem arbitrary |
| More explanation detail | Accountability | Extraction and inversion risk | Manipulation surface |
| More monitoring | Detection | Privacy of logs, cost | False positives and alert fatigue |
| More training data | Accuracy, subgroup coverage | Privacy exposure, cost | Disparity if the new data is skewed |

The entries are tendencies, not laws. The point of an evaluation is to measure the direction and size in the actual system.

### Why a single score fails

A weighted composite ("fairness score 0.82") hides the policy choice in the weights. Two reviewers with different priorities will disagree about the weights, and neither can audit the result. A constrained decision is more honest:

> Accuracy must be at least 0.73; the equalized-odds gap must be below 0.10; explanation stability must be at least 0.85 Spearman; no subgroup may have fewer than 100 evaluation rows. Among configurations that meet these, choose the one with the lowest cost.

The constraints are visible and can be debated. The choice inside the feasible set is a judgment, recorded as such.

## 2. Reading LAB-18 as a trade-off

LAB-18 compares two configurations on the same split. The measured differences:

| Quantity | Baseline | Reweighted | Change |
|---|---:|---:|---:|
| Overall accuracy | 0.7528 | 0.7389 | −0.0139 |
| Demographic-parity gap | 0.0013 | 0.0125 | +0.0112 |
| Equalized-odds gap | 0.1231 | 0.0930 | −0.0301 |
| Mean Spearman, gradient×input | 0.8979 | 0.9010 | +0.0031 |
| Top-feature flip rate, gradient×input | 0.1480 | 0.1497 | +0.0017 |

What the table supports:

- On this test set, reweighting reduced the equalized-odds gap by about 24% relative to the baseline.
- The reduction came from the FPR component; the TPR gap was unchanged at 0.0349.
- The demographic-parity gap increased, from 0.0013 to 0.0125.
- Accuracy fell by 1.39 percentage points.
- Explanation stability was essentially unchanged: Spearman moved by 0.0031 and the flip rate by 0.0017.

What it does not support:

- that the population gaps changed — the bootstrap intervals overlap;
- that the accuracy drop is acceptable — no utility floor was stated;
- that one configuration is better — "better" depends on which gap the policy prioritizes;
- that stability is adequate — no threshold was pre-registered;
- that either model is fair, private, or robust — none of those were fully measured.

### The decision

Suppose the policy is: equalized odds is the priority, accuracy must stay above 0.73, and the evaluation is a screening study, not a deployment gate.

Then the reweighted model meets the accuracy floor (0.7389 > 0.73) and lowers the prioritized gap. The decision record should say so, and should also say that the interval is wide and the DP gap rose. If the policy instead prioritizes demographic parity, the baseline is the better fit, and the EOd gap is the cost.

Neither choice is "the fair one." The record makes the choice auditable.

## 3. Fairness interventions and their costs

### Reweighting

Assigns each group total weight \(1/2\) (or another target), changing the fitted coefficients. It is simple and model-agnostic within a training API. Costs: accuracy can fall; the effect on each gap is not guaranteed; the weights depend on group labels, which may be missing or unreliable.

### Threshold adjustment

Choose a separate decision threshold per group to equalize a rate. It can hit a target precisely on the evaluation set. Costs: it can break calibration, it may be legally contested, and it does not change the underlying score's ranking. It also makes the group membership operationally necessary at decision time.

### Constrained optimization

Add a fairness penalty to the training objective. It can trade accuracy for a gap smoothly. Costs: the penalty weight is a hyperparameter, the optimization may be unstable, and the resulting model can satisfy the constraint on training data while failing on subgroups not represented.

### Post-processing

Adjust predictions after training using a held-out set. It is flexible and can target a specific criterion. Costs: it needs a reliable calibration set, can reduce accuracy, and may be fragile under distribution shift.

No intervention removes the need to measure. Each one moves a metric; the report must say which one and by how much.

## 4. Stability, robustness, and manipulation

Lesson 14.1 distinguished stability from fidelity. Lesson 14.2 showed that stability under random noise does not imply resistance to an optimizer.

| Claim | Evidence needed | LAB-18 status |
|---|---|---|
| Explanations are reproducible under small noise | Spearman and top-\(k\) overlap at a stated noise level | Measured: about 0.90 and 0.86 |
| Explanations are faithful | Deletion or insertion test, sanity check | Not measured |
| Explanations resist targeted manipulation | Optimization-based attack with a success criterion | Not measured |
| The model is robust | Adversarial accuracy against a stated threat model | Not measured |

A stability chart is not a robustness certificate. It is a measurement of one perturbation family. An attacker who optimizes against the explanation method is outside that family.

### The interaction with robustness training

Adversarial training changes the model's gradients, which changes gradient-based explanations. A model can become more robust and have less stable or less faithful explanations, or the reverse. Neither direction is guaranteed. If explanations are part of the product, stability and fidelity belong in the robustness evaluation, not in a separate appendix.

## 5. Privacy and subgroup outcomes

Differential privacy adds noise. The noise is calibrated to a global sensitivity, not to each group's sample size. Consequences:

- **Small groups can be hit harder.** A group with few rows contributes less to a statistic, so the same noise can swamp its signal. Utility loss can be uneven even when the privacy guarantee is uniform.
- **Fairness metrics become noisier.** A gap computed from noisy counts has a wider interval. Reporting a point estimate without the interval is worse under DP than without it.
- **Membership risk and group membership interact.** A record that is unusual within a small group may be easier to infer; DP bounds the influence of any one record, but the bound is on the mechanism, not on every downstream disparity.

These are hypotheses to measure per system. "DP is fair" and "DP is unfair" are both overclaims. The evaluation should report subgroup utility and subgroup intervals alongside the privacy budget.

## 6. The audit report

A report that supports a decision has eight parts.

```text
1. Scope
   System, version, decision, population, time period, and what is out of scope.

2. Data and groups
   Source, size, split, group definitions, counts per group, known label issues.

3. Configurations
   Baseline and each intervention, with hyperparameters and selection procedure.

4. Metrics
   Definitions, thresholds, and why each was chosen. State the policy priority.

5. Results
   Point estimates with intervals, per group and overall. Include utility cost.

6. Trade-offs
   What improved, what worsened, and the size of each change.

7. Residual risks
   Untested attacks, missing groups, calibration gaps, distribution shift,
   explanation fidelity, privacy claims not covered.

8. Decision and review
   Chosen configuration, owner, approval, monitoring plan, review date.
```

The report should be readable by someone who did not run the code. Every number should be reproducible from the artifact.

### A scoped statement

Using LAB-18's numbers:

> On a synthetic test set of 360 rows (214 in group 0, 146 in group 1), a group-reweighted logistic model reduced the equalized-odds gap from 0.1231 to 0.0930 (bootstrap 95% interval 0.0254–0.2190), increased the demographic-parity gap from 0.0013 to 0.0125 (0.0015–0.1230), and reduced accuracy from 0.7528 to 0.7389. Explanation stability under Gaussian noise at \(\sigma = 0.25\) was approximately 0.90 Spearman for both models. The intervals overlap; this study does not establish a population-level improvement. Calibration, targeted explanation manipulation, robustness, and privacy were not evaluated. The result applies to this synthetic distribution and this model family only.

This is longer than "the reweighted model is fairer." It is also the kind of statement a reviewer can check and a decision-maker can use.

## 7. What to do when the evidence is ambiguous

Ambiguity is the normal case. A practical sequence:

1. **Do not force a winner.** Report the interval and the direction.
2. **Revisit the evaluation size.** If the decision hinges on a gap whose interval spans zero, the study is underpowered for that decision.
3. **Separate the policy question from the measurement.** The measurement says what happened; the policy says what matters.
4. **Choose a reversible step.** Pilot the configuration with monitoring, rather than declaring a permanent change.
5. **Record the residual.** "We do not know whether the population gap changed" is a finding.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Optimizing one metric and reporting another | The dashboard has one number | Report the full trade-off |
| Treating a point estimate as a decision | The direction looks clear | Add intervals and a decision rule |
| Calling a stability result robustness | Both involve perturbation | State the perturbation family and the attack model |
| Assuming DP helps small groups | Privacy is uniform | Measure subgroup utility |
| Reporting fairness without utility cost | Fairness is the focus | Add accuracy and calibration |
| Hiding a worsened gap | It complicates the story | Report both directions |
| Using the test set to choose the intervention | Convenient | Use validation, then a final test |
| Writing an audit with no owner or review date | It reads like a paper | Add decision, owner, monitoring, date |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Every metric is green but the decision is unclear | No stated policy priority | Write constraints and a priority before the next run |
| Intervals are too wide to decide | Small evaluation | Increase the sample or narrow the claim |
| Fairness improved but accuracy collapsed | The intervention is too aggressive | Tune the strength; report the frontier |
| Stability improved but users distrust explanations | Stability is not fidelity or communication | Add fidelity checks and plain-language reasons |
| DP model has a larger subgroup gap | Noise interacts with group size | Report subgroup utility; consider stratified evaluation |
| Reviewers cannot reproduce a number | No artifact or seed | Publish the script, config, and split |

## Check your understanding

1. Why is a weighted "fairness score" difficult to audit?
2. State the three changes in LAB-18's reweighted model and which one the policy must prioritize.
3. Why do overlapping intervals matter for the decision?
4. Why is explanation stability not a manipulation defense?
5. Name two ways DP can affect subgroup utility unevenly.
6. Write the scope sentence you would put at the top of an audit report.

Answers are discussed in the [answer key](quiz-answers.md).

## Summary

- Accuracy, subgroup gaps, explanation stability, privacy, and robustness trade against each other. The direction and size are empirical.
- LAB-18's reweighting lowers the EOd gap by 0.0301, raises the DP gap by 0.0112, and lowers accuracy by 0.0139, with overlapping intervals.
- A constrained decision — floors, caps, and a stated priority — is auditable; a composite score is not.
- Stability under noise is not fidelity and not resistance to targeted manipulation.
- DP's uniform guarantee does not imply uniform subgroup utility.
- The audit report names scope, groups, configurations, metrics, results with intervals, trade-offs, residual risks, decision, owner, and review date.
- Ambiguity is a finding. Record it rather than forcing a winner.

## Next

Complete the [Module 14 quiz](quiz.md) and [exercises](exercises.md), then continue to [Module 15 — Generative AI, LLM, RAG, and AI Agent Security](../m15-genai-llm-agents/index.md).
