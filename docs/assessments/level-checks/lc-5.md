# Level 5 Check — Applied Projects (LC-5)

| Field | Value |
|---|---|
| Level | 5 — Applied projects |
| Modules | M16–M18 |
| Items | 10 |
| Points | 20 |
| Time guide | 40 minutes |
| Pass | 16/20 |
| Outcomes | LO-28, LO-29, LO-33, LO-34, LO-35 |
| Answer key | Separate file: `assessments/answer-keys/level-checks/lc-5-key.md` |

Answer without notes. Items 1–6 are worth 1 point, items 7–8 are worth 2 points, and items 9–10 are worth 5 points. Scenarios are marked element by element; use headings.

## 1. Non-goals (1 point)

Which item belongs in the **non-goals** of a bounded assessment of a local document-classification API?

A. The vendor's production infrastructure behind the API  
B. The local replica's `/classify` endpoint  
C. The synthetic document generator and its seed  
D. The model version named in the scope statement

## 2. Usable finding (1 point)

Which set makes an evasion finding usable by an engineer who was not present?

A. A screenshot of one altered document and the word "evadable"  
B. The request budget, base set and count, observed effect against a baseline, reproduction steps, and the affected decision  
C. The attack library name and its default settings  
D. A severity label and a recommendation to retrain

## 3. Research gap (1 point)

Which sentence states a researchable gap rather than a topic?

A. "Document classifiers are important for business processes."  
B. "Nobody has studied evasion of document classifiers."  
C. "Published detector evaluations report recall at one query rate; it is unmeasured whether the ranking of two detectors holds when the attacker paces queries to a fixed alert budget."  
D. "Evasion is a serious problem for machine learning."

## 4. Authorization (1 point)

What must exist before the first request of an assessment against a local replica?

A. Verbal approval from a teammate  
B. A signed authorization naming the target, time window, request budget, data rules, and stop conditions  
C. A public bug-bounty page for the vendor  
D. A completed findings table

## 5. Negative result (1 point)

True or false: a negative result reported with a confidence interval is weaker evidence than reporting no result at all.

## 6. Confirmatory label (1 point)

True or false: an analysis plan revised after seeing the results can still be labeled confirmatory if the revision is documented.

## 7. Costed remediation (2 points)

Name the three elements a remediation entry needs before an owner can schedule it, and state what a remediation without a verification test leaves unresolved.

## 8. Precision and evidence (2 points)

Explain why the precision of a detection alert depends on the base rate of malicious requests, not only on the detector's recall and false-positive rate. Then state why evidence should be captured before a mitigation is applied.

## 9. Scenario: the eleven-hour assessment (5 points)

You have 11 hours to assess a local replica of a document-classification API built from synthetic documents. The API returns a category and a confidence score and logs each request.

Write the scope: the decision the system supports, three assets with a classification each, one bounded adversary profile, three falsifiable test questions, the deliverables, and two non-goals. Do not test any third-party system.

## 10. Scenario: from finding to research question (5 points)

An assessment finds that a detector holds recall 0.80 at a 1% alert budget when queries are evenly paced, but recall falls to 0.55 when the same request budget is spent in short bursts.

Convert this into a bounded research question. State the gap, one claim with its planned comparison, one ablation or control, and two ethics or scope limits. Do not claim the result generalizes beyond the tested replica.

## Scoring

| Score | Interpretation |
|---:|---|
| 18–20 | Strong. You can scope, report, and extend an assessment. |
| 16–17 | Pass. Review the missed item and the linked project guidance. |
| 12–15 | Not yet. Rework the scope or report sections of your project. |
| Below 12 | Reread M16–M18 and the capstone brief before starting the capstone. |
