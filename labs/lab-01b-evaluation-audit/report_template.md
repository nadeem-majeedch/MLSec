# LAB-01B Report Template

Replace the prompts with your results. Keep the headings; the checker looks for them.

## Threat model

- Asset: the integrity of the reported churn metric and the decision it informs.
- Adversary: a validity failure, not a remote attacker — a post-outcome feature, repeated customers across a random split, or preprocessing fitted on evaluation data.
- Success criterion: a repaired estimate that a second person can reproduce and that does not depend on leakage.

## Data audit

- Rows, unique customers, churn rate.
- Exact duplicate rows and missing values, with counts.
- The suspect feature: how well it predicts the label, its univariate AUC, and why it is unavailable at scoring time.
- Random-split customer overlap: how many customers appear on both sides.

## Results

- Leaky baseline: split protocol, leakage sources, accuracy and ROC-AUC.
- Repaired model: deduplication, customer-grouped split sizes, features removed, threshold rule.
- Test accuracy, precision, recall, F1, ROC-AUC, and PR-AUC at the stated threshold.
- Bootstrap 95% intervals for recall and precision.
- Grouped cross-validation PR-AUC, mean and spread.

## Limitations

- What the synthetic data cannot show.
- Why the repaired model is a baseline, not a deployment candidate.
- Which leakage families are discussed but cannot be measured here (for example, temporal drift without dates).

## Reproduction

- Command to regenerate the artifacts.
- Command to run the checker.
- What the manifest and the dataset hash verify.
