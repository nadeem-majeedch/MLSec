# QZ-06B Answer Key — Module 06

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — clean accuracy and ASR on triggered inputs

A backdoor has two behaviors: normal predictions on ordinary inputs and target-class predictions when the trigger appears. Clean accuracy measures the first; attack success rate on triggered source rows measures the second. Reporting both is the minimum for a backdoor claim.

- **A** describes scale, not behavior.
- **C** describes training progress; neither isolates conditional behavior.
- **D** measures ordinary classification quality, not the triggered path.

Tag: M06 · LO-10 · Bloom 2 · D1.

## 2. A — a fixed patch

A trigger is a specific pattern whose presence causes the learned target behavior; in this module it is a fixed patch, value change, or token pattern. The key property is that the same pattern is applied consistently and is absent from ordinary inputs.

- **B** is random noise, not a fixed pattern; it is a perturbation, not a trigger.
- **C** is a label change in training, not a pattern at inference.
- **D** changes evaluation, not model behavior.

Tag: M06 · LO-10 · Bloom 2 · D1.

## 3. False

A backdoor can leave clean accuracy almost unchanged because the triggered path is rare in ordinary data. High clean accuracy shows the model works on the measured distribution; it does not exercise the conditional behavior. The defect is exactly the one clean evaluation is least likely to see.

Tag: M06 · LO-10 · Bloom 2 · D1.

## 4. True

Lowering the threshold flags more positions, including benign ones. That raises true positives only if some true triggers scored below the old threshold, but it always exposes more of the benign score distribution. The false-positive count is a cost of the threshold and must be measured, not assumed away.

Tag: M06 · LO-11 · Bloom 2 · D1.

## 5. Required element

Some clean models already send a fraction of triggered source rows to the target class, because the trigger values are unusual or the target class is common. Without that baseline, the backdoored model's raw target rate overstates the attack effect. The report must show the difference between the two rates on the same rows, not just the higher number.

Tag: M06 · LO-10 · Bloom 3 · D2.

## 6. 90 rows; 6.0% against the clean set; about 5.66% against the augmented set

- Poisoned rows: $0.06 \times 1500 = 90$.
- Clean-set rate: $90/1500 = 0.06$, or **6.0%**.
- Augmented-set rate: $90/(1500+90) = 90/1590 \approx 0.0566$, or **about 5.66%**.

The course requires the clean training-set denominator. It keeps the attacker's budget comparable across runs and makes clear how much of the final training set was attacker-controlled. The augmented rate is useful context but is not the poison rate.

Tag: M06 · LO-10 · Bloom 3 · D2.

## 7. Required elements (two flaws and why absence is not shown)

Two of:

- **Only one position is tested.** A backdoor trigger can sit at any position, size, or form; a scan at (0, 0) tests one hypothesis and says nothing about the rest.
- **The threshold has no baseline or false-positive calibration.** A mean target probability above 0.5 can occur for ordinary reasons, especially if class 1 is common. The clean model's response at the same position is missing.
- **The average is over all test rows, not triggered source rows.** The relevant denominator is the source class the attacker wants redirected; pooling classes dilutes or distorts the score.
- **The output is a binary verdict from one number.** There is no score distribution, no comparison across positions, and no held-out confirmation.

A "no backdoor" result is not evidence of absence because the test covered one candidate trigger at one position with an uncalibrated threshold. Absence would require a defined trigger family and a scan with a measured false-positive rate; even then it is absence of the tested triggers, not proof of a clean model.

Tag: M06 · LO-11 · Bloom 4 · D3.

## 8. Required elements (measurements, baselines, and two limits)

Measurements and baselines:

- **Clean accuracy** on held-out local inputs, untriggered, to establish ordinary behavior.
- **Trigger scan** over a declared family of candidate positions, patch sizes, and value patterns. For each candidate, measure the target-class probability on held-out source-class inputs, and compare with the same inputs without the trigger and with a clean reference model if one is available.
- **ASR** on triggered source rows, reported against the clean model's target rate on the identical rows. If no clean model is available, report the untriggered target rate and state that the baseline is weaker.
- **False-trigger rate** on benign inputs that carry the pattern but should keep their class, plus clean inputs without the pattern.
- **Multiplicity:** report how many candidate triggers were tested and the best score, not only the winning position; otherwise the best-of-many result is optimistic.

Two limits:

- The test covers only the trigger families and positions tried. A negative result is not proof that no backdoor exists.
- Black-box access may not expose a trigger that depends on training data, a rare input region, or a pattern outside the candidate set. Without training data, the poison rate and the attacker's access path are unknown.

The plan must run only on the local model and synthetic or licensed inputs. "We scanned it and found nothing" without the candidate family, thresholds, false positives, and limits is not a finding.

Tag: M06 · LO-11 · Bloom 5 · D3.
