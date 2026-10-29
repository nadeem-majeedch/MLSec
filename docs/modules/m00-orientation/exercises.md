---
title: Module 00 Exercises
---

# Module 00 Exercises

**Three exercises · about 60 minutes · Complete after the lessons**

These exercises produce the first entries in your portfolio. Write them in `work/m00/` in your local clone. Do not look at the [solutions](exercise-solutions.md) until you have written your own answers.

---

<a id="artifact"></a>

## Exercise 1 — Environment verification report

**Goal.** Prove that your environment works and that you can record it precisely.

**Tasks.**

1. Create and activate a virtual environment.
2. Install the Level 1 requirements from `labs/lab-01-environment/requirements.txt`.
3. Run the version check from Lesson 00.2 and save the output to `work/m00/versions.txt`.
4. Create a small text file `work/m00/artifact.txt` containing exactly `mlsec-lab-01` followed by a newline.
5. Compute its SHA-256 hash and write `work/m00/manifest.json` with the filename, size in bytes, and hash.
6. Modify the file by adding `-tampered`, recompute the hash, and record both hashes in your report.
7. Delete the tampered file and restore the original content. Verify that the original hash matches again.

**Deliverable.** `work/m00/environment-report.md` containing:

| Field | Your value |
|---|---|
| Operating system and version | |
| Python version and interpreter path | |
| Package versions (NumPy, pandas, scikit-learn, joblib, PyYAML) | |
| Virtual environment path | |
| Original file size and SHA-256 | |
| Tampered file SHA-256 | |
| Verification result before and after tampering | |
| One thing that surprised you | |

**Success criteria.**

- The interpreter path contains `.venv`.
- All six versions are recorded.
- The original hash is `4ff7794ac45e6255f7ed6926943f91bd4968b9834592ca2f2958504e4862380b` if the file contains exactly `mlsec-lab-01\n`.
- The report explains why the two hashes differ.

---

## Exercise 2 — Scenario-based authorization review

**Goal.** Apply the five-part authorization test to realistic requests and write a defensible decision.

Read each request, then complete the decision table.

**Request A.** A public capture-the-flag platform publishes a machine-learning challenge with a local container and an explicit rule that participants may attack only that container. The container has no network access. You want to run an evasion attack on the included model.

**Request B.** Your former employer asks you to "check whether the fraud model can be fooled" on their production API. They say you can use your old login, which still works, and that "legal will sort out the paperwork later." The model processes real customer transactions.

**Request C.** You trained a small classifier on the built-in scikit-learn digits dataset and want to test whether adding noise changes its predictions. Everything runs on your laptop.

**Request D.** While testing Request C, you discover that a popular open-source preprocessing library crashes on a malformed input in a way that could be used for denial of service. You want to publish a proof-of-concept exploit immediately.

**Tasks.**

1. For each request, decide `ALLOW`, `ASK`, or `DENY`.
2. For each decision, list which of the five conditions are met, missing, or violated.
3. For Request D, write the first three steps you would take before any public disclosure.
4. For Request B, write the exact sentence you would send to the requester explaining your decision. Keep it professional and under 80 words.

**Deliverable.** `work/m00/authorization-review.md` with the decision table, the disclosure steps, and the message.

**Success criteria.**

- Every decision names the condition that drives it.
- Request B is denied or paused, not accepted because of the old login.
- Request D does not publish before contacting the maintainer.
- The message is clear, non-accusatory, and proposes a lawful path forward.

---

## Exercise 3 — A 12-week study plan

**Goal.** Turn the course roadmap into a schedule you can actually keep.

**Constraints.**

- You have **6 hours per week**, in three 2-hour blocks.
- You work full time and cannot study on two consecutive weeknights.
- You want to finish the Foundations stage (M00–M03, including LAB-01, LAB-01B, and LAB-02) in 12 weeks.
- You need one buffer week for illness, work travel, or a lab that runs long.

**Tasks.**

1. Allocate the four modules and three labs across 12 weeks.
2. For each week, list the lesson or lab, the deliverable, and the retrieval activity.
3. Identify the two weeks most likely to slip and explain why.
4. State what you will cut first if you fall behind, and what you will never cut.
5. Schedule the 1-, 3-, 7-, and 21-day reviews for Module 03.

**Deliverable.** `work/m00/study-plan.md` containing a 12-row table and a short risk note.

**Success criteria.**

- Total planned time is at most 72 hours (12 weeks × 6 hours).
- Every module and lab appears.
- At least one buffer week exists.
- The plan includes retrieval, not just reading.
- The "never cut" list includes the threat model (LAB-02) and the evidence artifacts.

---

## Portfolio checklist

- [ ] `environment-report.md` with versions and hashes
- [ ] `ethics-statement.md` signed and dated
- [ ] `authorization-review.md` with four decisions
- [ ] `study-plan.md` with 12 weeks and a buffer
- [ ] Five-line reflection: what worked, what failed, what you would test next, what you misunderstood, what evidence is missing

When all five are complete, run [LAB-01](../../labs/lab-01.md). Compare your answers with the [exercise solutions](exercise-solutions.md) only after you have written your own.
