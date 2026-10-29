# Lesson 03.1 — Security Fundamentals for ML Systems

<a id="m03-l1"></a>

**1 hour · Lesson 1 of 5 · Module 03**

## What this lesson answers

What are we protecting, and where does trust change? Before you can say whether an attack matters, you need a model of the system that is independent of any particular attack technique. This lesson builds that model with five elements: assets, trust boundaries, attack surfaces, controls, and risk owners.

## Security is about harm, not algorithms

A vulnerability is a weakness. A threat is an adversary who can use it. A risk is the chance and size of the harm. These are different claims:

- "The model is sensitive to small input changes" is a **property**.
- "A remote attacker can change a triage score" is a **threat**.
- "A delayed pneumothorax can harm a patient" is an **impact**.
- "The queue is reordered for 3% of studies, with medium residual risk" is a **risk statement**.

Security work connects the four. Without the connection, a list of model properties is not a security assessment.

## The four things that can be harmed

The classic trio is confidentiality, integrity, and availability. ML systems add privacy as a first-class concern because model behavior can reveal the people in the training data.

| Property | Question | ML example | Failure |
|---|---|---|---|
| **Confidentiality** | Who can see it? | Patient images, model weights, credentials | Images leak from an export bucket |
| **Integrity** | Can you trust it? | Labels, weights, predictions, audit logs | An override is silently changed |
| **Availability** | Is it there when needed? | Inference API, worklist integration | Ransomware stops triage for a shift |
| **Privacy** | What does behavior reveal about people? | Membership in training data, reconstructed inputs | A patient's diagnosis is inferred from a score |

Privacy is not a synonym for confidentiality. Confidentiality protects the data store; privacy protects the person from inferences made about them, even when the data store is never directly read.

## Assets

An asset is anything of value that can be harmed. The model is only one asset. A useful inventory for an ML system covers six categories:

| Category | Examples | Why attackers want it |
|---|---|---|
| **Data** | Training data, labels, patient records, prompts, retrieved documents | Steal it, poison it, or learn from it |
| **Model** | Weights, architecture, preprocessing parameters, tokenizer | Copy it, tamper with it, or extract behavior |
| **Code and pipeline** | Training scripts, container images, CI/CD, dependencies | Execute code, insert a backdoor, persist |
| **Infrastructure** | Inference API, registry, storage, GPUs | Disrupt service or move laterally |
| **Credentials** | API keys, signing keys, admin sessions | Impersonate a trusted party |
| **Records and trust** | Audit logs, override history, clinician confidence, reputation | Hide activity or destroy accountability |

For each asset, record three things: what it is, why it matters, and which of confidentiality, integrity, availability, and privacy it needs. "High sensitivity" without a reason is not an inventory; it is a label.

## Trust boundaries

A trust boundary is a line where data or authority crosses between parties with different privilege, assumptions, or ownership. A boundary is not a network diagram line. It is a change in *who can say yes*.

Common boundaries in ML systems:

- A hospital network to a cloud ingestion endpoint.
- A vendor's build system to your model registry.
- A training environment to a production inference service.
- An analytics export to an external research partner.
- A support administrator to a production console.
- A user's browser to an LLM application that holds tool credentials.

Two tests help you find boundaries:

1. **Privilege test.** Does one side have authority the other side does not? If yes, there is a boundary.
2. **Assumption test.** Does one side trust a claim (identity, label, signature, file format) that the other side produces? If yes, there is a boundary.

### Worked example: find the unlabelled crossings

The following data-flow list describes a simplified MediScan. Each flow may carry a boundary label. The code flags flows that cross a zone without a label — a common modeling bug.

```python
FLOWS = [
    {"src": "acquisition device", "dst": "ingestion API", "boundary": "TB1"},
    {"src": "ingestion API", "dst": "image store", "boundary": None},
    {"src": "image store", "dst": "training job", "boundary": "TB2"},
    {"src": "vendor build", "dst": "model registry", "boundary": "TB3"},
    {"src": "model registry", "dst": "inference API", "boundary": None},
    {"src": "inference API", "dst": "clinician worklist", "boundary": "TB4"},
    {"src": "image store", "dst": "export job", "boundary": None},
    {"src": "export job", "dst": "research partner", "boundary": "TB5"},
    {"src": "support admin", "dst": "model registry", "boundary": "TB6"},
]

ZONE = {
    "acquisition device": "hospital",
    "clinician worklist": "hospital",
    "ingestion API": "ingest",
    "image store": "ingest",
    "training job": "train",
    "vendor build": "vendor",
    "model registry": "deploy",
    "inference API": "serve",
    "export job": "analytics",
    "research partner": "partner",
    "support admin": "admin",
}


def boundary_counts(flows):
    counts = {}
    for flow in flows:
        if flow["boundary"]:
            counts[flow["boundary"]] = counts.get(flow["boundary"], 0) + 1
    return counts


def unlabelled_crossings(flows, zones):
    found = []
    for flow in flows:
        if flow["boundary"] is None and zones[flow["src"]] != zones[flow["dst"]]:
            found.append((flow["src"], zones[flow["src"]], flow["dst"], zones[flow["dst"]]))
    return found


print("boundary crossings:", dict(sorted(boundary_counts(FLOWS).items())))
found = unlabelled_crossings(FLOWS, ZONE)
print("unlabelled zone crossings:", len(found))
for src, src_zone, dst, dst_zone in found:
    print(f"  {src} ({src_zone}) -> {dst} ({dst_zone})")
```

Expected output:

```text
boundary crossings: {'TB1': 1, 'TB2': 1, 'TB3': 1, 'TB4': 1, 'TB5': 1, 'TB6': 1}
unlabelled zone crossings: 2
  model registry (deploy) -> inference API (serve)
  image store (ingest) -> export job (analytics)
```

Both findings are real. The registry hands an artifact to inference across a deployment boundary, and the image store sends data to an analytics job that later leaves the network. Neither flow had a label, so a reader would not know what controls apply.

Add `TB7` for the export path and `TB8` for deployment, and the second run reports `0`. The code did not find a vulnerability; it found a **modeling gap**. That distinction matters: the output is a question for a human, not a proof of insecurity.

## Attack surfaces

An attack surface is a point where an adversary can interact with the system. A surface is not automatically a vulnerability. It is an opportunity that must be paired with an actor, a capability, and a goal.

| Lifecycle stage | Typical surfaces | Example question |
|---|---|---|
| Data collection | Upload API, sensor, label store, scraping pipeline | Who can add or relabel a record? |
| Training | Training job, hyperparameter store, dependency lockfile | Who can change the objective or the data snapshot? |
| Artifact | Model registry, serialization format, signing key | Who can publish an artifact? |
| Serving | Prediction API, worklist UI, query quota | Who can query, and what do they get back? |
| Monitoring | Log store, alerting, retention policy | Who can delete or alter evidence? |
| People | Support console, shared accounts, vendor access | Who has standing privilege they do not need? |

A useful surface entry has five fields: ID, name, boundary, entry point, and who can reach it. "The API" is not an entry. "The JSON scoring endpoint on TB4, reachable by any authenticated worklist client" is.

## Five principles that change decisions

These are not slogans. Each one changes a design choice you will make in the lab.

| Principle | What it means for ML | Example |
|---|---|---|
| **Least privilege** | Give each component and person the minimum authority needed | The preprocessing container can read images but cannot write the label store |
| **Defense in depth** | Assume one control fails; add an independent one | Rate limits plus output rounding plus monitoring |
| **Secure defaults** | The safe choice is the default, not an option | New endpoints require authentication; exports are denied unless approved |
| **Separation of duties** | No single person can both cause and hide an action | Label changes need a second approver; log admins cannot approve labels |
| **Fail safe** | When a control fails, the system does not silently become permissive | If the model registry signature check fails, deployment stops |

"Defense in depth" is often misused to mean "add more tools." It means the controls fail independently. Two filters that both miss the same encoding are one control, not two.

## Risk owners

Every accepted risk needs an owner who can accept it. A threat model that says "the team should fix this" has no owner. In a clinical system, the owner might be the chief medical information officer for patient-safety risks and the CISO for data-exposure risks. The owner matters because residual risk is a decision, not a measurement.

## Common mistakes and troubleshooting

| Mistake | Why it happens | Fix |
|---|---|---|
| Listing only the model as an asset | The model is the visible artifact | Add data, labels, credentials, availability, and audit records |
| Drawing boundaries around teams, not privilege | Org charts are easy to find | Ask who can say yes on each side |
| Calling every endpoint "vulnerable" | Surface and vulnerability are conflated | Pair each surface with an actor and a goal first |
| Treating privacy as confidentiality | Both are "data protection" | Ask what behavior reveals, not only who can read the store |
| Adding controls before threats | Tools are familiar; threats are hard | Write the threat and the harm first |
| No owner for residual risk | The model is treated as a technical document | Name a role that can accept the risk |

## Check yourself

| Question | Answer |
|---|---|
| Is a model weight an asset? | Yes: confidentiality (IP), integrity (tampering), and availability (service) all apply. |
| Is a trust boundary the same as a firewall? | No. A firewall may implement a boundary, but the boundary is the change in privilege or trust. |
| Is every attack surface a vulnerability? | No. A surface is reachable; a vulnerability is a weakness that a threat can use. |
| Why is privacy separate from confidentiality? | A model can reveal membership or attributes without anyone reading the raw data. |
| What makes a control "defense in depth"? | It fails independently of the other controls, so one bypass does not defeat the set. |

## Summary and key takeaways

- Security connects a property, a threat, an impact, and a risk statement.
- Assets include data, model, code, infrastructure, credentials, and records — not just weights.
- Trust boundaries are changes in privilege or trust, found with the privilege and assumption tests.
- Attack surfaces are reachable points; they become threats only with an actor and a goal.
- Least privilege, defense in depth, secure defaults, separation of duties, and fail-safe design are decision rules, not slogans.
- Every residual risk needs an owner.

## Next step

[Lesson 03.2 — Adversaries and the NIST taxonomy](lesson-2-adversaries-and-taxonomy.md) turns the system model into an adversary model: who acts, what they know, what they can do, and what they gain.
