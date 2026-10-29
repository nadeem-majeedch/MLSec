# Checking Guide — LAB-02

This guide lets a learner check a threat model without an instructor. The checker validates structure and consistency. The rubric at the end addresses the part a script cannot judge: whether the reasoning is sound.

## Reference model

| Item | Reference value |
|---|---|
| System | MediScan Triage Assistant |
| Assets | 7 |
| Trust boundaries | 6 |
| Attack surfaces | 10 |
| Accepted threats | 11 |
| Rejected threats | 1 |
| Severity spread | 1 critical, 8 high, 2 medium, 0 low |
| NIST goals | integrity 6, privacy 3, availability 1, abuse 1 |
| Attack classes | 9 |
| Lifecycle stages | 5 of 5 |
| Attack trees | 3 |
| OWASP ML entries | 6 |
| ATLAS IDs | AML.T0015, T0018, T0020, T0024, T0040, T0043 |

A sound model may be larger. The checker enforces minimums and coverage, not equality with these counts.

## How to check

From `labs/lab-02-threat-model/`:

```bash
python -m pip install -r requirements.txt
python check_threat_model.py --model solution.yaml --report solution-report.md
python check_threat_model.py --model threat-model.yaml --report report.md
```

`check_threat_model.py` exits 0 only if every check passes. Add `--summary out.json` to write the machine-readable summary.

## What the checker verifies

1. **Schema.** `system` has name, owner, description, and deployment. Assets have ID, name, description, CIA, and sensitivity. Boundaries have ID, name, between, and controls. Surfaces have ID, name, boundary, entry point, and attacker access.
2. **Minimums.** At least 6 assets, 5 boundaries, 8 surfaces, 9 accepted threats, 1 rejected threat, and 3 attack trees.
3. **References.** Every asset and surface ID is unique and exists. Every threat's assets and surfaces resolve. Every attack-tree step names an accepted threat.
4. **Threat fields.** Accepted threats contain actor, knowledge, capability, assumptions, impact, likelihood, severity, impact statement, mitigations, detection hypothesis, and residual risk.
5. **Severity arithmetic.** `severity` must equal the band for `impact × likelihood`: 1–4 low, 5–9 medium, 10–16 high, 17–25 critical.
6. **Control rule.** High and critical threats need at least two preventive controls and one detective control, and cannot carry high residual risk.
7. **ATLAS allowlist.** Only verified technique IDs are accepted: T0015, T0018, T0020, T0024, T0040, T0043, T0051. Use an empty list rather than inventing an ID.
8. **Coverage.** Every asset and surface is referenced by an accepted threat; every boundary owns at least one referenced surface; all five lifecycle stages and all four NIST goals appear; at least six attack classes appear.
9. **Crosswalk.** All four AI RMF functions have a note; at least four valid OWASP ML IDs map to accepted threats; OWASP LLM states applicability with a rationale when not applicable.
10. **Report.** All twelve headings are present, the report contains a Mermaid block, and at least one `TB` label appears.

## Diagnosing failures

| Message | Likely cause | Fix |
|---|---|---|
| `missing model file` | Running from the wrong directory | `cd labs/lab-02-threat-model` |
| `at least 6 assets are required` | Assets were merged into one row | Separate data, model, labels, availability, logs, credentials, vendor channel |
| `references unknown AS7` | Surface ID typo or deleted surface | Use the exact ID from the surfaces list |
| `severity is high; 2x3 should be medium` | Score was assigned by feel | Multiply impact by likelihood, then band it |
| `fewer than two preventive controls` | A high/critical threat has one control | Add a preventive control or lower the score with evidence |
| `residual_risk high` on a high threat | No control reduces the risk | Add a control or record an explicit risk acceptance in the report |
| `assets with no accepted threat` | An asset was listed but never analyzed | Add a threat or remove the asset |
| `trust boundary TB3 has no surface covered` | A boundary is decorative | Add a surface on that boundary and a threat that uses it |
| `missing ['monitoring']` | Lifecycle stages are incomplete | Add a monitoring-stage threat |
| `missing ['availability']` | No denial-of-service or outage threat | Add the outage path and score it |
| `unsupported ID AML.T9999` | Invented ATLAS ID | Use the allowlist or an empty list |
| `crosswalk.ai_rmf must cover all four functions` | GOVERN or MANAGE omitted | Add a note for each function |
| `report is missing heading` | Template headings changed | Restore the twelve headings |
| `report must contain at least one Mermaid diagram` | Diagram is an image or omitted | Add a Mermaid `flowchart` |

## Rubric (instructor-independent)

Score each row 0–2. A total of 12 or more out of 18 is a pass; 15 or more is strong work.

| Criterion | 2 — strong | 1 — adequate | 0 — weak |
|---|---|---|---|
| Adversary realism | Each actor has a plausible goal, access, and limit | Actors are named but capabilities are vague | "Hackers" with unlimited access |
| Boundary discipline | Every boundary separates real privilege or trust levels and has a control | Boundaries exist but some are decorative | Boxes without meaning |
| Coverage | Every asset, surface, stage, and NIST goal is covered | One or two gaps | Technique list with no system model |
| Scoring | Scores follow stated assumptions and ties are explained | Scores are plausible but unexplained | Scores are arbitrary |
| Detection hypotheses | Each is a metric, a baseline, and a threshold | Some are measurable | "Monitor for attacks" |
| Controls | Preventive, detective, and corrective controls are specific | One category is missing for some threats | "Use best practices" |
| Framework use | Mappings are accurate and disagreements are noted | Mappings are mostly correct | IDs are decoration |
| Rejection | At least one threat is rejected with a reopening condition | Rejection is asserted | Everything is accepted, or nothing is |

## Integrity notes

- A passing checker means the model is structurally complete. It does not mean the severity scores are correct. Have a second reader challenge the top three threats.
- Do not invent ATLAS IDs, OWASP IDs, or framework functions to satisfy the checker. An empty ATLAS list is valid; a fabricated ID is not.
- If you change the scenario, update the system block, the asset/surface lists, and the report together. A model that passes with stale references is worse than one that fails honestly.
- The checker never contacts the network.

## Reflection questions

1. Which trust boundary carries the most risk, and why?
2. Which accepted threat has the weakest detection hypothesis?
3. What did you reject, and what assumption would make it acceptable?
4. Which control addresses more than one threat, and where does it fail?
5. What does the model not tell you about the real MediScan system?
