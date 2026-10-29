# QZ-12B Answer Key — Module 12

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. A — sample-weighted average

FedAvg forms a weighted average of client updates, with weights proportional to the number of examples each client used. The coordinator does not receive raw data; that is the point of federated training.

- **B** describes a norm-based or robust selection rule, not FedAvg.
- **C** would be centralized training.
- **D** ignores the update values and cannot train a model.

Tag: M12 · LO-24 · Bloom 2 · D1.

## 2. A — closest to its neighbors

Krum scores each update by its distance to its nearest neighbors and selects the update with the smallest score, on the assumption that honest updates cluster. It is a selection rule, not a coordinate-wise average.

- **B** describes a trimmed mean variant.
- **C** describes clipping plus averaging.
- **D** confuses the client-count condition with the selection rule.

Tag: M12 · LO-24 · Bloom 2 · D1.

## 3. True

Clipping bounds how far one update can move the aggregate, so it can reduce an attacker's influence. It does not remove the attack: the lab reports attack success still well above the benign baseline under norm clipping. A defense can reduce harm without making the attack fail, and the report must show both clean accuracy and attack success.

Tag: M12 · LO-24 · Bloom 3 · D2.

## 4. False

More rounds give an adaptive attacker more opportunities to influence the aggregate, and they can also amplify a persistent bias. Whether robustness improves depends on the aggregator, the attacker's strategy, the client fraction, and the evaluation point. "More rounds" is not a defense property; it must be measured at a fixed comparison point.

Tag: M12 · LO-24 · Bloom 2 · D1.

## 5. Required element

The aggregator is only one variable. Different rounds or attack scales change both the attacker's opportunity and the model's state, so an improvement cannot be attributed to the defense. A fair comparison fixes the number of rounds, the attacker fraction, the update scale, the client sampling, and the seeds, then varies only the aggregator.

Tag: M12 · LO-24 · Bloom 3 · D2.

## 6. Weighted mean = (0.14, 0.08)

Total rows: $100 + 400 + 500 = 1000$.

- First coordinate: $(100 \times 0.1) + (400 \times -0.3) + (500 \times 0.5) = 10 - 120 + 250 = 140$; $140/1000 = 0.14$.
- Second coordinate: $(100 \times 0.2) + (400 \times 0.4) + (500 \times -0.2) = 20 + 160 - 100 = 80$; $80/1000 = 0.08$.

The weighted mean is $(0.14, 0.08)$. An unweighted mean would give a different answer, which is why the weighting rule must be stated with the result.

Tag: M12 · LO-24 · Bloom 3 · D2.

## 7. Required elements (two flaws and the influence explanation)

Two of:

- **Clipping is applied after averaging.** The mean is computed from unbounded updates, so a client can move it before any bound is applied. Clipping the aggregate does not bound any individual client's influence.
- **There is no per-update norm bound.** The code never computes or limits $\|u_i\|$; a scaled update enters the mean at full strength.
- **The clip range may not bind.** If the mean falls inside $[-1, 1]$, `np.clip` changes nothing and the attacker's effect is untouched.
- **No robust aggregation or sample-count control.** A client can also inflate its declared weight unless the coordinator caps or verifies it.

A client that scales its update by 20 shifts the mean by roughly $20/K$ times its original contribution (depending on the other updates), and the final clip only limits the coordinate value, not the direction or the influence. The defense must clip or normalize each update before aggregation, and it must state the norm and threshold.

Tag: M12 · LO-24 · Bloom 4 · D3.

## 8. Required elements (threat model, controls, metrics, conditions, risks)

Threat model:

- One or more malicious clients can submit updates; they know the aggregation rule and can scale, sign-flip, or craft updates; the attacker fraction and sybil capability are bounded and stated.
- The goal is a targeted or global integrity effect, not disclosure of other clients' data.

Controls:

- Coordinate-wise trimming with a stated $m$ and the condition $2m < K$.
- Norm clipping with a stated threshold applied per client before averaging.
- Optional: Krum or another selection rule, sample-count verification, and a cap on per-client weight.

Metrics:

- Clean or benign accuracy on a held-out set.
- Attack success on the targeted outcome, against the benign baseline.
- Benign-client accuracy or rejection rate, to show the cost of the defense.
- Uncertainty across seeds or client samples.

Comparison conditions: same rounds, same attacker fraction and scale, same client sampling, same data and seeds; vary only the aggregator. Report negative results, including a defense that fails.

Residual risks: sybil identities can defeat assumptions about the attacker fraction; a malicious coordinator can see or manipulate updates; an adaptive attacker can shape updates to survive trimming; clipping reduces but does not eliminate poisoning; secure aggregation protects confidentiality, not integrity.

Tag: M12 · LO-24 · Bloom 5 · D3.
