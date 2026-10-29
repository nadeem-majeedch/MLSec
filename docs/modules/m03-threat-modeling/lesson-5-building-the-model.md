# Lesson 03.5 — Building, Scoring, and Communicating the Model

<a id="m03-l5"></a>

**1.5 hours · Lesson 5 of 5 · Module 03**

## What this lesson answers

How do you turn a pile of notes into a threat model someone can act on? This lesson covers the build sequence, scoring with stated anchors, attack trees, controls, detection hypotheses, residual risk, rejection, and the one-page brief that decides what happens next.

## The build sequence

Work in this order. Skipping a step produces a document that looks complete but cannot be defended.

| Step | Output | Test of done |
|---:|---|---|
| 1 | Scope and system description | A reader can say what is in and out of scope |
| 2 | Data-flow diagram | Every flow has a direction; every boundary has a crossing |
| 3 | Asset inventory | Data, model, pipeline, infrastructure, credentials, records |
| 4 | Attack surfaces | Each has a boundary, entry point, and reachable actor |
| 5 | Adversary profiles | Actor, goal, knowledge, capability, assumptions, impact |
| 6 | Threat register | One row per threat, with lifecycle stage and NIST goal |
| 7 | Scoring | Impact, likelihood, severity, and a tie-break rule |
| 8 | Controls | Preventive, detective, corrective, specific enough to implement |
| 9 | Detection hypotheses | Metric, baseline, threshold, window, owner, response |
| 10 | Residual risk | A rating and an owner who accepts it |
| 11 | Attack trees | Three paths with the cheapest branch identified |
| 12 | Rejection | At least one threat rejected with a reopening condition |
| 13 | Crosswalk | AI RMF, OWASP, and recorded disagreements |
| 14 | Brief | One page for the decision-maker |

Steps 2–5 are the model. Steps 6–13 are the argument. Step 14 is how the argument travels.

## Scoring with anchors

A 1–5 scale without anchors is a mood. Write down what each number means in this system.

### Impact anchors

| Score | Label | MediScan anchor |
|---:|---|---|
| 1 | Negligible | No clinical effect; internal inconvenience |
| 2 | Minor | Recoverable operational delay; no patient harm |
| 3 | Moderate | Service degraded for a shift; reportable internal incident |
| 4 | Major | Delayed care, privacy exposure, or regulatory review |
| 5 | Severe | Serious patient harm, multi-patient impact, or loss of the service |

### Likelihood anchors

| Score | Label | Anchor |
|---:|---|---|
| 1 | Rare | Requires access or knowledge the actor is not assumed to have |
| 2 | Unlikely | Possible in theory; no evidence of capability or intent |
| 3 | Possible | Known capability; some access; motivated actor |
| 4 | Likely | Accessible surface; low cost; observed in comparable systems |
| 5 | Almost certain | Observed in this system or trivial to attempt |

### Bands and tie-breaks

`severity = impact × likelihood`:

| Score | Band |
|---:|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

Ties are common. State the tie-break rule **before** ranking, or the ranking becomes a preference. A clinical system might use: patient safety first, then privacy, then availability, then financial and reputational harm. A different system would use a different order.

## Attack trees and kill chains

An attack tree starts from an adversary goal and decomposes it into steps. Each step is a sub-goal; steps can be joined by AND (all required) or OR (any path). The tree is useful when it shows the **cheapest path** and the **cut set** — the smallest set of controls that breaks the most paths.

A kill chain is a linear version: reconnaissance, access, execution, persistence, action. It is easier to communicate but hides alternative paths. Use a tree to reason, a chain to brief.

For each tree:

- Name the root goal in adversary terms.
- Put the threat ID on every step.
- Mark AND/OR where it changes the analysis.
- Identify the cheapest branch and the control that cuts it.
- Note what evidence each step would leave.

## Controls that can be implemented

A control passes the specificity test if it answers four questions:

1. **Who** operates it? A role, not "the team."
2. **What mechanism** enforces it? A signature check, a quota, a second approval.
3. **What evidence** does it produce? A log line, a ticket, a metric.
4. **What happens when it fails?** Fail closed, alert, or degrade safely.

"We will use security best practices" fails all four. "The registry rejects any artifact without two signatures; the rejection is logged with the artifact hash and paged to the release owner" passes.

### Preventive, detective, corrective

| Type | Purpose | Example |
|---|---|---|
| Preventive | Stop the event | Two signatures before promotion |
| Detective | Notice the event | Canary trigger scan on every artifact |
| Corrective | Reduce the harm after | Revoke the artifact and roll back |

A high-severity threat with only preventive controls is one failure away from silent compromise. That is why the lab requires at least one detective control for high and critical threats.

## Detection hypotheses

A detection hypothesis is not "monitor for poisoning." It is a measurable statement:

> If a single source contributes more than 10% of a training batch, or more than 100 near-duplicate images in a day, alert the data-quality owner and quarantine the batch.

The template:

| Part | Question | Example |
|---|---|---|
| Metric | What is measured? | Share of a training batch from one source |
| Baseline | Compared with what? | The trailing 30-day median per source |
| Threshold | When does it fire? | Above 10% or above 100 near-duplicates |
| Window | Over what period? | Per batch and per day |
| Owner | Who responds? | Data-quality lead |
| Response | What happens? | Quarantine, review, retrain from a trusted snapshot |

If you cannot fill the table, you do not have a detection; you have a hope.

## Residual risk and acceptance

Residual risk is what remains after controls, under the same anchors. It is a judgment, not a subtraction. A control that reduces likelihood from 4 to 3 and impact from 5 to 4 changes the score from 20 to 12; state that reasoning if you use it.

A residual rating needs an owner and a review date. "Medium" with no owner is not a decision. In a clinical system, the owner of a patient-safety residual might be the chief medical information officer. In a bank, it might be the model risk committee.

## Rejection is a deliverable

A threat model that accepts everything is not prioritizing. Reject at least one threat explicitly:

- **Why is it rejected?** The path requires access the actor is not assumed to have, or a control already breaks it.
- **What would reopen it?** The assumption fails, a control is removed, or the system changes.
- **How would you still notice?** A cheap detection that remains even if the threat is out of scope.

Example: "Physical theft of a decommissioned workstation is rejected because full-disk encryption, no local image cache, and logged destruction make the path implausible. Reopen if a cache is introduced or encryption is removed. Detection: a disposal record without a destruction certificate within 30 days."

## The one-page brief

Decision-makers do not read the register. Give them one page:

| Section | Content |
|---|---|
| What we protect | Two or three assets and the harm that matters |
| Top five risks | ID, one-line threat, score, residual, owner |
| What we are doing | The controls already funded or committed |
| What we are accepting | Residual risks with owners and review dates |
| What we need decided | Budget, staffing, risk acceptance, or scope change |
| Evidence and limits | What was modeled, what was not, and the assumptions that would change the answer |

Write for three audiences in one document:

- **Engineers** need the surface, the mechanism, and the test.
- **Executives** need the harm, the decision, and the cost.
- **Auditors and regulators** need the scope, the assumptions, the framework mapping, and the evidence.

Avoid fear language. "Critical" is a score, not an argument. If a risk is critical, say what decision you need and what happens if it is not made.

## Worked example: score, rank, and check the control rule

```python
THREATS = [
    {"id": "T1", "impact": 5, "likelihood": 4, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T2", "impact": 5, "likelihood": 3, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T3", "impact": 5, "likelihood": 3, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T4", "impact": 4, "likelihood": 3, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T5", "impact": 4, "likelihood": 3, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T6", "impact": 5, "likelihood": 2, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T7", "impact": 5, "likelihood": 2, "preventive": 1, "detective": 2, "residual": "medium"},
    {"id": "T8", "impact": 4, "likelihood": 3, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T9", "impact": 4, "likelihood": 3, "preventive": 3, "detective": 2, "residual": "medium"},
    {"id": "T10", "impact": 3, "likelihood": 2, "preventive": 3, "detective": 2, "residual": "low"},
    {"id": "T12", "impact": 4, "likelihood": 2, "preventive": 3, "detective": 2, "residual": "low"},
]


def band(score):
    if score <= 4:
        return "low"
    if score <= 9:
        return "medium"
    if score <= 16:
        return "high"
    return "critical"


def issues(threat):
    score = threat["impact"] * threat["likelihood"]
    found = []
    if band(score) in {"high", "critical"}:
        if threat["preventive"] < 2:
            found.append("needs >=2 preventive controls")
        if threat["detective"] < 1:
            found.append("needs a detective control")
        if threat["residual"] == "high":
            found.append("high residual risk needs acceptance")
    return found


ranked = sorted(THREATS, key=lambda t: t["impact"] * t["likelihood"], reverse=True)
print(f"{'id':4s} {'score':>5s}  {'band':8s} {'residual':8s} issues")
for threat in ranked:
    score = threat["impact"] * threat["likelihood"]
    found = issues(threat) or ["-"]
    print(f"{threat['id']:4s} {score:5d}  {band(score):8s} {threat['residual']:8s} {'; '.join(found)}")

print("\nTop 5:")
for threat in ranked[:5]:
    print(f"  {threat['id']} score={threat['impact'] * threat['likelihood']}")
```

Expected output:

```text
id   score band     residual issues
T1      20 critical medium   -
T2      15 high     medium   -
T3      15 high     medium   -
T4      12 high     medium   -
T5      12 high     medium   -
T8      12 high     medium   -
T9      12 high     medium   -
T6      10 high     medium   -
T7      10 high     medium   needs >=2 preventive controls
T12      8 medium   low      -
T10      6 medium   low      -

Top 5:
  T1 score=20
  T2 score=15
  T3 score=15
  T4 score=12
  T5 score=12
```

Two lessons from the output:

- **T7 has only one preventive control.** The rule catches it, even though its score is high. Add a control or document an acceptance.
- **The top five cuts off at a tie.** T4, T5, T8, and T9 all score 12. The code preserves input order, but a human must choose the tie-break. In a clinical system, T5 (privacy of diagnosis) and T9 (priority tampering) may outrank T4 (IP) and T8 (export overreach).

The script is a consistency check. It does not know whether the scores are right.

## Communicating a rejection

Rejections are often challenged. Write them so a reader can see what would change your mind:

> **Rejected: physical theft of a decommissioned workstation.** The path assumes an unencrypted disk or a local image cache. Both are prohibited by the current build, and disposal requires a destruction certificate. Reopen if a cache is introduced, encryption is removed, or a disposal certificate is missing. The detection remains: a missing certificate within 30 days.

This is stronger than "low risk, accepted" because it names the assumption and the trigger.

## Common mistakes and troubleshooting

| Mistake | Symptom | Fix |
|---|---|---|
| Scoring before writing the threat | The score has no actor or impact statement | Write actor, capability, and impact first |
| No anchors | One reviewer says 3, another says 5 | Publish the anchors and use them |
| Ties broken silently | The top five looks arbitrary | State the tie-break rule before ranking |
| Controls without mechanism | "We will harden the API" | Name who, what, evidence, and failure mode |
| Detection without a baseline | Alert fires constantly or never | Add baseline, threshold, and window |
| Residual risk with no owner | "Medium" forever | Name an owner and a review date |
| No rejection | Every threat is accepted | Reject one with a reopening condition |
| Brief is a register dump | Decision-maker asks "what do you want?" | One page with a decision request |

## Check yourself

| Question | Answer |
|---|---|
| Why publish impact and likelihood anchors? | They make scores comparable and auditable across reviewers. |
| What is a cut set? | The smallest set of controls that breaks the most attack paths. |
| What four questions does a specific control answer? | Who operates it, what mechanism, what evidence, what happens on failure. |
| What six parts does a detection hypothesis need? | Metric, baseline, threshold, window, owner, response. |
| Why reject a threat explicitly? | It shows prioritization and names the assumption that would reopen it. |
| What belongs in the one-page brief? | Assets, top risks, current controls, accepted risks, decisions needed, and limits. |

## Summary and key takeaways

- Build in order: scope, diagram, assets, surfaces, adversaries, threats, scores, controls, detection, residual, trees, rejection, crosswalk, brief.
- Publish scoring anchors and a tie-break rule; otherwise the ranking is a mood.
- Attack trees show the cheapest path and the cut set; kill chains are for briefing.
- A control is specific when it names who, what, evidence, and failure behavior.
- A detection hypothesis has a metric, baseline, threshold, window, owner, and response.
- Residual risk needs an owner and a review date.
- Rejection is a deliverable with a reopening condition.
- The one-page brief is the decision document; the register is the evidence.

## Next step

You now have the method. [LAB-02](../../labs/lab-02.md) asks you to apply it to the MediScan Triage Assistant and produce a machine-checkable threat model. Take the [knowledge check](quiz.md) first if you want a fast read on what to review.
