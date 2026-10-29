# LAB-01 Report Template

Replace the prompts with your results. Keep the headings; the checker looks for them.

## Threat model

- Asset: the integrity of the reported metric and the saved model artifact.
- Adversary: a change that makes the metric irreproducible or optimistic (unseeded split, leakage, stale artifact).
- Success criterion: a second person reproduces the headline metric from the saved split and model.

## Setup

- Data: `load_digits`, number of samples, features, classes.
- Split: strategy, sizes, seed, saved indices.
- Model: preprocessing and classifier, hyperparameters.
- Environment: Python and package versions.

## Results

- Validation accuracy and macro F1.
- Test accuracy and macro F1.
- Per-class recall and the confusion matrix.
- One sentence comparing validation and test.

## Limitations

- What the random split cannot show.
- What the clean dataset does not represent.
- What depends on the pinned environment.

## Reproduction

- Command to regenerate the artifacts.
- Command to run the checker.
- What the manifest verifies.
