# Capstone — End-to-End ML Security Assessment

<a id="capstone"></a>

**Level 5 · 40 hours · CAP-A to CAP-F · Every rubric dimension at Proficient or above to complete**

The capstone is the course's final artifact. You choose one system, define one decision, ask one attack question and one defense question, execute the work, and defend the result. It integrates threat modeling, attack, defense, engineering, and communication; it is not a longer lab.

The six [project briefs](index.md) are starting points. Extend one, or design an equivalent system with the same scope discipline and get it approved against the criteria below.

If you are choosing a route through the course, the [research-bound path](../learning-paths.md#research-bound) and the [assessment specialization](../learning-paths.md#assessment-and-red-team-specialization) both end here. The difference is the axis you extend: a research question or an applied assessment.

## Options

| ID | Option | Core question | Typical starting point | Difficulty |
|---|---|---|---|---|
| CAP-A | End-to-end risk assessment of a local ML service | Is this system's posture adequate for its decision, and what remains after controls? | PRJ-01, PRJ-02, or RT-01 | 5 |
| CAP-B | Replication and critique of a robustness benchmark | Does the reported comparison reproduce, and does it survive an adaptive attack? | PRJ-06 or PRJ-02 | 5 |
| CAP-C | Privacy attack and DP defense study | What does an attack recover, and what does a DP mechanism cost in utility? | PRJ-03 | 5 |
| CAP-D | Secure ML supply-chain blueprint | Can the pipeline guarantee integrity from data to deployment, and does it fail closed? | PRJ-04 | 4 |
| CAP-E | Agentic or RAG security evaluation harness | Can hostile input be contained when the agent has tools, and at what utility cost? | PRJ-05 or RT-01 | 5 |
| CAP-F | Federated learning threat model and robust aggregation study | How do poisoning and robust aggregation interact under a fixed client budget? | LAB-16 + a new question | 5 |

Every option must include an **authorized-use statement**, a **reproducibility package**, and a **limitations** section. CAP-A and CAP-E must not target third-party production systems.

## Required artifacts

| # | Artifact | Minimum content |
|---|---|---|
| 1 | Problem statement and system diagram | Decision, stakeholders, harm, architecture, boundaries, versions |
| 2 | Threat model and risk register | Assets, adversary profiles, ≥ 8 scored risks, dispositions, assumptions |
| 3 | Reproducible experimental setup | Pinned environment, seeds, data generator/hash, configs, run commands |
| 4 | Baseline measurements | Clean metrics with denominators, intervals, and a zero-effect control |
| 5 | Attack experiments | ≥ 3 attacks with budgets, oracles, results, and negative results |
| 6 | Defense experiments | ≥ 1 control, replayed against the same attacks, plus an adaptive variant |
| 7 | Results tables and visualizations | One table per claim; figures with uncertainty, n, and budget |
| 8 | Limitations and residual risks | Construct, internal, external, statistical; residual risk with numbers |
| 9 | Security recommendations | Ordered by risk reduction per cost; owner, effort, retest for each |
| 10 | Technical report | 8–12 pages, structured as below |
| 11 | Demonstration instructions | Clean-checkout commands, expected runtime, expected headline number |
| 12 | Briefing | 10 minutes, recorded or presented, with slides |

Artifacts 1–9 are evidence. Artifacts 10–12 are communication. A capstone with strong evidence and no communication is incomplete, and so is the reverse.

## Milestones and checklists

### M0 — Proposal (2 hours)

- [ ] Option chosen and scored against skill, data, compute, measurement, risk, interest.
- [ ] One-system, one-decision scope written.
- [ ] Attack question and defense question are falsifiable.
- [ ] Data source, license, size, and generation method stated.
- [ ] 40-hour budget by milestone, with at least 8 hours of buffer.
- [ ] Non-goals list specific systems and activities.
- [ ] Three feasibility tests planned: data, compute, self-reproduction.
- [ ] `proposal.md` frozen and dated.

**Gate:** another person can state what will be measured and what will not.

### M1 — Threat model (4 hours)

- [ ] Architecture diagram with trust boundaries.
- [ ] Asset inventory with classification and owner.
- [ ] Two adversary profiles with goal, knowledge, capability, access, budget, success metric.
- [ ] ≥ 8 risks scored with published anchors.
- [ ] Disposition for every risk: test, accept, reject, defer.
- [ ] Every planned test traces to a risk.
- [ ] Assumptions and out-of-scope adversaries recorded.

**Gate:** no test exists without a risk, and no top-five risk lacks a test or a written acceptance.

### M2 — Baseline (6 hours)

- [ ] Environment pinned; Python and package versions recorded.
- [ ] Data generated or loaded; SHA-256 recorded.
- [ ] Split frozen; split hash recorded.
- [ ] Baseline metrics with denominators and intervals.
- [ ] Zero-effect control run and reported.
- [ ] `run.json` written for every run.
- [ ] Clean-checkout reproduction attempted once.
- [ ] `baseline/` treated as read-only after this gate.

**Gate:** the headline baseline number reproduces from a fresh environment, or the deviation is explained and bounded.

### M3 — Attacks (12 hours)

- [ ] ≥ 3 attacks, each with hypothesis, procedure, budget, oracle, metric, evidence.
- [ ] Attack success defined with a denominator and a base set.
- [ ] Results at more than one budget or condition where applicable.
- [ ] ≥ 1 negative or inconclusive result reported honestly.
- [ ] Adaptive variant planned (executed at M4).
- [ ] Results table frozen; figures sketched.
- [ ] Budget used per attack recorded.

**Gate:** each attack answers a registered risk, and each result can be traced to a run record.

### M4 — Defense (10 hours)

- [ ] ≥ 1 control implemented, not only proposed.
- [ ] Same attacks replayed against the control.
- [ ] One adaptive variant declared before running and executed.
- [ ] Costs measured: clean performance, false positives, latency, operational effort.
- [ ] Before/after matrix with versions.
- [ ] Residual-risk statement with adversary, controls, effect, decision.
- [ ] At least one limitation that the control does not address.

**Gate:** the control is tested against an adversary who knows it, and its cost is measured.

### M5 — Report and briefing (6 hours)

- [ ] Report follows the structure below and is 8–12 pages.
- [ ] Every claim has a table or figure with n, budget, and uncertainty.
- [ ] Limitations cover all four validity types.
- [ ] Recommendations are ordered and costed.
- [ ] Demonstration instructions reproduce the headline result from a clean checkout.
- [ ] Manifest hashes match artifacts.
- [ ] Briefing is 10 minutes and decision-oriented.
- [ ] Ethics and authorized-use statements included.

**Gate:** a stranger can reproduce the headline number and state the residual risk.

## Progress self-assessment

Review every week. Record the status in the log, not only in your head.

| Question | Green | Amber | Red |
|---|---|---|---|
| Is the last milestone gate closed with evidence? | Yes | One item missing | Two or more missing |
| Is the baseline reproducible? | Clean checkout passed | Reproduces with fixes | Not attempted or failing |
| Is the remaining work inside the budget? | ≤ 80% used | 80–100% | Over budget |
| Is the headline claim supported by a table? | Yes, with interval | Table without interval | No table |
| Is the package current? | Updated at last gate | One gate behind | Two or more behind |
| Are scope changes logged? | All | Most | Unlogged |
| Is the next action single and clear? | Yes | Two candidates | No |

Amber for two consecutive weeks is a signal to cut scope. Red on baseline or package is a stop-and-fix condition, regardless of the calendar.

## Capstone rubric (100 points)

Every dimension must reach **Proficient (3)** for completion. A score of 4 is exemplary; 2 is Developing; 1 is Insufficient.

| Dimension | Weight | 4 — Exemplary | 3 — Proficient | 2 — Developing | 1 — Insufficient |
|---|---:|---|---|---|---|
| Problem, system, and data | 10 | Scope enumerable; decision and harm explicit; data classified and licensed; boundaries complete | Clear scope and data inventory with minor gaps | Vague scope or missing classification | No usable scope or data record |
| Threat model | 15 | Testable adversaries; anchored risk scores; every test traced; rejections reasoned | Clear model with minor gaps | Generic threats; weak traceability | No threat model or misleading claims |
| Baseline and experimental design | 15 | Frozen, hashed baseline; controls; multiple budgets/seeds; uncertainty; confounders addressed | Sound baseline and comparison with limited uncertainty | Single run or confounded comparison | No baseline or invalid comparison |
| Attack execution and analysis | 20 | ≥ 3 attacks; correct budgets; adaptive variant; honest negative results; no overclaim | Attacks run correctly with minor omissions | Partial results or metric errors | Attacks do not run or results invalid |
| Defense and adaptive evaluation | 15 | Implemented control; replay; declared variant; costs measured; residual risk | Control evaluated with limited adaptivity | Static test only | No defense or no evaluation |
| Reproducibility and evidence | 10 | Clean checkout; manifest matches; run records; one-command reproduction | Reproduces with small fixes | Missing steps | Not reproducible |
| Communication and recommendations | 10 | Report and briefing decision-oriented; findings costed and ordered; residual risk clear | Clear with minor issues | Disorganized or overlong | Unsupported or unsafe recommendations |
| Ethics, safety, and limitations | 5 | Authorized-use statement; local/synthetic; all four validity types; no overclaim | Clear constraints with minor gaps | Weak limitations or safety statement | Unsafe, unlawful, or overclaiming |

**Automatic fail conditions:** a third-party production target; real personal data; a real credential; a fabricated result; a claim that contradicts the artifact.

### Score sheet

| Dimension | Weight | Score (1–4) | Weighted |
|---|---:|---:|---:|
| Problem, system, data | 10 | | |
| Threat model | 15 | | |
| Baseline and design | 15 | | |
| Attack execution | 20 | | |
| Defense and adaptive | 15 | | |
| Reproducibility | 10 | | |
| Communication | 10 | | |
| Ethics and limitations | 5 | | |
| **Total** | **100** | | |

Weighted score = weight × score / 4. Completion requires every row ≥ 3 (Proficient), not only a high total.

## Reproducibility requirements

The package must contain:

```text
README.md               # purpose, commands, runtime, expected result
proposal.md             # frozen at M0
threat-model.md
risk-register.csv
requirements.txt        # exact versions
environment.txt        # Python, OS, CPU, key libraries
data/                   # generator + DATA.md + checksum (no restricted data)
src/                    # training, attack, defense, evaluation
configs/                # baseline, attack, defense
scripts/run_all.sh      # one command for the headline result
results/                # run records + metrics + figures source
report/                 # report source and figures
manifest.json           # hashes of all artifacts
```

**Clean-checkout test.** Copy the package to a new directory, create a new virtual environment, install from `requirements.txt`, run `scripts/run_all.sh`, and compare the headline number to the report. Record the outcome in the report.

**Never commit:** real personal data, credentials, API keys, large model weights, licensed datasets that cannot be redistributed, absolute local paths, or notebook outputs containing secrets.

## Report structure

| Section | Content | Length |
|---|---|---|
| Abstract | System, question, method, headline result, residual risk | 150–200 words |
| 1. Problem and system | Decision, harm, architecture, scope | 1 page |
| 2. Threat model | Assets, boundaries, adversaries, risk register summary | 1–1.5 pages |
| 3. Method | Data, split, metrics, baselines, attacks, defenses, budgets | 1.5–2 pages |
| 4. Results | Tables and figures, one claim each, negative results | 2–3 pages |
| 5. Discussion | Alternative explanations, validity threats, residual risk | 1 page |
| 6. Recommendations | Ordered, costed, owner, retest | 1 page |
| 7. Limitations | Construct, internal, external, statistical | 0.5–1 page |
| 8. Reproduction | Commands, environment, expected number | 0.5 page |
| References | Verified sources only | As needed |
| Appendix | Per-seed values, configs, additional figures | Unlimited |

The report is 8–12 pages excluding appendix. A longer report is not a better one.

## Briefing and demonstration

The briefing is ten minutes, with five slides:

1. **Decision and system** — what the system decides, who is harmed when it fails.
2. **Threat** — one adversary, one budget, one risk.
3. **What we measured** — baseline and the attack result, with a number.
4. **What we changed** — the control, its cost, and the adaptive result.
5. **What remains** — residual risk and the first recommendation.

The demonstration is a terminal session, not a slide:

```bash
cd capstone
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash scripts/run_all.sh
# expected: results/baseline/metrics.json and results/defense/metrics.json
```

State the expected runtime and the expected headline number before running. If the demonstration fails, the capstone is incomplete until the package is fixed.

## Research extension (LO-35)

A capstone can become a research question. It is not required for course completion, but it is the route to an MPhil or a publication.

| Step | Artifact | Test |
|---|---|---|
| 1. Claim–evidence table | Ten nearest papers with claim, evidence, assumption, boundary | A repeated boundary is visible |
| 2. Gap statement | What is not known, under which condition, why it matters | A reader can disagree |
| 3. Research question | Population, intervention, comparator, outcome, budget | Can be answered no |
| 4. Contribution type | Replication, extension, negative result, benchmark, method, measurement | Evidentiary bar is stated |
| 5. Design | Controls, ablations, adaptive condition, seeds, analysis | Confounders addressed |
| 6. Validity plan | Construct, internal, external, statistical | Each threat has a mitigation or disclosure |
| 7. Ethics and supervision | Institutional review, data license, supervisor | Approval before data collection |

See [Lesson 18.4](../modules/m18-capstone-and-research/lesson-4-from-project-to-research-question.md) for the canvas and templates.

**What the capstone does not provide:** academic credit, a supervisor, ethics approval, or a publication. Those belong to your institution. The capstone is evidence you can do the work; the research route is a plan for what comes next.

## Ethics and authorized use

Every capstone includes a one-page statement:

```text
AUTHORIZED USE
Targets: [local mock / synthetic data / public sandbox]
Authorization: [self / system owner / sandbox terms]
Data: [synthetic / public licensed; no personal data]
Constraints: [no third-party systems; loopback only; budgets]
Stop conditions: [list]
Disclosure: [how findings are stored and shared]
```

Work that targets a system you do not own, uses real personal data, or distributes a malicious artifact is not assessed. If you discover a real vulnerability during an authorized sandbox exercise, stop and follow the sandbox's disclosure process.

## Completion

The capstone is complete when:

1. All twelve required artifacts exist.
2. Every rubric dimension is at Proficient (3) or above.
3. The clean-checkout test reproduces the headline number.
4. The briefing and demonstration have been delivered.
5. The ethics statement is signed and the limitations are stated.

Completion is a self-study record. No certificate, credit, or professional certification is issued.

## Frequently asked questions

**Can I extend a project I already submitted?** Yes. The capstone must add a new adversary, measurement, control, or a replication with a critique. More seeds alone is not enough.

**Can I change scope after M0?** Yes, with a logged change request and a revised budget. Silent scope changes invalidate the timeline and the claim.

**What if the defense fails?** Report the failure, the adaptive result, and the residual risk. A well-measured failure is a complete capstone.

**What if I run out of time?** Cut breadth, not validity: fewer attacks, one dataset, one seed with a stated limitation. Never cut the baseline, the evaluation-set hash, or the adaptive test without disclosing that the claim is narrower.

**Can I use cloud compute?** The course is CPU-first and offline. A local machine is sufficient; if you use a cloud sandbox, confirm its terms and keep the data synthetic.

**Is a negative result acceptable?** Yes, if it is measured with adequate budget and reported with an interval. "No effect observed at this budget" is a result; "the system is secure" is not.

## Next step

Read [Module 18](../modules/m18-capstone-and-research/index.md) for scoping, milestones, results, and the research route. Choose a [project](index.md) or an option above, then freeze the M0 proposal.
