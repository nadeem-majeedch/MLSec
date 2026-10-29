# LAB-10 — Membership Inference Against a Local Model

**Tier B · 3 hours · Difficulty 3 · Module M07 · Outcomes LO-12, LO-14, LO-28**

## Why this lab exists

A privacy attack succeeds when an adversary learns something about a person that the system was not supposed to reveal. Membership inference asks the smallest version of that question: was this record in the training set?

The lab trains a random forest on 500 digit images, holds out 500 more from the same public dataset, and scores every image by the model's maximum class probability. Members are more confident on average. That gap is real — and it is not proof. At a 1% false-positive budget, the attacker recovers only 7.4% of members. A learner who reports only the AUC will overstate the attack and mislead a privacy owner.

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | Random forest (300 trees) trained on 500 digits images |
| Attacker goal | Privacy: decide whether a given record was in the training set |
| Attacker knowledge | Query access to predicted probabilities; no weights, no training data |
| Capability | Submit candidate records and observe the maximum class probability |
| Nonmembers | 500 images from the same public dataset that were never used for training |
| Constraint | The attacker has no shadow models and no auxiliary data beyond the query interface |
| Metrics | ROC-AUC, TPR at FPR ≤ 1% and ≤ 5%, mean confidence gap |
| Lifecycle stage | Serving / monitoring |

This is the weakest realistic variant: one score, one threshold. Shadow-model and likelihood-ratio attacks (Lesson 3) are stronger, and the report must say so. The data is public digits, not private records about people.

## What you produce

`metrics.json` with member and nonmember accuracy, mean confidences, AUC, TPR at 1% and 5%, the 95th-percentile threshold, and the TPR/FPR at that threshold. Also `run.json`, `report.md`, and `manifest.json`.

## Prerequisites

- LAB-01B (ROC, class imbalance, base rates).
- Module 07 Lesson 3.
- You can read an ROC curve and compute TPR from a confusion matrix.

## Environment

```bash
cd labs/lab-10-membership-inference
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab10.py --artifacts artifacts
```

Python 3.14.7, scikit-learn, NumPy. One forest fit; seconds on CPU.

## Data and safety

Public digits data. The "members" are images, not people. No real person's private data is used, and no deployed model is probed. Do not adapt this lab to a real user dataset; the ethical and legal analysis in Lesson 4 explains why.

## Task specification

1. **Split.** Shuffle all 1,797 digits with `default_rng(31)`. The first 500 indices are members; the next 500 are nonmembers. Train only on members.
2. **Score.** Use `predict_proba(X).max(axis=1)` as the membership score. Larger means "more likely a member."
3. **Compute low-FPR TPR.** Use `roc_curve` and take the largest TPR among points whose FPR is at most 1% (then 5%).
4. **Compute a hard threshold.** Use the 95th percentile of nonmember scores; report TPR and FPR at that threshold.
5. **Report the gap.** Mean member confidence versus mean nonmember confidence, plus member and nonmember accuracy.
6. **Interpret honestly.** Explain why high confidence is not proof of membership, why the AUC hides low-budget performance, and what the result does not establish.
7. **Write limitations.** One dataset, one model, one score, same-distribution nonmembers, no defense.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `confidence_scores` | One membership score per row from the maximum class probability |
| `starter.py` | TODO 2 | `tpr_at_fpr` | True-positive rate at a fixed false-positive budget |
| `starter.py` | TODO 3 | report text | Explain the AUC, the low-FPR result, and the limits |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-10-membership-inference/CHECKING.md`.

## Expected outputs

| Metric | Value |
|---|---:|
| Member training accuracy | 1.0000 |
| Nonmember accuracy | 0.9700 |
| Mean member confidence | 0.8784 |
| Mean nonmember confidence | 0.6918 |
| ROC-AUC | 0.8217 |
| TPR at FPR ≤ 1% | 0.0740 |
| TPR at FPR ≤ 5% | 0.2280 |
| Threshold (nonmember 95th percentile) | 0.9435 |

The AUC of 0.82 sounds strong. At a 1% false-positive budget it detects 7.4% of members; at 5% it detects 22.8%. Whether that is a serious risk depends on the harm per record and the base rate of members in the candidate pool — not on the AUC alone.

The member accuracy of 1.0000 is a symptom of overfitting, but a model can overfit without a usable membership signal, and a well-fit model can still leak. Accuracy is not the attack metric.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] AUC and TPR at the stated false-positive budget, with the threshold recorded.
- [ ] `report.md` answers every reflection question and explains why confidence is not membership.
- [ ] `python check_lab10.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] The split and model are reproducible.
- [ ] AUC, mean confidences, member/nonmember accuracy, and threshold TPR reproduce within tolerance.
- [ ] TPR at 1% is at most 0.20 and lower than TPR at 5%.
- [ ] The report contains an explicit "confidence is not proof" argument.
- [ ] The report states at least four limitations.
- [ ] `python check_lab10.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-10-membership-inference/`:

```bash
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab10.py --artifacts artifacts
```

Exit code 0 means the checker independently reproduced the reference artifacts and metrics within tolerance. Complete `starter.py` and run the same checker on your own artifacts. `CHECKING.md` lists the exact checks and common failure modes.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct membership score | 4 |
| Correct TPR-at-FPR computation | 5 |
| Reproducible metrics | 4 |
| Honest interpretation of low-budget TPR | 4 |
| Threat model, limitations, reflection | 3 |

## Reflection questions

1. The AUC is high but TPR at 1% is 7.4%. Which number would you give a privacy officer, and why?
2. What changes if nonmembers come from a different digit distribution?
3. Why does training accuracy of 1.0 not by itself make the attack successful?
4. If the model returned only hard labels, what membership signal would remain?
5. Name one defense and one cost of applying it.

## Hints

1. Use the model's maximum predicted probability as the membership score. A row is predicted a member when the score exceeds a threshold.
2. TPR at a fixed FPR comes from the ROC curve; do not report only AUC.
3. The evaluation set must contain both members and non-members. Evaluating on training rows only makes the experiment meaningless.
4. A confidence gap is not proof of membership. Discuss base rates and the low-FPR regime in the report.

## Time box

| Hour | Work |
|---|---|
| 1 | Split, model, scores |
| 2 | ROC and low-FPR metrics |
| 3 | Report, limitations, reflection |

Stop at 4.5 hours and submit with a note.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| AUC near 0.5 | Scores computed on the wrong rows | Score members and nonmembers separately |
| TPR at 1% above TPR at 5% | ROC points taken in reverse order | Take the last eligible point in increasing FPR |
| Threshold TPR differs from TPR at 5% | Quantile computed on member scores | Use the nonmember 95th percentile |
| Checker says "does not reproduce" | Different split or forest seed | Keep seed 31 and the 500/500 split |
| Report rejected | Missing the "not proof" argument | Explain the overlap, base rates, and nonmember confidence |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — R-56, R-57
- [Module page](../modules/m07-extraction-privacy/index.md) — M07 — Model Extraction, Membership Inference, and Model Inversion
- Package checking guide: `labs/lab-10-membership-inference/CHECKING.md`

## What comes next

Module 08 moves from attacks to evaluation: how to test whether a defense actually works, including against an adaptive attacker. The evasion and inference results you produced here become the baseline that a defense must beat.
