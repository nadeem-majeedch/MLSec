# Lesson 17.4 — Purple-Team Synthesis and Adaptation

<a id="m17-l4"></a>

**Module 17 · Lesson 4 of 4 · 1 hour · LO-28, LO-29, LO-34**

## Scenario

The red team reports a quota bypass. The blue team reports that it detected quota abuse. Both are right about different tests: the red team bypassed the quota with a second key, and the blue team detected the first key's excess. Neither report mentions the other.

The exercise lead merges the two timelines and finds the gap: the second key was never linked to the first actor, so the detector saw two compliant keys. The finding is not "quota bypass" or "detection works." It is "detection keys on the credential, while the control is per actor, and the attacker can hold two credentials."

That finding exists only in the merge. Purple-team work is the merge.

## Objectives

By the end of this lesson you will be able to:

1. Merge red and blue evidence into one timeline with consistent clocks and correlation IDs.
2. Build a before/after matrix that shows what changed for each attack and each control.
3. Design and run an adaptive variant that tests whether a mitigation generalizes.
4. Evaluate mitigations on efficacy, benign cost, operational cost, and adaptivity.
5. Write a residual-risk statement that states what remains, under which adversary, and why.

## 1. Purple team is a review, not a third team

The purple team is the process that compares what the red team did with what the blue team saw and did, then decides what to change. It has four outputs.

| Output | Question | Artifact |
|---|---|---|
| Timeline | What happened, in what order, and what did each side see? | `timeline.md` |
| Gap analysis | Where did detection or response fail, and why? | `gaps.md` |
| Mitigation comparison | Did the control work, at what cost, against which variant? | `mitigations.md` |
| Residual risk | What remains after the controls, and for whom? | Section of `report.md` |

If the exercise ends with two separate reports and no merge, it has produced findings but not learning.

## 2. Timeline discipline

A timeline is only as good as its clocks.

### Use one time base

- Record UTC with milliseconds in every log.
- Record the session start in `run.json` and use it as time zero for relative times.
- If the host clock is unreliable, record both wall time and a monotonic counter, and note the drift.

### Correlate with request IDs

Every event carries `request_id`. The red team's client generates it (or reads it from the response header); the service logs it; the detector alert includes it. Without this, merging is guesswork.

### Minimum timeline columns

| Time (UTC) | Source | Event | Actor | Request ID | Detail |
|---|---|---|---|---|---|
| 09:14:03.221 | red | A-04 request 1 | key-12 | req-7f3a | status 200 |
| 09:14:03.402 | service | decision | key-12 | req-7f3a | block |
| 09:15:10.004 | blue | D-04 alert | key-12 | — | 2.4× quota |
| 09:22:41.117 | blue | containment | key-12 | — | key throttled |
| 09:23:02.550 | red | A-04 request 299 | key-12 | req-8c11 | status 429 |

### Merge, then read

Read the merged timeline three times:

1. **Red view:** did the attack proceed as planned? Where did it deviate?
2. **Blue view:** what was visible, when, and what was missed?
3. **Gap view:** what happened between an event and the response to it?

The gap view is where the findings are. A detection that fires 40 minutes late is a detection gap even though recall is 100%.

## 3. The before/after matrix

The central purple-team artifact is a table with one row per attack and columns for the state before and after mitigation.

| Attack | Before: outcome | Before: detected | Before: contained | After: outcome | After: detected | After: contained |
|---|---|---|---|---|---|---|
| A-01 no auth | 401 | D-01, 2 s | n/a | 401 | D-01, 2 s | n/a |
| A-02 tenant | cross-tenant decision | D-02, 0 s | 6 min | rejected | D-02, 0 s | 0 s |
| A-04 quota | 380 decisions | D-04, 66 s | 8 min | 100 decisions | D-04, 12 s | 2 min |
| A-05 evasion | segment 0.06 | not detected | — | segment 0.09 | D-05, 40 s | 5 min |
| A-06 extraction | agreement 0.93 | not detected | — | agreement 0.71 | D-06, 3 min | 4 min |

The numbers above are illustrative, not measured. In your report, every cell comes from a recorded run.

### What belongs in the matrix

- **Outcome:** did the attack achieve its objective? Use the attack's own oracle.
- **Detected:** rule ID and time to detect, or "not detected."
- **Contained:** time to contain, or "not contained," or "n/a" for attacks with no action.
- **Benign cost:** the false-positive rate or blocked benign requests introduced by the mitigation.
- **Version:** the control configuration tested. A matrix without versions is not reproducible.

## 4. The adaptive variant

A mitigation that blocks the scripted attack has blocked one script. The adaptive variant asks whether it blocks the class.

### Rules for a fair adaptive variant

1. **Same objective.** The variant pursues the same success criterion, not an easier one.
2. **Same budget class.** Requests, time, and perturbation stay within the exercise's stated budgets.
3. **One informed change.** The variant may use knowledge of the defense, but changes one dimension so the result is interpretable.
4. **Declared before running.** Write the variant and its oracle before you run it.
5. **Reported whether or not it works.** A variant that fails is evidence the control generalizes to that change.

### Dimensions to vary

| Dimension | Original | Variant | What it tests |
|---|---|---|---|
| Actor identity | one key | two keys linked by tenant | Whether detection keys on actor or credential |
| Timing | steady rate | slow ramp under the threshold | Whether the rule uses a window an attacker can pace |
| Payload | JSON body tenant | header or query tenant | Whether the check covers all input paths |
| Volume | 400 requests/min | 95 requests/min for 10 min | Whether quota is cumulative or per-minute |
| Feature search | single-feature steps | two-feature combinations | Whether the evasion control is per-feature |
| Query mix | random + boundary | boundary only, low diversity | Whether extraction detection depends on volume |
| Sequence | auth then admin | auth, benign action, admin | Whether sequence rules include the middle step |

### Worked variant

```text
VARIANT V-01 (after M-02: per-actor quota)
Original: A-04, one key, 400 requests in 60 s.
Observed: 100 decisions, then 429; D-04 alerted at 66 s.
Variant:  Two keys under tenant t-04, 60 requests/min each for 10 minutes.
Hypothesis: Per-key quota holds, but per-actor quota does not; total
            decisions exceed 100/min for the tenant.
Oracle: Tenant-level decisions > 100/min, or D-04 silent while total
        tenant volume exceeds 2× quota.
Budget: 1,200 requests, 10 minutes, 2 keys.
Result: [fill from run]
```

If the variant succeeds, the mitigation is per-credential, not per-actor. That is the finding, and it is more precise than either team's original report.

## 5. Evaluating a mitigation

A control is not "good" or "bad." It has a profile.

| Dimension | Question | Metric |
|---|---|---|
| Efficacy | Does it stop the tested attack? | Attack success before/after, at the same budget |
| Generalization | Does it stop the adaptive variant? | Variant success rate |
| Benign cost | Does it harm legitimate users? | False-positive rate, blocked benign requests |
| Performance cost | Does it slow the service? | p50/p95 latency, added CPU or memory |
| Operational cost | Who maintains it, and how often does it need tuning? | Analyst hours/week, change frequency |
| Bypass surface | What new path does it create? | Variant attempts, design review |
| Reversibility | Can it be rolled back quickly? | Rollback time, tested? |

### Compare at least two mitigations

A single mitigation evaluated alone tells you whether it works. Two mitigations evaluated on the same attacks tell you which to choose.

| Mitigation | Efficacy | Variant | Benign cost | Latency | Ops burden |
|---|---|---|---|---|---|
| M-01 strict schema validation | A-03 blocked | encoded variant blocked | 0.1% rejected | +2 ms | Low |
| M-02 per-actor quota | A-04 blocked | two-key variant **succeeds** | 0.0% | +1 ms | Medium |
| M-03 feature-delta monitor | A-05 detected | slower variant **missed** | 0.4% alerts | 0 | Medium |
| M-04 output score bucket only | A-06 agreement 0.71 | boundary-only variant 0.78 | 0.0% | 0 | Low |

The table is the deliverable. A recommendation that ignores benign cost or ops burden is not a security recommendation; it is a preference.

### Layering

Some controls are cheap and independent; combine them. Others overlap; choose one. The test is whether an attacker must defeat both.

- Validation + per-actor quota: independent; an attacker who passes validation still meets the quota.
- Two rate limiters at the same layer: redundant; the stricter one dominates.
- Detection + prevention: complementary; prevention blocks the common path, detection catches the variant.

## 6. The residual-risk statement

Residual risk is what remains after the controls, under a stated adversary and test set. Write it as a sentence with four parts.

```text
Under adversary RD-01 (API access, 2,000 requests, feature bounds),
after controls M-01, M-02, and M-04, attack A-05 still reduces the
target segment block rate to 0.09 at a global false-decline rate of
0.02, using a two-key, slow-ramp variant that stays under the
per-actor quota. Detection D-05 fires but containment takes 5 minutes,
during which roughly 60 decisions are affected. This residual risk is
accepted for the exercise; a production deployment would need a
tenant-level cumulative control and a faster containment path.
```

Four parts: adversary, controls, remaining effect with numbers, and the decision.

### What residual risk is not

- It is not "low" without a number and an adversary.
- It is not zero because the tested attack failed.
- It is not the same as the initial risk; it is the risk after specific controls.
- It is not permanent; it changes when the adversary, budget, or control changes.

## 7. The purple-team report

Use this structure for RT-01 and for any red/blue exercise in the capstone.

| Section | Content |
|---|---|
| 1. Scope and authorization | RoE summary; target; data; time; non-goals |
| 2. System and threat model | Architecture; assets; boundaries; adversary profiles |
| 3. Method | Attack plan summary; blue plan summary; separation protocol |
| 4. Baseline | Quiet traffic; evaluation set; hashes; seeds |
| 5. Red results | One row per attack: hypothesis, outcome, budget used |
| 6. Blue results | One row per detection: precision, recall, TTD, TTC |
| 7. Timeline | Merged, correlated, with the gap view |
| 8. Mitigations | Before/after matrix; at least two mitigations compared |
| 9. Adaptive variant | Declared variant, result, and what it shows |
| 10. Residual risk | The four-part statement |
| 11. Recommendations | Ordered by risk reduction per unit cost |
| 12. Limitations | Baseline size, missing telemetry, untested families |
| 13. Reproduction | Commands, seeds, manifest, environment |

Sections 5 and 6 stay separate. The merge happens in 7–10, where the reader can see both sides before the synthesis.

## 8. Worked example — mitigation comparison

```text
Exercise: RT-01, run 2026-10-28, seed 7, budget 1,980/2,000 requests.

| Attack | Before | After M-01+M-02+M-04 | Variant | Result |
| A-02   | cross-tenant decision | blocked at validation | header tenant | blocked |
| A-04   | 380 decisions | 100 decisions | two keys | 118 decisions (bypass) |
| A-05   | segment 0.06 | segment 0.09 | slow ramp | segment 0.08 |
| A-06   | agreement 0.93 | agreement 0.71 | boundary-only | agreement 0.78 |

Residual: A-05 remains feasible within bounds; A-04 bypasses per-key
quota with two keys; extraction is reduced but not prevented.
Recommendation order: tenant-level cumulative quota (A-04), feature-delta
detection with faster containment (A-05), output bucketing plus query
diversity limits (A-06).
```

The numbers are illustrative. The shape is the point: an attack that is blocked, an attack that is only detected, one that is reduced, and one that is bypassed. A report with four different outcomes is more credible than one where every control works.

## 9. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Two reports, no merge | No learning | Build the timeline and matrix |
| Different clocks | Events cannot be ordered | UTC + monotonic counter |
| No request IDs | Correlation is guesswork | Add and propagate IDs |
| Before/after without versions | Results not reproducible | Record control config per row |
| Variant weakens the objective | Control looks better than it is | Same objective, same budget class |
| Variant designed after seeing the result | Unfair test | Declare variant and oracle first |
| Ignoring benign cost | Control harms users | Measure FP and latency |
| One mitigation only | No trade-off analysis | Compare at least two |
| Residual risk without numbers | Unfalsifiable claim | Adversary + effect + decision |
| Recommendations unordered | Reader cannot prioritize | Rank by risk reduction per cost |

## 10. Check your understanding

1. What are the four outputs of a purple-team review?
2. Why is a merged timeline necessary when both teams have logs?
3. Name the columns of the before/after matrix and why versions are required.
4. State the five rules for a fair adaptive variant.
5. Compare two mitigations on at least four dimensions.
6. Write a residual-risk statement with the four required parts.

## 11. What you keep

A merged, correlated timeline; a gap analysis; a before/after matrix with versions; at least one declared adaptive variant with a result; a mitigation comparison across efficacy, generalization, benign cost, performance, and operations; a residual-risk statement; and a purple-team report with separate red and blue sections. These are the core artifacts of [RT-01](../../projects/rt-01-red-blue.md).

## 12. Next

Read the [RT-01 brief](../../projects/rt-01-red-blue.md) and run the exercise end to end. Then Module 18 turns the exercise and one project into a capstone, and shows how to turn a capstone finding into a research question.
