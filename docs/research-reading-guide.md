# Research reading guide

Security papers are written for other researchers, not for students. They assume you know the attack family, the standard baseline, and why the threat model matters. This guide gives you an order to read in, tells you what to extract from each source, and warns you about the claims that are easiest to misread.

The path runs from orientation to advanced work. You do not need to finish it to pass the course. You do need the first two stages to write a defensible lab report, and the later stages if you attempt the capstone or a research extension.

## How to read a paper

Start with **R-09**, Keshav, *How to Read a Paper* (2007). It describes a three-pass method: a five-minute skim for the claim and structure, a one-hour read for the argument and evidence, and a deep read only for papers you must reproduce or critique.

Use the passes differently in security:

| Pass | What you are looking for | Stop if |
|---|---|---|
| 1. Skim | Title, abstract, figures, threat model, headline result | You cannot state the adversary's goal in one sentence |
| 2. Read | Method, experimental setup, baselines, limitations | The paper never states what the attacker knows or can do |
| 3. Reconstruct | Re-derive the metric, check the split, test an assumption | You cannot reproduce the headline number from the description |

Before any pass, read the **threat model**. In this field, most apparent contradictions between papers disappear when you compare the adversaries they assume. A defense that looks strong against a weak attacker may be irrelevant against an adaptive one.

!!! note "Preprints and versions"
    Most research entries in [References](references.md) link to arXiv. An arXiv link is a **preprint** unless the entry names a venue. Preprints are not peer-reviewed at the time of posting, and the final published version can differ in method, numbers, or framing. When a venue is named in the reference entry, treat the venue version as the version of record. When it is not, say "preprint" in your own citation and give the arXiv identifier and the year on the abstract page.

## Stage 0 — Orient with frameworks (light reading)

Read these before the papers. They give you the vocabulary the papers assume, and they are more current than most surveys.

| Source | What to look for |
|---|---|
| [F-01](references.md#frameworks-standards-and-guidance) NIST AI 100-2 E2025 | The five impact classes, the difference between attack type and impact, and the definitions of adversary knowledge and capability. Do not read it cover to cover on the first pass; read the taxonomy index and the sections for the attacks you are studying. |
| [F-02](references.md#frameworks-standards-and-guidance) MITRE ATLAS v2026.09 | How tactics and techniques are separated, and how a technique page lists mitigations and case studies. Pick one technique you have run in a lab and trace it to its case studies. |
| [F-07](references.md#frameworks-standards-and-guidance) OWASP Top 10 for LLM Applications 2025 | The ten categories as the course uses them. Note that the 2026 edition renumbers the list; use the [crosswalk](framework-mapping.md#31-llm-application-risks-2025-taught-ids-and-2026-crosswalk) rather than mixing IDs. |
| [F-03](references.md#frameworks-standards-and-guidance) NIST AI RMF 1.0 | GOVERN, MAP, MEASURE, MANAGE. Read the function descriptions, not the whole document. |
| [R-01](references.md#foundations-and-surveys) Biggio & Roli, *Wild Patterns* (2017) | The historical frame: evasion, poisoning, and privacy as one field. Read the introduction and the taxonomy figures. This is a survey, not a new result. |

**What to extract.** A one-page vocabulary sheet: the impact classes, the adversary knowledge levels, and the names of the attack families. You will reuse it in every lab report.

## Stage 1 — Foundations (the papers that defined the problems)

| ID | Paper | Effort | What to look for |
|---|---|---|---|
| [R-02](references.md#foundations-and-surveys) Biggio et al., *Evasion Attacks against Machine Learning at Test Time* | Moderate | The original evasion formulation. Note how attacker knowledge is parameterized and why the attack is an optimization problem. This is the ancestor of every gradient attack you run. |
| [R-10](references.md#evasion-and-robustness) Szegedy et al., *Intriguing properties of neural networks* | Moderate | The existence result: imperceptible perturbations change predictions. Note what the paper does **not** claim about physical feasibility or defense. |
| [R-11](references.md#evasion-and-robustness) Goodfellow et al., *Explaining and Harnessing Adversarial Examples* | Light | The linearity hypothesis and the FGSM derivation. Check the assumption behind the linearization; it is the reason FGSM is fast but not the strongest attack. |
| [R-13](references.md#evasion-and-robustness) Kurakin et al., *Adversarial examples in the physical world* | Moderate | The gap between a digital perturbation and a camera. Look at the printing and photographing assumptions, and at which of them would fail in your lab. |
| [R-12](references.md#evasion-and-robustness) Papernot et al., *The Limitations of Deep Learning in Adversarial Settings* | Moderate | Targeted, saliency-based, few-pixel perturbation. Note the difference between \(L_0\) style attacks and the \(L_\infty\) attacks you run in LAB-03. |

**What to extract.** For each paper: the adversary's goal, knowledge, and capability; the metric; the baseline; and one assumption that would break the result. Write the assumption down even when the paper does not label it as a limitation.

## Stage 2 — The attack families you actually run

### Evasion

| ID | Paper | What to look for |
|---|---|---|
| [R-14](references.md#evasion-and-robustness) Carlini & Wagner, *Towards Evaluating the Robustness of Neural Networks* | The optimization formulation and the three distance metrics. This became a standard strong baseline; note the cost of the optimization and the defenses it defeated. |
| [R-15](references.md#evasion-and-robustness) Moosavi-Dezfooli et al., *DeepFool* | Minimal perturbation via iterative linearization. Compare its perturbation size with FGSM at the same success rate. |
| [R-16](references.md#evasion-and-robustness) Moosavi-Dezfooli et al., *Universal adversarial perturbations* | One perturbation across many inputs. Note the data dependence and the assumption that the attacker can query the model. |
| [R-17](references.md#evasion-and-robustness) Brown et al., *Adversarial Patch* | Localized, printable attacks. Read the physical assumptions: distance, lighting, camera, and placement. |
| [R-20](references.md#evasion-and-robustness) Andriushchenko et al., *Square Attack* | Query-efficient score-based search. Note the query budget and the difference between score-based and decision-based access. |
| [R-21](references.md#evasion-and-robustness) Chen et al., *HopSkipJumpAttack* | Decision-based attacks with labels only. This is the closest match to a realistic API that returns only the predicted class. |

### Poisoning, backdoors, and availability

| ID | Paper | What to look for |
|---|---|---|
| [R-30](references.md#poisoning-backdoors-and-availability) Biggio et al., *Poisoning Attacks against Support Vector Machines* | The foundational poisoning formulation. Note the assumption of training-set access and the optimization over added points. |
| [R-31](references.md#poisoning-backdoors-and-availability) Gu et al., *BadNets* | The canonical trigger-based backdoor. Identify the trigger, the poisoning rate, and the clean-accuracy cost. |
| [R-32](references.md#poisoning-backdoors-and-availability) Chen et al., *Targeted Backdoor Attacks* | Targeted behavior from a small poisoned fraction. Compare the threat model with BadNets. |
| [R-33](references.md#poisoning-backdoors-and-availability) Liu et al., *Trojaning Attack on Neural Networks* (NDSS 2018) | Weight-level trojaning without full retraining. Note what access the attacker needs to the model. |
| [R-34](references.md#poisoning-backdoors-and-availability) Wang et al., *Neural Cleanse* | Trigger reverse-engineering and the anomaly index. Ask what happens when the trigger is large or the backdoor is clean-label. |
| [R-35](references.md#poisoning-backdoors-and-availability) Gao et al., *STRIP* | Detection by input perturbation and prediction entropy. Note the false-positive cost on benign inputs. |
| [R-36](references.md#poisoning-backdoors-and-availability) Liu et al., *Fine-Pruning* | Pruning plus fine-tuning as mitigation. Look for the assumption that the backdoor depends on a small set of neurons. |
| [R-37](references.md#poisoning-backdoors-and-availability) Tran et al., *Spectral Signatures* | Latent-space separability of poisoned examples. Check the assumption about the poisoned fraction and the target class. |
| [R-38](references.md#poisoning-backdoors-and-availability) Schwarzschild et al., *Just How Toxic is Data Poisoning?* | A unified benchmark. Use it to see how much reported effectiveness depends on the evaluation harness. |
| [R-40](references.md#poisoning-backdoors-and-availability) Tramèr et al., *Truth Serum* | Poisoning used to reveal secrets. A useful example of an attack that crosses category boundaries. |
| [R-41](references.md#poisoning-backdoors-and-availability) Shumailov et al., *Sponge Examples* | Availability and cost amplification, not accuracy loss. Note the metric: energy or latency, not error rate. |

### Extraction and inference

| ID | Paper | What to look for |
|---|---|---|
| [R-50](references.md#extraction-inference-and-privacy) Tramèr et al., *Stealing Machine Learning Models via Prediction APIs* | The API-as-oracle framing. Note the query budget and the difference between equation-solving and learning-based extraction. |
| [R-51](references.md#extraction-inference-and-privacy) Orekondy et al., *Knockoff Nets* | Extraction with a substitute dataset. Look at how the substitute data distribution affects fidelity. |
| [R-52](references.md#extraction-inference-and-privacy) Jagielski et al., *High Accuracy and High Fidelity Extraction* | Fidelity as a distinct metric. Ask why task accuracy and agreement with the target are not the same number. |
| [R-53](references.md#extraction-inference-and-privacy) Carlini et al., *Cryptanalytic Extraction* | Exact extraction from precision and query behavior. This is a strong assumption; note how far it is from a rate-limited API. |
| [R-56](references.md#extraction-inference-and-privacy) Shokri et al., *Membership Inference Attacks* | Shadow models and the membership threat model. Identify the shadow-model assumption and the target's output format. |
| [R-57](references.md#extraction-inference-and-privacy) Carlini et al., *Membership Inference from First Principles (LiRA)* | Likelihood ratios and low-FPR evaluation. This is the paper to read before trusting an AUC near 0.5. |
| [R-58](references.md#extraction-inference-and-privacy) Fredrikson et al., *Model Inversion* (ACM CCS 2015) | Confidence leakage and reconstruction. Note what the attacker must know about the target and the auxiliary data. |
| [R-59](references.md#extraction-inference-and-privacy) Zhang et al., *The Secret Revealer* | Generative priors make inversion stronger. Compare the assumptions with R-58. |
| [R-63](references.md#extraction-inference-and-privacy) Carlini et al., *Extracting Training Data from Large Language Models* | Memorization in language models. Look at how the authors define and verify extraction, not just at the headline examples. |
| [R-64](references.md#extraction-inference-and-privacy) Carlini et al., *Extracting Training Data from Diffusion Models* | Extraction from generative image models. Note the difference between near-duplication and semantic similarity. |

## Stage 3 — Defenses and honest evaluation

Read this stage before you claim any defense works.

| ID | Paper | What to look for |
|---|---|---|
| [R-18](references.md#evasion-and-robustness) Madry et al., *Towards Deep Learning Models Resistant to Adversarial Attacks* | PGD as both attack and training method. Note the min-max formulation and the cost of adversarial training. |
| [R-19](references.md#evasion-and-robustness) Athalye et al., *Obfuscated Gradients Give a False Sense of Security* | Why a defense can look robust and still be broken. Learn the three families of gradient masking; you will use them as a checklist. |
| [R-22](references.md#evasion-and-robustness) Croce & Hein, *Reliable evaluation with an ensemble of attacks* | AutoAttack. Note why a single attack is not an evaluation and how the ensemble reduces false robustness claims. |
| [R-23](references.md#evasion-and-robustness) Croce et al., *RobustBench* | Comparing robustness claims on common ground. Check what the leaderboard controls and what it does not. |
| [R-24](references.md#evasion-and-robustness) Carlini et al., *On Evaluating Adversarial Robustness* | The checklist for a credible robustness claim. Turn it into a review checklist for your own lab report. |
| [R-25](references.md#evasion-and-robustness) Cohen et al., *Certified Adversarial Robustness via Randomized Smoothing* | A certified \(L_2\) radius. Note precisely what is certified and what is outside the guarantee. |
| [R-26](references.md#evasion-and-robustness) Wong & Kolter, *Provable defenses* | Certification by convex relaxation. Note the computational cost and the looseness of the bound. |
| [R-27](references.md#evasion-and-robustness) Zhang et al., *TRADES* | The robustness–accuracy trade-off made explicit. Use it to explain why a robust model can be less accurate on clean data. |

**What to extract.** A defense evaluation worksheet: threat model, attack suite, adaptive attack, clean accuracy, robust accuracy, false-positive cost, compute cost, and the conditions under which the defense fails.

## Stage 4 — Privacy engineering

Read R-62 before R-60 if you want the formal definitions; read R-60 first if you want to see them applied.

| ID | Paper | What to look for |
|---|---|---|
| [R-62](references.md#extraction-inference-and-privacy) Dwork & Roth, *The Algorithmic Foundations of Differential Privacy* | The formal basis for \(\varepsilon\) and \(\delta\). Read the definitions and the composition theorems; skip the advanced mechanism chapters on a first pass. |
| [R-60](references.md#extraction-inference-and-privacy) Abadi et al., *Deep Learning with Differential Privacy* | DP-SGD: clipping, noise, and the moments accountant. Note what the guarantee covers and what it does not. |
| [R-61](references.md#extraction-inference-and-privacy) Papernot et al., *PATE* | Private learning through teacher ensembles. Compare the trust assumptions with DP-SGD. |
| [R-70](references.md#federated-generative-and-agentic-systems) McMahan et al., *Communication-Efficient Learning* | FedAvg, the baseline every federated attack targets. Note the assumption that the server never sees raw client data. |
| [R-74](references.md#federated-generative-and-agentic-systems) Bonawitz et al., *Practical Secure Aggregation* (ACM CCS 2017) | What secure aggregation hides and what it does not. It protects updates in transit from the server, not the trained model or the output. |

## Stage 5 — Data, pipelines, and supply chain

These are not attack papers in the same sense, but they explain why many failures are pipeline failures.

| ID | Paper | What to look for |
|---|---|---|
| [R-05](references.md#foundations-and-surveys) Sambasivan et al., *Data Cascades in High-Stakes AI* | Why data quality and pipeline defects are a security problem, not only an ML problem. Read the case studies for the failure chain, not just the headline. |
| [R-06](references.md#foundations-and-surveys) Kaufman et al., *Leakage in Data Mining* | The leakage taxonomy used in LAB-12. Learn to distinguish leakage from legitimate signal. |
| [R-07](references.md#foundations-and-surveys) Sculley et al., *Hidden Technical Debt in Machine Learning Systems* | Why glue code, configuration, and pipeline boundaries accumulate risk. This is a position paper; read it for the failure modes, not for measurements. |
| [R-08](references.md#foundations-and-surveys) Ohm et al., *Backstabber's Knife Collection* | How dependency and install-time compromise actually happens. A survey of real incidents; use it to justify a threat in LAB-13. |
| [R-100](references.md#research-practice-reproducibility-and-evaluation) Pineau et al., *Improving Reproducibility in ML Research* | The reproducibility checklist behind the capstone's run record. |
| [R-101](references.md#research-practice-reproducibility-and-evaluation) Kapoor & Narayanan, *Leakage and the Reproducibility Crisis* | Why a result can be reproducible and still invalid. Read this before you trust a benchmark comparison. |

## Stage 6 — Federated, generative, and agentic systems

| ID | Paper | What to look for |
|---|---|---|
| [R-71](references.md#federated-generative-and-agentic-systems) Bagdasaryan et al., *How To Backdoor Federated Learning* | A single malicious client can persist a backdoor. Note the attacker's control over local training and the aggregation assumptions. |
| [R-72](references.md#federated-generative-and-agentic-systems) Blanchard et al., *Krum* (NeurIPS 2017) | Robust aggregation and its assumptions. Ask what fraction of clients must be honest. |
| [R-73](references.md#federated-generative-and-agentic-systems) Yin et al., *Byzantine-Robust Distributed Learning* | Trimmed mean and coordinate-wise robustness. Compare the assumptions with Krum. |
| [R-80](references.md#federated-generative-and-agentic-systems) Greshake et al., *Not what you've signed up for* | Untrusted content as an instruction channel. This is the indirect-injection paper behind LAB-19. |
| [R-81](references.md#federated-generative-and-agentic-systems) Zou et al., *Universal and Transferable Adversarial Attacks on Aligned Language Models* | Optimization-based jailbreak suffixes and transfer. Note the difference between a suffix attack and an instruction-hierarchy failure. |
| [R-82](references.md#federated-generative-and-agentic-systems) Wei et al., *Jailbroken* | Why safety training is not a security boundary. Read the competing-objectives explanation. |
| [R-83](references.md#federated-generative-and-agentic-systems) Carlini et al., *Are aligned neural networks adversarially aligned?* | The gap between alignment and adversarial robustness. |
| [R-84](references.md#federated-generative-and-agentic-systems) Wallace et al., *The Instruction Hierarchy* | A design pattern for instruction trust boundaries. This is the conceptual basis for separating system, developer, and retrieved content. |
| [R-85](references.md#federated-generative-and-agentic-systems) Debenedetti et al., *AgentDojo* | A dynamic test environment. Note how it measures utility and attack success together. |
| [R-86](references.md#federated-generative-and-agentic-systems) Debenedetti et al., *CaMeL* | Capability-based defense rather than prompt-level filtering. Compare its assumptions with LAB-20's approval gates. |

## Stage 7 — Explainability and fairness (specialization)

Read this stage if your capstone touches explanation stability, subgroup harm, or audit reporting.

| ID | Paper | What to look for |
|---|---|---|
| [R-90](references.md#explainability-and-fairness) Ribeiro et al., *LIME* | Local surrogate explanations. Note the sampling assumptions and the fidelity limits. |
| [R-91](references.md#explainability-and-fairness) Lundberg & Lee, *SHAP* | Additive attributions and the assumptions behind Shapley values. |
| [R-92](references.md#explainability-and-fairness) Adebayo et al., *Sanity Checks for Saliency Maps* | Model-randomization tests. This is the paper that shows an explanation can look meaningful and be nearly independent of the weights. |
| [R-93](references.md#explainability-and-fairness) Rudin, *Stop explaining black box models* | The case for inherently interpretable models. A position paper; read the argument, not the rhetoric. |
| [R-94](references.md#explainability-and-fairness) Slack et al., *Fooling LIME and SHAP* | Explanation manipulation when the attacker knows the method. This connects explainability to security directly. |
| [R-95](references.md#explainability-and-fairness) Hardt et al., *Equality of Opportunity* | Equalized odds and the trade-offs behind it. |
| [R-96](references.md#explainability-and-fairness) Chouldechova, *Fair prediction with disparate impact* | Why predictive parity and disparate impact can conflict. |
| [R-97](references.md#explainability-and-fairness) Kleinberg et al., *Inherent Trade-Offs* | An impossibility result. Read the assumptions before quoting the conclusion. |
| [R-99](references.md#explainability-and-fairness) Barocas et al., *Fairness and Machine Learning* | A book-length treatment. Use it as a reference, not as a single sitting. |

## Stage 8 — Research practice and the capstone

| ID | Source | What to look for |
|---|---|---|
| [R-09](references.md#foundations-and-surveys) Keshav, *How to Read a Paper* | The three-pass method. Re-read it when you start the capstone literature review. |
| [R-100](references.md#research-practice-reproducibility-and-evaluation) Pineau et al. | The reproducibility checklist. Use it to structure your run record. |
| [R-101](references.md#research-practice-reproducibility-and-evaluation) Kapoor & Narayanan | Leakage and invalid results. Use it to audit your own evaluation before you write conclusions. |
| [R-102](references.md#research-practice-reproducibility-and-evaluation) Ganguli et al., *Red Teaming Language Models* | What red-team evidence can and cannot establish, and how findings scale with effort. |
| [R-104](references.md#research-practice-reproducibility-and-evaluation) Brundage et al., *Toward Trustworthy AI Development* | Auditing, provenance, and verifiable claims for an assessment dossier. |

## Reading paths

You do not need to read everything. Pick the path that matches your current level.

| Path | Sequence | Purpose |
|---|---|---|
| **Core (everyone)** | R-09 → F-01 → R-01 → R-10 → R-11 → R-14 → R-18 → R-24 → R-30 → R-31 → R-50 → R-56 → R-60 | Enough to write a credible Level 2–3 lab report |
| **Defense** | Core → R-19 → R-22 → R-23 → R-25 → R-27 → R-36 → R-37 | Evaluating robustness and backdoor defenses |
| **Privacy** | Core → R-57 → R-58 → R-59 → R-62 → R-61 → R-63 → R-64 | Membership inference, inversion, DP, and extraction |
| **LLM and agents** | F-07 → R-80 → R-82 → R-84 → R-85 → R-86 → F-02 (technique pages) | Prompt injection, jailbreaks, and agent containment |
| **Research** | Core → R-100 → R-101 → R-09 (deep read) → two papers from your capstone topic | Capstone literature review and a defensible claim |

## What to look for in each section of a paper

| Section | Questions to ask |
|---|---|
| Abstract | What is the claim, and is it a new attack, a new defense, a measurement, or a survey? Is the claim about a specific model, dataset, and threat model? |
| Introduction | What problem is being solved, and what do the authors say is new? What do they concede is out of scope? |
| Threat model | Who is the adversary? What do they know? What can they do? What is the budget? What is the success metric? |
| Method | Is the method described well enough to reimplement? What are the hyperparameters, and are they justified or tuned on the test set? |
| Experiments | What are the baselines? Are they strong or straw men? Are results averaged over seeds? Are error bars reported? |
| Ablations | Which component actually causes the effect? Is the ablation controlling for the right variable? |
| Limitations | What do the authors admit? What did they omit that a reviewer would ask about? |
| Related work | Which prior result is the closest competitor, and why is the new result better? Is the comparison fair? |
| Appendix | Often contains the threat-model details, the full hyperparameters, and the failure cases. Read it before you cite a number. |

## Red flags in security papers and reports

- **No threat model, or a threat model that appears only in the appendix.** You cannot interpret the result without it.
- **One attack, one seed, one dataset.** A single run is an anecdote. Look for multiple seeds, multiple models, and a stated uncertainty.
- **A defense evaluated only against a non-adaptive attack.** This is the failure mode R-19 describes.
- **Accuracy reported without the attack success rate**, or an attack success rate with an undefined denominator.
- **A benchmark comparison across different threat models.** The numbers are not comparable.
- **"First to..." claims** without a serious related-work comparison.
- **A privacy claim without a threat model.** "Anonymized" is not a guarantee; ask against whom.
- **A robustness claim without a budget.** "Robust" means nothing without a norm, an epsilon, and an attack.
- **A citation to a blog post where a paper exists.** Read the paper.
- **A number with no run record.** If you cannot reproduce it, do not cite it as established.

## A reading log you can actually keep

For each paper, record six lines. This is enough to support a lab report or a literature review, and short enough that you will do it.

| Field | Example |
|---|---|
| Citation | Author, title, venue or arXiv ID, year |
| Claim | One sentence: what the paper establishes |
| Threat model | Goal, knowledge, capability, budget, metric |
| Evidence | Dataset, model, baselines, number of runs, uncertainty |
| Limitation | One assumption that would break the result |
| Use in my work | Which lesson, lab, or project claim it supports |

Store the log next to your lab notebook. When you write a report, cite from the log rather than from memory.

## From reading to citing

- Cite the **version you read**. If you read the arXiv preprint, say so and give the identifier; do not imply you read a peer-reviewed version you never opened.
- Give the **year on the source**, not the year you downloaded it.
- For frameworks, give the **edition and date** (for example, NIST AI 100-2 E2025, March 2025; ATLAS data release v2026.09; OWASP LLM Top 10 2025).
- Separate **what the paper measured** from **what you conclude**. "The paper reports X on dataset Y under threat model Z" is a citation; "therefore our system is secure" is an inference you must defend.
- If you could not verify a claim, write that down. An honest gap is better than an invented citation.

## Where to go next

- [References](references.md) — the full list, with the reason to read each entry.
- [Glossary](glossary.md) — plain-language definitions of the terms these papers use.
- [Framework mapping](framework-mapping.md) — how the papers map to NIST, ATLAS, and OWASP categories.
- [M18.4 — From project to research question](modules/m18-capstone-and-research/lesson-4-from-project-to-research-question.md) — turning a reading log into a capstone question.
