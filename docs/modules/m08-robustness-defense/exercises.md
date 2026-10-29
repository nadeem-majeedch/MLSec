---
title: Module 08 Exercises
---

# Module 08 Exercises

**Four exercises · about 50 minutes · one scenario**

These exercises test interpretation and reporting, not code copying. A calculator or a short Python session is enough. Keep your numbers and reasoning together so a reviewer can follow them.

---

## Exercise 1 — Read the defense table (10 minutes)

LAB-11 measured three systems on the same 540-row test set:

| Model | Clean acc. | Robust acc. ε=0.10 | ASR ε=0.10 | Robust acc. ε=0.20 | ASR ε=0.20 |
|---|---:|---:|---:|---:|---:|
| Undefended | 0.9667 | 0.6204 | 0.3582 | 0.0407 | 0.9579 |
| Adversarial training | 0.8907 | 0.7296 | 0.1809 | 0.3537 | 0.6029 |
| Input squeezing | 0.9500 | 0.7722 | 0.1871 | 0.0019 | 0.9981 (adaptive) |

1. For adversarial training, compute the clean-accuracy cost and the robust-accuracy gain in percentage points.
2. For squeezing, compute the same two quantities at ε = 0.10. Why is comparing them with adversarial training misleading without the stress column?
3. Compute the relative ASR reduction for each defense at ε = 0.10: \((0.3582 - \text{ASR}) / 0.3582\).
4. Rank the three systems at each budget. Does the ranking change? What does that imply for a one-budget report?
5. A colleague says "squeezing is the best defense because its robust accuracy is highest." Give two corrections.

---

## Exercise 2 — Detector precision and operating cost (12 minutes)

A team proposes a feature-squeezing detector in front of a document classifier. On a validation set, the detector flags 85% of attacked inputs and 2% of benign inputs. The security team estimates that 0.2% of production inputs will be attacked.

1. Compute precision at base rates \(\pi = 0.2\%\), \(1\%\), and \(10\%\), using

$$
\text{precision} = \frac{\text{TPR}\cdot\pi}{\text{TPR}\cdot\pi + \text{FPR}\cdot(1-\pi)}.
$$

2. At \(\pi = 0.2\%\), how many alerts arrive per true attack? Use 100,000 inputs and show the counts.
3. A flagged document is routed to a human reviewer who takes four minutes. At 0.2% prevalence and 100,000 documents per day, how many review minutes per day does the detector create? How many of those minutes concern real attacks?
4. Name two ways the team could reduce the operational burden without pretending the detector is perfect.
5. What would you measure to test whether an attacker can evade the detector adaptively?

---

## Exercise 3 — Scenario: the AegisShield claim (15 minutes)

A vendor offers a preprocessing module called AegisShield for an insurance-document classifier. The module quantizes and denoises uploads before classification. The vendor's evaluation states:

> "AegisShield improves robustness from 61% to 99.1%. Attack success falls to 0.4%. We evaluated with 3-step PGD at ε = 0.03, one restart, on the full test set. The attack does not know the preprocessing parameters."

Your deployment accepts uploads from external claimants, and the model's decision affects claim prioritization. A wrong prioritization is costly but reversible; a denial of legitimate claims is also costly.

1. Apply the pitfalls checklist from Lesson 08.4. Identify at least five problems with the evaluation as described.
2. The vendor says the preprocessing parameters are secret. Explain why this is not a security boundary, and what an attacker with API access can still do.
3. Design the adaptive attack you would run. State the attacker's knowledge, the technique for the quantizer, the budget, and the success criterion.
4. Write four questions you would send the vendor before a pilot. At least one must concern clean utility.
5. Assume the vendor's module does what it claims at ε = 0.03. Recommend a deployment posture: what to enable, what to monitor, and what residual risk to accept. Name one operational cost.
6. Write a six-sentence memo with finding, evidence, impact, limitation, recommendation, and owner/review date. Do not call the system secure.

---

## Exercise 4 — Turn numbers into a scoped claim (13 minutes)

A held-out evaluation of a four-class model returns:

- \(N = 1{,}000\) test rows;
- \(C = 940\) clean-correct rows;
- at ε = 0.05, the attack changes 235 of the 940 predictions;
- at ε = 0.15, the attack changes 590 of the same base rows;
- the defended model's clean accuracy is 0.9400, against 0.9667 for the undefended model on the same split;
- the attack is 20-step PGD with 2 restarts, white-box, L∞;
- no adaptive attack was run.

1. Compute clean accuracy, ASR, and robust accuracy at ε = 0.05.
2. Compute ASR and robust accuracy at ε = 0.15. What happens to the base set, and why does it stay 940?
3. Write the scoped claim in the Lesson 1 template. Include the cost and the boundary.
4. State two limitations that the evaluation itself creates, beyond "the model might be different in production."
5. Write one falsification condition and one monitoring signal that would tell you the claim no longer holds.
6. A product manager asks: "So is 0.05 safe?" Answer in two sentences without using the word "robust" as an adjective.

---

## Self-assessment

| Criterion | Check |
|---|---|
| Every rate shows its denominator | [ ] |
| Costs and gains are reported together | [ ] |
| The stress budget appears in the analysis, not only the table | [ ] |
| Detector precision is computed at a stated base rate | [ ] |
| Adaptive attacks are designed, not merely mentioned | [ ] |
| The memo has a recommendation, an owner, and a review date | [ ] |
| No conclusion claims universal robustness from one experiment | [ ] |

Worked answers: [exercise-solutions.md](exercise-solutions.md).
