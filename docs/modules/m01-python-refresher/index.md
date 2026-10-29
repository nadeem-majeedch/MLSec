---
title: Module 01 — Python, NumPy, pandas, and scikit-learn Refresher
---

# Module 01 — Python, NumPy, pandas, and scikit-learn Refresher

<a id="m01-start"></a>

**Level 1 · Foundations · 12 hours · Python basics recommended**

## Why this module exists

Most "security bugs" in machine-learning code are ordinary data bugs wearing a costume. A scaler is fitted before the train/test split. A feature is silently cast from float to integer. A join multiplies rows. A metric is computed on the wrong axis. The model still trains, the number still looks plausible, and the report is still wrong.

This module rebuilds the four tools you will use in every Level 1 lab: Python for structure, NumPy for numerical arrays, pandas for tabular data, and scikit-learn for models and evaluation. The goal is not to memorize APIs. It is to recognize when a result is structurally untrustworthy.

If you already write this code comfortably, take the [diagnostic](#diagnostic), skim the lessons, and go to LAB-01. If not, work through every example. The examples are short by design: you are meant to run them and change them.

## Real-world motivation

In 2023, a widely shared "97% accurate" student project turned out to scale its features before splitting the data. The leakage inflated the score by several points. Nobody had written an attack. The bug was a two-line ordering mistake that a reviewer could have caught by asking one question: *which rows did the scaler see?*

Security work inherits this problem and makes it worse. If you cannot trust your baseline, you cannot measure an attack. An attack success rate computed on a leaky pipeline is meaningless, and a defense evaluated against a broken baseline is worse than no evaluation.

## Measurable learning objectives

By the end of this module you will be able to:

1. **Write** small, testable Python functions with explicit inputs, outputs, and error handling, and explain why mutable defaults and silent type changes cause bugs (Bloom 3).
2. **Use** NumPy arrays correctly: inspect shape and dtype, apply broadcasting, compute reductions along a stated axis, and generate reproducible random numbers (Bloom 3).
3. **Clean and transform** a tabular dataset with pandas, including missing values, duplicates, joins, and grouped summaries, while preserving an audit trail (Bloom 3).
4. **Build** a scikit-learn `Pipeline` that keeps preprocessing inside cross-validation, and compute classification metrics with stated definitions (Bloom 3).
5. **Make** a run produce identical results on a second run, using seeds, pinned versions, saved splits, and a manifest (Bloom 3–4).

## Prerequisite checklist

| Skill | Check | If not |
|---|---|---|
| Run Python scripts and use a terminal | `python --version` works | Student guide, setup section |
| Variables, lists, dictionaries, loops | Read a 30-line script | Lesson 01.1 |
| Functions and imports | Write a function that returns a value | Lesson 01.1 |
| Basic statistics | Mean, median, percentage | Any introductory statistics resource |
| Linear algebra (helpful) | Vector, matrix, dot product | Lesson 01.2; revisit before M02 |
| No GPU or paid account | — | You are in the right place |

<a id="diagnostic"></a>

### Five-minute diagnostic

Without copying a tutorial, can you:

1. Load a CSV into a pandas `DataFrame` and print its shape and missing-value count?
2. Split it into train and test sets with a fixed seed?
3. Fit a `StandardScaler` and a logistic regression inside a `Pipeline`?
4. Compute accuracy, macro F1, and a confusion matrix?
5. Explain why fitting the scaler before the split is a bug?

If all five are comfortable, skim Lessons 01.1–01.5 and spend the time on LAB-01. If any is not, complete the module in order.

## Module map

| Unit | Title | Time | What you produce |
|---|---|---:|---|
| [01.1](lesson-1-python-for-security-work.md) | Python for security work | 1.5 h | A tested input-validation function |
| [01.2](lesson-2-numpy.md) | NumPy: arrays, shapes, and reproducibility | 1.5 h | A vectorized metric with shape checks |
| [01.3](lesson-3-pandas.md) | pandas: cleaning without lying | 1.5 h | An audit trail for a messy table |
| [01.4](lesson-4-scikit-learn.md) | scikit-learn: pipelines and honest evaluation | 1.5 h | A leak-free baseline pipeline |
| [01.5](lesson-5-reproducibility.md) | Reproducibility and experiment hygiene | 1.5 h | A manifest and a rerun proof |
| [LAB-01](../../labs/lab-01.md) | Reproducible environment and baseline pipeline | 3 h | Model, metrics, manifest |
| [Knowledge check](quiz.md) | QZ-01, 10 items | 20 min | Score and explanations |
| [Exercises](exercises.md) | Four exercises, one scenario | 60 min | Portfolio evidence |

Module effort includes the lab; the lesson times are reading and guided practice. Sum: 7.5 h lessons + 3 h lab + 1.5 h quiz and exercises ≈ 12 h.

## How the four tools divide the work

| Tool | Strength | Typical use in this course | Failure mode to watch |
|---|---|---|---|
| Python | Structure, control flow, files, tests | Glue code, validation, artifact writing | Silent type coercion, mutable defaults |
| NumPy | Fast homogeneous arrays | Model inputs, perturbations, metrics | Shape and axis mistakes, dtype overflow |
| pandas | Labeled tabular data | Loading, cleaning, joins, audits | Silent row multiplication, index misalignment |
| scikit-learn | Consistent model API | Baselines, pipelines, metrics, splits | Preprocessing leakage, wrong metric |

```mermaid
flowchart LR
    A[Raw CSV or array] --> B[pandas: inspect and clean]
    B --> C[NumPy: numeric arrays]
    C --> D[scikit-learn: split, fit, predict]
    D --> E[Metrics and artifact]
    E --> F[Manifest and report]
```

## Common mistakes across the module

| Mistake | Symptom | Consequence |
|---|---|---|
| Fitting preprocessing on all data | Cross-validation score is too high | Leakage; attack/defense results are invalid |
| Using `np.mean` on the wrong axis | One number where you expected one per class | Metrics look plausible but are wrong |
| Ignoring the pandas index after filtering | Joins or assignments attach to the wrong rows | Silent data corruption |
| Treating `float32` and `float64` as interchangeable | Small numerical differences; failed equality tests | Reproducibility and comparison problems |
| Relying on a global seed without passing it | Results change when code is reordered | Unreproducible experiments |
| Reporting a single number without a denominator | "95% success" with no base set | Uninterpretable claim |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ValueError: shapes ... not aligned` | Wrong axis or operand order | Print `.shape` for every operand and state the intended output shape first |
| Array values wrap or turn negative | Integer dtype overflow | Cast to `float32` or `float64` before arithmetic |
| Test score much higher than validation | Preprocessing was fitted before the split | Move the scaler into a `Pipeline` |
| A join multiplies rows | Duplicate keys on the right side | Check `duplicated`, then use `validate="many_to_one"` |
| Metrics differ from a reference | Different averaging, threshold, or zero-division rule | State `average`, `zero_division`, and the threshold next to the number |
| A rerun produces new numbers | Unseeded randomness or unordered iteration | Seed the generator, sort keys, save the split indices |

Per-tool fixes are in the troubleshooting section of [Lesson 01.2](lesson-2-numpy.md#troubleshooting), [Lesson 01.3](lesson-3-pandas.md#troubleshooting), and [Lesson 01.4](lesson-4-scikit-learn.md#troubleshooting).

## Glossary

| Term | Definition |
|---|---|
| **Array** | A fixed-type, fixed-shape block of numbers, indexed from zero |
| **Shape** | The length of each dimension, e.g. `(1000, 64)` |
| **dtype** | The element type, e.g. `float32`, `int64`, `object` |
| **Broadcasting** | NumPy's rules for combining arrays of different shapes |
| **Axis** | The dimension along which a reduction is applied |
| **DataFrame** | A labeled, two-dimensional table in pandas |
| **Index** | The row labels of a `DataFrame` or `Series` |
| **Estimator** | An object with `fit`, and usually `predict` or `transform` |
| **Transformer** | An estimator with `fit` and `transform` |
| **Pipeline** | A chain of transformers ending in an estimator |
| **Leakage** | Information from outside the training fold influencing training or evaluation |
| **Seed** | A value that initializes a pseudorandom generator |
| **Manifest** | A file recording artifact names, sizes, and hashes |

## Summary and key takeaways

- The four tools have different failure modes; knowing the tool is knowing its failure mode.
- **Shape, dtype, index, and seed** are the four things to check first when a result looks wrong.
- Preprocessing belongs inside a pipeline so it is fitted only on training folds.
- A metric without a denominator, threshold, and base set is not a result.
- Reproducibility is a design choice: save the split, pass the seed, pin the versions, hash the output.

## References and further reading

All links checked on 2026-10-28.

| Reference | Use |
|---|---|
| [Python tutorial](https://docs.python.org/3/tutorial/) | Language refresher |
| [NumPy user guide](https://numpy.org/doc/stable/user/) | Arrays, broadcasting, random generation |
| [pandas user guide](https://pandas.pydata.org/docs/user_guide/) | Indexing, joins, missing data |
| [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html) | Estimators, pipelines, model selection |
| [scikit-learn `Pipeline`](https://scikit-learn.org/stable/modules/compose.html) | Leak-free preprocessing |
| [scikit-learn metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) | Metric definitions |
| [NumPy random generator](https://numpy.org/doc/stable/reference/random/generator.html) | Modern reproducible RNG |

## Next step

Start with [Lesson 01.1 — Python for security work](lesson-1-python-for-security-work.md). If you are already comfortable, take the diagnostic and go directly to [LAB-01](../../labs/lab-01.md).
