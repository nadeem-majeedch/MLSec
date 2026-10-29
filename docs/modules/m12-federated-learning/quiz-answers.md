# Knowledge Check Answers — QZ-12

**Module 12 · 10 items · 14 points**

## 1. (1 point) — B

A client sends a model update, or its locally trained weights, derived from its local data. Raw data stays local in the honest protocol. The coordinator receives derived values, not records.

## 2. (2 points)

The weighted numerator is

\[
200(0.2,-0.1) + 300(0.4,0.2) + 500(-0.2,0.3)
= (40,-20) + (120,60) + (-100,150)
= (60,190).
\]

The total sample count is \(200+300+500=1{,}000\), so the weighted mean update is

\[
(60/1000,\ 190/1000) = (0.06,\ 0.19).
\]

The 500-row client has half the weight, which is why its negative first coordinate does not make the aggregate negative.

## 3. (2 points)

The \(5/12 = 0.4167\) figure assumes equal sample weights and only the update scale. Doubling the declared sample count also doubles the client's sample weight. With roughly equal benign counts \(n\), the malicious client reports \(2n\), so the total is \((K-1)n + 2n = (K+1)n\). Its weight is \(2/(K+1)\), not \(1/K\). For \(K=8\), that is \(2/9 = 0.2222\) instead of \(0.1111\). Scaling by 5 then makes its effective directional contribution about \(5 \times 0.2222 = 1.111\) units against \(0.1111\) per benign client, roughly ten times a benign client.

Controls:

- **Sample count:** cap and audit the declared count; use a contribution bound independent of self-reported size.
- **Update magnitude:** norm clipping or a per-coordinate bound.
- **Identity:** participation caps limit how many contributions one principal can make.

Any one bound addresses one source; the scenario needs both the count and the magnitude bounded.

## 4. (1 point) — B

The rule needs \(2m < K\) so that at least one value remains after trimming both tails. If \(2m \ge K\), there is nothing left to average, or the result is undefined.

## 5. (2 points)

Sorted: \(0.5,\ 0.6,\ 0.7,\ 0.8,\ 9.0\).

- Mean: \((0.5+0.6+0.7+0.8+9.0)/5 = 11.6/5 = 2.32\).
- 1-trimmed mean: remove 0.5 and 9.0, average \(0.6,0.7,0.8\) = \(2.1/3 = 0.70\).
- Median: the middle value, \(0.70\).

The mean is more than three times the robust statistics because of the single 9.0.

## 6. (1 point) — B

\(2m + 3 \le 9\) gives \(2m \le 6\), so \(m \le 3\). The largest integer is 3. With \(m=4\), Krum's condition is violated.

## 7. (2 points)

The clean accuracy of 0.8944 is close to the benign 0.9000, so the main task is largely intact. The attack success rate of 0.6276 means that 62.76% of triggered non-target rows are still predicted as the attacker's target. The backdoor is present and effective on most triggered inputs.

The conclusion is wrong because clean accuracy measures the main task, not the trigger condition. Clipping bounds the update's norm, but the backdoor direction survives the reduction. A defense that improves accuracy while leaving most of the backdoor intact has not removed the threat. The correct statement is that clipping reduced ASR by 37.24% and left 62.76% residual attack success in this configuration.

## 8. (1 point)

No. Secure aggregation hides individual updates from the coordinator, but the coordinator still aggregates the poisoned contribution into the global model. It is a confidentiality control, not an integrity control. Poisoning defenses such as robust aggregation, validation, and monitoring are still required.

## 9. (1 point)

The comparison does not hold the training budget fixed. The robust aggregator runs 40 rounds and FedAvg runs 10, so the difference in attack success may reflect longer training rather than robustness. A valid comparison uses equal rounds, the same clients, partition, local epochs, and evaluation set, and changes only the aggregation rule. The vendor should also report clean accuracy and the attacker model.

## 10. (1 point)

Any answer that scopes the claim to the tested configuration and states the residual risk earns the point. Example:

> Under the LAB-16 threat model — one malicious client among eight, digits data, a 2×2 trigger targeting class 0, a 6× update scale, and 12 equal rounds — the coordinate-wise trimmed mean with one value trimmed per tail reduced attack success from 1.0000 to 0.0000 while clean accuracy moved from 0.9000 to 0.8704. This does not establish robustness against two colluding clients, an adaptive attacker, a different trigger, a larger model, or Sybil identities, and it does not address privacy leakage.

The essential parts are the attacker, the fixed configuration, the measured result, and the exclusions.
