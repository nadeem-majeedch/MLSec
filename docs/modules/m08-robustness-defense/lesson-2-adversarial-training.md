# Lesson 08.2 — Adversarial Training

<a id="m08-l2"></a>

**Module 08 · Lesson 2 of 6 · 1.5 hours · LO-17**

## Scenario

Your team has a digits classifier that is 96.67% accurate and 62.04% robust at ε = 0.10. The product owner asks for "better robustness" and offers a week of engineering time. You can spend it on adversarial training, on a preprocessing filter, or on nothing.

This lesson is about the first option. Adversarial training is the most reliable empirical defense in this course, and it is not free. You will see exactly what it costs in clean accuracy, what it buys in robust accuracy, and why the answer changes when the attacker moves to a larger budget.

## Objectives

By the end of this lesson you will be able to:

1. Explain adversarial training as a min-max problem: an inner attack and an outer fit.
2. Describe how LAB-11 implements it and state the implementation's limits.
3. Compute the clean-accuracy cost and the robust-accuracy gain from a comparison table.
4. Explain why ASR denominators differ between defended models and why robust accuracy is the fairer cross-model comparison.
5. Predict what happens when the evaluation budget exceeds the training budget.

## 1. The min-max idea

Standard training minimizes the average loss on the training distribution:

\[
\min_{\theta} \; \mathbb{E}_{(x,y)\sim D}\left[ L(f_\theta(x), y) \right]
\]

Adversarial training changes the inner term. For each training batch, it first searches for an input near \(x\) that maximizes the loss, then trains on that input:

\[
\min_{\theta} \; \mathbb{E}_{(x,y)\sim D}\left[ \max_{\|\delta\|_\infty \le \epsilon_{\text{train}}} L(f_\theta(x+\delta), y) \right]
\]

Madry et al. (2017) made this the standard formulation and used PGD for the inner maximization. The outer minimization is ordinary gradient descent on the resulting examples.

Two budgets appear in any adversarial-training experiment, and they are not the same number:

| Budget | Meaning | LAB-11 value |
|---|---|---|
| \(\epsilon_{\text{train}}\) | Radius used to generate training examples | 0.10 |
| \(\epsilon_{\text{eval}}\) | Radius used by the evaluation attack | 0.10, stress 0.20 |

Confusing them is a common source of overclaimed robustness. A model trained at 0.10 has been taught to resist perturbations up to roughly that size. It has not been taught anything specific about 0.20.

### Why the inner attack matters

If the inner maximization is weak, the model learns to resist a weak attack. A one-step FGSM inner loop is much cheaper than PGD and sometimes works, but it can produce models that are easy to break with an iterative attack. The inner attack is a design choice that belongs in the report, alongside the outer optimizer and the number of epochs.

## 2. How LAB-11 implements it

The lab keeps the implementation small enough to read in one sitting. The relevant function is `adversarial_train` in the reference solution (`solution.py` in `labs/lab-11-defense-evaluation/`); the [LAB-11 brief](../../labs/lab-11.md) explains how to run it without opening the solution first:

```python
def adversarial_train(baseline, X_train, y_train, epsilon=TRAIN_EPSILON, steps=10, seed=SEED):
    """Augment the training set with PGD examples and refit."""
    X_adv_train = pgd(
        baseline, X_train, y_train, epsilon=epsilon,
        alpha=epsilon / 5.0, steps=steps, restarts=1, seed=seed,
    )
    return LogisticRegression(max_iter=5000, C=0.01).fit(
        np.vstack([X_train, X_adv_train]), np.concatenate([y_train, y_train])
    )
```

Read it in four steps:

1. Generate adversarial versions of every training row with 10-step PGD, step size \(\epsilon/5 = 0.02\), one restart.
2. Concatenate the clean rows and the adversarial rows, duplicating the labels.
3. Refit a logistic-regression model on the doubled training set.
4. Use a stronger regularizer than the baseline (`C = 0.01` instead of `C = 1.0`).

Then the evaluation uses a stronger attack than training: 20 steps, 2 restarts, and the step size is again \(\epsilon/5\).

### Three limitations you must state

The implementation is deliberately modest, and honesty about that is part of the lesson.

- **The inner attack uses the baseline model, not the model being trained.** This is a one-pass augmentation, not the iterative "attack the current model, update, repeat" loop of full PGD-AT. It is closer to training on a fixed adversarial dataset. It is cheaper, and it is weaker.
- **Two things change at once.** The refit changes both the training data and the regularization strength (`C`). Any clean-accuracy loss cannot be attributed purely to adversarial training; some of it may come from stronger regularization. A clean experiment would hold `C` fixed and run a third model.
- **The model family is linear.** Results on logistic regression do not transfer quantitatively to neural networks. The method transfers; the numbers do not.

None of these makes the lab invalid. They define what it measured. Write them in the report instead of hiding them.

## 3. What it bought and what it cost

LAB-11 evaluates all three systems on the same 540-row test set.

| Model | Clean acc. | Clean-correct rows | Robust acc. at ε = 0.10 | ASR at ε = 0.10 |
|---|---:|---:|---:|---:|
| Undefended | 0.9667 | 522 | 0.6204 | 0.3582 |
| Adversarially trained | 0.8907 | 481 | 0.7296 | 0.1809 |
| Input squeezing | 0.9500 | 513 | 0.7722 | 0.1871 |

Read the trade-off three ways.

**Clean cost.** \(0.9667 - 0.8907 = 0.0760\). Adversarial training spends 7.6 percentage points of clean accuracy.

**Robust gain.** \(0.7296 - 0.6204 = 0.1092\). It buys 10.9 points of robust accuracy at the training budget.

**Attack success.** ASR roughly halves, from 0.3582 to 0.1809.

A product owner who only sees "ASR halved" will approve it. A product owner who sees "7.6 points of clean accuracy" may want a decision meeting. Both numbers are required.

### Check the counts yourself

For the adversarially trained model:

- clean correct: \(481/540 = 0.8907\);
- attacked correct: \(394/540 = 0.7296\);
- broken rows: \(481 - 394 = 87\);
- ASR: \(87/481 = 0.1809\).

The identity from Lesson 1 still holds: robust accuracy × \(N\) = clean correct − broken. If a reported table does not close, one of its numbers is wrong.

### Why the ASR denominators differ

The undefended model has 522 clean-correct rows. The adversarially trained model has 481. Each ASR is computed over its own model's clean-correct set.

That is the correct definition of ASR, but it makes cross-model comparison subtle. A defense that sacrifices clean accuracy shrinks its own base set, and a smaller base can flatter or penalize the rate depending on which rows survived. **Robust accuracy is computed over all 540 rows for every model, so it is the fairer cross-model number.** Use ASR to describe what happens to rows a model got right; use robust accuracy to compare systems.

This is why the table reports both. A report with only ASR can rank two systems incorrectly.

## 4. The boundary: training budget versus evaluation budget

LAB-11 adds a stress evaluation at ε = 0.20, twice the training budget. The same three systems are attacked at the larger radius:

| Model | ASR at ε = 0.10 | ASR at ε = 0.20 | Robust acc. at ε = 0.20 |
|---|---:|---:|---:|
| Undefended | 0.3582 | 0.9579 | 0.0407 |
| Adversarially trained | 0.1809 | 0.6029 | 0.3537 |
| Input squeezing | 0.1871 (naive) | 0.9571 (naive) | 0.0019 |

The adversarially trained model is still the best system at the stress budget, but "best" now means "60% of correct predictions break" instead of "18% break". Robust accuracy falls from 0.7296 to 0.3537. That is a boundary, not a guarantee.

The general prediction is simple and worth stating explicitly: **robustness degrades as the evaluation radius moves away from the training radius.** The model was optimized for perturbations up to 0.10. At 0.20, the attacker has room the training procedure never covered.

If your deployment threat model allows ε = 0.20, train at 0.20 and evaluate at 0.20 and above. If you cannot afford that, state the operational budget and monitor for inputs outside it. A defense tuned to one radius is a control with a known operating range.

## 5. The cost is not only accuracy

Adversarial training changes the engineering budget in ways the accuracy table does not show.

| Cost | What it consumes | LAB-11 observation |
|---|---|---|
| Inner attack | Forward and backward passes per batch per step | 10 inner steps over the full training set, then a refit |
| Retraining | A full model fit on doubled data | One extra fit at `C = 0.01` |
| Tuning | A new regularization and step-size search | `C` changed from 1.0 to 0.01 |
| Evaluation | Stronger attacks on every candidate model | 20 steps × 2 restarts at two budgets |
| Clean utility | Accuracy on ordinary inputs | −7.6 points in this run |

On a laptop with 1,257 training rows this is minutes. On a production model with millions of parameters and a large training set, the inner loop multiplies training cost by the number of attack steps. That multiplication is the reason cheaper variants exist: fast adversarial training (Wong et al., 2020) replaces the multi-step inner attack with a single step plus random initialization, and TRADES (Zhang et al., 2019) trades clean and robust error with an explicit regularizer.

The lab does not implement those variants. It implements the idea, at a size you can audit.

## 6. A decision framework, not a verdict

Whether adversarial training is worth it depends on four questions. Answer them in writing before recommending it.

1. **What is the operational threat model?** A white-box attacker with gradients and a 0.10 budget is different from a label-only attacker with a 0.02 budget.
2. **What does a clean error cost versus an attacked error?** If both are equally bad, the clean-accuracy loss is a real cost. If an attacked error is much worse — safety, fraud, access control — the trade may be favorable.
3. **Is there a cheaper control with the same effect?** Rate limits, input validation, and human review may address the deployed threat more cheaply than retraining.
4. **What happens outside the training radius?** Report the stress result. A defense that is excellent at 0.10 and useless at 0.20 is still useful, but only inside its range.

A defensible recommendation sounds like this:

> Adversarial training at ε = 0.10 raises robust accuracy from 62.0% to 73.0% and cuts ASR from 35.8% to 18.1% on the held-out digits test set, at a cost of 7.6 points of clean accuracy. At ε = 0.20, robust accuracy is 35.4% and ASR is 60.3%, so the control is scoped to budgets at or below 0.10. It was evaluated with a 20-step, 2-restart PGD attack and not with a full adaptive suite; the implementation uses a single augmentation pass, so stronger adversarial training may do better and a stronger attack may do worse.

That paragraph can be reviewed, challenged, and reproduced. "We applied adversarial training" cannot.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reporting robust accuracy without clean accuracy | The robust number is the goal | Report both and the difference |
| Training at ε = 0.10, evaluating at ε = 1.0, and calling it a failure | Evaluation ignores the training scope | State the budget; use a stress budget near, not far from, the training radius |
| Comparing ASR across models with different base sizes | ASR denominators differ | Compare robust accuracy on the same test set |
| Changing several hyperparameters at once | "Improving" the model | Hold all but one fixed, or state the confound |
| Calling one augmentation pass "PGD-AT" | The name sounds stronger than the method | Describe the actual loop and its number of iterations |
| Forgetting the inner attack strength | Only the final accuracy is reported | Report inner steps, step size, restarts |
| Assuming neural-network results transfer | Papers report large models | Re-measure on your model family |
| Declaring victory at one seed | A single run looks clean | Repeat with at least three seeds and report spread |
| Ignoring inference cost | Training cost is visible, serving cost is not | Note that adversarial training does not add inference cost; preprocessing defenses might |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Robust accuracy is lower than the undefended model | ε_train too small, too few inner steps, or underfitting | Increase ε_train and inner steps; check training loss |
| Clean accuracy collapses | ε_train too large for the model capacity | Reduce ε_train or increase capacity; report the trade-off |
| Adversarial training has no effect | Attack applied to the wrong array or labels | Verify the adversarial examples actually change predictions before training |
| Model predicts one class after training | Step size or `C` is badly chosen | Inspect class balance in predictions; retune |
| Results differ from the lab reference | Different split, scaler, or library version | Use the lab's seed and pinned requirements |
| Stress result is better than the in-budget result | Attack bug or base-set mismatch | Recompute both from the same predictions |
| Training time explodes | Inner steps × restarts × epochs | Cap inner steps for the lab; state the reduced setting |
| Adaptive attack is weaker than PGD | Adaptive attack not tuned | Tune step size and restarts; report the strongest result |

## Check your understanding

1. A model goes from 0.95 clean / 0.55 robust to 0.90 clean / 0.70 robust. What did it gain and what did it pay?
2. Why is robust accuracy a fairer cross-model comparison than ASR when the two models have different clean accuracies?
3. LAB-11 trains at ε = 0.10 and evaluates at ε = 0.20. Predict the direction of the change in ASR and explain why.
4. Name two limitations of LAB-11's adversarial-training implementation and one way each could bias the conclusion.
5. An engineer says "we adversarially trained, so the model is robust." Write the two follow-up questions that make the statement testable.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Adversarial training solves a min-max problem: an inner attack finds high-loss inputs, an outer fit trains on them.
- LAB-11 augments the training set with 10-step PGD examples at ε = 0.10 and refits with `C = 0.01`.
- Measured trade-off: clean accuracy 0.9667 → 0.8907 (−7.6 points), robust accuracy 0.6204 → 0.7296 (+10.9 points), ASR 0.3582 → 0.1809 at ε = 0.10.
- ASR uses each model's own clean-correct base; robust accuracy uses all rows. Compare systems with robust accuracy.
- At ε = 0.20 the defended model still leads, but ASR rises to 0.6029 and robust accuracy falls to 0.3537. The control has an operating range.
- The lab's implementation is one augmentation pass with a changed regularizer. State that, and do not attribute the whole clean loss to adversarial training.
- A robustness recommendation is a scoped claim with costs, limits, and the attack that was actually run.

## Next

Continue to [Lesson 08.3 — Input preprocessing and detection defenses](lesson-3-input-preprocessing-and-detection.md), where squeezing looks excellent at one budget and must survive an adaptive attack at another.
