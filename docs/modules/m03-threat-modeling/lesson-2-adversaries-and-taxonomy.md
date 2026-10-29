# Lesson 03.2 — Adversaries and the NIST Taxonomy

<a id="m03-l2"></a>

**1 hour · Lesson 2 of 5 · Module 03**

## What this lesson answers

Who would attack this system, what do they know, what can they do, and what do they gain? A threat without an adversary is a rumor. This lesson turns the system model from Lesson 1 into an adversary model using the vocabulary of NIST AI 100-2e2025.

## An adversary is a profile, not a label

"The attacker" is not a useful entry. A useful profile has six fields:

| Field | Question | Example |
|---|---|---|
| **Actor** | Who is it? | A credentialed radiology informatics employee |
| **Goal** | What outcome do they want? | Suppress a finding in future models |
| **Knowledge** | What do they know about the system? | White-box knowledge of the label schema, black-box on model weights |
| **Capability** | What can they do, with what budget? | Edit labels, no direct registry access, weeks of access |
| **Assumptions** | What must be true for the path to work? | Overrides enter retraining without a second approver |
| **Impact** | What harm follows if it succeeds? | Delayed care, regulatory review, loss of trust |

Two profiles can share a goal and differ completely in risk. A curious user who can query a public API cannot flip labels. An insider who can flip labels may not be able to publish a model. The threat model must keep them separate.

## The NIST AI 100-2e2025 taxonomy

NIST's adversarial-ML taxonomy organizes attacks by **goals**, **knowledge**, and **capabilities**, then describes attack classes and mitigations. You do not need to memorize the document. You need to use its distinctions consistently.

### Four goals

| Goal | What the attacker wants | Examples in ML |
|---|---|---|
| **Integrity** | Make the system behave incorrectly in a way the attacker chooses | Evasion, poisoning, backdoor |
| **Availability** | Make the system unusable or degraded | Training-data poisoning at scale, flooding the inference API, ransomware |
| **Privacy** | Learn or reveal something about people or training data | Membership inference, model inversion, attribute inference, data exfiltration |
| **Abuse** | Use the system's functionality for a purpose its owner did not intend | Generating harmful content, phishing assistance, model extraction or resale |

Model extraction sits awkwardly. NIST treats it as abuse of functionality; many organizations also record it as intellectual-property loss. Record the NIST goal and add a taxonomy note rather than pretending one label covers both. This is the kind of disagreement a good threat model surfaces.

### Three knowledge levels

| Knowledge | What the attacker has | Typical consequence |
|---|---|---|
| **White-box** | Architecture, weights, gradients, preprocessing | Stronger, cheaper attacks; can optimize directly |
| **Black-box** | Inputs and outputs only | Query-based attacks; cost measured in queries |
| **Partial** | Some artifacts, documentation, or insider knowledge | Mixed strategies; often the most realistic |

Knowledge is not binary. An attacker may know the model family and the preprocessing but not the weights. Write down which part is known.

### Capabilities and budgets

Capability is what the attacker can *do*, not what they *know*:

- Control training data, labels, or the collection process.
- Query the model, with a rate and a budget.
- Read or write model artifacts.
- Execute code in a dependency, container, or CI job.
- Access credentials, logs, or a support console.
- Act physically or socially.

Always attach a budget: queries per day, dollars, wall-clock time, or number of accounts. "Can query the API" without a budget cannot be compared with a defense.

### Attack classes you will meet

| Class | Goal | When it happens | One-line description |
|---|---|---|---|
| Evasion | Integrity | Inference | Craft an input that is misclassified |
| Poisoning | Integrity or availability | Training | Change the data distribution or labels |
| Backdoor | Integrity | Training or artifact | Implant a trigger that causes a chosen behavior |
| Extraction | Abuse / IP | Inference | Clone model functionality through queries |
| Membership inference | Privacy | Inference | Decide whether a record was in training |
| Model inversion | Privacy | Inference | Reconstruct a representative input |
| Attribute inference | Privacy | Inference | Infer a sensitive attribute from outputs |
| Denial of service | Availability | Training or inference | Exhaust resources or corrupt service |
| Data exfiltration | Privacy | Any stage | Move data out through a dependency, export, or API |

A threat register that contains only evasion is unbalanced. The NIST goals are a quick check: if one goal is missing, ask whether it is truly irrelevant or merely unmodeled.

## Predictive and generative systems

The same four goals apply to generative systems, but the surfaces multiply:

| Predictive system | Generative system | New question |
|---|---|---|
| Fixed input schema | Free-text prompt | Who controls the instruction? |
| Model weights are the main artifact | Weights, prompt templates, retrieval corpus, tools | Which component carries the trust? |
| Output is a label or score | Output is text, code, or an action | What happens downstream of the output? |
| Query access is the main oracle | Query access plus context injection | Can retrieved content carry an instruction? |

A generative system is not automatically riskier. It has more places where an untrusted party can supply content, and more places where the output can cause an action. The taxonomy still asks: goal, knowledge, capability, impact.

## Impact is multi-dimensional

Score impact on the dimensions that matter to the owner, not only on model accuracy:

| Dimension | Question | Example |
|---|---|---|
| **Safety** | Can someone be harmed physically? | A missed urgent finding |
| **Privacy** | Can a person be identified or have an attribute revealed? | Membership inference on a diagnosis |
| **Financial** | What does it cost? | Fraud, fines, incident response |
| **Legal and regulatory** | What obligations are triggered? | Health-data breach notification |
| **Mission** | Does the service stop? | Triage offline during an outage |
| **Trust** | Will users keep using it? | Clinicians override every score after a scare |

A single number hides these differences. Record the dimension and the sentence behind the score.

## Worked example: the same threats, three profiles

The following scores are **illustrative judgments**, not measurements. The point is that the ranking changes when the adversary changes, even when impact stays fixed.

```python
IMPACT = {
    "evasion": 5,
    "label poisoning": 4,
    "backdoor": 5,
    "model extraction": 3,
    "outage": 4,
}

LIKELIHOOD = {
    "curious user": {"evasion": 3, "label poisoning": 1, "backdoor": 1, "model extraction": 3, "outage": 1},
    "credentialed insider": {"evasion": 2, "label poisoning": 4, "backdoor": 2, "model extraction": 2, "outage": 1},
    "supply-chain attacker": {"evasion": 3, "label poisoning": 3, "backdoor": 5, "model extraction": 2, "outage": 2},
}

for profile, scores in LIKELIHOOD.items():
    ranked = sorted(
        ((threat, IMPACT[threat] * score) for threat, score in scores.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    top = ranked[0]
    print(f"{profile:22s} top={top[0]:16s} score={top[1]}")
    print("  " + ", ".join(f"{name}={score}" for name, score in ranked))
```

Expected output:

```text
curious user           top=evasion          score=15
  evasion=15, model extraction=9, backdoor=5, label poisoning=4, outage=4
credentialed insider   top=label poisoning  score=16
  label poisoning=16, evasion=10, backdoor=10, model extraction=6, outage=4
supply-chain attacker  top=backdoor         score=25
  backdoor=25, evasion=15, label poisoning=12, outage=8, model extraction=6
```

The highest-impact threat is evasion and backdoor at 5. The top risk is not the same for every actor:

- A curious user is most likely to try evasion, because queries are cheap.
- An insider is most likely to poison labels, because that is the authority they hold.
- A supply-chain attacker is most likely to insert a backdoor, because they control the build.

If your register has one likelihood per threat, you have implicitly assumed one attacker. Name the profile, or produce one row per profile.

## Assumptions are part of the threat

An assumption is a statement that must hold for the threat to be feasible. Write it down, because it is where the model is most likely to be wrong.

Examples:

- "The API returns full probability vectors." If it returns only a label, extraction becomes harder.
- "Overrides enter retraining without a second approver." If dual approval exists, the insider path is weaker.
- "The container has outbound internet access." If egress is denied, exfiltration is harder.
- "The attacker has no physical access to the data center." If they do, the model changes.

A threat model that does not state assumptions cannot be audited. A reviewer cannot tell whether a disagreement is about the facts or about the reasoning.

## Common mistakes and troubleshooting

| Mistake | Symptom | Fix |
|---|---|---|
| One unnamed "attacker" | Every threat has the same likelihood | Write one profile per actor |
| Treating black-box as powerless | Evasion and extraction are dismissed | Black-box attackers can query repeatedly; attach a budget |
| Ignoring abuse and IP | The register covers only safety | Add extraction, resale, and misuse paths |
| Impact scored only as accuracy loss | A patient-safety threat looks minor | Score safety, privacy, financial, legal, mission, and trust |
| Assumptions left implicit | Reviewer cannot reproduce the judgment | List the conditions that make the path feasible |
| Forgetting availability | Only integrity threats appear | Ask what happens if the service is down for a shift |
| Taxonomy label forced | Extraction is called "privacy" or "integrity" | Use the closest NIST goal and add a note |

## Check yourself

| Question | Answer |
|---|---|
| What are the four NIST attack goals? | Integrity, availability, privacy, abuse. |
| Is black-box access the same as no access? | No. The attacker can query and observe; the cost is measured in queries. |
| Why does the same threat get different scores for different actors? | Likelihood depends on the actor's knowledge, capability, and authority. |
| Where does model extraction fit? | NIST treats it as abuse of functionality; many organizations also track IP loss. Record the note. |
| Why write assumptions? | They define when the threat is feasible and make disagreements auditable. |

## Summary and key takeaways

- An adversary profile has actor, goal, knowledge, capability, assumptions, and impact.
- NIST AI 100-2e2025 organizes attacks by goals, knowledge, and capabilities, then by attack class.
- The four goals are integrity, availability, privacy, and abuse; a balanced register covers all four.
- Knowledge is white-box, black-box, or partial; capability always carries a budget.
- Impact is multi-dimensional: safety, privacy, financial, legal, mission, and trust.
- The ranking changes when the adversary changes; one likelihood per threat hides that.
- Assumptions are part of the threat, not a disclaimer at the end.

## Next step

[Lesson 03.3 — Attack surfaces, lifecycle, and ATLAS](lesson-3-surfaces-lifecycle-atlas.md) places each threat on a lifecycle stage, draws the data-flow diagram, and maps techniques to MITRE ATLAS.
