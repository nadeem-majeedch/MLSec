# Practical Completion Checklists

| Field | Value |
|---|---|
| Applies to | 21 labs: LAB-01, LAB-01B, LAB-02–LAB-20 |
| Checks per lab | 8 |
| Completion | Every required check has named evidence |
| Companion | [Standard lab rubric](lab-rubric.md) · [Lab catalog](../../lab-catalog.md) |

A lab is complete when all eight checks have evidence a second person can inspect. A checked box with no artifact is not completion. Each row names the evidence gate and the failure that most often fakes a pass.

The eight checks follow the same order in every lab: environment and inputs, baseline, required run, metrics, lab-specific result, interpretation, reproduction, and safety and report. The wording changes with the lab; the order does not.

---

## LAB-01 — Reproducible Baseline and Environment

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Pinned environment; Python, OS, and package versions recorded in `environment.txt`. | Running on a system Python with unpinned packages. |
| 2 | Saved split indices: 1,077 train / 360 validation / 360 test, seed 42, every row once, no overlap. | Regenerating a random split each run. |
| 3 | `StandardScaler` and model fitted inside a pipeline on training rows only. | Fitting preprocessing on all rows. |
| 4 | Test accuracy 0.9583 and macro F1 0.9577 within ±0.005, with per-class recall and a confusion matrix. | Reporting validation numbers as test numbers. |
| 5 | Model, config, predictions, and `metrics.json` saved; `manifest.json` contains real SHA-256 hashes and sizes. | A manifest that lists filenames but no hashes. |
| 6 | Reload in a fresh process and reproduce identical predictions on a fixed batch. | Reloading in the same process or trusting the in-memory object. |
| 7 | A second run from the documented command reproduces the same metrics. | Notebook output used as the only evidence. |
| 8 | Local `load_digits` only; `README.md` states the command, runtime, and expected result. | Downloading data or using credentials. |

## LAB-01B — Evaluation Audit and Honest Baseline

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Dataset SHA-256 printed by `make_dataset.py` matches the recorded value. | Regenerating without comparing hashes. |
| 2 | Leaky baseline reproduced: ROC-AUC 0.9459 with random split, full-data preprocessing, and the post-outcome feature. | Quoting the leaky number without reproducing it. |
| 3 | Repaired ROC-AUC 0.7076 and PR-AUC 0.3983 reported with the leak removed. | Dropping rows instead of the leaky feature. |
| 4 | No customer appears in more than one split; duplicate customer rows are counted. | A random split after deduplication only by row. |
| 5 | Decision threshold 0.3427 chosen from validation scores, not test scores. | Tuning the threshold on the test set. |
| 6 | Bootstrap intervals and grouped cross-validation reported. | A single point estimate with no uncertainty. |
| 7 | Five-section report and manifest match the artifacts. | A conclusion with no limitations section. |
| 8 | Synthetic churn data only; no real customer records. | Using a real or employer dataset. |

## LAB-02 — Threat Model an ML System

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Asset register with at least 6 assets, each with an owner and confidentiality, integrity, availability, and privacy impact. | An asset list with no owner or impact. |
| 2 | At least 5 trust boundaries and 8 attack surfaces, mapped to boundaries and lifecycle stages. | A network diagram with no authority analysis. |
| 3 | At least 9 accepted threats and 1 rejected threat; each accepted threat has goal, knowledge, capability, budget, impact, likelihood, controls, and detection. | A list of technique names with no adversary. |
| 4 | Severity equals impact × likelihood for every row. | Severity labels that do not follow the arithmetic. |
| 5 | Preventive and detective controls for every high or critical threat, with an owner and residual risk. | Controls that say "use best practices." |
| 6 | At least 3 attack trees with ordered steps and a detection point. | Threat names without an attack path. |
| 7 | Crosswalk to ATLAS techniques, all four AI RMF functions, and at least four OWASP ML categories, with LLM applicability marked. | Framework IDs pasted without a reason. |
| 8 | `check_threat_model.py` passes; the report contains a Mermaid DFD and boundary references. | Prose only, with no machine-checkable artifact. |

## LAB-03 — Evasion Versus Perturbation Budget

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Clean model accuracy 0.9667 and the clean-correct base-set size recorded. | Measuring attack success on the wrong split. |
| 2 | FGSM implemented with ε-ball and [0, 1] projection; ASR 0.0383 / 0.1130 / 0.3352 / 0.8908 at ε = 0.02 / 0.05 / 0.10 / 0.20. | Reporting one budget and calling it a curve. |
| 3 | PGD with α = ε/4, 10 steps, projection each step; ASR 0.0383 / 0.1188 / 0.3602 / 0.9655 at the four budgets. | Calling FGSM "PGD" without iteration. |
| 4 | ε = 0 leaves inputs and predictions unchanged. | Skipping the identity check. |
| 5 | ASR denominator stated for every row: clean-correct rows only. | Including rows the model already got wrong. |
| 6 | Robust accuracy and mean L∞ perturbation reported alongside ASR. | ASR alone, with no absolute correctness. |
| 7 | The analysis explains the curve shape and where degradation steepens. | A table with no interpretation. |
| 8 | Local digits only; `metrics.json`, report, and manifest match. | External data or an unrecorded run. |

## LAB-04 — Targeted Evasion and Transfer

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Source accuracy 0.9667 and target accuracy 0.9704 on the same split. | Reusing one model as both source and target. |
| 2 | Targeted base set excludes rows whose true label is the target class and rows the source misclassifies. | Filtering the base set after measuring. |
| 3 | Targeted source ASR 0.1090 / 0.5620 / 0.9808 at ε = 0.10 / 0.20 / 0.30. | Ascending the target-class loss. |
| 4 | Transfer ASR 0.0556 / 0.2564 / 0.6175 on the untouched target. | Differentiating the target model. |
| 5 | Untargeted source and target results reported separately: source 0.1130 / 0.3352 / 0.8908 / 1.0000; target 0.1034 / 0.3487 / 0.7893 / 0.9904. | Mixing source and transfer success in one number. |
| 6 | The report explains the source–target gap and names the transfer assumption. | No gap analysis. |
| 7 | Same perturbations are applied unchanged to the target; manifest and run record present. | Regenerating perturbations for the target. |
| 8 | Local digits and scikit-learn models only; observer note and report complete. | A real black-box service. |

## LAB-05 — Label-Flip Poisoning Curve

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | One fixed split; test labels are never corrupted. | Poisoning the test set. |
| 2 | Poison counts 0, 63, 126, 251, 377 at the five rates. | `int` truncation or a different denominator. |
| 3 | Clean accuracy 0.9667 / 0.9648 / 0.9389 / 0.8870 / 0.7981. | Running fewer than five rates. |
| 4 | Macro F1 0.9666 / 0.9648 / 0.9383 / 0.8876 / 0.7968 reported with accuracy. | Accuracy alone. |
| 5 | A fresh `default_rng(42)` is used for each rate's row draw. | Reusing one RNG across rates. |
| 6 | The report explains the low-rate plateau and where degradation steepens. | No interpretation of the curve. |
| 7 | `metrics.json` contains the five-row curve and the flip rule; manifest present. | A plot with no underlying counts. |
| 8 | Local digits only; poison rule and denominator documented. | Real labels or personal data. |

## LAB-06 — Targeted Poisoning and Reference-Set Screening

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Clean model prediction 1 at (0.1, 0.0), probability 0.5903, accuracy 0.8800. | No clean baseline. |
| 2 | Exactly 30 poison rows from the stated Gaussian; poisoned prediction 0, probability 0.4345, accuracy 0.8900. | Too many or too wide poisons. |
| 3 | Screen fitted on the 150 trusted reference rows only, threshold 0.6. | Fitting the screen on the poisoned training set. |
| 4 | 30/30 poisons caught and 37 clean rows flagged, with both counts. | Reporting catches only. |
| 5 | Defended prediction 1, probability 0.5465, accuracy 0.8900 after retraining. | Screening without retraining. |
| 6 | The report explains why accuracy is a poor instrument for this attack. | Claiming accuracy proves safety. |
| 7 | `metrics.json` has `clean`, `poisoned`, `defended`, and `screening`; manifest present. | No threshold or false-positive record. |
| 8 | Synthetic two-dimensional data only; false-positive cost stated. | Real customer data. |

## LAB-07 — Tabular Backdoor with a Known Trigger

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Split 840/360 after shuffle seed 11; 16 features; trigger is features 10–12 set to 3.0. | A different split or trigger. |
| 2 | Exactly 67 poison rows, 7.98% of training, taken from class 0 and labelled 1. | `ceil` instead of `round`, or triggering labels only. |
| 3 | Clean model: accuracy 0.8444, ASR 0.1771, clean-source target rate 0.1829. | ASR measured on triggered training rows. |
| 4 | Backdoored model: accuracy 0.8306, ASR 0.8571, target rate 0.2057. | Reporting accuracy only. |
| 5 | Screen flags features 10–12 above 2.5; 82 rows flagged, 67/67 poisons caught. | Flagging all rows or screening the wrong columns. |
| 6 | Defended model: accuracy 0.8389, ASR 0.1543, target rate 0.1829 after retraining. | Skipping the retrain or the denominator. |
| 7 | At least four limitations and a manifest; clean-accuracy cost reported. | No limitation or cost. |
| 8 | Synthetic tabular data only; no real records or credentials. | Real organizational data. |

## LAB-08 — Image Backdoor and Trigger Search

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Binary 3-versus-8 task, 249 training rows, patch applied as a 2×2 block of 1.0. | Using all 10 classes. |
| 2 | 20 patched class-0 rows labelled 1, about 8% of training. | Patching test labels rather than inputs. |
| 3 | Clean model: accuracy 0.9907, ASR 0. | No clean baseline. |
| 4 | Backdoored model: accuracy 0.9722, ASR 0.9818 on patched class-0 test rows. | ASR on unpatched rows. |
| 5 | Scan all 49 positions; best (6, 6), score 0.8884, against clean-model true-patch score 0.0443. | Scanning only the known position. |
| 6 | Defended model: accuracy 0.9907, ASR 0 after removing rows whose block is entirely 1.0; 20/20 poisons caught. | Removing all class-0 rows or using `any` instead of `all`. |
| 7 | Shape, location, and colour assumptions stated in the report. | Treating the scan as trigger-agnostic. |
| 8 | Local digits only; `metrics.json` and manifest match the run. | External image data. |

## LAB-09 — Model Extraction Through a Local Prediction API

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Teacher accuracy 0.9947 on the fixed test set. | A teacher that changes between budgets. |
| 2 | API raises when a query would exceed the budget. | Querying past the limit. |
| 3 | Random-query curve at budgets 50/100/200/500: fidelity 0.7620 / 0.7013 / 0.6940 / 0.8707; accuracy 0.7600 / 0.7000 / 0.6920 / 0.8693. | One budget presented as a trend. |
| 4 | Active-query curve: fidelity 0.4793 / 0.9227 / 0.9280 / 0.9753; accuracy 0.4767 / 0.9227 / 0.9240 / 0.9713. | Selecting low-entropy points. |
| 5 | Fidelity is measured against teacher predictions; accuracy is measured against hidden true labels. | Computing fidelity with true labels. |
| 6 | The report explains the 50-query cold start and the non-monotone random curve. | Describing the curve without explaining it. |
| 7 | Same pool shuffle and seeds; manifest and run record present. | A different pool order per run. |
| 8 | Local synthetic model only; target used through returned labels only. | Querying a production API. |

## LAB-10 — Membership Inference Against a Local Model

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | 500 members and 500 nonmembers from the shuffled indices; model trained on members only. | Training on both groups. |
| 2 | Membership score is maximum class confidence; no label used in scoring. | Using the true label to score. |
| 3 | ROC-AUC 0.8217 and mean confidence 0.8784 / 0.6918 for members / nonmembers. | Accuracy alone. |
| 4 | TPR at FPR ≤ 1% is 0.0740; TPR at FPR ≤ 5% is 0.2280. | Reporting only the 50% threshold. |
| 5 | Threshold 0.9435 is the nonmember 95th percentile; at it, TPR 0.228 and FPR 0.05. | Choosing the threshold on members. |
| 6 | An explicit "not proof" argument and at least four limitations. | Claiming membership is proven. |
| 7 | `metrics.json`, report, and manifest agree; run reproduces. | No denominator or threshold record. |
| 8 | Local digits only; no real personal records. | Real member data. |

## LAB-11 — Defense Evaluation: Adversarial Training, Squeezing, and an Adaptive Attack

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | All models trained on identical rows and evaluated on the same base set. | Different training data per model. |
| 2 | Baseline: clean 0.9667, robust 0.6204, ASR 0.3582 at ε = 0.10. | No undefended baseline. |
| 3 | Adversarial training: clean 0.8907, robust 0.7296, ASR 0.1809. | Reporting clean accuracy only. |
| 4 | Squeezing: clean 0.9500, robust 0.7722, naive ASR 0.1871, adaptive ASR 0.1832. | Calling the naive result adaptive. |
| 5 | Stress at ε = 0.20: squeezing ASR 0.9571 naive, 0.9981 adaptive; robust accuracy 0.0019. | Omitting the stress test. |
| 6 | BPDA is explained and applied to the squeezing transform. | Re-running naive PGD and labelling it adaptive. |
| 7 | Every claim names budget, attack, base set, and clean cost. | "The defense is robust." |
| 8 | Local digits only; comparison table, metrics, and report complete. | External model or data. |

## LAB-12 — Dataset Validation and Leakage Audit

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | 632 raw rows with counts: 18 missing cells, 10 schema violations, 8 duplicate rows, 4 conflict groups (8 rows), 6 implausible labels, 28 duplicate customer IDs, 12 leaked customers, 1 leaky column. | Eyeballing the data without counts. |
| 2 | Leaky ROC-AUC 0.9584 reproduced with the original protocol. | Quoting the number without a run. |
| 3 | Same-rows ablation 0.7507 isolates the leaky column; repaired AUC 0.8485 on a grouped split. | Comparing leaky and repaired runs that differ in several ways. |
| 4 | 581 repaired rows; imputation fitted on training statistics only. | Imputing with full-data statistics. |
| 5 | `exit_survey` removed as a post-outcome column; every removal is documented. | Deleting the column after measuring, or silently dropping rows. |
| 6 | Governance memo names gate placement, quarantine owner, false-positive policy, and audit trail. | A memo with no owner or gate. |
| 7 | Metrics, repaired dataset, memo, and manifest agree; run reproduces. | No audit trail. |
| 8 | Synthetic churn data only; no real customers. | A real extract. |

## LAB-13 — Supply-Chain Audit of a Toy ML Project

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Five dependencies pinned with resolved versions. | Loose version ranges. |
| 2 | Pickle inspected statically with `pickletools.genops`; the canary is never unpickled. | Loading the canary to "see what it does." |
| 3 | Six findings: 1 critical, 3 high, 2 medium, including the all-zero hash and missing signature. | Copying scanner output without triage. |
| 4 | Hardened loader uses `allow_pickle=False`; manifest regenerated with real SHA-256 values. | Signing before scanning. |
| 5 | HMAC-SHA256 signature verified in constant time; tampered manifest rejected. | A signature that is never checked. |
| 6 | SBOM has 5 components with hashes; gate rejects the vulnerable project (exit 1) and accepts the hardened one (exit 0). | A gate that always exits 0. |
| 7 | Residual-risk statement notes that HMAC protects integrity, not publisher identity. | Claiming the key proves who built it. |
| 8 | Local toy project and benign canary only; no real malware. | Distributing or executing real malware. |

## LAB-14 — Hardening a Local Prediction API

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Service binds to loopback; Bearer authentication uses constant-time comparison. | Binding to 0.0.0.0 or comparing with `==`. |
| 2 | 8 KB body cap, 32-row batch cap, 64 finite values in [0, 1]; correct content type. | Validating only in the client. |
| 3 | Fixed-window limit of 10 requests / 60 s; generic JSON errors. | Leaking stack traces or tokens in errors. |
| 4 | Logs contain request metadata and decisions but no tokens or raw payloads. | Logging full inputs or Authorization headers. |
| 5 | 18/18 security cases pass with the documented status codes: 401, 403, 400, 415, 422, 413, 429, 404, 200. | Returning 200 for every case. |
| 6 | Admin route requires the `admin` scope; `predict` alone gets 403. | One token for every route. |
| 7 | Kill switch, fail-closed behavior, and residual risks documented. | No residual-risk section. |
| 8 | Local digits model only; no external service or real credentials. | Deploying publicly. |

## LAB-15 — Monitoring and Incident Response

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Five detectors calibrated on the quiet period only: input shift, low confidence, shadow disagreement, client concentration, throughput. | Calibrating on attack traffic. |
| 2 | 0/6 baseline false positives with the 5σ thresholds and documented floors. | Setting thresholds after seeing alerts. |
| 3 | Drift fires input shift only; evasion fires three content signals and is the one confirmed incident; the burst is volume-only and medium. | Calling benign drift an incident. |
| 4 | Adjacent alerting windows grouped into episodes with severity and action. | One alert per outlier. |
| 5 | IR playbook names owners, time bounds, evidence handling, and rollback steps. | A playbook with no owner or timing. |
| 6 | Rollback tested: restored = false, previous ASR 0.3299 versus 0.3507. | Claiming rollback fixed the vulnerability. |
| 7 | Squeezing mitigation: ASR 0.3507 → 0.1979, clean accuracy 0.9600 → 0.9433, with adaptive bypass stated. | Reporting mitigation success without cost or bypass. |
| 8 | Recovery verified only after clean windows return to the calibrated band; report and manifest complete. | Declaring recovery from a single quiet window. |

## LAB-16 — Federated Learning Attack and Defense Simulation

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Eight non-IID client shards with per-client class counts documented. | An accidentally IID partition. |
| 2 | FedAvg with local fitting and weighted averaging; clean accuracy recorded by round. | Reporting only the final round. |
| 3 | One malicious client with a stated update scale; clean accuracy and ASR both reported. | ASR with no clean-accuracy cost. |
| 4 | Trimmed mean and norm clipping compared at equal rounds and identical client order. | Different round counts per defense. |
| 5 | Benign, malicious, trimmed, and clipped runs in one comparison table. | Separate tables that cannot be compared. |
| 6 | One ablation on the clipping bound with the effect explained. | A single bound with no sensitivity. |
| 7 | Residual-risk memo covers sybil clients, server trust, and what secure aggregation would and would not hide. | "Aggregation solves poisoning." |
| 8 | Local simulation, synthetic/digits data only; no real federation. | Real client data or network. |

## LAB-17 — Privacy Budget, Noisy Release, and Utility

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Synthetic two-class data with a fixed seed and per-class release groups. | Real tabular records. |
| 2 | Per-example clipping and the L1 sensitivity of the noisy centroid stated explicitly. | Reporting ε with no sensitivity. |
| 3 | Releases at ε ∈ {0.1, 0.5, 1, 2, 8}; parallel composition across disjoint classes accounted. | Treating each release as independent without composition. |
| 4 | Utility and centroid L2 error reported for every budget. | Accuracy alone. |
| 5 | A naive membership-inference AUC reported with the caveat that it is not a formal privacy proof. | Calling a high AUC a DP violation, or a low AUC proof of privacy. |
| 6 | One ablation on clipping norm or sample size, with the sensitivity–utility effect explained. | No ablation. |
| 7 | Audit-ready claim names ε, δ, sensitivity, mechanism, neighboring relation, and composition. | "The release is anonymous." |
| 8 | Local synthetic data; budget table, claim, limitations, and manifest complete. | Real personal data. |

## LAB-18 — Explanation Stability and Subgroup Audit

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Synthetic data with a sensitive subgroup attribute; subgroup counts recorded. | No subgroup accounting. |
| 2 | Baseline and reweighted classifiers compared on overall accuracy and subgroup TPR/FPR. | Overall accuracy only. |
| 3 | Demographic-parity and equalized-odds gaps with bootstrap intervals. | Point gaps with no uncertainty. |
| 4 | Both gradient×input and occlusion attributions implemented for individual predictions. | One method called "the explanation." |
| 5 | Stability under bounded Gaussian noise measured by rank correlation and top-k overlap. | Stability asserted without perturbation. |
| 6 | Prediction-preserving explanation flips counted separately from prediction flips. | Counting every attribution change as instability. |
| 7 | At least one trade-off identified and the limits of stability stated. | "The explanation is stable, therefore fair." |
| 8 | Local synthetic data; tables, limitations, and manifest complete. | Real sensitive attributes. |

## LAB-19 — RAG Trust Boundary and Indirect Injection

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Every document labelled `trusted` or `untrusted`, with retrieval scores recorded. | Treating all retrieved text as trusted. |
| 2 | Deterministic keyword retriever and scripted mock assistant; no external model or API. | Calling a real LLM service. |
| 3 | Attack success defined before defenses, using a harmless canary string. | Defining success after seeing the output. |
| 4 | Layered defenses: trust-aware formatting, instruction hierarchy, output validation, canary tripwire. | A stronger system prompt as the only control. |
| 5 | Residual attack success and benign-document false positives both reported. | No benign evaluation. |
| 6 | One adaptive phrasing of the injection tested and reported. | Re-running the same phrasing. |
| 7 | Findings mapped to OWASP LLM risks, with the limits of prompt filtering stated. | "Injection is solved." |
| 8 | Local synthetic corpus only; retrieval log, defense table, and residual-risk statement complete. | Real documents or services. |

## LAB-20 — Agent Containment and Approval Boundaries

| # | Required check and evidence | What fakes a pass |
|---:|---|---|
| 1 | Four mock tools only: read-only file access, calculator, mock email, mock fetch to an allowlisted host. | A real mailbox, filesystem, or network. |
| 2 | Benign task run with a complete action trace. | No trace of what the agent did. |
| 3 | Four unauthorized tests: read outside workspace, send without approval, fetch a non-allowlisted host, follow instructions in tool output. | Testing only one path. |
| 4 | Capability scoping, approval gate, egress allowlist, and append-only log enforced in code. | Policy enforced only in the prompt. |
| 5 | Re-run reports attempted, blocked, and succeeded actions for every test. | Claiming a block without the log. |
| 6 | Benign false positives measured: the approved task still completes. | Blocking every action and calling it secure. |
| 7 | Residual risks stated: prompt policy is not a boundary, approval fatigue, incomplete logs. | No residual-risk statement. |
| 8 | Local synthetic files, mailbox, and endpoint only; action log and report complete. | Real credentials or egress. |

---

## Scoring completion

A lab is complete only when all eight rows have evidence. The [standard lab rubric](lab-rubric.md) then scores quality. A checklist pass with a rubric dimension below 3 is not completion; fix the dimension before moving on.

| Situation | Action |
|---|---|
| One required row lacks evidence | Lab incomplete; produce the artifact, not a written excuse. |
| A row is satisfied only by a notebook output | Replace it with a run record and manifest. |
| The expected value is outside tolerance | Diagnose the protocol before adjusting the tolerance. |
| A safety row fails | Stop; the lab is not complete regardless of the other rows. |
| All rows pass, rubric dimension below 3 | Improve the artifact in that dimension and re-score. |
