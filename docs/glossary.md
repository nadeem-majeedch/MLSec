# Glossary

Security work is full of acronyms that hide simple ideas. This glossary explains each term in plain language, expands every acronym on first use, and points to the lesson or lab where the term is actually used. If a definition here conflicts with a primary source, the primary source wins.

The entries are short on purpose. A glossary tells you what a word means; a lesson shows you how to measure it.

## How to use this page

- Read the **Meaning** column first. The **Where it is taught** column is for when you need the full treatment.
- Terms are grouped by topic, not alphabetized, because related ideas are easier to learn together.
- An acronym in *italics* in a definition is defined in the [acronym quick reference](#acronym-quick-reference).

## 1. Evidence, measurement, and method

| Term | Meaning | Where it is taught |
|---|---|---|
| **Threat model** | A written statement of who the adversary is, what they know, what they can do, what they want, and what they are willing to spend. Every lab starts with one. | [M03.5](modules/m03-threat-modeling/lesson-5-building-the-model.md), [LAB-02](labs/lab-02.md) |
| **Adversary knowledge** | What the attacker knows about the model: white-box (architecture and weights), grey-box (partial), or black-box (inputs and outputs only). | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **Capability** | The actions an adversary can take: submit inputs, add training rows, modify a checkpoint, call a tool. | [M03.2](modules/m03-threat-modeling/lesson-2-adversaries-and-taxonomy.md) |
| **Budget** | The limit on attack effort, usually measured in queries, perturbation size, poisoned rows, or wall-clock time. | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **Metric** | The number that decides whether an attack or defense worked: accuracy, attack success rate, false-positive rate, latency. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **Baseline** | The unmodified result you compare against. Without one, a change is not evidence. | [LAB-01B](labs/lab-01b.md) |
| **Ablation** | Removing or changing one component to see how much it contributed. | [M08.5](modules/m08-robustness-defense/lesson-5-standardized-evaluation.md) |
| **Seed** | The number that makes a pseudo-random process repeatable. Report it, or your result cannot be reproduced. | [M01.5](modules/m01-python-refresher/lesson-5-reproducibility.md) |
| **Manifest** | A file listing artifacts with cryptographic hashes so someone else can check exactly what you ran. | [M09.4](modules/m09-data-integrity/lesson-4-reproducible-training.md) |
| **Artifact** | Any output of work that can be inspected and re-run: code, metrics, report, environment file, manifest. | [M00.2](modules/m00-orientation/lesson-2-lab-and-evidence.md) |
| **Clean checkout** | A fresh copy of the repository with no leftover state, used to test whether your work really reproduces. | [M01.5](modules/m01-python-refresher/lesson-5-reproducibility.md) |
| **Reproducibility** | Another person, on another machine, gets the same result from the same inputs and instructions. | [M09.4](modules/m09-data-integrity/lesson-4-reproducible-training.md) |
| **Leakage** | Information in the training data or pipeline that would not be available at prediction time, which inflates measured performance. | [M02.4](modules/m02-ml-fundamentals/lesson-4-leakage-and-reporting.md), [LAB-12](labs/lab-12.md) |
| **Data cascade** | A chain of data-quality defects that compounds downstream and undermines an otherwise well-built model. | [M09.2](modules/m09-data-integrity/lesson-2-data-quality-and-integrity.md) |
| **Train / validation / test split** | Three disjoint parts of the data: one to fit, one to tune, one to report. Reusing the test set turns it into a tuning set. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **Cross-validation** | Repeatedly splitting the data into folds so each part serves as validation once. | [M01.4](modules/m01-python-refresher/lesson-4-scikit-learn.md) |
| **Calibration** | Whether a model's stated confidence matches its observed accuracy. A model can be accurate and badly calibrated. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **False positive rate (FPR)** | The share of negative cases wrongly flagged. In security, the FPR at a fixed operating point often matters more than overall accuracy. | [M11.4](modules/m11-serving-monitoring/lesson-4-monitoring-drift-and-attack-indicators.md) |
| **False negative rate (FNR)** | The share of positive cases missed. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **Precision and recall** | Precision is the share of flagged cases that were positive; recall is the share of positive cases that were flagged. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **Receiver operating characteristic (ROC) curve** | A plot of true-positive rate against false-positive rate across thresholds. The area under it (AUROC) summarizes ranking quality, not security. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **Attack success rate (ASR)** | The share of attacked inputs that achieve the attacker's goal. Define the denominator: all inputs, only originally-correct inputs, or only targeted ones. | [M04.5](modules/m04-evasion/lesson-5-measuring-honestly.md) |
| **Robust accuracy** | Accuracy on adversarial inputs at a stated threat model and budget. Meaningless without both. | [M08.1](modules/m08-robustness-defense/lesson-1-what-robustness-claims-mean.md) |
| **Confidence interval** | A range that expresses uncertainty in an estimate. A single run is not a result. | [M08.6](modules/m08-robustness-defense/lesson-6-reporting-robustness.md) |
| **Benchmark** | A shared dataset, metric, and protocol that lets results be compared. | [M08.5](modules/m08-robustness-defense/lesson-5-standardized-evaluation.md) |

## 2. Machine learning basics

| Term | Meaning | Where it is taught |
|---|---|---|
| **Model** | A function with learned parameters that maps inputs to outputs. | [M02.1](modules/m02-ml-fundamentals/lesson-1-learning-problems.md) |
| **Feature** | A measurable input variable, such as a pixel value or a transaction amount. | [M01.3](modules/m01-python-refresher/lesson-3-pandas.md) |
| **Label** | The target answer used for training or evaluation. | [M02.1](modules/m02-ml-fundamentals/lesson-1-learning-problems.md) |
| **Classifier** | A model that assigns an input to one of a fixed set of classes. | [M02.1](modules/m02-ml-fundamentals/lesson-1-learning-problems.md) |
| **Loss function** | A number that measures how wrong a prediction is; training tries to reduce it. | [M02.2](modules/m02-ml-fundamentals/lesson-2-loss-and-gradients.md) |
| **Gradient** | The direction in which the loss changes fastest. Attacks and training both use it. | [M02.2](modules/m02-ml-fundamentals/lesson-2-loss-and-gradients.md) |
| **Gradient descent** | Repeatedly stepping the parameters in the direction that lowers the loss. | [M02.2](modules/m02-ml-fundamentals/lesson-2-loss-and-gradients.md) |
| **Hyperparameter** | A setting chosen before training, such as learning rate or tree depth. | [M01.4](modules/m01-python-refresher/lesson-4-scikit-learn.md) |
| **Overfitting** | Fitting the training data so closely that performance on new data suffers. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **Regularization** | A penalty or constraint that discourages overfitting. | [M01.4](modules/m01-python-refresher/lesson-4-scikit-learn.md) |
| **Decision boundary** | The surface in input space where a classifier changes its predicted class. | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **Logit** | The raw score a model produces before converting it to a probability. | [M04.2](modules/m04-evasion/lesson-2-fgsm.md) |
| **Softmax** | A function that turns scores into probabilities that sum to one. | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **Generalization** | Performance on data the model did not train on. | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| **Distribution shift** | A change in the data distribution after deployment. It can be benign drift or attacker-induced. | [M11.4](modules/m11-serving-monitoring/lesson-4-monitoring-drift-and-attack-indicators.md) |

## 3. Evasion and adversarial examples

| Term | Meaning | Where it is taught |
|---|---|---|
| **Adversarial example** | An input deliberately modified to cause a wrong output while remaining valid for the task. | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **Perturbation** | The change made to a clean input to create an adversarial one. | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **\(L_p\) norm** | A way to measure perturbation size. \(L_0\) counts changed features; \(L_1\) sums absolute changes; \(L_2\) is Euclidean distance; \(L_\infty\) is the largest single change. | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **Epsilon (\(\varepsilon\)) budget** | The maximum allowed perturbation under the chosen norm. It is part of the threat model, not a detail. | [M04.1](modules/m04-evasion/lesson-1-threat-models-and-geometry.md) |
| **Evasion** | An attack at prediction time that changes the output without changing the model. | [M04](modules/m04-evasion/index.md) |
| **Targeted attack** | An attack that forces a specific chosen output. | [M04.3](modules/m04-evasion/lesson-3-pgd.md) |
| **Untargeted attack** | An attack that only needs the output to be wrong. | [M04.2](modules/m04-evasion/lesson-2-fgsm.md) |
| **Fast Gradient Sign Method (FGSM)** | A one-step attack that moves each input feature by \(\varepsilon\) in the sign of the loss gradient. | [M04.2](modules/m04-evasion/lesson-2-fgsm.md) |
| **Projected Gradient Descent (PGD)** | An iterative attack that takes gradient steps and projects back into the allowed perturbation ball. | [M04.3](modules/m04-evasion/lesson-3-pgd.md) |
| **Carlini–Wagner (C&W) attack** | An optimization-based attack that minimizes perturbation while achieving the target. A common strong baseline. | [M08.5](modules/m08-robustness-defense/lesson-5-standardized-evaluation.md) |
| **Transferability** | The property that an example crafted for one model also fools another. It is why black-box attacks work. | [M04.4](modules/m04-evasion/lesson-4-black-box-and-transfer.md) |
| **Surrogate model** | A local model an attacker trains or obtains to approximate the target. | [M04.4](modules/m04-evasion/lesson-4-black-box-and-transfer.md) |
| **Query budget** | The number of predictions an attacker may request. | [M04.4](modules/m04-evasion/lesson-4-black-box-and-transfer.md) |
| **Universal perturbation** | One perturbation that fools the model across many inputs. | [M04.4](modules/m04-evasion/lesson-4-black-box-and-transfer.md) |
| **Adversarial patch** | A localized, printable pattern that causes misclassification when present in a scene. | [M04.4](modules/m04-evasion/lesson-4-black-box-and-transfer.md) |
| **Gradient masking** | A defense that hides or distorts gradients, making attacks look weaker without making the model robust. Also called obfuscated gradients. | [M08.4](modules/m08-robustness-defense/lesson-4-adaptive-attacks-and-pitfalls.md) |
| **Adaptive attack** | An attack designed with knowledge of the defense. The only fair test of a defense. | [M08.4](modules/m08-robustness-defense/lesson-4-adaptive-attacks-and-pitfalls.md) |

## 4. Poisoning, backdoors, and supply chain

| Term | Meaning | Where it is taught |
|---|---|---|
| **Poisoning** | Changing training data or the training process so the learned model behaves as the attacker wants. | [M05.1](modules/m05-poisoning/lesson-1-poisoning-threat-models.md) |
| **Label flipping** | Changing labels in the training set, often from one class to another. | [M05.2](modules/m05-poisoning/lesson-2-label-flipping.md) |
| **Clean-label poisoning** | Poisoning features while keeping labels correct, so a human reviewer sees nothing wrong. | [M05.3](modules/m05-poisoning/lesson-3-targeted-poisoning.md) |
| **Poisoning curve** | Attack success plotted against the fraction of poisoned training data. | [LAB-05](labs/lab-05.md) |
| **Backdoor** | A hidden behavior that activates on a specific trigger and stays dormant otherwise. | [M06.1](modules/m06-backdoors/lesson-1-backdoor-anatomy.md) |
| **Trigger** | The pattern that activates a backdoor: a pixel patch, a rare token, a specific value combination. | [M06.1](modules/m06-backdoors/lesson-1-backdoor-anatomy.md) |
| **Trojan** | A model with an implanted backdoor, usually delivered through a checkpoint or supply chain. | [M06.1](modules/m06-backdoors/lesson-1-backdoor-anatomy.md) |
| **Model replacement** | An attacker substitutes a malicious global model or update, common in federated learning. | [M12.2](modules/m12-federated-learning/lesson-2-malicious-clients-and-update-poisoning.md) |
| **Sybil attack** | One adversary creates many fake identities to gain influence, for example many federated clients. | [M12.2](modules/m12-federated-learning/lesson-2-malicious-clients-and-update-poisoning.md) |
| **Byzantine-robust aggregation** | A rule for combining client updates that tolerates some malicious or arbitrary updates. Krum, trimmed mean, and coordinate median are examples. | [M12.3](modules/m12-federated-learning/lesson-3-aggregation-and-its-limits.md) |
| **Supply chain attack** | Compromise that arrives through a dependency, model, dataset, container, or tool rather than through the target directly. | [M10.1](modules/m10-supply-chain/lesson-1-ml-supply-chain-and-artifact-trust.md) |
| **Dependency confusion** | Publishing a public package with the same name as an internal one so installers fetch the attacker's version. | [M10.3](modules/m10-supply-chain/lesson-3-dependency-and-artifact-scanning.md) |
| **Typosquatting** | Publishing a package with a name close to a popular one, hoping for a typo. | [M10.3](modules/m10-supply-chain/lesson-3-dependency-and-artifact-scanning.md) |
| **Deserialization** | Reconstructing an object from stored bytes. Some formats can execute code while doing so. | [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md) |
| **Pickle** | Python's built-in serialization format. It can execute arbitrary code when loading untrusted files. | [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md) |
| **safetensors** | A tensor format that stores data without executable code, designed to avoid pickle risk. | [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md) |
| **Open Neural Network Exchange (ONNX)** | An open format for representing trained models across frameworks. | [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md) |
| **Software bill of materials (SBOM)** | A machine-readable inventory of the components in a software product. | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |
| **ML bill of materials (ML-BOM)** | An SBOM-style inventory for a model: data, code, hyperparameters, dependencies, and artifacts. | [M09.1](modules/m09-data-integrity/lesson-1-provenance-and-lineage.md) |
| **Provenance** | The record of where an artifact came from and what was done to it. | [M09.1](modules/m09-data-integrity/lesson-1-provenance-and-lineage.md) |
| **Lineage** | The graph linking datasets, code, runs, and models across a pipeline. | [M09.1](modules/m09-data-integrity/lesson-1-provenance-and-lineage.md) |
| **Hash / digest** | A fixed-length fingerprint of data. A changed file produces a different hash. | [M09.4](modules/m09-data-integrity/lesson-4-reproducible-training.md) |
| **Checksum** | A hash used to verify that a file arrived intact and unmodified. | [LAB-13](labs/lab-13.md) |
| **Digital signature** | A cryptographic proof that a specific key holder approved an artifact. | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |
| **Supply-chain levels for software artifacts (SLSA)** | A framework of levels describing how strongly a build's provenance can be trusted. | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |
| **Sigstore / cosign** | Open-source tooling for signing and verifying software artifacts. | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |
| **in-toto** | A framework for cryptographically linking each step of a supply chain. | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |

## 5. Privacy attacks and privacy engineering

| Term | Meaning | Where it is taught |
|---|---|---|
| **Model extraction** | Recovering a model, or a close functional copy, by querying it. | [M07.2](modules/m07-extraction-privacy/lesson-2-model-extraction.md) |
| **Fidelity** | How closely a stolen model's predictions match the target's. Distinct from task accuracy. | [M07.2](modules/m07-extraction-privacy/lesson-2-model-extraction.md) |
| **Membership inference** | Deciding whether a specific record was part of a model's training data. | [M07.3](modules/m07-extraction-privacy/lesson-3-membership-inference.md) |
| **Shadow model** | A model an attacker trains on data resembling the target's training set to learn what membership looks like. | [M07.3](modules/m07-extraction-privacy/lesson-3-membership-inference.md) |
| **Model inversion** | Reconstructing representative inputs or attributes from a model's outputs. | [M07.4](modules/m07-extraction-privacy/lesson-4-inversion-and-attribute-inference.md) |
| **Attribute inference** | Inferring a sensitive property of a record from model behavior or partial data. | [M07.4](modules/m07-extraction-privacy/lesson-4-inversion-and-attribute-inference.md) |
| **Property inference** | Inferring a dataset-level characteristic, such as whether a subgroup was present. | [M07.4](modules/m07-extraction-privacy/lesson-4-inversion-and-attribute-inference.md) |
| **Personally identifiable information (PII)** | Data that can identify a person directly or in combination with other data. | [M13.1](modules/m13-privacy-preserving-ml/lesson-1-privacy-threat-models.md) |
| **Quasi-identifier** | A field that is not unique alone but can identify someone when combined with others, such as ZIP code, birth date, and sex. | [M13.1](modules/m13-privacy-preserving-ml/lesson-1-privacy-threat-models.md) |
| **Anonymization** | Removing or altering identifiers. It does not guarantee privacy against linkage attacks. | [M13.1](modules/m13-privacy-preserving-ml/lesson-1-privacy-threat-models.md) |
| **k-anonymity** | A property where each record is indistinguishable from at least \(k-1\) others on the chosen quasi-identifiers. | [M13.1](modules/m13-privacy-preserving-ml/lesson-1-privacy-threat-models.md) |
| **De-identification** | A process for reducing identifiability, judged against a stated threat model. | [M13.1](modules/m13-privacy-preserving-ml/lesson-1-privacy-threat-models.md) |
| **Differential privacy (DP)** | A guarantee that a mechanism's output distribution changes only slightly when one individual's data changes. | [M13.2](modules/m13-privacy-preserving-ml/lesson-2-differential-privacy-first-principles.md) |
| **Epsilon (\(\varepsilon\))** | The DP privacy-loss parameter. Smaller means stronger privacy and usually less utility. | [M13.2](modules/m13-privacy-preserving-ml/lesson-2-differential-privacy-first-principles.md) |
| **Delta (\(\delta\))** | The small probability in approximate \((\varepsilon,\delta)\)-DP that the guarantee fails. | [M13.2](modules/m13-privacy-preserving-ml/lesson-2-differential-privacy-first-principles.md) |
| **Sensitivity** | The maximum amount a query's result can change when one record changes. It sets how much noise is needed. | [M13.2](modules/m13-privacy-preserving-ml/lesson-2-differential-privacy-first-principles.md) |
| **Laplace mechanism** | Adding Laplace-distributed noise calibrated to sensitivity; gives pure \(\varepsilon\)-DP. | [M13.2](modules/m13-privacy-preserving-ml/lesson-2-differential-privacy-first-principles.md) |
| **Gaussian mechanism** | Adding Gaussian noise; gives approximate \((\varepsilon,\delta)\)-DP. | [M13.2](modules/m13-privacy-preserving-ml/lesson-2-differential-privacy-first-principles.md) |
| **Composition** | Privacy loss accumulates when you answer multiple queries on the same data. | [M13.3](modules/m13-privacy-preserving-ml/lesson-3-composition-budgets-and-noisy-releases.md) |
| **Privacy budget** | The total privacy loss an application allows across all releases. | [M13.3](modules/m13-privacy-preserving-ml/lesson-3-composition-budgets-and-noisy-releases.md) |
| **Clipping** | Limiting each example's contribution to a gradient or query so sensitivity is bounded. | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| **Differentially private stochastic gradient descent (DP-SGD)** | Training with per-example gradient clipping, added noise, and privacy accounting. | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| **Secure aggregation** | A protocol that lets a server compute a sum of client updates without seeing any individual update. | [M12.4](modules/m12-federated-learning/lesson-4-validation-monitoring-and-privacy.md) |
| **Secure multi-party computation (MPC)** | Computing a function across parties without revealing each party's inputs. | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| **Homomorphic encryption (HE)** | Encryption that allows computation on ciphertext. | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| **Trusted execution environment (TEE)** | A hardware-isolated execution area that protects code and data from the host. | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| **Privacy–utility trade-off** | The tension between stronger privacy guarantees and useful model performance. | [M13.5](modules/m13-privacy-preserving-ml/lesson-5-privacy-utility-evaluation.md) |

## 6. Defenses and robustness evaluation

| Term | Meaning | Where it is taught |
|---|---|---|
| **Adversarial training** | Training on adversarial examples so the model learns to resist them. | [M08.2](modules/m08-robustness-defense/lesson-2-adversarial-training.md) |
| **Certified robustness** | A proof that no perturbation within a stated radius can change the prediction. Stronger than empirical robustness, and narrower in scope. | [M08.1](modules/m08-robustness-defense/lesson-1-what-robustness-claims-mean.md) |
| **Randomized smoothing** | A certification method that averages predictions over random noise and certifies a radius around the input. | [M08.5](modules/m08-robustness-defense/lesson-5-standardized-evaluation.md) |
| **Input preprocessing** | Transforming inputs before prediction to remove or disrupt perturbations. Often bypassed by adaptive attacks. | [M08.3](modules/m08-robustness-defense/lesson-3-input-preprocessing-and-detection.md) |
| **Adversarial detection** | Flagging likely-adversarial inputs rather than making the model correct on them. | [M08.3](modules/m08-robustness-defense/lesson-3-input-preprocessing-and-detection.md) |
| **AutoAttack** | An ensemble of parameter-free attacks used as a stronger robustness evaluation than a single attack. | [M08.5](modules/m08-robustness-defense/lesson-5-standardized-evaluation.md) |
| **RobustBench** | A standardized leaderboard and benchmark for adversarial robustness. | [M08.5](modules/m08-robustness-defense/lesson-5-standardized-evaluation.md) |
| **Neural Cleanse** | A backdoor-detection method that reverse-engineers a minimal trigger for each class and flags anomalous ones. | [M06.4](modules/m06-backdoors/lesson-4-detection-and-mitigation.md) |
| **STRIP** | A backdoor-detection method that perturbs inputs and looks for suspiciously stable predictions. | [M06.4](modules/m06-backdoors/lesson-4-detection-and-mitigation.md) |
| **Fine-pruning** | Removing neurons that are inactive on clean data, then fine-tuning, to weaken a backdoor. | [M06.4](modules/m06-backdoors/lesson-4-detection-and-mitigation.md) |
| **Spectral signature** | A latent-space signal used to separate poisoned from clean examples. | [M06.4](modules/m06-backdoors/lesson-4-detection-and-mitigation.md) |
| **Defense in depth** | Layering independent controls so one failure does not compromise the system. | [M11.6](modules/m11-serving-monitoring/lesson-6-secure-configuration-secrets-and-least-privilege.md) |

## 7. Serving, monitoring, and incident response

| Term | Meaning | Where it is taught |
|---|---|---|
| **Application programming interface (API)** | A defined way for software to call another service. | [M11.1](modules/m11-serving-monitoring/lesson-1-serving-architecture-and-attack-surface.md) |
| **Endpoint** | A specific URL and method that an API exposes. | [M11.1](modules/m11-serving-monitoring/lesson-1-serving-architecture-and-attack-surface.md) |
| **Authentication** | Proving who you are. | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| **Authorization** | Deciding what an authenticated identity may do. | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| **Role-based access control (RBAC)** | Granting permissions by role rather than by individual. | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| **Least privilege** | Giving each component only the access it needs for its task. | [M11.6](modules/m11-serving-monitoring/lesson-6-secure-configuration-secrets-and-least-privilege.md) |
| **Broken object level authorization (BOLA)** | A flaw where a user can access another user's object by changing its identifier. | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| **Rate limiting** | Restricting how many requests a caller may make in a time window. | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| **Quota** | A total allowance, often per day or per account, rather than per second. | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| **Input validation** | Rejecting requests that do not match the expected shape, type, or range. | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| **Schema** | A formal description of the fields and types a request must contain. | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| **Server-side request forgery (SSRF)** | Tricking a server into making a request to a destination the attacker chooses. | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) |
| **Secrets management** | Storing and rotating credentials outside source code and logs. | [M11.6](modules/m11-serving-monitoring/lesson-6-secure-configuration-secrets-and-least-privilege.md) |
| **Drift** | A change in input distribution or input–output relationship after deployment. | [M11.4](modules/m11-serving-monitoring/lesson-4-monitoring-drift-and-attack-indicators.md) |
| **Concept drift** | A change in the relationship between inputs and the correct output. | [M11.4](modules/m11-serving-monitoring/lesson-4-monitoring-drift-and-attack-indicators.md) |
| **Incident response** | The structured process of detecting, containing, eradicating, recovering from, and learning from an incident. | [M11.5](modules/m11-serving-monitoring/lesson-5-incident-response-rollback-and-evidence.md) |
| **Rollback** | Reverting a deployment to a previous known-good artifact. | [M11.5](modules/m11-serving-monitoring/lesson-5-incident-response-rollback-and-evidence.md) |
| **Canary string** | A unique marker placed in data or prompts so you can detect if it leaks. | [LAB-19](labs/lab-19.md) |

## 8. Generative AI, retrieval, and agents

| Term | Meaning | Where it is taught |
|---|---|---|
| **Large language model (LLM)** | A model trained on large text corpora to predict and generate text. | [M15.1](modules/m15-genai-llm-agents/lesson-1-from-predictive-ml-to-llm-security.md) |
| **Token** | A unit of text, roughly a word piece, that a language model processes. | [M15.1](modules/m15-genai-llm-agents/lesson-1-from-predictive-ml-to-llm-security.md) |
| **Prompt** | The input text given to a language model. | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| **System prompt** | Developer-supplied instructions that set the model's role and constraints. Treat it as sensitive, not as a security boundary by itself. | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| **Prompt injection** | Input that causes the model to follow attacker instructions instead of the intended ones. | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| **Direct prompt injection** | The attacker is the user and types the malicious instruction. | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| **Indirect prompt injection** | The malicious instruction arrives through retrieved documents, web pages, or tool output. | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md), [LAB-19](labs/lab-19.md) |
| **Instruction hierarchy** | A design where the model is trained or prompted to rank instruction sources by trust. | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| **Jailbreak** | An input that bypasses a model's safety or policy constraints. | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| **Retrieval-augmented generation (RAG)** | Supplying a model with retrieved documents at answer time to ground its output. | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md) |
| **Embedding** | A numeric vector representing text or another object so similarity can be computed. | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md) |
| **Vector store** | A database of embeddings with similarity search. | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md) |
| **Grounding** | Tying an answer to retrieved evidence so it can be checked. | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md) |
| **Hallucination** | A confident output that is not supported by evidence. | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| **Tool calling** | Letting a model invoke an external function or service. | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) |
| **Agent** | A system that uses a model to plan and take actions through tools, often over multiple steps. | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) |
| **Excessive agency** | An agent has more capability, permissions, or autonomy than the task requires. | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md), [LAB-20](labs/lab-20.md) |
| **Confused deputy** | A privileged component is tricked into using its authority on behalf of an attacker. | [LAB-20](labs/lab-20.md) |
| **Approval gate** | A control that pauses a sensitive action until a human or policy authorizes it. | [LAB-20](labs/lab-20.md) |
| **Allowlist** | An explicit list of permitted values; anything else is denied. | [LAB-20](labs/lab-20.md) |
| **Exfiltration** | Moving data out of a system without authorization. | [M07.1](modules/m07-extraction-privacy/lesson-1-prediction-apis-as-attack-surface.md) |
| **Unbounded consumption** | Resource use without limits, leading to cost or availability harm. | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |

## 9. Explainability and fairness

| Term | Meaning | Where it is taught |
|---|---|---|
| **Explanation** | Information about why a model produced an output. It can be faithful, plausible, or neither. | [M14.1](modules/m14-explainability-fairness/lesson-1-explanation-methods-and-assumptions.md) |
| **Local explanation** | An explanation for one prediction rather than the whole model. | [M14.1](modules/m14-explainability-fairness/lesson-1-explanation-methods-and-assumptions.md) |
| **LIME (Local Interpretable Model-agnostic Explanations)** | A method that fits a simple surrogate around one prediction. | [M14.1](modules/m14-explainability-fairness/lesson-1-explanation-methods-and-assumptions.md) |
| **SHAP (SHapley Additive exPlanations)** | A method that assigns additive feature attributions based on cooperative-game theory. | [M14.1](modules/m14-explainability-fairness/lesson-1-explanation-methods-and-assumptions.md) |
| **Attribution** | The share of an output assigned to each feature. | [M14.1](modules/m14-explainability-fairness/lesson-1-explanation-methods-and-assumptions.md) |
| **Explanation stability** | Whether small input changes produce small explanation changes. Unstable explanations are hard to audit and easy to manipulate. | [M14.2](modules/m14-explainability-fairness/lesson-2-explanation-leakage-and-manipulation.md), [LAB-18](labs/lab-18.md) |
| **Demographic parity** | A fairness criterion requiring similar positive rates across groups. | [M14.3](modules/m14-explainability-fairness/lesson-3-fairness-metrics-and-subgroups.md) |
| **Equalized odds** | A fairness criterion requiring similar true-positive and false-positive rates across groups. | [M14.3](modules/m14-explainability-fairness/lesson-3-fairness-metrics-and-subgroups.md) |
| **Subgroup audit** | Measuring performance separately for defined groups instead of only in aggregate. | [LAB-18](labs/lab-18.md) |

## 10. Governance and assessment

| Term | Meaning | Where it is taught |
|---|---|---|
| **Risk** | A combination of the likelihood of harm and its severity, for a stated system and use. | [M03.4](modules/m03-threat-modeling/lesson-4-frameworks-and-crosswalks.md) |
| **Residual risk** | The risk that remains after controls are applied. Every lab report should state it. | [M16.4](modules/m16-end-to-end-assessment/lesson-4-findings-severity-and-remediation.md) |
| **Control** | A safeguard that reduces risk: a technical mechanism, a process, or a policy. | [M03.1](modules/m03-threat-modeling/lesson-1-security-fundamentals.md) |
| **Severity** | A structured judgment of how serious a finding is, ideally tied to impact and exploitability. | [M16.4](modules/m16-end-to-end-assessment/lesson-4-findings-severity-and-remediation.md) |
| **Rules of engagement** | The written scope, authorization, limits, and reporting rules for a security test. | [M00.3](modules/m00-orientation/lesson-3-rules-of-engagement.md), [M17.1](modules/m17-red-team-blue-team/lesson-1-rules-of-engagement-and-threat-model.md) |
| **Red team** | The group playing the adversary, within the rules of engagement. | [M17.2](modules/m17-red-team-blue-team/lesson-2-red-team-planning-and-execution.md) |
| **Blue team** | The group defending, detecting, and responding. | [M17.3](modules/m17-red-team-blue-team/lesson-3-blue-team-detection-and-response.md) |
| **Purple team** | A joint exercise where red and blue share findings to improve detection and prevention. | [M17.4](modules/m17-red-team-blue-team/lesson-4-purple-team-synthesis-and-adaptation.md) |
| **Coordinated disclosure** | Reporting a vulnerability privately, allowing time to fix it, before publishing details. | [M00.3](modules/m00-orientation/lesson-3-rules-of-engagement.md) |

## Acronym quick reference

| Acronym | Expansion | First explained in |
|---|---|---|
| AML | Adversarial machine learning | [M03.2](modules/m03-threat-modeling/lesson-2-adversaries-and-taxonomy.md) |
| API | Application programming interface | [M11.1](modules/m11-serving-monitoring/lesson-1-serving-architecture-and-attack-surface.md) |
| ASR | Attack success rate | [M04.5](modules/m04-evasion/lesson-5-measuring-honestly.md) |
| ATLAS | Adversarial Threat Landscape for AI Systems (MITRE) | [M03.3](modules/m03-threat-modeling/lesson-3-surfaces-lifecycle-atlas.md) |
| BOLA | Broken object level authorization | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| DP | Differential privacy | [M13.2](modules/m13-privacy-preserving-ml/lesson-2-differential-privacy-first-principles.md) |
| DP-SGD | Differentially private stochastic gradient descent | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| FGSM | Fast Gradient Sign Method | [M04.2](modules/m04-evasion/lesson-2-fgsm.md) |
| FPR / FNR | False positive rate / false negative rate | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| HE | Homomorphic encryption | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| LLM | Large language model | [M15.1](modules/m15-genai-llm-agents/lesson-1-from-predictive-ml-to-llm-security.md) |
| ML-BOM | Machine-learning bill of materials | [M09.1](modules/m09-data-integrity/lesson-1-provenance-and-lineage.md) |
| MPC | Secure multi-party computation | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |
| ONNX | Open Neural Network Exchange | [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md) |
| PGD | Projected Gradient Descent | [M04.3](modules/m04-evasion/lesson-3-pgd.md) |
| PII | Personally identifiable information | [M13.1](modules/m13-privacy-preserving-ml/lesson-1-privacy-threat-models.md) |
| RAG | Retrieval-augmented generation | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md) |
| RBAC | Role-based access control | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| ROC / AUROC | Receiver operating characteristic / area under the ROC curve | [M02.3](modules/m02-ml-fundamentals/lesson-3-evaluation.md) |
| SBOM | Software bill of materials | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |
| SLSA | Supply-chain levels for software artifacts | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |
| SSDF | Secure Software Development Framework (NIST) | [M09.4](modules/m09-data-integrity/lesson-4-reproducible-training.md) |
| SSRF | Server-side request forgery | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) |
| TEE | Trusted execution environment | [M13.4](modules/m13-privacy-preserving-ml/lesson-4-private-training-and-secure-computation.md) |

## Terms that are often confused

| Pair | The distinction that matters |
|---|---|
| Evasion vs. poisoning | Evasion happens at prediction time; poisoning happens during training. A backdoor uses poisoning to set up later evasion. |
| Robustness vs. security | Robustness is a measured property under a stated perturbation model. Security is a broader claim about an adversary achieving a goal. A robust model can still leak data. |
| Anonymization vs. differential privacy | Anonymization edits records and is vulnerable to linkage. Differential privacy bounds the influence of any one record and comes with a formal parameter. |
| Authentication vs. authorization | Authentication proves identity; authorization decides permission. Confusing them produces broken access control. |
| Prompt injection vs. jailbreak | Injection overrides *whose* instruction is followed. A jailbreak bypasses *policy* constraints. They overlap but are not the same test. |
| Drift vs. attack | Drift is a change in data. An attack is deliberate. Monitoring sees both, and neither label is safe to assume without evidence. |
| Fairness vs. accuracy | A model can be accurate overall and unequal across subgroups. Aggregate accuracy hides the harm. |
| Hash vs. signature | A hash detects change but anyone can recompute it. A signature binds an artifact to a key holder. |

## Where to go next

- [References](references.md) — the primary sources for these definitions.
- [Framework mapping](framework-mapping.md) — how these terms map to NIST, ATLAS, and OWASP identifiers.
- [Research reading guide](research-reading-guide.md) — reading order for the papers that introduced these ideas.
- [Course roadmap](modules/index.md) — module outcomes and prerequisites.
