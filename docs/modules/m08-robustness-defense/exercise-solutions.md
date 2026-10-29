# Exercise Solutions — Module 08

**Worked answers and marking guidance.** Numbers are rounded to four decimals; accept small differences from intermediate rounding.

## Exercise 1 — Read the defense table

**1. Adversarial training trade-off.**

- Clean cost: \(0.9667 - 0.8907 = 0.0760\), or 7.60 percentage points.
- Robust gain at ε = 0.10: \(0.7296 - 0.6204 = 0.1092\), or 10.92 percentage points.

**2. Squeezing trade-off.**

- Clean cost: \(0.9667 - 0.9500 = 0.0167\), or 1.67 points.
- Robust gain: \(0.7722 - 0.6204 = 0.1518\), or 15.18 points.

Those numbers make squeezing look better than adversarial training on both axes. The stress column reverses the conclusion: at ε = 0.20, squeezing's robust accuracy is 0.0019 against 0.3537 for adversarial training. Squeezing buys its gain inside a narrow operating range by discarding precision. Comparing only the ε = 0.10 columns hides that boundary.

**3. Relative ASR reduction at ε = 0.10.**

- Adversarial training: \((0.3582 - 0.1809)/0.3582 = 0.1773/0.3582 = 0.4950\), or 49.5%.
- Squeezing (naive attack): \((0.3582 - 0.1871)/0.3582 = 0.1711/0.3582 = 0.4777\), or 47.8%.

The two are close. The difference is that adversarial training keeps working at the stress budget and squeezing does not.

**4. Rankings.**

- ε = 0.10: squeezing 0.7722 > adversarial training 0.7296 > undefended 0.6204.
- ε = 0.20: adversarial training 0.3537 > undefended 0.0407 > squeezing 0.0019.

The ranking changes, and the system that is first at the smaller budget is last at the larger one. A one-budget report can therefore recommend the wrong control. Report the curve or a table with both budgets.

**5. Two corrections.**

- Robust accuracy is defined at a budget. "Highest robust accuracy" without a budget does not identify a best defense.
- The comparison must include clean utility, adaptive-attack behavior, and the stress result. Squeezing's high ε = 0.10 number is paired with a 1.67-point clean cost and near-total failure at ε = 0.20 under an adaptive attack.

## Exercise 2 — Detector precision and operating cost

**1. Precision at three base rates.**

At \(\pi = 0.002\):

\[
\frac{0.85 \times 0.002}{0.85 \times 0.002 + 0.02 \times 0.998}
= \frac{0.0017}{0.0017 + 0.01996}
= \frac{0.0017}{0.02166}
\approx 0.0785.
\]

At \(\pi = 0.01\):

\[
\frac{0.0085}{0.0085 + 0.0198} = \frac{0.0085}{0.0283} \approx 0.3004.
\]

At \(\pi = 0.10\):

\[
\frac{0.085}{0.085 + 0.018} = \frac{0.085}{0.103} \approx 0.8252.
\]

Precision rises from 7.8% to 30.0% to 82.5% while TPR and FPR are unchanged. The base rate does the work.

**2. Alerts per true attack at 0.2%.**

In 100,000 inputs: 200 attacked, 99,800 benign.

- True positives: \(0.85 \times 200 = 170\).
- False positives: \(0.02 \times 99{,}800 = 1{,}996\).
- Total alerts: \(170 + 1{,}996 = 2{,}166\).
- Alerts per true attack: \(2{,}166 / 170 \approx 12.7\).

**3. Review burden.**

\(2{,}166 \times 4 = 8{,}664\) minutes per day, or 144.4 hours. Of that, \(170 \times 4 = 680\) minutes (11.3 hours) concern real attacks; 7,984 minutes (133.1 hours) concern false positives. At 8 hours per reviewer-day, the queue needs about 18 reviewer-equivalents. A detector with 85% TPR and 2% FPR is not operationally cheap at a low base rate.

**4. Reducing burden without overclaiming.**

Accept two of:

- raise the threshold and re-measure the TPR/FPR curve at the deployment prevalence;
- tier the response: automatic quarantine for high scores, sampling for low scores;
- reduce the attack base rate with rate limits, authentication, or input validation upstream;
- review a random sample rather than every alert, and track misses;
- automate triage with a second signal, validating it on benign inputs.

Any change to the threshold changes TPR and FPR. Re-measure; do not assume the old operating point.

**5. Adaptive-detector test.**

Optimize the attacker's input against the detector's score while preserving the classifier attack: for example, add a penalty when the detector score rises, or search for perturbations that keep the squeezed/original disagreement below the threshold. Measure evasion rate at a fixed detector FPR, with the attacker knowing the transform and threshold. Report the strongest result and the attack's cost.

## Exercise 3 — The AegisShield claim

**1. At least five problems.**

- **Budget too small.** ε = 0.03 is small relative to a quantizer's cell size; the defense may be arithmetically protected rather than robust.
- **Underpowered attack.** 3 steps with one restart is unlikely to traverse the budget or find the worst case.
- **Wrong base set.** "Full test set" includes rows the model already misclassified, diluting ASR; the clean-correct base size is not reported.
- **No clean utility.** The claim does not say what the module costs on benign uploads or whether it changes predictions.
- **No adaptive attack.** The attacker is described as not knowing the preprocessing parameters, which is not a threat model; an adaptive attack is missing.
- **No stress budget.** There is no result above ε = 0.03, so the operating range is unknown.
- **Metric ambiguity.** "Improves robustness from 61% to 99.1%" does not define the metric or the denominator; 0.4% ASR is quoted without its base.
- **Single model and dataset.** No uncertainty, no second split, no statement of what was not tested.

**2. Why secrecy is not a boundary.**

The module is deployed in a product that external claimants can query. Its behavior is observable: repeated submissions reveal which inputs are unchanged by quantization, which are rejected, and how predictions respond near boundaries. Parameters can be inferred approximately from probes, and the code or a copy may leak. Kerckhoffs's principle applies: assume the attacker knows the design, and evaluate under that assumption. Secrecy raises the cost of an attack; it does not change what is possible.

**3. Adaptive attack design.**

- **Knowledge:** white-box or high-query black-box; transform code and parameters known.
- **Technique:** PGD with BPDA through the quantizer (identity backward), or EOT if the denoiser is stochastic; if scores are hidden, a query-based boundary attack.
- **Budget:** ε = 0.03 as claimed, plus ε = 0.06 and 0.12 as stress points.
- **Success:** the classifier's label after preprocessing differs from the true label, measured on clean-correct rows.
- **Protocol:** 20+ steps, tuned step size, 2+ restarts, report the strongest valid result and the failed attempts.

**4. Questions for the vendor.**

Accept four, including at least one on clean utility:

- What is clean accuracy on our data before and after the module, and how many benign inputs change prediction?
- Was the module applied during training, serving, or both, and how is that versioned?
- What is the strongest adaptive attack you ran, at which budgets, and what were the results?
- What happens at ε = 0.06 and 0.12? Provide the curve.
- What is the false-positive/rejection rate on benign uploads, and how is a rejection handled?
- Can we reproduce the evaluation with a fixed environment and command?

**5. Deployment posture.**

Enable the module as one layer behind authentication, rate limits, and schema validation; do not treat it as a boundary. Pilot on a sample with human review and a rollback path. Monitor the rejection rate, the distribution of low-confidence predictions, upload anomalies, and any drift in the input pipeline. Residual risk: an adaptive attacker at or above the tested budget, other norms, and a training/serving preprocessing mismatch. Operational cost: added per-upload latency and the human review of flagged or rejected documents.

**6. Memo.**

> **Finding.** AegisShield's claimed robustness is measured at a small budget with an underpowered, non-adaptive attack on an unspecified base set. **Evidence.** Three-step PGD at ε = 0.03 with one restart and no clean-utility or adaptive result does not establish robustness at the deployment threat model. **Impact.** External claimants can submit adaptive uploads; a wrong prioritization is reversible, but a denial of legitimate claims is not free. **Limitation.** We have not measured the module on our data. **Recommendation.** Run the adaptive evaluation in item 3 on a pilot sample, enable the module only as one layer, and keep human review and rollback. **Owner and review.** ML security team; review after the pilot, before any expansion.

## Exercise 4 — Turn numbers into a scoped claim

**1. At ε = 0.05.**

\[
\text{clean accuracy} = 940/1{,}000 = 0.9400
\]

\[
\text{ASR} = 235/940 = 0.2500
\]

\[
\text{robust accuracy} = (940 - 235)/1{,}000 = 705/1{,}000 = 0.7050
\]

**2. At ε = 0.15.**

\[
\text{ASR} = 590/940 = 0.6277
\]

\[
\text{robust accuracy} = (940 - 590)/1{,}000 = 350/1{,}000 = 0.3500
\]

The base stays 940 because it is defined by the clean predictions, which do not change when the evaluation budget changes. It is not re-filtered to rows that survived the smaller attack.

**3. Scoped claim.**

> On the 940 clean-correct rows of a 1,000-row held-out test set, the defended four-class model has clean accuracy 0.9400, against 0.9667 for the undefended model on the same split (a 2.67-point clean cost). Under a white-box, 20-step, 2-restart PGD attack in L∞, its robust accuracy is 0.7050 and ASR is 0.2500 at ε = 0.05; at ε = 0.15, robust accuracy is 0.3500 and ASR is 0.6277. No adaptive attack was run. This is an empirical result for the tested attack family and budgets; it does not certify robustness at any radius and does not cover other norms, models, or data.

**4. Two evaluation-created limitations.**

Accept two:

- Only one attack family and one hyperparameter setting were used; a stronger or adaptive attack could lower robust accuracy.
- Only one split and one model were evaluated; run-to-run and split-to-split variation are unknown.
- The 0.15 stress result is on the same base set, which is correct, but it does not reveal behavior at intermediate budgets between 0.05 and 0.15.
- The clean cost is measured against one undefended baseline, not against alternative defenses at equal cost.

**5. Falsification condition and monitoring signal.**

- **Falsification:** an adaptive or query-based attack at ε = 0.05 raises ASR materially above 0.2500 on a second split, or the clean cost exceeds the product threshold.
- **Monitoring:** a sustained rise in low-confidence or high-entropy predictions, an increase in rejected or anomalous inputs, or a drift alert on the upload distribution. Each is a proxy; none proves an attack, which is why alerts route to review rather than automatic action.

**6. Two-sentence answer.**

"At the tested budget, one in four predictions that were correct before the attack becomes wrong, so the model is not safe against that attacker. It is better than the undefended baseline inside the tested range, and the evidence stops at that range; an adaptive attack or a larger budget could change the conclusion."
