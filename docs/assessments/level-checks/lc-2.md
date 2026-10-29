# Level 2 Check — Core Attacks (LC-2)

| Field | Value |
|---|---|
| Level | 2 — Core attacks |
| Modules | M04–M07 |
| Items | 10 |
| Points | 20 |
| Time guide | 30 minutes |
| Pass | 16/20 |
| Outcomes | LO-05, LO-06, LO-08, LO-10, LO-11, LO-13, LO-14 |
| Answer key | Separate file: `assessments/answer-keys/level-checks/lc-2-key.md` |

Answer without notes. Items 1–6 are worth 1 point, items 7–8 are worth 2 points, and items 9–10 are worth 5 points. Show denominators in every calculation.

## 1. Zero budget (1 point)

A correct untargeted FGSM implementation at ε = 0 should produce which attack success rate?

A. 0  
B. 0.5  
C. 1  
D. It is undefined

## 2. Poison rate (1 point)

A clean training set has 1,600 rows. An attacker appends 40 poisoned rows. What is the poison rate against the clean set?

A. 2.5%  
B. 2.44%  
C. 40%  
D. 4.0%

## 3. Backdoor effect (1 point)

The clean model sends 0.12 of triggered source rows to the target class. The backdoored model sends 0.88. What is the attack effect?

A. 88 percentage points  
B. 12 percentage points  
C. 76 percentage points  
D. 100 percentage points

## 4. Privacy metric (1 point)

Which metric is most directly relevant to privacy harm from membership inference?

A. TPR at FPR ≤ 1%  
B. Overall accuracy of the membership classifier  
C. Training loss  
D. Number of model parameters

## 5. Transfer (1 point)

True or false: a transfer attack requires gradients through the target model.

## 6. Fidelity (1 point)

True or false: high fidelity to the teacher proves that the attacker obtained the training data.

## 7. ASR and robust accuracy (2 points)

Explain the difference between attack success rate and robust accuracy. State the denominator each uses and why both can be reported in the same experiment.

## 8. Poisoning and backdoors (2 points)

Distinguish poisoning from a backdoor in one sentence each. Then state one baseline that each evaluation needs.

## 9. Scenario: three budgets (5 points)

Design an evasion evaluation for a local speech-command classifier at ε = 0.01, 0.03, and 0.06. Name the attack configuration, base set, metrics, clean or random baseline, one adaptive check, and two limits of the result.

## 10. Scenario: the opaque vendor model (5 points)

A vendor supplies a compiled keyword-spotting model with no training data. You may run it locally on synthetic audio.

Design a bounded two-part test for (a) a backdoor and (b) membership inference. For each, name one baseline and one limit. State two conclusions the test cannot support, even if both tests are negative.

## Scoring

| Score | Interpretation |
|---:|---|
| 18–20 | Strong. You can execute and scope attack evaluations. |
| 16–17 | Pass. Review the missed item and the linked lab. |
| 12–15 | Not yet. Rerun the relevant labs before Level 3. |
| Below 12 | Reread M04–M07 and rebuild the metrics and baselines. |
