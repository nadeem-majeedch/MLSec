# QZ-05B Answer Key — Module 05

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — access to preprocessing or pipeline code

The poisoning attack surface is the path from raw data to trained model. An attacker who can change a join, a deduplication rule, or a filter alters which rows reach training and what they mean, even if every submitted label is correct. That is a pipeline-level attack and it requires code or configuration access.

- **A** is label-level access: it can flip labels but does not change joins or deduplication.
- **C** is inference-time access and does not touch training.
- **D** reads results; it does not alter training data.

Tag: M05 · LO-08 · Bloom 2 · D1.

## 2. B — broad degradation across many classes

An availability attack aims to reduce overall usefulness, so accuracy falls across the population. A targeted integrity attack is the opposite pattern: it redirects one class or decision while aggregate accuracy can stay flat or even improve.

- **A** describes a targeted integrity effect.
- **C** is model extraction.
- **D** is membership inference.

Tag: M05 · LO-08 · Bloom 2 · D1.

## 3. False

Accuracy is an aggregate availability metric. A targeted poisoning attack can leave accuracy unchanged, or raise it slightly, while reliably redirecting the chosen inputs. The correct conclusion is that accuracy did not detect the attack, not that the attack failed. The protected outcome must be measured separately.

Tag: M05 · LO-08 · Bloom 2 · D1.

## 4. False

A clean-label attack uses correct labels that sit in the wrong region of feature space. A screen that compares rows with a trusted reference set can still catch rows far from their labelled class, but rows placed near the target boundary are designed to look plausible and can pass. Screening is therefore weaker against clean-label attacks, not equally effective; the lab's dense, mislabelled poisons are an easier case.

Tag: M05 · LO-09 · Bloom 3 · D2.

## 5. Required elements

Test-label corruption changes the **measurement**, not the learned model. The model was trained on unchanged data; the reported score is invalid because the answer key is wrong. Report it as an evaluation-integrity failure: the test set was corrupted, the affected rows were excluded or corrected, and any result computed before the fix is withdrawn. Calling it poisoning confuses an attack on training with an error in evaluation.

Tag: M05 · LO-08 · Bloom 2 · D1.

## 6. 2.5% against the clean set; about 2.44% against the augmented set

- Clean-set denominator: $50/2000 = 0.025$, or **2.5%**.
- Augmented-set denominator: $50/(2000+50) = 50/2050 \approx 0.02439$, or **about 2.44%**.

The course requires the clean training-set size as the denominator. The difference is small at this rate but grows with the attack, and a report that switches denominators can make two runs look different when the attacker did the same thing. The rate must be accompanied by the count and the denominator, not just a percentage.

Tag: M05 · LO-08 · Bloom 3 · D2.

## 7. Required elements (two flaws and why the catch rate is not evidence)

Two of:

- **The threshold is fitted to the evaluation poisons.** `threshold = scores[poison_idx].min()` uses the very rows the screen is supposed to catch. Any screen will catch all of them at or below that threshold by construction; the 100% catch is a tautology.
- **False positives are hardcoded, not measured.** `false_positives 0` is printed, not computed. The benign cost of the threshold is unknown.
- **There is no held-out evaluation.** The same rows choose the threshold and score the result, so the estimate is optimistic and says nothing about future poison.
- **There is no trusted reference set.** `screen` has no stated clean baseline, so its scores have no calibrated meaning.

The catch rate is not evidence about future data because the threshold was chosen with knowledge of the test poisons. A valid evaluation fixes the threshold on separate clean/reference data, then measures catches and false positives on held-out rows, and reports both counts with denominators.

Tag: M05 · LO-09 · Bloom 4 · D3.

## 8. Required elements (three gaps and a bounded plan)

Gaps such as:

- **A signature authenticates origin and transit integrity, not correctness.** A signed feed from a compromised or malicious source is still correctly signed. It does not establish that the labels are true.
- **Deduplication removes repeats, not crafted or mislabelled rows.** An attacker can submit unique rows that survive deduplication.
- **The threat model omits insiders and account compromise.** A vendor employee or a stolen publishing key can produce validly signed bad data.
- **There is no row-level provenance or label lineage.** The feed's signature covers the package, not each row's origin and review history.
- **No measured screening performance.** The claim provides no catch rate, false-positive rate, or trust assumption for the vendor's own checks.

A bounded plan:

1. Build a local replica with synthetic or licensed data and the vendor's documented schema.
2. Define the protected outcome and a threat model limited to the feed path (label errors, crafted rows, pipeline joins).
3. Inject a small set of controlled poison rates and both mislabelled and clean-label rows.
4. Apply label/reference screening with a threshold fixed on clean reference data; report catches, false positives, and the protected-outcome effect separately.
5. State the residual risk: screening cannot certify the feed, and provenance plus audit remains necessary.

The plan must stay on the local replica and must not probe the vendor's production systems. "Ask the vendor to be careful" is not a control.

Tag: M05 · LO-09 · Bloom 5 · D3.
