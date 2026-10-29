# Module 13 Alternate Quiz (QZ-13B)

| Field | Value |
|---|---|
| Module | M13 — Privacy-Preserving Machine Learning and Differential Privacy |
| Quiz A | [QZ-13](../../modules/m13-privacy-preserving-ml/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-19 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-13b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Noise scale

For the Laplace mechanism, which quantity determines the noise scale?

A. The number of features only  
B. The sensitivity divided by ε  
C. The number of rows only  
D. The model's accuracy

## 2. What ε bounds

In differential privacy, ε bounds:

A. The maximum accuracy loss on the test set  
B. How much the output distribution can change when one neighboring record changes  
C. The number of queries a user may make  
D. The size of the model

## 3. Poisoning protection

True or false: differential privacy protects a federated model against a malicious client poisoning the global update.

## 4. Sequential composition

True or false: under basic sequential composition, the ε values of queries released over the same data add.

## 5. Reporting ε

Name three facts that must accompany a reported ε before the number can be interpreted.

## 6. Mean sensitivity

A release computes the mean of 500 rows with 4 features. Each feature is clipped to $[-1, 1]$.

Compute the L1 sensitivity of the mean vector and the Laplace scale for ε = 0.4. Show the arithmetic.

## 7. Find the flaw

The code below is described as an ε = 0.5 differentially private mean.

```python
mean = X.mean(axis=0)
noisy = mean + np.random.laplace(0, 1.0 / 0.5, size=mean.shape)
released = np.clip(noisy, -2.5, 2.5)
return released
```

Identify two flaws and explain why the stated ε is not established.

## 8. Scenario: the dashboard release

A team wants to publish summary statistics from a local, synthetic dataset: a mean, two counts, and a histogram.

Outline a bounded DP design: the neighboring relation, clipping and sensitivity, how ε and δ are chosen and composed across releases, one utility measurement, and two limits of the privacy claim. Do not use real personal data.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can state a DP claim that another person could audit. |
| 10 | Pass. Review the missed item before LAB-17. |
| 8–9 | Reread M13.L2 and L3, especially sensitivity and composition. |
| Below 8 | Reread M13 and rerun LAB-17 with a written budget first. |
