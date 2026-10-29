# Lesson 03.3 — Attack Surfaces, Lifecycle, and ATLAS

<a id="m03-l3"></a>

**1.5 hours · Lesson 3 of 5 · Module 03**

## What this lesson answers

Where, in the life of an ML system, can an adversary act? This lesson places surfaces on the ML lifecycle, draws a data-flow diagram, and introduces MITRE ATLAS as a technique index. The goal is not to list every technique. It is to attach the right technique to a surface you can already defend.

## The ML lifecycle is an attack surface map

An ML system is not a model. It is a pipeline that collects data, trains, packages, serves, and monitors. Each stage has its own surfaces and its own evidence.

| Stage | What exists | Surfaces | Typical threats |
|---|---|---|---|
| **Data collection** | Sensors, upload APIs, labelers, scraped corpora | Upload endpoint, label store, collection credentials | Poisoning, label flipping, data exfiltration |
| **Training** | Data snapshot, code, hyperparameters, compute | Training job, dependency lockfile, experiment tracker | Poisoning, backdoor, code execution, model skewing |
| **Artifact** | Weights, preprocessing, tokenizer, registry | Registry, serialization format, signing key | Backdoor, artifact swap, malicious deserialization |
| **Serving** | API, UI, autoscaling, quotas | Prediction endpoint, worklist, query quota | Evasion, extraction, denial of service, credential abuse |
| **Monitoring** | Logs, metrics, alerts, retention | Log store, alerting rules, dashboards | Log tampering, detection evasion, data overreach |
| **People and process** | Support, vendor access, approvals | Admin console, shared account, change ticket | Insider abuse, privilege misuse, social engineering |

A threat model that covers only serving is a partial model. Poisoning begins earlier; detection happens later; credentials cross every stage.

## Data-flow diagrams

A data-flow diagram (DFD) has five element types:

| Element | Meaning | Example |
|---|---|---|
| External entity | A person or system outside your control | Acquisition device, research partner |
| Process | Code that transforms data | Preprocessing, training, inference |
| Data store | Data at rest | Image store, model registry, log store |
| Data flow | Data moving between elements | Upload, export, deployment |
| Trust boundary | A change in privilege or trust | Hospital to cloud, vendor to registry |

Four rules make a DFD useful:

1. **Every flow has a direction and a name.** An unlabeled arrow is a guess.
2. **Every boundary is crossed by at least one flow.** A boundary with no flow is decoration.
3. **A store does not send data directly to another store.** A process reads and writes; otherwise you cannot say what transformed the data.
4. **The diagram and the register use the same IDs.** `TB3` in the picture must be `TB3` in the YAML.

### Worked example: generate a Mermaid DFD

The following script turns a node table and a flow list into Mermaid. It enforces shapes by element type and labels every boundary.

```python
NODES = {
    "DEV": ("Acquisition device", "actor"),
    "ING": ("Ingestion API", "process"),
    "STORE": ("Image store", "store"),
    "TRAIN": ("Training job", "process"),
    "REG": ("Model registry", "store"),
    "INF": ("Inference API", "process"),
    "WL": ("Clinician worklist", "actor"),
    "VEND": ("Vendor build", "actor"),
    "EXP": ("Export job", "process"),
    "PART": ("Research partner", "actor"),
}

FLOWS = [
    ("DEV", "ING", "TB1"),
    ("ING", "STORE", ""),
    ("STORE", "TRAIN", "TB2"),
    ("VEND", "REG", "TB3"),
    ("REG", "INF", "TB8"),
    ("INF", "WL", "TB4"),
    ("STORE", "EXP", "TB7"),
    ("EXP", "PART", "TB5"),
]


def shape(label, kind):
    if kind == "store":
        return f"[({label})]"
    if kind == "process":
        return f"([{label}])"
    return f"[{label}]"


lines = ["flowchart LR"]
for code, (label, kind) in NODES.items():
    lines.append(f"  {code}{shape(label, kind)}")
for src, dst, boundary in FLOWS:
    arrow = f"-->|{boundary}|" if boundary else "-->"
    lines.append(f"  {src} {arrow} {dst}")

print("\n".join(lines))
```

Expected output:

```text
flowchart LR
  DEV[Acquisition device]
  ING([Ingestion API])
  STORE[(Image store)]
  TRAIN([Training job])
  REG[(Model registry)]
  INF([Inference API])
  WL[Clinician worklist]
  VEND[Vendor build]
  EXP([Export job])
  PART[Research partner]
  DEV -->|TB1| ING
  ING --> STORE
  STORE -->|TB2| TRAIN
  VEND -->|TB3| REG
  REG -->|TB8| INF
  INF -->|TB4| WL
  STORE -->|TB7| EXP
  EXP -->|TB5| PART
```

Paste the output into a Markdown page inside a `mermaid` code fence. It renders as a diagram on the course site and in many editors.

The script is a consistency tool, not a security oracle. It cannot tell you whether `TB8` is a real boundary or whether `REG --> INF` should cross one. It only keeps the picture and the IDs in sync.

## MITRE ATLAS

MITRE ATLAS is a catalog of adversary tactics and techniques against AI systems. It is maintained like ATT&CK: techniques have stable IDs, descriptions, and case studies. It is useful for three things:

1. **Naming behavior precisely.** "Evade the model" becomes a technique with a known procedure.
2. **Finding adjacent threats.** A technique page shows what an adversary does before and after.
3. **Communicating with security teams.** ATLAS IDs are a shared language across red teams and defenders.

ATLAS is **not** a checklist. A system that maps to twenty techniques is not twenty times less secure. A technique matters only if an actor can reach the surface it needs.

### Verified technique IDs used in this course

Only the following IDs are used in examples and in LAB-02. They were checked against the ATLAS site on 2026-10-28. Do not invent IDs; an empty mapping is better than a fabricated one.

| ID | Technique | Fits a threat when |
|---|---|---|
| `AML.T0015` | Evade AI Model | An attacker crafts inputs to change a prediction at inference |
| `AML.T0043` | Craft Adversarial Data | The threat includes producing adversarial inputs or examples |
| `AML.T0020` | Training Data Poisoning | The attacker can influence training data or labels |
| `AML.T0018` | Manipulate AI Model | The attacker can alter the model artifact or its behavior |
| `AML.T0040` | AI Model Inference API Access | The path begins with access to a prediction API |
| `AML.T0024` | Exfiltration via AI Inference API | The attacker uses the inference API to extract information |
| `AML.T0051` | LLM Prompt Injection | A language model consumes untrusted instructions |

### Mapping MediScan threats

| Threat | ATLAS mapping | Reason |
|---|---|---|
| T1 Adversarial image downgrades a finding | `AML.T0015`, `AML.T0043` | Crafted input changes an inference decision |
| T2 Insider flips override labels | `AML.T0020` | Training labels are poisoned |
| T3 Compromised vendor update | `AML.T0018` | The model artifact is manipulated |
| T4 Model extraction via API | `AML.T0040`, `AML.T0024` | API access enables extraction |
| T5 Membership inference | none in the allowlist | ATLAS has adjacent privacy techniques, but none of the verified IDs above fit precisely |
| T9 Credential stuffing | none | This is a conventional credential attack, not an ML-specific technique |
| T10 Log tampering | none | ATLAS focuses on AI attack behavior; log tampering is covered by general security controls |

Two empty mappings in a seven-row table are normal. A threat does not become more real because it has an ATLAS ID, and a conventional attack does not become an ML attack because the system contains a model.

## ATLAS and NIST are different instruments

| Question | NIST AI 100-2e2025 | MITRE ATLAS |
|---|---|---|
| What is it for? | Classifying attacks by goals, knowledge, and capability | Cataloging adversary tactics and techniques |
| Unit of analysis | Attack class and attacker profile | Technique and procedure |
| Best use | Framing a threat and checking coverage | Naming behavior and finding adjacent techniques |
| Failure mode | Abstract categories with no operational detail | Technique list with no adversary or asset |
| In a threat model | The `nist_goal` and `attack_class` fields | The `atlas` field |

Use both: NIST tells you whether the register is balanced; ATLAS tells a defender what behavior to look for.

## Common mistakes and troubleshooting

| Mistake | Symptom | Fix |
|---|---|---|
| One stage dominates | Every threat is "serving" | Walk the lifecycle table and add a threat per stage |
| DFD is a network diagram | Only hosts and subnets appear | Add processes, stores, and data flows |
| Boundary with no flow | The diagram has a line but no crossing | Remove it or add the flow it protects |
| Mapping every threat to ATLAS | The register looks thorough but generic | Leave empty when no verified technique fits |
| Technique-first enumeration | The threat list is a copy of the ATLAS catalog | Start from a surface and an actor |
| IDs drift between diagram and register | `TB3` in the picture is `TB4` in the YAML | Generate both from one source or check them together |

## Check yourself

| Question | Answer |
|---|---|
| Which lifecycle stage does label flipping belong to? | Training, usually with a data-collection path; record the stage where the change occurs. |
| Why is a DFD better than a network diagram? | It shows processes, stores, and data transformations, not only hosts. |
| Is an empty ATLAS list a weakness? | No. It is honest when no verified technique fits. |
| What is the difference between ATLAS and NIST AI 100-2? | ATLAS catalogs techniques; NIST classifies attacks by goals, knowledge, and capability. |
| Why label every flow? | An unlabeled flow hides what data moves and which controls apply. |

## Summary and key takeaways

- The ML lifecycle is an attack-surface map: data collection, training, artifact, serving, monitoring, and people.
- A DFD has entities, processes, stores, flows, and trust boundaries; every flow and boundary must earn its place.
- Generate diagrams from a data structure so IDs stay consistent with the register.
- ATLAS names behavior; it is an index, not a checklist.
- Use only verified technique IDs; an empty mapping is better than an invented one.
- NIST and ATLAS answer different questions; use both.

## Next step

[Lesson 03.4 — Risk frameworks and crosswalks](lesson-4-frameworks-and-crosswalks.md) connects the register to the NIST AI RMF and the OWASP lists, and shows where the frameworks disagree.
