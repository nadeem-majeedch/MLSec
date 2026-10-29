# Integrated Final Assessment (FIN-01)

| Field | Value |
|---|---|
| Assessment | FIN-01 — Integrated final assessment |
| Covers | M00–M18, all five levels |
| Items | 25 |
| Points | 100 |
| Time guide | 3 hours |
| Pass | 80/100 |
| Outcomes sampled | LO-02, LO-03, LO-05, LO-08, LO-10, LO-13, LO-14, LO-16, LO-17, LO-18, LO-19, LO-21, LO-22, LO-23, LO-24, LO-26, LO-27, LO-28, LO-32, LO-33, LO-34 |
| Answer key | Separate file: `assessments/answer-keys/final-assessment-key.md` |
| Safety rule | Any request to test a third party, use real personal data, or produce a harmful artifact is an automatic fail |

Answer without notes, the module pages, or an AI assistant. Write reasoning where an item asks for it: a correct letter with a wrong reason is a miss. The time guide is a pacing aid, not a proctoring rule. Record the item numbers you miss in the [progress record](../progress-and-reflection.md).

## Structure

The assessment has five parts, one per level. Each part has the same shape and is worth 20 points: two multiple-choice items at 2 points, one true/false item at 2 points, one short-answer item at 4 points, and one scenario at 10 points.

| Part | Level | Modules | Items | Points |
|---|---|---|---:|---:|
| A | Foundations | M00–M03 | 1–5 | 20 |
| B | Core attacks | M04–M07 | 6–10 | 20 |
| C | Defenses and secure engineering | M08–M11 | 11–15 | 20 |
| D | Advanced and emerging security | M12–M15 | 16–20 | 20 |
| E | Applied assessment and research | M16–M18 | 21–25 | 20 |

Parts A–D each sample one level; Part E integrates the applied outcomes. Every part contains at least one item that requires a calculation, a comparison, or a design decision, so no part can be passed by recall alone.

---

## Part A — Foundations (M00–M03, 20 points)

### 1. Reproducibility check (2 points)

Which action is the strongest test of a reproducibility claim?

A. Rebuild from a clean checkout with pinned dependencies, regenerate the artifacts from the raw inputs, and compare hashes and headline numbers  
B. Open the notebook and confirm that the cells contain saved output  
C. Check that the repository has a README and a license  
D. Ask the author to confirm the reported number

### 2. Precision and recall (2 points)

A test set has 1,000 rows and 50 positives. At the chosen threshold the model flags 100 rows, of which 30 are true positives. What are precision and recall?

A. Precision 0.30, recall 0.60  
B. Precision 0.60, recall 0.30  
C. Precision 0.03, recall 0.05  
D. Precision 0.50, recall 0.30

### 3. Threshold summary (2 points)

True or false: a confusion matrix at one threshold fully describes a model's ranking quality.

### 4. Questions behind AUC (4 points)

A team says its model is ready because ROC-AUC is 0.93 and the dataset is hashed. Name two questions the claim leaves unanswered and the evidence that would answer each.

### 5. Scenario: the reproducibility audit (10 points)

A project package contains a notebook with saved outputs, a `requirements.txt` that lists `numpy`, `pandas`, and `scikit-learn` without versions, a script that downloads data from a URL, a reported ROC-AUC of 0.91, and no seed.

Design a six-step audit of the package. Name three reasons the 0.91 is not yet reproducible and one artifact that would change your verdict. Use only the package and a local environment; do not contact or probe the data host.

---

## Part B — Core attacks (M04–M07, 20 points)

### 6. Non-monotonic attack result (2 points)

A learner reports that attack success **falls** as $\varepsilon$ increases from 0.02 to 0.04 on the same model and test set. Which explanation is most likely?

A. The attack implementation or accounting is wrong, for example the perturbation is clipped away or $\varepsilon$ is applied more than once  
B. The model becomes more robust as the budget grows  
C. Attack success is expected to fall as the budget grows  
D. The test set is too small to show any effect

### 7. Targeted effect (2 points)

A poisoning run leaves overall accuracy unchanged, but rows from one source class are now routed to a chosen target class on clean inputs. Which label fits?

A. An availability attack  
B. A targeted integrity attack  
C. Model extraction  
D. Membership inference

### 8. Membership proof (2 points)

True or false: a membership inference attack with TPR 0.60 at FPR 1% proves that the model memorized the tested record.

### 9. Extraction result (4 points)

An extraction run against a local teacher reports teacher accuracy 0.90, student accuracy 0.88, and fidelity 0.92 at 10,000 queries. State what the result supports, what it does not support, and one additional measurement that would make the claim stronger.

### 10. Scenario: poisoning and backdoor evaluation (10 points)

A local spam classifier trains on 2,000 synthetic clean rows. You will test poison rates of 1%, 3%, and 5%, with a trigger consisting of the phrase "invoice attached" plus a link.

Design the evaluation: control condition, metrics with denominators, baselines, a decision rule for calling an effect real, and two limits. Do not use real messages or a production mail system.

---

## Part C — Defenses and secure engineering (M08–M11, 20 points)

### 11. Adaptive attack (2 points)

Which is an adaptive attack against an input-preprocessing defense?

A. FGSM on the undefended model  
B. BPDA that approximates the preprocessing gradient  
C. A transfer attack with no knowledge of the defense  
D. Evaluating clean accuracy only

### 12. Signed but unpinned (2 points)

A model artifact passes signature verification, but its build installs an unpinned `numpy` wheel at deploy time. Which risk remains?

A. The artifact's hash no longer matches its manifest  
B. A dependency can be substituted or compromised without changing the signed model  
C. The signature key is exposed  
D. The model cannot be loaded

### 13. Rate limits (2 points)

True or false: rate-limiting a prediction API prevents model extraction.

### 14. Known-string filter (4 points)

A serving team reports that its filter "blocked 100% of known attack strings." Explain why this is weak evidence, and name two tests that would measure the control.

### 15. Scenario: preprocessing defense (10 points)

A defense applies JPEG compression and random resizing before classification. On a local synthetic image set it reports ASR 0.03 under FGSM, against 0.45 for the undefended model.

Design a static and an adaptive evaluation. Include the metrics and denominators, the baselines and controls, a decision rule for whether the defense is worth deploying, and two limits. State what the current 0.03 does and does not support.

---

## Part D — Advanced and emerging security (M12–M15, 20 points)

### 16. Composition (2 points)

Two independent releases from the same dataset each use ε = 0.5 under basic composition with the same neighboring relation. What is the composed ε?

A. 0.25  
B. 0.5  
C. 1.0  
D. 2.0

### 17. Agent tool boundary (2 points)

An agent requests `send_email` to a domain that is not on the code-enforced allowlist. What should the runtime do?

A. Send the email and log a warning  
B. Refuse the call with a policy error, log it, and require an approved recipient change  
C. Ask the model to reconsider in a follow-up prompt  
D. Raise the sampling temperature so the model chooses differently

### 18. Proxy features (2 points)

True or false: removing the sensitive attribute from a model's input features eliminates disparate impact.

### 19. Aggregation and privacy (4 points)

State what secure aggregation protects and what differential privacy protects. Then name one thing neither protects in a federated training run.

### 20. Scenario: retrieval and egress (10 points)

A local assistant retrieves policy documents and can call `send_email`. A canary document contains an instruction to email a confidential attachment to an external address.

Design the test and the controls: one injection test, one benign false-positive check, three layered controls with at least one enforced in code, one success metric, and two residual risks. Test only a local replica with synthetic documents.

---

## Part E — Applied assessment and research (M16–M18, 20 points)

### 21. Baseline gate (2 points)

A learner overwrites the undefended baseline after seeing the defense results. Which milestone gate failed?

A. The data-classification gate  
B. The baseline-freeze and versioning gate  
C. The disclosure gate  
D. The report-format gate

### 22. Costed remediation (2 points)

Which remediation entry can an owner schedule and verify?

A. "Improve robustness before launch."  
B. "Retrain the model and review results."  
C. "Add norm-clipped adversarial training to the nightly job; owner: ML platform; 3 days; verify with PGD at ε = 2/255 on the frozen evaluation set, target ASR below 0.20 with no more than 0.03 clean-accuracy loss."  
D. "Ask the vendor to fix the model."

### 23. Negative result (2 points)

True or false: a negative result is not worth reporting unless the attack succeeded.

### 24. Evidence for a red-team finding (4 points)

Name two artifacts that make a red-team finding attributable to a specific action, and two measurements that make a detection claim auditable.

### 25. Scenario: the integrated mini-assessment (10 points)

You have one working day to assess a local replica of a return-risk model that consumes a vendor feature feed. The replica uses synthetic data and a documented API.

Write the assessment plan: the decision the model supports, the scope and two non-goals, three falsifiable tests that cover data, model, and serving, one control with a negative test, the report's required sections, and one residual-risk statement. Do not test the vendor's production feed.

---

## Scoring

| Part | Items | Points |
|---|---|---:|
| A Foundations | 1–5 | 20 |
| B Core attacks | 6–10 | 20 |
| C Defenses | 11–15 | 20 |
| D Advanced | 16–20 | 20 |
| E Applied | 21–25 | 20 |
| **Total** | **25** | **100** |

| Score | Interpretation | Next action |
|---:|---|---|
| 90–100 | Distinction. You integrate mechanisms, evidence, and limits across levels. | Proceed to the capstone; use the missed items as review targets. |
| 80–89 | Pass, specialist-ready. | Proceed; repair any part below 14/20 before the capstone defense. |
| 70–79 | Practitioner, not yet passing. | Rework the weakest two parts and retake after review. |
| 60–69 | Foundations present. | Revisit the level checks and labs for the weak parts. |
| Below 60 | Not yet. | Return to the level checks and rebuild the underlying labs. |

A safety violation is an automatic fail regardless of the score. A pass on this assessment is not a certificate and does not replace the project, RT-01, or capstone evidence.

## Revision map

| If you missed | Revisit | Then |
|---|---|---|
| Part A | M00–M03; LAB-01, LAB-01B, LAB-02 | LC-1 and the module quizzes |
| Part B | M04–M07; LAB-03…LAB-10 | LC-2; rerun the matching attack lab |
| Part C | M08–M11; LAB-11…LAB-15 | LC-3; rebuild the defense or serving artifact |
| Part D | M12–M15; LAB-16…LAB-20 | LC-4; rerun the matching privacy or agent lab |
| Part E | M16–M18; project or RT-01 guidance | LC-5; rewrite the scope and report sections |

For each miss, write the item number, the concept, the required element you omitted, and the section you will reread. A retake without that list is recognition practice.
