# Module 12 Alternate Quiz (QZ-12B)

| Field | Value |
|---|---|
| Module | M12 — Federated Learning: Architecture, Threats, and Defenses |
| Quiz A | [QZ-12](../../modules/m12-federated-learning/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-24 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-12b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. What FedAvg aggregates

In a FedAvg round, how does the coordinator combine client updates?

A. It averages them, weighted by each client's sample count  
B. It picks the update with the largest norm  
C. It trains a fresh model on the raw data it receives  
D. It counts clients and ignores the update values

## 2. Krum's selection rule

Which statement describes Krum?

A. It selects the update closest to its neighbors under a distance measure  
B. It removes the largest value in each coordinate  
C. It averages every update after clipping  
D. It requires the number of clients to equal the number of attackers

## 3. Clipping effects

True or false: norm clipping can reduce a malicious update's influence while leaving attack success above the benign baseline.

## 4. More rounds

True or false: increasing the number of federated rounds always improves robustness to poisoning.

## 5. Fair comparison

Why must two aggregation defenses be compared at the same number of rounds and the same attacker budget? Answer in one or two sentences.

## 6. Weighted mean

Three clients hold 100, 400, and 500 rows. Their two-coordinate updates are $(0.1, 0.2)$, $(-0.3, 0.4)$, and $(0.5, -0.2)$.

Compute the sample-weighted mean update. Show the numerator and denominator for each coordinate.

## 7. Find the flaw

The code below is meant to bound each client's influence before aggregation.

```python
updates = [client.update() for client in clients]
mean = np.mean(updates, axis=0)
bounded = np.clip(mean, -1.0, 1.0)
return bounded
```

Identify two flaws and explain why a client that scales its update by 20 can still dominate the result.

## 8. Scenario: the aggregator trial

You are evaluating two aggregation defenses for a local federated simulation with synthetic data. One defense is coordinate-wise trimming and the other is norm clipping.

Outline the trial: threat model, controls, metrics, comparison conditions, and two residual risks. Do not use real client data or test a production federation.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can evaluate an aggregator under equal conditions. |
| 10 | Pass. Review the missed item before LAB-16. |
| 8–9 | Reread M12.L2–L4, especially influence and aggregation assumptions. |
| Below 8 | Reread M12 and rerun LAB-16 with a prediction recorded first. |
