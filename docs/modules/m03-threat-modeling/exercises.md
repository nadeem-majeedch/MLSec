---
title: Module 03 Exercises
---

# Module 03 Exercises

**Four exercises · about 60–90 minutes · Complete after the lessons**

Write your work in `work/m03/`. Run the code; do not only read it. Compare with the [solutions](exercise-solutions.md) after a first attempt.

---

## Exercise 1 — Find the unlabelled trust crossings

**Goal.** Audit a data-flow list for flows that change zone without a boundary label.

**Scenario.** ParcelPilot is a fictional delivery-ETA system. A driver app sends location updates; a training job learns from trip data; a weather vendor supplies features; a model registry deploys to inference; a support agent uses an admin console; an analytics job exports to a partner.

**Data.**

```python
FLOWS = [
    {"src": "driver app", "dst": "location ingest", "boundary": "TB1"},
    {"src": "location ingest", "dst": "trip store", "boundary": None},
    {"src": "trip store", "dst": "training job", "boundary": None},
    {"src": "weather vendor", "dst": "feature store", "boundary": "TB2"},
    {"src": "feature store", "dst": "inference API", "boundary": None},
    {"src": "model registry", "dst": "inference API", "boundary": None},
    {"src": "inference API", "dst": "customer app", "boundary": "TB3"},
    {"src": "support agent", "dst": "admin console", "boundary": "TB4"},
    {"src": "trip store", "dst": "analytics export", "boundary": None},
    {"src": "analytics export", "dst": "research partner", "boundary": "TB5"},
]

ZONE = {
    "driver app": "edge",
    "customer app": "edge",
    "location ingest": "ingest",
    "trip store": "ingest",
    "training job": "ml",
    "weather vendor": "vendor",
    "feature store": "ml",
    "model registry": "deploy",
    "inference API": "serve",
    "support agent": "corp",
    "admin console": "admin",
    "analytics export": "analytics",
    "research partner": "partner",
}
```

**Tasks.**

1. Write a function that prints every flow where `boundary is None` and the source and destination zones differ.
2. Report the findings with source zone and destination zone.
3. Assign new boundary IDs (`TB6`, `TB7`, …) to each finding and rerun. Report the count after the fix.
4. For one finding, name one control you would attach to the new boundary.

**Deliverable.** `work/m03/boundaries.py` and a five-line note.

**Success criteria.** Four findings before the fix; zero after; each new boundary has a control that matches the trust change.

---

## Exercise 2 — One threat, three adversaries

**Goal.** Show how likelihood and ranking change with the adversary profile.

**Data.**

| Threat | Impact |
|---|---:|
| Evasion of the ETA model | 5 |
| Poisoning of trip labels | 5 |
| Model extraction via the API | 3 |
| ETA service outage | 4 |

Profiles:

- **External user:** black-box API access, low budget, no insider authority.
- **Insider:** partial knowledge, can edit labels and support tickets, medium budget.
- **Vendor:** white-box on the model, can publish an update, high budget.

**Tasks.**

1. Assign a likelihood from 1–5 for each threat under each profile. Write a one-sentence justification per cell.
2. Compute `impact × likelihood` and print a ranked table per profile.
3. Identify the top threat for each profile. Explain, in two sentences, why the top threat changes.
4. Name one assumption that, if false, would lower the insider's top score.

**Deliverable.** `work/m03/profiles.py` and `work/m03/profiles.md`.

**Success criteria.** Scores use the course bands; justifications refer to knowledge, capability, or authority; the explanation names a real assumption rather than "the insider is dangerous."

---

## Exercise 3 — Crosswalk and gaps

**Goal.** Map six threats to the NIST AI RMF and OWASP ML Top 10, then report gaps.

**Data.**

| Threat | NIST goal |
|---|---|
| T1 Evasion | Integrity |
| T2 Label poisoning | Integrity |
| T3 Backdoor in a vendor update | Integrity |
| T4 Model extraction | Abuse |
| T5 Membership inference | Privacy |
| T6 Triage outage | Availability |

**Tasks.**

1. For each threat, choose at most two primary AI RMF functions and one or two OWASP ML IDs. Leave a cell empty when the fit is not real.
2. Write a script that prints which RMF functions are covered, which are missing, and which threats have no RMF or no OWASP mapping.
3. Explain each gap in one sentence. For T6, state whether the gap is a modeling error or a real limitation of the OWASP ML list.
4. Add one threat that would fill a missing function, or explain why no such threat exists.

**Deliverable.** `work/m03/crosswalk.py` and `work/m03/crosswalk.md`.

**Success criteria.** All four RMF functions are considered; at least one gap is reported and explained; the OWASP IDs are from the ML01–ML10 list.

---

## Exercise 4 — Scenario: threat-model ResumeRank

**Goal.** Produce a mini threat model for a fictional hiring system, including a rejection and a detection hypothesis.

**Scenario.** ResumeRank ranks job applicants for a recruiter:

- Applicants upload PDF/DOCX resumes through a public API.
- A parsing service extracts education, skills, and years of experience.
- A gradient-boosted model scores each applicant from 0 to 100.
- Recruiters see a ranked list and mark candidates as "advance" or "reject."
- Those decisions become labels for monthly retraining.
- A third-party assessment vendor supplies test scores through a nightly feed.
- An audit team receives a monthly export of scores and decisions.
- Support administrators can access the production console.

**Tasks.**

1. List at least six assets and five trust boundaries.
2. List at least eight attack surfaces.
3. Write at least eight accepted threats. Cover all four NIST goals and at least four lifecycle stages.
4. Score each threat (impact 1–5, likelihood 1–5, band). Rank the top three and state your tie-break rule.
5. Write two attack trees, each with at least three steps.
6. For the top three threats, give preventive, detective, and corrective controls and a detection hypothesis with a metric, baseline, and threshold.
7. Reject one threat with a reopening condition.
8. Map the threats to the AI RMF and at least three OWASP ML categories. Note one disagreement or gap.

You may write YAML, Markdown tables, or both. The output must be readable without your explanation.

**Deliverable.** `work/m03/resumerank-threat-model.md` (and optional `resumerank.yaml`).

**Success criteria.**

- At least eight threats, all four NIST goals, at least four lifecycle stages.
- Scores use the course bands and the ranking has a stated tie-break.
- At least one threat is rejected with a reopening condition.
- Each top-three threat has a specific control set and a measurable detection hypothesis.
- At least one threat involves the feedback loop (recruiter decisions → training labels).
- The report states one assumption that would change the ranking.

---

## Portfolio checklist

- [ ] `boundaries.py` with four findings before and zero after
- [ ] `profiles.py` and `profiles.md` with three ranked tables
- [ ] `crosswalk.py` and `crosswalk.md` with at least one explained gap
- [ ] `resumerank-threat-model.md` with eight threats, two trees, and a rejection
- [ ] Five-line reflection: what you misunderstood, what you would test next, which assumption is weakest

Then run [LAB-02](../../labs/lab-02.md). The lab turns the method into a machine-checkable artifact.
