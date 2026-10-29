# Assessment Validation Report

| Field | Value |
|---|---|
| Document | Structural and content validation of the self-assessment layer |
| Date | 2026-10-28 |
| Scope | 19 alternate module quizzes, 5 level checks, DIA-01, QB-01, FIN-01, 4 rubrics, the progress record, the practice sampler, and 27 answer-key files |
| Environment | Windows 10 x64, Python 3.14.7, MkDocs 1.6.1, Material for MkDocs 9.8.0, Node.js 24.19.0, CPU only |
| Structural result | **30 of 30 instruments pass**; 65 repository-level checks; 0 failures, 0 warnings |
| Scoring result | Every quiz totals 12 points, every level check 20, the final 100; all four rubric weight tables sum to 100 |
| Unit tests | **25 of 25 pass** (0.296 s) |
| Internal links | **0 broken** in 355 Markdown files |
| MkDocs strict build | **Pass** (14.93 s, 268 HTML pages) |
| Assessment-layer answer keys in build output | **0** (module self-check keys are built deliberately; see §4) |
| Browser test | Widget behavior verified by scripted DOM checks; no visual confirmation is claimed |

This report separates what was checked mechanically from what was judged by reading. A structural pass means the instruments are internally consistent, correctly scored, and correctly separated from their keys. It does not mean the items are psychometrically validated, and no external standard is claimed for any item.

## 1. What was checked

### 1.1 Instrument contracts

`scripts/validate_assessments.py` checks each instrument against its declared shape.

| Instrument | Items | Points | Pass mark | Declared shape that is enforced |
|---|---:|---:|---:|---|
| QZ-00B … QZ-18B (19 files) | 8 each | 12 | 10 | points `1,1,1,1,1,2,2,3`; key covers every item |
| LC-1 … LC-5 | 10 each | 20 | 16 | points `1,1,1,1,1,1,2,2,5,5`; key covers every item |
| DIA-01 | 20 | 20 | 14 | one point per item; key covers every item |
| QB-01 | 56 | 92 | n/a | 24 × 1 + 12 × 1 + 12 × 2 + 8 × 4; sections 14/14/14/9/5 |
| FIN-01 | 25 | 100 | 80 | five parts at 20 points each: 2 × 2 + 2 + 4 + 10 |

For each quiz, level check, diagnostic, and the final, the validator also enforces that the outcomes listed in the page metadata are exactly the outcomes tagged in the answer key. That rule is what caught the metadata overclaims listed in section 3.

### 1.2 Answer-key integrity

- Every key tag line carries a module (or `PRE`), at least one `LO-xx`, a Bloom level 1–6, and a difficulty `D1`–`D5`.
- Tag lines that fail to carry all four are reported as malformed rather than skipped.
- Compound tags such as `M04/M06` and `LO-05/LO-10` are expanded, so a question that spans two modules is counted against both.
- Every quiz key must tag its own module at least once.
- Each key explains the correct answer and, for multiple-choice items, why each distractor is wrong.
- No assessment-layer key file (quiz, level check, diagnostic, bank, or final) lives under `docs/`; those keys are stored in `assessments/answer-keys/`, outside `docs_dir`, and do not appear in the built `site/` directory. The module self-check keys described in §4 are a separate, deliberately published layer.

### 1.3 Rubrics

- The lab rubric, project/RT-01 rubric, and capstone rubric each have a weight table that sums to exactly 100.
- The lab completion checklists cover all 21 lab IDs (LAB-01, LAB-01B, LAB-02 … LAB-20).
- The project rubric covers PRJ-01 … PRJ-06 and RT-01; the capstone rubric covers all six capstone components.

### 1.4 Navigation, links, and duplication

- Every student assessment page is reachable from the Assessments nav section or from an index page that is.
- No answer-key file is referenced from `docs/` or from `mkdocs.yml` as a nav target.
- Alternate quiz and level-check pages are excluded from the sidebar with `not_in_nav` and reached through their index pages.
- Internal Markdown links resolve (`scripts/check_links.py`).
- No two items share a normalized stem, which catches copy-paste duplicates across quizzes and the bank.

### 1.5 Practice sampler

- 10 items, four options each, answer key `[1,0,1,0,1,1,1,1,2,1]`.
- No `fetch`, no storage, no network call, no external service.
- Feedback is withheld until all 10 items are answered; then the keyed option and the chosen wrong option are both marked, and explanations appear one item at a time.

## 2. Results

| Area | Result |
|---|---|
| 19 alternate quizzes | 19 pass, 95 item-level checks |
| 5 level checks | 5 pass, 25 item-level checks |
| Diagnostic | Pass, 5 checks |
| Question bank | Pass, 7 checks |
| Final assessment | Pass, 5 checks |
| Rubrics | Pass, 6 checks |
| Progress record | Pass, 3 checks |
| Practice sampler | Pass, 3 checks |
| Repository-level checks | 65 pass, 0 failures, 0 warnings |

Validator summary line: `30 assessments checked, 0 failed; 65 global checks, 0 global failures, 0 global warnings`.

## 3. Defects found and corrected

The validator found real inconsistencies, and the content was corrected rather than the check relaxed.

| Defect | Correction |
|---|---|
| QZ-02B metadata claimed LO-05, which no keyed item tested | Metadata reduced to the outcomes the key tags |
| QZ-03B metadata claimed LO-30, which no keyed item tested | Metadata reduced to LO-02, LO-03, LO-04 |
| LC-1 and LC-5 metadata claimed LO-30 | Removed; LO-30 is sampled by the question bank only |
| LC-2 metadata claimed LO-12 and LO-15 | Removed; those outcomes are not sampled at that level |
| LC-4 metadata claimed LO-25 | Removed; LO-25 is sampled by QZ-15B only |
| QZ-15B and QZ-18B had no outcomes row | Rows added, matching the key tags |
| Diagnostic metadata covered M00–M01 only, while keyed items also test M04 and LO-29 | Modules and outcomes broadened to match the key |
| Five directory links pointed at key folders without an `index.md` | Index pages created for the quiz and level-check key directories |
| `docs/learning-outcomes.md` linked `../assessments/index.md` | Corrected to `assessments/index.md` |
| The practice sampler marked only correct/incorrect at the fieldset level | Per-option marking added, so the keyed option and the chosen wrong option are distinguished |

## 4. What is not validated

- **No psychometric evidence.** Item difficulty and discrimination are designed, not measured on a population. Bloom and difficulty tags are author judgments. No reliability statistic, standard error, or norm group exists, and none is claimed.
- **No external-standard claim.** Items are aligned to this course's own outcomes. They are not mapped to, endorsed by, or validated against any certification body or published standard.
- **The answer is in the page source.** The practice sampler withholds feedback in the interface, but a learner who reads the HTML or JavaScript can recover the key. This is disclosed on the page. It stops accidental early feedback, not deliberate cheating. The graded instruments (quizzes, level checks, diagnostic, final) have their keys only in `assessments/answer-keys/`, outside the built site, so the same limitation does not apply to them.
- **`not_in_nav` does not remove a page from the build.** Alternatives are hidden from the sidebar but still rendered; they are reachable by URL and are not secret. Only the repository-root key directory is outside `docs_dir`.
- **Pre-existing answer pages remain in the build.** `docs/modules/*/quiz-answers.md` and `docs/modules/*/exercise-solutions.md` were already in `docs/` and are still rendered to `site/`, reachable by URL though absent from the sidebar. This predates the assessment layer and was left unchanged. A follow-up would be to move them beside `assessments/answer-keys/`, which requires deciding whether they stay publishable.
- **Visual layout was not confirmed.** The in-app browser returned `NATIVE_BROWSER_VIEWPORT_UNAVAILABLE` when asked for a screenshot. The widget was exercised through scripted DOM checks (submit blocking, 10/10, 9/10, reset, disabled inputs, option marking, review links), but no claim is made about rendering, spacing, or contrast on a real screen.
- **Answer explanations were reviewed by reading, not by a second subject-matter expert.** Every short-answer and scenario key states the required elements and the acceptable alternatives, but there is no independent grading study.

## 5. Coverage

Section 4.3 of [Learning outcomes](learning-outcomes.md) maps all 35 outcomes to the instrument that samples them. Three outcomes are sampled thinly and are recorded there rather than padded:

| Outcome | Self-assessment coverage | Primary evidence |
|---|---|---|
| LO-25 | QZ-15B only | LAB-19 |
| LO-30 | QB-01 only | LAB-02, LAB-12, LAB-13, LAB-14, LAB-17 |
| LO-11 | QZ-06B and LC-2 | LAB-08 |

A score on any of these instruments is a signal about recall and reasoning, not a substitute for the artifact-based evidence that the course weights.

## 6. How to reproduce

```bash
python scripts/validate_assessments.py            # instrument and repository checks
python scripts/check_links.py                     # internal links and anchors
python -m unittest discover -s tests -v           # unit tests for both validators
node --check docs/javascripts/self-check.js       # widget syntax
mkdocs build --strict                             # navigation and build gate
```

`validate_assessments.py` exits 0 only when every enabled check passes; `--json` writes machine-readable results and `--strict-warnings` promotes warnings to failures.
