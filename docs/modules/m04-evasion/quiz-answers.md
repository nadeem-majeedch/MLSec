# Module 04 Knowledge Check — Answers and Explanations

**QZ-04 · 12 points · Pass 10/12**

Do not read this file before attempting the quiz.

---

## 1. Parts of an evasion claim — **B** (1 point)

Goal, knowledge, capability, budget, and metric. Without all five, the claim cannot be tested or compared. Assets and boundaries matter (M03), but they are not the five parts of a specific evasion result.

## 2. The L∞ norm — **B** (1 point)

L∞ is the maximum absolute coordinate change. A is the L1 norm, C is L0, and D is L2.

## 3. FGSM update — **B** (1 point)

Untargeted FGSM ascends the loss with a sign step. A descends; C is an unnormalized gradient step; D differentiates with respect to parameters.

## 4. The ε = 0 test — **B** (1 point)

It is a cheap invariant check. If ε = 0 changes predictions, the attack code is corrupting the input, and every later number is suspect. It does not establish robustness.

## 5. Base set — **B** (1 point)

Rows already misclassified cannot show that the attack caused an error. Whole-test-set ASR is a valid but different metric and must be labeled as such.

## 6. Targeted accuracy — **D** (1 point)

Targeted success is measured on rows that are not already the target class and that the clean model gets right. Including rows labeled 3 would count unattacked successes. Option C describes the exclusion but then removes them from the base entirely, which is not the same as "exclude from success."

## 7. PGD projection — **B** (1 point)

The projection enforces the budget and the valid domain. Integer pixels would require a different threat model; the sphere is an L2 constraint.

## 8. Transfer reasoning — **C** (1 point)

Transfer depends on both decision boundaries. A perturbation can cross the target's boundary while missing the source's. This does not prove greater vulnerability in general, and shared training data is not required for transfer (though it helps).

## 9. Find the flaw — **2 points**

A strong answer names at least two flaws and a consequence:

- **Wrong sign.** The code uses `−` and therefore descends the loss, reducing the chance of a label change. Depending on the gradient, ASR may be near zero.
- **No base set.** The denominator is the whole test set, including rows that were already wrong. The reported number is not the clean-correct ASR.
- **No clipping consistency / no validity check.** Although values are clipped to [0, 1], the code does not verify the L∞ bound or print it. (Only count this if the answer explains why it matters.)
- Consequence: the ASR is likely understated and cannot be compared with the lab reference.

One point for two flaws, two points for two flaws plus a clear consequence.

## 10. Evaluate the claim — **2 points**

Any two of:

- One model, one dataset, one budget, one attack configuration cannot support a claim about "all image classifiers."
- The attack's strength depends on steps, restarts, and step size; 99% may reflect the base set or an under-defended model.
- The experiment may be digital only, with no preprocessing or physical transformations.
- A high ASR says nothing about whether an attacker can reach the model or reproduce the examples.
- The claim does not state the base set or the perturbation budget.

A supportable rewrite: "On this model and dataset, under a white-box L∞ budget of ε, PGD with the stated steps and restarts changed X% of clean-correct test predictions. The result does not generalize to other models or deployment conditions."

One point for two valid reasons; two points for both reasons and a rewritten claim that keeps the budget and scope.
