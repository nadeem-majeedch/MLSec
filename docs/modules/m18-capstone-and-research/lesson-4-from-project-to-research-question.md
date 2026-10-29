# Lesson 18.4 — From Project to Research Question

<a id="m18-l4"></a>

**Module 18 · Lesson 4 of 4 · 1 hour · LO-35**

## Scenario

A student finishes a capstone with a useful result: a feature-delta detector reduced evasion on a local credit-scoring mock, but the reduction disappeared when the attacker paced requests below the detector's window. The student wants to continue to an MPhil.

The first proposal is "Security of AI in finance." It names no gap, no method, and no contribution. The second is: "Do window-based evasion detectors generalize across pacing strategies when calibrated at a fixed false-positive budget? A controlled comparison of three detectors under adaptive pacing." It names a gap, a design, a population, and a measurable outcome.

The second proposal came from the capstone's limitation section. That is usually where research questions come from: not from a topic you find interesting, but from a result you cannot yet explain.

## Objectives

By the end of this lesson you will be able to:

1. Distinguish a topic, a question, and a researchable gap.
2. Choose a contribution type and state what evidence it requires.
3. Write a gap statement from a claim–evidence table rather than from impressions.
4. Design a study with controls, ablations, and an adaptive condition.
5. Plan the ethics, supervision, and reporting a research route requires.

## 1. Topic, question, gap

| Level | Example | Why it is not yet research |
|---|---|---|
| Topic | "AI security in finance" | No question, no measurement |
| Question | "Are fraud models robust to evasion?" | Too broad; no system, budget, or metric |
| Bounded question | "Does a feature-delta detector reduce bounded evasion in a local credit model at a 0.5% FP budget?" | Answerable, but may be a capstone rather than a contribution |
| Researchable gap | "Existing window-based detectors are evaluated at a single pacing rate; it is unknown whether their measured recall survives adaptive pacing at a fixed FP budget." | Names what is not known and why it matters |

A research question sits on a gap: a specific, defensible statement about what current work does not establish. "Nobody has studied X" is rarely true and is not a gap. "Studies of X evaluate at one pacing rate, so their recall estimates do not bound performance under adaptive pacing" is a gap.

### The six tests of a research question

| Test | Question | Fail example |
|---|---|---|
| Gap | What exactly is not known? | "Security is important" |
| Novelty | How is this different from the nearest work? | Re-running a published benchmark |
| Falsifiability | What observation would answer no? | "How can we improve detection?" |
| Feasibility | Can it be done with available data, compute, and time? | Requires a production feed |
| Significance | Who would change a decision based on the answer? | Trivially true either way |
| Ethics | Can it be studied lawfully and safely? | Real customer data without approval |

If any test fails, revise the question before designing the study.

## 2. Contribution types

A contribution is a claim to new knowledge, and each type has a different evidentiary bar.

| Type | Contribution | Required evidence | Common failure |
|---|---|---|---|
| Replication | The reported effect reproduces under stated conditions | Same protocol, independent implementation, reported deviations | Replication in name only; changed protocol |
| Extension | The effect holds or changes under a new condition | New condition isolated; controls for the original | Confounded by other changes |
| Negative result | A predicted effect is absent or smaller than reported | Adequate power, stated budget, interval | Underpowered null presented as proof |
| Benchmark | A measurement instrument others can use | Coverage argument, baselines, leakage checks, maintenance plan | Benchmark measures the wrong construct |
| Method | A new attack or defense | Threat model, baselines, adaptive evaluation, ablation | Compared only to weak baselines |
| Measurement study | A systematic characterization of a phenomenon | Sampling frame, coding scheme, reliability, prevalence estimates | Anecdotal sample, no denominators |

For an MPhil, replication with a methodological critique, a careful negative result, or a measurement study are all legitimate. Novelty of technique is not the only route, and it is usually the hardest to defend.

## 3. Finding the gap: the claim–evidence table

Read the nearest ten papers with one table per paper.

| Field | Content |
|---|---|
| Claim | What the paper asserts |
| Evidence | Dataset, model, budget, metric, sample size |
| Assumption | What must be true for the claim to hold |
| Boundary | Conditions the authors did not test |
| Reproducible? | Code/data available; protocol complete |
| Threat to validity | The weakness a reviewer would name |

Then look for a column with repeated entries: the same boundary in five papers is a gap.

### The assumption audit

Most gaps hide in assumptions:

- the attacker does not adapt;
- the evaluation set is fixed and representative;
- the detector's false-positive budget is unconstrained;
- one model family stands in for all;
- the metric is a proxy for harm that was never validated.

Pick one assumption, state what happens if it is false, and design the smallest study that tests it.

### Gap statement template

```text
Existing work on [topic] evaluates [intervention] under [condition].
These studies establish [claim] for [population/budget], but they hold
[assumption] fixed. It is therefore unknown whether [claim] survives
when [assumption] is relaxed. This matters because [decision/practice]
depends on [claim] under [the relaxed condition]. This study tests
[hypothesis] by [design] on [system/data], measuring [outcome] at
[budget].
```

Every blank is a decision. A gap statement with a vague blank is a vague project.

## 4. Designing the study

### The research-question canvas

| Element | Content | Example |
|---|---|---|
| Question | One falsifiable sentence | Does detector recall survive adaptive pacing at a fixed FP budget? |
| Population / system | Where the claim applies | Local credit-scoring mock; synthetic applications |
| Intervention | What is varied | Three detectors: fixed window, cumulative, sequence |
| Comparator | What it is compared to | Baseline detector at the published window |
| Outcome | What is measured | Recall at 0.5% FP; time to detect; benign block rate |
| Budget | Bounds on the adversary | Requests, pacing range, feature changes |
| Design | How conditions are assigned | Same data/split; three seeds; adaptive condition |
| Controls | What is held fixed | Model, threshold, evaluation set, benign baseline |
| Analysis | How uncertainty is estimated | Bootstrap intervals; per-seed results |
| Ethics | Approval and data handling | Synthetic data; no human subjects; local only |

### Controls and ablations

- **Controls:** everything that must stay the same so the comparison is valid — model, split, threshold, benign baseline, budget.
- **Ablations:** remove one component to estimate its contribution — detector without the cumulative feature, pacing without adaptation.
- **Adaptive condition:** the variant a real adversary would use after learning the defense. Without it, the study measures the scripted attack.

### Pre-registration-lite

You do not need a formal registry for an MPhil, but fixing the plan before data collection prevents accidental p-hacking.

```text
PRE-REGISTRATION (lite)
Hypothesis: Recall of window-based detection falls below 0.50 under
  adaptive pacing at a 0.5% FP budget.
Primary outcome: recall at 0.5% FP, measured on 100 held-out attack events.
Secondary: time to detect; benign block rate.
Conditions: 3 detectors x 2 pacing regimes x 3 seeds.
Exclusion rule: runs with a failed manifest are excluded and reported.
Analysis: mean and bootstrap interval; no threshold changes after seeing
  test results.
What would falsify: recall >= 0.50 with an interval excluding 0.50.
```

The last line is the most important. A study that cannot be falsified is a demonstration.

## 5. Threats to validity, and how reviewers attack

| Threat | Reviewer question | Pre-emption |
|---|---|---|
| Construct | Does recall measure the harm? | Add a decision-level outcome; discuss the proxy |
| Internal | What else changed? | Freeze controls; report the config diff |
| External | Does it hold beyond this mock? | State the boundary; add a second dataset if possible |
| Statistical | Is the interval compatible with the claim? | Report intervals and n; avoid best-seed |
| Ethical | Was the work authorized and safe? | Approval, synthetic data, no third-party targets |
| Reproducibility | Can I rerun it? | Package, manifest, seeds, clean-checkout test |

A reviewer will find the weakest of these. Write the limitations section as if you were the reviewer, then fix what you can and disclose what you cannot.

## 6. From capstone to paper

A paper is not the capstone report with a new title. The emphasis changes.

| Section | Capstone report | Research paper |
|---|---|---|
| Introduction | Problem and scope | Gap and contribution |
| Related work | Brief context | Position against the nearest work |
| Method | Enough to reproduce | Enough to critique and extend |
| Results | All claims | Claims tied to the contribution |
| Limitations | Residual risk | Threats to validity |
| Conclusion | Recommendations | What is now known and what remains |

### The three reviewer questions

1. **What is new?** One sentence, in the abstract.
2. **Why should I believe it?** Design, controls, uncertainty, adaptive test.
3. **What does it not show?** Boundaries and threats to validity.

If the abstract cannot answer all three, the paper is not ready.

### Negative results and artifacts

A well-measured negative result is publishable in venues that value replication and null results, and it is valuable to practitioners. Artifact evaluation badges reward packages that reproduce; build the package as if it will be reviewed, because it may be.

## 7. The MPhil route: supervision, ethics, and scope

| Question | What to do |
|---|---|
| Is this an MPhil-sized question? | One gap, one design, one system, 12–24 months part-time; ask a supervisor |
| Who approves the ethics? | Your institution's review board, before data collection |
| Whose data? | Synthetic or licensed; never personal data without approval and a lawful basis |
| Who owns the artifact? | Clarify with the supervisor and institution before publishing |
| What if the result is negative? | That is a result; design the study so a null is informative |
| How does the capstone count? | As a pilot or a chapter, usually after extension and re-analysis |

This lesson is guidance, not supervision. An MPhil requires a supervisor, institutional review, and adherence to your institution's rules. Nothing here substitutes for those.

### A realistic first-year plan

| Quarter | Work |
|---|---|
| 1 | Read 30 papers; claim–evidence table; gap statement; ethics application |
| 2 | Build the testbed; reproduce the nearest baseline; pilot study |
| 3 | Main experiment; adaptive condition; analysis |
| 4 | Write the paper or thesis chapter; artifact package; review |

The plan assumes the testbed exists. If it does not, add a quarter. Most first-year delays are testbed delays, not idea delays.

## 8. Worked example — from capstone finding to question

**Capstone finding.** A feature-delta detector reduced evasion success from 0.31 to 0.12 at a fixed threshold, but a slower pacing variant restored success to 0.27. Detection recall fell from 0.80 to 0.46.

**Gap.** Evaluations of window-based evasion detectors report recall at one pacing rate. It is unknown whether that recall survives pacing adapted to the window, at a fixed false-positive budget.

**Question.** Does the recall of window-based evasion detection remain above 0.50 under adaptive pacing at a 0.5% false-positive budget?

**Contribution type.** Measurement study with a negative result if recall falls below 0.50; extension if it holds for some detector families.

**Design.** Three detectors (fixed window, cumulative count, sequence), two pacing regimes (steady, adaptive slow ramp), three seeds, one frozen evaluation set, one benign baseline, 100 held-out attack events.

**Controls.** Same model, threshold, split, and budget; detector calibration at 0.5% FP before attack events are opened.

**Threats.** Construct: recall is not harm; add decisions affected per hour. External: one mock and one model family. Statistical: 100 events gives a wide interval; report it.

**Ethics.** Synthetic data, local service, no human subjects; institutional review may still be required for publication.

This is an MPhil-shaped question because it names a gap, a design, and a decision that depends on the answer.

## 9. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Topic as question | No falsifiable study | Name the gap and the outcome |
| "Nobody has studied X" | False gap | Read the nearest ten papers |
| Novelty as the only contribution | Hard to defend, often weak | Consider replication or measurement |
| No adaptive condition | Overstates defense | Add the variant |
| No controls | Confounded comparison | Freeze model, split, threshold |
| Underpowered null | "No effect" overclaim | Report interval and power |
| Ethics deferred | Work cannot be published | Apply before data collection |
| Ignoring the supervisor | Scope mismatch | Bring two options and a recommendation |
| Paper as report | No contribution statement | Answer the three reviewer questions |
| No artifact | Results cannot be checked | Build the package |

## 10. Check your understanding

1. Distinguish a topic, a question, a bounded question, and a researchable gap.
2. Name the six tests of a research question.
3. Choose a contribution type for a replication study and state its evidentiary bar.
4. Write a gap statement with all six blanks filled.
5. What is the difference between a control and an ablation?
6. Why is an adaptive condition necessary for a defense study?

## 11. What you keep

A claim–evidence table for ten papers, a gap statement, a research-question canvas, a contribution-type statement, a pre-registration-lite plan, a validity-threat table, and an ethics and supervision checklist. Together with the capstone, these are the portfolio evidence for LO-35.

## 12. Next

Return to the [capstone brief](../../projects/capstone.md), choose an option, and freeze the M0 proposal. The six [project briefs](../../projects/index.md) are the starting points; RT-01 supplies the red/blue evidence for CAP-A and CAP-E.
