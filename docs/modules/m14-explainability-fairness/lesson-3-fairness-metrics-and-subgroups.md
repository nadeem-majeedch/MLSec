# Lesson 14.3 — Fairness Metrics and Subgroup Evaluation

<a id="m14-l3"></a>

**Module 14 · Lesson 3 of 4 · 1.5 hours · LO-32**

## Scenario

A model review reports overall accuracy 0.75 and a demographic-parity gap of 0.001. The slide is green. A reviewer asks for the false-positive rates by group. The model's false-positive rate is 0.2595 for group 0 and 0.1364 for group 1 — a gap of 0.1231. The selection rates are nearly identical, so the parity metric was satisfied while the error burden was not.

Neither number is a lie. They measure different things, and the choice of metric determined which harm was visible.

## Objectives

By the end of this lesson you will be able to:

1. Compute selection rate, TPR, FPR, and accuracy for a subgroup.
2. Compute demographic parity, equal opportunity, and equalized-odds gaps.
3. Explain why these criteria can conflict when base rates differ.
4. Report subgroup results with counts and confidence intervals.
5. Evaluate calibration and state when it is missing.
6. Write a subgroup evaluation that supports a decision without overclaiming.

## 1. The confusion matrix, per group

For a binary decision \(\hat{y} \in \{0,1\}\) and outcome \(y \in \{0,1\}\), each group has four counts:

| | \(\hat{y}=1\) | \(\hat{y}=0\) |
|---|---:|---:|
| \(y=1\) | TP | FN |
| \(y=0\) | FP | TN |

From these:

\[
\text{TPR} = \frac{TP}{TP+FN}, \qquad
\text{FPR} = \frac{FP}{FP+TN},
\]

\[
\text{selection rate} = \frac{TP+FP}{N}, \qquad
\text{accuracy} = \frac{TP+TN}{N}.
\]

TPR is the fraction of true positives that are selected. FPR is the fraction of true negatives that are selected. Selection rate mixes both and depends on the base rate.

### A small worked example

Group A: 100 rows, 40 positives, 24 TP, 16 FN, 12 FP, 48 TN.

\[
\text{TPR} = 24/40 = 0.60,\quad
\text{FPR} = 12/60 = 0.20,\quad
\text{selection} = 36/100 = 0.36.
\]

Group B: 100 rows, 60 positives, 42 TP, 18 FN, 6 FP, 34 TN.

\[
\text{TPR} = 42/60 = 0.70,\quad
\text{FPR} = 6/40 = 0.15,\quad
\text{selection} = 48/100 = 0.48.
\]

The selection rates differ by 0.12, but so do the base rates (0.40 versus 0.60). A single parity number mixes the model's behavior with the population's prevalence.

## 2. The metrics

| Metric | Definition | Asks | Blind to |
|---|---|---|---|
| Demographic parity (DP) | Equal selection rates | Are groups selected at the same rate? | Error rates and base rates |
| Equal opportunity (EOp) | Equal TPR | Are true positives found at the same rate? | False positives |
| Equalized odds (EOd) | Equal TPR and equal FPR | Are both error rates equal? | Calibration and base rates |
| Predictive parity | Equal precision | Are positive predictions equally reliable? | False negatives |
| Calibration | Predicted probability matches observed frequency, per group | Are scores interpretable the same way? | Ranking within a group |
| Accuracy parity | Equal accuracy | Is overall correctness equal? | Error composition |

LAB-18 uses two gaps:

\[
\text{DP gap} = |\text{selection}_0 - \text{selection}_1|,
\]

\[
\text{EOd gap} = \max\left(|\text{TPR}_0 - \text{TPR}_1|,\ |\text{FPR}_0 - \text{FPR}_1|\right).
\]

The max makes the gap report the worse of the two error-rate differences. A model can have equal TPR and very different FPR; the max catches that.

## 3. LAB-18 results

The synthetic data has 1,200 rows, six features, and a group indicator that enters the logit with coefficient 1.0. Group 0 is 60% of the data; group 1 is 40%. The test split has 214 rows in group 0 and 146 in group 1. Reweighting assigns each group total weight 1/2, which changes the fitted coefficients.

### Baseline

| Group | n | Accuracy | TPR | FPR | Selection rate |
|---|---:|---:|---:|---:|---:|
| 0 | 214 | 0.7383 | 0.7349 | 0.2595 | 0.4439 |
| 1 | 146 | 0.7740 | 0.7000 | 0.1364 | 0.4452 |

\[
\text{DP gap} = |0.4439 - 0.4452| = 0.0013,
\]

\[
\text{EOd gap} = \max(|0.7349-0.7000|,\ |0.2595-0.1364|)
= \max(0.0349,\ 0.1231) = 0.1231.
\]

The demographic-parity gap is essentially zero. The false-positive rates differ by 12.3 percentage points: group 0 is falsely flagged at nearly twice the rate of group 1. A review that reported only DP would have missed the larger disparity.

### Reweighted

| Group | n | Accuracy | TPR | FPR | Selection rate |
|---|---:|---:|---:|---:|---:|
| 0 | 214 | 0.7290 | 0.7349 | 0.2748 | 0.4533 |
| 1 | 146 | 0.7534 | 0.7000 | 0.1818 | 0.4658 |

\[
\text{DP gap} = |0.4533 - 0.4658| = 0.0125,
\]

\[
\text{EOd gap} = \max(0.0349,\ 0.0930) = 0.0930.
\]

Overall accuracy falls from 0.7528 to 0.7389, a drop of 0.0139. The equalized-odds gap improves by 0.0301 (about 24%), driven entirely by a narrower FPR gap: group 1's FPR rises from 0.1364 to 0.1818 while group 0's rises from 0.2595 to 0.2748. TPRs do not change in this run.

Three observations:

1. **The intervention trades one gap for another.** DP worsens from 0.0013 to 0.0125. A team that had optimized DP would call this a regression.
2. **The improvement is in one error type.** The TPR gap is unchanged at 0.0349; only the FPR gap moves.
3. **Accuracy is not free.** The reweighted model makes 0.0139 more errors overall, because it shifts decision thresholds implicitly through the fitted coefficients.

### Intervals

LAB-18 bootstraps the test rows within each group 2,000 times:

| Model | DP gap (95% interval) | EOd gap (95% interval) |
|---|---|---|
| Baseline | 0.0013 (0.0015–0.1186) | 0.1231 (0.0408–0.2373) |
| Reweighted | 0.0125 (0.0015–0.1230) | 0.0930 (0.0254–0.2190) |

The intervals overlap substantially. The point estimates move in the reported directions, but this test set does not establish that the population gaps changed. A decision that depends on the improvement needs a larger evaluation or a different design, not a fourth decimal place.

The baseline DP interval not containing the point estimate is a reminder that percentile intervals are not centered on the observed value in small samples. Report the method, not just the bounds.

## 4. Why the criteria conflict

When base rates differ, several common fairness criteria cannot all hold at once.

- **Calibration + equal FPR + equal FNR** cannot all hold for a non-trivial classifier when prevalence differs across groups (Kleinberg, Mullainathan & Raghavan).
- **Equal PPV + equal FPR** implies equal prevalence (Chouldechova); with different base rates, the criteria are incompatible.
- **Demographic parity** can require different thresholds for groups with different score distributions, which conflicts with equalized odds.

A concrete intuition: if group B has more true positives, a model that selects the same fraction from each group (DP) will usually miss more true positives in group A or flag more negatives in group B. The metric choice decides which error is visible.

This is not a reason to abandon measurement. It is a reason to report several metrics and to state which harm the decision prioritizes.

| If the priority is... | Report | Accept |
|---|---|---|
| Equal access to the benefit | DP gap, selection rates | Possibly unequal error rates |
| Equal detection of true cases | TPR gap (equal opportunity) | Possibly unequal false positives |
| Equal error burden | TPR and FPR gaps (equalized odds) | Possibly unequal selection rates |
| Scores mean the same thing | Calibration curves per group | Possibly unequal selection and error rates |

## 5. Calibration

Calibration asks whether a predicted probability of 0.7 corresponds to a 70% observed rate, within a group. It is not the same as accuracy or equalized odds.

A model can be well calibrated overall and miscalibrated for a subgroup, or calibrated within each group while selecting at different rates. LAB-18 does not measure calibration; its outputs are hard labels. Any audit of a probability-generating model should add:

- reliability diagrams per group;
- observed/expected ratios in score bins;
- counts per bin, because empty or sparse bins produce unstable estimates;
- a statement about whether the model is used as a ranker or as a probability.

## 6. Subgroup evaluation protocol

1. **Define groups before looking at results.** Use the categories the decision affects, and state how they were collected.
2. **Report counts with rates.** A rate from 12 rows is not comparable to a rate from 2,000.
3. **Report at least two metric families.** DP plus equalized odds is a minimum; add calibration when probabilities are used.
4. **Attach intervals.** Bootstrap within groups; do not bootstrap the gap by resampling rows across groups without preserving group sizes.
5. **Check intersectional groups when sample size allows.** A gap can hide inside an aggregate; small cells need pooling or a flag, not a point estimate.
6. **State the base rates.** A selection-rate gap means something different when prevalence differs.
7. **Pre-register the decision rule.** "We will accept a gap only if the upper interval bound is below X" prevents post-hoc rationalization.
8. **Report the utility cost.** A fairness intervention that destroys accuracy is not a free improvement.

### Confidence intervals for a rate

For a proportion \(\hat{p}\) with \(n\) observations, the standard error is approximately

\[
SE = \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}.
\]

For a subgroup with 40 rows and 20 positives, a TPR of 0.70 has

\[
SE = \sqrt{0.70 \times 0.30 / 20} = \sqrt{0.0105} \approx 0.1025,
\]

so an approximate 95% interval is \(0.70 \pm 1.96(0.1025) \approx [0.50, 0.90]\). A reported gap of 0.15 against another group is well inside that uncertainty. The exact interval (Wilson or Clopper–Pearson) is better near 0 or 1, but the message is the same: count the rows before interpreting the rate.

## 7. What fairness metrics do not establish

| Claim | Why the metric cannot support it |
|---|---|
| "The model is fair." | Fairness is a family of criteria, not a single property |
| "There is no discrimination." | Metrics describe outcomes; they do not establish intent or legality |
| "The disparity is caused by the model." | Labels, features, and base rates may carry the disparity |
| "The intervention helped." | Point estimates can move without a population change; intervals may overlap |
| "The model is fair for everyone." | Aggregate groups hide intersectional and individual variation |
| "The explanation shows why." | Attributions are model descriptions, not causal effects |

Labels deserve separate scrutiny. If the historical outcome encodes biased decisions, a model trained to predict it can reproduce that bias while satisfying a parity metric. Fairness measurement is necessary and insufficient.

## 8. The security connection

Fairness and security interact in three ways that later lessons develop.

- **Poisoning can be targeted at a subgroup.** A backdoor or label-flip campaign can degrade one group's TPR while overall accuracy stays acceptable. Subgroup evaluation is a detection surface.
- **Evasion can be group-dependent.** A perturbation budget that works for one group's feature distribution may not transfer. Average robust accuracy hides the worst group.
- **Explanations can shift blame.** Lesson 14.2 showed that a crafted input can preserve the decision and change the stated reason. A fairness dispute that relies on the explanation is vulnerable to the same manipulation.

LAB-18 does not run attacks. It establishes the measurement baseline that an attack evaluation would compare against.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reporting only demographic parity | It is the simplest gap | Add TPR and FPR gaps |
| Reporting only equalized odds | It sounds stricter | Add selection rates and calibration |
| Reporting a gap without counts | Rates look precise | Report n and intervals |
| Comparing groups with different base rates as if parity were the goal | The metric is intuitive | State the base rates and the chosen criterion |
| Treating a point-estimate improvement as established | The direction looks clear | Check the interval |
| Ignoring calibration | The model outputs labels | Add reliability analysis for scores |
| Calling reweighting "debiasing" | It changes group influence | Call it a trade-off with measured effects |
| Evaluating on a test set used for model selection | Convenient | Hold out a final evaluation set |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| DP gap near zero but EO gap large | Error rates differ while selection rates match | Report both; investigate FPR and TPR separately |
| TPR gap zero but FPR gap large | Threshold behavior differs by group | Report the max gap and each component |
| Huge interval | Small group or rare outcome | Report counts; pool or flag |
| Reweighting changes accuracy a lot | Group weights shift the decision boundary | Report utility cost; tune the intervention |
| Calibration is poor in one group | Score distribution differs | Recalibrate per group or avoid probability claims |
| Results change across seeds | Small test set | Repeat splits; report variability |
| Subgroup counts are missing | Data collection omitted the attribute | State the gap in evidence; do not infer the attribute |

## Check your understanding

1. Compute the DP and EOd gaps for the baseline table. Which group bears the higher false-positive rate?
2. Why does the reweighted model improve EOd but worsen DP?
3. Why can calibration, equal FPR, and equal FNR not all hold when base rates differ?
4. A subgroup has 30 rows and a TPR gap of 0.2. What else must you report?
5. Why is "overall accuracy 0.75" insufficient for a fairness review?
6. Name two ways a security attack could create a subgroup disparity that aggregate accuracy hides.

Answers are discussed in the [answer key](quiz-answers.md).

## Summary

- Subgroup evaluation starts with counts and the confusion matrix, not with a single fairness score.
- DP measures selection rates; equal opportunity measures TPR; equalized odds measures TPR and FPR. They answer different questions.
- LAB-18's baseline has a DP gap of 0.0013 and an EOd gap of 0.1231. Reweighting lowers EOd to 0.0930, raises DP to 0.0125, and lowers accuracy from 0.7528 to 0.7389.
- Bootstrap intervals overlap; the point estimates alone do not establish a population change.
- Fairness criteria conflict when base rates differ. The choice of metric is a policy decision that should be stated.
- Calibration is a separate property; LAB-18 does not measure it.
- Metrics describe outcomes. They do not establish causation, legality, or the absence of discrimination.

## Next

Continue to [Lesson 14.4 — Security trade-offs and audit reporting](lesson-4-security-trade-offs-and-audit-reporting.md), where these measurements become a decision record.
