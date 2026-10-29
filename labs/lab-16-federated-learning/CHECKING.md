# Checking Guide — LAB-16

## What the checker verifies

1. `metrics.json`, `run.json`, `report.md`, and `manifest.json` exist, and the manifest covers the three output files.
2. `run.json` records LAB-16, eight clients, twelve rounds, a malicious client at index 0, an attack scale above 1, and a positive clipping norm.
3. The checker rebuilds the digits training split and the non-IID partition; the shards cover all 1,257 training rows and every client sees at most four classes.
4. Every run has twelve round histories and accuracy/ASR values in [0, 1].
5. Benign mean aggregation: clean accuracy ≥ 0.85 and ASR ≤ 0.10.
6. Malicious mean aggregation: clean accuracy ≥ 0.60 and ASR ≥ 0.90.
7. Trimmed mean: ASR ≤ 0.10 and clean accuracy ≥ 0.80.
8. Norm clipping: ASR between 0.30 and 0.90 and clean accuracy ≥ 0.85.
9. Both defenses lower ASR relative to mean aggregation.
10. The report contains "equal rounds", "residual risk", "limitations", "Sybil", and "secure aggregation".

## Reference results (seed 42)

| Run | Clean accuracy | Attack success rate |
|---|---:|---:|
| Benign, mean aggregation | 0.9000 | 0.0021 |
| Malicious, mean aggregation | 0.7056 | 1.0000 |
| Malicious, trimmed mean | 0.8704 | 0.0000 |
| Malicious, norm clipping | 0.8944 | 0.6276 |

All runs use the same eight-client partition (1,257 training rows), twelve rounds,
eight local epochs, attack scale 6.0, and norm bound 2.0.

## Why these numbers matter

The scaled update is strong enough to install a trigger while leaving about 70%
clean accuracy, which is why a single clean-accuracy check would miss it. Trimmed
mean discards the extreme coordinate values, so in this configuration it removes
the attack almost completely. Clipping limits the update norm but preserves its
direction, so the backdoor still succeeds on 62.8% of triggered rows.

The correct conclusion is conditional: "trimmed mean removed this scaled update
in this partition, at this attack scale." It is not "trimmed mean prevents
backdoors." A Sybil attacker with several identities, a smaller and slower update,
or a different trigger can change the result.

## Threat-to-control mapping

| Threat | Control tested | Metric | Residual risk |
|---|---|---|---|
| One client injects a backdoor | Mean aggregation baseline | Clean accuracy, ASR | No defense; attack succeeds |
| Scaled update dominates the mean | Coordinate-wise trimmed mean | ASR, clean cost | Sybil clients can fill the trimmed middle |
| Large update norm | Per-client norm clipping | ASR, clean cost | Direction survives; slow attack evades the bound |
| Server reads every update | Secure aggregation (discussed, not implemented) | Privacy only | Hides contents, not a poisoned aggregate |
| Overstated defense claim | Equal-round comparison | Both metrics | One trigger, target, partition, and scale |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Benign accuracy near 0.1 | Clients reinitialize instead of starting from global weights | Pass the current global model into local training |
| Malicious ASR near 0 | Trigger not applied at evaluation, or target not in the model's labels | Apply the same trigger function to test rows |
| Trimmed mean code crashes | Trimming more rows than the client count allows | With eight clients and `trim=1`, six rows remain |
| All runs identical | The malicious flag or aggregation rule is not reaching the training loop | Print the rule and client id per round |
| ASR reported without clean accuracy | Missing the utility side of the trade-off | Report both for every run |

## Rubric

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
