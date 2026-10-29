# About the Instructor

<span class="mlsec-kind">About</span>

## Engr. Dr. Muhammad Nadeem Majeed

**Professor**
Department of Data Science (PUCIT)
University of the Punjab, Lahore

PUCIT is the Punjab University College of Information Technology. ML-Sec is written and maintained by Engr. Dr. Muhammad Nadeem Majeed as a self-study course for people who need to measure machine-learning security, not merely describe it.

## Why the course is built this way

Most ML curricula teach a model to be accurate. Most security curricula teach a network or an application to resist attack. ML-Sec sits where those two meet: the data distribution is an attack surface, the model is an artifact that can be stolen or trojaned, and the prediction API is both a product and an oracle.

The course therefore repeats one discipline in every module:

> **Model the adversary, measure the effect, engineer the control, and re-test.**

That discipline shows up as four teaching choices:

| Choice | What it means for you |
|---|---|
| Threat model before code | You state the attacker's goal, knowledge, capability, budget, base set, and metric before you run anything |
| Measurement over demonstration | “The attack worked” is replaced by a number with a denominator, a budget, and a limitation |
| Reproducibility as a requirement | Pinned environments, fixed seeds, manifests, and a command another person can run |
| Safety as part of the method | Local, synthetic, or sandbox targets; benign payloads; authorized use only |

The labs are the course. Reading makes them intelligible; the artifacts make the learning inspectable. A learner who finishes should be able to hand another engineer a threat model, a bounded experiment, a defense evaluation, and an honest statement of residual risk.

## What this course is not

- It is **not a certification**. Completing the modules, labs, or capstone does not certify you, and it does not certify that any organization complies with NIST, ISO/IEC, OWASP, MITRE ATLAS, the EU AI Act, or any other framework. The [framework mapping](framework-mapping.md) shows where topics align; alignment is not compliance.
- It is **not legal advice**. The rules of engagement and responsible-use guidance are teaching material. Authorization, data protection, and disclosure obligations depend on your jurisdiction and your organization.
- It is **not a license to test third-party systems**. Every offensive lab targets a model or service you build locally. If you are unsure whether a target is authorized, it is not.
- It is **not a substitute for a supervised assessment**. The course teaches a method and gives you self-checks; a qualified reviewer is still the right person to judge a production system.

## How the site and materials are published

The course is a static site built from Markdown with MkDocs Material and served from a GitHub project path. The site has no accounts, no database, no analytics, and no paid service. Search runs in your browser. The labs run on your machine with the pinned Python stack and bundled or synthetic data.

The [course repository](https://github.com/nadeem-majeedch/MLSec) holds the source, lab packages, starter code, reference implementations, and checkers. The repository is the authoritative copy when a page and a lab package disagree.

## Corrections and communication

Corrections are welcome through the repository's issue tracker. A useful report names the page address, the exact command or sentence, what you expected, and what happened. Please do not post credentials, personal data, or confidential material in an issue.

For a security issue in the course materials themselves, follow coordinated disclosure: report it privately to the repository owner, allow reasonable time for a fix, and do not publish an exploit before remediation. The course's own safety rules are in the [student guide](student-guide.md#safety).

## Where to start

- New to the subject: [Learning paths](learning-paths.md), then [Module 00](modules/m00-orientation/index.md).
- Choosing a route by available time: [Student guide — schedules](student-guide.md#schedules).
- Checking what the course covers: [Course roadmap](modules/index.md) and [Learning outcomes](learning-outcomes.md).
- Reading the research behind it: [References](references.md) and the [research reading guide](research-reading-guide.md).
