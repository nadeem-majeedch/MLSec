# Project and RT-01 Scoring Rubric

| Field | Value |
|---|---|
| Applies to | PRJ-01…PRJ-06 and RT-01 |
| Dimensions | 8 |
| Total | 100 |
| Project completion | Every dimension at Developing (2) or above, and at least six at Proficient (3) |
| RT-01 completion | Every dimension at 2 or above, and at least six at 3, including rules of engagement, evidence, detection, and mitigation |
| Companion | [Project catalog](../../project-catalog.md) · [Capstone rubric](capstone-rubric.md) · [Evaluator guide](../../projects/evaluator-guide.md) |

This rubric scores applied work that reuses the labs. It is deliberately close to the capstone rubric so that a learner can see the same standards at a smaller scale. The capstone adds stakeholder analysis, multiple seeds, an adaptive variant, and a clean-checkout demonstration.

## 1. Dimensions and weights

| Dimension | Weight | Project evidence | RT-01 evidence |
|---|---:|---|---|
| Scope, system, data | 10 | Scope, diagram, data inventory, authorization | Scope, targets, non-goals, data rules |
| Threat model or rules of engagement | 15 | Two adversary profiles, risk register, traceability | Written RoE, authorization, budgets, stop conditions |
| Baseline and experimental design | 15 | Frozen evaluation set, control, budgets, seeds | Quiet baseline, test windows, request budget |
| Attack or red-team execution | 20 | At least 3 attacks with denominators and oracles | Testable attack plan, execution within budget, attributable evidence |
| Defense, mitigation, and evaluation | 15 | At least 1 control, replay, cost, residual risk | Detection calibration, mitigation, adaptive retest, residual risk |
| Reproducibility and evidence | 10 | Run records, manifest, one-command reproduction | Request logs, timestamps, hashes, evidence manifest |
| Communication and recommendations | 10 | Report and briefing, findings ordered and costed | Red and blue reports, joint synthesis, residual risk |
| Ethics, safety, and limitations | 5 | Local/synthetic, authorized use, limitations | RoE compliance, no third party, disclosure, limitations |

## 2. Descriptors

Score each dimension 1–4. The weighted score is $\text{weight} \times \text{level} / 4$.

| Dimension | 4 — Exemplary | 3 — Proficient | 2 — Developing | 1 — Insufficient |
|---|---|---|---|---|
| Scope, system, data | Enumerable scope; decision and harm explicit; data classified and licensed; non-goals complete | Clear scope with minor gaps | Vague scope or missing classification | No usable scope or unsafe target |
| Threat model / RoE | Testable adversaries; every test traced; RoE names targets, limits, data rules, and stop conditions; rejections reasoned | Clear model or RoE with minor gaps | Generic threats or an incomplete RoE | No model or no authorization |
| Baseline and design | Frozen, hashed baseline; zero-effect control; matched budgets and seeds; confounders addressed | Sound baseline with limited uncertainty | Single run or confounded comparison | No baseline or invalid comparison |
| Attack / red-team execution | At least 3 attacks; correct budgets and denominators; adaptive variant; attributable evidence; honest negatives | Attacks run correctly with minor omissions | Partial results or metric errors | Attacks do not run or evidence is not attributable |
| Defense, mitigation, evaluation | Implemented control; replay; adaptive variant; false-positive and clean cost; residual risk | Control evaluated with limited adaptivity | Static test only | No defense or no evaluation |
| Reproducibility and evidence | Clean checkout or replayable run; manifest matches; one command; evidence chain intact | Reproduces with small fixes | Missing steps or incomplete evidence | Not reproducible or evidence incomplete |
| Communication | Decision-oriented report and briefing; findings ordered and costed; residual risk clear | Clear with minor issues | Disorganized or overlong | Unsupported or unsafe recommendations |
| Ethics and limitations | Authorized-use statement; local/synthetic; construct, internal, external, and statistical limits; no overclaim | Clear constraints with minor gaps | Weak limitations or safety statement | Unsafe, unlawful, or overclaiming |

## 3. Project-specific evidence

| Project | Minimum evidence for Proficient |
|---|---|
| PRJ-01 Fraud scoring | Segment-level evasion results, duplicate audit, global-versus-segment comparison, data-quality gate, costed control |
| PRJ-02 Visual defect pipeline | Poison-rate curve, trigger evaluation with false-trigger rate, screening calibration, retraining check, adaptive trigger |
| PRJ-03 Prediction API privacy | Query-budget extraction curve, low-FPR membership result, DP release with accounting, output minimization, log review |
| PRJ-04 Secure pipeline | Validation gate, signed manifest, SBOM with hashes, failure-injection matrix, fail-closed CI, rollback |
| PRJ-05 RAG assistant | Trusted/untrusted corpus, injection and benign sets, code-enforced tool boundary, approval test, residual risk |
| PRJ-06 Robustness comparison | Three-defense matrix, frozen baseline, matched budgets, clean-cost table, adaptive test, pre-declared ranking |
| RT-01 Red/blue | Signed RoE, attack plan with budgets, attributable request logs, quiet baseline, detection precision, mitigation retest, joint report |

## 4. RT-01 scoring detail

RT-01 uses the same eight dimensions, with these emphases:

- **Rules of engagement (15).** The document names the target, the time window, the request budget, data handling, communication, and stop conditions. "Everything else is out of scope" is not enumerable.
- **Attack execution (20).** Every attack traces to an objective and a budget. The report states what was attempted, what succeeded, and what was blocked. Evidence includes timestamps and request IDs.
- **Detection and mitigation (15).** Detections are calibrated on a quiet baseline. The report gives false positives as a count and a rate, not a percentage alone. Mitigations are retested with a variant that is not the original script with a new seed.
- **Evidence (10).** Logs, hashes, and an evidence manifest preserve attribution before mitigation changes the state.
- **Reporting (10).** Red and blue reports are separate, then synthesized. The residual-risk statement names the condition, the evidence, and what remains.

## 5. Completion and interpretation

| Result | Meaning | Action |
|---|---|---|
| All dimensions ≥ 3 | Complete at Proficient | Suitable as capstone preparation; archive the artifact |
| Six dimensions ≥ 3, all ≥ 2 | Project complete | Repair the two developing dimensions before citing the project as capstone evidence |
| Any dimension = 1 | Not complete | Stop and fix the artifact; a high total does not compensate |
| Automatic fail | Not complete regardless of score | Review the safety condition with the course owner |

Automatic fails are the same as the capstone: a third-party production target, real personal data, a real credential, a fabricated result, or a claim that contradicts the artifact.

## 6. Common ways a project fakes a pass

- A scope that names a topic instead of a system and a decision.
- A threat model that lists techniques without an adversary or budget.
- A baseline that changes between the attack and defense runs.
- An attack success rate without a denominator or base set.
- A defense tested only against the original static attack.
- A detection rate without a false-positive count.
- A repository with a manifest that lists filenames but not hashes.
- A report that says "the system is secure" or "no risks remain."

## 7. Self-scoring method

1. Check the project's artifact contract first. A missing required file is a scope problem, not a writing problem.
2. Score each dimension from the artifact, not from the intended design.
3. Write the evidence reference for every score.
4. Fix any dimension at 2 before polishing the report.
5. Re-score after the fix; do not average across attempts.

The project and RT-01 rubrics are self-assessment tools. They are not externally validated, not proctored, and not a substitute for the evaluator guide.
