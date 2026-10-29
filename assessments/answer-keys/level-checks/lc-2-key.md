# LC-2 Answer Key — Level 2 Core Attacks

**Scoring:** items 1–6 = 1 point each; items 7–8 = 2 points each; items 9–10 = 5 points each. Total 20. Pass 16/20.

## 1. A — 0

FGSM perturbs each input by $\varepsilon \cdot \operatorname{sign}(\nabla_x L)$. At $\varepsilon = 0$ the perturbation is zero, so every input is unchanged and no previously correct prediction can flip. An attack success rate above zero would indicate a bug in the implementation, the data pipeline, or the accounting.

- **B** and **C** would mean the attack changes predictions without changing inputs.
- **D** is wrong: the rate is defined and equals zero.

Tag: M04 · LO-05 · Bloom 2 · D1.

## 2. A — 2.5%

The course measures the poison rate against the clean training set: $40/1600 = 0.025$, or **2.5%**.

- **B** is the rate against the augmented set: $40/1640 \approx 2.44\%$. It is a defensible alternative denominator but not the one the course requires, and switching denominators between runs can disguise a change in attack size.
- **C** would require a clean set of 100 rows.
- **D** would require a clean set of 1,000 rows.

Always report the count and the denominator with the percentage.

Tag: M05 · LO-08 · Bloom 2 · D1.

## 3. C — 76 percentage points

The attack effect is the difference between the backdoored model's triggered rate and the clean model's triggered rate: $0.88 - 0.12 = 0.76$, or **76 percentage points**.

- **A** is the backdoored rate alone and ignores the clean baseline.
- **B** is the clean model's rate alone.
- **D** would be the effect only if the clean model sent none of the triggered rows to the target.

Tag: M06 · LO-10 · Bloom 2 · D1.

## 4. A — TPR at FPR ≤ 1%

Membership inference harm depends on how well an attacker can pick out members while keeping false accusations low. The standard report is true-positive rate at a fixed low false-positive rate (1% and 5%). Overall accuracy hides the low-FPR operating region where the attack is actually used.

- **B** is dominated by the majority class and can look high while the low-FPR attack is useless.
- **C** is a training signal, not a privacy metric, and does not by itself establish membership.
- **D** says nothing about whether any record can be distinguished.

Tag: M07 · LO-14 · Bloom 2 · D1.

## 5. False

A transfer attack computes gradients on a **surrogate** the attacker controls, then applies the resulting perturbations to the target. The target is never differentiated; that is what makes the attack black-box. Requiring target gradients would make it a white-box attack.

Tag: M04 · LO-06 · Bloom 2 · D1.

## 6. False

High fidelity means the extracted model reproduces the teacher's outputs on the queried distribution. It does not establish how the teacher was trained, what data it saw, or whether the attacker holds that data. Fidelity and data possession are different claims; the lab requires the learner to state this limit.

Tag: M07 · LO-13 · Bloom 2 · D1.

## 7. Required elements (definitions, denominators, why both)

- **ASR** is the share of *successfully attacked* inputs among the inputs the clean model classified correctly (the base set). The denominator is the count of clean-correct rows, so ASR is conditional on the model already working on that input.
- **Robust accuracy** is the share of *all* base-set inputs still classified correctly after the attack. The denominator is the full base set, including rows the clean model already misclassified.

Both belong in one report because they answer different questions. ASR says how often the attack works when it has something to break; robust accuracy says how much correct behaviour survives overall. A model with low clean accuracy can post a high ASR while retaining little absolute correctness, and a model with high clean accuracy can post a moderate ASR while retaining most correctness. Reporting only one lets the denominator choice flatter the result.

Two points: one for both definitions with denominators, one for the reason to report both. An answer that treats ASR as a share of all rows without saying so is ambiguous and loses the first point.

Tag: M04 · LO-05 · Bloom 3 · D2.

## 8. Required elements (distinction and baselines)

- **Poisoning** corrupts training data or the training process so the learned model behaves wrongly, often broadly or toward a chosen subpopulation.
- **Backdoor** implants a trigger-conditioned behaviour that stays dormant on clean inputs and activates on the trigger, usually with clean accuracy preserved.

Baselines:

- **Poisoning:** a clean-trained model on the same data and architecture, plus a random-label or random-row control at the same rate, so the effect is attributable to the attack rather than to noise or capacity.
- **Backdoor:** the clean model evaluated on the same triggered inputs (false-trigger rate) and clean accuracy on untriggered inputs, so the trigger effect is separated from ordinary error.

Two points: one for a correct distinction in both sentences, one for a relevant baseline for each. A single shared baseline such as "compare with the clean model" earns the second point only if the answer says what is measured on it.

Tag: M05 · LO-08 · Bloom 3 · D2 and M06 · LO-10 · Bloom 3 · D2.

## 9. Required elements (three budgets, configuration, base set, metrics, baseline, adaptive check, limits)

- **Attack configuration.** Untargeted PGD in $L_\infty$ at $\varepsilon \in \{0.01, 0.03, 0.06\}$, with a stated step count, step size, restarts, and clipping to the valid audio range. The same configuration is used at all three budgets.
- **Base set.** Synthetic clips the clean model classifies correctly, with the count stated. Report the clean accuracy on the full evaluation set separately.
- **Metrics.** ASR at each budget with its denominator; robust accuracy over the full base set; clean accuracy before attack.
- **Baselines.** $\varepsilon = 0$ (identity check, ASR must be 0) and a random perturbation of the same $L_\infty$ size, to show that the effect is not just added noise.
- **Adaptive check.** At least one check against a defence or obfuscation: BPDA or EOT if gradients are masked, or a transfer attack from an undefended surrogate. If no defence is present, vary steps and restarts to show the result is not an artefact of one setting.
- **Two limits.** For example: white-box access and digital audio only, so physical playback and microphone effects are untested; one model, one synthetic corpus, and one command set, so the result does not establish robustness generally.

Five points: one for the configuration and base set, one for the metrics, one for the baselines, one for the adaptive check, one for two specific limits. A result table without denominators earns at most two.

Tag: M04 · LO-05 · Bloom 5 · D4.

## 10. Required elements (two tests, baselines, limits, unsupported conclusions)

**(a) Backdoor.**

- Test synthetic clips with a set of candidate triggers (a tone, a short noise burst, a repeated word) against a target label, and compare the triggered rate with the same clips untriggered. Report clean accuracy and false-trigger rate on untriggered clips.
- **Baseline:** a locally trained clean model of comparable architecture on the same synthetic distribution, or at minimum the vendor model's own untriggered behaviour on the same clips.
- **Limit:** the trigger space is unbounded; a finite search can miss the implanted trigger, and a clean result does not prove absence.

**(b) Membership inference.**

- Train shadow models on synthetic data matched to the vendor's documented input format, score candidate records by a loss- or confidence-based membership signal, and report TPR at FPR ≤ 1% and ≤ 5%.
- **Baseline:** random guessing and a shadow model trained without the candidate records.
- **Limit:** the synthetic distribution may not match the vendor's training distribution; a membership signal is not proof of membership and not proof of harm.

**Two conclusions the tests cannot support even if both are negative:**

1. That the model contains no backdoor. The search covered a finite trigger family and a synthetic corpus.
2. That the model was not trained on a specific real person's data, or that the vendor's data practices are compliant. Membership inference tests a statistical signal, not data provenance or lawfulness.

A third acceptable conclusion is that the model is privacy-preserving; a negative membership test does not establish that.

Five points: up to two for each test design (with baseline and limit), one for two unsupported conclusions. A plan that proposes attacking the vendor's production endpoint rather than the local copy earns zero for safety.

Tag: M06 · LO-11 · Bloom 5 · D4 and M07 · LO-14 · Bloom 5 · D4.
