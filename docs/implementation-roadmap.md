# ML-Sec Implementation Roadmap

| Field | Value |
|---|---|
| Document | Staged plan for building the course, site, and labs |
| Version | 0.6 (Levels 1–5 implemented) |
| Date | 2026-10-28 |
| Status | Levels 1–5 (M00–M18, LAB-01…LAB-20, PRJ-01…PRJ-06, RT-01, capstone brief) **implemented and locally verified**; no commit, push, or deployment performed |
| Companion documents | [Course blueprint](course-blueprint.md) · [Module map](module-map.md) · [Lab catalog](lab-catalog.md) · [Project catalog](project-catalog.md) · [Learning outcomes](learning-outcomes.md) |

## 1. Current state (2026-10-28)

| Item | Finding | Implication |
|---|---|---|
| Local working directory | Contains the written course and lab code; **not a Git repository** | Work is file-based; nothing has been committed from this workspace |
| Remote repository | `nadeem-majeedch/MLSec` was public and empty at the Phase 0 audit (no commits, no branches, no workflows) | No history to preserve or conflict with; owner controls the first commit |
| GitHub Pages | Not verified to be serving this site; the Phase 0 audit found the Pages URL returning 404 | Treat deployment as unconfigured until the owner enables and verifies it |
| GitHub Actions | No workflow files in this workspace | CI remains an owner/infrastructure task |
| Published content | M00–M18 (88 lessons plus module indexes, quizzes, exercises, and answer keys); LAB-01…LAB-20 lab packages and briefs; six project briefs, RT-01, and the capstone brief | Levels 1–5 learning paths and the assessment track are usable offline |
| Planning documents | Blueprint, module map, lab catalog, project catalog, learning outcomes, and this roadmap at version 0.6 | All totals describe the same 18-module + capstone structure |

**What this means.** The course is a locally built content tree, not a released product. No Git history, remotes, settings, issues, or Pages configuration have been changed by this work.

## 2. Implementation principles

1. **Vertical slices, not horizontal stubs.** Publish a complete module (lessons + lab + quiz + artifact) before starting the next. Empty placeholder lessons are prohibited.
2. **Lab-first quality.** If the lab cannot be reproduced from a clean environment on a reference machine, the module is not done.
3. **Cite or reproduce.** Every technical claim is backed by a verified reference or a measured result in the lab.
4. **Pin and date.** Pin tool versions; date framework versions ("ATLAS as of 2026-10", "OWASP LLM 2026", "NIST AI 100-2e2025").
5. **Safety gate.** Any lab that deserializes or executes untrusted content runs in a disposable container with no host credentials and no egress by default.
6. **Separate audiences.** Learner content lives in `docs/`; deployment and maintenance instructions live in the maintainer guide and are not published in student navigation.
7. **No publishing by the agent.** Commits, pushes, Pages changes, and repository settings are owner actions.
8. **Modest compute.** Labs default to NumPy/scikit-learn on CPU; specialized libraries appear only where they materially improve the lesson.

## 3. Build slices

The course is produced in ten vertical slices. A slice is complete only when its pages, labs, projects, and checks pass together.

| Slice | Scope | Status | Gate |
|---|---|---|---|
| 1 | M00 + M01 + LAB-01 | **Published** | Deterministic baseline; site builds; manifest verified |
| 2 | M02 + M03 + LAB-01B + LAB-02 | **Published** | Evaluation audit and threat-model checker pass |
| 3 | M04 + LAB-03 + LAB-04 | **Published** | FGSM/PGD/targeted results reproduce within stated tolerance |
| 4 | M05 + M06 + LAB-05…LAB-08 + MP-01 brief | **Published** | Poisoning and backdoor metrics, screening, and false-positive counts reproduce |
| 5 | M07 + LAB-09 + LAB-10 + MP-03 part 1 | **Published** | Extraction fidelity and low-FPR membership metrics reproduce |
| 6 | M08 + M09 + LAB-11 + LAB-12 + MP-02 brief | **Published** | Defense evaluation under adaptive attack; dataset validation catches defects with measured false positives |
| 7 | M10 + M11 + LAB-13…LAB-15 | **Published** | Supply-chain, serving, and monitoring controls verified by negative tests and a replayable incident |
| 8 | M12 + M13 + M14 + M15 + LAB-16…LAB-20 + MP-03 part 2 + MP-04 | **Published** | Federated, privacy, explanation/fairness, RAG, and agent labs are local-only and checker-verified |
| 9 | M16 + M17 + M18 + PRJ-01…PRJ-06 + RT-01 + QZ-16…QZ-18 | **Published** | Every project traces threats to tests to evidence; RT-01 measures red and blue from the same timeline |
| 10 | Capstone brief (CAP-A…CAP-F) + evaluator guide + project catalog + QA | **Published** | Every outcome has a published assessment and a rubric; strict build and link check pass |

Each slice ends with a site build, an internal link check, and a reproducibility test of its labs from a clean environment. A failed check blocks the next slice.

## 4. Milestones

| Milestone | Content | Gate | State |
|---|---|---|---|
| M0 | Planning baseline | Five planning documents reviewed and consistent | Met at v0.3 |
| M1 | Site builds | `mkdocs build --strict` passes; internal links resolve | Met locally for Levels 1–4 |
| M2 | Foundations | M00–M03 + LAB-01/01B/02 complete and checker-verified | Met |
| M3 | Core attacks (Level 2) | M04–M07 + LAB-03…LAB-10 complete and checker-verified | Met locally |
| M4 | Defenses and data integrity (Level 3, part 1) | M08–M09 + LAB-11–LAB-12 complete and checker-verified | Met locally |
| M5 | Secure engineering and operations (Level 3, part 2) | M10–M11 + LAB-13…LAB-15 complete and checker-verified | Met locally |
| M6 | Distributed, private, and frontier systems (Level 4) | M12–M15 + LAB-16…LAB-20 complete and checker-verified | Met locally |
| M7 | Applied projects and synthesis (Level 5) | M16–M18 + six project briefs + RT-01 + capstone brief complete; catalogs updated | Met locally |
| M8 | Public v1.0 | Owner licensing, Pages enablement, CI, external review, release notes | Not started |

## 5. Slice detail

### Slice 1 — Foundation (M00, M01, LAB-01) ✅

**Deliverables.** Orientation lessons, Python/NumPy/pandas/scikit-learn lessons, reproducible digits baseline lab, shared artifact helpers.
**Exit criteria met.**
- LAB-01 runs offline (scikit-learn bundled digits), writes a manifest, and reproduces its metrics from a fresh process.
- LAB-01 scores 0.9583 test accuracy and 0.9577 macro F1 within ±0.005 as documented in the lab brief.
- The shared `labs/shared/mlsec_labs` package builds manifests and environment records used by all later labs.

### Slice 2 — Evaluation and threat modeling (M02, M03, LAB-01B, LAB-02) ✅

**Deliverables.** Evaluation and leakage lessons, threat-model lessons, evaluation-audit lab, threat-model lab and checker.
**Exit criteria met.**
- LAB-01B reproduces the leaky and repaired churn results and requires a threshold chosen on validation data.
- LAB-02's checker enforces asset, boundary, surface, severity, control, and crosswalk coverage; the starter fails with a specific error.
- Framework mappings use allowlisted ATLAS technique IDs rather than invented ones.

### Slice 3 — Evasion (M04, LAB-03, LAB-04) ✅

**Deliverables.** Five evasion lessons, ε-sweep lab, targeted/transfer lab, quiz and exercises.
**Exit criteria met.**
- LAB-03 reports clean accuracy and ASR for FGSM and PGD at four budgets, with clipping and sign checks.
- LAB-04 separates source and target models and reports targeted and untargeted success at three budget levels.
- Base sets are the clean-correct rows; ASR denominators are explicit.

### Slice 4 — Integrity (M05, M06, LAB-05…LAB-08, MP-01) ✅

**Deliverables.** Poisoning and backdoor lessons, label-poisoning lab, targeted-poisoning lab, tabular backdoor lab, image backdoor detection lab, MP-01 brief.
**Exit criteria met.**
- LAB-05 reports accuracy and macro F1 by poison count with an explicit poison-rate denominator.
- LAB-06 reports targeted success before and after screening, including caught poisons and clean false positives.
- LAB-07 reports clean accuracy, attack success, and false-trigger rate for clean, backdoored, and defended models.
- LAB-08 reports a trigger scan, clean-model false positives, and a mitigated model's clean and triggered behavior.

### Slice 5 — Extraction and privacy (M07, LAB-09, LAB-10, MP-03 part 1) ✅

**Deliverables.** Five extraction/privacy lessons, extraction lab, membership-inference lab, quiz and exercises.
**Exit criteria met.**
- LAB-09 reports teacher accuracy, fidelity, and student accuracy at four query budgets for random and active sampling.
- LAB-10 reports ROC-AUC, TPR at FPR ≤ 1% and ≤ 5%, mean confidence gap, and a hard threshold, and requires an explicit "confidence is not proof" argument.
- Both labs use local models and public digits data only.

### Slice 6 — Defenses and data integrity (M08, M09, LAB-11, LAB-12, MP-02) ✅

**Deliverables.** Six robustness lessons, five data-integrity lessons, LAB-11 defense evaluation, LAB-12 dataset validation, quizzes and exercises, MP-02 brief.
**Exit criteria met.**
- LAB-11 reports clean and robust accuracy for the undefended model, adversarial training, and input squeezing at ε = 0.10, a stress budget at ε = 0.20, and a naive-versus-adaptive attack comparison; the report states that no universal defense follows.
- LAB-12 finds and counts every planted defect class, reports false positives, removes the post-outcome column, and isolates its effect with a same-rows ablation.
- Both labs use local, synthetic or bundled data and run on CPU in under ten minutes.

### Slice 7 — Secure engineering and operations (M10, M11, LAB-13…LAB-15) ✅

**Scope.** Supply chain (4 lessons), serving, monitoring, and response (6 lessons); LAB-13 supply-chain audit, LAB-14 secure serving, LAB-15 monitoring and incident response.
**Exit criteria met.**
- LAB-13 includes a negative test that fails the gate, a verified signature and SBOM, and a static pickle scan that never executes the canary.
- LAB-14's 18 auth, quota, body, validation, error, and logging cases fail closed; tokens and payloads do not appear in logs.
- LAB-15 reconstructs its detectors from the logs, separates benign drift from an evasion campaign, rejects a rollback to an equally vulnerable checkpoint, and measures a mitigation with its clean cost.
- No lab payload reaches the network or uses host credentials.

### Slice 8 — Distributed, private, and frontier (M12–M15, LAB-16…20, MP-04) ✅

**Scope.** Federated learning (5 lessons), privacy-preserving ML (5 lessons), explainability and fairness (4 lessons), generative AI/RAG/agents (6 lessons); LAB-16 FL attack and defense, LAB-17 privacy budget and utility, LAB-18 explanation stability and subgroup audit, LAB-19 RAG trust boundary, LAB-20 agent containment.
**Exit criteria met.**
- FL defenses are compared at equal rounds with clean accuracy and ASR both reported and secure-aggregation claims scoped.
- The privacy lab states sensitivity and composition, reports utility and an MIA signal, and does not treat the empirical signal as a proof.
- The explainability lab reports subgroup intervals and explanation stability under bounded noise, and names the trade-offs.
- LLM and agent labs use local synthetic content, benign canaries, mock tools, and no external services.
- Agent controls are enforced in code; the action log records attempted, blocked, and succeeded actions.
- Every lab is independently checker-verified from a clean process.

### Slice 9 — Applied projects (M16–M18, PRJ-01…PRJ-06, RT-01) ✅

**Scope.** Integrated-assessment lessons (4), red/blue lessons (4), capstone-planning lessons (4); six 11-hour project briefs with staged tasks, required experiments, deliverables, acceptance criteria, rubrics, and reflection; RT-01 rules of engagement, red plan, blue detection plan, and purple-team synthesis.
**Exit criteria met.**
- Every project brief states a fictional organization, system architecture, data classification, trust boundaries, adversary capabilities, staged tasks, required experiments, deliverables, acceptance criteria, 100-point rubric, reflection questions, and extensions.
- Each brief names the local toy system it uses, the synthetic or bundled data, and what must not be targeted.
- Every required test traces to a threat-model entry with a stated budget, oracle, metric, and evidence path.
- RT-01 includes written authorization, stop conditions, quiet-traffic baselines, detection calibration, containment evidence, and an adaptive retest.
- Evaluator guidance is separated from student pages so the project is not reduced to an answer key.
- All content is local-only: no external services, real credentials, or personal data.

### Slice 10 — Capstone and release (CAP + QA) ✅ (brief published)

**Scope.** Capstone guide and six option briefs; assessment pages; project catalog; full QA; accessibility; release notes (owner action).
**Exit criteria.**
- Every LO has a mapped assessment with a published rubric.
- Six capstone options have briefs, milestones, progress self-assessment, and a research-extension path.
- Full link check, strict build, accessibility audit, and clean-environment reproduction of all Tier A labs. *Build and link check run locally at this milestone; accessibility and clean-environment reproduction remain open review items.*
- Versioned framework note ("as of" dates) on reference pages.
- Release notes list known limitations and the next review date. *Owner action; not performed.*

## 6. Technical implementation details

### 6.1 Site configuration

`mkdocs.yml` is the single source of truth for navigation. It uses Material, search, code copy, arithmetic and Mermaid fences, and a `not_in_nav` block for planning documents, the maintainer guide, the project catalog, the evaluator guide, quiz answers, and exercise solutions. Nav entries are added only for pages that exist; `mkdocs build --strict` fails on broken entries.

```yaml
site_name: Machine Learning Security (ML-Sec)
site_url: https://nadeem-majeedch.github.io/MLSec/
repo_url: https://github.com/nadeem-majeedch/MLSec
docs_dir: docs
theme:
  name: material
  features:
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - content.code.copy
plugins:
  - search
nav:
  - Home: index.md
  - Student guide: student-guide.md
  - Course roadmap: modules/index.md
  - "Level 1 — Foundations": ...   # M00–M03
  - "Level 2 — Core attacks": ...  # M04–M07
  - "Level 3 — Defenses and secure engineering": ...  # M08–M11
  - "Level 4 — Advanced and emerging security": ...  # M12–M15
  - "Level 5 — Applied security projects": ...      # M16–M18
  - Labs: ...                      # LAB-01…LAB-20 published
  - Projects: ...                  # PRJ-01…PRJ-06, RT-01, capstone, catalog
  - References: references.md
```

### 6.2 CI outline (not yet added)

| Workflow | Trigger | Steps | Failure policy |
|---|---|---|---|
| `ci.yml` | PR, push | checkout → Python 3.14 → install pinned MkDocs → `mkdocs build --strict` → internal link check → lab smoke tests | Blocks merge |
| `pages.yml` | Push to `main` | build → upload artifact → deploy Pages | Deploy only if build passes |
| `labs.yml` | Weekly + manual | CPU smoke tests for a rotating sample of labs | Opens an issue; does not block docs |

Permissions: `contents: read`; the Pages job adds `pages: write` and `id-token: write`. No repository secrets are required for the docs build. Lab tests must not use credentials.

### 6.3 Content production pipeline

1. **Citation sheet** — collect official docs and papers; record version/date/URL.
2. **Outline** — map sections to LO IDs and quiz items.
3. **Draft** — lesson text with a worked example; no unexplained jargon.
4. **Lab** — implement in `labs/`, run clean, measure runtime.
5. **Quiz** — items with explanations and misconception tags.
6. **Review** — ML reviewer + security reviewer; check claims, budgets, and limitations.
7. **Editorial/accessibility** — alt text, headings, plain language, link check.
8. **Publish** — add nav entry only now; update changelog.

### 6.4 Lab conventions

Every lab directory contains `README.md`, `starter.py`, `solution.py`, `check_*.py`, `expected_metrics.json`, `requirements.txt`, and `CHECKING.md`. Labs emit `metrics.json`, `run.json`, `report.md`, and `manifest.json`. The starter must fail loudly and the checker must reject an incomplete artifact.

### 6.5 Repository hygiene

- `.gitignore`: virtualenvs, `data/`, model checkpoints, notebook checkpoints, `site/`, `.env`, `__pycache__/`.
- Large artifacts: never commit; use download scripts or release assets (owner decision).
- Commit messages: imperative, scoped (`docs(m04): add PGD lesson`), no secrets.
- Branching: short-lived branches; PR review for every lesson and lab.

## 7. Owner actions (cannot be performed by the agent)

| # | Action | Why | When |
|---|---|---|---|
| 1 | Confirm repository access and create the initial commit | Workspace is not a Git repository | Before any release |
| 2 | Enable GitHub Pages with source **GitHub Actions** | Deployment is unverified | Before first public release |
| 3 | Choose licenses for content and code | Legal reuse terms are undefined | Before any publication |
| 4 | Provide instructor bio, photo, and contact policy | About page must not invent details | Before first public release |
| 5 | Decide solutions policy (public, gated, or private) | Affects assessment integrity | Before publishing solutions |
| 6 | Approve analytics/privacy posture | Default is no analytics | Before v1.0 |
| 7 | Approve brand/navigation | Site identity | Before first public release |

## 8. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Deployment remains unconfigured | Medium | High (no site) | Owner enables Pages; verify URL before announcing |
| No license | High (currently none) | High | Owner decision before any publication |
| Framework drift | High | Medium | Date every framework; quarterly review; pin versions in labs |
| Lab breakage from dependency updates | High | Medium | Lockfiles, CI smoke tests, deprecation policy |
| Dataset access changes | Medium | Medium | Digits are the primary dataset; fallbacks documented per lab |
| Compute disparity | High | Medium | CPU tiers, subsets, reference hardware and tolerances |
| Offensive-content misuse | Low | High | Sandbox-only, authorized-use statement, safety review gate |
| Breadth overwhelms learners | Medium | High | Tracks, explicit minimum paths, 88-lesson/84-hour lab cap, and one 11-hour project rather than all six |
| Citation errors | Medium | High | Verified reference list; "cite or reproduce" rule; review gate |
| Solution leakage | Medium | Medium | Solutions and the evaluator guide outside nav; owner policy |
| Assessment drift between brief and rubric | Medium | Medium | Project catalog is the single inventory; rubric dimensions fixed in blueprint §10.3 |
| Maintainer burnout | Medium | High | Vertical slices, reusable lab package, no placeholder debt |
| Accessibility gaps | Medium | Medium | Alt text, contrast, heading structure, review checklist |

## 9. Definition of done (slice-level)

A slice is complete only when:

- [ ] All planned pages exist and contain complete content (no stubs).
- [ ] All planned labs run from a clean environment and meet their time tier.
- [ ] Starters fail as intended and checkers accept only complete artifacts.
- [ ] `mkdocs build --strict` and internal link checks pass.
- [ ] Every new claim has a verified citation or a reproduced result.
- [ ] Rubrics and exemplars exist for new assessments.
- [ ] Safety review is recorded for offensive labs.
- [ ] Technical and editorial reviews are signed off.
- [ ] The changelog and framework-version note are updated.
- [ ] No secrets, personal data, or large artifacts are committed.

## 10. Immediate next steps

1. Owner: confirm repository access, choose licenses, enable Pages (Actions), supply instructor bio and contact policy.
2. Run the final Level 5 validation pass: strict build, internal link check, count verification, and lab regression. Report results; do not publish.
3. Keep the reference hardware and tolerance notes current for iterative-attack, FL, and monitoring labs.
4. Commission the ML and security reviews that this roadmap still lists as open, including the accessibility audit.
5. After owner review, add CI workflows and the first commit.

## 11. Explicit non-goals for this milestone

- Committing, pushing, publishing, changing remotes, or modifying repository settings.
- Enabling Pages or altering GitHub configuration.
- Selecting licenses on the owner's behalf.
- Shipping a runnable project harness that students confuse with a complete solution; briefs specify evidence, not canned answers.
- Adding analytics, tracking, or third-party embeds.
- Claiming external review or Linux verification that has not occurred.

## 12. Next milestone

**Milestone M7 — public v1.0**: capstone guide and six option briefs, assessment pages, full QA, accessibility review, release notes, and a clean-environment replay of every Tier A lab.

Until that slice passes its definition of done, no capstone material should be published.

---

*End of roadmap. Companion documents: [course-blueprint.md](course-blueprint.md), [module-map.md](module-map.md), [lab-catalog.md](lab-catalog.md), [learning-outcomes.md](learning-outcomes.md).*
