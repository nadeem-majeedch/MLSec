# LAB-02 — Threat Model an ML System

| Field | Value |
|---|---|
| Lab ID | LAB-02 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M03 — Threat Modeling |
| Outcomes | LO-03, LO-28 |
| Prerequisites | M03 lessons 1–4; LAB-01B or equivalent |
| Data | none; fictional system |
| Compute | CPU only; instant |

Full brief: [docs/labs/lab-02.md](../../docs/labs/lab-02.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

**MediScan Triage Assistant** is a fictional radiology triage system. It scores chest X-ray studies as routine, urgent, or critical and places them on a radiologist worklist. Images arrive from six hospital sites, pass through a preprocessing service, are scored by a vendor-supplied vision model, and are reviewed by a radiologist. Overrides feed a monthly retraining job, and an analytics team exports de-identified data to research partners.

The system is fictional. No real patient data, vendor, or endpoint is involved.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python check_threat_model.py --model solution.yaml --report solution-report.md

# your path
python check_threat_model.py --model threat-model.yaml --report report.md
```

## What you produce

- Completed `threat-model.yaml` with no remaining TODO markers and a balanced set of threats.
- Completed `report.md` with the data-flow diagram, attack trees, control table, crosswalk, and rejected-threat rationale.
- `python check_threat_model.py --model threat-model.yaml --report report.md` exits 0.
- `report.md` answers every reflection question.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `threat-model.yaml` | schema TODOs | assets, boundaries, attack surfaces | Complete the inventory sections and remove every placeholder |
| `threat-model.yaml` | threat TODOs | accepted and rejected threats | Add at least nine accepted threats and one rejected threat, with controls and detections |
| `threat-model.yaml` | crosswalk TODOs | NIST and OWASP mapping | Map the four NIST goals and at least four OWASP ML entries; decide on the LLM list |
| `report.md` | section TODOs | diagram, trees, controls, assumptions | Replace each prompt with the corresponding analysis |

## Hints

- Draw the data flow before writing threats. Every arrow that changes owner, trust level, or storage location is a candidate trust boundary.
- An attack surface is an entry point; a threat is an actor using it for a goal. Do not list the same item in both columns.
- A detection hypothesis needs a metric, a baseline, and a threshold. `Monitor the logs` will not pass the checker or a security review.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_threat_model.py` | Independent artifact checker |
| `expected_summary.json` | Reference values and tolerances |
| `report.md` | Learner report skeleton |
| `report_template.md` | Report headings and prompts |
| `requirements.txt` | Pinned dependencies |
| `solution-report.md` | Reference narrative, diagram, and ranking |
| `solution.yaml` | Reference threat model |
| `threat-model.yaml` | Learner starter with schema and TODOs |

## Safety and cleanup

The system is fictional. No patient data, vendor, endpoint, or credential is used. The checker reads only the two files you give it and makes no network calls.

Restore `threat-model.yaml` and `report.md` from the templates if you want to start over. No model artifacts are generated.
