# Student Guide

This guide is the operating manual for studying ML-Sec on your own. It covers the baseline you need, how to set up a lab that you can reproduce, how to work through a module, how to schedule the course, how to assess your own work, and what to do when something breaks.

The course is complete through Level 5. **M00–M18, LAB-01…LAB-20, six applied project briefs, RT-01, and the capstone brief are published and runnable.** Section [Publication status](#incomplete) explains what remains maintenance work.

For site navigation, page types, and accessibility, read [How to use this site](site-guide.md). For a page that will not render, search that returns nothing, or a broken link, use [Troubleshooting](troubleshooting.md); this guide's troubleshooting section covers the lab environment.

## Contents

- [Before you start: baseline and recovery](#baseline)
- [Set up your lab](#setup)
- [How to study a module](#study-loop)
- [Schedules and workload](#schedules)
- [Working through a lab](#labs)
- [Working through a project](#projects)
- [Self-assessment and portfolio](#assessment)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Using AI assistants](#ai-policy)
- [Responsible use and law](#safety)
- [Publication status and extension work](#incomplete)

---

<a id="baseline"></a>

## Before you start: baseline and recovery

### The baseline

| Area | Minimum | Self-check |
|---|---|---|
| Python | Functions, classes, virtual environments, NumPy arrays | Load a CSV, train a scikit-learn classifier, and plot a confusion matrix without copying a full tutorial |
| ML | Train/test splits, loss, overfitting, precision/recall, ROC-AUC | Explain why 99% accuracy can be useless on imbalanced data |
| Math | Gradients, chain rule, basic probability, norms | Differentiate cross-entropy for a linear layer; explain an L-infinity ball in plain language |
| Tooling | Terminal, Git basics, Jupyter | Clone a repository, create a virtual environment, and run a notebook end to end |
| Security | CIA triad, authentication versus authorization | Explain the difference between a vulnerability and an exploit |

You do not need to be strong in all five rows on day one. You do need to be honest about which rows are weak, because every lab will expose them.

### Four-week recovery path

Use this alongside Module 0, not as a gate before it. Repeat a week if the self-check still feels shaky.

| Week | Focus | Work | Done when |
|---|---|---|---|
| 1 | Python and NumPy | Load a CSV into NumPy and pandas; split it; train a classifier; print a confusion matrix. Rewrite the preprocessing as a function and run it from a script, not a notebook cell. | You can run the script from a clean shell with no tutorial open. |
| 2 | ML fundamentals | Train the same classifier with a deliberate train/test leak, then fix the split. Compare accuracy, precision, recall, F1, and ROC-AUC on an imbalanced subset. | You can explain which metric you would monitor and what it would miss. |
| 3 | Calculus and probability | Derive the gradient of cross-entropy for a linear layer on paper. Implement one gradient-descent step in NumPy. Compute the accuracy of a trivial classifier on an imbalanced set. | You can state what a gradient points toward and what an L-infinity budget constrains. |
| 4 | Tooling and security vocabulary | Create a Git repository and commit a notebook. Write a one-page description of a login system using confidentiality, integrity, and availability; name one vulnerability, one exploit, and one risk. | You can distinguish vulnerability, exploit, and risk in one sentence each. |

**Pass standard.** If four of the five baseline rows feel comfortable, start M00. If two or three do not, take the recovery path in parallel with M00 and M01. If all five feel weak, spend four weeks on the recovery path before M02.

A short diagnostic starts Module 01. Until you reach it, use the self-checks above. Do not substitute watching videos for writing code; the labs assess artifacts.

---

<a id="setup"></a>

## Set up your lab

### What you need

- A laptop with at least 8 GB of RAM and 15 GB of free disk space.
- Windows, macOS, or Linux. Windows users can do every Tier A lab natively; a few container labs are easier under WSL2.
- Python 3.11–3.14. Pick one minor version and stay with it for the course. The Levels 1–5 stack was verified on 3.14.7.
- Git, a terminal, and a notebook environment. VS Code with the Jupyter extension is sufficient.
- No GPU, no paid cloud account, and no dataset purchase. Every published lab uses bundled or synthetic data.

### Create an isolated environment

Do not install the course stack into your system Python. Each lab will ship a pinned requirements file; the commands below create a starting environment for the early modules.

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash on Windows
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r labs/shared/requirements-level1.txt
python -m pip install jupyterlab
```

The Levels 1–5 stack is NumPy, pandas, scikit-learn, joblib, and PyYAML — all CPU-only. Every published lab and project, including the robustness, supply-chain, serving, federated, privacy, explanation, LLM/agent, and end-to-end assessment work, uses this stack plus the Python standard library (`pickletools`, `hmac`, `http.server`, `json`, `logging`, `hashlib`). PyTorch is not required by any published lab or project; the lessons discuss it only where a tool would change the experiment. If you want it early, install the CPU wheel with `--index-url https://download.pytorch.org/whl/cpu` and keep it out of the shared requirements file. If a later lab requires a GPU, its own instructions will say so.

### Verify the environment

Run these checks before your first notebook:

```bash
python -c "import sys, numpy, pandas, sklearn, yaml; print(sys.version); print(numpy.__version__, pandas.__version__, sklearn.__version__)"
jupyter lab
```

| Check | Expected |
|---|---|
| Python version | 3.11.x–3.14.x (3.14.7 was used for verification) |
| NumPy, pandas, scikit-learn, PyYAML imports | All print a version |
| JupyterLab | Opens in your browser |
| A trivial notebook | Runs a cell that imports the libraries and prints an array shape |

If any check fails, see [Troubleshooting](#troubleshooting) before installing anything else.

### Workspace layout

Keep your work outside the course repository. A simple layout is:

```text
mlsec-work/
├─ m00-lab01/
│  ├─ lab.ipynb
│  ├─ README.md
│  ├─ requirements.txt
│  ├─ manifest.sha256
│  └─ reflection.md
├─ m01-lab01/
├─ data/                 # gitignored; never commit datasets
├─ checkpoints/          # gitignored
└─ .gitignore
```

Create one folder per lab. Do not reuse a single notebook for several labs; the artifact must be readable on its own.

### Git hygiene

- Initialize a private repository for your portfolio, or keep a local repository with meaningful commits.
- Commit notebooks, write-ups, requirements, and manifests. Do not commit datasets, model checkpoints, virtual environments, or secrets.
- Use imperative, scoped commit messages such as `lab(m04): add epsilon sweep and threat-model note`.
- Before submitting a lab, confirm that `git status` shows no data files or credentials.
- If you use a public repository, remember that notebooks can contain outputs with paths, usernames, or API errors. Clear outputs before publishing.

### Notebook hygiene

- Restart the kernel and run all cells before calling a lab done.
- Do not rely on hidden state from an earlier session.
- Keep long-running outputs small; save tensors to disk and report hashes instead of embedding them.
- Put the seed and version print at the top of the notebook so the artifact is self-describing.

---

<a id="study-loop"></a>

## How to study a module

### The module anatomy

Every module follows the same pattern:

> **Scenario → objectives → lessons → lab → quiz → reflection → artifact**

The scenario tells you what is at risk. The objectives state what you will be able to do. The lessons supply the minimum theory. The lab turns theory into measured evidence. The quiz checks retrieval. The reflection exposes what you still misunderstand. The artifact is what you keep.

### The six-step lesson protocol

| Step | Action | Time box | Output |
|---|---|---|---|
| 1. Scenario | Read the failure story and name the asset, adversary, and harm | 10 min | Three sentences in your notes |
| 2. Objectives | Rewrite each objective as a testable claim about what you can do | 5 min | A checklist |
| 3. Concept | Read one explanation; close the page; restate it in your own words | 30–45 min | A short explain-back paragraph |
| 4. Guided practice | Run the notebook; change one variable; predict the result first | 30–60 min | One recorded before/after result |
| 5. Check | Answer the knowledge check without looking anything up | 15 min | Score and a list of misses |
| 6. Artifact | Complete the lab deliverable and write the reflection | 1–3 h | A portfolio folder |

If step 3 produces a paragraph you would not show anyone, you have not understood it yet. Re-read one section, not the whole lesson.

### Read with a prediction

Before running any lab code, write down:

- what you expect the clean accuracy to be;
- how much accuracy you expect the attack to remove at the stated budget;
- which examples you expect to be easiest and hardest;
- what would surprise you.

A wrong prediction is more instructive than a correct result. Record it in the lab write-up; the gap between prediction and measurement is the actual lesson.

### The weekly loop

| Block | Time | Activity |
|---|---:|---|
| Preview | 20 min | Skim objectives, lab deliverable, and quiz topics; write three questions |
| Read | 60–90 min | One lesson at a time, with notes in your own words |
| Practice | 60–120 min | Run the guided notebook and alter one parameter |
| Lab | 2–4 h | Complete the artifact and commit it locally |
| Retrieve | 20 min | Closed-book quiz; re-derive the key equation or attack loop |
| Reflect | 15 min | Update the study log; schedule review at 1, 3, 7, and 21 days |

A 6–10 hour week does not require six separate sittings, but it does require at least one retrieval session that is not reading.

### Spaced review

Review each module at **1, 3, 7, and 21 days**. Use retrieval only:

- Re-derive FGSM and the PGD update from memory.
- Restate the difference between poisoning and a backdoor, with an example of each.
- Sketch a threat model for a service you use, naming two trust boundaries.
- Explain epsilon, delta, and composition to an imaginary colleague.
- Name one reason a defense that reports 0% attack success might still be broken.

Do not re-read passively and call it review. If you cannot produce the idea without the page, you have found the section to study again.

### Study log template

```text
Date:
Module / lab:
Time spent:
What I predicted:
What happened:
Metric(s):
Surprise / failure:
Next test:
Question for review:
```

Keep one log for the whole course. It becomes the raw material for your capstone's limitations section and for explaining your own progress.

---

<a id="schedules"></a>

## Schedules and workload

### Tracks

| Track | Modules | Effort | Typical duration |
|---|---|---:|---|
| Foundations | M00–M03 | 39 h | 4–7 weeks |
| Core attacks | M00–M07 | 94 h | 10–16 weeks |
| Practitioner | M00–M11 | 148 h | 15–25 weeks |
| Applied assessment specialization | M00–M03, M16–M18 + one project + CAP | 113 h | 12–19 weeks |
| Full program plus capstone | M00–M18 + CAP | 276 h | 28–46 weeks |
| GenAI and agent specialization | M00–M03, M15 + CAP | 97 h | 10–16 weeks |

### Pace table

| Pace | Foundations | Core attacks | Practitioner | Full program | Assessment specialization | GenAI specialization |
|---|---:|---:|---:|---:|---:|---:|
| 6 h/week | 7 weeks | 16 weeks | 25 weeks | 46 weeks | 19 weeks | 17 weeks |
| 8 h/week | 5 weeks | 12 weeks | 19 weeks | 35 weeks | 15 weeks | 13 weeks |
| 10 h/week | 4 weeks | 10 weeks | 15 weeks | 28 weeks | 12 weeks | 10 weeks |
| 15 h/week | 3 weeks | 7 weeks | 10 weeks | 19 weeks | 8 weeks | 7 weeks |

These are study-time estimates. Calendar time is longer when life intervenes; plan for it rather than pretending it will not.

### A 28-week full-program plan at 10 hours per week

| Weeks | Effort | Focus | Milestone |
|---|---:|---|---|
| 1–10 | ≈ 94 h | M00–M07: orientation, Python and data tooling, ML fundamentals, threat modeling, evasion, poisoning, backdoors, extraction and privacy | LAB-01…LAB-10 complete; a threat model and an attack dossier you would show a colleague |
| 11–13 | ≈ 28 h | M08–M09: robustness evaluation, adversarial training, data integrity, leakage, and reproducible pipelines | Robustness audit and validation report |
| 14–16 | ≈ 26 h | M10–M11: supply chain, signing, serving security, monitoring, and incident response | Signed artifact, hardened API, and IR package |
| 17–21 | ≈ 54 h | M12–M15: federated learning, privacy engineering, explainability and fairness, generative and agentic security | LAB-16…LAB-20 complete; frontier reports |
| 22–23 | ≈ 16 h | M16: assessment method and one project | Project dossier (PRJ-01…PRJ-06) |
| 24–25 | ≈ 18 h | M17 and M18: red/blue exercise, results, limitations, research question | RT-01 package and a scoped capstone proposal |
| 26–28 | ≈ 40 h | Capstone milestones M0–M5 and briefing | Capstone report, reproduction package, and briefing |

The plan is a route, not a contract. Each block assumes you complete the labs and one project rather than skim the reading; if a lab runs long, take the extra week and adjust the later blocks.

### If you have less time

- Choose a track rather than the full program. The Foundations track is a coherent course on its own.
- Protect the lab blocks. Cutting reading is survivable; cutting the lab turns the course into a reading list.
- Use the 1-3-7-21 review schedule even in a busy week; twenty minutes of retrieval preserves more than an hour of re-reading.
- Do not start a new module while the previous lab artifact is unfinished. The debt compounds.

### If you have more time

Do not compress the whole program into a month. Add depth instead: complete the optional challenge exercise for each module, run a second seed, attempt the adaptive attack, or write the capstone early and revise it as you learn more.

---

<a id="labs"></a>

## Working through a lab

The [lab guide](labs/index.md) lists the sequence, tiers, and standard artifact. This section covers how to do the work.

### Before

1. Read the threat model and metric definitions. If the threat model is missing, write one before writing code.
2. Write your prediction: expected clean performance, expected attack effect, expected failure mode.
3. Confirm the environment: activate the lab environment, print versions, set seeds.
4. Confirm the data path and checksum. Do not let a download failure masquerade as an attack failure.

### During

1. Run the notebook top to bottom once without edits. Record the result.
2. Change one variable at a time. Keep a table of settings and outcomes.
3. When a result looks too good, test the measurement before celebrating: zero perturbation, shuffled labels, a random baseline, a known-correct input.
4. When a result looks impossible, reduce to one batch and one step.
5. Record failures in the log as you go. You will not remember the exact error later.

### After

1. Restart the kernel and run all cells.
2. Re-run the headline result in a fresh process.
3. Score the artifact against the rubric.
4. Write the five-line reflection.
5. Commit the notebook, write-up, requirements, and manifest. Do not commit data or checkpoints.

### The lab write-up

Use the same structure every time:

| Section | Content |
|---|---|
| Threat model | Goal, knowledge, capability, access, budget, metric, and what is out of scope |
| Setup | Data, versions, hardware, seeds, and runtime |
| Method | What you did, with enough detail for another learner to repeat it |
| Results | Tables and figures with denominators, confidence intervals where relevant, and the baseline |
| Limitations | What the result does not show; one alternative explanation |
| Reproduction | The command or notebook path that regenerates the headline number |
| Reflection | Five lines, including what you misunderstood |

### Reporting a negative result

A negative result is a result. If an attack fails, a defense does not help, or a detection produces too many false positives, report it with the same rigor as a success: state the budget, the number of attempts, the baseline, and the most likely explanation. Do not tune until the story looks impressive and then hide the earlier runs.

### Self-review checklist

- [ ] The notebook runs from a clean kernel.
- [ ] Seeds and versions are recorded.
- [ ] Every metric has a stated denominator and budget.
- [ ] The clean or random baseline is present.
- [ ] The threat model matches the experiment actually run.
- [ ] At least one failure or limitation is reported.
- [ ] The manifest hashes match the artifacts.
- [ ] No personal data, credentials, or third-party target appears anywhere.

### Stop rule

If a lab exceeds 150% of its stated time, stop. Write down what you tried, the exact error, the smallest reproducer, and the question you would ask. That note is evidence of debugging skill. Continuing on exhaustion produces bad measurements and worse write-ups.

---

<a id="projects"></a>

## Working through a project

Level 5 projects are not larger labs. A lab asks you to execute a method and report a result. A project asks you to decide what deserves testing, prove that your test can fail, and defend a recommendation to an owner who cares about cost.

### Choose and scope

Use the [project catalog](projects/index.md) to pick one of PRJ-01…PRJ-06, or RT-01 if you want the red/blue format. Read the business objective and the data classification before the attack list. Write a one-page scope that names:

- the system, model version, and decision you are assessing;
- what is explicitly out of scope;
- the assets and their classification;
- the adversary profiles you will use;
- the two or three questions the project must answer;
- the artifacts you will deliver.

If the scope cannot fit in one page, it is not scoped yet.

### Budget the 11 hours

| Stage | Typical time | Output |
|---|---:|---|
| Scope, architecture, and data classification | 1.0 h | System diagram and asset table |
| Threat model and risk register | 1.5 h | Scored entries with dispositions |
| Test plan and baseline | 1.5 h | Falsifiable tests and baseline table |
| Attack or analysis experiments | 3.0 h | Tables, figures, and negative controls |
| Defense and adaptive retest | 3.0 h | Control evaluation with cost |
| Report, briefing, and package | 1.0 h | Findings, residual risk, reproduction |

Stop at 150% of the budget, as with a lab. A partial dossier with honest gaps is more useful than an unfinished experiment with no report.

### Evidence contract

Every project produces the same core: scope and authorization, architecture and data classification, threat model and register, test matrix, baseline table, experiment outputs, defensive evaluation, report with costed remediation and residual risk, a reproduction package, and a reflection. The project brief lists the exact files and acceptance criteria.

### How projects are scored

| Dimension | Weight | What strong work looks like |
|---|---:|---|
| Scope, system, and data understanding | 10 | One decision, explicit non-goals, correct asset classification |
| Threat model | 15 | Testable adversary profiles, anchored scores, dispositions for every entry |
| Baseline and experimental design | 15 | Frozen evaluation set, negative controls, uncertainty, falsifiable oracle |
| Attack or analysis correctness | 20 | Correct budgets, denominators, and metrics; no zero-budget artifact |
| Defense design and evaluation | 15 | Control tested statically and adaptively, with benign cost |
| Reproducibility and evidence | 10 | Clean-checkout run, pinned environment, hashed manifest |
| Risk communication | 10 | Severity tied to exposure, costed remediation, clear residual risk |
| Ethics, safety, and limitations | 5 | Authorized local target, no personal data, honest scope of claim |

A score of 3 (Proficient) on every dimension is the completion standard. The evaluator's reference explains typical findings and common failures; it is excluded from student navigation so that it does not replace your own analysis.

---

<a id="assessment"></a>

## Self-assessment and portfolio

### Weights

| Component | Weight | Notes |
|---|---:|---|
| Knowledge checks (QZ-00 to QZ-18) | 10% | Highest 16 of 19 scores; pass mark 80% per quiz; unlimited retakes |
| Labs and applied project (LAB-01 to LAB-20 including LAB-01B; one of PRJ-01…PRJ-06 or RT-01) | 40% | 16 labs required by the Practitioner track; one project required for the applied track; rubric-scored; lowest two lab scores may be dropped |
| Mini-projects (MP-01 to MP-04) | 20% | Choose any two; 8 hours each |
| Capstone (CAP) | 30% | Required for the Full track; rubric-scored |

### Assessment layer

The [assessments section](assessments/index.md) adds a 20-item diagnostic, an alternate quiz for every module, a 56-item tagged question bank, five level checks, and a 25-item integrated final. These are **self-scored retrieval and judgment checks**. They are not part of the weights above and they do not replace a lab artifact.

- Unsure of the baseline? Start with the [prerequisite diagnostic](assessments/diagnostic/index.md).
- Want a ten-item orientation? Use the [practice sampler](assessments/practice.md).
- Revising one module? Use its [alternate quiz](assessments/module-quizzes/index.md) after the module's own knowledge check.
- Preparing for a level or the capstone? Use the [level checks](assessments/level-checks/index.md) and the [final assessment](assessments/final-assessment/index.md).
- Scoring an artifact? Use the [lab](assessments/rubrics/lab-rubric.md), [project](assessments/rubrics/project-rubric.md), and [capstone](assessments/rubrics/capstone-rubric.md) rubrics, and record the result in the [progress record](assessments/progress-and-reflection.md).

Answer keys are separate files outside the site build. Attempt each assessment before opening them.

### Standard lab rubric

| Dimension | Weight | Exemplary (4) | Proficient (3) | Developing (2) | Insufficient (1) |
|---|---:|---|---|---|---|
| Technical correctness | 30 | Runs as specified; metrics correct; edge cases handled | Runs with minor omissions | Partially works; metric errors | Does not run or results invalid |
| Security reasoning | 25 | Explicit threat model, budgets, assumptions, limitations | Clear model with minor gaps | Vague model; overclaims | No threat model or misleading claims |
| Experimental method | 20 | Controlled comparisons, multiple seeds, uncertainty, ablations | Sound comparison, limited uncertainty | Single run or confounded comparison | Anecdotal |
| Reproducibility | 15 | Pinned environment, seeds, commands, manifest; clean-checkout reproduction | Reproduces with small fixes | Missing steps | Not reproducible |
| Communication and ethics | 10 | Concise; correct severity; safety and legal constraints addressed | Clear with minor issues | Disorganized or overlong | Unsafe or unprofessional |

### Self-assessment protocol

1. Attempt the lab without reading a reference solution.
2. Score your artifact against the rubric *before* viewing any solution or peer report.
3. Write the five-line reflection.
4. Re-run the headline result from a clean environment.
5. If a claim cannot be reproduced, mark the lab incomplete regardless of how good the write-up looks.

### Reflection template

```text
1. What worked:
2. What failed:
3. What I would test next:
4. What I misunderstood:
5. What evidence is missing:
```

### Competency levels

| Level | Definition | Evidence required |
|---|---|---|
| Aware | Can explain concepts and recognize attacks; can run guided labs | M00–M03; LAB-01, LAB-01B, and LAB-02; quizzes at 80% or above |
| Practitioner | Can execute and evaluate attacks and defenses with correct budgets and metrics | Aware plus M04–M11; LAB-03…LAB-15 (13 labs); two of MP-01 to MP-03 |
| Specialist | Can design assessments, handle frontier systems, and defend conclusions under adaptive pressure | Practitioner plus M12–M16; LAB-16 to LAB-20; MP-04; one of PRJ-01…PRJ-06 or RT-01; capstone at Proficient or above |
| Researcher | Can critique and extend the literature and design novel evaluations | Specialist plus M18 and a research-style capstone (CAP-B or CAP-E) with a methodological contribution and external review |

These levels describe capability, not accreditation. No university credit, professional certification, or license is conferred.

### Acceptable and unacceptable evidence

| Acceptable | Not acceptable |
|---|---|
| A notebook that runs end to end from a clean environment | Screenshots without the code that produced them |
| Metrics defined in code with denominators and budgets | "Robust" or "secure" without an adversary, budget, and metric |
| A threat model with explicit assumptions and a rejected alternative | Results copied from a tutorial without independent execution |
| A correctly measured negative result | Attack success reported without defining the base set |
| A mitigation evaluated against an adaptive attempt | A defense declared successful because one attack failed |
| Work on local, synthetic, or authorized targets | Any test against a system you do not own or have permission to test |

### Completion

The design defines a self-study completion record at 80% overall, all required labs submitted, one applied project at Proficient or above, a capstone at Proficient on every dimension, and a signed ethics statement. **No certificate is issued at this stage**, and no formal credit is implied.

---

<a id="troubleshooting"></a>

## Troubleshooting

Site-level problems — missing pages, search, mathematics that does not render, or keyboard navigation — are covered in [Troubleshooting](troubleshooting.md). This section covers the lab environment.

### The seven-step protocol

1. Reproduce the smallest failing case.
2. Check shapes, dtypes, ranges, device, and seeds.
3. Compare against a reference implementation on one batch.
4. Reduce to a subset and a single iteration.
5. Search the exact error text plus the library version.
6. Ask a precise question with a minimal reproducer.
7. If you are blocked for more than 90 minutes, switch to the theory and return with fresh eyes.

### Common problems

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Wrong environment | Activate the lab virtual environment; reinstall from the pinned file |
| CUDA error or no GPU | Driver and wheel mismatch | Use the CPU requirements; set the device explicitly to CPU |
| `torch` install is huge or slow | Default CUDA wheels | Install from the CPU-only wheel index |
| Dataset download fails (optional labs) | Network or proxy | Use the bundled-dataset lab path, or download manually and verify the checksum |
| Kaggle 401 or 403 | Missing API token or unaccepted terms | Configure the token; accept the dataset terms |
| Out of memory | Batch or model too large | Reduce batch size, use a subset, or enable mixed precision |
| Results differ between runs | Non-determinism | Set seeds, deterministic algorithms, `num_workers=0`, and pin versions |
| Attack "succeeds" at zero perturbation | Metric or label bug | Verify the perturbation norm and that predictions actually changed |
| Zero attack success | Underpowered attack or gradient masking | Increase steps and restarts; try a gradient-free attack |
| Notebook state is confusing | Out-of-order execution | Restart the kernel and run all cells |
| Colab disconnects | Session limit | Checkpoint artifacts to mounted storage |
| AutoAttack takes hours | Full test set | Use a fixed subset and document it |
| Server returns `401` for a demo token | Missing or malformed header | Send `Authorization: Bearer <token>` and check the token's role |
| Every request returns `429` | Fixed-window limiter exhausted | Wait for the window to reset; LAB-14 allows 10 requests per 60 seconds per role |
| A validation rule rejects good rows | Boundary error or unit mismatch | Print the failing values and compare with the documented rule before widening it |
| Flower version errors | API drift | Pin the version used by the lab |
| Opacus rejects a layer | Unsupported module | Replace the layer or compute per-sample gradients manually |
| `pip` resolver conflict | Mixed environments | Create a fresh virtual environment and install from the lockfile |
| Windows path too long | Legacy path limit | Enable long paths or use WSL2 |
| Attack loop is slow on CPU | Too many rows or iterations | Use a fixed subset, reduce steps, and record the trade-off |

### Reset an environment

If an environment is beyond repair, do not patch it blindly:

```bash
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `requirements.txt` is missing, that is the real bug: the lab was not packaged reproducibly.

### Asking for help

Include:

- the exact command you ran;
- the full error, not a paraphrase;
- Python, library, and OS versions;
- a minimal reproducer or the smallest notebook cell that fails;
- what you expected and what happened;
- what you already tried.

A question with these six items usually gets a useful answer. A screenshot of a traceback without the command rarely does.

---

<a id="faq"></a>

## FAQ

**Do I need a GPU?** No. The course is CPU-first. Tier A labs target ten minutes or less per run, and Tier B labs ship a reduced CPU configuration. A GPU only shortens some optional runs.

**Is this course free?** The course materials are designed around free and open-source tools and public datasets. Every published lab runs with the shared Level 1 requirements; no dataset purchase or service account is required. Licensing for the course content itself is still an owner decision.

**Is there a certificate?** Not at this stage. The design defines a self-study completion record, but no certificate is issued and no accreditation is implied.

**Are solutions available?** Built labs ship reference implementations and checking guides inside their folders, outside student navigation. The owner has not set a public solutions policy beyond that.

**Can I start a module that is not published yet?** All modules M00–M18 are published. The remaining work is maintenance, not missing content. If a link or claim is wrong, report it as an issue.

**Can I skip modules?** Yes, through the entry paths in the [roadmap](modules/index.md#entry-paths). The capstone assumes foundational vocabulary, so read the threat-model sections of anything you skip.

**How much math do I need?** Gradients, the chain rule, basic probability, and norms. You should be able to explain an L-infinity ball and differentiate cross-entropy for a linear layer. The recovery path covers this.

**Does this work on Windows?** Yes. Tier A labs run natively. A few container labs are easier under WSL2, and legacy path-length limits can affect deep virtual environments.

**How long does the full program take?** About 276 hours including the capstone. At 6–10 hours per week, that is roughly 7–11 months, including review and slippage.

**Do I have to complete a project before the capstone?** It is strongly recommended. A project is an 11-hour rehearsal of the assessment method in a smaller system; RT-01 adds the red/blue format. The capstone assumes you have already produced one traceable dossier.

**Is this a university course?** It is a self-study course written by a university professor, designed for independent learners. It is not currently offered for credit, and no enrollment or examination is implied.

**Can I use ChatGPT, Claude, or another assistant?** Yes, within the policy below. Disclose material assistance and verify every factual claim and every line of attack code.

**Can I teach this to a cohort?** The materials are designed to support a facilitated cohort, but licensing and contribution terms are not settled. Ask the repository owner before organizing a public cohort.

**How do I report an error?** Open an issue in the [repository](https://github.com/nadeem-majeedch/MLSec) with the page, the claim, and the evidence. Do not include personal data or unpatched vulnerability details in a public issue.

**Why are the frameworks dated?** NIST, MITRE, OWASP, and tool versions change. Every framework claim carries a version and date so you can tell whether it is still current. Re-verify before citing it in your own work.

---

<a id="ai-policy"></a>

## Using AI assistants

Assistants are useful and unreliable in predictable ways. They are good at explaining an error, proposing a test, or reviewing a threat model. They are unreliable for exact API signatures, dataset availability, and citations.

| Allowed | Not allowed for graded artifacts | Required | Never |
|---|---|---|---|
| Asking for an explanation, a debugging hint, a code review, or a test idea | Submitting analysis you cannot defend line by line | A short "Tools used" note: tool, purpose, what you verified | Pasting private, proprietary, or restricted data into a third-party assistant |
| Generating a small example to compare against your own | Fabricating results or copying another learner's report | Verification of every factual claim and citation | Using an assistant to attack systems you do not own |
| Rewriting your own explanation for clarity | Letting an assistant write the threat model or conclusions for you | Independent execution of every experiment | Treating a confident answer as evidence |

A useful disclosure note looks like this:

> **Tools used.** I used an AI assistant to explain a `RuntimeError` about tensor shapes and to suggest a unit test for the projection step. I verified the fix by re-running the attack and comparing against the reference implementation. The analysis and conclusions are my own.

The standard is simple: if you cannot explain and defend a line, it does not belong in your artifact.

---

<a id="safety"></a>

## Responsible use and law

The techniques in this course are published research. Learning them is legitimate. Using them against systems you do not own is not.

- **Authorized targets only.** Use local processes, local containers, synthetic services, or explicitly public sandbox datasets.
- **No real personal data.** Use public benchmarks or synthetic records. Do not attempt re-identification.
- **Contain offensive code.** Run artifact and agent labs in a disposable container or VM with no host credentials and no network egress unless required.
- **Responsible disclosure.** Report real vulnerabilities privately, allow reasonable remediation time, and do not publish an exploit before a fix.
- **Law and policy.** Follow applicable law, institutional policy, and terms of service. This is not legal advice.
- **Harm minimization.** Do not generate targeted disinformation, impersonation, or content harmful to real people.

### Authorized-use statement

Every project, the red/blue exercise, every capstone, and every lab that touches a service should include a statement like this, adapted to the work:

> I, **[name]**, confirm that I own or have written permission to test **[system]**, that all targets are local, synthetic, or public sandboxes, that I will use no real personal data, that I will not disrupt third-party services, and that I will follow coordinated disclosure for any real vulnerability I find.

If you cannot sign that statement honestly, stop. The lab is not worth the risk.

---

<a id="incomplete"></a>

## Publication status and extension work

Levels 1–5 are complete: M00–M18, LAB-01…LAB-20, six project briefs, RT-01, and the capstone brief with milestones and rubric. No module page is an empty placeholder.

What remains is maintenance and optional extension, not missing student content:

1. **Deploy the site.** The owner has not approved a public deployment. Until then, build locally with MkDocs.
2. **Re-verify external references.** Framework versions, paper links, and tool documentation change. Re-check them before citing them in your own work.
3. **Add learner evidence carefully.** Worked examples can help, but a full solution set would weaken projects that depend on independent analysis. The evaluator's reference is excluded from student navigation.
4. **Keep the portfolio.** Store the artifact, write-up, requirements, manifest, and reflection in one folder per lab or project. The capstone reuses them.
5. **Track maintenance.** The [implementation roadmap](implementation-roadmap.md) lists completed slices and the remaining quality gates.

If a page is wrong, a citation is broken, or a claim is unsupported, report it as an issue. Corrections are more valuable than new content at this stage.

---

## Where to go next

- [Course roadmap](modules/index.md) — every module, prerequisite, and outcome.
- [Assessments](assessments/index.md) — diagnostic, alternate quizzes, level checks, final, question bank, and rubrics.
- [Labs](labs/index.md) — sequence, tiers, rubric, and safety.
- [Projects](projects/index.md) — six applied projects, RT-01, and selection guidance.
- [Capstone](projects/capstone.md) — requirements, milestones, rubric, and research route.
- [References](references.md) — frameworks, papers, and benchmarks.
- [Glossary](glossary.md) — plain-language definitions with links to the lesson that teaches each term.
- [Framework mapping](framework-mapping.md) — how modules and labs map to NIST, ATLAS, and OWASP categories.
- [Research reading guide](research-reading-guide.md) — reading order and what to extract from each paper.
- [Dataset catalog](dataset-catalog.md) — origins, licenses, limitations, and download steps.
- [Learning outcomes](learning-outcomes.md) — the full 35-outcome catalog.
- [Repository](https://github.com/nadeem-majeedch/MLSec) — source and issue tracker.
