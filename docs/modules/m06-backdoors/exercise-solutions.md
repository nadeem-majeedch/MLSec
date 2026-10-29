# Module 06 Exercise Solutions

**Read after a first attempt.** Some exercises ask for judgment; the reasoning matters more than matching these ratings exactly.

---

## Exercise 1 — Audit backdoor metrics

**1. Attack effect.**

- LAB-07: $0.8571 - 0.1771 = 0.6800$, or **68.0 percentage points**.
- LAB-08: $0.9818 - 0.0000 = 0.9818$, or **98.2 percentage points**.

**2. Poison rates.**

- LAB-07: $67 / 840 = 0.0798$, or **7.98%**.
- LAB-08: $20 / 249 = 0.0803$, or **8.03%**.

**3. Clean-accuracy drops.**

- LAB-07: $0.8444 - 0.8306 = 0.0138$, or **1.4 points**.
- LAB-08: $0.9907 - 0.9722 = 0.0185$, or **1.9 points**.

**4. Which is cleaner.** LAB-08 has a cleaner baseline: the clean model never sends a patched class-0 image to class 1 (0.0000), so almost the entire 0.9818 is attack effect. LAB-07 is still a valid demonstration: its increase is 68 points, the trigger and screen are visible, and the mechanism is clear. But its raw ASR of 0.8571 includes a 0.1771 clean-model response, so the number looks larger than the attack's contribution.

**5. Two errors in "85.7% ASR means 85.7% compromised."**

- **No baseline.** The clean model already sends 17.7% of triggered source inputs to the target; the attack effect is the 68-point increase, not the raw 85.7%.
- **ASR is conditional.** It measures behavior only on inputs carrying the trigger, not the fraction of the model's overall behavior that is compromised. The model's behavior on ordinary inputs is described by clean accuracy and slice metrics, not by ASR.

---

## Exercise 2 — Trigger design trade-offs

**1. Example ratings.**

| ID | Effectiveness | Stealth | Detectability | Reasoning |
|---|---|---|---|---|
| A | High | Low | High | Three extreme values strongly shift a linear score, but a simple threshold sees them |
| B | Medium | Medium | Medium | One 2.0 value is weaker but sits just below the LAB-07 screen; a distribution check can still notice it |
| C | High | Low | High if scanned | A white 2×2 block reliably shifts an image model but is visible and shape-specific |
| D | Medium | High | Low for patch/feature checks | A small global shift is hard to localize; distribution-level checks may see it |
| E | High (in text) | High | High if text filters exist | A rare phrase is a strong conditional cue and invisible to image defenses |

A defensible answer can change a rating if it gives a reason. "A is high effectiveness because the trigger sets three features to an extreme value and linear models can give them large weights" is better than a bare label.

**2. Attacker ranking.** A reasonable criterion is reliability per poisoned row. C or A rank high because the trigger is discrete and strongly associated with the target; D ranks lower because a small global shift requires more rows or a larger budget to overcome the clean signal. E can rank high in a text system, but its effectiveness depends on the tokenizer and the model.

**3. Defender ranking.** With data inspection and one patch scan, **D** is hardest to cover: it has no fixed location or shape for the scan, and a small per-pixel change may not cross a feature threshold. A distribution-level check or an input-sensitivity test is a better fit. E is outside an image-only defense entirely. The point is that the defender's ranking depends on the tools, not just on the attack's strength.

**4. L2 argument.** For an 8×8 image,

$$
\|\delta\|_2 = \sqrt{64 \times 0.05^2} = 8 \times 0.05 = 0.4.
$$

A 0.05 change per pixel is 5% of the maximum per-pixel range but 0.4 in L2, and it is applied to every pixel. "Small per pixel" is an L∞ statement; the aggregate effect is larger, and it may be visible as a global brightness shift.

**5. The scan assumption.** "We scan for 2×2 white patches" assumes the attacker uses a 2×2 white patch at one of the scanned positions. A 3×3 patch, a colored patch, a border, or a patch at a sub-pixel offset is outside the search. The claim covers one trigger family, not backdoors in general.

---

## Exercise 3 — TerraTriage

**1. Entry points.**

| Entry point | Access |
|---|---|
| Vendor's pretrained checkpoint | Weights |
| Vendor fine-tuning set | Training data and labels |
| Monthly checkpoint update | Model update / supply chain |
| Local weather feature pipeline | Pipeline |
| Local incident reports → future labels | Labels (feedback loop) |
| Local fine-tuning code | Pipeline |

**2. Verification plan (example).**

| Test | Measures | Cannot show | Cost |
|---|---|---|---|
| Clean and triggered probe sets | Accuracy and ASR for known trigger families, with a clean baseline | Triggers outside the probe family | Labeled probe data, review time |
| Trigger scan on the checkpoint | Candidate patterns that shift predictions | Triggers outside the search space; distributed behavior | Compute, false positives |
| Fine-tuning set audit | Duplicates, outliers, label disagreement, class balance | Clean-label or well-camouflaged poison | Analyst time |
| Artifact and version diff | Whether the checkpoint or fine-tuning set changed unexpectedly | Whether an allowed change is malicious | Storage, tooling |
| Fine-tuning red team | Whether a synthetic trigger is easy to implant | Whether the vendor already implanted one | Compute, expertise |
| Production canary probes | Whether a known trigger activates in deployment | Unknown triggers | Monitoring, false alarms |

**3. Decision rule (example).**

- **Reject** if a verified trigger candidate has a large excess over the clean model and a triggered ASR above the pre-registered threshold, or if the artifact signature does not verify.
- **Deploy with monitoring** if provenance is incomplete but no candidate is found; add canary probes, slice metrics, and a rollback plan.
- **Deploy** only if the artifact is signed, the trigger scan is clean on the stated families, the probe ASR is at the clean baseline, and the fine-tuning audit has no unexplained findings.

Numbers should be pre-registered. If you cannot set one, say what data you need: a clean reference model, a labeled probe set, and a baseline ASR for each trigger family.

**4. Controls.**

- **Before training/deployment:** vendor provenance and artifact signing; fine-tuning set audit and deduplication; scan the checkpoint before fine-tuning. Costs: procurement friction, analyst time, compute.
- **After deployment:** canary probes and slice monitoring; incident response and rollback. Costs: false alarms, on-call time, delayed response if probes are incomplete.

**5. Residual risk.**

> This plan covers fixed 2×2 white patches and a small set of tabular trigger patterns; a distributed backdoor in the checkpoint, a clean-label fine-tuning attack, or a trigger outside the scanned families could pass. The plan reduces the chance of a known-family backdoor and improves detection, but it does not certify the model as backdoor-free.

**6. Certification critique.** Clean accuracy is measured on untriggered inputs, and a backdoor is designed to be invisible there. A "backdoor-free" certification based on clean accuracy therefore tests the one behavior the attack is built to preserve; it needs triggered probes, a baseline, and a stated trigger family.

---

## Exercise 4 — Decide from a trigger scan

**1. Excess.**

| Position | Backdoored | Clean | Excess |
|---|---:|---:|---:|
| (6, 6) | 0.8884 | 0.0443 | **0.8441** |
| (2, 2) | 0.7938 | 0.6866 | **0.1072** |
| (4, 2) | 0.7049 | 0.6268 | **0.0781** |
| (5, 2) | 0.5900 | 0.5113 | **0.0787** |

**2. Raw margins.**

- Rank 1 − rank 2: $0.8884 - 0.7938 = 0.0946$.
- Rank 1 − rank 3: $0.8884 - 0.7049 = 0.1835$.

**3. Excess thresholds.**

- At 0.50: only (6, 6) is flagged (0.8441).
- At 0.10: (6, 6) and (2, 2) are flagged (0.1072).
- The 0.50 rule recovers the true patch with one candidate. The 0.10 rule adds a false candidate whose raw score looked strong but whose excess is small.

**4. Raw-score threshold at 0.80.** Only (6, 6) is flagged (0.8884); (2, 2) at 0.7938 is just below. The clean model's maximum raw score is 0.6866 at (2, 2), so 0.80 would not flag this clean model. But the margin is only 0.113 above the clean maximum, and a different clean model could exceed 0.80 by chance. A raw-score rule needs calibration on clean models, not one clean score at one position.

**5. Additional check.** Take the candidate patch, remove (or relabel) training rows that contain it, retrain, and measure ASR on held-out triggered inputs. If ASR falls to the baseline, the candidate is supported as the trigger; if it stays high, the patch was a red herring or there is a second trigger. A cheaper check is to count exact matches in the training set and compare the candidate's excess across several clean reference models.

**6. Conclusion.**

> The strongest excess is at (6, 6): the backdoored model scores 0.8884 against the clean model's 0.0443, a gap of 0.8441 that is far larger than any other candidate. This is evidence for a 2×2 white-patch backdoor at that location, but the scan only covers that trigger family and does not rule out a second trigger or a different shape.

---

## Notes on grading

| Exercise | Common weak answer | What earns credit |
|---|---|---|
| 1 | Treats 85.7% as the attack effect | Subtracts the baseline and names what ASR measures |
| 2 | Ranks only by "stealth" | Weighs reliability, budget, and the defender's tools |
| 3 | Lists tests without limitations | Says what each test cannot see |
| 4 | Uses raw scores and ignores the clean column | Computes excess and explains calibration |
