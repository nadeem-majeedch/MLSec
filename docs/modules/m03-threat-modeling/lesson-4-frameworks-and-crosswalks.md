# Lesson 03.4 — Risk Frameworks and Crosswalks

<a id="m03-l4"></a>

**1 hour · Lesson 4 of 5 · Module 03**

## What this lesson answers

How does a threat model connect to the frameworks an organization already uses? Frameworks are useful when they sharpen a decision and harmful when they become a checklist. This lesson covers the NIST AI Risk Management Framework, the OWASP ML and LLM lists, and the ISO standards you will hear named. It ends with a crosswalk method and a coverage check.

## Why frameworks exist

A framework gives a team shared words, a governance structure, and a way to compare systems. It does not tell you which threat matters in your system. That judgment still comes from the assets, boundaries, actors, and impact you established in Lessons 1–3.

Three failure modes are common:

- **Compliance theater.** The team maps every control to a framework and changes nothing.
- **Framework capture.** The register is reorganized to fit the framework's headings, and the system disappears.
- **False completeness.** A framework with ten categories makes a team feel covered even when a category is irrelevant and a real threat is missing.

Use a framework as a **lens**, not a **scorecard**.

## NIST AI Risk Management Framework

The AI RMF is organized around four functions:

| Function | Question | What it produces |
|---|---|---|
| **GOVERN** | Who is accountable, and what are the rules? | Roles, policies, risk tolerance, oversight |
| **MAP** | What is the system, its context, and its risks? | System model, stakeholders, risk framing |
| **MEASURE** | How do we know whether risks are managed? | Metrics, tests, monitoring, evaluation |
| **MANAGE** | What do we do about the risk? | Prioritization, response, residual risk, review |

The functions are not a lifecycle. GOVERN runs throughout; MAP, MEASURE, and MANAGE iterate.

The AI RMF also names trustworthiness characteristics, including valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair. A threat model usually touches secure and resilient, privacy-enhanced, safe, and accountable. It should say which characteristics it is **not** assessing. A threat model is not a fairness audit.

NIST published a companion profile for generative AI (NIST AI 600-1). It is a profile, not a separate framework. If your system uses an LLM, use the profile to add generative-specific risks to the same four functions.

### Mapping examples

| Threat | Primary function | Why |
|---|---|---|
| Insider flips labels | MAP, MEASURE | The label path must be mapped, and drift must be measured |
| Vendor backdoor | GOVERN, MANAGE | Signing authority and promotion are governance; response is management |
| Model extraction | GOVERN | Contracts, quotas, and IP policy are the primary levers |
| Triage outage | MANAGE | Downtime response and residual risk acceptance |

A threat can touch several functions. Pick the **primary** one and note the others; otherwise the crosswalk becomes a wall of checkmarks.

## OWASP ML Top 10

The OWASP ML Top 10 is an application-security list for ML systems. The 2023 edition contains:

| ID | Category | Typical MediScan threat |
|---|---|---|
| ML01 | Input manipulation attack | T1 adversarial image |
| ML02 | Data poisoning attack | T2 label flipping, T12 ingestion poisoning |
| ML03 | Model inversion attack | A privacy threat that reconstructs inputs |
| ML04 | Membership inference attack | T5 membership inference |
| ML05 | Model theft | T4 extraction |
| ML06 | AI supply chain attacks | T3 vendor update, T7 malicious dependency |
| ML07 | Transfer learning attack | A threat that abuses a pretrained base model |
| ML08 | Model skewing | A threat that shifts behavior for a subgroup |
| ML09 | Output integrity attack | T1, T9 priority manipulation |
| ML10 | Model poisoning | T3 backdoor |

Two cautions:

1. **The list is not exhaustive.** Availability and conventional credential attacks are not cleanly represented. An empty cell is a finding, not a failure.
2. **Editions change.** Cite the edition you used and verify the category names. Do not assume an ID from a blog post is current.

## OWASP Top 10 for LLM Applications

The LLM list applies when the system consumes natural-language instructions or untrusted context. The current edition includes categories such as prompt injection, sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency, system prompt leakage, vector and embedding weaknesses, misinformation, and unbounded consumption. Numbering has changed between editions; cite the edition you used.

For MediScan, the list is **not applicable** in this release: it is a vision classifier with no prompt path. That is a reasoned decision, not an omission. If a report-generation assistant is added, the crosswalk must be repeated, because retrieved text becomes a new surface.

A common mistake is to apply the LLM list to every AI system because it is newer. A vision classifier does not have a prompt-injection surface just because it uses a neural network.

## ISO/IEC standards

Two standards are often named in AI governance:

- **ISO/IEC 42001** specifies requirements for an AI management system. It is about organizational governance, not a specific model.
- **ISO/IEC 23894** provides guidance on AI risk management. It complements the AI RMF and uses similar concepts.

Both are paid standards. This course does not reproduce their text. If your organization is certified or pursuing certification, map the threat model to the management-system clauses your auditor will ask about. Do not claim compliance from a threat model alone.

## The crosswalk method

1. **Start from the register.** Do not start from the framework's table of contents.
2. **Map each threat to at most two primary functions.** Note secondary functions only when they change a decision.
3. **Map to an OWASP category only when the fit is real.** Leave the cell empty if the category does not describe the threat.
4. **Compute coverage.** Which functions are represented? Which goals and lifecycle stages are represented? Which threats have no mapping?
5. **Record gaps and disagreements as findings.** A gap is a question, not necessarily a defect.
6. **Do not let coverage change a score.** A threat is not more severe because a framework has a category for it.

### Worked example: find crosswalk gaps

```python
MAPPING = {
    "T1 evasion": {"rmf": ["MEASURE"], "owasp_ml": ["ML01"]},
    "T2 label poisoning": {"rmf": ["MAP", "MEASURE"], "owasp_ml": ["ML02"]},
    "T3 vendor backdoor": {"rmf": ["MANAGE"], "owasp_ml": ["ML06"]},
    "T4 model extraction": {"rmf": ["GOVERN"], "owasp_ml": ["ML05"]},
    "T5 membership inference": {"rmf": ["MEASURE"], "owasp_ml": []},
    "T6 triage outage": {"rmf": ["MANAGE"], "owasp_ml": []},
}
REQUIRED_RMF = {"GOVERN", "MAP", "MEASURE", "MANAGE"}

covered_rmf = set()
covered_owasp = set()
unmapped = []
for threat, mapping in MAPPING.items():
    covered_rmf.update(mapping["rmf"])
    covered_owasp.update(mapping["owasp_ml"])
    if not mapping["rmf"] or not mapping["owasp_ml"]:
        unmapped.append(threat)

print("RMF covered:", ", ".join(sorted(covered_rmf)))
print("RMF missing:", ", ".join(sorted(REQUIRED_RMF - covered_rmf)) or "none")
print("OWASP ML covered:", ", ".join(sorted(covered_owasp)))
print("Threats with a crosswalk gap:")
for threat in unmapped:
    print(f"  {threat}")
```

Expected output:

```text
RMF covered: GOVERN, MANAGE, MAP, MEASURE
RMF missing: none
OWASP ML covered: ML01, ML02, ML05, ML06
Threats with a crosswalk gap:
  T5 membership inference
  T6 triage outage
```

The RMF coverage looks complete, but two threats have no OWASP ML mapping. That is the useful result:

- **T5** should map to ML04 (membership inference). The empty cell is a data-entry gap.
- **T6** is an availability threat. The ML Top 10 does not have a clean availability category. The gap is real; record it and explain that availability is covered by the AI RMF's secure-and-resilient characteristic and by conventional service controls.

A crosswalk that reports "100% coverage" on the first pass is usually hiding a mapping decision like this one.

## Where frameworks disagree

| Issue | NIST AI 100-2 | AI RMF | OWASP ML |
|---|---|---|---|
| Model extraction | Abuse of functionality | Governance and IP risk | Model theft |
| Poisoning | Integrity or availability, depending on effect | Map and measure | ML02 and ML10 |
| Availability | An attack goal | Secure and resilient characteristic | Weakly represented |
| Prompt injection | An attack class for generative systems | Generative AI profile | Not in the ML list |

Record the disagreement in one sentence. It shows a reader that you used the frameworks thoughtfully rather than pasting labels.

## Common mistakes and troubleshooting

| Mistake | Symptom | Fix |
|---|---|---|
| Framework drives the register | Headings are RMF functions, not system stages | Reorganize by asset and surface, then map |
| Everything maps to everything | Every threat has four functions and three OWASP IDs | Choose the primary mapping and justify it |
| 100% coverage claimed | No gaps reported | Look for availability and conventional attacks |
| LLM list applied to a vision model | Prompt injection appears with no prompt surface | State non-applicability and why |
| Compliance claimed from a threat model | "We are ISO 42001 compliant" | A threat model is evidence, not certification |
| ISO text reproduced | Copyright risk | Cite the standard by name and number only |

## Check yourself

| Question | Answer |
|---|---|
| What are the four AI RMF functions? | GOVERN, MAP, MEASURE, MANAGE. |
| Why is an empty OWASP mapping sometimes correct? | The category may not describe the threat, or the list may not cover the harm (for example, availability). |
| Does mapping to a framework increase a threat's severity? | No. Severity comes from impact and likelihood, not from framework coverage. |
| When does the OWASP LLM list apply? | When the system consumes natural-language instructions or untrusted context. |
| What is the difference between ISO/IEC 42001 and 23894? | 42001 is an AI management-system standard; 23894 is AI risk-management guidance. |

## Summary and key takeaways

- Frameworks provide shared language and governance, not a verdict on your system.
- The AI RMF's four functions are GOVERN, MAP, MEASURE, and MANAGE; profiles adapt them to a context.
- The OWASP ML Top 10 is useful for ML-specific application risks but weakly covers availability and conventional attacks.
- The OWASP LLM list applies only when there is a language or untrusted-context surface.
- Crosswalks should produce findings, not a wall of checkmarks.
- Record disagreements between frameworks instead of forcing one label.

## Next step

[Lesson 03.5 — Building, scoring, and communicating the model](lesson-5-building-the-model.md) turns everything into a scored register, attack trees, controls, and a report that another person can audit.
