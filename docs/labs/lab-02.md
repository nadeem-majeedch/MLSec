# LAB-02 — Threat Model an ML System

**Tier A · 4 hours · Difficulty 3 · Module M03 · Outcomes LO-03, LO-28**

## Why this lab exists

An attack technique is only relevant if an adversary can reach the system, has the knowledge to act, and causes harm someone cares about. A threat model is the argument that connects those facts. Without it, a red-team report is a list of tricks; with it, the report tells an owner what to fix first and how they will know it failed.

In this lab you produce a complete threat model for a fictional clinical ML system. You do not attack anything. The deliverable is a structured model that a second person can read, challenge, and check.

## The system and the threat model

Northbridge University Hospital Network (fictional) deploys a radiology triage assistant:

- Chest X-ray studies arrive from six hospital sites through an ingestion API.
- A preprocessing service normalizes images and strips most DICOM metadata.
- A vendor-supplied vision model scores each study as routine, urgent, or critical.
- The score places the study on a radiologist worklist. The radiologist makes the final read and can override the priority.
- Overrides are stored and used in a monthly retraining job.
- Model updates arrive from the vendor through a private registry.
- An analytics team exports de-identified data to research partners.
- Support administrators and the vendor have privileged access to production consoles.

The system is **decision support**, not autonomous diagnosis. The queue order still affects which study is seen first, so a wrong score can delay care.

## What you produce

1. A data-flow diagram with at least five labelled trust boundaries (`TB1`, `TB2`, …).
2. An asset inventory of at least six assets, each with a CIA rating and sensitivity.
3. At least eight attack surfaces, each attached to a boundary and an entry point.
4. At least nine accepted threats and at least one rejected threat with a reopening condition.
5. Threat coverage of all five lifecycle stages (data collection, training, artifact, serving, monitoring) and all four NIST goals (integrity, availability, privacy, abuse).
6. At least six distinct attack classes.
7. Three attack trees, each with at least three steps.
8. Preventive, detective, and corrective controls and a residual-risk rating per threat.
9. A detection hypothesis per accepted threat: a metric, a baseline, and a threshold.
10. A crosswalk to the NIST AI RMF and the OWASP ML Top 10, plus a reasoned decision about the OWASP LLM Top 10.

The model is written in `threat-model.yaml`; the narrative is `report.md`.

## Prerequisites

- Module 03 Lessons 1–4.
- You can explain the difference between an asset, a trust boundary, an attack surface, and a threat.
- You can read a Mermaid `flowchart`.
- You have completed LAB-01B or can state the difference between a model error and an attack.

## Environment

- Python 3.14.7 with `PyYAML==6.0.3`; no other package is needed.
- CPU only, no network, no cloud account, no API key.
- The checker is local and reads only the two files you give it.

## Data and safety

There is no dataset. The scenario is fictional and contains no real patient data, vendor, or endpoint. Do not replace it with a real hospital's architecture or real patient records. If you adapt the scenario to a real system, use only public documentation and do not include credentials, hostnames, or personal data.

## Task specification

Work in `labs/lab-02-threat-model/`.

1. **Read the brief and draw the system.** Start from `report.md` and replace the starter Mermaid diagram. Mark every place where data or authority crosses an organizational or privilege boundary.
2. **Build the asset inventory.** Include data, model, labels, availability, audit records, credentials, and the vendor channel. For each, state confidentiality, integrity, and availability needs and a sensitivity level.
3. **Enumerate surfaces.** For each surface, name the boundary it sits on, the entry point, and who can reach it.
4. **Write the adversary model.** For each actor, state goal, knowledge, capability, and an assumed limit. State what the adversary is *not* assumed to have.
5. **Write the threat register.** At least nine accepted threats. Use the schema below. Classify each with a NIST goal, an attack class, and a lifecycle stage. Map to a MITRE ATLAS ID only when a verified ID fits; otherwise use an empty list.
6. **Score and rank.** `severity = impact × likelihood` with the bands below. Explain ties. Rank the top five.
7. **Add controls and detection.** For every accepted threat: at least one preventive, one detective, and one corrective control; a residual-risk rating; and a detection hypothesis with a metric, baseline, and threshold.
8. **Write three attack trees.** Each root is an adversary goal; each step names a threat.
9. **Crosswalk.** Cover GOVERN, MAP, MEASURE, and MANAGE. Map at least four OWASP ML entries. Decide whether the OWASP LLM list applies and say why.
10. **Reject at least one threat.** Give a reasoned rejection and the condition that would reopen it.
11. **Run the checker** and fix structural failures.

## Schema

| Section | Required fields |
|---|---|
| `system` | `name`, `owner`, `description`, `deployment`, `out_of_scope` |
| `assets[]` | `id`, `name`, `description`, `cia` (list), `sensitivity` |
| `trust_boundaries[]` | `id`, `name`, `between` (list), `controls` (list) |
| `attack_surfaces[]` | `id`, `name`, `boundary`, `entry_point`, `attacker_access` |
| `threats[]` | `id`, `title`, `status`, `attack_class`, `nist_goal`, `lifecycle_stage`, `atlas`, `assets`, `surfaces`, `actor`, `knowledge`, `capability`, `assumptions`, `impact`, `likelihood`, `severity`, `impact_statement`, `mitigations` (preventive/detective/corrective), `detection_hypothesis`, `residual_risk` |
| `attack_trees[]` | `id`, `name`, `root`, `steps[]` with `action` and `threat` |
| `crosswalk` | `ai_rmf`, `owasp_ml`, `owasp_llm` |

**Severity bands.** 1–4 low, 5–9 medium, 10–16 high, 17–25 critical. The checker requires the stated severity to equal the band for `impact × likelihood`.

**Control rule.** High and critical threats require at least two preventive controls and at least one detective control, and cannot carry high residual risk.

**ATLAS allowlist.** Only these verified technique IDs are accepted: `AML.T0015` Evade AI Model, `AML.T0018` Manipulate AI Model, `AML.T0020` Training Data Poisoning, `AML.T0024` Exfiltration via AI Inference API, `AML.T0040` AI Model Inference API Access, `AML.T0043` Craft Adversarial Data, `AML.T0051` LLM Prompt Injection. An empty list is valid; an invented ID is not.

**OWASP ML IDs.** `ML01` input manipulation, `ML02` data poisoning, `ML03` model inversion, `ML04` membership inference, `ML05` model theft, `ML06` supply chain, `ML07` transfer learning, `ML08` model skewing, `ML09` output integrity, `ML10` model poisoning.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `threat-model.yaml` | schema TODOs | assets, boundaries, attack surfaces | Complete the inventory sections and remove every placeholder |
| `threat-model.yaml` | threat TODOs | accepted and rejected threats | Add at least nine accepted threats and one rejected threat, with controls and detections |
| `threat-model.yaml` | crosswalk TODOs | NIST and OWASP mapping | Map the four NIST goals and at least four OWASP ML entries; decide on the LLM list |
| `report.md` | section TODOs | diagram, trees, controls, assumptions | Replace each prompt with the corresponding analysis |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-02-threat-model/CHECKING.md`.

## Reference results

The reference model (`solution.yaml` + `solution-report.md`) contains:

| Item | Value |
|---|---|
| Assets | 7 |
| Trust boundaries | 6 |
| Attack surfaces | 10 |
| Accepted threats | 11 |
| Rejected threats | 1 |
| Severity | 1 critical, 8 high, 2 medium |
| NIST goals | integrity 6, privacy 3, availability 1, abuse 1 |
| Attack classes | 9 |
| Lifecycle stages | 5 |
| Attack trees | 3 |
| OWASP ML entries | 6 |

A sound model may be larger. The checker enforces minimums and coverage, not equality with these counts.

## Deliverables checklist

| File | Contents |
|---|---|
| `threat-model.yaml` | Machine-checkable threat model |
| `report.md` | Data-flow diagram, narrative, ranking, controls, crosswalk, assumptions |

- [ ] Completed `threat-model.yaml` with no remaining TODO markers and a balanced set of threats.
- [ ] Completed `report.md` with the data-flow diagram, attack trees, control table, crosswalk, and rejected-threat rationale.
- [ ] `python check_threat_model.py --model threat-model.yaml --report report.md` exits 0.
- [ ] `report.md` answers every reflection question.

## Success criteria

- [ ] At least 6 assets, 5 boundaries, and 8 surfaces, all referenced by at least one accepted threat.
- [ ] At least 9 accepted threats and 1 rejected threat with a reopening condition.
- [ ] All five lifecycle stages and all four NIST goals represented.
- [ ] At least 6 attack classes and 3 attack trees.
- [ ] Severity arithmetic is correct; high and critical threats meet the control rule.
- [ ] Every accepted threat has a testable detection hypothesis.
- [ ] ATLAS and OWASP IDs come from the allowlists, not invention.
- [ ] The crosswalk covers all four AI RMF functions and at least four OWASP ML entries.
- [ ] The report has all twelve headings and a Mermaid diagram.
- [ ] `python check_threat_model.py --model threat-model.yaml --report report.md` exits 0.

## How to check yourself

```bash
cd labs/lab-02-threat-model
python -m pip install -r requirements.txt
python check_threat_model.py --model threat-model.yaml --report report.md
```

The checker prints PASS lines and exits nonzero on the first structural failure. `CHECKING.md` contains the failure table and the rubric.

The checker cannot judge whether the analysis is good. Use the rubric below and ask a second reader to challenge the top three threats.

## Rubric

Score each row 0–2; 12/18 is a pass, 15+ is strong work.

| Criterion | 2 — strong | 1 — adequate | 0 — weak |
|---|---|---|---|
| Adversary realism | Each actor has a plausible goal, access, and limit | Actors are named but capabilities are vague | "Hackers" with unlimited access |
| Boundary discipline | Boundaries separate real privilege or trust levels and carry controls | Some boundaries are decorative | Boxes without meaning |
| Coverage | Every asset, surface, stage, and goal is covered | One or two gaps | Technique list with no system model |
| Scoring | Scores follow stated assumptions and ties are explained | Plausible but unexplained | Arbitrary |
| Detection | Metric, baseline, and threshold for each threat | Some are measurable | "Monitor for attacks" |
| Controls | Preventive, detective, and corrective controls are specific | One category missing in places | "Use best practices" |
| Framework use | Accurate mappings and noted disagreements | Mostly correct | IDs as decoration |
| Rejection | Rejected threat with a reopening condition | Asserted rejection | Everything accepted, or nothing |

## Reflection questions

1. Which trust boundary carries the most risk, and why?
2. Which accepted threat has the weakest detection hypothesis?
3. What did you reject, and what assumption would make it acceptable?
4. Which control addresses more than one threat, and where does it fail?
5. What does the model not tell you about the real MediScan system?

## Hints

1. Draw the data flow before writing threats. Every arrow that changes owner, trust level, or storage location is a candidate trust boundary.
2. An attack surface is an entry point; a threat is an actor using it for a goal. Do not list the same item in both columns.
3. A detection hypothesis needs a metric, a baseline, and a threshold. `Monitor the logs` will not pass the checker or a security review.
4. Keep one plausible threat in the rejected list and state the assumption that made you reject it, plus what would reopen it.

## Time box

| Hour | Work |
|---|---|
| 1 | Read the brief, draw the diagram, list assets and boundaries |
| 2 | Surfaces, actors, threats, goals, stages |
| 3 | Score, rank, controls, detection hypotheses |
| 4 | Attack trees, crosswalk, rejected threat, report, checker |

If you pass 6 hours, stop and submit what you have with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Checker reports a missing asset reference | An asset is listed but never analyzed | Add a threat or remove the asset |
| A boundary has no covered surface | Boundary is decorative | Add a surface and a threat on that boundary |
| Severity mismatch | Score assigned by feel | Recompute `impact × likelihood` |
| High threat has high residual risk | No effective control | Add a control or record a risk acceptance |
| An ATLAS ID is rejected | ID invented or unverified | Use the allowlist or an empty list |
| Crosswalk incomplete | A RMF function was skipped | Add GOVERN, MAP, MEASURE, and MANAGE |
| Report heading missing | Template edited | Restore all twelve headings |

## Cleanup

No generated model artifacts are produced. If you edited `threat-model.yaml` or `report.md` and want to start over, restore them from `threat-model.yaml` and `report_template.md` in the lab package. Deactivate the virtual environment when finished.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — F-01, F-02, F-03, F-09
- [Module page](../modules/m03-threat-modeling/index.md) — M03 — Cybersecurity Fundamentals and ML Threat Modeling
- Package checking guide: `labs/lab-02-threat-model/CHECKING.md`

## What comes next

Module 04 uses this model to justify an evasion experiment. You will state the attacker's knowledge and budget before writing a single line of attack code, then measure success against the baseline from LAB-01.
