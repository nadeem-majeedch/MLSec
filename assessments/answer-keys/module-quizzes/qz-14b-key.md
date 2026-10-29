# QZ-14B Answer Key — Module 14

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — local model behavior under a stated method

An attribution describes how the model's output changes relative to a baseline under a particular method. It is not a causal claim about the world, and it does not establish that the feature is fair or lawful to use.

- **A** confuses model behavior with causation.
- **C** is a normative and legal question that an attribution cannot answer.
- **D** is a stability property, measured separately.

Tag: M14 · LO-31 · Bloom 2 · D1.

## 2. B — small input changes, small attribution changes

Stability is a continuity property relative to a metric and a perturbation size. Exact invariance for every input is stronger than any practical method provides and is not the definition. A stable explanation can still be unfaithful; stability and faithfulness are different claims.

- **A** describes invariance, not stability.
- **C** is an additivity property some methods have.
- **D** is human agreement, not stability.

Tag: M14 · LO-31 · Bloom 2 · D1.

## 3. False

Equal selection rates are demographic parity. Equal TPR and FPR are equalized odds. When base rates or score distributions differ, a model can have equal selection rates while its error rates differ across groups; the metrics constrain different quantities and can conflict.

Tag: M14 · LO-32 · Bloom 2 · D1.

## 4. True

An explanation endpoint returns information about the model's local sensitivity or feature contributions. Even without a predicted label, repeated queries can support model extraction, inference about features, or reconstruction of decision behavior. Explanation access is model access and needs authentication, quotas, and monitoring.

Tag: M14 · LO-31 · Bloom 2 · D1.

## 5. Required elements (two metrics and the conflict)

Metrics such as demographic parity, equalized odds (TPR/FPR), predictive parity (precision), calibration, or individual fairness. The conflict: when group base rates differ, equal selection rates and equal error rates generally cannot both hold; satisfying one forces a trade-off in the other. The choice among them is a normative decision about which error matters, not a purely technical one.

Tag: M14 · LO-32 · Bloom 3 · D2.

## 6. Group A: TPR 0.75, FPR 0.167, precision 0.75, selection 0.40. Group B: TPR 0.50, FPR 0.083, precision 0.80, selection 0.25. DP gap 0.15; EO gaps 0.25 (TPR) and 0.083 (FPR).

Group A:

- TPR $= 60/(60+20) = 0.75$.
- FPR $= 20/(20+100) = 0.167$.
- Precision $= 60/(60+20) = 0.75$.
- Selection rate $= (60+20)/200 = 0.40$.

Group B:

- TPR $= 20/(20+20) = 0.50$.
- FPR $= 5/(5+55) = 0.083$.
- Precision $= 20/(20+5) = 0.80$.
- Selection rate $= (20+5)/100 = 0.25$.

Gaps:

- Demographic parity: $|0.40 - 0.25| = 0.15$.
- Equalized odds, TPR: $|0.75 - 0.50| = 0.25$.
- Equalized odds, FPR: $|0.167 - 0.083| = 0.083$.

Group A is selected more often and has the higher TPR, but also the higher FPR. A single "fairness gap" number would hide which error is unequal.

Tag: M14 · LO-32 · Bloom 3 · D2.

## 7. Required elements (two flaws and what magnitude does not show)

Two of:

- **Magnitude is not faithfulness.** A method can produce large attributions that do not track the model's behavior; scale depends on the method, the baseline, and normalization.
- **No ground truth or randomization baseline.** Without a deletion/insertion test, a random attribution, or a known-behavior check, "larger" has no interpretation.
- **The methods may use different scales.** Comparing mean absolute values across methods without normalization is not a comparison of quality.
- **No stability test.** A method can be large and unstable; stability must be measured under controlled input changes.
- **One dataset and one model.** The comparison does not generalize without repeats or a stated scope.

Magnitude does not show that method A is more faithful, stable, or useful. A valid comparison defines a faithfulness metric, a stability metric, a common baseline, and reports uncertainty.

Tag: M14 · LO-31 · Bloom 4 · D3.

## 8. Required elements (groups and metrics, uncertainty, stability, mitigation, limits)

A bounded review:

- **Groups and metrics:** define the groups in the synthetic data; report TPR, FPR, precision, selection rate, and calibration per group; state the decision threshold. Report counts and denominators, not only percentages.
- **Uncertainty:** bootstrap confidence intervals for each metric and gap; with small groups, the interval may be wide enough that the apparent gap is inconclusive.
- **Stability test:** perturb inputs by a small, stated amount (for example, feature noise within measurement precision) and measure rank correlation or top-k overlap of attributions; report the distribution, not one example.
- **Mitigation:** for example, reweighting, threshold adjustment, or constrained training; measure the effect on subgroup metrics, overall accuracy, and the explanation behavior, and state the trade-off.
- **Limits:** the data are synthetic and de-identified, so the result is a method demonstration, not a finding about real applicants; the analysis is observational, not causal; the choice of fairness metric is normative; one split and one model do not cover deployment drift.

A conclusion such as "the model is fair" is not supportable. A supportable statement names the metric, the group, the interval, the threshold, and the fact that the evaluation used synthetic data.

Tag: M14 · LO-32 · Bloom 5 · D3.
