# Question Bank (QB-01)

| Field | Value |
|---|---|
| Assessment | QB-01 — Tagged question bank |
| Coverage | M00–M18 |
| Items | 56 (24 multiple-choice, 12 true/false, 12 short answer, 8 scenario) |
| Points | 92 |
| Time | Self-paced; suggested 3–5 sittings of 45–60 minutes |
| Pass | No fixed pass mark; use the section scores for diagnosis |
| Answer key | Separate file: `assessments/answer-keys/question-bank-key.md` |

This bank is for practice, spaced review, and targeted diagnosis. It is not a fifth quiz for each module and it is not a substitute for the labs. Items integrate material across modules; a single item may ask you to combine a metric, a threat model, and a control.

## How to use the bank

1. **Do not attempt all 56 items in one sitting.** Choose a section, set a 45–60 minute limit, and answer without notes.
2. Write answers in `work/assessments/qb-01.md`, numbering each item (A1, A2, …). For scenarios, use the headings named in the item.
3. Score with the key. For written items, compare against the **required elements**, not the exact wording.
4. Record the section score and the item IDs missed. Use the revision map at the end to choose what to reread.
5. Revisit missed items after 1, 3, 7, and 21 days. A second attempt should produce the reasoning, not just the letter.

## Scoring

| Item type | Count | Points each | Total |
|---|---:|---:|---:|
| Multiple-choice | 24 | 1 | 24 |
| True/false | 12 | 1 | 12 |
| Short answer | 12 | 2 | 24 |
| Scenario | 8 | 4 | 32 |
| **Total** | **56** | | **92** |

For a short answer, 2 points means two required elements or one element with a correct explanation. For a scenario, 4 points means a bounded answer with a threat model, a measurement, a baseline or control, and a limitation. A correct conclusion with no reasoning earns half credit on written items.

## Section A — Foundations (M00–M03)

**14 items · 23 points.** Answer all items.

### Multiple-choice (1 point each)

**A1.** Which activity is permitted under the course's authorized-use policy?

A. Sending crafted inputs to a public demo API  
B. Running an attack against an isolated local replica built from synthetic data  
C. Scanning the university network for exposed model endpoints  
D. Testing a leaked model on a former employer's data

**A2.** A team scales features before splitting the data. What is the main evaluation risk?

A. The scaler learns test-set statistics, inflating test performance  
B. The model trains too slowly  
C. The labels become unbalanced  
D. The test set becomes larger

**A3.** A fraud dataset is 1% positive. A model reports 99% accuracy. Which metric best shows whether the model finds fraud?

A. Accuracy  
B. Recall for the positive class  
C. Training loss  
D. Number of features

**A4.** Which item is a **goal** rather than an adversary capability?

A. Send 5,000 queries to the API  
B. Use a compromised account  
C. Cause a targeted misclassification  
D. Spend ten hours on the attack

**A5.** A threat has impact 3 and likelihood 5. Using the course bands (1–4 low, 5–9 medium, 10–16 high, 17–25 critical), what is its severity?

A. Low  
B. Medium  
C. High  
D. Critical

**A6.** Which NIST AI RMF function covers selecting and prioritizing risk treatments?

A. GOVERN  
B. MAP  
C. MEASURE  
D. MANAGE

### True/false (1 point each)

**A7.** An isolated local replica with synthetic data is an acceptable target for the course's offensive labs.

**A8.** A random row-wise split is appropriate for data collected over time when the goal is deployment performance.

**A9.** A threat register should delete rejected threats so the remaining list is shorter.

### Short answer (2 points each)

**A10.** Name two checks that can reveal target leakage before training.

**A11.** Explain why 99% accuracy can be uninformative at 1% prevalence, and name one metric pair that is more informative.

**A12.** Give one preventive and one detective control for model-extraction risk through a public prediction API, and state one cost of each.

### Scenario (4 points each)

**A13.** A notebook reports ROC-AUC 0.99 for a readmission model. Review finds three problems:

1. the scaler was fit on all rows before the split;
2. the same patient appears in training and test;
3. the decision threshold was chosen on the test set.

Identify the three protocol errors, state the likely direction of each effect on the reported score, and give a corrected protocol in four steps. Use only local synthetic data.

**A14.** A hospital deploys a local triage model. Build a four-row threat register. For each row give the threat, impact (1–5), likelihood (1–5), score and band, one control, and an owner. Include one rejected threat with a reason. Do not use real patient data.

## Section B — Core attacks (M04–M07)

**14 items · 23 points.** Answer all items.

### Multiple-choice (1 point each)

**B1.** Two evasion papers report 90% and 60% attack success. Which missing detail most directly prevents a comparison?

A. The model architecture  
B. The norm, budget, and base set  
C. The authors' affiliations  
D. The GPU used for training

**B2.** A poisoning experiment flips 2% of labels; test accuracy stays at 0.90. What is the best conclusion?

A. The attack failed  
B. The model is robust to poisoning  
C. Accuracy alone cannot rule out a targeted effect  
D. Poisoning is impossible at this rate

**B3.** A backdoored model has 0.98 clean accuracy, 0.95 ASR on triggered source rows, and the clean model sends 0.10 of those rows to the target. What is the attack effect in percentage points?

A. 95  
B. 10  
C. 85  
D. 5

**B4.** Which prediction-API response generally gives the strongest membership-inference signal per query?

A. The class name only  
B. The top-1 confidence only  
C. The full probability vector  
D. The API version string

**B5.** An attacker computes gradients on a local source model and applies the resulting perturbation to a target model without querying the target. What is this?

A. A white-box attack on the target  
B. A transfer attack  
C. A poisoning attack  
D. A model inversion attack

**B6.** A surrogate has fidelity 0.92 to its teacher and task accuracy 0.70. What does this show?

A. The attacker obtained the training data  
B. The teacher's task accuracy is 0.70  
C. The surrogate copies the teacher's behavior, which may be wrong  
D. Fidelity cannot exceed task accuracy

### True/false (1 point each)

**B7.** A poison rate must name the clean training-set denominator.

**B8.** A backdoor claim can rest on ASR alone.

**B9.** At low prevalence, TPR at a fixed low FPR is more useful than ROC-AUC for privacy harm.

### Short answer (2 points each)

**B10.** Give two reasons a digital L∞ evasion result may not transfer to a physical camera system.

**B11.** State the trust assumption behind reference-set poisoning screening and one way it fails.

**B12.** Distinguish a representative inversion output from a recovered training record, and explain why the distinction matters for harm.

### Scenario (4 points each)

**B13.** A local image classifier is claimed to be "99% robust at ε = 0.01." Design a three-budget evaluation at ε = 0.005, 0.01, and 0.02. Name the attack settings, base set, metrics, baseline, and one adaptive check. State what a negative result would and would not show.

**B14.** A vendor supplies a compiled model with no training data. You may run it locally on synthetic data. Design a two-part test for (a) a backdoor and (b) membership inference, naming one baseline and one limit for each. Do not query vendor systems.

## Section C — Defenses and secure engineering (M08–M11)

**14 items · 23 points.** Answer all items.

### Multiple-choice (1 point each)

**C1.** Which result best supports an adaptive robustness claim?

A. ASR 0 under FGSM at one budget  
B. ASR 0.12 under PGD with BPDA at a stated budget, with clean accuracy and the base set reported  
C. Clean accuracy 0.99  
D. No attack was run

**C2.** What is the usual clean-accuracy cost of adversarial training?

A. Lower clean accuracy in exchange for higher robust accuracy  
B. Higher clean accuracy with no robustness change  
C. No change in either metric  
D. Removal of the need for attack evaluation

**C3.** Which split prevents entity leakage when customers have multiple rows?

A. A random row-wise split  
B. `GroupShuffleSplit` grouped by customer  
C. Stratification by the label  
D. A larger test set

**C4.** Which control establishes artifact **integrity**, as distinct from authenticity?

A. An SBOM  
B. A signature  
C. A SHA-256 manifest  
D. A model card

**C5.** A valid token has exceeded its quota. Which status code is most appropriate?

A. 400  
B. 401  
C. 403  
D. 429

**C6.** Which artifact makes a rollback decision testable?

A. Clean accuracy alone  
B. Attack success on a captured batch for the current and previous checkpoints  
C. The number of alerts  
D. The model size

### True/false (1 point each)

**C7.** A defense that blocks one PGD run is proven robust.

**C8.** A dataset version may be deleted after training because the deployed model no longer needs it.

**C9.** A signature over a manifest protects files that the manifest does not list.

### Short answer (2 points each)

**C10.** Name two signs of gradient masking and one adaptive test that can reveal it.

**C11.** Name three fields a transformation record needs beyond the output hash to reproduce the transformation.

**C12.** Explain why rollback alone may not contain a model compromise.

### Scenario (4 points each)

**C13.** A defense report says ASR fell from 0.40 to 0.02 under FGSM; clean accuracy fell from 0.94 to 0.86; the decision threshold was also changed; no adaptive attack was run. Identify three confounds or gaps, and design the minimum retest that would make the claim interpretable.

**C14.** A model registry accepts unsigned uploads and the serving API has no authentication. Design four controls across supply chain and serving, each with a negative test, and name one residual risk.

## Section D — Advanced and emerging security (M12–M15)

**9 items · 14 points.** Answer all items.

### Multiple-choice (1 point each)

**D1.** What does secure aggregation protect?

A. Model integrity against poisoning  
B. Individual updates from the server  
C. Differential privacy of the final model  
D. Sybil resistance

**D2.** Which set is needed to interpret a reported ε?

A. Model accuracy and latency  
B. δ, the neighboring relation, the mechanism, and composition  
C. The number of features  
D. The GPU model

**D3.** An explanation changes little under small input noise. What does this support?

A. The explanation is faithful  
B. The explanation is stable under that test, not necessarily faithful  
C. The model is fair  
D. The model is accurate

**D4.** Which control enforces least privilege for an agent's email tool?

A. A system-prompt instruction  
B. A recipient allowlist and approval enforced in code  
C. A higher sampling temperature  
D. A longer context window

### True/false (1 point each)

**D5.** Differential privacy prevents a malicious federated client from poisoning the global model.

**D6.** Retrieved documents should be treated as data, not as instructions with authority.

### Short answer (2 points each)

**D7.** A release reports ε = 1 but no δ, clipping, neighboring relation, or composition. Give two reasons the claim is unauditable.

**D8.** Explain how equal selection rates can coexist with unequal TPR and FPR when group base rates differ.

### Scenario (4 points)

**D9.** An HR assistant retrieves policy documents and can call `read_file` and `create_ticket`. A retrieved document contains an instruction to attach a confidential file to a ticket. Design four layered controls, one success metric, one benign-document false-positive check, and two residual risks. Test only a local replica.

## Section E — Applied assessment and research (M16–M18)

**5 items · 9 points.** Answer all items.

### Multiple-choice (1 point each)

**E1.** Which finding is usable by a system owner?

A. "The model is vulnerable."  
B. "At ε = 0.05, 40-step PGD on a frozen 500-row base changed 68 of 450 clean-correct predictions (ASR 0.151) against a 0.020 baseline; the affected segment is X; reproduction path R."  
C. "Fix the model."  
D. "Risk is high."

**E2.** Which is a valid ablation for a defense claim?

A. Change the dataset and the model at the same time  
B. Run the same attack with the defense on and off, holding seeds and budget fixed  
C. Remove the baseline  
D. Add more prose to the report

### True/false (1 point)

**E3.** A red-team action outside the rules of engagement is acceptable if it finds a real issue.

### Short answer (2 points)

**E4.** Name three elements of a costed remediation recommendation.

### Scenario (4 points)

**E5.** A local credit model's differentially private release reduces overall accuracy, and you suspect the subgroup accuracy gap widens. Turn this into a research question: state the gap, one claim–evidence pair, one ablation, and the scope and ethics limits.

## Revision map

| If you missed | Reread | Then do |
|---|---|---|
| A1–A9, A13 | M00–M03, especially the diagnostic, leakage, and threat-register lessons | Rerun LAB-01B and LAB-02 |
| A10–A12, A14 | M01.L3, M02.L4, M03.L3–L5 | Rebuild the threat register and the baseline table |
| B1–B7, B10, B13 | M04.L5, M05.L1 and L4, M06.L1 | Rerun LAB-04, LAB-06, or LAB-08 |
| B8–B9, B11–B12, B14 | M06.L3–L4, M07.L3–L5 | Rerun LAB-08 and LAB-10 |
| C1–C2, C7, C10, C13 | M08.L1, L4–L6 | Rerun LAB-11 with an adaptive attack |
| C3, C8, C11 | M09.L2–L5 | Rerun LAB-12 from a clean state |
| C4, C9, C14 | M10.L2–L4, M11.L1 | Rerun LAB-13 and LAB-14 |
| C5–C6, C12 | M11.L2–L5 | Rerun LAB-14 and LAB-15 |
| D1–D2, D5, D7 | M12.L3–L4, M13.L2–L3 | Rerun LAB-16 or LAB-17 |
| D3, D8 | M14.L3–L5 | Rerun LAB-18 |
| D4, D6, D9 | M15.L3–L6 | Rerun LAB-19 or LAB-20 |
| E1–E5 | M16–M18 | Rebuild the scope, test matrix, and claim–evidence table |

## What this bank is not

It is not a validated psychometric instrument, a proctored exam, or a substitute for lab and project evidence. A high score means you can reason about the material on paper. It does not mean you can run the experiment, reproduce the result, or defend it under an adaptive attack. The answer key is a separate file; this repository is public, so the key is not secret.
