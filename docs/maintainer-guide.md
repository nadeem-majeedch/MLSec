# Maintainer Guide

**Audience: maintainers and the repository owner.** This page is not student content. It is excluded from the published navigation through `not_in_nav` in `mkdocs.yml`, but it lives in `docs/` because that path was requested for this milestone. If the project later adopts the planned `maintainers/` directory, move this page there and update the exclusion and any inbound links.

The design rationale for the course is in the [course blueprint](course-blueprint.md). This guide is about building, validating, and releasing the site without breaking the student experience.

## 1. Current state

| Item | State as of 2026-10-28 |
|---|---|
| Local workspace | Not a Git repository; created from a blank directory |
| Remote repository | Public and empty at the time of the audit; no baseline commit |
| GitHub Pages | No serving site at the time of the audit; treated as unconfigured |
| Workflows | None; no CI or Pages workflow exists |
| Planning documents | Complete through Level 5: blueprint, module map, lab catalog, project catalog, learning outcomes, implementation roadmap, and evaluator guide |
| Student layer | README, landing page, student guide, course roadmap, lab guide, project catalog, capstone brief, references |
| Site configuration | `mkdocs.yml` updated with Level 5, project, and assessment navigation; local build only |
| Lessons and labs | Levels 1–5 published: M00–M18 (88 lessons), QZ-00–QZ-18, 75 exercises, LAB-01…LAB-20 built and checker-verified, six project briefs, RT-01, and the capstone brief with rubric |
| Assessment layer | 19 alternate module quizzes, five level checks, a 20-item diagnostic, a 56-item bank, a 25-item final, four rubrics, a progress record, and a static practice sampler; answer keys live in `assessments/answer-keys/` outside `docs/` |

No commit, push, deployment, remote change, or repository setting was performed in this milestone. Those remain owner actions.

## 2. Audience separation and navigation

| Location | Audience | Published in nav |
|---|---|---|
| `docs/index.md` | Students | Yes, as Home |
| `docs/learning-paths.md` | Students | Yes, first page of the Start here tab |
| `docs/site-guide.md` | Students | Yes, Start here |
| `docs/about.md` | Students | Yes, Start here |
| `docs/troubleshooting.md` | Students | Yes, Start here |
| `overrides/404.html` | Students | Built as `404.html`; not in the sidebar |
| `docs/student-guide.md` | Students | Yes |
| `docs/modules/index.md` | Students | Yes, as Course roadmap |
| `docs/labs/index.md` | Students | Yes |
| `docs/projects/index.md` and project briefs | Students | Yes |
| `docs/projects/capstone.md` | Students | Yes |
| `docs/assessments/` (index, practice, diagnostic, quizzes, level checks, final, bank, rubrics, progress checklist, progress record) | Students | Yes, except the alternate quiz and level-check pages, which are reachable from their index pages and excluded from the sidebar |
| `assessments/answer-keys/` | Instructors and self-graders | Not part of the built site; outside `docs_dir` |
| `docs/references.md` | Students | Yes |
| `docs/maintainer-guide.md` | Maintainers | No; excluded with `not_in_nav` |
| `docs/projects/evaluator-guide.md` | Evaluators | No; excluded with `not_in_nav` |
| Planning and catalog documents | Maintainers and reviewers | No; excluded with `not_in_nav` |
| `README.md` (repository root) | Everyone; GitHub front door | Not part of the built site |
| `mkdocs.yml` | Maintainers | Not content |

**Rules**

1. Never add a nav entry for a page that does not exist. `mkdocs build --strict` should fail rather than ship a dead link.
2. Never place deployment, credentials, or maintainer process in a student page. The student guide is already long enough.
3. Planning documents are built as pages but excluded from navigation. They are linked from maintainer and student pages where useful, so do not add them to `exclude_docs` unless you also remove those links.
4. Do not link from inside `docs/` to `../README.md`. MkDocs cannot resolve files outside `docs_dir`, and strict mode will fail. Duplicate the necessary fact in a student page or link to a site page instead. This rule was applied to the landing page during this milestone.

## 3. Source-of-truth hierarchy

When documents disagree, resolve in this order:

| Priority | Document | Authority |
|---:|---|---|
| 1 | [Course blueprint](course-blueprint.md) | Course scope, module hours, assessment weights, reference policy |
| 2 | [Learning outcomes](learning-outcomes.md) | Outcome statements, success standards, assessment mapping |
| 3 | [Module map](module-map.md) | Lesson IDs, counts, dependencies, build order |
| 4 | [Lab catalog](lab-catalog.md) | Lab objectives, tasks, deliverables, rubric checks |
| 5 | [Project catalog](project-catalog.md) | Project scenarios, reuse map, artifact contract, evaluator policy |
| 6 | [Implementation roadmap](implementation-roadmap.md) | Phase sequencing and quality gates |
| 7 | README and site pages | Derivative summaries; must not introduce new scope |

A change to a module hour, lab ID, outcome mapping, or assessment weight requires updating every document that states it, plus the derivative pages. The quick consistency checks are in section 9.

## 4. Identifier conventions

| Prefix | Meaning | Example | Rule |
|---|---|---|---|
| `Mxx` | Module | `M04` | Two digits; never reused |
| `Mxx.Ly` | Lesson | `M04.L3` | Stable within a module |
| `LAB-xx` | Lab | `LAB-07` | Two digits; sequence is the recommended order |
| `QZ-xx` | Knowledge check | `QZ-06` | One per module, `QZ-00` to `QZ-18` |
| `MP-xx` | Mini-project | `MP-02` | Four total |
| `PRJ-xx` | Applied project | `PRJ-03` | Six total, `PRJ-01` to `PRJ-06` |
| `RT-xx` | Red/blue exercise | `RT-01` | One total |
| `CAP-x` | Capstone option | `CAP-E` | Six options, `CAP-A` to `CAP-F` |
| `CH-xx` | Challenge exercise | `CH-09` | One per module, optional |
| `LO-xx` | Learning outcome | `LO-17` | 35 outcomes, `LO-01` to `LO-35` |
| `PLO-x` | Program outcome | `PLO-3` | Seven outcomes |
| `F-xx` | Framework reference | `F-07` | `F-01` to `F-23` |
| `R-xx` | Research reference | `R-60` | `R-01` to `R-103`; gaps are intentional; do not renumber |

Stable site anchors currently in use:

- `#m00` to `#m18`, and `#cap` in `docs/modules/index.md`;
- `#stage-1` to `#stage-6`;
- `#entry-paths`;
- `#baseline`, `#setup`, `#study-loop`, `#schedules`, `#labs`, `#projects`, `#assessment`, `#troubleshooting`, `#faq`, `#ai-policy`, `#safety`, `#incomplete` in `docs/student-guide.md`.

Anchors are implemented with raw `<a id="..."></a>` tags so they work in both MkDocs and GitHub's Markdown renderer. Do not add `attr_list` anchor syntax (`{: #id }`); GitHub displays it literally.

## 5. Content model

Every module is published as a complete vertical slice:

> **Scenario → objectives → lessons → lab → quiz → reflection → artifact**

No page is a stub. A module is published only when all seven parts exist and the lab runs from a clean environment.

### Lesson requirements

- Observable objectives, each mapped to an LO ID.
- A worked example with a minimal code path.
- A guided practice cell the learner can run and modify.
- A knowledge check with explanations and misconception tags.
- A link to the lab and a statement of what the learner keeps.
- Citations for every technical claim, using the verified reference list.

### Quiz requirements

- 10 items per module.
- Mix: 20% recall, 40% apply, 30% analyze, 10% evaluate or create.
- Pass mark 80%, unlimited retakes, no time limit.
- An explanation for every option, including why distractors are wrong.
- At least one "find the flaw" item per quiz.

### Lab requirements

- Threat model and metric definitions written before the code.
- Pinned environment, fixed seeds, documented runtime.
- Public or synthetic data with a checksum and a fallback.
- Benign payloads only; containers for anything that deserializes or executes untrusted content.
- Rubric-specific checks: three to five per lab.
- A reduced CPU configuration for every Tier B lab.
- A "stop here" point at 150% of the stated time.

### Writing and accessibility

- Plain language; define jargon on first use.
- Alt text for every figure; no meaning conveyed by color alone.
- One `h1` per page; do not skip heading levels.
- Tables must have a header row and consistent column counts.
- Prefer concrete numbers with units and budgets over adjectives such as "strong" or "robust".
- Do not invent authors, DOIs, URLs, dataset properties, or framework requirements. If a claim cannot be verified, mark it as unverified or remove it.

## 6. Local build

The site uses MkDocs with the Material theme. The configuration is `mkdocs.yml` at the repository root.

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash on Windows
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install mkdocs-material
mkdocs serve                       # http://127.0.0.1:8000
mkdocs build --strict              # validates nav, links, and warnings
```

**Configuration decisions**

| Setting | Value | Reason |
|---|---|---|
| `docs_dir` | `docs` | README stays at the repository root for GitHub |
| Nav | Seven tabs: Home, Start here, Modules, Labs, Projects, Assessments, Reference. Modules contains the roadmap and five level sections; all 19 modules keep their lessons | A stable top-level structure without dead entries; planning docs excluded |
| `not_in_nav` | Planning documents, `maintainer-guide.md`, module quiz answers, exercise solutions, the validation reports, alternate quiz and level-check pages | Built but hidden from student navigation. The assessment-layer keys in `assessments/answer-keys/` are outside `docs_dir` and never built; the module self-check keys are built deliberately (see the note below) |
| Theme | Material with tabs, section indexes, breadcrumbs, previous/next footer, tracking, back-to-top, table-of-contents following, code copy, and search suggest/highlight/share | Responsive navigation and readable long lessons without custom JavaScript |
| Palette | Light and dark schemes with a header toggle; indigo primary and teal accent | Accessible contrast in both schemes; the toggle follows the operating system until chosen |
| Logo and favicon | `assets/logo.svg` and `assets/favicon.svg` | Local assets, no third-party image requests; the logo carries an accessible title |
| `edit_uri` | Empty | The default branch and Pages source are owner decisions; an unverified “edit this page” link would be worse than none |
| Plugins | `search` | Client-side search; no analytics |
| `custom_dir` | `overrides` | Holds `404.html`, which MkDocs renders as a static template; Markdown in `docs/404.md` is not available to that template |
| Markdown | admonition, attr_list, md_in_html, tables, footnotes, toc, arithmatex, superfences, tabbed | Supports the landing-page cards, lesson tables, and Mermaid/TeX used by the labs |
| CSS | `stylesheets/site.css` then `stylesheets/self-check.css` | Site typography, focus, links, cards, print styles; self-check styles remain isolated |

The built `site/` directory must never be committed. `.gitignore` excludes `site/`, virtual environments, generated datasets, checkpoints, notebook checkpoints, lab artifacts, and `.env` files.

**Note on README.** The root `README.md` is the GitHub front door, not a site page. Do not add it to `docs/` or to the nav. If a fact must appear on both, keep the README summary short and the site page authoritative.

**Note on `not_in_nav`.** The key hides a page from the sidebar; MkDocs still renders it into `site/`, and the page is reachable by direct URL. Never store an answer key under `docs/` on the assumption that `not_in_nav` protects it. The assessment keys live in `assessments/answer-keys/` at the repository root, outside `docs_dir`, so they are never built. The module `quiz-answers.md` and `exercise-solutions.md` files that already sit under `docs/modules/` are a pre-existing decision; the residual exposure is listed in the [assessment validation report](assessment-validation-report.md).

## 7. Link and anchor validation

`mkdocs build --strict` catches missing nav targets and unresolved relative links, but it does **not** validate fragments (`#anchor`). Use both checks:

1. **Relative file links.** Every `](path)` target must resolve relative to the containing file inside `docs/`. Links that escape `docs_dir` are invalid.
2. **Anchors.** Every `](#fragment)` must match either an explicit `<a id="fragment"></a>` or a heading that MkDocs will slugify. Prefer explicit anchors for anything linked from another page.
3. **External links.** Check status codes, but treat 403 from publisher sites (ACM, ISO, some DOI resolvers) as bot-blocking rather than a dead link. Verify those in a browser.
4. **Reference policy.** Date every framework and re-verify quarterly. Do not add a reference you have not opened.

The repository now ships those checks rather than describing them:

| Command | What it does |
|---|---|
| `python scripts/check_links.py` | Walks `docs/**/*.md`, resolves every relative link and fragment, and reports broken targets |
| `python scripts/validate_labs.py` | Structural checks on all 21 labs; add `--execute` to run reference solutions and checkers in a temporary directory |
| `python scripts/validate_assessments.py` | Structural checks on all assessment pages and answer keys, including scoring totals, tag parsing, metadata/key outcome agreement, nav coverage, and duplicate stems |
| `python -m unittest discover -s tests -v` | Unit tests for both validators |

Keep new one-off checks in `scripts/`, not in `docs/`, and wire them into this section when they become part of the release gate.

## 8. Deployment policy

**Do not add or replace a Pages workflow until the owner verifies the repository settings.** At the time of the audit there was no serving site and no workflow, so there is nothing to replace — but deployment is still an owner action, not an agent action.

When the owner authorizes deployment:

1. Confirm the default branch and repository access.
2. Set Pages source to **GitHub Actions**.
3. Add a workflow that checks out the repository, installs pinned MkDocs dependencies, runs `mkdocs build --strict`, uploads the `site/` artifact, and deploys it.
4. Use least privilege: `contents: read` for the build job; `pages: write` and `id-token: write` only for the deploy job; a `github-pages` environment.
5. Verify the published URL and a sample of internal links after the first deployment.
6. Record the deployment date and framework versions in the release notes.

Do not commit the built site, add repository secrets for the docs build, or change remote settings as part of a content change.

## 9. Quality gates

Run these before any release or after a structural change.

| Check | Pass condition |
|---|---|
| Build | `mkdocs build --strict` exits 0 |
| Internal links | Every relative link resolves to an existing file |
| Anchors | Every fragment resolves to an explicit anchor or heading |
| Navigation | Every nav entry exists; no student nav entry points to a maintainer page |
| Placeholders | No page is an empty stub; planned content is labelled as planned |
| Module hours | Guided modules, projects, and RT-01 sum to 236; capstone 40; total 276 |
| Labs | 21 lab documents (LAB-01…LAB-20 plus LAB-01B); 84 hours; each maps to at least one LO |
| Projects | Six project briefs (11 h each) and RT-01 (9 h); every brief has rubric, deliverables, safety, and reflection |
| Outcomes | 35 LOs; every LO has a primary evidence source other than a quiz |
| Assessments | `scripts/validate_assessments.py` exits 0: every quiz totals 12 points, every level check 20, the final 100, every rubric 100 weight, and every key tag names its module and outcomes |
| Answer keys | No assessment-layer key under `docs/`; `assessments/answer-keys/` covers every quiz, level check, diagnostic, bank, and final and is never built. Module `quiz-answers.md` and `exercise-solutions.md` are self-check pages built deliberately and linked after an attempt; no lab reference solution is built |
| IDs | No duplicate or reused module, lab, quiz, project, exercise, or outcome ID |
| References | New references verified; framework versions dated |
| Safety | Offensive labs, projects, and RT-01 use local, synthetic, or sandbox targets and benign payloads |
| Accessibility | Alt text or accessible SVG titles, heading order, table headers, visible focus, no color-only meaning, readable at 200% zoom |
| Base path | The built site is served from `/MLSec/`; no internal link or asset resolves from the domain root, and `site/404.html` works |
| Page metadata | Every built page has a unique `<title>` and exactly one first-level heading |
| Hygiene | No secrets, personal data, datasets, checkpoints, or `site/` committed |

A content change that alters scope, hours, or assessment must update the blueprint, outcomes, module map, and lab catalog together. A site-only change must not silently contradict them.

## 10. Release process

1. Freeze content for the release.
2. Run the quality gates in section 9.
3. Re-run one Tier A lab from a clean environment if the release includes lab changes.
4. Update the changelog and the framework-version note.
5. Tag the release using the roadmap's version sequence (`v0.1`, `v0.2`, and so on).
6. Publish only after the owner approves the deployment.

**Maintenance cadence.** Quarterly: re-check ATLAS, OWASP, NIST, and tool versions; update references and affected labs. Per release: re-run CI, links, and a sample of labs. When a tool breaks, pin an older version, provide a replacement, or mark the lab deprecated with a migration note. Reproducibility bug reports take priority over new content.

## 11. Current milestone and remaining work

Levels 1–5 are complete and verified: eighteen modules (M00–M18), 88 lessons, nineteen knowledge checks, 75 exercises, twenty-one labs, six project briefs, RT-01, and the capstone brief with milestones and a rubric.

The remaining work is maintenance and owner-authorized release:

- run the strict build and link check before each release;
- deploy only after the owner approves, then verify internal links on the published site;
- keep `site/`, `__pycache__/`, and generated artifacts out of version control;
- re-verify external links and framework versions quarterly;
- add worked examples only where they do not reveal the analysis a project or capstone is meant to assess.

**Explicit non-goals for now:** committing, pushing, deploying, changing remotes, or modifying repository settings without the owner's instruction.

## 12. Open owner decisions

| Decision | Why it blocks | Current default |
|---|---|---|
| Content license | Legal reuse terms are undefined | None chosen |
| Code license | Lab reuse terms are undefined | None chosen |
| Pages enablement | No site is served | Unconfigured |
| Instructor bio, photo, contact | About page must not invent details | Short profile only |
| Solutions policy | Affects assessment integrity | Reference lab solutions live in `labs/`, outside `docs_dir`, and are never built; the evaluator guide is built but excluded from nav. Module self-check keys under `docs/modules/` are published deliberately |
| Analytics and privacy | Tracking posture | No analytics |
| Brand and navigation | Site identity | Material defaults |
| Contribution workflow | External contributions | Issues only |

Do not fill these gaps by assumption. Record the owner's decision in this guide and in the blueprint before publishing dependent content.

## 13. Risks

| Risk | Mitigation |
|---|---|
| Framework drift | Date every framework; quarterly review |
| Dependency breakage | Pin versions; CI smoke tests; deprecation policy |
| Lab hardware disparity | CPU tiers, subsets, documented tolerances |
| Placeholder debt | Vertical slices only; strict build |
| Citation errors | Verified list; "cite or reproduce"; review gate |
| Solution leakage | Keep lab solutions outside `docs_dir` and the evaluator guide out of nav; publish expectations, not full answers. Module self-check keys are published only as separate pages linked after an attempt |
| Assessment drift | Keep project rubrics and capstone milestones aligned with the outcome map and re-check weights together |
| Offensive-content misuse | Sandbox-only labs and projects; authorized-use statement; safety review |
| Navigation drift | Nav only for real pages; strict build in CI |
| Maintainer burnout | Reusable lab package; no placeholder debt |
| Material theme end-of-life (May 2027) | Pin the current version; evaluate the upstream successor and plan a migration before the EOL date. The notice is informational and does not fail the build. |

## 14. Repository content map

| Path | Purpose |
|---|---|
| `README.md` | Student entry point on GitHub |
| `mkdocs.yml` | Local site build and navigation |
| `docs/index.md` | Site landing page |
| `docs/student-guide.md` | Setup, study loop, labs, assessment, troubleshooting |
| `docs/modules/index.md` | Course roadmap with stable module anchors |
| `docs/modules/m00-orientation` … `m18-capstone-and-research` | Published lessons, quizzes, exercises, and answer keys |
| `docs/labs/lab-01.md` … `lab-20.md` | Published lab briefs |
| `docs/labs/index.md` | Lab sequence, tiers, artifact, rubric |
| `docs/projects/index.md` | Six applied projects, RT-01, and capstone route |
| `docs/projects/prj-01-fraud-detection.md` … `prj-06-robustness-comparison.md`, `rt-01-red-blue.md` | Published project and exercise briefs |
| `docs/projects/capstone.md` | Capstone requirements, milestones, rubric, research extension |
| `docs/projects/evaluator-guide.md` | Evaluator reference and calibration; excluded from nav |
| `docs/project-catalog.md` | Project design contract, reuse map, and build notes |
| `docs/references.md` | Annotated references |
| `labs/lab-01-environment` … `lab-20-agent-containment` | Runnable lab packages |
| `labs/shared/mlsec_labs` | Manifest, environment, and metric helpers shared by labs |
| `docs/maintainer-guide.md` | This page |
| Planning documents | Blueprint, module map, lab catalog, project catalog, outcomes, roadmap |

Levels 1–5 are published; workflows, licenses, and deployment files do not exist yet.
