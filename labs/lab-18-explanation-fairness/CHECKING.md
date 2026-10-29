# Checking Guide — LAB-18

## What the checker verifies

1. `metrics.json`, `run.json`, `report.md`, and `manifest.json` exist, and the manifest covers the three output files.
2. `run.json` records LAB-18, noise σ = 0.25, and top-k = 2.
3. The checker regenerates the synthetic data and refits both models; reported overall accuracy reproduces within 0.01.
4. Every subgroup has rows and all accuracy, TPR, FPR, and selection-rate values lie in [0, 1].
5. The reported demographic-parity and equalized-odds gaps match the subgroup values within 0.002.
6. Both bootstrap intervals are ordered and lie inside [0, 1].
7. Reweighting lowers the equalized-odds gap and raises the demographic-parity gap; accuracy falls by at least 0.005.
8. Both explanation methods are present for both models; Spearman is in [-1, 1], overlap in [0, 1], Spearman is at least 0.80 in this setup, and the prediction-preserving top-feature flip rate is between 0.05 and 0.30.
9. The report contains "demographic parity", "equalized odds", "stability", "trade-off", and "limitations".

## Reference results (seed 42)

| Model | Accuracy | TPR g0 | TPR g1 | FPR g0 | FPR g1 | DP gap | EO gap |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 0.7528 | 0.7349 | 0.7000 | 0.2595 | 0.1364 | 0.0013 | 0.1231 |
| Reweighted | 0.7389 | 0.7349 | 0.7000 | 0.2748 | 0.1818 | 0.0125 | 0.0930 |

Bootstrap 95% intervals: baseline DP [0.0015, 0.1186], EO [0.0408, 0.2373];
reweighted DP [0.0015, 0.1230], EO [0.0254, 0.2190].

Explanation stability, σ = 0.25:

| Model | Method | Spearman | Top-2 overlap | Flip rate |
|---|---|---:|---:|---:|
| Baseline | gradient × input | 0.8979 | 0.8639 | 0.1480 |
| Baseline | occlusion | 0.8979 | 0.8653 | 0.1390 |
| Reweighted | gradient × input | 0.9010 | 0.8639 | 0.1497 |
| Reweighted | occlusion | 0.9010 | 0.8653 | 0.1497 |

## Why these numbers matter

The baseline looks parity-perfect on demographic parity (gap 0.0013) while its
equalized-odds gap is 0.1231, driven mostly by the false-positive-rate difference
(0.2595 for group 0 versus 0.1364 for group 1). Reweighting the groups moves the
false-positive rate for group 1 up and lowers the equalized-odds gap, but it also
separates the selection rates and costs accuracy. A report that shows only one
fairness metric can therefore reverse the recommendation.

The explanation result is a warning about interpreting a single attribution. Under
noise small enough to leave 331 of 360 predictions unchanged, the top feature still
changes about 14% of the time. High rank correlation is not a certificate of
faithfulness, and the two explanation methods share the same linear structure, so
their agreement is expected rather than independent confirmation.

## Threat-to-control mapping

| Threat | Control tested | Metric | Residual risk |
|---|---|---|---|
| Hidden subgroup harm | Subgroup TPR/FPR audit | Gaps with bootstrap intervals | Population summary hides individual harm |
| Single fairness metric | Two conflicting metrics | DP and EO gaps | Neither metric is universally appropriate |
| Optimizing one gap | Group reweighting | Accuracy and both gaps | Metric conflict and accuracy cost |
| Brittle explanation | Gaussian perturbation | Spearman, top-k, flip rate | One noise scale and one model family |
| Explanation leakage | Discussed, not measured | — | Attributions can expose feature values |
| Adversarial explanation | Discussed, not measured | — | Manipulation not tested in this lab |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Reweighted model identical to baseline | `sample_weight` not passed or all weights equal | Check per-group weights |
| Negative or empty subgroup | Wrong group mask or label encoding | Print group counts before metrics |
| TPR/FPR divide-by-zero | Subgroup has no positives or negatives | Report the count and skip the undefined cell |
| Flip rate is 0 | Comparing predictions instead of top features | Compare argmax attributions |
| Both fairness gaps move down together | Synthetic data or weighting changed | Verify the data seed and weighting formula |

## Rubric

| Item | Points |
|---|---:|
| Baseline and reweighted models with correct weights | 4 |
| Subgroup metrics and both gap definitions | 4 |
| Stratified bootstrap intervals | 2 |
| Gradient × input and occlusion implementations | 4 |
| Stability measurement and flip-rate definition | 3 |
| Trade-off interpretation and scoped limitations | 2 |
| Reproducible artifacts and manifest | 1 |

## Reflection questions

1. The baseline DP gap is 0.0013, but the EO gap is 0.1231. How can both be true
   at once, and which one would you show a regulator?
2. Reweighting lowers EO by raising both FPRs. Is that a fairness improvement?
   State the value judgment in your answer.
3. The EO intervals overlap. What can you claim about the improvement, and what
   would you need to claim more?
4. Mean Spearman is about 0.90, but the top feature flips in about 15% of
   prediction-preserved rows. Reconcile those two numbers.
5. Does stability establish that an explanation is faithful? Give a counterexample.
6. What could an adversary do to manipulate an explanation that isotropic
   Gaussian noise does not model?
7. Which fairness metric would you prioritize for a credit decision, and what
   would you disclose about the metrics you did not optimize?
8. What would you add to this audit before using the model in a real decision
   about people?
