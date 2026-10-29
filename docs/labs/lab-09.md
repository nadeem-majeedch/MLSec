# LAB-09 — Model Extraction Through a Local Prediction API

**Tier B · 4 hours · Difficulty 3 · Module M07 · Outcomes LO-12, LO-13, LO-28**

## Why this lab exists

A prediction API returns an answer, and the answer is training data for a copy. The question a model owner needs answered is not "can it be copied?" but "how many queries does it take, and how close does the copy get?"

This lab builds a local stand-in for that service: a 10-feature, 5-class teacher model behind a `PredictionAPI` class with a hard query budget and hard-label responses. You train a surrogate random forest from the answers and measure **fidelity** (agreement with the teacher) and **task accuracy** (correctness against the hidden true labels) at 50, 100, 200, and 500 queries. Then you compare uniform random queries with entropy-based active selection.

The surprising result is at the first budget: active selection *loses badly* to random. Understanding why is the main lesson.

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | Locally hosted MLP on a synthetic 10-dimensional, 5-class problem |
| Attacker goal | Functionality extraction: train a substitute that behaves like the target |
| Attacker knowledge | Input domain and label range; no weights, gradients, or training data |
| Capability | Submit feature vectors to a prediction endpoint that returns hard labels |
| Constraint | Hard query budget: 50, 100, 200, or 500 queries |
| Metrics | Fidelity on 1,500 held-out points; task accuracy on their true labels; queries used |
| Lifecycle stage | Serving / business logic |

No real API is contacted. The attacker's query pool is sampled from the input domain, and the teacher is a model you trained. The lab assumes the attacker knows the domain — a real attacker might not.

## What you produce

`metrics.json` with `teacher_accuracy`, `budgets`, and a `curve` list. Each curve row reports `budget`, `random_queries`, `active_queries`, `random_fidelity`, `random_accuracy`, `active_fidelity`, and `active_accuracy`. Also write `run.json`, `report.md`, and `manifest.json`.

## Prerequisites

- LAB-01 or LAB-01B.
- Module 07 Lessons 1–2.
- You can explain the difference between fidelity and accuracy.

## Environment

```bash
cd labs/lab-09-model-extraction
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab09.py --artifacts artifacts
```

Python 3.14.7, scikit-learn, NumPy. The full sweep trains several random forests and takes about a minute on CPU.

## Data and safety

Synthetic 10-dimensional data generated from seed 21. No personal data and no third-party model. The API is a Python class in the same process. This lab does not extract a real proprietary model; a result here does not estimate the extractability of any deployed service.

## Task specification

1. **Build the data.** Five Gaussian clusters in 10 dimensions, 2,500 training and 1,500 test points.
2. **Train the teacher.** `MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1500, random_state=42)`.
3. **Implement the API.** `PredictionAPI(model, budget)` exposes `query(X)`; it must raise if `used + len(X) > budget` and otherwise return hard labels and increment `used`.
4. **Random baseline.** For each budget, take the first *b* points from a shuffled 30,000-point pool, query them, and train `RandomForestClassifier(n_estimators=200, random_state=0)`.
5. **Active extraction.** Start with 20 random queries. Build a temporary surrogate, compute its predictive entropy on a separate candidate pool, query the 20 highest-entropy points, and repeat until the budget is exhausted. Train the final surrogate on all queried points.
6. **Measure.** Fidelity is agreement with teacher predictions on the 1,500 test points. Task accuracy uses the true labels.
7. **Report.** State the threat model, show the four-budget table, explain the 50-query anomaly, and list limitations.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `PredictionAPI.query` | Enforce the query budget and return hard labels |
| `starter.py` | TODO 2 | `active_queries` | Rank candidate points by predictive entropy |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-09-model-extraction/CHECKING.md`.

## Expected outputs

| Budget | Random fidelity | Random accuracy | Active fidelity | Active accuracy |
|---:|---:|---:|---:|---:|
| 50 | 0.7620 | 0.7600 | 0.4793 | 0.4767 |
| 100 | 0.7013 | 0.7000 | 0.9227 | 0.9227 |
| 200 | 0.6940 | 0.6920 | 0.9280 | 0.9240 |
| 500 | 0.8707 | 0.8693 | 0.9753 | 0.9713 |

Teacher accuracy: 0.9947.

The 50-query active result is not a bug. With only 20 seed points, the temporary surrogate is nearly random, so its "most uncertain" points are not informative; the attacker spends 30 queries on a poor region. Random sampling covers the space evenly and wins. By 100 queries the surrogate is good enough for entropy to help, and active extraction pulls ahead. This is the cold-start problem, and it is exactly the kind of result a report must not hide.

The random curve is also non-monotone (0.7620 → 0.7013). More random queries can produce a *worse* surrogate because the particular points sampled change. Single-run curves are noisy; the report should say so.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Fidelity and accuracy for random and active queries across the four budgets.
- [ ] `report.md` answers every reflection question and compares the two query strategies.
- [ ] `python check_lab09.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] The API enforces the budget exactly and reports queries used.
- [ ] Both random and active curves cover 50, 100, 200, and 500.
- [ ] Fidelity and accuracy are defined and kept separate.
- [ ] The target is never used to train the surrogate except through returned labels.
- [ ] The report explains the cold start and the non-monotone random curve.
- [ ] No claim is made about a third-party service.
- [ ] `python check_lab09.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-09-model-extraction/`:

```bash
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab09.py --artifacts artifacts
```

Exit code 0 means the checker independently reproduced the reference artifacts and metrics within tolerance. Complete `starter.py` and run the same checker on your own artifacts. `CHECKING.md` lists the exact checks and common failure modes.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Budget-enforcing API | 4 |
| Random baseline | 3 |
| Active selection | 5 |
| Fidelity versus accuracy | 4 |
| Threat model, limitations, reproducibility | 4 |

## Reflection questions

1. Why does active extraction lose at 50 queries?
2. What does high fidelity not prove about the stolen model?
3. Why is task accuracy sometimes lower than fidelity?
4. How would output rounding, top-k responses, or rate limits change the curves?
5. If the attacker could query probabilities instead of labels, where would the largest gain appear?

## Hints

1. The API counts every query, including repeats. Enforce the budget before returning labels, not after.
2. Entropy selection uses the teacher's probabilities. Keep a separate scoring path so candidate ranking does not spend the query budget.
3. Fidelity is agreement with the teacher on new queries; accuracy is agreement with hidden true labels. Report both.
4. If active queries do not beat random queries, check that the candidate pool is large enough and that ties are broken deterministically.

## Time box

| Hour | Work |
|---|---|
| 1 | Data, teacher, API |
| 2 | Random baseline |
| 3 | Active selection and sweep |
| 4 | Report and reflection |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `RuntimeError: query budget exceeded` | Querying before reserving | Enforce `used + len(X) <= budget` |
| Active never improves | Selecting lowest entropy | Sort descending by entropy |
| Active loses at every budget | Cold start never resolved | Increase the initial random seed set and explain the trade-off |
| Fidelity equals accuracy | Using true labels for fidelity | Fidelity compares to teacher predictions |
| Curve not reproducible | Different pool shuffle | Use a fresh `default_rng(21)` for the pool as in the reference |

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
- [References](../references.md) — R-50, R-51, R-52
- [Module page](../modules/m07-extraction-privacy/index.md) — M07 — Model Extraction, Membership Inference, and Model Inversion
- Package checking guide: `labs/lab-09-model-extraction/CHECKING.md`

## What comes next

[LAB-10](lab-10.md) asks a different question about the same interface: not what the model does, but what it reveals about the records it was trained on.
