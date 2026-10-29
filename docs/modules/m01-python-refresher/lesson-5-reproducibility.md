# Lesson 01.5 — Reproducibility and Experiment Hygiene

**Module 01 · 1.5 hours · Complete Lessons 01.1–01.4 first**

## Scenario

A learner reports that their attack lowers accuracy from 96.9% to 41.2%. A colleague tries to reproduce it and gets 96.9% to 44.8%. The difference is larger than the effect of the defense they are arguing about. The code has a seed for the train/test split but not for the attack; the model is reloaded from a file with no recorded version; and the test set was regenerated with a different library version.

Neither number is wrong. Neither number is evidence either. Reproducibility is the control that turns a run into a result.

## Learning objectives

By the end of this lesson you will be able to:

1. Identify the sources of nondeterminism in a Python ML experiment.
2. Use seeds, saved splits, and pinned versions to make a run repeatable.
3. Write a configuration file and an artifact manifest for a run.
4. Distinguish "same machine, same environment" reproducibility from cross-platform reproducibility.
5. Keep an experiment log that another person can follow.

## What changes between runs

| Source | Example | Control |
|---|---|---|
| Random initialization | Model weights, random forest splits | Pass `random_state`; save the fitted model |
| Data splitting | `train_test_split` without a seed | Pass `random_state`; save the indices |
| Sampling | Bootstraps, negative sampling, mini-batches | Seed a dedicated generator |
| Library version | Solver defaults, metric definitions | Pin versions; record them |
| Hardware and BLAS | Floating-point summation order, threads | Record hardware; use tolerances |
| Data version | A silent dataset update | Record checksum and source |
| Code version | An uncommitted edit | Record a local commit hash or file hashes |
| Environment | Different OS, Python, wheels | Ship a lockfile; test on the reference platform |

The first four are usually fixable exactly. The last four may only be reproducible within a tolerance. State which kind of reproducibility you are claiming.

## A repeatable run in code

```python
import hashlib
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def run(seed):
    X, y = load_digits(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=seed
    )
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(max_iter=5000, random_state=42)),
    ])
    pipe.fit(X_train, y_train)
    predictions = pipe.predict(X_test)
    digest = hashlib.sha256(predictions.tobytes()).hexdigest()[:16]
    return len(X_train), len(X_test), digest


print(run(42))
print(run(42))
print(run(43))
```

Expected output with scikit-learn 1.9.0:

```text
(1437, 360, '07712188bf16e52f')
(1437, 360, '07712188bf16e52f')
(1437, 360, 'd5e3a95f05a8c2a6')
```

The first two runs match exactly: same seed, same environment, same code. The third changes the split and produces a different prediction digest. That is expected. A changed result is not a failure; an **unexplained** changed result is.

The digest is a quick fingerprint of the prediction vector. It does not prove the model is good. It proves the outputs are identical.

## Save the split, not just the seed

A seed reproduces a split only if the data, library, and code are identical. A stronger control is to save the row indices:

```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

X, y = load_digits(return_X_y=True)
indices = np.arange(len(y))
train_idx, test_idx = train_test_split(
    indices, test_size=0.2, stratify=y, random_state=42
)
np.save("train_indices.npy", train_idx)
np.save("test_indices.npy", test_idx)
print(train_idx.shape, test_idx.shape)
print(test_idx[:10])
```

Expected output (the exact indices depend on the scikit-learn version):

```text
(1437,) (360,)
[ 618 1427  158 1256 1079  648 1773 1531 1063  781]
```

Later labs load these arrays and assert that the same rows are used. If a library upgrade changes the splitter, the saved indices still define the evaluation set. The seed is a convenience; the indices are the contract.

## Configuration and manifest

Keep the run parameters in a file, not scattered through the notebook:

```json
{
  "seed": 42,
  "test_size": 0.2,
  "stratify": true,
  "model": "logreg",
  "max_iter": 5000,
  "dataset": "sklearn.digits",
  "n_samples": 1797
}
```

Then write a manifest after the run:

```json
{
  "run_id": "lab01-2026-10-28-a",
  "python": "3.14.7",
  "scikit_learn": "1.9.0",
  "numpy": "2.5.2",
  "config_sha256": "...",
  "files": {
    "model.joblib": "...",
    "metrics.json": "...",
    "predictions.npy": "...",
    "test_indices.npy": "..."
  }
}
```

The manifest answers "what was in this run?" without opening every file. It does not answer "is this run correct?" That is what the metrics and the report are for.

## The experiment log

For each run, record:

```text
Date/time:
Run ID:
Question:
Prediction before running:
Config (or hash):
Command:
Result (headline metric):
Surprise or failure:
Next test:
```

The prediction line is not optional. A prediction that turns out wrong is the most informative entry in the log, because it exposes the mental model that needs correcting.

## Determinism is not portability

Two claims are often confused:

| Claim | Meaning | How to support it |
|---|---|---|
| **Repeatable** | Same machine, same environment, same seed gives the same result | Save code, config, versions, split |
| **Portable** | A different machine or library version gives the same result within tolerance | Publish tolerances; test on a second platform |

Floating-point operations are not associative. Different BLAS libraries, thread counts, or CPU instructions can change the last digits. A model's predictions usually survive, but a threshold comparison near 0.5 can flip. For attack experiments, a flipped prediction changes the success count. Report a tolerance and the number of examples, or fix the environment.

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Seeding only the split | Attack or model still varies | Seed every randomized component |
| Setting a global seed after the split | The early operations are unseeded | Set seeds at the start; pass explicitly |
| Saving predictions without indices | Cannot map predictions back to rows | Save the indices |
| Recording versions in prose | They drift and cannot be checked | Write them into the manifest |
| Re-running the notebook out of order | Hidden state changes results | Restart and run all |
| Comparing runs across library versions without saying so | Difference may be version, not treatment | State versions and tolerance |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Same seed, different results | Unseeded component or thread nondeterminism | Audit every random call; set thread counts |
| Results differ only on another machine | BLAS or floating-point ordering | Report tolerance; test on a second platform |
| Model reload gives different predictions | Preprocessing not saved | Save the pipeline, not the estimator alone |
| Hash changes although accuracy is identical | File metadata or row order changed | Hash the array bytes, not the file wrapper |
| Split indices differ after upgrade | Splitter implementation changed | Load saved indices instead of regenerating |

## Key terms

**Seed**, **determinism**, **repeatability**, **portability**, **split indices**, **configuration**, **manifest**, **run ID**, **lockfile**, **tolerance**, **nondeterminism**.

## Summary

- Reproducibility is designed, not hoped for: seed every component, save the split, pin versions.
- A prediction digest is a fast equality check; saved indices are the durable contract.
- Record config, command, versions, and result in one run record.
- Claim "repeatable" and "portable" separately; floating point is not associative.
- A wrong prediction in the log is useful evidence, not a failure.

## References

| Reference | Use |
|---|---|
| [scikit-learn reproducibility](https://scikit-learn.org/stable/common_pitfalls.html) | Common sources of nondeterminism |
| [`random_state` glossary](https://scikit-learn.org/stable/glossary.html#term-random_state) | How seeds are handled |
| [NumPy random generator](https://numpy.org/doc/stable/reference/random/generator.html) | Independent generators |
| [Python `hashlib`](https://docs.python.org/3/library/hashlib.html) | Digests for artifacts |
| [pip requirements files](https://pip.pypa.io/en/stable/reference/requirements-file-format/) | Pinning versions |

Next: complete [LAB-01](../../labs/lab-01.md), the [knowledge check](quiz.md), and the [exercises](exercises.md).
