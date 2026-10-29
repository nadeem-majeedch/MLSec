# Module 06 Knowledge Check — Answers and Explanations

**QZ-06 · 12 points · Pass 10/12**

Do not read this file before attempting the quiz.

---

## 1. What a backdoor is — **B** (1 point)

A backdoor is conditional: ordinary inputs are handled normally, and a trigger changes the behavior. Option A describes evasion; option C describes a globally bad model; option D describes data theft.

## 2. Clean accuracy and ASR — **A** (1 point)

The two numbers answer different questions. Clean accuracy says the model behaves on untriggered inputs; ASR says it produces the target on triggered sources. A high clean accuracy does not weaken the backdoor claim.

## 3. The baseline — **C** (1 point)

The attack effect is the increase over the clean model's behavior: $0.86 - 0.18 = 0.68$, or about 68 percentage points. Reporting 86% as if it started from zero overstates the attack. Option D is impossible.

## 4. Poison budget — **B** (1 point)

$67 / 840 = 0.0798$, about 8.0%. The test set is not the denominator. Option A divides by 1,000; option C confuses the count with a rate.

## 5. Trigger-scan score — **B** (1 point)

The clean model's score at the same patch is the false-trigger baseline: how much the pattern shifts predictions without a backdoor. Without it, 0.89 has no scale. It is not the ASR, the false-positive rate, or the poison rate.

## 6. Threshold choice — **B** (1 point)

Raising the threshold makes the detector more conservative: it flags fewer candidates, so both true and false positives generally decrease. Whether that is good depends on the cost of a missed backdoor versus a wasted investigation.

## 7. Supply chain — **A** (1 point)

A trojaned checkpoint can carry behavior with no poisoned rows in your pipeline. A corrupted test set breaks evaluation, a threshold is a decision rule, and a missing seed breaks reproducibility; none of those implants a conditional behavior.

## 8. Find the flaw — **2 points**

Award one point per flaw with its consequence.

**Flaw 1 — the label array has the wrong length.** `X_poisoned` has $840 + 67 = 907$ rows, but `y_poisoned` is a copy of an 840-row array. The fit raises a length mismatch, and even if it ran, the appended rows would have no target label.

```python
y_poisoned = np.concatenate([y_train, np.ones(len(chosen), dtype=int)])
```

**Flaw 2 — ASR is measured on the poisoned training rows.** `X_poisoned[840:]` is the 67 rows the model was trained on, so the score measures memorization. It should be measured on triggered **held-out source** rows.

```python
source = X_test[y_test == 0]
asr = (model.predict(add_trigger(source)) == 1).mean()
```

A third issue worth noting: overwriting `y_poisoned[chosen] = 1` changes the original labels instead of appending new labelled rows. The corrected construction above appends the labels, preserving the clean rows.

## 9. Appending versus overwriting — **1 point**

$0.08 \times 840 = 67.2$, which rounds to **67**. Appending preserves the clean class-0 rows, so the model keeps its ordinary behavior and learns a **conditional** rule; overwriting would remove class-0 evidence, hurt clean accuracy, and make the attack easier to notice.

## 10. Evaluate the claim — **2 points**

Award one point for three real problems and one point for a rewrite that keeps the scope of the evidence. Any three of:

- **Clean accuracy does not test the trigger.** A backdoor is conditional by design; a clean test set can be passed completely.
- **500 random images are not a trigger search.** Random inputs almost never contain a structured trigger, so the trial bounds only that particular random sample, not the space of triggers.
- **There is no ASR, no baseline, and no probe set.** The vendor reports no triggered evaluation, no clean-model comparison, and no false-trigger check.
- **The test set's provenance and the model artifact's provenance are unstated.** A clean test set does not cover a trojaned checkpoint.
- **"No backdoor" is an absence claim.** The evidence can support "we did not find this behavior with these tests," not "there is none."

**Example rewrite.**

> On our 10,000-image clean test set, the model reaches 99% accuracy. On a triggered probe set for trigger family T, ASR was X% versus a clean-model baseline of Y%, and a scan over the stated trigger space flagged Z candidates with W false positives on a clean model. These results cover the tested trigger family and test distribution; they do not establish the absence of other backdoors, and the artifact's provenance should be verified separately.

Accept any rewrite that names the trigger family, the ASR and baseline, the false-positive evidence, and at least one scope limit. A rewrite that says "the model has no backdoor" earns no credit.

---

## Score guide

| Score | Next step |
|---:|---|
| 11–12 | Move to LAB-08 or Module 07 |
| 10 | Review the missed item, then continue |
| 8–9 | Re-read Lessons 1 and 3; rerun the LAB-08 scan |
| Below 8 | Re-read all four lessons before continuing |
