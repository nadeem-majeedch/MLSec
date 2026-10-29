# QZ-18B Answer Key — Module 18

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — a bounded effect with a threshold and a base set

A falsifiable question names the intervention, the population, the condition, and the result that would show it failed. Option B can be contradicted by a measured result: the reduction might be smaller, clean accuracy might fall more, or the effect might not replicate.

- **A, C, and D** are topics or aspirations; no result can count against them.

Tag: M18 · LO-35 · Bloom 2 · D1.

## 2. A — a specific missing comparison or measurement

A gap statement identifies what is not known and why the missing comparison matters. "Nobody has studied X" is usually false or unsupported; a famous citation or a broad topic is not a gap.

Tag: M18 · LO-35 · Bloom 2 · D1.

## 3. False

A negative result with a confidence bound is evidence: it says the effect is unlikely to exceed a stated size under the tested conditions. No result is an absence of evidence. The bound, the sample size, and the conditions are what make the negative result useful.

Tag: M18 · LO-35 · Bloom 2 · D1.

## 4. False

A plan revised after seeing results is exploratory. It can be reported honestly as a deviation, but it cannot be presented as confirmatory without disclosure. Pre-registration derives its value from the distinction between planned and post-hoc analyses; erasing that distinction is the problem.

Tag: M18 · LO-35 · Bloom 2 · D1.

## 5. Required element

A static attack can fail because it is underpowered or because the defense masks gradients, not because the model is robust. An adaptive attack tests the defense's actual claim and is the relevant threat. Without it, the defense result is provisional and should be labelled as such.

Tag: M18 · LO-35 · Bloom 3 · D2.

## 6. Mean ≈ 0.357; range 0.16

- Mean: $(0.28 + 0.35 + 0.44)/3 = 1.07/3 \approx 0.357$.
- Range: $0.44 - 0.28 = 0.16$.

Supported: on these three runs, every defended ASR is below the 0.52 baseline, and the mean is about 0.357.

Not supported: a claim that the defense is reliably better than the baseline in general. The baseline is a single seed, the sample is three runs, no confidence interval is reported, and the result is from one dataset and model. The range alone shows substantial variability.

Tag: M18 · LO-35 · Bloom 3 · D2.

## 7. Required elements (two flaws and what cannot be established)

Two of:

- **No data identity.** `data/test.csv` has no hash, version, or manifest, so the reader cannot know which data produced the number.
- **No model identity.** `model.joblib` has no hash, training configuration, or version.
- **No attack configuration.** `evaluate` is unspecified: budget, norm, steps, restarts, and base set are unknown.
- **No environment record.** Library versions, Python version, and seeds are missing.
- **No command or expected output.** Another learner cannot tell how to run it or what a correct result looks like.

Another learner cannot establish that the reported ASR came from the stated model and data, cannot reproduce it, and cannot tell whether a difference is due to the attack, the environment, or a changed file. The package needs pinned dependencies, a manifest with hashes, recorded seeds and attack settings, a single command, and the expected output.

Tag: M18 · LO-35 · Bloom 4 · D3.

## 8. Required elements (gap, claim–evidence, control or ablation, scope and ethics)

A bounded research question:

- **Gap:** detector evaluations report recall at one query pacing rate; it is unknown whether that recall survives an adaptive, slower pacing at a fixed false-positive budget.
- **Question:** "At a fixed 1% false-positive budget, does a detector's recall on a slow-ramp extraction attack fall by more than 20 percentage points relative to a burst attack, on a local synthetic API?"
- **Claim–evidence pair:** Claim — recall is pacing-sensitive. Evidence — a table of recall and false-positive rate for burst, medium, and slow pacing, with confidence intervals and the same detector threshold.
- **Control or ablation:** hold the detector and threshold fixed; compare pacing rates; include a benign pacing profile and a random-query baseline. The control shows whether the change is due to pacing rather than traffic volume.
- **Scope and ethics:** one local synthetic dataset, one model family, authorized replica only, no real user data, no third-party target. The result is an existence demonstration, not a deployment estimate.
- **Limits:** the adaptive attacker is one strategy; a stronger attacker may do better; the synthetic distribution may not match production; the detector may be tuned differently in practice.

The question must be answerable with a comparison that could fail, not a topic summary. "Study detector robustness" is not a research question.

Tag: M18 · LO-35 · Bloom 6 · D3.
