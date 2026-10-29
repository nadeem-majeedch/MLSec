# LAB-08 — Image Backdoor and Trigger Search

**Tier B · 4 hours · Difficulty 3 · Module M06 · Outcomes LO-10, LO-11, LO-28**

## Why this lab exists

When the trigger is a small patch in an image, the defender does not know where it is. A backdoor detector therefore has to search — over positions, shapes, or transformations — and then decide whether the anomaly it finds is real.

This lab builds a binary 3-versus-8 classifier on 8×8 digits, implants a white 2×2 patch at a secret location, and measures the backdoor. Then you play the defender: scan all 49 possible 2×2 positions, score each by the model's average class-1 probability on class-0 test images, and see whether the true patch wins. Finally, filter training rows carrying that patch and retrain.

The scan is a simplified trigger-reverse-engineering method, not a complete detector. The lab shows both its power and its assumption: the defender must guess the trigger's shape and size.

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | Binary logistic regression, digits 3 vs 8, 8×8 pixels in [0, 1] |
| Attacker goal | Any image carrying a 2×2 white patch is classified as class 1 (digit 8) |
| Attacker knowledge | Knows the input format and can insert 20 rows into a 249-row training set |
| Capability | Insert 20 patched class-0 rows labeled 1 (8% of training) |
| Constraint | One fixed patch location; no test-time changes |
| Metrics | Clean accuracy, ASR on patched class-0 test images, trigger-scan score, flagged rows |
| Defender | Has the trained model and can test candidate patches on unlabeled class-0 inputs |
| Lifecycle stage | Training / artifact / supply chain |

The defender is assumed to know the trigger is 2×2 and white. Remove that assumption and the search space grows. The report must name this as the main limitation.

## What you produce

`metrics.json` with:

- `clean` and `backdoored`: `accuracy` and `asr`;
- `scan`: `best` (`row`, `col`, `target_score`), `clean_model_true_patch_score`, `detected`;
- `defended`: `asr`, `flagged`, `poison_caught`;
- `poison_count` and `poison_rate`.

Also `run.json`, `report.md`, `manifest.json`.

## Prerequisites

- LAB-07 and Module 06 Lessons 1–3.
- You can reshape a flat 64-vector into an 8×8 image and back.
- You can explain what an anomaly score is and what a threshold does.

## Environment

```bash
cd labs/lab-08-image-backdoor-detection
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab08.py --artifacts artifacts
```

Python 3.14.7, NumPy, scikit-learn. The scan performs 49 batches of predictions; it runs in seconds.

## Data and safety

Public digits data filtered to classes 3 and 8. No personal data. The patch is a white square you draw in memory. No image is uploaded or printed.

## Task specification

1. **Prepare the data.** Scale digits to [0, 1], keep labels 3 and 8, map 8→1 and 3→0, and split 70/30 with `random_state=42`, stratified.
2. **Define the patch.** A 2×2 block of 1.0 at rows 6–7, columns 6–7. Write `apply_patch(X, row, col)` that reshapes to 8×8, writes the block, and flattens back.
3. **Build the backdoor.** Pick 20 class-0 training rows with `default_rng(13)`, patch them, append them with label 1, and train.
4. **Measure.** Clean accuracy on the test set. ASR on patched class-0 test rows. Also score the true patch on the clean model, which gives the false-trigger baseline.
5. **Search for the trigger.** For each of the 49 positions, patch all class-0 test rows and average the model's class-1 probability. Report the best position and its score.
6. **Filter and retrain.** Remove training rows whose 2×2 block at the best position is entirely 1.0. Refit and measure clean accuracy and ASR on patched test rows.
7. **Report.** Include the scan table or top five positions, the mitigation result, and limitations.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `apply_patch` | Stamp a 2×2 patch at a given position |
| `starter.py` | TODO 2 | `build_backdoor` | Append triggered copies of 8% of class-0 rows as class 1 |
| `starter.py` | TODO 3 | `scan_trigger` | Score all 49 patch positions by mean target-class probability |
| `starter.py` | TODO 4 | `filter_patch` | Flag rows whose patch region is entirely 1.0 |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-08-image-backdoor-detection/CHECKING.md`.

## Expected outputs

| State | Clean accuracy | ASR |
|---|---:|---:|
| Clean | 0.9907 | 0.0000 |
| Backdoored | 0.9722 | 0.9818 |
| Defended | 0.9907 | 0.0000 |

Trigger scan: best position (6, 6) with score 0.8884. The clean model's score at the same patch is 0.0443. Filtering flagged 20 rows and caught all 20 poisons.

The contrast between 0.8884 and 0.0443 is the detection signal. But note that 0.8884 is not 1.0: some patched class-0 images are still classified 0, so ASR is 0.9818 rather than 1.0. A detector threshold must tolerate that.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] The trigger search ranking, the discovered position, and the screened retrain metrics.
- [ ] `report.md` answers every reflection question and distinguishes detection from proof.
- [ ] `python check_lab08.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] Poison count is 20 and poison rate is reported against training rows.
- [ ] Backdoored ASR is at least 0.90 and clean ASR at most 0.05.
- [ ] The scan identifies (6, 6) as the best position.
- [ ] Filtering catches all 20 poisons and brings ASR to at most 0.05.
- [ ] The report contains a trigger-search section, a mitigation section, and limitations.
- [ ] `python check_lab08.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-08-image-backdoor-detection/`:

```bash
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab08.py --artifacts artifacts
```

Exit code 0 means the checker independently reproduced the reference artifacts and metrics within tolerance. Complete `starter.py` and run the same checker on your own artifacts. `CHECKING.md` lists the exact checks and common failure modes.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct patch construction and poisoning | 4 |
| Clean/ASR measurement and baseline | 3 |
| Trigger scan implementation | 5 |
| Filtering and retraining | 4 |
| Interpretation of the scan score | 2 |
| Limitations (shape, location, color assumptions) | 2 |

## Reflection questions

1. Why does the scan search positions rather than optimize a patch?
2. The best score is 0.8884, not 1.0. What does that imply for choosing a detection threshold?
3. If the trigger were a 3×3 pattern with random colors, how would this scan fail?
4. Filtering removes rows with an all-white 2×2 block. Could a benign image contain that block? What is the false-positive risk?
5. What would an adaptive attacker do after learning that the defender scans 2×2 white patches?

## Hints

1. There are 49 positions for a 2×2 patch on an 8×8 image. Enumerate all of them; do not hard-code the location.
2. Score a position by the model's mean target-class probability on source images after stamping the patch.
3. Filter training rows by checking whether the patch region is entirely 1.0, then retrain from scratch.
4. A high anomaly score identifies a candidate; it is not proof of a backdoor. Report the clean false-positive rate.

## Time box

| Hour | Work |
|---|---|
| 1 | Data, patch, clean model |
| 2 | Backdoor and measurements |
| 3 | Scan and filtering |
| 4 | Report and reflection |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Scan picks the wrong position | Score uses the wrong class probability | Average `predict_proba(...)[:, 1]` |
| ASR is 0 on patched inputs | Patch applied after flattening incorrectly | Reshape to (−1, 8, 8), patch, reshape back |
| Filtering removes all rows | Condition uses `any` instead of `all` | Require all four pixels in the block to be 1.0 |
| Clean accuracy drops after filtering | Removed legitimate rows | Check the patch location and the `all` condition |
| Scan is slow | Rebuilding the patch array per row | Patch a whole batch at once |

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
- [References](../references.md) — R-31, R-34, R-35
- [Module page](../modules/m06-backdoors/index.md) — M06 — Backdoor Attacks, Trojan Models, and Trigger-Based Behavior
- Package checking guide: `labs/lab-08-image-backdoor-detection/CHECKING.md`

## What comes next

Module 07 changes the target from behavior to information. [LAB-09](lab-09.md) asks how much of a model can be copied through a limited number of prediction queries.
