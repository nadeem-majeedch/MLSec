---
title: Module 00 — How to Use This Self-Study Course
---

# Module 00 — How to Use This Self-Study Course

<a id="m00-start"></a>

**Level 1 · Foundations · 4 hours · No prerequisites**

## Why this module exists

A learner clones a repository, opens a notebook, and gets 97% accuracy on the first try. Two weeks later they cannot reproduce the number, cannot explain which rows were used for training, and cannot say whether the result means anything. Nothing was learned that survives contact with a real system.

This module prevents that outcome. It explains what the course is for, how every module is built, what counts as evidence, and which rules keep your work lawful and safe.

## Real-world motivation

A number without a provenance trail is not evidence. Teams regularly discover that a reported metric cannot be reproduced because the split changed, a package version drifted, or a file was edited after the run. The cost is a retracted result, a failed audit, or a model deployed on a flawed evaluation. The same failure appears in security work: a threat model that lists technologies instead of assets and attacker goals gives no one a decision to act on.

You do not need an instructor for this course. You need a system. This module is the system.

## What this module is for

ML-Sec is a self-study, lab-driven course. There are no lectures to attend and no one will check your homework. The course therefore gives you:

- **A repeatable study loop** — preview, read, practice, lab, retrieve, reflect.
- **An evidence standard** — a claim is credible when another person can reproduce it from your artifact.
- **A safety contract** — every offensive technique is practised on local, synthetic, or explicitly public targets.
- **A portfolio** — each module ends with an artifact that later modules reuse.

This module has three lessons, one short environment lab, a knowledge check, and three exercises. It is the smallest module in the course and the one most likely to be skipped. Do not skip it.

## Measurable learning objectives

By the end of this module you will be able to:

1. **Distinguish** adversarial ML, application security, and AI safety, and classify a described incident into the right category with a stated asset and adversary (Bloom 2–3).
2. **Set up and verify** a reproducible Python environment on a laptop CPU, recording interpreter, package, and operating-system versions (Bloom 3).
3. **Create an artifact manifest** that detects a modified file using SHA-256 hashes (Bloom 3).
4. **Apply** the course's authorized-use test to a described request and reach an allow, ask, or deny decision with reasons (Bloom 3).
5. **Produce** a 12-week study plan and a signed ethics and authorized-use statement (Bloom 3–4).

Each objective is assessed by an exercise or the lab, not by reading this page.

## Prerequisite checklist

| Requirement | Minimum | Check |
|---|---|---|
| Computer | 8 GB RAM, 10 GB free disk, 64-bit OS | You can install Python packages and run a script for 10 minutes |
| Terminal | Create a directory, change directory, run a command | `python --version` works in a terminal |
| Python | Variables, functions, lists, dictionaries, `import` | You can read a 30-line script without help |
| Files | Relative and absolute paths | You can explain the difference between `data.csv` and `/home/me/data.csv` |
| Time | 4 hours for this module | You can protect two 2-hour blocks |
| Network | Ability to download packages once | `pip` can reach a package index, or you have a local mirror |
| Accounts | None | No paid cloud account, GPU, or API key is required |

If Python is the weak row, read [Module 01](../m01-python-refresher/index.md) first and return here for Lesson 3. If terminal basics are weak, complete the four-week recovery path in the [student guide](../../student-guide.md#baseline) before LAB-01.

## Module map

| Unit | Title | Format | Time |
|---|---|---|---:|
| [00.1](lesson-1-what-ml-security-is.md) | What ML security is — and is not | Lesson | 45 min |
| [00.2](lesson-2-lab-and-evidence.md) | Your lab, your evidence | Lesson | 60 min |
| [00.3](lesson-3-rules-of-engagement.md) | Rules of engagement | Lesson | 45 min |
| [LAB-01](../../labs/lab-01.md) | Reproducible environment and baseline pipeline | Lab (shared) | 3 h, counted in M01 |
| [Knowledge check](quiz.md) | QZ-00, 10 items | Self-graded | 20 min |
| [Exercises](exercises.md) | Environment report, authorization scenario, study plan | Practice | 60 min |
| [Artifact](exercises.md#artifact) | Environment report, ethics statement, 12-week plan | Portfolio | — |

The lab is shared with Module 01: Module 00 installs and verifies the environment, and Module 01 supplies the data and modelling concepts that LAB-01 uses. Its 3 hours are counted under Module 01, so this module totals 2.5 h of lessons + 1.5 h of quiz and exercises ≈ 4 h.

## How every module works

Each module follows the same anatomy:

> **Scenario → objectives → lessons → lab → quiz → reflection → artifact**

Each lesson follows the same six-step protocol:

| Step | What you do | Why |
|---|---|---|
| 1. Scenario | Read the failure story and name the asset at risk | Security work starts with something worth protecting |
| 2. Objectives | Turn "read about X" into "be able to do Y" | You can tell whether you are finished |
| 3. Concept | Read one explanation and restate it in your own words | Recognition is not understanding |
| 4. Guided practice | Run the example, change one input, predict the effect | Debugging exposes gaps that reading hides |
| 5. Check | Answer the knowledge check before opening the answers | Retrieval is what builds durable memory |
| 6. Artifact | Finish the lab and write a five-line reflection | The portfolio is the evidence |

### The evidence standard

A result is **acceptable evidence** when:

- the code runs end to end from a clean environment;
- seeds and versions are recorded;
- the metric has a stated denominator and budget;
- the artifact includes hashes or a manifest;
- limitations and negative results are reported.

A screenshot without the code, a copied tutorial number, or the word "robust" without a threat model is **not** evidence. The full standard is in [Learning outcomes](../../learning-outcomes.md#6-what-counts-as-acceptable-evidence).

### Course identifiers

| Prefix | Meaning | Example |
|---|---|---|
| `Mxx` | Module | `M03` |
| `Mxx.Ly` | Lesson | `M03.L4` |
| `LAB-xx` | Lab | `LAB-01B` |
| `QZ-xx` | Knowledge check | `QZ-02` |
| `LO-xx` | Learning outcome | `LO-03` |
| `MP-xx` | Mini-project | `MP-01` |
| `CAP-x` | Capstone option | `CAP-A` |

Identifiers are stable. `LAB-01B` is an added lab that sits between LAB-01 and LAB-02; it was not renumbered because the other lab IDs are already referenced throughout the course.

## What you produce

By the end of Module 00 you will have:

1. **An environment report** — OS, Python, package versions, and a successful verification run.
2. **A signed ethics and authorized-use statement** — the rules you will follow for every lab.
3. **A 12-week study plan** — which modules, which weeks, and which artifacts.

These are the first entries in your portfolio. LAB-01 adds the baseline model and manifest. No artifact in this course is graded by an instructor; you score it against the published rubric and keep it for the capstone.

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Skipping Module 00 to "get to the attacks" | Attacks without threat models; unsafe habits; unreproducible results | Spend the four hours; the rest of the course depends on it |
| Treating the course as a reading list | You recognize techniques but cannot execute or evaluate them | Budget lab time equal to or greater than reading time |
| Installing packages globally | Version conflicts; labs break between modules | One virtual environment per lab or per level |
| Saving screenshots instead of artifacts | Claims cannot be checked | Save code, config, metrics, and hashes |
| Using a personal cloud account "just for one lab" | Cost, data exposure, non-reproducible setup | Every Level 1 lab runs on a laptop CPU with no account |
| Treating a public model API as a practice target | Terms-of-service and legal risk | Use local replicas or explicitly public sandboxes |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `python` is not recognized | Python is not on `PATH` | Reinstall with "Add Python to PATH", or use `py -3`; reopen the terminal |
| `pip install` cannot reach the index | Proxy, firewall, or offline machine | Use your organization's mirror, or download wheels once and install from the local folder |
| Activating `.venv` is blocked in PowerShell | Execution policy | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for that shell only |
| A manifest hash does not match | A file changed after hashing | Re-run the manifest step; never hand-edit an artifact |
| Predictions differ after reload | Hidden notebook state or a missing seed | Restart the kernel, run all cells, and follow [Lesson 00.2](lesson-2-lab-and-evidence.md#troubleshooting) |

More environment fixes are in [Lesson 00.2](lesson-2-lab-and-evidence.md#troubleshooting).

## Glossary

| Term | Working definition |
|---|---|
| **Adversary** | A person or process that deliberately causes an ML system to fail or misbehave |
| **Asset** | Something of value: data, model weights, predictions, availability, reputation, privacy |
| **Attack surface** | The set of inputs and interfaces an adversary can influence or observe |
| **Trust boundary** | A line where data or control passes between parties with different privileges or assumptions |
| **Threat** | A potential event that could harm an asset |
| **Vulnerability** | A weakness that makes a threat possible |
| **Exploit** | A concrete method that turns a vulnerability into an effect |
| **Risk** | Likelihood and impact of harm, usually combined with a stated scoring method |
| **Artifact** | A file produced by your work: model, config, metrics, notebook, report |
| **Manifest** | A file listing artifact names, sizes, and cryptographic hashes |
| **Reproducibility** | Another person can obtain the same result from your instructions and inputs |
| **Authorized target** | A system you own or have explicit written permission to test within a defined scope |

## Summary and key takeaways

- ML security is a discipline of **model, measure, defend, re-test**, not a catalogue of attacks.
- Self-study works when it has a **system**: a study loop, an evidence standard, and a portfolio.
- Every result must be reproducible from a **clean environment** with recorded versions and seeds.
- Every offensive action must be **authorized, scoped, and safe**; local and synthetic targets are the default.
- Module 00 is small but sets the rules that make Modules 01–17 trustworthy.

## References and further reading

All links were checked on 2026-10-28.

| Reference | Why it matters here |
|---|---|
| [NIST AI 100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | The taxonomy of adversarial ML used throughout the course |
| [MITRE ATLAS](https://atlas.mitre.org/) | Adversary tactics and techniques; data release v2026.09 |
| [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) | Risk-management functions used in Module 03 |
| [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | Application-facing risk list for generative systems |
| [Python virtual environments](https://docs.python.org/3/library/venv.html) | The setup mechanism used in Lesson 2 and LAB-01 |
| [Git documentation](https://git-scm.com/doc) | Local version control without a remote |

## Next step

Start with [Lesson 00.1 — What ML security is, and is not](lesson-1-what-ml-security-is.md). Then set up your environment in Lesson 00.2, complete Lesson 00.3, and run [LAB-01](../../labs/lab-01.md).
