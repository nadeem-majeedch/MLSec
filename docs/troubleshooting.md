# Troubleshooting

<span class="mlsec-kind">Help</span>

Most problems fall into one of three buckets: the site did not render something, a lab command failed, or a result does not reproduce. Identify the bucket first; the fixes are different.

## First 60 seconds

1. Reload the page. A cached page can hide a corrected link.
2. Check the address. This site is served from the `/MLSec/` project path, and paths are case-sensitive on GitHub Pages.
3. Try the search box with a distinctive term or an identifier such as `LAB-03` or `QZ-07B`.
4. If you are in a lab, confirm that your virtual environment is active and that you are in the lab folder.
5. If nothing works, record the page address and the exact error before changing anything. A precise report is faster than a rebuild.

## Site and navigation

| Symptom | Likely cause | What to do |
|---|---|---|
| “Page not found” after clicking a link | A moved page or a typo in a shared URL | Open the [course roadmap](modules/index.md) or [labs index](labs/index.md) and search for the title |
| A page loads without styling | A blocked stylesheet, an interrupted build, or an offline cache | Reload with a hard refresh; if you are running a local copy, rebuild it |
| Search returns nothing | JavaScript is disabled, the index has not loaded, or the query is too generic | Enable JavaScript, wait for the page to finish loading, and search a distinctive term |
| Mathematics shows as `$...$` | The MathJax CDN is blocked by your network | Read the surrounding prose, which defines each symbol; try another network if you need typeset math |
| A diagram shows as code | The Mermaid CDN is blocked | The diagram source is still readable; the surrounding text explains the flow |
| The copy button is missing | JavaScript is disabled or the browser is old | Select the code manually; the blocks are plain text |
| The dark-mode choice resets | Private browsing or storage restrictions | The site follows your operating system; set the OS preference |
| The menu does not open on a phone | JavaScript failed to load | Use the tab links or a direct page address |
| No previous/next links | The page is the home page, a reference page, or a 404 | Use the breadcrumbs, sidebar, or the [course roadmap](modules/index.md) |
| A publisher link returns 403 | The publisher blocks scripted requests | Open it in a normal browser; the [references](references.md) page records this behavior |
| Text is too small or a table is cut off | Narrow window or high zoom | Zoom the browser; tables and code scroll horizontally by design |
| Printing includes the navigation | The browser ignored the print stylesheet | Use the browser’s print preview; choose “background graphics off” and hide headers and footers |

If a navigation control is hard to use with a keyboard or screen reader, read [Accessibility](site-guide.md#accessibility) and report the page. Accessibility barriers are treated as defects, not preferences.

## Lab commands and environments

The [student guide](student-guide.md#troubleshooting) has the full lab troubleshooting table and the environment reset procedure. Start with these checks:

| Check | Why it matters |
|---|---|
| The virtual environment is active | `python` may point at a different interpreter than the one you installed into |
| You are in the lab folder | Commands such as `python solution.py --out artifacts` write relative to the current directory |
| The pinned requirements are installed | A different NumPy or scikit-learn version can move a metric outside its tolerance |
| The artifact directory exists | The reference writers create it, but a custom script may not |
| The checker is pointed at the right folder | `--artifacts artifacts` is the documented default; a different path is a different run |
| The seed and split match the brief | Most mismatched metrics are a split or preprocessing difference, not a modeling difference |

Common first failures:

| Symptom | What to try |
|---|---|
| `python: command not found` | Try `py` on Windows or `python3` on macOS/Linux; then activate the environment |
| `ModuleNotFoundError` | Install from the lab’s pinned requirements inside the active environment |
| `FileNotFoundError` for `metrics.json` | Run the solution or starter with the documented `--out` folder before the checker |
| The checker reports one metric outside tolerance | Read the first failing check; compare seed, split, and preprocessing with the lab brief |
| Results change between runs | Set seeds, use deterministic settings, and pin versions; record both runs |
| `pip` fails behind a proxy or with SSL errors | Configure the proxy or certificate for your environment; do not disable verification silently |
| The run is far slower than the stated time | Reduce the test subset or steps as the lab allows, and record the trade-off |

If a lab passes 150% of its stated time, stop and write the blocker. A documented blocker is evidence of debugging skill; an exhausted all-nighter is not. The stop rule is in the [student guide](student-guide.md#labs).

## A result does not reproduce

Work in this order:

1. **Environment.** Compare Python and package versions with `run.json` and the pinned requirements.
2. **Data.** Confirm the dataset and seed. LAB-01B and LAB-12 include hashes for this reason.
3. **Split.** Check row counts, stratification, grouping, and overlap. A random split where the brief requires a grouped split changes the result legitimately.
4. **Preprocessing.** Confirm that scalers and imputers were fitted on training rows only.
5. **Metric.** Confirm the denominator. Attack success rate is usually conditional on the clean-correct base set; accuracy drop is not.
6. **Command.** Run the documented command in a fresh process, not a notebook with hidden state.

If all six match and the number still differs, report the difference with both `run.json` files and the exact commands. Do not adjust the expected value to match your run.

## Report a broken page or a course error

Open an issue in the [course repository](https://github.com/nadeem-majeedch/MLSec/issues) with:

- the page address and the section heading;
- the exact command or sentence;
- what you expected and what happened;
- your browser or Python version, when relevant;
- a minimal reproducer for a code problem.

Do not include credentials, personal data, or confidential material. For a security issue in the course materials, use coordinated disclosure rather than a public issue with an exploit.

## Still stuck

Use the six-item question format in the [student guide](student-guide.md#troubleshooting): command, full error, versions, minimal reproducer, expected versus actual, and what you tried. A question with those six items usually gets a useful answer; a screenshot of a traceback without the command rarely does.

## Related pages

- [How to use this site](site-guide.md) — navigation, page types, accessibility, and conventions.
- [Student guide](student-guide.md) — setup, study loop, lab troubleshooting, FAQ, and AI policy.
- [Course roadmap](modules/index.md) — find a module by title or outcome.
- [Assessment index](assessments/index.md) — attempt rules, scoring, and retakes.
