# Practice and Review Widget

This page is a small, static sampler of ten items across the five levels. It is a convenient way to check whether the course's vocabulary is still available; it is not a scored assessment and not a substitute for the diagnostic, level checks, or labs.

| Field | Value |
|---|---|
| Items | 10 |
| Coverage | Ten modules across all five levels: M02, M04, M06, M08, M10, M12, M14, M15, M17, M18 |
| Backend | None |
| Account | None |
| Network calls | None |
| Storage | None; reloading the page clears the attempt |
| Feedback | Withheld until you submit all ten answers |

## How it works

1. Answer all ten items. The counter tracks how many you have answered.
2. Select **Check answers**. The page scores the attempt locally in your browser.
3. Read the result and the modules to revisit. After scoring, the keyed option and any option you selected are marked, and an explanation is available one item at a time.
4. If you missed an item, open the linked module quiz or level check and review the named concept before retrying.

The feedback is withheld in the interface, not protected in the source. The page is static and the repository is public, so anyone who reads the JavaScript can find the keyed answers. Do not inspect the source before attempting; the workflow is attempt-first by design, not by enforcement.

No answer is sent anywhere. The widget uses no backend, no account, no API key, no cookie, and no external service. It does not store your score; write it in the [progress record](progress-and-reflection.md) if you want to keep it.

<div id="self-check-app">
  <p class="sc-loading">Loading the sampler…</p>
</div>

<noscript>
  <p><strong>JavaScript is disabled.</strong> The sampler cannot run without it. Use the <a href="../diagnostic/">prerequisite diagnostic</a> or a <a href="../level-checks/">level check</a> instead.</p>
</noscript>

## What this sampler does not measure

- It does not measure whether you can run an attack, reproduce a metric, or write a reproducible package. The labs do that.
- It does not measure whether you can scope an assessment, defend a finding, or design a control. The projects, RT-01, and capstone do that.
- Ten items cannot cover 19 modules. A good score here is a reason to attempt a full check, not evidence that the course is complete.
- The items are design-rated, not psychometrically calibrated.

## Where to go next

| If you want… | Use |
|---|---|
| A prerequisite baseline | [Diagnostic](diagnostic/index.md) |
| A second attempt at a module | [Module alternate quizzes](module-quizzes/index.md) |
| A cumulative check | [Level checks](level-checks/index.md) |
| A full-course sample | [Final assessment](final-assessment/index.md) |
| Targeted practice by module | [Question bank](question-bank/index.md) |
| Artifact scoring | [Rubrics](rubrics/index.md) |
