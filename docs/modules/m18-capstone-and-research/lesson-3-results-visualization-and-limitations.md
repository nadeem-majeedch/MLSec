# Lesson 18.3 — Results, Visualization, and Limitations

<a id="m18-l3"></a>

**Module 18 · Lesson 3 of 4 · 1 hour · LO-33**

## Scenario

A capstone report contains fourteen figures and no tables. The headline figure is a bar chart with a truncated y-axis (0.72 to 0.79), no error bars, and a caption that says "defense improves robustness." The appendix lists three seeds, but the figure shows the best one. The limitations section says "time constraints limited the scope."

An evaluator cannot tell whether the defense improved anything. The difference between 0.72 and 0.79 might be noise, the axis exaggerates it, and the seed selection hides the variance. The work may be good; the reporting makes it unverifiable.

Results are not decoration. They are the argument, and every element either supports the claim or weakens it.

## Objectives

By the end of this lesson you will be able to:

1. Structure results claim-first, with one table per claim and denominators stated.
2. Design tables and figures that show budgets, baselines, and uncertainty.
3. Report negative and null results without overclaiming or apologizing.
4. Classify limitations as construct, internal, external, and statistical.
5. Write a results paragraph that states evidence, alternative explanation, and limitation.

## 1. Claim-first results

Write the claim before the table. If the table does not support the claim, change the claim.

| Claim type | Form | Table columns |
|---|---|---|
| Comparison | "Defense D reduces ASR from X to Y at budget B" | Condition, ASR, clean accuracy, budget, n, interval |
| Effect size | "The effect is Z points, with interval [a, b]" | Effect, interval, baseline, seeds |
| Trade-off | "D reduces ASR at a cost of C false declines" | ASR, false decline, threshold, cost |
| Detection | "Detector achieves recall R at FP rate F" | Threshold, recall, FP, precision at prevalence |
| Failure | "Attack A did not exceed the baseline at budget B" | Attempts, budget, observed effect, interval |

### One claim per table

A table with nine metrics and four conditions invites the reader to find the flattering cell. A table with one claim and the metrics that support it invites scrutiny of that claim.

### The claim sentence

```text
CLAIM 3: At an L-infinity budget of 4/255 and 20 restarts, adversarial
training reduces attack success from 0.62 [0.58, 0.66] to 0.31
[0.27, 0.35] on the frozen evaluation set, while clean accuracy falls
from 0.941 to 0.918.
```

The claim names the budget, the procedure, the metric, the interval, the base set, and the cost. A reader can disagree with it precisely.

## 2. Table design

A results table is an audit form. It needs enough information for a reader to recompute the claim.

| Column | Why |
|---|---|
| Condition or configuration | What was run |
| Metric | What was measured |
| Value | The number |
| Interval or spread | Uncertainty over seeds or bootstrap |
| n / denominator | What the number is over |
| Budget | Perturbation, queries, poison rate, epochs |
| Baseline | The comparator |
| Seed(s) | Which runs produced the value |

### Example — robustness comparison

| Defense | Clean acc. | ASR @ ε=2/255 | ASR @ ε=4/255 | ASR @ ε=8/255 | Seeds | Eval n |
|---|---:|---:|---:|---:|---:|---:|
| None | 0.941 | 0.58 | 0.71 | 0.86 | 5 | 1,000 |
| Input squeezing | 0.936 | 0.49 | 0.63 | 0.81 | 5 | 1,000 |
| Adversarial training | 0.918 | 0.24 | 0.38 | 0.57 | 5 | 1,000 |
| Adv. training + squeezing | 0.914 | 0.21 | 0.35 | 0.54 | 5 | 1,000 |

The numbers are illustrative, not measured. The structure is the point: clean cost is visible, the budget is a column, the base set is stated, and seeds are reported.

### Formatting rules

- Put the metric's range in the header (`ASR`, lower is better) or the caption.
- Use the same decimal precision within a column.
- Bold nothing; let the numbers speak.
- Report the baseline in the same table, not in prose.
- Put per-seed values in an appendix or a supplementary CSV.
- Never round a small effect into invisibility (0.918 vs 0.914 is 0.4 points, not "no difference").

## 3. Figures answer a question

Choose the figure from the question, not from the chart menu.

| Question | Figure | Avoid |
|---|---|---|
| How does the effect change with budget? | Line with interval band | Bar chart at one budget |
| How do conditions compare at one budget? | Dot plot with intervals | 3D bars |
| What is the distribution over seeds? | Strip or box plot with points | Mean-only bar |
| What is the trade-off between two costs? | Scatter or ROC-style curve | Dual y-axis |
| Where does the detector fail? | Confusion matrix or per-class bars | Pie chart |
| Is the attack targeted? | Per-class success bars | Single aggregate number |

### Rules that prevent misleading figures

1. **Start the y-axis at zero for bar charts.** If the interesting range is narrow, use a dot plot and say so; do not truncate bars.
2. **Show uncertainty.** Error bars or bands from seeds or bootstrap; state what they represent in the caption.
3. **No dual axes.** Two scales invite false correlation. Use two panels.
4. **No 3D, no rainbow colormaps, no shadows.** They distort and exclude readers.
5. **Label units and budgets.** "ASR" without ε is not a result.
6. **Caption carries n, budget, seed count, and what the interval is.**
7. **One message per figure.** If the caption needs three sentences, split the figure.

### Example caption

> **Figure 4.** Attack success rate versus L∞ budget for three defenses. Points are the mean over five training seeds; bands are the min–max range across seeds. Evaluation set: 1,000 held-out digits, frozen at M2 (hash `a71b…`). Attack: PGD, 40 steps, 10 restarts. Lower is better.

The caption is longer than the figure's title and shorter than the method section. It contains everything a reader needs to interpret the plot without hunting.

## 4. Uncertainty with small samples

Capstones run few seeds. That does not excuse point estimates without intervals; it requires honest ones.

| Situation | Report | Do not |
|---|---|---|
| 3–5 seeds | Mean and min–max or a bootstrap interval; state n | Standard deviation alone, implying a population |
| One seed | The value and "single seed; no interval" | A fake interval |
| 20 attack events | Count and a Wilson interval | "90% detection" with no denominator |
| 1,000 evaluation records | Bootstrap interval | Three significant figures without uncertainty |
| Zero observed failures | "0 of n" and the upper bound of the interval | "0% failure rate" |

The rule of three is a useful approximation: if zero events occur in n trials, the upper 95% bound is about 3/n. "0 of 100" is consistent with a rate as high as ~3%, not 0%.

## 5. Negative and null results

A negative result is a result when it is measured.

| Statement | Meaning | Acceptable |
|---|---|---|
| "Attack A succeeded 0 of 200 times at budget B" | Observed failure at a budget | Yes, with the budget and n |
| "No effect was detected at this sample size" | Underpowered null | Yes, with the interval |
| "Defense D is robust" | Universal claim | No |
| "Attack A is impossible" | Unfalsifiable | No |
| "The defense works" (after one seed) | Overclaim | No |

Write the negative result with the same structure as a positive one: hypothesis, budget, procedure, observation, interval, interpretation, and what would change the conclusion.

### Absence of evidence

If the interval is wide, the honest conclusion is "the data are consistent with effects up to X." That is useful: it bounds the risk. It is not the same as "no effect."

## 6. Limitations as validity analysis

A limitation explains why the conclusion might be wrong. It is not an apology and not a list of things you did not have time for.

| Validity type | Question | Capstone example | How to address |
|---|---|---|---|
| Construct | Does the metric measure the harm? | ASR measures model error, not customer harm | State the proxy; add a decision-level metric |
| Internal | Is the comparison confounded? | Defense retrained with a different split | Freeze the split; rerun the control |
| External | Does it generalize? | One synthetic dataset, one model family | State the boundary; add a second dataset if time |
| Statistical | Does the uncertainty support the claim? | Three seeds, overlapping intervals | Report intervals; soften the claim |

### Writing a limitation

```text
Internal validity. The defense run used the same split as the baseline,
but the threshold was retuned after the attack results were seen. The
reported ASR is therefore a post-tuning estimate. A pre-registered rerun
with the threshold fixed at 0.55 is in results/defense_fixed/ and is the
number cited in the abstract.
```

That is a limitation with evidence and a fix. "Time was short" is neither.

### Residual risk belongs in limitations

State what remains after the controls, under which adversary, with numbers. The four-part residual-risk statement from Module 17 applies here.

## 7. The results paragraph

Use the same four moves for every claim.

```text
1. Claim:      At ε=4/255, adversarial training reduces ASR to 0.38.
2. Evidence:   Mean over 5 seeds, 1,000-record frozen set; interval
               [0.34, 0.42]; clean accuracy 0.918.
3. Alternative: The reduction could reflect gradient masking rather than
               robustness; a transfer attack from an undefended model is
               reported in Table 6 and shows ASR 0.44, which argues
               against pure masking but does not rule it out.
4. Limitation: One architecture and one dataset; the result does not
               establish robustness at larger ε or other modalities.
```

The alternative-explanation move is what separates an assessment from a sales pitch. If you cannot name one, you have not looked.

## 8. Worked example — from results folder to report

A capstone comparing three defenses has these runs:

- baseline, 5 seeds, 3 budgets;
- squeezing, 5 seeds, 3 budgets;
- adversarial training, 5 seeds, 3 budgets;
- adaptive PGD against the best defense, 3 seeds, 1 budget.

### Table plan

| Table | Claim | Contents |
|---|---|---|
| 1 | Clean cost of each defense | Clean accuracy with interval, 5 seeds |
| 2 | Robust accuracy at three budgets | ASR per condition and budget |
| 3 | Adaptive attack result | ASR under adaptive PGD vs static PGD |
| 4 | Computational cost | Train time, inference latency, memory |

### Figure plan

| Figure | Question | Type |
|---|---|---|
| 1 | How does ASR change with budget? | Line with seed band, three defenses |
| 2 | What does the defense cost in latency? | Dot plot with intervals |
| 3 | Where does the adaptive attack succeed? | Per-class bars |

Three figures, four tables, one appendix with per-seed values. The report does not need fourteen figures; it needs the ones that carry claims.

## 9. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Figure-first reporting | No claim, no audit | Claim, then table, then figure |
| Truncated bar axis | Exaggerated effect | Zero baseline or dot plot |
| No uncertainty | False precision | Seeds, intervals, n |
| Best-seed selection | Overstated result | Report all seeds |
| Dual axes | Implied correlation | Two panels |
| "No effect" from a wide interval | Overclaim | "Consistent with effects up to X" |
| Limitations as apology | No validity analysis | Construct/internal/external/statistical |
| No alternative explanation | Advocacy | Name and test one |
| Metric without denominator | Uninterpretable | State n and base set |
| Appendix hides the failure | Misleading summary | Report failures in the main text |

## 10. Check your understanding

1. Why write the claim before the table?
2. Name six columns a results table needs and the reason for each.
3. When may a bar chart y-axis be truncated, and what should be used instead?
4. What does "0 of 100" imply about the upper bound of the failure rate?
5. Distinguish construct, internal, external, and statistical validity with one example each.
6. What are the four moves of a results paragraph?

## 11. What you keep

A claim register, one table per claim with denominators and uncertainty, a figure plan with captions that state budget and n, a negative-results section, a four-part limitations analysis, and a results narrative with alternative explanations. These feed directly into the capstone report.

## 12. Next

Lesson 18.4 turns a capstone finding into a research question: gap statement, contribution type, study design, validity threats, and the ethics and supervision that a research route requires.
