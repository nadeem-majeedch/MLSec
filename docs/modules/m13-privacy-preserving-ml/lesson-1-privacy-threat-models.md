# Lesson 13.1 — Privacy Threat Models and Why Anonymization Fails

<a id="m13-l1"></a>

**Module 13 · Lesson 1 of 5 · 2 hours · LO-19**

## Scenario

A hospital wants to publish a research dataset: patient age band, postal code, admission date, length of stay, and a readmission flag. Names, medical record numbers, and addresses are removed. The privacy review signs off because "there are no identifiers left."

A journalist links the table to a public voter file on postal code, age band, and admission date. Several rows become unique. One row matches a local news story about a named patient. The dataset is re-identified without anyone breaking an encryption key.

The identifiers were not removed. They were replaced by quasi-identifiers, and the auxiliary data needed to link them was already public.

## Objectives

By the end of this lesson you will be able to:

1. Distinguish membership, attribute, reconstruction, and linkage harms.
2. Explain how quasi-identifiers and auxiliary data defeat de-identification.
3. State why k-anonymity, aggregation, and synthetic data do not by themselves provide a privacy guarantee.
4. Write a privacy threat model with data, release, adversary, auxiliary knowledge, and harm.
5. Separate a formal guarantee from an empirical privacy measurement.
6. Describe what LAB-17 does and does not test.

## 1. Four harms

| Harm | Question answered | Example | Typical evidence |
|---|---|---|---|
| Membership | Was this person in the dataset? | "This record was in the HIV study" | Membership-inference AUC |
| Attribute inference | What is this person's sensitive value? | Inferring income from a loan model | Accuracy on a sensitive target |
| Reconstruction | What did the training data contain? | Recovering an image from gradients | Pixel or token similarity |
| Linkage / re-identification | Which person is this record? | Matching a table to a voter file | Unique match rate |

The harms are related but not interchangeable. A model can resist membership inference and still leak attributes. A dataset can be non-membership-revealing and still be linkable. A privacy evaluation should name the harm it measures.

Module 07 covered the attack mechanics in a centralized setting. This lesson focuses on the release decision: what is being shared, with whom, under what auxiliary knowledge.

## 2. Quasi-identifiers and auxiliary data

A **direct identifier** names a person: name, email, medical record number, national id. A **quasi-identifier** is not unique alone but becomes unique in combination: age, postal code, date of birth, admission date, job title, family size.

Sweeney's 2000 report estimated that 87% of the U.S. population could be uniquely identified by the combination of 5-digit ZIP code, gender, and date of birth. The exact figure depends on the population and the date; the structural lesson does not. A small combination of ordinary attributes can single out a person.

Linkage requires auxiliary data. The adversary already holds a public or purchased dataset with the same quasi-identifiers and a direct identifier. It joins on the quasi-identifiers and attaches the identifier to the released row. Removing names from the release does nothing to prevent this; the names come from the auxiliary data.

| Defense | What it removes | Why it fails |
|---|---|---|
| Remove names | Direct identifier | Quasi-identifiers remain |
| Generalize age to bands | Some precision | Bands can still be unique with postal code and date |
| Suppress rare rows | Some uniqueness | Suppression is visible and can leak |
| Aggregate to counts | Individual rows | Small counts and differencing leak |
| Synthetic data | Direct copies | Generative models can memorize or approximate |
| Add random noise without accounting | Exact values | No bound on what repeated releases reveal |

## 3. Why k-anonymity is not enough

k-anonymity requires every record to be indistinguishable from at least \(k-1\) others on the quasi-identifiers. It reduces uniqueness. It does not address:

- **Homogeneity:** if all \(k\) records in a group share the sensitive value, the group reveals it.
- **Background knowledge:** an adversary who knows a target is in a group can infer the group's sensitive value.
- **Composition:** linking multiple k-anonymous releases can re-identify.
- **Choice of quasi-identifiers:** an attribute omitted from the model can still be auxiliary data.

l-diversity and t-closeness extend the idea, and each adds assumptions. None of them is a formal guarantee against an adversary with arbitrary auxiliary knowledge. That is what differential privacy is designed to provide.

## 4. Aggregation and differencing

Publishing only counts feels safer. It is not automatically safe.

| Release | Risk |
|---|---|
| Count of patients with a condition in a small cell | The count may be 1 or 2; the cell reveals an individual |
| Two releases with and without one person | The difference isolates that person |
| A mean over a small group | The mean plus \(n-1\) known values reveals the last |
| A histogram with rare bins | Rare bins are effectively individual records |
| A model trained on a small cohort | The model can memorize or overfit |

Differencing is the key pattern: if an adversary can obtain two releases that differ by one record, the difference is a release about that record. Composition accounting exists because repeated releases accumulate risk.

## 5. Synthetic data is not automatically private

A generative model trained on sensitive records can reproduce them, especially rare ones. A synthetic dataset can also preserve statistical relationships that enable attribute inference. "Synthetic" describes the generation process, not the privacy property.

There are two defensible positions:

1. Train the generator with a formal privacy guarantee (for example, DP-SGD) and account for the budget; or
2. Treat the synthetic data as sensitive and evaluate it with the same linkage and inference tests as the original.

A synthetic dataset that has never been attacked is not evidence of privacy.

## 6. A privacy threat model

Write five lines before choosing a mechanism.

| Field | Question | Example |
|---|---|---|
| Data | What records, and who is in them? | 12,000 admissions, 2019–2024 |
| Release | What exactly is published or shared? | Per-cohort readmission rates and a trained model |
| Unit | Whose change must be hidden? | One patient, or one hospital |
| Adversary | What does the attacker know and see? | Public voter file, access to the model API |
| Harm | What outcome matters? | Re-identification, stigma, insurance discrimination |

Then add the mechanism and the guarantee:

| Field | Question | Example |
|---|---|---|
| Adjacency | What counts as a neighboring dataset? | Add or remove one patient |
| Mechanism | How is randomness introduced? | Laplace noise on each cohort count |
| Parameters | What are \(\varepsilon\) and \(\delta\)? | \(\varepsilon=0.5\), \(\delta=0\) |
| Composition | How many releases, and how do they combine? | Monthly for 12 months, sequential |
| Residual | What is outside the guarantee? | Linkage to an external file using released cohort labels |

The last row is important. DP protects the output of the mechanism under the stated adjacency. If the release also includes a non-private field, or if the cohort definition itself is sensitive, the guarantee does not cover it.

## 7. Formal versus empirical

| Evidence | What it shows | What it does not show |
|---|---|---|
| DP proof for a mechanism | A bound on output-distribution change | That the implementation matches the proof |
| Membership AUC near 0.5 | One attack failed on one split | That no attack can succeed |
| Reconstruction error | One reconstruction attempt was inaccurate | That the data is private |
| Linkage match rate | One auxiliary dataset failed to match | That no auxiliary data exists |
| Red-team report | Named attacks were tested | That unnamed attacks will fail |

An empirical result is a measurement under a threat model. A formal result is a bound under a threat model. Neither substitutes for the other. The strongest documentation includes both, and states the gap between the proof and the code.

## 8. LAB-17's threat model

LAB-17 is deliberately narrow:

| Field | LAB-17 |
|---|---|
| Data | Two synthetic Gaussian classes, 4 features, 800 rows per class |
| Release | Two clipped centroids with Laplace noise |
| Unit | One row |
| Adversary | Sees the released centroids, knows the generative family, tries to decide membership by distance |
| Harm proxy | Membership inference via distance to the nearest centroid |
| Mechanism | Laplace, per-coordinate noise scale \(\Delta_1/\varepsilon\) |
| Composition | Parallel over disjoint class datasets |
| What is not tested | Linkage, attribute inference, reconstruction, side knowledge, implementation bugs |

The membership test is intentionally simple: compute the distance from a candidate row to its class centroid and compare members with nonmembers. A more powerful attacker might use the known generative model, multiple releases, or the clipping pattern. The lab reports near-chance AUC and states that this is not a proof.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Treating removed names as anonymization | Names are the obvious identifier | Enumerate quasi-identifiers and auxiliary sources |
| Assuming small groups are safe | Aggregation feels protective | Check small counts and differencing |
| Trusting synthetic data | It does not look like the original | Evaluate it like the original |
| Confusing k-anonymity with DP | Both are privacy models | State the adversary each assumes |
| Reporting AUC as proof | It is the available metric | Call it empirical and name the attack |
| Ignoring the release channel | The model is "just a model" | Include API access and repeated queries |
| Forgetting the unit | "Privacy" is vague | State whether one row or one client |
| Omitting the residual row | The mechanism looks complete | Name what the guarantee does not cover |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Re-identification despite removed names | Quasi-identifiers and auxiliary data | Generalize, suppress, or use a formal mechanism |
| Small-cell counts leak | Rare categories | Suppress or noise the cells; account for the release |
| Synthetic rows match real rows | Memorization | Use DP training or stronger generation controls |
| Threat model cannot name the adversary | The release purpose is vague | Write the use case and the attacker |
| Empirical attack is weak | The attack is not adapted | Strengthen it before drawing conclusions |
| Formal claim cannot be verified | No mechanism or parameters documented | Record mechanism, sensitivity, epsilon, delta |

## Check your understanding

1. Give an example of a quasi-identifier that is not a direct identifier.
2. Why does removing names not prevent linkage?
3. What does k-anonymity fail to protect against, and why?
4. How can two aggregate releases leak an individual?
5. Why is synthetic data not automatically private?
6. What is the difference between a DP guarantee and a membership AUC near 0.5?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Privacy harms include membership, attribute inference, reconstruction, and linkage. Name the one you are addressing.
- Quasi-identifiers plus auxiliary data defeat de-identification.
- k-anonymity, aggregation, and synthetic data reduce some risks and do not provide a formal guarantee.
- A privacy threat model states data, release, unit, adversary, and harm.
- A DP guarantee bounds output-distribution change under an adjacency definition. An empirical attack measures one attempt.
- LAB-17 tests a narrow centroid release with a distance-based membership probe and explicitly limits its claims.

## Next

Continue to [Lesson 13.2 — Differential privacy from first principles](lesson-2-differential-privacy-first-principles.md), where the guarantee is defined and the noise is computed.
