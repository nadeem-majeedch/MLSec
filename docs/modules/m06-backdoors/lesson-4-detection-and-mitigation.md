# Lesson 06.4 — Detection, Mitigation, and the Arms Race

<a id="m06-l4"></a>

**1.25 hours · Lesson 4 of 4 · Module 06**

## What this lesson answers

Which defenses actually find a backdoor, what do they assume, and what does an adaptive attacker do next? This lesson compares detection and mitigation families, then sets the evaluation standard that keeps a defense claim honest.

## Detection is a search problem with a cost model

Every backdoor detector looks for a signal that separates triggered behavior from ordinary behavior. The families differ in **where** they look:

| Family | Signal | Needs | Fails when |
|---|---|---|---|
| **Data inspection** | Rows with extreme or anomalous features | Feature schema, thresholds | Trigger looks ordinary; clean-label attack |
| **Provenance and audit** | Who added what, when | Logs, signatures, review | Logs are incomplete or the insider is trusted |
| **Trigger search** | A pattern that shifts predictions | Trigger shape/size guess, model access | Trigger is outside the search space |
| **Spectral / representation** | A separable direction in features or activations | Representation access, clean reference | Poison is small or spread; adaptive attacker |
| **Input perturbation (STRIP)** | Prediction instability under input mixing | Inference access, benign inputs | Trigger survives the perturbation; cost per query |
| **Neuron / weight analysis** | Dormant or trigger-specific units | White-box access, clean calibration | Backdoor is distributed across many units |
| **Behavioral probes** | Targeted inputs that should be classified a certain way | Knowledge of the decision | Probe set misses the trigger |

No row in the table is "the best." Each one converts a different kind of access into a different kind of evidence. A defender with only black-box query access cannot run spectral analysis; a defender with weights but no clean reference cannot calibrate a neuron test.

## What the labs' defenses actually assume

LAB-07 screens known columns for extreme values. LAB-08 searches 2×2 patches at all positions. Both are **trigger-specific**:

| Defense | Assumption | Attack that defeats it |
|---|---|---|
| Feature threshold > 2.5 | Trigger columns and scale known | Trigger at 2.0, or spread across ordinary features |
| 2×2 white-patch scan | Patch size, color, and shape known | 3×3 patch, random color, border trigger |
| Filter rows with the patch | Trigger is present in training rows | Clean-label trigger; trigger added only at inference |
| Retrain on kept rows | Removed rows are the only source | A second trigger, or a trojaned initial model |

The labs are honest about this in their limitations sections. A student report that says "screening works" without naming the trigger family is making a broader claim than the experiment supports.

## A detection result is a confusion matrix

A detector's output has four cells:

| | Backdoor present | No backdoor |
|---|---|---|
| **Flagged** | True positive | False positive |
| **Not flagged** | False negative | True negative |

Two rates summarize it:

$$
\text{detection rate} = \frac{TP}{TP + FN},
\qquad
\text{false-positive rate} = \frac{FP}{FP + TN}.
$$

A detector that flags everything has a perfect detection rate and a useless false-positive rate. A detector that flags nothing has the reverse. The operating point is a **threshold**, and the threshold should be chosen with the costs of both errors in mind.

In LAB-08, the scan's top score is 0.8884 and the runner-up is 0.7938. If the decision rule is "flag the argmax," the true patch is selected. If the rule is "flag every position above 0.8," two positions are flagged and the defender must disambiguate. Neither rule is wrong; they have different false-positive behavior, and the report should say which one it used.

## The spectral idea, in one paragraph

Tran, Li, and Madry (2018) observed that poisoned examples often share a direction in representation space that clean examples do not. If you stack the representations of training examples and compute the top singular vectors, the poison can appear as an outlier direction. Removing examples that load heavily on that direction can reduce the backdoor. The method is powerful when the poison is a coherent subpopulation, and it weakens when the attacker spreads the poison or makes it look like the clean data. The lesson is not "use SVD"; it is "a detector is a hypothesis about what the attack leaves behind."

## Mitigation families

| Mitigation | What it does | Cost | What it does not do |
|---|---|---|---|
| **Remove flagged rows and retrain** | Deletes the teaching signal | Clean data loss; retraining | Remove a backdoor in the initial weights |
| **Fine-pruning** | Prunes units inactive on clean data, then fine-tunes | Clean-accuracy loss; tuning | Guarantee removal of a distributed backdoor |
| **Input filtering** | Rejects or sanitizes suspected triggers at inference | False rejects; latency | Repair the model for unseen triggers |
| **Retrain from trusted data** | Rebuilds the model on a clean corpus | Expensive; may be impossible | Prove the new data is clean |
| **Replace the artifact** | Deploys a known-good model | Supply-chain and rollback work | Address the process that admitted the bad one |

Fine-pruning is a useful example of a defense with a mechanism: a backdoor often relies on units that are quiet on clean inputs, so pruning those units can remove the conditional path. But "often" is not "always," and a determined attacker can distribute the behavior. The defense must be evaluated on the attack it faces, not on the attack it was designed for.

## The adaptive attacker

An adaptive attacker knows the defense and changes the attack. Against the defenses in this module, the moves are predictable:

- **Trigger design.** Move the trigger off the searched grid; change its size, color, or shape; blend it into the input.
- **Budget.** Use fewer rows, or rows that are harder to separate from clean data.
- **Labels.** Use clean labels so label screening has no signal.
- **Placement.** Spread the poison so it does not form a dense cluster.
- **Multiple triggers.** Keep a second trigger that the defender has not found.
- **Supply chain.** Trojan the weights or the fine-tuning set instead of the training data.

A defense evaluation that does not include at least one adaptive attempt is a lower bound on the attacker's capability, not a guarantee. This is the same lesson as Module 04's "a failed attack is weak evidence," applied to training-time behavior.

## What to demand from a model vendor

Backdoors are a supply-chain risk, so the controls include procurement and artifact handling:

1. **Provenance.** Where did the training data come from, and who could add to it?
2. **Reproducibility.** Can the vendor rebuild the model from pinned data and code?
3. **Artifact integrity.** Is the model signed and hash-pinned? Can you verify it before loading?
4. **Evaluation evidence.** Clean accuracy, triggered behavior on a stated probe set, false-trigger checks, and the trigger families tested.
5. **Incident process.** Who is notified if a backdoor is found, and how fast can the artifact be withdrawn?
6. **Update controls.** Are updates signed, diffed, and staged? Does a new version require a new evaluation?

None of these proves the absence of a backdoor. Together they make the attack harder, the evidence better, and the response faster.

## Evaluating a defense: a checklist

| Item | Question |
|---|---|
| Attack | Which trigger, budget, source class, and target? |
| Baseline | What does the clean model do on the same triggered inputs? |
| Detection | TP, FP, FN, TN, and the threshold |
| Protected outcome | Did ASR fall and clean accuracy hold? |
| Adaptive attempt | Did the attacker know the defense? What changed? |
| Scope | Which trigger families does the defense cover? |
| Cost | Clean data removed, accuracy lost, latency added |
| Replication | More than one seed, model, or dataset? |

A report that answers all eight is auditable. A report that answers only "ASR fell to zero" is a demo.

## Common mistakes and troubleshooting

| Mistake | Why it is wrong | Fix |
|---|---|---|
| "Our detector has 100% recall" | Says nothing about false positives | Report both rates and the threshold |
| Testing only the trigger you implanted | The detector may not generalize | Test a second trigger family |
| Treating pruning as a proof | Pruning removes a path, not the concept | Evaluate ASR after pruning, including adaptive attacks |
| Ignoring clean-accuracy cost | A defense that breaks the model is not a defense | Report accuracy and slices |
| Assuming the attacker is static | Adaptive attacks are the relevant test | Include one defense-aware attempt |
| Confusing artifact integrity with behavior | A signed model can still be backdoored | Verify both provenance and behavior |

## Summary and key takeaways

- Detection families differ by where they look and what access they need.
- A detector is a confusion matrix with a threshold, not a single score.
- LAB-07 and LAB-08 defenses are trigger-specific; their reports must name the trigger family.
- Spectral and pruning defenses work when their assumptions hold and weaken under adaptive attacks.
- An adaptive attacker changes trigger design, budget, labels, placement, or supply-chain entry.
- Backdoor risk is a supply-chain problem; provenance, signing, reproducibility, and update controls matter.
- A defense claim needs catches, false positives, a protected outcome, costs, and an adaptive attempt.
- "ASR fell to zero on our trigger" is a result, not a guarantee.

## Check yourself

1. Why is a detector's false-positive rate as important as its detection rate?
2. What assumption does the LAB-08 scan make about the trigger?
3. How does fine-pruning try to remove a backdoor, and when does it fail?
4. Name three ways an adaptive attacker changes the attack after learning the defense.
5. What six things would you demand from a vendor before trusting a model artifact?

## Next step

Module 07 changes the target from behavior to information. [LAB-09](../../labs/lab-09.md) asks how much of a model can be copied through a limited number of prediction queries. Read [Module 07](../m07-extraction-privacy/index.md) next.
