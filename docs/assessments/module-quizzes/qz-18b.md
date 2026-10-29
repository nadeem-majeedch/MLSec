# Module 18 Alternate Quiz (QZ-18B)

| Field | Value |
|---|---|
| Module | M18 — Capstone, Synthesis, and Research |
| Quiz A | [QZ-18](../../modules/m18-capstone-and-research/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-35 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-18b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. A falsifiable question

Which is a falsifiable capstone question?

A. "Is AI security important for society?"  
B. "Does input squeezing reduce PGD success at ε = 0.03 by at least 20 percentage points on a frozen 500-row base set without lowering clean accuracy by more than 2 points?"  
C. "An exploration of adversarial defenses."  
D. "How can we make models robust?"

## 2. A researchable gap

What makes a gap statement researchable rather than a topic?

A. It names a specific missing comparison or measurement, with a population and a condition  
B. It cites a well-known paper  
C. It says that nobody has studied the area  
D. It is broad enough to cover several fields

## 3. Negative results

True or false: a negative result with a stated confidence bound is weaker evidence than no result at all.

## 4. Analysis plans

True or false: a pre-registration-style analysis plan may be revised after seeing results and still be reported as confirmatory without disclosure.

## 5. Adaptive evaluation

Why must a capstone defense claim include an adaptive attack? Answer in one or two sentences.

## 6. Seed arithmetic

A defense is evaluated with three seeds: ASR = 0.28, 0.35, and 0.44. The undefended baseline is 0.52 from a single seed.

Compute the mean and range of the defended results. State one conclusion the numbers support and one they do not.

## 7. Find the flaw

The evaluation script below is offered as the reproduction package for a capstone result.

```python
model = joblib.load("model.joblib")
X_test = pd.read_csv("data/test.csv")
asr = evaluate(model, X_test)
print(asr)
```

Identify two reproducibility flaws and explain what another learner would be unable to establish.

## 8. Scenario: from assessment to question

You have completed a local assessment showing that a detector's recall falls when an attacker slows its query rate. Turn this into a bounded research question: state the gap, one claim–evidence pair, one control or ablation, and the scope and ethics limits. Do not propose testing a third-party system.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can turn an assessment into a testable research plan. |
| 10 | Pass. Review the missed item before the capstone proposal. |
| 8–9 | Reread M18.L2 and L3, especially gaps and claim–evidence tables. |
| Below 8 | Reread M18 and rewrite the research question using the six tests. |
