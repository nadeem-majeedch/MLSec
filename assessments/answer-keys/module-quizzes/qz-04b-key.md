# QZ-04B Answer Key — Module 04

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — an untargeted attack

An untargeted attack succeeds when the prediction differs from the true label, whatever the new label is. A targeted attack names a specific destination class and measures success against that class, not against "anything else."

- **A** describes a targeted attack, which has a different base set and denominator.
- **C** changes training data, not one input at inference time.
- **D** asks whether a record was in the training set; it is not an evasion method.

Tag: M04 · LO-05 · Bloom 2 · D1.

## 2. B — more search starting points

A restart begins the optimization again from a different random point near the input. With a fixed budget and step count, more restarts give the attacker more chances to find a high-loss example, usually raising measured ASR. The budget does not change, and the model is not retrained.

- **A** is wrong: the ε-ball is fixed by the threat model, not by restarts.
- **C** is wrong: clean accuracy is measured without perturbation.
- **D** is wrong: the success definition is unchanged; restarts change how hard the attacker searches.

Tag: M04 · LO-05 · Bloom 2 · D1.

## 3. True

Projection has two constraints: the perturbation must stay within the ε-ball around the original input, and the resulting input must remain in the valid domain (for images, usually [0, 1]). Clipping only to the ε-ball can produce values outside the valid range, which is both unrealistic and a likely bug in the reported perturbation size.

Tag: M04 · LO-05 · Bloom 2 · D1.

## 4. False

A transfer attack is black-box with respect to the target: the attacker computes gradients on a local source model and applies the resulting perturbation to the target. Requiring gradients through the target would make it a white-box attack and would remove the property that makes transfer interesting.

Tag: M04 · LO-06 · Bloom 2 · D1.

## 5. Required element

The clean model's errors are not attack effect. If the base set included rows the model already misclassifies, a "success" could be counted without any perturbation, inflating ASR and making runs with different clean accuracy incomparable. Restricting the base set to clean-correct rows measures the change the attack caused.

A full-credit answer states either the exclusion of pre-existing errors or the comparability/baseline reason. "Because those rows are easier" earns no credit without the baseline logic.

Tag: M04 · LO-05 · Bloom 3 · D2.

## 6. ASR = 0.25; robust accuracy = 0.675

- **ASR** uses the 360 clean-correct rows as the denominator: $90/360 = 0.25$.
- **Robust accuracy** uses all 400 test rows. Of the 360 clean-correct rows, 90 turn wrong and 270 stay correct. The 40 clean-wrong rows do not change, so they stay wrong. The numerator is 270, giving $270/400 = 0.675$.

ASR and robust accuracy answer different questions: ASR is conditional on the attackable base set, while robust accuracy describes the whole population. A report that gives only one of them has not said enough for a deployment decision.

Tag: M04 · LO-05 · Bloom 3 · D2.

## 7. Required elements (two flaws and a consequence)

Two of:

- **The budget is not ε = 0.10.** The loop raises `eps` by 0.10 up to 0.50, so successful rows may use perturbations as large as 0.50 while the output is labelled "FGSM at ε = 0.10." The reported number describes an unknown, per-image budget.
- **The clean-wrong rows enter the numerator.** The ASR denominator is the whole test set, and a row the clean model already misclassifies can be counted as a hit before any successful perturbation.
- **The search selects on the evaluation examples.** The loop stops at the first epsilon that flips each image, so the result is the outcome of a per-image search, not a fixed-budget attack; there are no restarts and no held-out protocol.
- **The gradient is not recomputed.** The loop reuses `grad[i]` from the original input, so it is not the iterative attack its name implies.

Consequence: the printed ASR is inflated and not comparable to any other result at ε = 0.10, because neither the budget nor the base set is the one stated.

A corrected version fixes the budget at 0.10, restricts the base set to clean-correct rows, and either reports success under that fixed budget or reports the distribution of minimum successful ε as a separate measurement.

Tag: M04 · LO-05 · Bloom 4 · D3.

## 8. Required elements (three questions and a bounded rewrite)

Questions such as:

- **Units and norm:** is ε = 0.01 measured on pixels in [0, 1], and is the norm L∞? A number without units and norm cannot be compared with another result.
- **Attack strength:** what step size, and why is 5 steps with one restart adequate? Were restarts, more steps, or an adaptive attack attempted? A failed weak attack is a lower bound, not a robustness certificate.
- **Metric and base set:** is 99.2% robust accuracy over all 2,000 rows or 1 − ASR on a clean-correct base set? How many rows changed, and with what uncertainty?
- **Threat-model coverage:** does the test set represent deployment inputs, and does the claim cover only digital L∞ perturbations? Physical, query, and distribution-shift constraints are out of scope unless tested.
- **Defense status:** if any defense is present, was the attack designed against it? If none, the result says nothing about adaptive attackers.

A supportable rewrite:

> On this 2,000-image test set, under a white-box L∞ budget of 0.01 with pixels in [0, 1], 5-step PGD with one restart and a fixed step size changed 16 predictions (0.8%). This is a lower bound on attack success for this budget and attack configuration; no adaptive or distribution-shift evaluation was performed, and the result does not establish deployment robustness.

The rewrite must keep the budget, the denominator, the attack configuration, and a limitation. "The model is robust at ε = 0.01" without the lower-bound caveat is not supportable.

Tag: M04 · LO-07 · Bloom 5 · D3.
