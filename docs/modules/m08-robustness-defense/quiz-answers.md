# Answer Key — QZ-08

**Module 08 · 10 items · 14 points**

Use this key after attempting the quiz. For calculation items, the reasoning and denominators matter as much as the final number.

## 1. (1 point) A — Model, adversary, norm and budget, base set, metric

A robustness claim names what was tested, against whom, at what size of change, on which rows, and how success was counted. Without any one of these, the number cannot be compared or reproduced.

## 2. (2 points) Clean 0.90; ASR 0.25; robust accuracy 0.675

$$
\text{clean accuracy} = \frac{180}{200} = 0.90
$$

$$
\text{ASR} = \frac{45}{180} = 0.25
$$

$$
\text{robust accuracy} = \frac{180-45}{200} = \frac{135}{200} = 0.675
$$

Award 1 point for the three correct values, 1 point for the correct denominators (200 for accuracy, 180 for ASR). ASR uses the clean-correct set; robust accuracy uses all rows. The identity \(135 = 180 - 45\) closes.

## 3. (1 point) B — ASR denominators differ

Each model's ASR is computed over its own clean-correct rows (522 and 481). That is the right definition, but it means the rates are not computed on the same population. Robust accuracy is computed over all 540 test rows for every model, so it compares systems on equal footing.

## 4. (1 point) B — The min-max problem

The inner maximization searches for the worst input within the budget; the outer minimization trains the model to do well on those inputs. Option A is standard training; D describes only the attacker's step.

## 5. (1 point) B — ASR increases; the defense has a range

Training at 0.10 teaches the model to resist perturbations up to about that radius. At 0.20 the attacker has room the training procedure did not cover. In LAB-11, the adversarially trained model's ASR rises from 0.1809 to 0.6029 and robust accuracy falls from 0.7296 to 0.3537.

## 6. (1 point) B — Forward true, backward approximate

Rounding is non-differentiable and its true derivative is zero almost everywhere, so a gradient attack through it cannot move. BPDA keeps the true transform in the forward pass and substitutes a differentiable approximation (identity in LAB-11) in the backward pass.

## 7. (2 points) Two distinct, correctly scoped conclusions

Accept two of the following, one point each:

- **At ε = 0.10, squeezing provides real but limited protection** against these attacks: ASR is about 0.18–0.19, compared with 0.3582 for the undefended model. The adaptive attack did not dominate the naive attack, which suggests the transform is the main obstacle rather than the attack being badly wrong.
- **The slightly lower adaptive ASR is not evidence of safety.** An adaptive attack weaker than the naive attack signals an approximation or tuning problem (BPDA identity, step size, restarts). The result should prompt a stronger adaptive attempt, not a stronger claim.
- **At ε = 0.20, the protection collapses** under the adaptive attack: ASR 0.9981 and robust accuracy about 0.0019. The defense has an operating range.
- **None of the three numbers supports a universal robustness claim.** They cover one model, one transform, two budgets, and one attack family.

Deduct a point for a conclusion that treats the ε = 0.10 result as proof of security or that ignores the budget difference.

## 8. (2 points) Precision ≈ 0.154

In 10,000 inputs at 1% prevalence: 100 attacked, 9,900 benign.

- True positives: \(0.90 \times 100 = 90\).
- False positives: \(0.05 \times 9{,}900 = 495\).
- Precision: \(90 / (90 + 495) = 90 / 585 \approx 0.1538\).

So about 15% of alerts are real attacks. At a 10% base rate, precision would be \(0.90 \times 1{,}000 / (900 + 0.05 \times 9{,}000) = 900 / 1{,}350 \approx 0.667\). Award 1 point for correct counts, 1 point for the result and the interpretation that precision depends on prevalence.

## 9. (1 point) B — Consistency within tolerance

A checker verifies that artifacts match a reference experiment within a stated tolerance. It does not prove security, attack strength, or generalization. Those require argument, threat modeling, and broader evaluation.

## 10. (2 points) Any four missing elements

Accept four of the following, half a point each:

- the **attack**: which procedure, how many steps, restarts, and what the attacker knows;
- the **norm and budget** at which 40% and 2% were measured;
- the **base set**: clean-correct rows, size, and whether the defense changed clean accuracy;
- the **clean utility cost** of the defense;
- the **adaptive attempt** against the defense, not only the naive attack;
- the **stress budget** and behavior outside the defended range;
- the **dataset, model, and versions** that make the result reproducible;
- the **residual risk** and the statement that the defense is not universal.

A suitable answer: "It does not state the attack configuration or budget, does not give the base set or clean-accuracy cost, and does not report an adaptive attack or a stress budget. Without those, 2% is a number, not a robustness claim."
