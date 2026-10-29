# References

This is the student-facing reference list. It is curated, not exhaustive: every entry is meant to be read for a specific reason, and the frameworks are the ones the course actually uses.

All links were checked on **2026-10-28**. Publisher sites (ACM, ISO, and some DOI resolvers) may block automated checks and return 403 while resolving normally in a browser. Framework versions change faster than courses; re-verify before citing them in your own work.

**How the list was checked.** On 2026-10-28, a full sweep of the site's external URLs returned 198 HTTP 200, 5 HTTP 202, 15 HTTP 403 from publisher bot filters, and 14 local-lab or example domains that are not meant to resolve. After the reference pages were expanded, those five pages alone were re-swept: 144 unique external URLs, 133 HTTP 200, 2 HTTP 202, 9 HTTP 403 (ACM DOI and ISO bot filters), and no HTTP 404. A 403 from a publisher means the automated request was blocked; it does not by itself show that the link is dead. For research entries, each arXiv identifier was checked against the arXiv metadata API and each DOI against Crossref, and the returned title was compared with the title printed here. That check found two entries whose identifier pointed to a different paper; both are corrected below. The counts in the ATLAS entry were recomputed from the published `ATLAS-2026.09.yaml` release rather than copied from a secondary summary.

## How to use this list

- **Read primary sources.** A blog post about a paper is not the paper. The abstract and the experiments usually contain the caveats a summary drops.
- **Cite the version and date.** "ATLAS" is not a citation; "MITRE ATLAS, data release v2026.09" is. The same applies to OWASP lists and NIST documents.
- **Read the threat model first.** Most disagreements about a paper disappear once you compare the adversary each result assumes.
- **Do not cite what you have not opened.** This list is a starting point, not a substitute for reading.

**Companion pages.** [Glossary](glossary.md) explains the vocabulary. [Framework mapping](framework-mapping.md) connects the frameworks to modules and labs. [Research reading guide](research-reading-guide.md) gives a staged reading order. [Dataset catalog](dataset-catalog.md) records provenance, licenses, and access for every dataset mentioned in the course.

---

## Frameworks, standards, and guidance

| ID | Reference | Use it for |
|---|---|---|
| F-01 | Vassilev, A., Oprea, A., Fordyce, A., Anderson, H., Davies, X., & Hamin, M. *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations.* NIST AI 100-2 E2025, March 2025. [DOI](https://doi.org/10.6028/NIST.AI.100-2e2025) · [CSRC](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) | The vocabulary for adversary goals, knowledge, capabilities, and attack classes; the section structure is mapped in the [framework mapping](framework-mapping.md) |
| F-02 | MITRE ATLAS knowledge base, data release v2026.09 (published 2026-09-15; 16 tactics, 120 techniques, 88 sub-techniques, 40 mitigations, 73 case studies). [atlas.mitre.org](https://atlas.mitre.org/) · [atlas-data](https://github.com/mitre-atlas/atlas-data) | Mapping threats and detections to adversary tactics and techniques |
| F-03 | NIST. *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1, January 2023. [DOI](https://doi.org/10.6028/NIST.AI.100-1) | GOVERN, MAP, MEASURE, and MANAGE as a governance structure |
| F-04 | NIST. *AI RMF: Generative Artificial Intelligence Profile.* NIST AI 600-1, July 2024. [DOI](https://doi.org/10.6028/NIST.AI.600-1) | Generative-AI-specific risk framing |
| F-05 | NIST. *Secure Software Development Framework (SSDF) Version 1.1.* NIST SP 800-218, February 2022. [DOI](https://doi.org/10.6028/NIST.SP.800-218) | Secure development practices that apply to ML pipelines |
| F-06 | NIST. *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile.* NIST SP 800-218A, July 2024. [PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218A.pdf) | SSDF practices adapted to generative models |
| F-07 | OWASP GenAI Security Project. *OWASP Top 10 for LLM Applications 2025* (LLM01–LLM10). [Resource](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) · [Project index](https://genai.owasp.org/llm-top-10/) | The edition whose category IDs the course uses in M15 and LAB-19; the worked table is in M15.L1 |
| F-07A | OWASP GenAI Security Project. *OWASP GenAI LLM Top 10 2026*, v1.0, published 2026-08-04. [Resource](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) · [DOI](https://doi.org/10.5281/zenodo.22109015) | The current edition. It renumbers every category, so do not mix IDs across editions; the crosswalk is in the [framework mapping](framework-mapping.md) |
| F-08 | OWASP GenAI Security Project. *Agentic AI — Threats and Mitigations*, v1.1, December 2025. [Resource](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | Agent-specific threats, including excessive agency |
| F-09 | OWASP. *Machine Learning Security Top 10* (incubator project). [Project](https://owasp.org/projects/machine-learning-security-top-ten) · [Repository](https://github.com/OWASP/www-project-machine-learning-security-top-10) | ML-specific application risks; useful as a cross-check |
| F-10 | OWASP. *AI Exchange* (AI security and privacy guide). [owaspai.org](https://owaspai.org/) | Practical control guidance across the AI lifecycle |
| F-11 | CISA and UK NCSC et al. *Guidelines for Secure AI System Development*, November 2023. [CISA alert](https://www.cisa.gov/news-events/alerts/2023/11/26/cisa-and-uk-ncsc-unveil-joint-guidelines-secure-ai-system-development) · [NCSC collection](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) | Secure-by-design guidance for AI development |
| F-12 | ISO/IEC 42001:2023, *Information technology — Artificial intelligence — Management system.* [ISO catalogue](https://www.iso.org/standard/81230.html) | AI management-system obligations and governance |
| F-13 | ISO/IEC 23894:2023, *Information technology — Artificial intelligence — Guidance on risk management.* [ISO catalogue](https://www.iso.org/standard/77304.html) | AI risk-management process detail |
| F-14 | Regulation (EU) 2024/1689 (Artificial Intelligence Act). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Regulatory context; not legal advice |
| F-15 | Cloud Security Alliance. *Agentic AI Threat Modeling Framework (MAESTRO)*, 2025. [CSA](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) | Threat modeling for agentic systems |
| F-16 | Google. *Secure AI Framework (SAIF).* [saif.google](https://saif.google/) | A complementary secure-AI control framework |
| F-17 | OpenSSF. *SLSA*, *Sigstore*, CycloneDX *ML-BOM*, SPDX 3.0. [slsa.dev](https://slsa.dev/) · [sigstore.dev](https://www.sigstore.dev/) · [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/) · [spdx.dev](https://spdx.dev/) | Provenance, signing, and software bill of materials for ML artifacts |
| F-18 | OWASP. *API Security Top 10*, 2023 edition. [api-security.owasp.org](https://api-security.owasp.org/editions/2023/en/0x11-t10/) | API risk taxonomy used in M11 and LAB-14 |
| F-19 | NIST. *Cybersecurity Framework (CSF) 2.0.* NIST CSWP 29, February 2024. [DOI](https://doi.org/10.6028/NIST.CSWP.29) | Govern, identify, protect, detect, respond, and recover |
| F-20 | NIST. *Incident Response Recommendations and Considerations for Cybersecurity Risk Management.* NIST SP 800-61r3, April 2025. [CSRC](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Incident-response lifecycle used in M11 and LAB-15 |
| F-21 | OWASP. *Application Security Verification Standard (ASVS).* [Project](https://owasp.org/www-project-application-security-verification-standard/) | Testable application-security requirements |
| F-22 | NIST. *Technical Guide to Information Security Testing and Assessment.* NIST SP 800-115, September 2008. [CSRC](https://csrc.nist.gov/pubs/sp/800/115/final) | Planning, executing, and reporting a bounded security test; used in M17 and RT-01 |
| F-23 | OWASP. *Web Security Testing Guide (WSTG)*, v4.2. [Project](https://owasp.org/www-project-web-security-testing-guide/) | Test-case structure and evidence expectations for application-facing checks |

---

## Foundations and surveys

| ID | Reference | Why read it |
|---|---|---|
| R-01 | Biggio, B., & Roli, F. *Wild Patterns: Ten Years After the Rise of Adversarial Machine Learning.* arXiv:1712.03141, 2017. [arXiv](https://arxiv.org/abs/1712.03141) | The historical frame: evasion, poisoning, and privacy as one field |
| R-02 | Biggio, B., Corona, I., Maiorca, D., et al. *Evasion Attacks against Machine Learning at Test Time.* ECML PKDD 2013; arXiv posting 2017. [arXiv:1708.06131](https://arxiv.org/abs/1708.06131) | The original evasion formulation, including attacker knowledge assumptions |
| R-03 | Kairouz, P., McMahan, H. B., Avent, B., et al. *Advances and Open Problems in Federated Learning.* arXiv:1912.04977, 2019. [arXiv](https://arxiv.org/abs/1912.04977) | Federated learning's open problems, including security and privacy |
| R-04 | Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. *A Survey on Concept Drift Adaptation.* ACM Computing Surveys, 2014. [DOI](https://doi.org/10.1145/2523813) | Why drift is not the same as attack, and why detection needs both |
| R-05 | Sambasivan, N., Kapania, S., Highfill, H., et al. *"Everyone wants to do the model work, not the data work": Data Cascades in High-Stakes AI.* CHI 2021. [DOI](https://doi.org/10.1145/3411764.3445518) | Why data quality and pipeline defects are a security problem, not only an ML problem |
| R-06 | Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. *Leakage in Data Mining: Formulation, Detection, and Avoidance.* ACM TKDD, 2012. [DOI](https://doi.org/10.1145/2382577.2382579) | The leakage taxonomy used in M09 and LAB-12 |
| R-07 | Sculley, D., Holt, G., Golovin, D., et al. *Hidden Technical Debt in Machine Learning Systems.* NeurIPS 2015. (Venue citation; no DOI asserted.) | Why glue code, configuration, and pipeline boundaries accumulate risk |
| R-08 | Ohm, M., Plate, H., Sykosch, A., & Meier, M. *Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks.* arXiv:2005.09535, 2020. [arXiv](https://arxiv.org/abs/2005.09535) | How dependency and install-time compromise actually happens |
| R-09 | Keshav, S. *How to Read a Paper.* ACM SIGCOMM Computer Communication Review 37(3), 2007. [DOI](https://doi.org/10.1145/1273445.1273458) | The three-pass reading method used in the [research reading guide](research-reading-guide.md) |

---

## Evasion and robustness

| ID | Reference | Why read it |
|---|---|---|
| R-10 | Szegedy, C., Zaremba, W., Sutskever, I., et al. *Intriguing properties of neural networks.* arXiv:1312.6199, 2013. [arXiv](https://arxiv.org/abs/1312.6199) | The result that started the field |
| R-11 | Goodfellow, I. J., Shlens, J., & Szegedy, C. *Explaining and Harnessing Adversarial Examples.* arXiv:1412.6572, 2014. [arXiv](https://arxiv.org/abs/1412.6572) | The linearity explanation and the FGSM derivation |
| R-12 | Papernot, N., McDaniel, P., Jha, S., et al. *The Limitations of Deep Learning in Adversarial Settings.* arXiv:1511.07528, 2015. [arXiv](https://arxiv.org/abs/1511.07528) | Saliency-based, targeted, L0-style perturbation |
| R-13 | Kurakin, A., Goodfellow, I., & Bengio, S. *Adversarial examples in the physical world.* arXiv:1607.02533, 2016. [arXiv](https://arxiv.org/abs/1607.02533) | The gap between digital perturbation and a camera |
| R-14 | Carlini, N., & Wagner, D. *Towards Evaluating the Robustness of Neural Networks.* arXiv:1608.04644, 2016. [arXiv](https://arxiv.org/abs/1608.04644) | The optimization attack that became a standard baseline |
| R-15 | Moosavi-Dezfooli, S.-M., Fawzi, A., & Frossard, P. *DeepFool: a simple and accurate method to fool deep neural networks.* arXiv:1511.04599, 2015. [arXiv](https://arxiv.org/abs/1511.04599) | Minimal-perturbation attacks via linearization |
| R-16 | Moosavi-Dezfooli, S.-M., Fawzi, A., Fawzi, O., & Frossard, P. *Universal adversarial perturbations.* arXiv:1610.08401, 2016. [arXiv](https://arxiv.org/abs/1610.08401) | One perturbation that transfers across inputs |
| R-17 | Brown, T. B., Mané, D., Roy, A., et al. *Adversarial Patch.* arXiv:1712.09665, 2017. [arXiv](https://arxiv.org/abs/1712.09665) | Localized, printable attacks and their physical assumptions |
| R-18 | Madry, A., Makelov, A., Schmidt, L., et al. *Towards Deep Learning Models Resistant to Adversarial Attacks.* arXiv:1706.06083, 2017. [arXiv](https://arxiv.org/abs/1706.06083) | PGD as an evaluation and adversarial training as a defense |
| R-19 | Athalye, A., Carlini, N., & Wagner, D. *Obfuscated Gradients Give a False Sense of Security.* arXiv:1802.00420, 2018. [arXiv](https://arxiv.org/abs/1802.00420) | Why a defense can look robust and still be broken |
| R-20 | Andriushchenko, M., Croce, F., Flammarion, N., & Hein, M. *Square Attack: a query-efficient black-box adversarial attack via random search.* arXiv:1912.00049, 2019. [arXiv](https://arxiv.org/abs/1912.00049) | Query-efficient score-based attacks |
| R-21 | Chen, J., Jordan, M. I., & Wainwright, M. J. *HopSkipJumpAttack: A Query-Efficient Decision-Based Attack.* arXiv:1904.02144, 2019. [arXiv](https://arxiv.org/abs/1904.02144) | Attacking with labels only |
| R-22 | Croce, F., & Hein, M. *Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks.* arXiv:2003.01690, 2020. [arXiv](https://arxiv.org/abs/2003.01690) | AutoAttack: why one attack is not an evaluation |
| R-23 | Croce, F., Andriushchenko, M., Sehwag, V., et al. *RobustBench: a standardized adversarial robustness benchmark.* arXiv:2010.09670, 2020. [arXiv](https://arxiv.org/abs/2010.09670) | Comparing robustness claims on common ground |
| R-24 | Carlini, N., Athalye, A., Papernot, N., et al. *On Evaluating Adversarial Robustness.* arXiv:1902.06705, 2019. [arXiv](https://arxiv.org/abs/1902.06705) | The checklist for a credible robustness claim |
| R-25 | Cohen, J. M., Rosenfeld, E., & Kolter, J. Z. *Certified Adversarial Robustness via Randomized Smoothing.* arXiv:1902.02918, 2019. [arXiv](https://arxiv.org/abs/1902.02918) | A certified L2 radius, and what it does not cover |
| R-26 | Wong, E., & Kolter, J. Z. *Provable defenses against adversarial examples via the convex outer adversarial polytope.* arXiv:1711.00851, 2017. [arXiv](https://arxiv.org/abs/1711.00851) | Certification by convex relaxation and its cost |
| R-27 | Zhang, H., Yu, Y., Jiao, J., et al. *Theoretically Principled Trade-off between Robustness and Accuracy (TRADES).* arXiv:1901.08573, 2019. [arXiv](https://arxiv.org/abs/1901.08573) | The robustness-accuracy trade-off, made explicit |

---

## Poisoning, backdoors, and availability

| ID | Reference | Why read it |
|---|---|---|
| R-30 | Biggio, B., Nelson, B., & Laskov, P. *Poisoning Attacks against Support Vector Machines.* arXiv:1206.6389, 2012. [arXiv](https://arxiv.org/abs/1206.6389) | The foundational poisoning formulation |
| R-31 | Gu, T., Dolan-Gavitt, B., & Garg, S. *BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain.* arXiv:1708.06733, 2017. [arXiv](https://arxiv.org/abs/1708.06733) | The canonical trigger-based backdoor |
| R-32 | Chen, X., Liu, C., Li, B., et al. *Targeted Backdoor Attacks on Deep Learning Systems Using Data Poisoning.* arXiv:1712.05526, 2017. [arXiv](https://arxiv.org/abs/1712.05526) | Targeted behavior from a small poisoned fraction |
| R-33 | Liu, Y., Ma, S., Aafer, Y., et al. *Trojaning Attack on Neural Networks.* NDSS 2018. (Venue citation; no DOI asserted.) | Weight-level trojaning without full retraining |
| R-34 | Wang, B., Yao, Y., Shan, S., et al. *Neural Cleanse: Identifying and Mitigating Backdoor Attacks in Neural Networks.* IEEE S&P 2019. [DOI](https://doi.org/10.1109/SP.2019.00031) | Trigger reverse-engineering and the anomaly index |
| R-35 | Gao, Y., Xu, C., Wang, D., et al. *STRIP: A Defence Against Trojan Attacks on Deep Neural Networks.* arXiv:1902.06531, 2019. [arXiv](https://arxiv.org/abs/1902.06531) | Detection by input perturbation and prediction entropy |
| R-36 | Liu, K., Dolan-Gavitt, B., & Garg, S. *Fine-Pruning: Defending Against Backdooring Attacks on Deep Neural Networks.* arXiv:1805.12185, 2018. [arXiv](https://arxiv.org/abs/1805.12185) | Pruning and fine-tuning as a mitigation, with limits |
| R-37 | Tran, B., Li, J., & Madry, A. *Spectral Signatures in Backdoor Attacks.* arXiv:1811.00636, 2018. [arXiv](https://arxiv.org/abs/1811.00636) | Latent-space separability of poisoned examples |
| R-38 | Schwarzschild, A., Goldblum, M., Gupta, A., et al. *Just How Toxic is Data Poisoning? A Unified Benchmark for Backdoor and Data Poisoning Attacks.* arXiv:2006.12557, 2020. [arXiv](https://arxiv.org/abs/2006.12557) | Comparing attacks under one evaluation harness |
| R-39 | Carlini, N., & Terzis, A. *Poisoning and Backdooring Contrastive Learning.* arXiv:2106.09667, 2021. [arXiv](https://arxiv.org/abs/2106.09667) | Poisoning beyond supervised classification |
| R-40 | Tramèr, F., Shokri, R., San Joaquin, A., et al. *Truth Serum: Poisoning Machine Learning Models to Reveal Their Secrets.* arXiv:2204.00032, 2022. [arXiv](https://arxiv.org/abs/2204.00032) | Poisoning as a privacy attack |
| R-41 | Shumailov, I., Zhao, Y., Bates, D., et al. *Sponge Examples: Energy-Latency Attacks on Neural Networks.* arXiv:2006.03463, 2020. [arXiv](https://arxiv.org/abs/2006.03463) | Availability and cost amplification, not accuracy loss |

---

## Extraction, inference, and privacy

| ID | Reference | Why read it |
|---|---|---|
| R-50 | Tramèr, F., Zhang, F., Juels, A., et al. *Stealing Machine Learning Models via Prediction APIs.* arXiv:1609.02943, 2016. [arXiv](https://arxiv.org/abs/1609.02943) | The API-as-oracle framing |
| R-51 | Orekondy, T., Schiele, B., & Fritz, M. *Knockoff Nets: Stealing Functionality of Black-Box Models.* arXiv:1812.02766, 2018. [arXiv](https://arxiv.org/abs/1812.02766) | Extraction with a substitute dataset |
| R-52 | Jagielski, M., Carlini, N., Berthelot, D., et al. *High Accuracy and High Fidelity Extraction of Neural Networks.* arXiv:1909.01838, 2019. [arXiv](https://arxiv.org/abs/1909.01838) | Fidelity as a distinct extraction metric |
| R-53 | Carlini, N., Jagielski, M., Mironov, I., et al. *Cryptanalytic Extraction of Neural Network Models.* arXiv:2003.04884, 2020. [arXiv](https://arxiv.org/abs/2003.04884) | Exact extraction from precision and query behavior |
| R-54 | Adi, Y., Baum, C., Cisse, M., et al. *Turning Your Weakness Into a Strength: Watermarking Deep Neural Networks by Backdooring.* arXiv:1802.04633, 2018. [arXiv](https://arxiv.org/abs/1802.04633) | Ownership evidence, and its fragility |
| R-55 | Uchida, Y., Nagai, Y., Sakazawa, S., & Satoh, S. *Embedding Watermarks into Deep Neural Networks.* arXiv:1701.04082, 2017. [arXiv](https://arxiv.org/abs/1701.04082) | Embedding ownership signals in weights |
| R-56 | Shokri, R., Stronati, M., Song, C., & Shmatikov, V. *Membership Inference Attacks against Machine Learning Models.* arXiv:1610.05820, 2016. [arXiv](https://arxiv.org/abs/1610.05820) | Shadow models and the membership threat model |
| R-57 | Carlini, N., Chien, S., Nasr, M., et al. *Membership Inference Attacks From First Principles (LiRA).* arXiv:2112.03570, 2021. [arXiv](https://arxiv.org/abs/2112.03570) | Likelihood ratios and low-FPR evaluation |
| R-58 | Fredrikson, M., Jha, S., & Ristenpart, T. *Model Inversion Attacks that Exploit Confidence Information and Basic Countermeasures.* ACM CCS 2015. [DOI](https://doi.org/10.1145/2810103.2813677) | Confidence leakage and reconstruction |
| R-59 | Zhang, Y., Jia, R., Pei, H., et al. *The Secret Revealer: Generative Model-Inversion Attacks Against Deep Neural Networks.* arXiv:1911.07135, 2019. [arXiv](https://arxiv.org/abs/1911.07135) | Generative priors make inversion stronger |
| R-60 | Abadi, M., Chu, A., Goodfellow, I., et al. *Deep Learning with Differential Privacy.* arXiv:1607.00133, 2016. [arXiv](https://arxiv.org/abs/1607.00133) | DP-SGD: clipping, noise, and accounting |
| R-61 | Papernot, N., Abadi, M., Erlingsson, Ú., et al. *Semi-supervised Knowledge Transfer for Deep Learning from Private Training Data (PATE).* arXiv:1610.05755, 2016. [arXiv](https://arxiv.org/abs/1610.05755) | Private learning through teacher ensembles |
| R-62 | Dwork, C., & Roth, A. *The Algorithmic Foundations of Differential Privacy.* Foundations and Trends in Theoretical Computer Science, 2014. [DOI](https://doi.org/10.1561/0400000042) | The formal basis for epsilon and delta |
| R-63 | Carlini, N., Tramèr, F., Wallace, E., et al. *Extracting Training Data from Large Language Models.* arXiv:2012.07805, 2020. [arXiv](https://arxiv.org/abs/2012.07805) | Memorization in language models |
| R-64 | Carlini, N., Hayes, J., Nasr, M., et al. *Extracting Training Data from Diffusion Models.* arXiv:2301.13188, 2023. [arXiv](https://arxiv.org/abs/2301.13188) | Extraction from generative image models |

---

## Explainability and fairness

| ID | Reference | Why read it |
|---|---|---|
| R-90 | Ribeiro, M. T., Singh, S., & Guestrin, C. *"Why Should I Trust You?": Explaining the Predictions of Any Classifier (LIME).* arXiv:1602.04938, 2016. [arXiv](https://arxiv.org/abs/1602.04938) | Local surrogate explanations, sampling assumptions, and fidelity limits |
| R-91 | Lundberg, S. M., & Lee, S.-I. *A Unified Approach to Interpreting Model Predictions (SHAP).* arXiv:1705.07874, 2017. [arXiv](https://arxiv.org/abs/1705.07874) | Additive attributions and the assumptions behind Shapley values |
| R-92 | Adebayo, J., Gilmer, J., Muelly, M., et al. *Sanity Checks for Saliency Maps.* arXiv:1810.03292, 2018. [arXiv](https://arxiv.org/abs/1810.03292) | Model-randomization tests, and why a saliency map can be nearly independent of the weights |
| R-93 | Rudin, C. *Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead.* arXiv:1811.10154, 2018. [arXiv](https://arxiv.org/abs/1811.10154) | The case for inherently interpretable models over post-hoc explanation |
| R-94 | Slack, D., Hilgard, S., Jia, E., et al. *Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods.* arXiv:1911.02508, 2019. [arXiv](https://arxiv.org/abs/1911.02508) | Explanation manipulation when the attacker knows the explanation method |
| R-95 | Hardt, M., Price, E., & Srebro, N. *Equality of Opportunity in Supervised Learning.* arXiv:1610.02413, 2016. [arXiv](https://arxiv.org/abs/1610.02413) | Equalized odds and the error-rate trade-offs behind it |
| R-96 | Chouldechova, A. *Fair prediction with disparate impact: A study of bias in recidivism prediction instruments.* arXiv:1703.00056, 2017. [arXiv](https://arxiv.org/abs/1703.00056) | Why predictive parity and disparate impact can conflict |
| R-97 | Kleinberg, J., Mullainathan, S., & Raghavan, M. *Inherent Trade-Offs in the Fair Determination of Risk Scores.* arXiv:1609.05807, 2016. [arXiv](https://arxiv.org/abs/1609.05807) | An impossibility result for combining calibration and balance |
| R-98 | Dwork, C., Hardt, M., Pitassi, T., et al. *Fairness Through Awareness.* arXiv:1104.3913, 2011. [arXiv](https://arxiv.org/abs/1104.3913) | Individual fairness as a metric-based condition |
| R-99 | Barocas, S., Hardt, M., & Narayanan, A. *Fairness and Machine Learning: Limitations and Opportunities.* fairmlbook.org, 2023. [fairmlbook.org](https://fairmlbook.org/) | A book-length treatment of measurement, legal context, and trade-offs |

---

## Federated, generative, and agentic systems

| ID | Reference | Why read it |
|---|---|---|
| R-70 | McMahan, H. B., Moore, E., Ramage, D., et al. *Communication-Efficient Learning of Deep Networks from Decentralized Data.* arXiv:1602.05629, 2016. [arXiv](https://arxiv.org/abs/1602.05629) | FedAvg, the baseline every FL attack targets |
| R-71 | Bagdasaryan, E., Veit, A., Hua, Y., et al. *How To Backdoor Federated Learning.* arXiv:1807.00459, 2018. [arXiv](https://arxiv.org/abs/1807.00459) | A single malicious client can persist a backdoor |
| R-72 | Blanchard, P., El Mhamdi, E. M., Guerraoui, R., & Stainer, J. *Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent (Krum).* NeurIPS 2017. (Venue citation.) | Robust aggregation and its assumptions |
| R-73 | Yin, D., Chen, Y., Ramchandran, K., & Bartlett, P. *Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates.* arXiv:1803.01498, 2018. [arXiv](https://arxiv.org/abs/1803.01498) | Trimmed mean and coordinate-wise robustness |
| R-74 | Bonawitz, K., Ivanov, V., Kreuter, B., et al. *Practical Secure Aggregation for Privacy-Preserving Machine Learning.* ACM CCS 2017. [DOI](https://doi.org/10.1145/3133956.3133982) | What secure aggregation hides, and what it does not |
| R-80 | Greshake, K., Abdelnabi, S., Mishra, S., et al. *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* arXiv:2302.12173, 2023. [arXiv](https://arxiv.org/abs/2302.12173) | Untrusted content as an instruction channel |
| R-81 | Zou, A., Wang, Z., Carlini, N., et al. *Universal and Transferable Adversarial Attacks on Aligned Language Models.* arXiv:2307.15043, 2023. [arXiv](https://arxiv.org/abs/2307.15043) | Optimization-based jailbreak suffixes and transfer |
| R-82 | Wei, A., Haghtalab, N., & Steinhardt, J. *Jailbroken: How Does LLM Safety Training Fail?* arXiv:2307.02483, 2023. [arXiv](https://arxiv.org/abs/2307.02483) | Why safety training is not a security boundary |
| R-83 | Carlini, N., Nasr, M., Choquette-Choo, C. A., et al. *Are aligned neural networks adversarially aligned?* arXiv:2306.15447, 2023. [arXiv](https://arxiv.org/abs/2306.15447) | The gap between alignment and adversarial robustness |
| R-84 | Wallace, E., Xiao, K., Leike, R., et al. *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions.* arXiv:2404.13208, 2024. [arXiv](https://arxiv.org/abs/2404.13208) | A design pattern for instruction trust boundaries |
| R-85 | Debenedetti, E., Zhang, J., Balunović, M., et al. *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* arXiv:2406.13352, 2024. [arXiv](https://arxiv.org/abs/2406.13352) | A test environment for agent injection |
| R-86 | Debenedetti, E., Shumailov, I., Fan, T., et al. *Defeating Prompt Injections by Design (CaMeL).* arXiv:2503.18813, 2025. [arXiv](https://arxiv.org/abs/2503.18813) | Capability-based defense rather than prompt-level filtering |

---

## Research practice, reproducibility, and evaluation

| ID | Reference | Why read it |
|---|---|---|
| R-100 | Pineau, J., Vincent-Lamarre, P., Sinha, K., et al. *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program).* arXiv:2003.12206, 2020; JMLR 22(164), 2021. [arXiv](https://arxiv.org/abs/2003.12206) | The reproducibility checklist behind the capstone's run record and clean-checkout test |
| R-101 | Kapoor, S., & Narayanan, A. *Leakage and the Reproducibility Crisis in ML-based Science.* arXiv:2207.07048, 2022. [arXiv](https://arxiv.org/abs/2207.07048) | Why a result can be reproducible and still invalid because of data leakage |
| R-102 | Ganguli, D., Hernandez, D., Lovitt, L., et al. *Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned.* arXiv:2209.07858, 2022. [arXiv](https://arxiv.org/abs/2209.07858) | What red-team evidence can and cannot establish, and how findings scale with effort |
| R-103 | Brundage, M., Avin, S., Clark, J., et al. *The Malicious Use of Artificial Intelligence: Forecasting, Prevention, and Mitigation.* arXiv:1802.07228, 2018. [arXiv](https://arxiv.org/abs/1802.07228) | Threat framing and defensive priorities for the red-team exercise |
| R-104 | Brundage, M., Avin, S., Wang, J., et al. *Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims.* arXiv:2004.07213, 2020. [arXiv](https://arxiv.org/abs/2004.07213) | Auditing, provenance, and verifiable claims for an assessment dossier |
| R-105 | Ganguli, D., Hernandez, D., Lovitt, L., et al. *Predictability and Surprise in Large Generative Models.* arXiv:2202.07785, 2022. [arXiv](https://arxiv.org/abs/2202.07785) | Scaling, emergence, and why frontier-system claims need careful scope |

---

## Datasets and benchmarks

No published lab downloads a dataset: the labs use `sklearn.datasets.load_digits` or a seeded synthetic generator. The table below lists the resources that appear in the course and in optional extensions, with the license or terms that could be verified at the source on 2026-10-28. Provenance, limitations, and download steps are in the [dataset catalog](dataset-catalog.md).

| Resource | Used for | Access | License or terms (verified) |
|---|---|---|---|
| scikit-learn digits | Primary dataset for published labs | Bundled with scikit-learn | scikit-learn is BSD-3-Clause; the underlying UCI *Optical Recognition of Handwritten Digits* page states CC BY 4.0 |
| Synthetic fixtures | Tabular, systems, and agent labs | Generated by lab code | No third-party terms; the generator is part of this repository |
| MNIST and Fashion-MNIST | Fast baselines, inversion, monitoring | `torchvision` | The original MNIST page states no explicit license; verify at the source before redistributing |
| CIFAR-10 | Standard vision benchmark | [cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html) | No explicit license statement found on the download page; verify before redistribution |
| UCI Adult | Tabular classification and extraction | [UCI dataset 2](https://archive.ics.uci.edu/dataset/2/adult) | CC BY 4.0 |
| SMS Spam Collection | Text classification and evasion | [UCI dataset 228](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) | CC BY 4.0 |
| NSL-KDD and CICIDS2017 | Intrusion-detection context | [NSL-KDD](https://www.unb.ca/cic/datasets/nsl.html) · [CICIDS2017](https://www.unb.ca/cic/datasets/ids-2017.html) | Usage terms are stated on the UNB pages; read them before use |
| EMBER | Malware static features | [github.com/elastic/ember](https://github.com/elastic/ember) | No license file in the repository; ask the maintainers before redistributing |
| FEMNIST (LEAF) | Federated non-IID partitions | [leaf.cmu.edu](https://leaf.cmu.edu/) | LEAF code is BSD-2-Clause; dataset terms are stated at the source |
| Credit card fraud (ULB) | Imbalanced tabular monitoring | [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) | Account required; the Kaggle listing carries its own terms. The [OpenML mirror](https://www.openml.org/d/1597) is labeled "Public" |
| BackdoorBench | Backdoor evaluation | [github.com/SCLBD/BackdoorBench](https://github.com/SCLBD/BackdoorBench) | CC BY-NC 4.0 — **non-commercial**; not suitable for a commercial course product |
| TrojAI | Trojan detection rounds | [www.trojandetection.ai](https://www.trojandetection.ai/) | Terms are stated at the source; verify before use |
| RobustBench | Robustness leaderboard | [robustbench.github.io](https://robustbench.github.io/) | Benchmark code is MIT |
| HarmBench and JailbreakBench | LLM safety and jailbreak evaluation | [HarmBench](https://www.harmbench.org/) · [JailbreakBench](https://jailbreakbench.github.io/) | MIT |
| AgentDojo | Agent prompt-injection evaluation | [github.com/ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) | MIT |

**Purchase-100** is a common membership-inference benchmark. It is not used by any published lab; an optional extension would require a Kaggle account and a digits-based fallback. Dataset availability changes, so every lab needs a fallback path.

---

## Tools referenced in the course

You do not need all of these on day one. Tool names are listed by function; install pins and versions will ship with each lab.

### Official documentation

Documentation changes between releases. When a lesson and the documentation disagree, the pinned version in the lab's `requirements.txt` wins, and the lesson should be corrected.

| Stack | Documentation | Use it for |
|---|---|---|
| Python | [docs.python.org/3](https://docs.python.org/3/) · [`pickle`](https://docs.python.org/3/library/pickle.html) | Language reference; the deserialization warning in M10.L2 |
| NumPy | [numpy.org/doc/stable](https://numpy.org/doc/stable/) · [`Generator`](https://numpy.org/doc/stable/reference/random/generator.html) | Array semantics and seeded random generators |
| pandas | [pandas.pydata.org/docs](https://pandas.pydata.org/docs/) | Tabular loading, dtypes, and joins in M01 |
| scikit-learn | [scikit-learn.org/stable](https://scikit-learn.org/stable/) · [model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) · [cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) · [calibration](https://scikit-learn.org/stable/modules/calibration.html) | Estimators, metrics, splits, and calibration used in every lab |
| PyTorch | [pytorch.org/docs/stable](https://pytorch.org/docs/stable/) | Autograd and optimizers behind the gradient-based attacks |
| Adversarial Robustness Toolbox | [ART docs](https://adversarial-robustness-toolbox.readthedocs.io/) | Cross-checking an attack implementation |
| Foolbox | [foolbox.readthedocs.io](https://foolbox.readthedocs.io/) | Reference implementations of gradient and boundary attacks |
| TextAttack | [textattack.readthedocs.io](https://textattack.readthedocs.io/) | Text-domain evasion examples |
| Opacus | [opacus.ai](https://opacus.ai/) | DP-SGD implementation details in M13 |
| diffprivlib | [diffprivlib.readthedocs.io](https://diffprivlib.readthedocs.io/) | Differentially private estimators and budget accounting |

### Libraries by function

| Function | Tools |
|---|---|
| Models and numerics | PyTorch, NumPy, scikit-learn |
| Attacks and robustness | IBM Adversarial Robustness Toolbox, Foolbox, SecML, AutoAttack, RobustBench |
| Text attacks | TextAttack |
| Backdoors | BackdoorBench |
| Artifact and supply chain | ModelScan, picklescan, safetensors, ONNX, Sigstore and cosign, in-toto, SLSA, CycloneDX, SPDX, `pip-audit` |
| Serving and containers | FastAPI, Uvicorn, Docker, Trivy |
| Monitoring | Evidently, Alibi-Detect |
| Federated learning | Flower |
| Differential privacy | Opacus, diffprivlib |
| Explainability | LIME, SHAP |
| LLM and agent evaluation | garak, PyRIT, promptfoo, NeMo Guardrails, LLM Guard, Inspect, AgentDojo |

CleverHans appears in older literature as historical context; it is not a maintained dependency for this course.

---

## Citation practice

When you write a lab report:

- Cite the paper or standard, not a summary of it.
- State the framework version and date.
- For an arXiv paper, cite the arXiv identifier and the year shown on the abstract page.
- For a standard, cite the exact edition (for example, ISO/IEC 42001:2023).
- If you could not verify a claim, say so instead of citing something adjacent.

A short, accurate reference list is worth more than a long one you have not read.

## Known gaps and unresolved items

These are recorded rather than papered over. Re-check them before you rely on the entry in published work.

| Item | Status on 2026-10-28 |
|---|---|
| ISO/IEC catalogue pages (F-12, F-13) | Return 403 to automated clients. Edition numbers were taken from the catalogue listing; the full text was not read and no clause-level claim is made anywhere in the course |
| ACM, IEEE, and Elsevier DOI pages | Return 403 to automated clients. Titles and years were verified through Crossref metadata, not by reading the articles |
| OWASP category IDs | The 2026 edition renumbers all ten categories. The course teaches the 2025 IDs and states so in M15; the crosswalk is in the [framework mapping](framework-mapping.md) |
| EMBER | The repository contains no license file. Treat redistribution as unresolved and ask the maintainers |
| CIFAR-10 and MNIST | The download pages state no explicit license. They are widely redistributed, but this course does not assert a license for them |
| NSL-KDD and CICIDS2017 | Use is governed by the UNB site's terms of use, which can change; no license was asserted here |
| R-07, R-33, R-72 | Venue citations only. No DOI or arXiv identifier was verified for the specific venue version, so none is printed |
| R-102 and R-103 | Their identifiers pointed at different papers before this pass. Corrected on 2026-10-28 by matching each identifier to its arXiv title |
