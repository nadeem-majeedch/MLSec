# Level 4 Check — Advanced and Emerging Security (LC-4)

| Field | Value |
|---|---|
| Level | 4 — Advanced and emerging security |
| Modules | M12–M15 |
| Items | 10 |
| Points | 20 |
| Time guide | 35 minutes |
| Pass | 16/20 |
| Outcomes | LO-19, LO-24, LO-26, LO-27, LO-31, LO-32 |
| Answer key | Separate file: `assessments/answer-keys/level-checks/lc-4-key.md` |

Answer without notes. Items 1–6 are worth 1 point, items 7–8 are worth 2 points, and items 9–10 are worth 5 points.

## 1. Secure aggregation (1 point)

What does secure aggregation protect?

A. Model integrity against poisoning  
B. Individual updates from the server  
C. Differential privacy of the final model  
D. Resistance to sybil clients

## 2. Interpreting epsilon (1 point)

Which set is needed to interpret a reported ε?

A. Model accuracy and latency  
B. δ, the neighboring relation, the mechanism, and composition  
C. The number of features  
D. The GPU model

## 3. Explanation stability (1 point)

An explanation changes little under small input noise. What does this support?

A. The explanation is faithful  
B. The explanation is stable under that test, not necessarily faithful  
C. The model is fair  
D. The model is accurate

## 4. Agent authorization (1 point)

Which control is the authorization boundary for an agent's email tool?

A. A system-prompt instruction not to email external addresses  
B. A recipient allowlist and approval enforced in code  
C. A higher sampling temperature  
D. A longer context window

## 5. DP and poisoning (1 point)

True or false: differential privacy prevents a malicious federated client from poisoning the global model.

## 6. Retrieved content (1 point)

True or false: retrieved documents should be treated as data, not as instructions with authority.

## 7. Federated comparison (2 points)

Why must two aggregation defenses be compared at the same number of rounds and the same attacker budget? Name one aggregation assumption that can fail in practice.

## 8. Privacy and fairness reporting (2 points)

Name two facts missing from the claim "ε = 1, so the release is private." Then name one fairness metric and one reason it can conflict with another.

## 9. Scenario: the federated trial (5 points)

You are evaluating coordinate-wise trimming and norm clipping in a local federated simulation with synthetic data.

Design the trial: threat model, controls, metrics, comparison conditions, and two residual risks. Do not use real client data or test a production federation.

## 10. Scenario: the HR assistant (5 points)

An HR assistant retrieves policy documents and can call `read_file` and `create_ticket`. A retrieved document contains an instruction to attach a confidential file to a ticket. You may test only a local replica.

Design four layered controls, one success metric, one benign-document false-positive check, and two residual risks.

## Scoring

| Score | Interpretation |
|---:|---|
| 18–20 | Strong. You can assess distributed, private, explainable, and agentic systems. |
| 16–17 | Pass. Review the missed item and the linked lab. |
| 12–15 | Not yet. Rerun LAB-16 through LAB-20 as needed. |
| Below 12 | Reread M12–M15 before Level 5. |
