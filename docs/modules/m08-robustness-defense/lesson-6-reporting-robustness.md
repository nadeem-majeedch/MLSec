# Lesson 08.6 — Reporting Robustness and Defense Limits

<a id="m08-l6"></a>

**Module 08 · Lesson 6 of 6 · 1 hour · LO-28**

## Scenario

You have a table, an adaptive attack, and a stress budget. Now you have to write two pages for a committee that will decide whether to ship the model. One member is a security engineer, one is a product manager, and one is a lawyer. None of them will read your code.

The committee does not need every number. It needs three things: what was measured, what it means for the decision, and what would change your mind. This lesson turns an evaluation into that document.

## Objectives

By the end of this lesson you will be able to:

1. Structure a robustness report for a decision-maker without hiding the technical basis.
2. Write a scoped claim that includes cost, budget, attack, and residual risk.
3. Present a defense comparison as a trade-off rather than a winner.
4. State limitations and a falsification condition for your own result.
5. Map the report to a governance function so it can be filed and audited.

## 1. Start from the decision

A report has a decision it supports. Write it down first.

| Decision | What the report must answer |
|---|---|
| Ship the model | Is the residual risk acceptable at the stated threat model? |
| Buy the vendor's defense | Does the evidence support the vendor's claim, on our data? |
| Fund adversarial training | What does the robustness gain cost in accuracy and compute? |
| Accept a preprocessing filter | What does it stop, what does it miss, and for how long? |
| Deploy with monitoring only | What would we see if the threat model is wrong? |

A report that answers none of these is a lab notebook. That is useful, but it is not a decision document.

## 2. The scoped claim

Every robustness statement in the report should be one sentence with the same structure you practiced in Lesson 1, plus a consequence.

> At the ε = 0.10 L∞ budget, against a white-box 20-step, 2-restart PGD attacker, adversarial training raises robust accuracy from 62.0% to 73.0% and lowers ASR from 35.8% to 18.1% on the 540-row held-out digits test set, at a cost of 7.6 points of clean accuracy. At ε = 0.20, robust accuracy is 35.4% and ASR is 60.3%. The control is recommended for budgets up to 0.10; above that, it is a partial mitigation.

Four properties make this usable:

| Property | Where it appears |
|---|---|
| Measured quantity | Robust accuracy, ASR, clean accuracy |
| Conditions | Budget, norm, attack, knowledge, base set |
| Cost | Clean accuracy and compute |
| Scope | "Up to 0.10"; what happens beyond |

A claim without the fourth property invites the reader to assume the result holds everywhere.

## 3. Present a trade-off, not a winner

The comparison in LAB-11 has no single winner, and pretending otherwise is the most common reporting failure.

| Model | Clean acc. | Robust acc. ε=0.10 | ASR ε=0.10 | Robust acc. ε=0.20 | Best for |
|---|---:|---:|---:|---:|---|
| Undefended | 0.9667 | 0.6204 | 0.3582 | 0.0407 | Maximum clean accuracy when the attack is not credible |
| Adversarial training | 0.8907 | 0.7296 | 0.1809 | 0.3537 | Deployments where attacked errors are costly and the budget is bounded near 0.10 |
| Input squeezing | 0.9500 | 0.7722 | 0.1871 | 0.0019 | A cheap speed bump when clean accuracy matters and the threat is naive |

Notice the "best for" column. It forces the report to say what the reader should do, instead of ranking models on a metric that hides the decision.

The squeezing row is the most likely to be misread. Its ε = 0.10 numbers are the best in the table, and its ε = 0.20 numbers are the worst. A reader who sees only the first three numeric columns will choose the wrong system.

## 4. Residual risk and what the tests did not cover

Every defense leaves risk. Name it.

| Residual risk | Evidence or reason | Who owns it |
|---|---|---|
| Adaptive attacks stronger than BPDA | Only one adaptive attack was run; it matched, but did not dominate, the naive attack at ε = 0.10 | ML security team |
| Budgets above 0.20 | Not evaluated; the trend suggests failure | Product owner with the threat model |
| Other norms (L2, L1, rotation, occlusion) | Not evaluated | ML security team |
| Other model families | Only logistic regression; the method transfers, the numbers do not | Model owner |
| Detector false positives | No detector was deployed in this lab | Operations, if a detector is added |
| Serving drift | Transform version mismatch is possible | Platform team |
| Attack cost | Not measured; a stronger attacker may afford more queries | Threat-model owner |

A residual-risk table is not an admission of failure. It is the part of the report that lets a reader decide whether the untested areas matter for their deployment.

## 5. Limitations and a falsification condition

State what would change your conclusion. This is the difference between a report and a press release.

> This conclusion would change if (a) a query-based or better-tuned adaptive attack exceeded the PGD results at ε = 0.10, (b) the clean-accuracy cost rose above the product threshold, (c) evaluation on a second data split moved the robust-accuracy gain within the seed-to-seed range, or (d) the deployed budget were raised above 0.10.

Each condition is testable. Each has an owner. None of them requires the reader to trust the author's judgment.

### Report the negative results too

If an attack failed, say so and say why. If a defense did nothing, say that. Negative results:

- prevent another team from repeating the work;
- show the evaluation was broad enough to try;
- make the positive results more credible.

A report that contains only successes is a selection of evidence, not a summary of it.

## 6. Map to the governance function

A robustness report that is filed against a framework can be audited later. NIST AI RMF's MEASURE and MANAGE functions are a natural fit: MEASURE covers the evaluation, MANAGE covers the response and residual risk.

| Report section | Governance question | Evidence |
|---|---|---|
| Threat model | What risk are we measuring? | Norm, budget, knowledge, base set |
| Measurement | What did we find? | Metrics with denominators |
| Comparison | What are the alternatives? | Trade-off table |
| Residual risk | What remains? | Risk table with owners |
| Monitoring | How would we know if we are wrong? | Alerts, review cadence, rollback |
| Decision | What do we recommend? | Scoped recommendation with conditions |

Monitoring belongs in a robustness report even though it is not a robustness measurement. If the defense is scoped to ε ≤ 0.10, the deployment needs a way to notice inputs outside that range. A report that recommends a control without a detection plan is half a report.

## 7. A two-page structure

Use this outline. It fits on two pages and answers the committee's questions in order.

```text
1. Decision requested (one paragraph)
2. What we measured (threat model, data, attack, base set)
3. Results (one table, every column labeled)
4. Interpretation (what the numbers do and do not support)
5. Cost (clean accuracy, compute, operational)
6. Residual risk (table with owners)
7. Limitations and falsification conditions
8. Recommendation (scoped, with monitoring)
9. Reproduction (command, versions, artifact location)
```

The reproduction line is not decoration. It is what lets a reviewer check the claim six months later, when the author has left the team.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Leading with the best number | It is the most impressive | Lead with the decision and the conditions |
| Hiding the clean-accuracy cost | It weakens the recommendation | Put it in the same table as the gain |
| Calling one defense "best" | Ranking is simpler than trade-offs | Add a "best for" column and a scope |
| Omitting residual risk | It feels like admitting failure | Name the risk and its owner |
| No falsification condition | The conclusion feels final | State what would change it |
| No monitoring plan | Robustness is treated as a one-time test | Add detection and review cadence |
| Reproduction command missing | It worked on the author's machine | Include the command and versions |
| Sending the lab notebook instead of a report | The data is all there | Write the two-page structure |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Committee asks "so is it safe?" | The report has no scoped recommendation | Convert the claim into "safe for X, not for Y" |
| Reviewer disputes a number | Denominator or attack configuration missing | Point to the protocol section and the artifact |
| Recommendation is rejected as overclaiming | Limitations were buried | Move them next to the claim |
| Nobody can reproduce the result | Versions or command missing | Add the reproduction section |
| Risk owner is unclear | Residual risk has no assignment | Add an owner column and confirm it |
| Report grows without limit | Every experiment is included | Move detail to an appendix; keep the decision page short |

## Check your understanding

1. What four properties must a scoped robustness claim contain?
2. Why is a "best for" column more useful than a ranking in a defense comparison?
3. Give three residual risks that LAB-11 does not measure.
4. Write one falsification condition for the claim that adversarial training is worth its cost.
5. Which NIST AI RMF functions map to measurement and to response, and why does monitoring belong in the report?

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Start the report from the decision it supports, not from the table.
- A scoped claim states the quantity, the conditions, the cost, and the boundary.
- Present defenses as trade-offs with a "best for" column; the LAB-11 table has no single winner.
- Name residual risks with owners, including attacks and budgets that were not evaluated.
- State falsification conditions and include negative results.
- Map the report to MEASURE and MANAGE, and include a monitoring plan for the defense's operating range.
- A passing test is evidence for one threat model. The report's job is to say which one, and what lies outside it.

## Next

Complete [LAB-11](../../labs/lab-11.md), then the [knowledge check](quiz.md) and [exercises](exercises.md). LAB-11 asks you to produce the comparison, the stress test, and the scoped claim this module has built toward.
