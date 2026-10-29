# LAB-02 Report Template

Fill in every section. Keep the headings; the checker looks for them. The YAML model is the machine-checkable register; this report is the explanation a colleague can read.

## System and scope

- What the system does, who uses it, and the decision it influences.
- What is in scope and what is explicitly out of scope.
- One sentence on why the system is a decision-support tool rather than an autonomous one.

## Data-flow diagram

- A Mermaid `flowchart` with actors, stores, services, and at least four labelled trust boundaries.
- Label each boundary `TB1`, `TB2`, and so on; use the same IDs as the YAML.

## Assets

- Table: ID, asset, why it matters, CIA, sensitivity.
- At least six assets, including data, model, credentials, and availability.

## Trust boundaries

- Table: ID, boundary, what it separates, primary controls.
- At least five boundaries; each must have at least one surface in the threat register.

## Attack surfaces

- Table: ID, surface, boundary, entry point, who can reach it.
- At least eight surfaces.

## Adversary model

- Table: actor, goal, knowledge, capability, assumed limit.
- State what the adversary is **not** assumed to have.

## Threat register

- Table: ID, threat, status, NIST goal, class, lifecycle stage, likelihood × impact, severity, residual risk.
- At least nine accepted threats and at least one rejected threat with reasoning.
- All five lifecycle stages and all four NIST goals must appear.
- At least six distinct attack classes.

## Attack trees

- Three trees, each with a root goal and at least three steps.
- Every step names the threat ID it depends on.

## Mitigations and residual risk

- For each top threat: preventive, detective, and corrective controls.
- A residual-risk rating with one sentence of justification.
- At least one detection hypothesis per accepted threat, expressed as a metric and a threshold.

## Framework crosswalk

- NIST AI RMF: one line for GOVERN, MAP, MEASURE, and MANAGE.
- OWASP ML Top 10: at least four entries mapped to threat IDs.
- OWASP LLM Top 10: state applicable or not, with a reason.

## Assumptions and rejected threats

- List the assumptions that, if false, would change the ranking.
- Explain the rejected threat and what would reopen it.

## Reproduction

- Commands to run the checker.
- What the checker validates and what it does not.
