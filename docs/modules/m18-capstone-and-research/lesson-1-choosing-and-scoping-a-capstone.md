# Lesson 18.1 — Choosing and Scoping a Capstone

<a id="m18-l1"></a>

**Module 18 · Lesson 1 of 4 · 1 hour · LO-33**

## Scenario

Two capstone proposals arrive in the same week.

The first: *"An investigation of security risks in large language models."* It lists fourteen topics, no system, no dataset, and no measurement. Six weeks later it is a 30-page summary of papers with three screenshots of a chatbot.

The second: *"Does adding a feature-delta detector to a local credit-scoring API reduce successful evasion without increasing false declines above 2%?"* It names a system, a control, a metric, two thresholds, a dataset of 5,000 synthetic records, a 4-week plan, and a stop rule. It is narrow enough to finish and specific enough to be wrong.

The second proposal is not more ambitious. It is more falsifiable, which makes it a better capstone.

## Objectives

By the end of this lesson you will be able to:

1. State what a capstone must demonstrate that a lab does not.
2. Choose a capstone option using explicit criteria rather than interest alone.
3. Apply a scoping rule that keeps the work inside 40 hours.
4. Write a one-page proposal with a question, system, method, data, budget, and non-goals.
5. Run three feasibility tests before committing.

## 1. What a capstone must demonstrate

| Skill | Lab evidence | Capstone evidence |
|---|---|---|
| Execution | Runs a specified technique | Chooses the technique that fits the risk |
| Measurement | Uses a given metric and budget | Defines the metric, denominator, and budget |
| Threat modeling | Fills in a template | Decides what is out of scope and why |
| Engineering | Completes a pipeline | Makes the pipeline reproducible by someone else |
| Judgment | Reports the expected result | Reports an inconvenient result honestly |
| Communication | Writes a lab note | Writes a report a decision-maker can use |

A capstone is graded on the second column. A project that executes flawlessly but cannot explain why the metric matters is not a capstone; it is a long lab.

## 2. Choosing an option

The six project families cover the main surfaces. Choose by fit, not by novelty.

| Criterion | Question | Weight |
|---|---|---:|
| Skill fit | Do I have the prerequisites for this surface? | 25% |
| Data access | Can I obtain or generate the data this week? | 20% |
| Compute | Does it run on my machine within the time box? | 15% |
| Measurement clarity | Can I state the oracle and denominator now? | 20% |
| Risk and ethics | Can I test this safely and lawfully? | 10% |
| Interest | Will I still care at hour 35? | 10% |

Score each option 1–5 and multiply. A score of 4+ on data access is close to mandatory: a capstone that waits for data is a capstone that runs out of time.

### The six options in one line each

| Option | Question it answers | Hard part |
|---|---|---|
| CAP-A | Is this system's security posture adequate for its decision? | Keeping scope to one decision path |
| CAP-B | Does this published robustness claim reproduce, and does it survive an adaptive attack? | Reimplementing the evaluation faithfully |
| CAP-C | What does a privacy attack recover, and what does a DP defense cost in utility? | Accounting and utility comparison |
| CAP-D | Can the pipeline guarantee artifact integrity from data to deployment? | Building gates that actually fail closed |
| CAP-E | Can an agent be contained when its inputs are hostile? | Designing adaptive injection variants |
| CAP-F | How do poisoning attacks and robust aggregation interact in federation? | Simulating clients fairly |

The [capstone brief](../../projects/capstone.md) expands each option with deliverables and a rubric. The [project catalog](../../projects/index.md) maps each to a project brief you can extend.

### What to avoid

- **A topic with no system.** "AI safety" is not a system.
- **A system you cannot run.** A cloud service, a proprietary model, or a dataset behind an approval queue.
- **A question already answered by a lab.** Re-running LAB-11 with more seeds is not a capstone.
- **A question with no possible negative answer.** "How can we improve security?" cannot fail.
- **A target you do not own.** Never a production service, even read-only.

## 3. The scoping rule

Use this rule for a 40-hour capstone:

> **One system, one decision, two questions, one control.**

| Element | Meaning | Example |
|---|---|---|
| One system | A single local mock or authorized sandbox | A local credit-scoring API and its retraining pipeline |
| One decision | The decision the system makes | Approve, review, or decline a synthetic application |
| Two questions | One attack question, one defense question | Can evasion cross the threshold within feature bounds? Does a delta detector reduce it without raising false declines? |
| One control | A control you can implement and evaluate | Feature-delta detection with a calibrated threshold |

Anything beyond this becomes a non-goal. Write the non-goals in the proposal; they are the scope's immune system.

### Scope as a list

```text
IN SCOPE
  - System: local scoring API (127.0.0.1:8080) + training script
  - Decision: approve/review/decline for synthetic applications
  - Attack: bounded feature perturbation on 3 applicant features
  - Defense: feature-delta detector + threshold calibration
  - Data: 5,000 synthetic records, seed 7, temporal holdout
  - Metrics: segment approval rate, global false-decline, detector FP rate

OUT OF SCOPE
  - Model extraction, membership inference, prompt injection
  - Production deployment, real applicant data, vendor feeds
  - Network, host, and identity-provider attacks
  - Retraining-pipeline poisoning (covered by PRJ-02, not this capstone)
  - Multi-tenant behavior
```

The out-of-scope list is not a confession of weakness. It is what lets the reader trust the in-scope claims.

## 4. The one-page proposal

Write it before the first experiment and freeze it. Changes after M0 are logged, not silent.

| Section | Content | Test of quality |
|---|---|---|
| Title | System + question | A reader knows what is measured |
| Problem | The decision and who is harmed when it fails | Names an asset |
| System | Architecture in five lines, with versions | A reader could sketch it |
| Threat model summary | Adversary, access, budget, objective | One profile, not a list |
| Question | One attack question, one defense question | Both can be answered no |
| Method | Data, split, metrics, baselines, controls | Denominators are stated |
| Deliverables | Artifact, report, briefing, package | Each has an acceptance test |
| Budget | Hours by milestone; compute; data | Adds to ≤ 40 h |
| Risks | Three ways it could fail | Each has a mitigation |
| Non-goals | What is excluded | Specific systems and activities |

### Proposal template

```text
TITLE: Does feature-delta detection reduce bounded evasion in a local
       credit-scoring API without raising false declines above 2%?

PROBLEM: The API decides approve/review/decline. A missed decline costs
         the lender; a false decline harms an applicant. The decision is
         the asset.

SYSTEM: Python 3.14 mock API, scikit-learn gradient boosting, version
        1.4, threshold 0.55, 5,000 synthetic records, seed 7.

THREAT: External applicant, API access only, no weights or training data,
        ≤ 3 feature changes within the 1st–99th percentile, 900 requests.

QUESTIONS:
  Q1 (attack): Can a bounded perturbation lower the target segment's
     decline rate below 0.10 at global false-decline ≤ 0.02?
  Q2 (defense): Does a feature-delta detector with threshold t reduce Q1
     success below 0.05 while keeping detector FP ≤ 0.5% of benign?

METHOD: Temporal holdout 1,000 records; baseline decline rate; bounded
        search over 3 features; detector calibrated on 2,000 quiet
        requests; replay Q1; adaptive variant with a slower ramp.

DELIVERABLES: code + tests, report (8–12 pp), 10-min briefing,
        reproducibility package, risk register.

BUDGET: M0 2 h, M1 4 h, M2 6 h, M3 12 h, M4 10 h, M5 6 h = 40 h.

RISKS: (1) synthetic data too easy -> add realistic overlap; (2) detector
       too noisy -> calibrate at FP budget; (3) scope creep -> non-goals.

NON-GOALS: extraction, membership inference, production, real data,
        network attacks, retraining poisoning.
```

This is one page. It is also a contract with yourself.

## 5. Three feasibility tests

Run these before committing. Each takes under an hour.

| Test | Procedure | Pass condition |
|---|---|---|
| Data | Generate or load the dataset; hash it; train the baseline | Baseline metric reproduces within a stated tolerance |
| Compute | Time one training run and one attack run | Full experiment suite fits in the remaining hours |
| Reproduction | Follow your own setup notes in a fresh environment | You can rerun the baseline without guessing |

If any test fails, change the option or the scope now. Discovering a data problem at hour 20 is the most common capstone failure.

### A cold-start check

Ask: could another student reproduce my baseline from the proposal alone? If not, the method section is incomplete. This is the same standard the evaluator will apply at M5.

## 6. Worked example — from broad interest to a scoped question

| Stage | Statement | Problem |
|---|---|---|
| Interest | "I want to study RAG security." | No system, no question |
| Surface | "Indirect prompt injection in a local RAG assistant." | Better, still no measurement |
| System | "A local assistant with 40 mock policy documents and two tools." | Runnable |
| Decision | "Whether to answer, refuse, or call a tool." | One decision |
| Question | "Does document provenance labeling plus a tool allowlist reduce successful indirect injection below 0.10 without refusing more than 5% of benign queries?" | Falsifiable |
| Non-goal | "No model fine-tuning, no real documents, no third-party services." | Bounded |

The move from stage 1 to stage 5 is the lesson. Each step removes a degree of freedom.

## 7. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Topic instead of question | No falsifiable result | Name the decision and the metric |
| Choosing by novelty | Prerequisites missing | Score options on skill and data |
| No non-goals | Scope expands | Write excluded systems |
| Data unavailable | Work stalls | Feasibility test in week 1 |
| Compute underestimated | Experiments cut | Time one run before committing |
| Two systems | Neither is finished | One system, one decision |
| Control assumed, not implemented | No defense result | Build and test the control |
| Proposal never frozen | Scope drifts silently | Freeze at M0; log changes |
| No negative question | Cannot fail | Ask "does X reduce Y below Z?" |
| Ignoring ethics | Unsafe or unlawful target | Local/synthetic only; authorized-use statement |

## 8. Check your understanding

1. What does a capstone demonstrate that a lab does not?
2. Why does data access carry more weight than interest in the scoring table?
3. State the one-system scoping rule and apply it to one project family.
4. Which sections of the proposal make a question falsifiable?
5. What are the three feasibility tests, and what does each prove?
6. Why should the proposal be frozen at M0?

## 9. What you keep

A scored option comparison, a one-page proposal, an in-scope/out-of-scope list, a 40-hour budget by milestone, three feasibility results, and a frozen M0 baseline. Lesson 18.2 turns the proposal into a milestone plan and a reproducibility contract.

## 10. Next

Lesson 18.2 covers milestones with exit criteria, the reproducibility package, weekly logging, and the stop rules that keep a 40-hour project from becoming an 80-hour one.
