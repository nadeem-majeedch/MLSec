# LAB-16 — Federated Learning Attack and Defense Simulation

**Tier A · 5 hours · Difficulty 4 · Module M12 · Outcomes LO-24, LO-28**

## Why this lab exists

Federated learning moves the data to the clients and the model to the server. It
does not move trust. A participant that controls its own data and its own update
can try to steer the shared model, and the server may see nothing but a vector of
numbers. The practical question is not whether federation is "private" or
"secure" in general. It is which trust assumptions the aggregation rule actually
needs, and what happens when one of them is false.

This lab builds a small FedAvg simulation with eight non-IID clients, one
compromised participant, and three aggregation rules. Every run uses the same
partition, the same twelve rounds, and the same local training budget. The
comparison is therefore about the rule, not about training longer. The reference
result is deliberately mixed: coordinate-wise trimmed mean removes this
particular scaled update, norm clipping does not, and neither result is a
guarantee.

## The system and the threat model

| Element | Assumption |
|---|---|
| Asset | A shared digit classifier and its behavior on inputs carrying a trigger |
| Attacker goal | Integrity: install a target-class backdoor without controlling the server or the other clients |
| Attacker knowledge | The protocol, model architecture, local data, and the fact that updates are averaged |
| Attacker capability | Control one client's training data and the update it submits; scale that update |
| Coordinator | Honest in this lab: it follows the chosen rule and evaluates the global model |
| Constraints | Eight clients, twelve rounds, eight local epochs, one malicious client, update scale 6.0 |
| Data | Bundled scikit-learn digits, 1,257 training rows split non-IID, 540 test rows |
| Metric | Clean test accuracy and attack success rate on the 486 test rows whose label is not the target |
| Lifecycle stage | Training and model supply chain |
| Out of scope | Network failures, stragglers, client sampling, secure aggregation implementation, differential privacy, Sybil majorities, adaptive attackers |

The clients are Python objects in one process. No socket, federated framework,
GPU, or cloud account is involved. That simplification removes systems noise so
the aggregation arithmetic is visible. It also removes realism: production
federation has partial participation, variable client availability, and a
coordinator that may be honest-but-curious rather than merely honest.

## What you produce

A folder inside `labs/lab-16-federated-learning/` containing:

| File | Contents |
|---|---|
| `metrics.json` | Configuration, partition sizes and class counts, four runs, twelve-round histories |
| `run.json` | Lab id, seed, clients, rounds, malicious client, attack scale, clip norm, trigger, target |
| `report.md` | Setup, equal-round results, interpretation, residual risk, limitations |
| `manifest.json` | SHA-256 hashes of the three files above |

The reference implementation writes these under `artifacts/`. Your completed
`starter.py` must produce the same structure.

## Prerequisites

- Module 12 Lessons 1–5 (architecture, update poisoning, aggregation, validation, evaluation).
- Module 04 Lessons 2–4 (poisoning and backdoors) and LAB-05 or LAB-07.
- Module 02 (softmax regression, cross-entropy, train/test evaluation).
- Module 03 (threat modeling and scoped claims).

## Environment

- Python 3.14.7; `numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `joblib==1.5.3`, `PyYAML==6.0.3`.
- CPU only; the reference run takes a few seconds and writes well under 1 MB.
- No network, no cloud account, no API key. The digits dataset ships with scikit-learn.
- No federated-learning framework is required. Flower, TensorFlow Federated, or a
  production parameter server would add orchestration, serialization, and client
  sampling, but they would not change the aggregation logic you are studying.
  This lab is the lightweight alternative.

```bash
cd labs/lab-16-federated-learning
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab16.py --artifacts artifacts
```

## Safety rules

- Use only the bundled digits data and the synthetic trigger. Do not point this code at a real federated deployment.
- Do not add network transport or connect the simulated clients to any external service.
- Do not describe the result as a working attack on a named product or as proof that federated learning is unsafe.
- Keep the malicious update bounded and local. The lab is a simulation, not a tool for disrupting a training job.
- Delete `artifacts/` when finished if your environment does not ignore it.

## Task specification

1. **Build the non-IID partition.** For each class 0–9, collect its training
   indices, shuffle them with `np.random.default_rng(42)`, and split 70/30. Give
   the first 70% to client `label % 8` and the last 30% to client
   `(label + 3) % 8`. Return sorted index arrays. The shards must cover all 1,257
   rows, and no client may see more than a few classes.
2. **Train locally.** Start from the current global `(weights, bias)` pair. Run
   eight full-batch softmax-regression epochs with cross-entropy, learning rate
   0.5, and L2 coefficient `1e-3`. Return new arrays; do not mutate the global
   model in place.
3. **Run benign FedAvg.** For twelve rounds, collect all eight client updates and
   average them weighted by local sample count. This is the reference for clean
   accuracy and the false-positive behavior of the trigger.
4. **Run the malicious baseline.** Client 0 appends triggered copies of its own
   training rows, relabels those copies to class 0, trains locally, and then
   scales its update by 6.0 relative to the global model. Aggregate with the same
   size-weighted mean.
5. **Implement coordinate-wise trimmed mean.** Stack the eight flattened updates,
   sort each coordinate independently, drop the lowest one and the highest one,
   and average the six remaining values. Unflatten to `(weights, bias)`.
6. **Evaluate norm clipping.** For each client, compute the delta from the global
   model, scale it down when its L2 norm exceeds 2.0, and average the clipped
   deltas with equal weights. Clipping preserves direction; it does not remove a
   coordinated backdoor signal.
7. **Measure both sides.** Clean accuracy is the fraction of all test rows
   classified correctly. Attack success is the fraction of triggered test rows
   whose true label is not 0 that are classified as 0. Report both for every run.
8. **Keep the comparison fair.** Use the same partition, client order, round
   count, local epochs, and trigger for all four runs. A defense that wins only
   because it trained longer has not been evaluated.
9. **Report the residual risk.** Explain why trimmed mean worked here, why that
   does not generalize, what a Sybil attacker changes, and what secure
   aggregation does and does not protect.

## Aggregation and measurement protocol

The order below is part of the experiment design:

1. **Split once.** Hold out 30% of digits as a test set; never train on it.
2. **Partition the training rows.** Freeze the shards before any attack run.
3. **Train benign.** Record clean accuracy and the base rate of trigger false
   positives.
4. **Train malicious with mean aggregation.** Establish that the scaled update
   installs the trigger.
5. **Re-run with each defense.** Change only the aggregation rule.
6. **Evaluate on the same test rows.** Use 486 non-target rows for attack success.
7. **Compare at equal rounds.** Do not tune one rule with more rounds or epochs.
8. **State the scope.** One trigger, one target, one partition, one attack scale.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `partition_clients` | Build a deterministic non-IID client partition |
| `starter.py` | TODO 2 | `train_local` | Train a softmax model for a fixed number of full-batch steps |
| `starter.py` | TODO 3 | `aggregate_trimmed_mean` | Apply coordinate-wise trimmed mean |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-16-federated-learning/CHECKING.md`.

## Expected outputs

Reference results from the seed-42 run:

| Run | Clean accuracy | Attack success rate |
|---|---:|---:|
| Benign, mean aggregation | 0.9000 | 0.0021 |
| Malicious, mean aggregation | 0.7056 | 1.0000 |
| Malicious, coordinate-wise trimmed mean | 0.8704 | 0.0000 |
| Malicious, norm clipping | 0.8944 | 0.6276 |

The partition has eight shards with sizes 210, 215, 124, 164, 165, 126, 127,
and 126. Each client sees two or three classes. The test set has 540 rows, of
which 486 are eligible attack rows.

Useful deltas:

| Comparison | Clean accuracy | Attack success |
|---|---:|---:|
| Malicious mean minus benign mean | −0.1944 | +0.9979 |
| Trimmed mean minus malicious mean | +0.1648 | −1.0000 |
| Trimmed mean minus benign mean | −0.0296 | −0.0021 |
| Clipping minus malicious mean | +0.1888 | −0.3724 |
| Clipping minus benign mean | −0.0056 | +0.6255 |

Trimmed mean removed the attack in this configuration and cost 2.96 points of
clean accuracy relative to benign training. Clipping preserved almost all clean
accuracy but blocked only 37.24 points of attack success, leaving 62.76% of
triggered rows misclassified to the target.

## Threat-to-control mapping

| Threat | Evidence in the lab | Control tested | Residual risk |
|---|---|---|---|
| One client poisons the global model (AML.T0020) | Malicious mean reaches ASR 1.0000 | None; this is the baseline | Any participant can influence the aggregate |
| Backdoor installed in the global model (AML.T0018) | Trigger works while clean accuracy stays at 0.7056 | Clean-accuracy monitoring alone | A 70% clean model still looks usable |
| Scaled update dominates the mean | One client moves the aggregate | Coordinate-wise trimmed mean | Sybil clients can fill the trimmed middle |
| Large update norm | Clipping changes ASR to 0.6276 | Per-client L2 norm bound | Direction survives; a patient attacker spreads the signal |
| Update inspection by the server | Server sees every vector in this lab | Secure aggregation (discussed, not implemented) | Hides contents; does not detect a poisoned aggregate |
| Overstated defense claim | Trimmed mean ASR is exactly 0.0000 here | Equal-round comparison and scoped reporting | One trigger, target, partition, and scale |

ATLAS identifiers are used for orientation only. The mapping is not a claim that
these are the only techniques an attacker could use.

## Defense-in-depth perspective

Robust aggregation is one layer. It assumes a bounded number of malicious
clients, and its guarantees usually depend on assumptions about update geometry
or on knowing which clients are honest. Client validation adds identity,
provenance, and update-statistic checks. Monitoring compares the global model
against a clean reference and tests known triggers. Secure aggregation protects
update confidentiality from the server, but a poisoned aggregate can still be
computed from hidden updates. Differential privacy in federated learning limits
what any single client contributes and can bound some influence, but it is a
privacy mechanism, not a backdoor detector.

The layers fail differently. Trimmed mean fails when the attacker controls enough
identities. Clipping fails when the attack direction is consistent across rounds.
Secure aggregation fails to help with integrity at all. A clean-accuracy check
fails when the backdoor is rare. The lab is designed so that each defense looks
good on one metric and incomplete on another.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Clean accuracy and ASR for the benign baseline, the attack, and each defense at equal rounds.
- [ ] `report.md` answers every reflection question and states the limits of trimmed mean and clipping.
- [ ] `python check_lab16.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] The partition covers all 1,257 training rows and every client sees at most four classes.
- [ ] Each of the four runs records twelve round histories.
- [ ] Benign mean aggregation reaches clean accuracy ≥ 0.85 and ASR ≤ 0.10.
- [ ] Malicious mean aggregation keeps clean accuracy ≥ 0.60 and reaches ASR ≥ 0.90.
- [ ] Trimmed mean reaches ASR ≤ 0.10 and keeps clean accuracy ≥ 0.80.
- [ ] Norm clipping leaves ASR between 0.30 and 0.90 and keeps clean accuracy ≥ 0.85.
- [ ] Both defenses lower ASR relative to mean aggregation.
- [ ] The report contains "equal rounds", "residual risk", "limitations", "Sybil", and "secure aggregation".
- [ ] `python check_lab16.py --artifacts artifacts` exits 0.

## How to check yourself

The checker rebuilds the digits split and the non-IID partition, validates the
recorded configuration, and checks each run against the expected bands. It does
not re-train your model. A forged `metrics.json` with plausible numbers could
pass the checker, which is why the report and the reflection questions carry part
of the grade. Reproduce the four rows from a clean process before you submit.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct non-IID partition and local training | 5 |
| Correct attack construction and ASR evaluation | 4 |
| Correct coordinate-wise trimmed mean | 3 |
| Correct per-client norm clipping | 2 |
| Equal-round comparison with both metrics | 2 |
| Residual risk, Sybil, secure aggregation, and limitations | 2 |
| Reproducible artifacts and manifest | 2 |

## Reflection questions

1. Why does starting each local epoch from the global model matter for FedAvg?
2. The malicious client's clean accuracy is 0.7056. Why is that still a
   dangerous outcome, and what would a clean-accuracy-only monitor conclude?
3. Trimmed mean reaches ASR 0.0000 here. State the strongest claim you can make
   from that result, and one claim you cannot make.
4. Clipping preserves the update direction. Explain why that makes it a poor
   defense against a consistently directed backdoor.
5. How would a Sybil attacker with three of eight identities change the trimmed
   mean calculation? What would the server need to know to prevent it?
6. Secure aggregation hides updates from the server. Why is that a privacy
   control rather than an integrity control?
7. If you added differential privacy to the local updates, which metric would
   move first, and why would that not prove the backdoor is gone?
8. What would you add to this experiment before using either defense in a real
   cross-silo federation?

## Hints

1. Partition by class and client so the federation is non-IID, but keep every client's data non-empty and deterministic.
2. Local training is full-batch softmax regression for a fixed number of epochs. Record the learning rate and epochs.
3. Trimmed mean sorts each coordinate, removes the extremes, and averages the rest. Do it per coordinate, not per client.
4. Compare all methods at the same number of rounds. If the defense gets more rounds, the comparison is invalid.

## Time box

| Hour | Work |
|---|---|
| 1 | Read the simulation, implement the partition, inspect class counts |
| 2 | Implement local training and reproduce benign FedAvg |
| 3 | Implement the malicious update and the mean-aggregation baseline |
| 4 | Implement trimmed mean and clipping; run all four comparisons |
| 5 | Write the report: equal-round interpretation, residual risk, limitations |

Stop at 7.5 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement `partition_clients`, `train_local`, or `aggregate_trimmed_mean` |
| Benign accuracy near 0.1 | Local training reinitializes weights each round | Start from the current global `(weights, bias)` |
| Benign accuracy far below 0.90 | Too few local epochs or a wrong learning rate | Keep eight epochs and learning rate 0.5 |
| Malicious ASR near 0 | Trigger not applied at evaluation | Apply the same four-pixel trigger to test rows |
| All runs identical | The `malicious` flag or rule name is not reaching the loop | Print the rule and client id per round |
| Trimmed mean crashes | `trim=1` leaves six rows; a larger trim can empty the array | Keep eight clients and one trimmed value per side |
| Clipping has no effect | Delta computed after aggregation rather than per client | Clip each client delta against the global model |
| Report rejected | Missing one of the required phrases | Discuss equal rounds, Sybil clients, and secure aggregation explicitly |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — R-70, R-71, R-72, R-73, R-74
- [Module page](../modules/m12-federated-learning/index.md) — M12 — Federated Learning Security and Distributed ML Threats
- Package checking guide: `labs/lab-16-federated-learning/CHECKING.md`

## What comes next

[LAB-17](lab-17.md) turns from model integrity to the privacy of the people in
the training data. Module 13 Lessons 1–5 introduce neighboring datasets,
sensitivity, composition, and the difference between a formal differential
privacy claim and an empirical membership signal.
