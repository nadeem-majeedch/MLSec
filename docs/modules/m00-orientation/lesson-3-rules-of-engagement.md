# Lesson 00.3 — Rules of Engagement

**Module 00 · 45 minutes · Complete Lessons 00.1 and 00.2 first**

## Scenario

A message arrives: "We saw your ML security posts. Our startup has a fraud model. Can you try to break it this weekend? We will send the API key." The request is flattering, urgent, and vague. There is no written scope, no named system owner, no data-handling agreement, and no statement of what happens if you find something.

This is not an opportunity. It is an unauthorized test waiting to happen. This lesson gives you a decision procedure you can apply before touching any system, including your own.

## Learning objectives

By the end of this lesson you will be able to:

1. Apply a five-part authorization test to a described engagement.
2. Write a scoped authorized-use and ethics statement for your lab work.
3. Distinguish acceptable data from data you must not use.
4. Describe the first three steps of responsible disclosure.

## The authorization test

A target is authorized only when **all five** conditions hold:

| # | Condition | Evidence you should be able to point to |
|---|---|---|
| 1 | **Ownership or permission** | You own the system, or the owner has given written permission |
| 2 | **Defined scope** | Named hosts, endpoints, model versions, time window, and excluded actions |
| 3 | **Lawful purpose** | Testing, research, or defense; not extortion, fraud, or harassment |
| 4 | **Safe handling** | No real personal data; no destructive actions; rate limits and stop conditions agreed |
| 5 | **Contact and disclosure path** | A named person to report findings to, and a remediation window |

If any condition is missing, the answer is **no** — or **ask**, never "probably fine."

### The course default

For every lab in this course, the default target is:

- a process running on your own machine;
- a synthetic dataset you generated;
- a public benchmark with a license that permits the use; or
- an explicitly public sandbox designed for practice.

The course never requires you to test a third-party production system, create an account, or use an API key.

## Worked example: an authorization function

The function below encodes the test. It is deliberately conservative: missing written scope on a third-party system produces `DENY`, and personal data produces `ASK` even when permission exists.

```python
def authorize(ownership: str, written_scope: bool, personal_data: bool, destructive: bool) -> str:
    if ownership == "third-party":
        return "DENY: third-party system without a course-approved sandbox"
    if destructive:
        return "DENY: destructive action outside course scope"
    if personal_data:
        return "ASK: replace with synthetic data or obtain a privacy review"
    if not written_scope and ownership != "public-sandbox":
        return "DENY: scope is not documented"
    return "ALLOW: local or public sandbox, non-destructive"


cases = [
    ("own", True, False, False),
    ("public-sandbox", False, False, False),
    ("third-party", True, False, False),
    ("client", True, True, False),
    ("own", True, False, True),
]
for case in cases:
    print(case, "->", authorize(*case))
```

Expected output:

```text
('own', True, False, False) -> ALLOW: local or public sandbox, non-destructive
('public-sandbox', False, False, False) -> ALLOW: local or public sandbox, non-destructive
('third-party', True, False, False) -> DENY: third-party system without a course-approved sandbox
('client', True, True, False) -> ASK: replace with synthetic data or obtain a privacy review
('own', True, False, True) -> DENY: destructive action outside course scope
```

Notice that written permission alone does not produce `ALLOW` for a third-party system. The course sandbox rule is stricter than the law in some jurisdictions; that is intentional. A conservative rule is easier to follow consistently.

## Data ethics

| Data | Use it? | Conditions |
|---|---|---|
| Synthetic records you generated | Yes | Document the generator and seed |
| Public benchmark with an open license | Yes | Record the license, version, and checksum |
| Public data containing personal information | Usually no | Aggregate, minimize, or replace; never attempt re-identification |
| Customer or patient data | No | Not permitted in this course, even with permission |
| Scraped data from a site that prohibits it | No | Terms of service and copyright still apply |
| A dataset a friend sent you "for research" | Ask | Provenance and license must be documented |

The rule is simple: **if you cannot explain where the data came from and why you may use it, do not use it.**

## Responsible disclosure

If you find a real vulnerability during authorized work:

1. **Stop testing.** Do not expand the scope to see how bad it is.
2. **Write a private report.** Include the affected version, a minimal reproduction, the impact, and a suggested fix. Do not include real user data.
3. **Contact the owner through the agreed channel.** Give a reasonable remediation window before any public discussion.
4. **Do not publish an exploit before a fix.** Coordinate the disclosure timeline with the owner.
5. **Keep records.** Preserve logs and correspondence; do not alter evidence.

If there is no agreed contact, the engagement was not authorized. That is why condition 5 exists.

## Using AI assistants

| Allowed | Not allowed |
|---|---|
| Ask for an explanation of a concept | Submit analysis you cannot defend line by line |
| Ask for help debugging an error | Fabricate results or citations |
| Ask for a test you might have missed | Paste private, proprietary, or restricted data |
| Ask for a code review | Generate attacks against systems you do not own |

Disclose material assistance in a short "Tools used" note: the tool, what you used it for, and what you verified yourself. An assistant's confidence is not evidence.

## Law and policy

This course does not provide legal advice. Laws differ by country and institution, and terms of service can prohibit actions that are technically possible. When the law, the platform policy, and the course rule disagree, follow the strictest one. If you are unsure whether a target is authorized, it is not.

## Your ethics and authorized-use statement

Copy this template into `work/m00/ethics-statement.md` and complete it before LAB-01.

```markdown
# Ethics and authorized-use statement

I, <name>, will use the techniques in ML-Sec only on:
- systems I own;
- local synthetic services and datasets;
- public sandboxes and benchmarks whose licenses permit this use.

I will not:
- test third-party production systems;
- use real personal, customer, or patient data;
- perform destructive actions or denial-of-service tests outside a lab;
- publish an exploit before coordinated disclosure.

For every lab I will record the target, the scope, the data source, and the stop conditions.
I understand that the course does not provide legal advice and that I am responsible for
complying with applicable law, institutional policy, and terms of service.

Signed: ____________________    Date: __________
```

## Common mistakes

| Mistake | Why it matters | Fix |
|---|---|---|
| Treating a public API as a sandbox | Public does not mean authorized for attack testing | Use a local replica |
| Assuming "research" grants permission | Research exemptions are narrow and jurisdiction-specific | Get written scope |
| Testing "just one request" beyond scope | Scope is not a suggestion | Stop at the boundary |
| Using real data because it is "already public" | Public personal data is still personal data | Aggregate or synthesize |
| Posting a finding before the fix | Can expose users and create legal risk | Coordinate disclosure |
| Letting an assistant write the whole report | You cannot defend it | Disclose and verify |

## Troubleshooting

| Situation | Response |
|---|---|
| The owner says "go ahead" in a chat but will not sign a scope | Ask for written scope; if refused, decline |
| The lab dataset download requires an account | Use the documented fallback; do not create a paid account |
| You accidentally receive real user data | Stop, do not open or copy it, notify the owner, delete your copy per their instruction |
| A public sandbox has no license | Treat it as not authorized for this course |
| You are unsure about a jurisdiction | Do not test; ask the course community for a safer alternative |

## Key terms

**Authorization**, **scope**, **rules of engagement**, **sandbox**, **personal data**, **provenance**, **responsible disclosure**, **remediation window**, **terms of service**, **ethics statement**.

## Summary

- Authorization requires ownership or written permission, defined scope, lawful purpose, safe handling, and a disclosure path.
- The course default is local, synthetic, or explicitly public; no paid accounts or API keys.
- Never use real personal, customer, or patient data.
- Disclosure is coordinated, private first, and never before a fix.
- Sign an ethics statement before your first lab and keep it in your portfolio.

## References

| Reference | Use |
|---|---|
| [NIST AI 100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | Terminology for adversary goals and impacts |
| [CISA/NCSC secure AI guidelines](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) | Lifecycle security and responsible practice |
| [OWASP AI Exchange](https://owaspai.org/) | Application security and privacy guidance |
| [GitHub coordinated disclosure guidance](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately) | A practical disclosure process |
| [Python `dataclasses`](https://docs.python.org/3/library/dataclasses.html) | Structuring scoped requests in code |

Next: complete the [knowledge check](quiz.md), the [exercises](exercises.md), and [LAB-01](../../labs/lab-01.md).
