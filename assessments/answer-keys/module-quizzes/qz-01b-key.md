# QZ-01B Answer Key — Module 01

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. C — a Series with index `[0, 1, 2, 3]` and values `[NaN, 21, 32, NaN]`

pandas aligns on the index union. Index 0 exists only in `s1` (10 + missing = NaN), index 3 exists only in `s2` (missing + 3 = NaN), and indices 1 and 2 add normally. Because NaN is a float, the result is float-valued.

- **A** assumes positional addition and ignores the index.
- **B** shows the right values but as a plain list with a fabricated fourth element; the actual result is a Series.
- **D** is false; pandas does not raise on misaligned indices, which is exactly the danger.

Tag: M01 · LO-01 · Bloom 3 · D2.

## 2. B — preserve label proportions

Stratification makes each split's class distribution approximate the full dataset's. It is important for small or imbalanced data, where a random split can put too few positives in the test set.

- **A** describes sorting, which is not what `stratify` does.
- **C** is controlled by `test_size`, not stratification.
- **D** is `drop_duplicates`.

Tag: M01 · LO-01 · Bloom 2 · D1.

## 3. True

With `subset=None`, `drop_duplicates` compares all columns. `keep="first"` is the default, so the first occurrence is retained. If duplicates are defined by a key such as `customer_id`, pass `subset=["customer_id"]` explicitly and state which row is kept.

Tag: M01 · LO-01 · Bloom 2 · D1.

## 4. True

Fitting the pipeline on training rows means the imputer, scaler, and any other learned transform see only training data. Calling `predict` on test rows applies those frozen statistics. Leakage returns if you call `fit` or `fit_transform` on the test rows, or fit on the combined dataset before splitting.

Tag: M01 · LO-01 · Bloom 2 · D1.

## 5. Required elements (two)

- A saved split is a fixed evaluation set: every run, model, and report uses the same rows, so comparisons are like-for-like.
- Re-calling the splitter can produce different rows when the library version, row order, or arguments change, even with the same seed.
- Saved indices let another person audit exactly which rows were evaluated and reproduce a headline number.
- They make leakage and overlap checks possible after the fact.

Tag: M01 · LO-28 · Bloom 3 · D2.

## 6. Training: 1,600 rows, 160 positives; test: 400 rows, 40 positives

Total positives: $2{,}000 \times 0.10 = 200$.

Training split: $2{,}000 \times 0.80 = 1{,}600$ rows, of which $200 \times 0.80 = 160$ are positive.

Test split: $2{,}000 \times 0.20 = 400$ rows, of which $200 \times 0.20 = 40$ are positive.

Stratification preserves the 10% rate in both splits.

Tag: M01 · LO-01 · Bloom 2 · D1.

## 7. Flaw: the scaler is fitted on the test set

`StandardScaler().fit(X_test)` learns the test mean and variance, then applies them to the training rows. The training transform now depends on the evaluation data, which is pipeline leakage and can make the reported result optimistic. It also means the scaler is not centered on the training distribution, which is what deployment will use.

Correct line:

```python
scaler = StandardScaler().fit(X_train)
```

Then transform both `X_train` and `X_test`.

Tag: M01 · LO-01 · Bloom 3 · D2.

## 8. Required elements (three, each with what it reveals)

- **Remove the label from `X` and rerun.** If accuracy collapses, the model was reading the answer; this is target leakage.
- **Check duplicate and near-duplicate rows, and whether groups (customers, patients, devices) cross the split.** A random row split can put the same entity on both sides, inflating the score.
- **Check the class balance and a trivial baseline.** With a rare positive class, 0.999 accuracy may reflect the base rate rather than skill.
- **Inspect the split and preprocessing for leakage** (scaling, imputation, feature selection fitted before the split). Any learned transform fitted on all rows is suspect.
- **Ask for a confidence interval and the exact split hash.** A single 0.999 is not a distribution.

Three checks with a plausible reveal earn the 3 points. A list of three generic "check for overfitting" answers earns at most 1.

Tag: M02 · LO-01 · Bloom 4 · D3.
