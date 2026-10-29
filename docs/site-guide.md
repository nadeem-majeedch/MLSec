# How to Use This Site

<span class="mlsec-kind">Start here</span>

This site is the reading and navigation layer of ML-Sec. The labs, starter code, reference solutions, and checkers live in the [course repository](https://github.com/nadeem-majeedch/MLSec). You can read the course here; you run it on your own machine.

The site has no accounts, no backend, and no analytics. Search runs in your browser against a static index. Nothing you type is sent to a server.

## Navigate the course

| Control | Where it is | What it does |
|---|---|---|
| Top tabs | Below the header | Switches between Start here, Modules, Labs, Projects, Assessments, and Reference |
| Sidebar | Left, inside the current tab | Opens the modules and lessons in that area |
| Breadcrumbs | Below the header | Shows where the current page sits; each step is a link |
| Previous / next | Bottom of every lesson | Moves through the course in reading order |
| Table of contents | Right side on wide screens | Jumps to a section on a long page |
| Search | Top right | Searches page titles and body text; results open in place |
| Dark mode | Sun or moon icon in the header | Follows your system setting until you choose |
| Home | The ML-Sec logo and the Home tab | Returns to the landing page |

On a phone or narrow window, the tabs move into the menu button. The table of contents collapses. Code blocks scroll sideways instead of shrinking the text.

## Know what kind of page you are on

The course uses the same page types everywhere so you can tell a lesson from an assessment.

| Page type | How to recognize it | What to do |
|---|---|---|
| Module overview | Title begins “Module 04 —”; a level, hours, and prerequisite line; measurable objectives | Read the objectives and prerequisite checklist before the first lesson |
| Lesson | Title begins “Lesson 04.2 —”; time and “Lesson 2 of 5”; ends with “Check yourself” and “Next step” | Read actively, run the examples, answer the check questions without notes |
| Lab | Title begins “LAB-03 —”; a line with tier, hours, difficulty, module, and outcomes | State the threat model first, produce the artifact, run the checker |
| Exercises | Title ends “Exercises”; a table of exercises and deliverables | Attempt in `work/mXX/` before opening the solutions |
| Knowledge check | Title includes “Knowledge Check — QZ-04”; item points and a pass mark | Answer closed-book, then compare with the answer key |
| Hints | A “Hints” section, often with collapsible blocks | Open one hint at a time; write what you tried first |
| Solutions | A separate “Exercise solutions” or “Quiz answers” page | Use only after a complete attempt; these pages are linked from exercises but kept out of the sidebar |
| Reference | Glossary, references, framework mapping, reading guide, dataset catalog | Use while reading; every entry links back to the lesson or lab that uses it |
| Assessment | Diagnostic, quizzes, level checks, final, rubrics, progress record | Follow the attempt-first rules on the [assessment index](assessments/index.md) |

A lab brief is not the lab. The brief tells you what to build and how it is scored; the repository contains the starter, the reference implementation, and the checker. The brief always names the command.

## Code, mathematics, and diagrams

- **Copy a command.** Every code block has a copy control in its top-right corner. Copy the whole block, then read it before running it.
- **Read the language label.** Commands are `bash` unless the block says PowerShell. Python blocks are complete enough to run from the stated working directory.
- **Mathematics.** Equations are rendered with MathJax. If your network blocks the MathJax CDN, you will see the TeX source instead of typeset math. The surrounding prose defines each symbol, so the lesson remains readable.
- **Diagrams.** Mermaid diagrams render in the browser. If the Mermaid CDN is blocked, the diagram source remains visible as text.
- **External links.** Publisher pages may block automated checks or require a subscription. The [references](references.md) page records the verification date and the few publisher links that return 403 to scripts.

## Accessibility

The site is designed to work with a keyboard, a screen reader, and text zoom.

| Feature | How to use it |
|---|---|
| Skip link | Press <kbd>Tab</kbd> once on load; a “Skip to content” link appears before the header |
| Keyboard navigation | <kbd>Tab</kbd> and <kbd>Shift</kbd>+<kbd>Tab</kbd> move through links and controls; <kbd>Enter</kbd> or <kbd>Space</kbd> activates; <kbd>Esc</kbd> closes the search dialog |
| Visible focus | A high-contrast outline marks the focused control; it is never removed |
| Text zoom | Browser zoom to 200% reflows the page without hiding content |
| Dark mode | The header toggle switches schemes; contrast is checked in both |
| Reduced motion | The site respects your operating-system “reduce motion” setting |
| Links | Content links are underlined, not distinguished by color alone |
| Tables | Every data table has a header row; tables scroll horizontally on narrow screens |
| Page structure | One first-level heading per page, then nested section headings; the table of contents mirrors them |
| Images | The only site image is the logo, which has an accessible name; course diagrams are text or Mermaid, not raster images |

If a page is hard to use with your assistive technology, open an issue in the [course repository](https://github.com/nadeem-majeedch/MLSec/issues) with the page address, your browser, and what happened. Do not include personal data.

## Track your progress

- The [practice sampler](assessments/practice.md) is a ten-item, unscored self-check. It stores nothing; reloading resets it.
- The [progress checklist](assessments/progress-checklist.md) is a printable list of modules, labs, checks, and evidence.
- The [progress record](assessments/progress-and-reflection.md) is the fuller log: scores, missed item IDs, concepts, and retake dates.
- The [rubrics](assessments/rubrics/index.md) define what “complete” means for a lab, project, and capstone.

Tick a box only when the named evidence exists. A score without an artifact is a memory, not a record.

## Read the identifiers

| Prefix | Meaning | Example |
|---|---|---|
| `Mxx` | Module | M04 |
| `Mxx.Ly` | Lesson | M04.L3 |
| `LAB-xx` | Lab | LAB-07 |
| `QZ-xx` / `QZ-xxB` | Module knowledge check / alternate form | QZ-04 / QZ-04B |
| `LC-x` | Level check | LC-2 |
| `PRJ-xx` | Applied project | PRJ-03 |
| `RT-xx` | Red/blue exercise | RT-01 |
| `CAP-x` | Capstone option | CAP-E |
| `LO-xx` | Learning outcome | LO-17 |

**Tiers.** Tier A runs on a laptop CPU in about ten minutes or less per run. Tier B needs a reduced CPU configuration or 30–60 minutes. Tier C is optional GPU work and is never required. No published lab requires a GPU, a paid service, or an API key.

**Difficulty.** Lab difficulty runs from 1 (foundational) to 4 (advanced). Difficulty describes the reasoning and measurement burden, not the length.

**Hours.** Every estimate is learner time for a typical attempt, including reading and reflection. If a lab passes 150% of its stated time, stop and write down the blocker; that is the course stop rule.

## When something does not work

Use [Troubleshooting](troubleshooting.md) for navigation, search, rendering, keyboard, and lab-environment problems. It links to the deeper lab troubleshooting in the [student guide](student-guide.md#troubleshooting) rather than repeating it.

If a link is broken, the page is missing, or a command in a brief does not match the repository, report it as an issue with the page address and the exact command. Corrections are welcome; please do not include credentials, personal data, or third-party material you do not have permission to share.

## Related pages

- [Learning paths](learning-paths.md) — choose an entry point.
- [Student guide](student-guide.md) — setup, study loop, schedules, labs, assessment, and lab troubleshooting.
- [Course roadmap](modules/index.md) — every module with prerequisites and outcomes.
- [Glossary](glossary.md) — plain-language definitions and acronym expansions.
