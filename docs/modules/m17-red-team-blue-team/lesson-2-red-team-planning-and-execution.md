# Lesson 17.2 — Red-Team Planning and Execution

<a id="m17-l2"></a>

**Module 17 · Lesson 2 of 4 · 1 hour · LO-34**

## Scenario

Two red teams get the same target and the same four hours. The first writes a tool list — `curl`, a fuzzer, a PGD script — and runs whatever seems promising. At the end it has twenty screenshots, three of which it can reproduce.

The second writes seven attack hypotheses, each with a budget, an oracle, and a place to record the result. It runs them in order, logs every request, and stops at 1,900 requests. At the end it has seven results, four negative, and one finding with a replay command. The negative results are as useful as the positive one: they tell the blue team which detections were never exercised and which controls held.

The difference is not skill. It is that an attack plan is an experiment design, not a bag of tricks.

## Objectives

By the end of this lesson you will be able to:

1. Convert a red objective into an ordered attack sequence with explicit hypotheses.
2. Allocate finite request, time, perturbation, and concurrency budgets across tests.
3. Capture evidence that another person can replay without your notes.
4. Execute an unexpected success safely: stop, preserve, report, and do not explore.
5. Record failures and near misses as first-class results.

## 1. A plan is a sequence of falsifiable hypotheses

An attack hypothesis says: under this access and budget, this action will produce this observable effect. It must be possible for the answer to be no.

| Weak plan item | Why it fails | Testable version |
|---|---|---|
| "Try injection" | No oracle, no target, no budget | "A record with `tenant_id` in the body overrides the authenticated tenant; oracle is a 200 response whose decision differs from the same record scored under the caller's tenant" |
| "Test rate limits" | No threshold, no consequence | "300 requests in 60 s from one key produce fewer than 300 decisions; oracle counts 429 responses" |
| "Check auth" | Cannot fail | "A request with no `Authorization` header returns a decision rather than 401; oracle is status code and body" |
| "Try evasion" | No budget or metric | "Changing up to 3 merchant-controlled features within observed percentiles lowers the target segment block rate below 0.10 while global false-decline stays ≤ 0.02" |
| "Extract the model" | No fidelity target | "A surrogate trained on 1,500 label queries agrees with the target on ≥ 0.90 of a 500-record holdout" |

The technique comes after the hypothesis. A hypothesis about tenant isolation can be tested with a single forged request; a hypothesis about evasion needs a search procedure. Choosing the tool first inverts the experiment.

## 2. The ML API kill chain

For an application-level exercise, a simple chain is enough to order the work. Each stage narrows what the next can attempt.

| Stage | Question | Example activity | Evidence produced |
|---|---|---|---|
| 1. Enumerate | What is reachable? | Read the brief; probe `/health`; confirm ports | Endpoint inventory |
| 2. Map boundaries | Where does trust change? | Unauthenticated request; wrong-tenant key; malformed body | Boundary map with status codes |
| 3. Establish access | Can I act as a legitimate user? | Use the synthetic key; create a key through `/keys` | Access record |
| 4. Exploit | Can I exceed my authority or shift a decision? | Forge tenant, exceed bounds, evade, extract | Attack results |
| 5. Objective | Did I get the decision or data I should not have? | Compare against the oracle | Finding with reproduction |
| 6. Preserve | Can someone else replay it? | Save requests, seeds, logs, script | Evidence package |

Stages 1–3 are cheap and should be done first. They also produce the benign-looking traffic that makes stage 4 interpretable.

### What "exploit" does not include

In RT-01, exploitation stops at the target's documented surface. If a request returns a stack trace, that is a finding about error handling. Following the path in the trace into the host filesystem is out of scope. Record it, stop, and report.

## 3. Budgets and budget accounting

A budget is only real if it is counted. RT-01 has five.

| Budget | Limit | Counted by | Exhausted action |
|---|---|---|---|
| Requests | 2,000 total | Client-side counter | Stop; report partial |
| Time | 4 hours | Session clock | Stop at 150% (6 h) |
| Perturbation | 3 features per record; 1st–99th percentile | Script validation | Reject the record |
| Concurrency | 50 in flight | Client semaphore | Queue, do not raise |
| Attempts per test | Stated per test | Test log | Mark "inconclusive at budget" |

### Allocate before you start

| Test | Hypothesis | Request budget | Attempts | Time |
|---|---|---:|---:|---:|
| A-01 | Unauthenticated request is rejected | 20 | 1 | 5 min |
| A-02 | Cross-tenant body field is ignored | 40 | 2 | 10 min |
| A-03 | Malformed and oversized input is rejected safely | 60 | 3 | 15 min |
| A-04 | Quota is enforced per key | 400 | 2 | 30 min |
| A-05 | Evasion within feature bounds shifts a segment | 900 | 3 | 90 min |
| A-06 | Threshold can be approximated by querying | 500 | 2 | 45 min |
| A-07 | Admin rollback requires the admin credential | 30 | 2 | 10 min |
| Reserve | Unexpected follow-ups | 50 | — | 20 min |

The reserve matters. An unexpected result is a reason to spend the reserve on one controlled follow-up, not a reason to ignore the budget.

### Budget honesty

Report the budget you used, not the budget you planned. If A-05 consumed 1,400 requests because the search was inefficient, say so. An attack that succeeds at 1,400 requests is a weaker finding than one that succeeds at 40, and the reader needs the number to judge severity.

## 4. The attack library for RT-01

Seven tests exercise the main boundary families. They are deliberately ordinary; the exercise is about measurement, not novelty.

### A-01 — Authentication enforcement

```text
Hypothesis: /score returns 401 for requests with no Authorization header
            and for requests with a malformed or expired key.
Procedure:  Send four requests: no header, empty bearer, malformed bearer,
            and a well-formed but unknown key. Record status and body.
Budget:     20 requests, 1 attempt.
Oracle:     All four return 401 or 403, with no decision in the body.
Evidence:   requests/a01.jsonl, responses/a01.jsonl, result note.
```

### A-02 — Tenant isolation

```text
Hypothesis: A request authenticated as tenant T cannot obtain a decision
            for a record whose body claims tenant U.
Procedure:  Score the same synthetic record three ways: with body tenant T;
            with body tenant U; with no tenant field. Compare decisions and
            response metadata. A differing decision for U is the signal.
Budget:     40 requests, 2 attempts (one with a field, one with a header).
Oracle:     Response for U either rejected, or identical to T's decision
            with T's metadata. Any U-specific decision is a failure.
Evidence:   requests/a02.jsonl, responses/a02.jsonl, diff table.
```

### A-03 — Input validation

```text
Hypothesis: /score rejects NaN, infinity, negative amounts, strings in
            numeric fields, and payloads over the documented size limit,
            without echoing internal errors.
Procedure:  One request per malformed class, plus one oversized payload at
            the documented limit + 1 KB.
Budget:     60 requests, up to 3 attempts per class.
Oracle:     4xx with a generic message; no stack trace, path, or SQL.
Evidence:   responses/a03.jsonl; list of leaked strings if any.
```

### A-04 — Quota enforcement

```text
Hypothesis: A single key cannot obtain more than the documented 100
            decisions per minute; excess requests receive 429.
Procedure:  Send 400 well-formed requests in 60 s with one key; count 200
            and 429 responses; confirm the service remains responsive after.
Budget:     400 requests; concurrency ≤ 20; duration ≤ 90 s.
Oracle:     At most 100 decisions; at least one 429; /health responds after.
Evidence:   quota.csv (timestamp, status), summary.
```

Note the concurrency cap: the test measures quota enforcement, not the host's ability to survive a flood. Those are different hypotheses, and only the first is in scope.

### A-05 — Evasion within feature bounds

```text
Hypothesis: For the target segment (merchant category M, amount band B),
            changing up to three merchant-controlled features within the
            observed 1st–99th percentile lowers the block rate below 0.10
            while global false-decline stays ≤ 0.02.
Procedure:  Freeze a 1,000-record evaluation set; confirm the clean block
            rate; run a bounded search over the three features; rescore;
            report segment and global rates with a 95% interval.
Budget:     900 requests, 3 restarts, 3 features.
Oracle:     Segment block rate < 0.10 at global false-decline ≤ 0.02.
Evidence:   eval set hash, search log, results CSV, script, seed.
```

### A-06 — Extraction-style querying

```text
Hypothesis: 500 label queries are enough to train a surrogate that agrees
            with the target on ≥ 0.90 of a 500-record holdout.
Procedure:  Query random and boundary-adjacent records; train a small
            model; measure agreement; repeat with a second sampling scheme.
Budget:     1,000 queries total (two schemes × 500).
Oracle:     Agreement ≥ 0.90 on the holdout.
Evidence:   queries.jsonl, surrogate metrics, holdout hash.
```

### A-07 — Administrative action

```text
Hypothesis: /admin/rollback rejects a normal scoring key and accepts only
            the synthetic admin credential, and the action is logged.
Procedure:  Attempt rollback with no key, a scoring key, and the admin key.
            Inspect the service log for an entry with actor, time, action.
Budget:     30 requests, 2 attempts.
Oracle:     Two rejections, one success, one complete log entry.
Evidence:   responses/a07.jsonl, log excerpt.
```

These seven cover authentication, authorization, validation, availability, integrity, confidentiality, and audit. They do not cover everything; the report's limitations section says what is missing.

## 5. Evidence capture

If it is not logged, it did not happen. Capture at the moment of the request, not from memory afterward.

| Artifact | Content | Why |
|---|---|---|
| `run.json` | Run ID, start/end, seed, commit hash, config path, budget | Binds results to a version |
| `requests/<test>.jsonl` | Method, URL, headers (redacted), body, timestamp | Replay |
| `responses/<test>.jsonl` | Status, latency, body hash (and body if safe) | Oracle input |
| `result.md` per test | Hypothesis, observed, verdict, budget used | Interpretation |
| `replay.sh` | One command per test | Reproduction |
| `negative.md` | Tests that did not work and why | Prevents repetition |

### Redaction

Log the header names and a fingerprint, not the secret values. A synthetic key is still a key; do not copy it into a report that might be shared. Record `Authorization: Bearer <redacted sha256:ab12…>`.

### Record the negative results

A failed attack is evidence that a control held **under this test**. It is not evidence that the control is sound. Write the distinction:

- "A-02 did not produce a cross-tenant decision in 40 requests using body and header manipulation."
- Not: "Tenant isolation is secure."

The first is a measurement. The second is a claim the test cannot support.

## 6. Executing the sequence

### Preflight (10 minutes)

1. Confirm the service is the local mock: resolve the host, print the base URL, check `/health`.
2. Confirm egress is unnecessary: the script should fail if the host is not `127.0.0.1`.
3. Freeze the evaluation set and hash it.
4. Start the request counter and the session clock.
5. Write the first journal entry: plan ID, budget, start time.

### One variable at a time

When a test fails, change one thing: the payload, the header, the feature, the timing. If two things change and the result flips, you have learned nothing about which mattered.

### When something succeeds unexpectedly

An unexpected success is the moment the exercise is most likely to go wrong. Apply the same four steps every time:

1. **Stop.** Do not send another request along the new path.
2. **Preserve.** Save the exact request, response, and timestamp.
3. **Check scope.** Is the path still inside the target and data rules?
4. **Report.** Log it; if it is outside scope, stop and notify the lead.

The temptation is to "just confirm it once more." Confirmation is a new request; make it deliberately, within budget, after the scope check.

### When a test is inconclusive

Mark it inconclusive at budget, not failed. "No effect observed in 900 requests" and "the attack failed" are different claims. The first is honest; the second overstates the evidence.

## 7. Worked example — a four-hour session

| Time | Activity | Output |
|---|---|---|
| 0:00–0:10 | Preflight, freeze eval set, start clock | `run.json`, eval hash |
| 0:10–0:25 | A-01, A-02 | Two result notes |
| 0:25–0:40 | A-03, A-07 | Two result notes |
| 0:40–1:10 | A-04 quota test | `quota.csv` |
| 1:10–1:20 | Break; review budget | Journal update |
| 1:20–2:50 | A-05 evasion search | Results CSV, plot |
| 2:50–3:35 | A-06 extraction | Surrogate metrics |
| 3:35–3:50 | Reserve: one follow-up on the strongest signal | Follow-up note |
| 3:50–4:00 | Freeze logs, write session summary, stop | `session-01.md` |

The schedule leaves no time for "one more idea." That is deliberate. The reserve is the only unstructured time, and it is bounded.

## 8. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Tool-first plan | Tests do not answer the objective | Hypothesis, then technique |
| No per-test budget | One test consumes the session | Allocate before starting |
| Counting only successes | Budget report is wrong | Count every request |
| Logging after the session | Evidence is reconstructed | Log at request time |
| Storing secrets in logs | Report leaks credentials | Redact; hash |
| Exploring an unexpected path | Out-of-scope access | Stop, preserve, check, report |
| Calling a null result "secure" | Overclaim | "No effect observed at this budget" |
| Changing several variables | Confounded result | One variable at a time |
| No replay script | Findings cannot be reproduced | Script every test |
| Skipping preflight | Traffic goes somewhere unintended | Host check before the first request |

## 9. Check your understanding

1. What makes an attack hypothesis falsifiable? Give a weak and a strong example.
2. Name the five budgets in RT-01 and how each is counted.
3. Why is a failed attack not evidence that a control is secure?
4. What are the four steps after an unexpected success?
5. Why should the evaluation set be frozen and hashed before the attack?
6. What does "inconclusive at budget" mean, and why is it better than "failed"?

## 10. What you keep

An ordered attack plan with seven hypotheses, a budget allocation table, a request/response log, a replay script, per-test result notes, and a negative-results record. Lesson 17.3 uses the traffic and the timeline to build detections.

## 11. Next

Lesson 17.3 switches sides: telemetry design, detection hypotheses, calibration against quiet traffic, and a response runbook with time-to-detect and time-to-contain.
