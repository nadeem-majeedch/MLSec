# Module 03 Exercise Solutions

**Model answers and marking notes.** Read after a first attempt. Several exercises accept more than one sound answer; the criteria below say what makes an answer defensible.

---

## Exercise 1 — Find the unlabelled trust crossings

The audit checks two conditions at once: the flow has no boundary label, and its endpoints are in different zones. Either condition alone is not a finding.

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


def findings(flows, zones):
    out = []
    for flow in flows:
        if flow["boundary"] is None and zones[flow["src"]] != zones[flow["dst"]]:
            out.append((flow["src"], zones[flow["src"]], flow["dst"], zones[flow["dst"]]))
    return out


for src, src_zone, dst, dst_zone in findings(FLOWS, ZONE):
    print(f"{src} ({src_zone}) -> {dst} ({dst_zone})")
print("count:", len(findings(FLOWS, ZONE)))
```

Expected output:

```text
trip store (ingest) -> training job (ml)
feature store (ml) -> inference API (serve)
model registry (deploy) -> inference API (serve)
trip store (ingest) -> analytics export (analytics)
count: 4
```

**Repair.** Assign `TB6` to trip store → training, `TB7` to feature store → inference, `TB8` to registry → inference, and `TB9` to trip store → export. Rerun: `count: 0`.

**Control for one boundary.** For `TB6` (ingest → training), a read-only dataset snapshot with a recorded hash and no write-back to production is a control that matches the trust change. For `TB9` (ingest → analytics), the control is a de-identification job plus export approval.

**Marking.** Four findings, a zero after repair, and a control that addresses the specific crossing. A student who labels every `None` flow fails the "same zone" test (ingestion → trip store is fine without a boundary).

---

## Exercise 2 — One threat, three adversaries

There is no single correct likelihood. A defensible answer explains the number from the profile.

| Threat | Impact | External user | Insider | Vendor |
|---|---:|---:|---:|---:|
| Evasion of the ETA model | 5 | 4 | 3 | 4 |
| Poisoning of trip labels | 5 | 1 | 4 | 3 |
| Model extraction via the API | 3 | 3 | 2 | 2 |
| ETA service outage | 4 | 2 | 2 | 3 |

**Scores.**

| Profile | Evasion | Poisoning | Extraction | Outage | Top |
|---|---:|---:|---:|---:|---|
| External user | 20 | 5 | 9 | 8 | Evasion (20, critical) |
| Insider | 15 | 20 | 6 | 8 | Poisoning (20, critical) |
| Vendor | 20 | 15 | 6 | 12 | Evasion (20, critical) |

**Why the top changes.** The external user can query the API cheaply, so evasion is the accessible path. The insider holds label authority, so poisoning becomes both feasible and high-impact. The vendor has white-box knowledge of the model and a deployment channel, so evasion and a bad update both become plausible; the example scores evasion highest, but a defensible answer could put the vendor's outage/backdoor path at 20 and rank it first.

**Assumption that would lower the insider's score.** "Overrides enter retraining without a second approver." If dual approval and label provenance are enforced, the insider's likelihood drops, and the poisoning score falls from 20 to 10–12.

**Marking.** Full credit for scores that follow the anchors, justifications that name knowledge/capability/authority, and a top-threat explanation. Deduct for one likelihood reused across all profiles without justification.

---

## Exercise 3 — Crosswalk and gaps

**Model mapping.**

| Threat | AI RMF (primary) | OWASP ML |
|---|---|---|
| T1 Evasion | MEASURE | ML01 |
| T2 Label poisoning | MAP, MEASURE | ML02 |
| T3 Backdoor in vendor update | MANAGE | ML06, ML10 |
| T4 Model extraction | GOVERN | ML05 |
| T5 Membership inference | MEASURE | ML04 |
| T6 Triage outage | MANAGE | none |

```python
MAPPING = {
    "T1 Evasion": {"rmf": ["MEASURE"], "owasp_ml": ["ML01"]},
    "T2 Label poisoning": {"rmf": ["MAP", "MEASURE"], "owasp_ml": ["ML02"]},
    "T3 Backdoor in vendor update": {"rmf": ["MANAGE"], "owasp_ml": ["ML06", "ML10"]},
    "T4 Model extraction": {"rmf": ["GOVERN"], "owasp_ml": ["ML05"]},
    "T5 Membership inference": {"rmf": ["MEASURE"], "owasp_ml": ["ML04"]},
    "T6 Triage outage": {"rmf": ["MANAGE"], "owasp_ml": []},
}
REQUIRED_RMF = {"GOVERN", "MAP", "MEASURE", "MANAGE"}

covered_rmf, covered_owasp, gaps = set(), set(), []
for threat, mapping in MAPPING.items():
    covered_rmf.update(mapping["rmf"])
    covered_owasp.update(mapping["owasp_ml"])
    if not mapping["rmf"] or not mapping["owasp_ml"]:
        gaps.append(threat)

print("RMF covered:", ", ".join(sorted(covered_rmf)))
print("RMF missing:", ", ".join(sorted(REQUIRED_RMF - covered_rmf)) or "none")
print("OWASP ML covered:", ", ".join(sorted(covered_owasp)))
print("Threats with a crosswalk gap:", ", ".join(gaps) or "none")
```

Expected output:

```text
RMF covered: GOVERN, MANAGE, MAP, MEASURE
RMF missing: none
OWASP ML covered: ML01, ML02, ML04, ML05, ML06, ML10
Threats with a crosswalk gap: T6 Triage outage
```

**Gap explanation.** T6 has no OWASP ML category because the ML Top 10 is organized around model-centric application risks and does not include a clean availability category. This is a **real limitation of the list**, not a modeling error. Availability is covered by the AI RMF's secure-and-resilient characteristic and by conventional service controls (rate limits, failover, backups).

**Filling a missing function.** All four functions are already covered in this mapping. If one were missing — for example, if no threat mapped to GOVERN — a governance threat such as "no owner for vendor signing" or "no data-use approval" would fill it. Do not invent a technical threat to satisfy a function.

**Marking.** Full credit for all four functions considered, at least one gap explained as a real limitation, and no fabricated OWASP IDs. Deduct for mapping every threat to all four functions.

---

## Exercise 4 — Scenario: ResumeRank

This is a model answer, not the only acceptable one. It demonstrates the required coverage and the reasoning a grader looks for.

### Assets

| ID | Asset | Why it matters |
|---|---|---|
| A1 | Applicant PII and resumes | Identity, contact data, employment history |
| A2 | Ranking model | Determines who gets seen |
| A3 | Recruiter decision labels | Control future model behavior and encode bias |
| A4 | Scoring availability | Recruiters depend on it during hiring cycles |
| A5 | Audit export and logs | Evidence for fairness and incident review |
| A6 | Vendor assessment feed | Influences features and scores |
| A7 | Deployment credentials | Control what reaches production |

### Trust boundaries

| ID | Boundary | Between |
|---|---|---|
| TB1 | Applicant to upload | Public applicant, upload API |
| TB2 | Vendor to feature store | Assessment vendor, internal feature store |
| TB3 | Training to serving | Training pipeline, model registry, inference |
| TB4 | Scoring to recruiter | Inference API, recruiter dashboard |
| TB5 | Audit export to auditor | Internal analytics, external auditor |
| TB6 | Administration to production | Support admins, production console |

### Attack surfaces

Upload API (TB1), parser dependencies (TB1), recruiter review UI and accounts (TB4), label store and feedback loop (TB3), model registry and CI (TB3), scoring API (TB4), vendor feed (TB2), audit export (TB5), admin console (TB6). Nine surfaces.

### Threat register

| ID | Threat | Goal | Class | Stage | I×L | Band |
|---|---|---|---|---|---:|---|
| T1 | Keyword-stuffed resume boosts rank | Integrity | Evasion | Data collection | 4×4 | High (16) |
| T2 | Recruiter feedback poisons labels | Integrity | Poisoning | Training | 5×3 | High (15) |
| T3 | Vendor feed poisoning | Integrity | Poisoning | Data collection | 4×2 | Medium (8) |
| T4 | Parser dependency exfiltrates resumes | Privacy | Data exfiltration | Artifact | 5×3 | High (15) |
| T5 | Model extraction via scoring API | Abuse | Extraction | Serving | 3×4 | High (12) |
| T6 | Membership inference via scores and audit export | Privacy | Membership inference | Monitoring | 4×3 | High (12) |
| T7 | Credential stuffing on recruiter accounts | Integrity | Credential abuse | Serving | 4×3 | High (12) |
| T8 | Scoring outage during hiring peak | Availability | Denial of service | Serving | 4×2 | Medium (8) |
| T9 | Audit log tampering | Integrity | Log tampering | Monitoring | 3×2 | Medium (6) |
| T10 | Laptop theft exposes cached resumes | Privacy | Data exfiltration | Artifact | 4×1 | Low (4) — rejected |

All four goals appear (integrity, privacy, abuse, availability), and all five stages appear. Eight attack classes appear.

**Tie-break.** Applicant fairness and access to opportunity first, then privacy, then availability, then financial and reputational harm.

**Top three:** T1 (16), T2 (15), T4 (15). T2 and T4 tie; fairness comes before privacy in the published rule, so T2 ranks above T4.

### Attack trees

**AT1 — Boost an unqualified applicant.** Submit a keyword-stuffed resume (T1) → submit variants to learn what the parser rewards (T1) → or compromise a recruiter account to advance the candidate directly (T7) → or query the scoring API to infer feature weights (T5).

**AT2 — Exfiltrate applicant data.** Compromise a parser dependency (T4) → use the audit export to move records (T6) → alter audit logs to hide the export (T9).

### Controls and detection for the top three

| Threat | Preventive | Detective | Corrective | Detection hypothesis |
|---|---|---|---|---|
| T1 | Structured fields for key qualifications; human review before auto-advance; text-anomaly screening | Score distribution by keyword density; canary resumes with known qualifications | Re-review the batch; retrain without the manipulated pattern | Share of applicants with more than 20 rare skill keywords triples above the 30-day baseline while their mean score exceeds 90 |
| T2 | Dual approval for bulk decisions; label provenance; fairness audit; canary labels | Per-recruiter approval and rejection rates against peer median | Revert labels; retrain from a trusted snapshot; review affected applicants | A recruiter's rejection rate for a protected group deviates by more than two standard deviations from the peer median for two consecutive cycles |
| T4 | Hash-pinned dependencies; private package index; egress deny | Container egress alerts; SBOM diff on every build | Rebuild the image; rotate credentials; start breach assessment | The parser container opens an outbound connection to any host outside the allowlist |

### Rejected threat

**T10 — Laptop theft exposes cached resumes.** Rejected because resumes are not cached locally, full-disk encryption is enforced, and device disposal is logged. Reopen if a local cache is introduced or encryption is removed. Detection remains: a missing disposal certificate or an encrypted device reported lost with an active session.

### Crosswalk

| Framework | Mapping |
|---|---|
| AI RMF | GOVERN: label and vendor ownership; MAP: applicant data flows; MEASURE: fairness and drift metrics; MANAGE: incident response and residual risk |
| OWASP ML | ML01 → T1; ML02 → T2, T3; ML04 → T6; ML05 → T5; ML06 → T4; ML09 → T1, T7 |
| OWASP LLM | Not applicable: no natural-language prompt path in this release |
| Gap | T8 (availability) has no clean OWASP ML category; note it rather than forcing a mapping |

### Assumptions that would change the ranking

- Recruiter decisions are used as labels without review. If labels are audited, T2 falls.
- The parser has outbound network access. If egress is denied, T4 falls.
- The scoring API returns a numeric score. If it returns only "advance/reject," T5 becomes harder.

### Marking

| Criterion | Points |
|---|---:|
| At least 6 assets, 5 boundaries, 8 surfaces | 3 |
| 8+ threats, all 4 goals, 4+ stages | 3 |
| Correct scores, stated tie-break, top three | 2 |
| Two attack trees with 3+ steps | 2 |
| Controls and detection for top three | 3 |
| Rejection with reopening condition | 2 |
| Crosswalk with a gap or disagreement | 2 |
| Assumptions that would change the ranking | 1 |
| **Total** | **18** |

A pass is 12/18. Full credit for a different but defensible ranking requires the tie-break to be published before the ranking and applied consistently.
