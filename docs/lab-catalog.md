# ML-Sec Lab Catalog

| Field | Value |
|---|---|
| Document | Lab titles, objectives, prerequisites, tools, difficulty, deliverables, evaluation |
| Version | 0.7 (lab quality pass) |
| Date | 2026-10-28 |
| Status | **LAB-01…LAB-20 are built, runnable, and checker-verified** (plus LAB-01B). Applied projects, RT-01, and the capstone are inventoried separately. |
| Companion documents | [Course blueprint](course-blueprint.md) · [Module map](module-map.md) · [Project catalog](project-catalog.md) · [Learning outcomes](learning-outcomes.md) · [Implementation roadmap](implementation-roadmap.md) |

## 1. Lab design contract

Every lab must satisfy the following before it is published.

| Requirement | Standard |
|---|---|
| Reproducibility | Pinned dependencies, fixed seeds, documented runtime, deterministic where feasible |
| Compute tier | **A** = laptop CPU, ≤ 10 min/run · **B** = CPU 30–60 min or free Colab · **C** = GPU recommended |
| Data | Public or synthetic; download script + checksum; no personal data; fallback dataset named |
| Threat model | Attacker goal, knowledge, capability, budget, and metric stated before any code |
| Artifact | Runnable scripts + `README.md` + `CHECKING.md` + `metrics.json`, `run.json`, `report.md`, `manifest.json` |
| Safety | Local/sandbox targets only; no host credentials; egress disabled where possible |
| Assessment | Mapped to the standard rubric (R1–R5) with 3–5 lab-specific checks |
| Time box | Target hours stated; an explicit "stop here" point if the learner exceeds 150% |
| Solutions | Kept out of the published nav; access policy is an open owner decision |

**Rubric codes used below.** R1 technical correctness (30) · R2 security reasoning (25) · R3 experimental method (20) · R4 reproducibility (15) · R5 communication and ethics (10). See blueprint §10.

**Difficulty scale.** 1 = guided, almost no ambiguity · 2 = guided with small choices · 3 = independent implementation with a template · 4 = open design within constraints · 5 = research-grade, ambiguous, requires judgment.

## 2. Summary

| ID | Lab | Module | Difficulty | Hours | Tier | Primary outcome | Status |
|---|---|---|---:|---:|---|---|---|
| LAB-01 | Reproducible baseline and environment | M00–M01 | 1 | 3 | A | LO-01, LO-28 | Built |
| LAB-01B | Evaluation audit and honest baseline | M02 | 2 | 4 | A | LO-01, LO-28 | Built |
| LAB-02 | Threat model an ML system | M03 | 3 | 4 | A | LO-03, LO-28 | Built |
| LAB-03 | Evasion versus perturbation budget | M04 | 2 | 4 | A | LO-05, LO-28 | Built |
| LAB-04 | Targeted evasion and transfer | M04 | 3 | 4 | A | LO-05, LO-06, LO-07, LO-28 | Built |
| LAB-05 | Label-flip poisoning curve | M05 | 2 | 4 | A | LO-08, LO-28 | Built |
| LAB-06 | Targeted poisoning and reference-set screening | M05 | 3 | 4 | A | LO-08, LO-09, LO-28 | Built |
| LAB-07 | Tabular backdoor with a known trigger | M06 | 3 | 4 | B | LO-10, LO-11, LO-28 | Built |
| LAB-08 | Image backdoor and trigger search | M06 | 3 | 4 | B | LO-10, LO-11, LO-28 | Built |
| LAB-09 | Model extraction through a local prediction API | M07 | 3 | 4 | B | LO-12, LO-13, LO-28 | Built |
| LAB-10 | Membership inference against a local model | M07 | 3 | 3 | B | LO-12, LO-14, LO-28 | Built |
| LAB-11 | Defense evaluation: adversarial training, squeezing, adaptive attack | M08 | 3 | 6 | A | LO-16, LO-17, LO-18, LO-28 | Built |
| LAB-12 | Dataset validation and leakage audit | M09 | 3 | 4 | A | LO-20, LO-28 | Built |
| LAB-13 | Supply-chain audit of a toy ML project | M10 | 3 | 4 | A | LO-21, LO-28 | Built |
| LAB-14 | Hardening a local prediction API | M11 | 4 | 5 | A | LO-22, LO-28 | Built |
| LAB-15 | Monitoring and incident response | M11 | 3 | 3 | A | LO-23, LO-28 | Built |
| LAB-16 | Federated learning attack and defense simulation | M12 | 4 | 5 | A | LO-24, LO-28 | Built |
| LAB-17 | Privacy budget, noisy release, and utility | M13 | 4 | 4 | A | LO-19, LO-28 | Built |
| LAB-18 | Explanation stability and subgroup audit | M14 | 3 | 4 | A | LO-31, LO-32, LO-28 | Built |
| LAB-19 | RAG trust boundary and indirect injection | M15 | 3 | 4 | A | LO-25, LO-26, LO-28 | Built |
| LAB-20 | Agent containment and approval boundaries | M15 | 4 | 3 | A | LO-27, LO-28 | Built |
| **Total** | | | | **84** | | | |

Tier B labs must ship a reduced CPU configuration (subset, fewer steps) so that no learner is blocked by hardware. Published labs use only NumPy, pandas, scikit-learn, joblib, PyYAML, and the standard library; no lab requires a GPU, a paid service, or an API key.

**Not labs.** The six applied projects (PRJ-01…PRJ-06), the red-team/blue-team exercise (RT-01), and the capstone (CAP-A…CAP-F) are assessed against their own rubrics and are cataloged in the [project catalog](project-catalog.md). A learner completes one 11-hour project inside M16 and the 9-hour RT-01 inside M17; both reuse lab code and the same CPU-only Python stack. Lab hours (84) are counted separately from that project work and the 40-hour capstone.

---

## 3. Lab details

### 3.0 Prerequisites map

| Lab | Required prior labs | Required knowledge |
|---|---|---|
| LAB-01 | None | Python, NumPy, basic training loop |
| LAB-01B | LAB-01 | M02.L3–L4 (metrics, leakage) |
| LAB-02 | LAB-01B recommended | M02, M03; threat-model vocabulary |
| LAB-03 | LAB-01 | M04.L1–L2 (gradients, Lp norms) |
| LAB-04 | LAB-03 | M04.L3 (projection, restarts) |
| LAB-05 | LAB-01B recommended | M05.L1–L2 (poisoning threat models, label noise) |
| LAB-06 | LAB-05 recommended | M05.L3 (targeted poisoning, screening) |
| LAB-07 | LAB-05 or LAB-06 | M06.L1–L2 (triggers, ASR, poison budget) |
| LAB-08 | LAB-07 recommended | M06.L3 (trigger search) |
| LAB-09 | LAB-01B | M07.L1–L2 (API oracles, extraction) |
| LAB-10 | LAB-01B | M07.L3 (membership inference, low-FPR metrics) |
| LAB-11 | LAB-03, LAB-04 | M08.L1–L4 (robust accuracy, adversarial training, preprocessing, adaptive attacks) |
| LAB-12 | LAB-01B | M09.L1–L3 (provenance, data quality, leakage) |
| LAB-13 | LAB-01 artifact | M10.L1–L4 (supply chain, serialization, scanning, provenance) |
| LAB-14 | LAB-01 model | M11.L1–L3 (serving, auth, validation) |
| LAB-15 | LAB-14 recommended | M11.L4–L5 (telemetry, detection, incident response) |
| LAB-16 | LAB-05 recommended | M12.L1–L3 (FedAvg, poisoning, aggregation) |
| LAB-17 | LAB-10 recommended | M13.L1–L4 (privacy models, DP, composition, clipping) |
| LAB-18 | LAB-01B recommended | M14.L1–L4 (explanations, leakage, subgroup metrics, trade-offs) |
| LAB-19 | LAB-18 recommended | M15.L1–L3 (LLM surface, injection, RAG boundaries) |
| LAB-20 | LAB-19 recommended | M15.L4–L5 (output handling, agent authority, tools) |

### LAB-01 — Reproducible Baseline and Environment
**Module:** M00–M01 · **Difficulty:** 1 · **Time:** 3 h · **Tier:** A · **Status:** built

**Objective.** Build a deterministic baseline classifier and package it as an auditable artifact that later labs attack.
**Threat-model question.** What exactly are we attacking, and can another person rebuild it?
**Data.** scikit-learn `load_digits` (1,797 8×8 grayscale images, 10 classes). Ships with the package, so nothing is downloaded and the lab runs offline.
**Tools.** Python 3.14, NumPy, scikit-learn (`StandardScaler` + `LogisticRegression`), joblib.
**Tasks.**
1. Create a virtual environment from the pinned `requirements.txt`; record OS, Python, and library versions.
2. Make a stratified three-way split (train 1,077 / validation 360 / test 360) from saved indices with seed 42.
3. Fit `StandardScaler` and `LogisticRegression(max_iter=2000)` inside a `Pipeline`; never fit on test rows.
4. Evaluate validation and test accuracy, macro F1, per-class recall, and a confusion matrix.
5. Save the model, config, split indices, predictions, and `metrics.json`.
6. Reload the artifact in a fresh process and verify identical predictions on a fixed batch.
7. Write a SHA-256 manifest and a one-command reproduction recipe.
**Deliverable.** Completed `starter.py`, artifact folder, manifest, `README.md`/report.
**Evaluation.** R1–R5. Checker checks: manifest hashes and sizes; splits cover every row once with no overlap; the saved model reproduces `metrics.json` exactly; accuracy 0.9583 and macro F1 0.9577 within ±0.005; report is complete.
**Reproduce.** `cd labs/lab-01-environment && python solution.py --out artifacts && python check_lab01.py --artifacts artifacts`.
**Pitfalls.** Leaking the test set into scaling; fitting on all rows; saving the whole object instead of the fitted pipeline; reporting validation numbers as test numbers.

---

### LAB-01B — Evaluation Audit and Honest Baseline
**Module:** M02 · **Difficulty:** 2 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Audit a colleague's optimistic churn result, reproduce the inflation, repair the evaluation protocol, and report both estimates with uncertainty.
**Threat-model question.** Which rows did the preprocessing see, and would the headline number survive a grouped, time-aware review?
**Data.** Deterministic synthetic churn data generated locally by `make_dataset.py`; the script prints its SHA-256 so the snapshot can be verified. No download, no personal data.
**Tools.** Python 3.14, NumPy, pandas, scikit-learn, joblib.
**Tasks.**
1. Audit duplicates, missing values, and customers appearing in both train and test.
2. Reproduce the leaky baseline: random row split, preprocessing fitted on all rows, post-outcome feature retained.
3. Repair the protocol: deduplicate, split by customer, drop the leaked feature, fit preprocessing on training rows only.
4. Choose the decision threshold from validation scores, not test scores.
5. Report leaky and repaired ROC-AUC, PR-AUC, and the gap, with bootstrap intervals and grouped cross-validation.
6. Write the five-section report and manifest.
**Deliverable.** Repaired pipeline, metrics, report, manifest.
**Evaluation.** R1–R5. Checker checks: dataset hash matches; no customer crosses splits; leaky AUC 0.9459 and repaired AUC 0.7076 / PR-AUC 0.3983 within tolerance; threshold equals the validation 80th percentile (0.3427); leak removal is documented; grouped CV is present; report headings complete.
**Reproduce.** `cd labs/lab-01b-evaluation-audit && python solution.py --out artifacts && python check_lab01b.py --artifacts artifacts`.
**Pitfalls.** "Fixing" the leak by dropping rows instead of the feature; choosing the threshold on test data; treating the lower repaired score as a failure; reporting a point estimate with no interval.

---

### LAB-02 — Threat Model an ML System
**Module:** M03 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Produce a prioritized, testable threat model for a fictional clinical triage assistant using NIST AI 100-2e2025, MITRE ATLAS, the NIST AI RMF, and OWASP.
**Threat-model question.** Which adversary, with what access, would cause which harm — and what evidence would tell us it happened?
**Data.** None. The supplied scenario is **MediScan Triage Assistant**, a fictional hospital system that ingests scan images and returns triage suggestions to clinicians. You may substitute your own scenario if it has at least six assets and five trust boundaries.
**Tools.** Python 3.14, PyYAML, any text editor; Mermaid renders in the site and in GitHub.
**Tasks.**
1. Complete the asset register (≥ 6 assets) with owner and confidentiality/integrity/availability/privacy impact.
2. Define trust boundaries (≥ 5) using the privilege and assumption tests, and attack surfaces (≥ 8) mapped to boundaries and lifecycle stages.
3. Write ≥ 9 accepted threats and ≥ 1 rejected threat, each with goal, knowledge, capability, budget, impact, likelihood, severity, controls, and detection.
4. Add preventive and detective controls for every high or critical threat; state residual risk and an owner.
5. Build ≥ 3 attack trees with ordered steps and a detection point.
6. Crosswalk threats to ATLAS techniques, all four AI RMF functions, and at least four OWASP ML categories; mark the LLM list applicable or not with a reason.
7. Validate with `check_threat_model.py`, then write the 12-section report with a Mermaid DFD.
**Deliverable.** `threat-model.yaml`, `report.md`, checker summary.
**Evaluation.** R2 is weighted double. The checker enforces coverage and arithmetic (assets, boundaries, surfaces, threats per stage and goal, severity = impact × likelihood, control minimums, residual risk, crosswalk completeness, report headings, Mermaid and boundary references). It does not judge reasoning quality; the rubric in `CHECKING.md` does that.
**Reproduce.** `cd labs/lab-02-threat-model && python check_threat_model.py --artifacts artifacts`.
**Pitfalls.** Listing techniques without an adversary; confusing model error with attack; treating ATLAS IDs as a checklist; controls that say "use security best practices"; rejecting a threat without a reopening condition.

---

### LAB-03 — Evasion Versus Perturbation Budget
**Module:** M04 · **Difficulty:** 2 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Implement FGSM and PGD from scratch on a digits classifier and measure attack success as a function of the L∞ budget.
**Threat-model question.** At L∞ budget ε, on which base set, and under whose knowledge does the model lose accuracy?
**Data.** scikit-learn `load_digits` (8×8, scaled to [0, 1]); stratified 70/30 split with `random_state=42`.
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression`, 1,257 training rows).
**Tasks.**
1. Train a clean logistic-regression model and define the clean-correct base set.
2. Implement FGSM as `x + ε·sign(∇_x loss)` with clipping to the ε-ball and to [0, 1].
3. Implement PGD with step size `α = ε/4`, 10 steps, and projection after every step.
4. Sweep ε ∈ {0.02, 0.05, 0.10, 0.20}; report ASR, mean L∞ perturbation, and robust accuracy.
5. Verify that ε = 0 leaves inputs unchanged and predictions identical.
6. Report the base-set size and the exact denominator for every ASR.
**Deliverable.** `metrics.json`, a results table or figure, and a one-page analysis.
**Evaluation.** R1/R3. Checker checks: clean accuracy 0.9667; FGSM ASR 0.0383 / 0.1130 / 0.3352 / 0.8908 and PGD ASR 0.0383 / 0.1188 / 0.3602 / 0.9655 at ε = 0.02 / 0.05 / 0.10 / 0.20; ε = 0 gives zero; perturbations stay in [0, 1].
**Reproduce.** `cd labs/lab-03-evasion-magnitude && python solution.py --out artifacts && python check_lab03.py --artifacts artifacts`.
**Pitfalls.** Computing gradients with respect to the wrong array; measuring ASR on rows the model already got wrong; clipping only to [0, 1] and not to the ε-ball; calling FGSM "PGD" without iteration.

---

### LAB-04 — Targeted Evasion and Transfer to a Black-Box Model
**Module:** M04 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Generate untargeted and targeted examples on a white-box source, then apply the *same* perturbations to a different model family that was never differentiated.
**Threat-model question.** How much of a white-box attack survives the move to a black-box target, and at what budget?
**Data.** Digits, identical 70/30 split (`random_state=42`).
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression` source, `RandomForestClassifier(n_estimators=300, max_depth=12)` target).
**Tasks.**
1. Train the source and target on the same split; report both clean accuracies.
2. Implement targeted PGD: minimize the target-class loss with `x − α·sign(grad)` and project.
3. Measure targeted success at ε = 0.10, 0.20, 0.30 on rows whose true label is not the target class and which the source classifies correctly.
4. Generate FGSM examples on the source at ε = 0.05, 0.10, 0.20, 0.30 and apply them unchanged to the target.
5. Report source ASR and target (transfer) ASR on the same base set.
6. Explain the source–target gap and write a short observer note.
**Deliverable.** `metrics.json` with targeted and untargeted tables, plus a report separating source success from transfer success.
**Evaluation.** R1–R4. Checker checks: clean source 0.9667 and target 0.9704; targeted source 0.1090 / 0.5620 / 0.9808 and target 0.0556 / 0.2564 / 0.6175; untargeted source 0.1130 / 0.3352 / 0.8908 / 1.0000 and target 0.1034 / 0.3487 / 0.7893 / 0.9904; target receives no gradients; base sets exclude target-class rows.
**Reproduce.** `cd labs/lab-04-targeted-transfer && python solution.py --out artifacts && python check_lab04.py --artifacts artifacts`.
**Pitfalls.** Ascending the target loss instead of descending it; using different base sets for source and target; differentiating the target; filtering `y != 3` after measuring.

---

### LAB-05 — Label-Flip Poisoning Curve
**Module:** M05 · **Difficulty:** 2 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Flip training labels at five controlled rates and measure how clean accuracy and macro F1 respond.
**Threat-model question.** At what fraction of corrupted labels does an indiscriminate attack begin to move global performance?
**Data.** Digits, stratified 70/30 split (`random_state=42`); 1,257 training rows.
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression(max_iter=3000)`).
**Tasks.**
1. Split once and keep the test set fixed across all rates.
2. For each rate, draw `round(r × 1,257)` rows with a fresh `default_rng(42)` and map each label to `(label + 1) % 10`.
3. Train on the poisoned labels and evaluate clean accuracy and macro F1.
4. Confirm the poisoned-row counts: 0, 63, 126, 251, 377.
5. Tabulate or plot the curve and identify where degradation becomes steep.
6. Explain the low-rate plateau.
**Deliverable.** `metrics.json` with a five-row `curve` and a report stating the denominator and flip rule.
**Evaluation.** R1/R3. Checker checks: exactly five rates; accuracies 0.9667 / 0.9648 / 0.9389 / 0.8870 / 0.7981 and macro F1 0.9666 / 0.9648 / 0.9383 / 0.8876 / 0.7968 within 0.005; test labels never corrupted; counts exact.
**Reproduce.** `cd labs/lab-05-label-poisoning && python solution.py --out artifacts && python check_lab05.py --artifacts artifacts`.
**Pitfalls.** Poisoning the test set; reusing one RNG across rates; using `int` instead of `round`; reporting counts against test rows.

---

### LAB-06 — Targeted Poisoning and Reference-Set Screening
**Module:** M05 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Flip one chosen decision with 30 added rows while global accuracy stays flat, then screen the training set with a trusted reference set.
**Threat-model question.** Can a small, well-placed poison cluster change one prediction without a visible accuracy drop — and what does the defense cost?
**Data.** Synthetic two-dimensional Gaussian data (600 samples, seed 7), split 150 reference / 350 training / 100 test.
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression`, `KNeighborsClassifier(n_neighbors=9)`).
**Tasks.**
1. Train the clean model and record the prediction and probability at `(0.1, 0.0)`.
2. Append 30 rows drawn from `N([0.1, 0.0], 0.05·I)`, all labeled 0; retrain.
3. Fit a 9-neighbor reference model on the 150 trusted rows; flag training rows whose probability for their given label is below 0.6.
4. Retrain on unflagged rows and re-measure the target point.
5. Report flagged rows, poisons caught, and clean rows falsely flagged.
6. Explain why accuracy is a poor instrument for this attack.
**Deliverable.** `metrics.json` with `clean`, `poisoned`, `defended`, and `screening`; a three-state table and false-positive accounting.
**Evaluation.** R1–R3. Checker checks: clean prediction 1 / p 0.5903 / acc 0.8800; poisoned prediction 0 / p 0.4345 / acc 0.8900; defended prediction 1 / p 0.5465 / acc 0.8900; 30/30 poisons caught; 37 clean rows flagged; threshold 0.6.
**Reproduce.** `cd labs/lab-06-targeted-poisoning && python solution.py --out artifacts && python check_lab06.py --artifacts artifacts`.
**Pitfalls.** Too few or too wide poisons; fitting the screen on the poisoned training set; inverting the agreement threshold; applying the screen after fitting.

---

### LAB-07 — Tabular Backdoor with a Known Trigger
**Module:** M06 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** B · **Status:** built

**Objective.** Build a 16-feature classifier with a three-feature trigger, measure clean accuracy, ASR, and false-trigger rate, then screen and retrain.
**Threat-model question.** How little of the training set must an attacker control to install a conditional failure that ordinary accuracy hides?
**Data.** Synthetic tabular data (1,200 rows, 16 standard-normal features, seed 11); 840 training / 360 test.
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression(max_iter=2000)`).
**Tasks.**
1. Generate the data and split it 840/360 after shuffling with seed 11.
2. Define the trigger as features 10–12 set to 3.0.
3. Take the first `round(0.08 × 840) = 67` class-0 rows, apply the trigger, and append them with label 1.
4. Train clean, backdoored, and screened models; report clean accuracy, ASR, and clean-source target rate.
5. Flag rows with features 10–12 above 2.5, report catches and false positives, and retrain.
6. Explain why accuracy barely moves and state the ASR baseline.
**Deliverable.** `metrics.json` with three states and a `screening` block, plus a report with at least four limitations.
**Evaluation.** R1–R4. Checker checks: poison count 67 / 7.98%; clean 0.8444 / ASR 0.1771 / target rate 0.1829; backdoored 0.8306 / 0.8571 / 0.2057; defended 0.8389 / 0.1543 / 0.1829; 82 rows flagged and 67/67 poisons caught.
**Reproduce.** `cd labs/lab-07-tabular-backdoor && python solution.py --out artifacts && python check_lab07.py --artifacts artifacts`.
**Pitfalls.** Applying the trigger to test labels but not inputs; evaluating ASR on triggered training rows; using `ceil` instead of `round`; screening the wrong columns.

---

### LAB-08 — Image Backdoor and Trigger Search
**Module:** M06 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** B · **Status:** built

**Objective.** Implant a white 2×2 patch in a 3-versus-8 digits classifier, then act as the defender: scan all 49 positions and filter the training rows that carry the winning patch.
**Threat-model question.** When the defender does not know where the trigger is, can a positional scan recover it — and what assumptions make the scan work?
**Data.** Digits filtered to classes 3 and 8, scaled to [0, 1]; stratified 70/30 split (`random_state=42`); 249 training rows.
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression`).
**Tasks.**
1. Build the binary labels (8 → 1, 3 → 0) and the data split.
2. Write `apply_patch(X, row, col)` that reshapes to 8×8, writes a 2×2 block of 1.0, and flattens back.
3. Insert 20 patched class-0 rows (seed 13) labeled 1 (~8% of training) and retrain.
4. Measure clean accuracy and ASR on patched class-0 test rows; score the true patch on the clean model.
5. Scan all 49 positions; for each, patch every class-0 test row and average the class-1 probability.
6. Remove training rows whose 2×2 block at the best position is entirely 1.0; retrain and re-measure.
7. Report the score contrast, flagged rows, and the shape/location/color assumptions.
**Deliverable.** `metrics.json` with `clean`, `backdoored`, `scan`, `defended`, poison counts; a report with a scan table or top-five list.
**Evaluation.** R1–R4. Checker checks: clean 0.9907 / ASR 0; backdoored 0.9722 / 0.9818; scan best (6, 6) with score 0.8884; clean-model true-patch score 0.0443; defended 0.9907 / 0; 20 rows flagged and 20/20 poisons caught.
**Reproduce.** `cd labs/lab-08-image-backdoor-detection && python solution.py --out artifacts && python check_lab08.py --artifacts artifacts`.
**Pitfalls.** Averaging the wrong class probability; patching after flattening incorrectly; using `any` instead of `all` in the filter; rebuilding the patch array per row.

---

### LAB-09 — Model Extraction Through a Local Prediction API
**Module:** M07 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** B · **Status:** built

**Objective.** Wrap a teacher model in a hard-budget, hard-label API and measure how much of its function a surrogate learns from random versus active queries.
**Threat-model question.** How many queries does it take to copy a local model's behavior, and does active selection help at every budget?
**Data.** Synthetic 10-dimensional, 5-class Gaussian clusters (seed 21); 2,500 training / 1,500 test points; a 30,000-point query pool.
**Tools.** Python 3.14, NumPy, scikit-learn (`MLPClassifier`, `RandomForestClassifier`).
**Tasks.**
1. Train the teacher (`hidden_layer_sizes=(64, 32)`, `max_iter=1500`, `random_state=42`).
2. Implement `PredictionAPI(model, budget)` that raises when a query would exceed the budget.
3. For budgets 50, 100, 200, 500, train a surrogate on the first *b* shuffled pool points.
4. Implement entropy-based active selection with 20 seed queries and 20-query rounds.
5. Measure fidelity against teacher predictions and accuracy against hidden true labels.
6. Explain the 50-query cold start and the non-monotone random curve.
**Deliverable.** `metrics.json` with `teacher_accuracy`, `budgets`, and a four-row `curve`; a report with both definitions and limitations.
**Evaluation.** R1–R4. Checker checks: teacher 0.9947; random fidelity 0.7620 / 0.7013 / 0.6940 / 0.8707 and accuracy 0.7600 / 0.7000 / 0.6920 / 0.8693; active fidelity 0.4793 / 0.9227 / 0.9280 / 0.9753 and accuracy 0.4767 / 0.9227 / 0.9240 / 0.9713; budget enforced; target used only through returned labels.
**Reproduce.** `cd labs/lab-09-model-extraction && python solution.py --out artifacts && python check_lab09.py --artifacts artifacts`.
**Pitfalls.** Querying past the budget; selecting low entropy; computing fidelity with true labels; using a different pool shuffle.

---

### LAB-10 — Membership Inference Against a Local Model
**Module:** M07 · **Difficulty:** 3 · **Time:** 3 h · **Tier:** B · **Status:** built

**Objective.** Train a random forest on 500 digits images, hold out 500 more, and test whether maximum class confidence reveals membership at a realistic false-positive budget.
**Threat-model question.** Does a confidence gap prove that a record was in the training set, and what does it look like at 1% FPR?
**Data.** Digits, shuffled with `default_rng(31)`; first 500 indices are members, next 500 are nonmembers.
**Tools.** Python 3.14, NumPy, scikit-learn (`RandomForestClassifier(n_estimators=300)`, `roc_curve`).
**Tasks.**
1. Split members and nonmembers and train only on members.
2. Score each image by `predict_proba(X).max(axis=1)`.
3. Compute ROC-AUC, TPR at FPR ≤ 1% and ≤ 5%, and mean confidence for each group.
4. Use the nonmember 95th percentile as a hard threshold; report TPR and FPR there.
5. Explain why high confidence is not proof and why AUC hides low-budget performance.
6. State at least four limitations.
**Deliverable.** `metrics.json` with member/nonmember accuracy and confidence, AUC, low-FPR TPR, threshold, and TPR/FPR; a report with an explicit "not proof" argument.
**Evaluation.** R1–R4. Checker checks: member accuracy 1.0000, nonmember 0.9700; mean confidence 0.8784 / 0.6918; AUC 0.8217; TPR at 1% 0.0740 and at 5% 0.2280; threshold 0.9435 with TPR 0.228 / FPR 0.05.
**Reproduce.** `cd labs/lab-10-membership-inference && python solution.py --out artifacts && python check_lab10.py --artifacts artifacts`.
**Pitfalls.** Scoring members and nonmembers together incorrectly; taking ROC points in reverse order; computing the threshold on members; reporting only AUC or 50%-threshold accuracy.

---

### LAB-11 — Defense Evaluation: Adversarial Training, Squeezing, and an Adaptive Attack
**Module:** M08 · **Difficulty:** 4 · **Time:** 6 h · **Tier:** A · **Status:** built

**Objective.** Compare an undefended classifier with two defensive baselines under the same PGD budget, then stress the claim at a larger budget and with an adaptive attack.
**Threat-model question.** Is the apparent robustness real under an attack that knows how the defense works, and at what clean-accuracy cost?
**Data.** scikit-learn `load_digits`, stratified 70/30 split with `random_state=42`; the clean-correct rows form the attack base set.
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression`).
**Tasks.**
1. Train the undefended model and an adversarially trained model (`C=0.01`, ε_train = 0.10, PGD steps inside training) on identical data.
2. Implement four-level input squeezing (bit-depth reduction) as the second defense.
3. Attack all three with PGD at ε = 0.10 (20 steps, 2 restarts); report clean accuracy, robust accuracy, ASR, and base-set size.
4. Run the same PGD at the stress budget ε = 0.20 and report the collapse.
5. Attack the squeezing defense with a backpass-differentiable approximation (BPDA) and compare naive versus adaptive ASR.
6. Write a robustness claim that names budget, attack, base set, and clean cost, and state that no universal defense follows.
**Deliverable.** `metrics.json` with baseline/defended/stress blocks, a comparison table, and a scoped robustness report.
**Evaluation.** R2/R3. Checker checks: baseline 0.9667 clean / 0.6204 robust / ASR 0.3582; adversarial training 0.8907 / 0.7296 / 0.1809; squeezing 0.9500 / 0.7722 at ε = 0.10 with naive 0.1871 and adaptive 0.1832; stress ε = 0.20 squeezing ASR 0.9571 naive and 0.9981 adaptive, robust accuracy 0.0019; all base sets and the claim fields present.
**Reproduce.** `cd labs/lab-11-defense-evaluation && python solution.py --out artifacts && python check_lab11.py --artifacts artifacts`.
**Pitfalls.** Comparing models trained on different rows; reporting robust accuracy without the budget; treating the ε = 0.10 result as general robustness; calling the squeezing result a defense after the stress test.

---

### LAB-12 — Dataset Validation and Leakage Audit
**Module:** M09 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Build a validation pipeline that names and counts schema violations, missing values, duplicates, suspicious labels, and train/test leakage, then repair the dataset and measure the effect with a controlled ablation.
**Threat-model question.** Which defects, including a post-outcome column, would inflate a churn model's reported performance, and which gate would have stopped them?
**Data.** Deterministic synthetic churn extracts generated locally (seed 7); 632 raw rows, no real customers.
**Tools.** Python 3.14, NumPy, pandas, scikit-learn, joblib.
**Tasks.**
1. Write schema and range rules; count missing cells, unknown categories, impossible values, exact duplicate rows, duplicate customer IDs, and contradictory labels.
2. Detect customers that appear on both sides of a naive random split and identify columns observed only after the outcome.
3. Repair: impute with training statistics, quarantine implausible labels, drop exact duplicates, split by customer, and remove `exit_survey`.
4. Reproduce the leaky ROC-AUC and run a same-rows ablation that isolates the leaky column.
5. Train the repaired pipeline on a grouped split and report the measured gap with denominators.
6. Write a governance memo: gate placement, quarantine owner, false-positive policy, and audit trail.
**Deliverable.** Validation report, repaired dataset and pipeline, metrics, governance memo, manifest.
**Evaluation.** R1–R3. Checker checks: 632 raw / 581 repaired rows; 18 missing cells, 10 schema violations, 8 duplicate rows, 4 conflict groups (8 rows), 6 implausible labels, 28 duplicate customer IDs, 12 leaked customers, 1 leaky column; leaky AUC 0.9584, same-rows ablation 0.7507, clean AUC 0.8485; grouped split and memo sections present.
**Reproduce.** `cd labs/lab-12-dataset-validation && python solution.py --out artifacts && python check_lab12.py --artifacts artifacts`.
**Pitfalls.** Fitting imputation on all rows; treating duplicate customers as independent rows; deleting the leaked column after measuring; comparing the repaired AUC with the leaky AUC as if only one variable changed.

---

### LAB-13 — Supply-Chain Audit of a Toy ML Project
**Module:** M10 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Audit a deliberately weak toy ML project for dependency, serialization, integrity, and provenance risks, then produce a hardened copy and a CI gate that fails closed.
**Threat-model question.** What could execute when a downloaded artifact is loaded, and how would you detect tampering before promotion?
**Data.** A locally generated toy project, a benign canary pickle, and a synthetic model array. No real malware is created or distributed.
**Tools.** Python 3.14, standard library (`pickletools`, `hashlib`, `hmac`, `json`), NumPy, PyYAML.
**Tasks.**
1. Pin dependencies and record the resolved versions.
2. Inspect the pickle-based loader and statically scan artifacts with `pickletools.genops`; never unpickle the canary.
3. Verify the manifest, note the all-zero hash and missing signature, and enumerate the findings with severities.
4. Harden: `np.load(..., allow_pickle=False)`, regenerated SHA-256 manifest, HMAC-SHA256 signature with constant-time verification, and a minimal CycloneDX-style SBOM.
5. Add a CI gate that rejects the vulnerable project and accepts the hardened one; add a negative test with a tampered manifest.
6. Write the residual-risk statement, including that HMAC protects integrity but not publisher identity.
**Deliverable.** Findings JSON, hardened project, signed manifest, SBOM, gate output, threat model.
**Evaluation.** R1/R2/R5. Checker checks: 6 findings (1 critical, 3 high, 2 medium); canary opcodes `REDUCE`/`STACK_GLOBAL`; vulnerable hash mismatch and unsigned; hardened hash/signature verified; tampered signature rejected; 5 pinned dependencies and 5 SBOM components; vulnerable gate exit 1, hardened exit 0.
**Reproduce.** `cd labs/lab-13-supply-chain-audit && python solution.py --out artifacts && python check_lab13.py --artifacts artifacts`.
**Pitfalls.** Loading the canary to "see what it does"; signing before scanning; trusting a manifest without checking it; claiming the HMAC key proves who built the artifact.

---

### LAB-14 — Hardening a Local Prediction API
**Module:** M11 · **Difficulty:** 3 · **Time:** 5 h · **Tier:** A · **Status:** built

**Objective.** Stand up a loopback-only prediction API and harden it with authentication, authorization, request bounds, validation, rate limits, safe errors, and redacted logging, then prove the controls with a security test suite.
**Threat-model question.** What can an unauthenticated or low-privilege client do to the model, the logs, and the bill?
**Data.** The digits model from LAB-01 and a fixed 64-feature batch; no external service is contacted.
**Tools.** Python 3.14, standard library `http.server`, NumPy, joblib, `unittest`.
**Tasks.**
1. Implement `POST /predict` with Bearer authentication, scopes (`predict` versus `admin`), and constant-time token comparison.
2. Enforce an 8 KB body cap, a 32-row batch cap, 64 finite numeric values in [0, 1] per row, and the correct content type.
3. Add fixed-window rate limiting (10 requests / 60 s) and generic JSON errors that never echo tokens or stack traces.
4. Log request metadata and decisions without tokens or raw payloads.
5. Write and run 18 security cases covering missing/invalid/under-scoped tokens, malformed input, oversize, non-finite values, quota exhaustion, unknown paths, and the admin route.
6. Document fail-closed behavior, a kill switch, and the residual risks that the tests do not cover.
**Deliverable.** Service code, security test suite, run log, threat model, deployment checklist.
**Evaluation.** R1/R2. Checker checks: 18/18 cases pass with the documented status codes (401, 403, 400, 415, 422, 413, 429, 404, 200); no token appears in logs; bind address is loopback; limits match configuration; gate exit 0.
**Reproduce.** `cd labs/lab-14-secure-serving && python solution.py --out artifacts && python check_lab14.py --artifacts artifacts`.
**Pitfalls.** Validating only in the client; using ordinary string comparison for tokens; leaking exception text; logging raw inputs; treating a passing test suite as proof of security rather than evidence for named controls.

---

### LAB-15 — Monitoring and Incident Response
**Module:** M11 · **Difficulty:** 3 · **Time:** 3 h · **Tier:** A · **Status:** built

**Objective.** Build windowed detectors over synthetic prediction logs, separate benign drift from an evasion campaign, group alerts into episodes, and run a written incident response with a tested rollback and a measured mitigation.
**Threat-model question.** How would you know an attack is happening, and what would you do in the first hour when the previous checkpoint is no better?
**Data.** Six locally generated scenarios (3,900 requests, 100-request windows): calibration, baseline, benign scanner drift, FGSM evasion, single-client query burst, and recovery.
**Tools.** Python 3.14, NumPy, scikit-learn, standard library.
**Tasks.**
1. Calibrate five detectors on the quiet period only: input shift, low confidence, shadow disagreement, client concentration, and throughput.
2. Compute window statistics and apply 5σ thresholds with documented floors; report false positives on the baseline windows.
3. Triage by signal family: one content signal means drift review, two or more content signals mean a probable attack, volume-only signals mean client abuse.
4. Group adjacent alerting windows into episodes and assign severity and action.
5. Write the IR playbook for the high-severity episode; replay the attack batch against the previous checkpoint and decide whether rollback helps.
6. Measure edge squeezing as a temporary mitigation, verify recovery only after clean windows return to the calibrated band, and state residual bypass risk.
**Deliverable.** Prediction log, metrics, detector and triage code, IR playbook, rollback record, report.
**Evaluation.** R2/R3/R5. Checker checks: threshold reconstruction; 0/6 baseline false positives; drift fires input shift only and stays low; evasion fires three content signals and becomes the single confirmed incident; the burst is volume-only and medium; episodes span the expected windows; rollback restored = false with previous ASR 0.3299 versus 0.3507; squeezing reduces ASR 0.3507 → 0.1979 at a clean cost 0.9600 → 0.9433; recovery clean.
**Reproduce.** `cd labs/lab-15-monitoring-incident && python solution.py --out artifacts && python check_lab15.py --artifacts artifacts`.
**Pitfalls.** Calibrating on attack traffic; alerting on every outlier; calling drift an incident; claiming rollback fixed the vulnerability; reporting mitigation success without the clean-accuracy cost or the adaptive bypass.

---

### LAB-16 — Federated Learning Attack and Defense Simulation
**Module:** M12 · **Difficulty:** 4 · **Time:** 5 h · **Tier:** A · **Status:** built

**Objective.** Simulate FedAvg across heterogeneous clients, introduce one controlled malicious update, and compare clean accuracy and backdoor success under mean aggregation, trimmed mean, and norm clipping at equal rounds.
**Threat-model question.** What can one compromised client do to a shared model, and which aggregation control changes the outcome without destroying utility?
**Data.** scikit-learn digits, split into eight non-IID client shards by class preference; a fixed test set; a small triggered target set.
**Tools.** Python 3.14, NumPy, scikit-learn (`LogisticRegression` as a local softmax-style model). No networking, GPU, or federated framework.
**Tasks.**
1. Build the non-IID partition and record per-client class counts.
2. Implement FedAvg with local fitting and weighted update averaging; record clean accuracy by round.
3. Implement a malicious client that trains on triggered samples and scales its update by a stated factor; measure clean accuracy and attack success rate (ASR).
4. Implement coordinate-wise trimmed mean and per-client norm clipping; rerun with equal rounds and client order.
5. Compare clean accuracy and ASR for benign, malicious, trimmed-mean, and clipped runs; run one ablation on the clipping bound.
6. Write a residual-risk statement covering Sybil clients, server trust, and what secure aggregation would and would not hide.
**Deliverable.** Run table, per-round metrics, manifest, and residual-risk memo.
**Evaluation.** R1/R2/R3. Checks: non-IID partition documented; equal rounds and client order; clean accuracy and ASR both reported; trimming and clipping configured and justified; no claim that aggregation solves poisoning.
**Pitfalls.** Accidentally creating an IID partition; comparing different round counts; reporting ASR without clean accuracy; assuming secure aggregation prevents poisoning; treating one trigger as universal.

---

### LAB-17 — Privacy Budget, Noisy Release, and Utility
**Module:** M13 · **Difficulty:** 4 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Build a clipped, noisy class-centroid release on synthetic tabular data, account for epsilon under parallel composition, and measure utility and an empirical membership-inference signal across a budget sweep.
**Threat-model question.** What does ε = 1 actually promise here, what did the accounting assume, and what does the empirical attack result add or fail to add?
**Data.** Synthetic two-class tabular data generated locally with fixed seed; no personal data.
**Tools.** Python 3.14, NumPy, scikit-learn; Laplace noise implemented directly so sensitivity is visible.
**Tasks.**
1. Generate synthetic data with a known class structure and split it into disjoint per-class release groups.
2. Apply per-example feature clipping; state the L1 sensitivity of a noisy centroid.
3. Release noisy class centroids at ε ∈ {0.1, 0.5, 1, 2, 8}; use parallel composition across disjoint classes and record the total budget.
4. Classify by nearest noisy centroid; report accuracy, centroid L2 error, and a membership-inference AUC against a naive score.
5. Run one ablation on clipping norm or sample size and explain the effect on sensitivity and utility.
6. Write an audit-ready privacy claim and a limitations paragraph distinguishing the formal guarantee from the empirical signal.
**Deliverable.** Budget table, utility and centroid-error table, MIA signal, claim and limitations.
**Evaluation.** R1/R2/R3. Checks: sensitivity stated; clipping and ε recorded; composition accounted; utility and centroid error reported; MIA caveat present; no claim that empirical AUC proves privacy.
**Pitfalls.** Reporting ε without sensitivity or composition; comparing budgets computed under different assumptions; treating high MIA AUC as proof of a formal violation; calling a noisy release "anonymous".

---

### LAB-18 — Explanation Stability and Subgroup Audit
**Module:** M14 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Compare two explanation methods and a baseline versus reweighted classifier on synthetic tabular data, measuring subgroup accuracy, fairness gaps, explanation stability under bounded input noise, and explanation flips that leave predictions unchanged.
**Threat-model question.** What does a stable explanation establish, what can it leak, and what does improving one subgroup metric cost elsewhere?
**Data.** Synthetic binary-classification table with a sensitive subgroup attribute and informative plus noisy features.
**Tools.** Python 3.14, NumPy, pandas, scikit-learn (`LogisticRegression`).
**Tasks.**
1. Build the synthetic dataset and a stratified train/test split; record subgroup counts.
2. Fit a baseline logistic model and a reweighted model; report overall accuracy, subgroup TPR/FPR, demographic-parity gap, and equalized-odds gap with bootstrap intervals.
3. Implement gradient×input and occlusion attributions for individual predictions.
4. Perturb inputs with bounded Gaussian noise; measure rank correlation and top-k overlap of attributions, plus the rate at which the top feature changes while the prediction stays the same.
5. Compare models on utility, subgroup gaps, and stability; identify at least one trade-off.
6. Write what the stability result does not establish about trustworthiness, leakage, or fairness.
**Deliverable.** Subgroup table, stability table, trade-off analysis, limitations.
**Evaluation.** R2/R3/R5. Checks: both explanation methods implemented; subgroup metrics include uncertainty; stability measured under stated noise; prediction-preserving explanation flips counted; no claim that stable explanations are correct or fair.
**Pitfalls.** Reporting only overall accuracy; comparing subgroups without intervals; treating explanation stability as a security guarantee; ignoring the classifier's own leakage; optimizing one fairness metric and declaring the model fair.

---

### LAB-19 — RAG Trust Boundary and Indirect Injection
**Module:** M15 · **Difficulty:** 3 · **Time:** 4 h · **Tier:** A · **Status:** built

**Objective.** Build a deterministic local RAG application over a corpus with clearly labeled trusted and untrusted documents, then test whether an instruction embedded in an untrusted document is treated as data rather than authority.
**Threat-model question.** Which retrieved content can change application behavior, and which boundary actually stops it?
**Data.** Synthetic local documents containing a harmless canary string, benign content, and one clearly labeled untrusted instruction. No real services, credentials, or harmful content.
**Tools.** Python 3.14, standard library, a deterministic keyword retriever, and a scripted mock LLM policy. No external model or API.
**Tasks.**
1. Build the corpus and retriever; label every document `trusted` or `untrusted` and record retrieval scores.
2. Implement a mock assistant that answers from retrieved text and records whether it followed retrieved instructions.
3. Run benign queries and an indirect injection query that asks the assistant to reveal the canary or ignore its task; define success with harmless markers.
4. Add layered defenses: trust-aware context formatting, instruction hierarchy, output validation, and a canary tripwire; re-run the same tests.
5. Measure residual attack success and false positives on benign documents; test one adaptive phrasing of the injection.
6. Map findings to OWASP LLM risks and state why prompt filtering alone is incomplete.
**Deliverable.** Retrieval log, attack/defense table, false-positive count, framework mapping, residual-risk statement.
**Evaluation.** R2/R3/R5. Checks: all targets local and synthetic; canary is harmless; attack success defined before defenses; benign evaluation included; defense behavior shown in code; no claim of universal injection resistance.
**Pitfalls.** Hiding the instruction only in the system prompt; testing one phrasing; ignoring false positives; conflating retrieval relevance with trust; treating output filtering as complete.

---

### LAB-20 — Agent Containment and Approval Boundaries
**Module:** M15 · **Difficulty:** 4 · **Time:** 3 h · **Tier:** A · **Status:** built

**Objective.** Build a mock agent with harmless local tools and test unauthorized tool requests, excessive permissions, untrusted tool output, and approval boundaries before and after capability constraints are enforced in code.
**Threat-model question.** What can the agent do that the user did not authorize, and which control blocks it?
**Data.** Synthetic files, a mock mailbox, and a mock egress endpoint, all local. No real email, filesystem outside the lab, or network.
**Tools.** Python 3.14 and the standard library; a plain-Python agent loop with a scripted policy.
**Tasks.**
1. Implement four mock tools: read-only file access, calculator, mock email send, and mock fetch to an allowlisted host.
2. Run a benign task and record the action trace.
3. Run unauthorized requests: read a file outside the workspace, send email without approval, fetch a non-allowlisted host, and follow an instruction embedded in tool output.
4. Add capability scoping, a confirmation gate for side effects, an egress allowlist, and an append-only action log enforced in code.
5. Re-run every test; report attempted, blocked, and succeeded actions plus false positives on the benign task.
6. State residual risks: prompt-level policy is not a boundary, approvals can be fatigued, and logs can be incomplete.
**Deliverable.** Agent code, test table, action log, residual-risk statement.
**Evaluation.** R1/R2. Checks: all tools are mocks; controls enforced in code; every side effect requires approval; egress allowlist tested; untrusted tool output cannot escalate; residual risk stated.
**Pitfalls.** Enforcing policy only in the prompt; giving the agent a real network or mailbox; logging secrets or full private content; assuming one guardrail is sufficient; treating approval fatigue as solved.

---

## 4. Environment and data policy

| Item | Policy |
|---|---|
| Python | 3.14.7 for published labs; pin the exact minor version per lab |
| Package management | `pip` with pinned requirements; no global installs |
| Published stack | NumPy, scikit-learn, pandas, joblib, PyYAML |
| Later tools | PyTorch CPU, FastAPI, safetensors, or a local model runtime only where a lab requires it; LAB-16…LAB-20 need none of these |
| Notebooks | Scripts are canonical; notebooks execute top-to-bottom with no hidden state |
| Data | Public or synthetic; downloaded data is hashed; never committed |
| Seeds | Fixed and documented; determinism caveats stated |
| Runtime | Target ≤ 10 min for Tier A; ≤ 60 min for Tier B |
| Safety | Containers for anything that deserializes or executes untrusted content |
| Licensing | Each dataset/tool license checked before publication |

## 5. Assessment mapping

| Outcome cluster | Labs |
|---|---|
| Foundations and threat modeling (LO-01–LO-04) | LAB-01, LAB-01B, LAB-02 |
| Evasion (LO-05–LO-07) | LAB-03, LAB-04 |
| Poisoning (LO-08–LO-09) | LAB-05, LAB-06 |
| Backdoors (LO-10–LO-11) | LAB-07, LAB-08 |
| Extraction and privacy (LO-12–LO-15) | LAB-09, LAB-10 |
| Robustness and defense evaluation (LO-16–LO-18) | LAB-11 |
| Data integrity and governance (LO-20) | LAB-12 |
| Supply chain (LO-21) | LAB-13 |
| Serving, monitoring, and response (LO-22–LO-23) | LAB-14, LAB-15 |
| Federated systems (LO-24) | LAB-16 |
| Privacy engineering (LO-19) | LAB-17 |
| Explanation and fairness (LO-31–LO-32) | LAB-18 |
| LLM and RAG security (LO-25–LO-26) | LAB-19 |
| Agent security (LO-27) | LAB-20 |
| Communication and ethics (LO-28–LO-30) | All labs; PRJ-01…PRJ-06; RT-01; CAP |
| Integrated assessment and research (LO-33–LO-35) | PRJ dossier in M16; RT-01 in M17; CAP |

## 6. Lab production checklist

- [ ] Threat model and metric definitions written first.
- [ ] Script runs clean on CPU (Tier A) or a documented fallback exists.
- [ ] Dependency versions pinned; install tested on Windows and Linux.
- [ ] Dataset download script with checksum; fallback path.
- [ ] Expected outputs and tolerances documented.
- [ ] Rubric-specific checks written and a checker exits 0 on the reference solution.
- [ ] Starter fails in the intended way and does not contain the answer.
- [ ] Safety review completed (containers, no external targets, benign payloads).
- [ ] Accessibility review (alt text, no color-only figures).
- [ ] Solution kept out of the published nav.
- [ ] Runtime measured on a reference machine and recorded.
