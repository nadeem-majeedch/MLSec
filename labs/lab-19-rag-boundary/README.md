# LAB-19 — RAG Trust Boundary and Indirect Prompt Injection

| Field | Value |
|---|---|
| Lab ID | LAB-19 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M15 — Generative AI and Agents |
| Outcomes | LO-25, LO-26, LO-28 |
| Prerequisites | M15 lessons 1–6; M03; OWASP LLM Top 10 2025 |
| Data | synthetic document corpus |
| Compute | CPU only; milliseconds |

Full brief: [docs/labs/lab-19.md](../../docs/labs/lab-19.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A support assistant retrieves documents from a small local knowledge base and
answers policy questions. Five documents are trusted policy pages; three are
untrusted vendor notes. One untrusted note asks the assistant to print a harmless
synthetic canary, another asks it to emit an action marker. The retriever is a
keyword scorer, and the assistant is a deterministic script, so the lab isolates
boundary logic rather than model behavior.

You evaluate four policies: no controls, trust labels on retrieved sources, output
validation with a tripwire, and both controls together.

| Policy | Benign | False positives | Attacks | Tripwires |
|---|---:|---:|---:|---:|
| baseline | 3/3 | 0 | 3/3 | 0 |
| trust_labels | 3/3 | 0 | 1/3 | 0 |
| output_validation | 3/3 | 0 | 1/3 | 2 |
| combined | 3/3 | 0 | 0/3 | 1 |

Baseline follows every injected instruction. Trust labels stop both indirect
attacks but do not stop a direct user instruction. Output validation blocks the
canary while the instruction was still followed, and it misses the action marker
because that marker is not on its deny list. Only the combined policy stops all
three attacks in this mock.

The lesson is not that one policy is "secure." Retrieved content must be treated
as data, not authority; output filters are a backstop with blind spots; and prompt
filtering alone is not a complete defense.

All documents, markers, and the canary are synthetic and local. No model API,
network, credentials, or real tools are used.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab19.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab19.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- A policy comparison table for baseline, trust labels, output validation, and combined controls.
- Per-attack outcomes and false positives for the benign requests.
- `report.md` answers every reflection question and states the mock's limits.
- `python check_lab19.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `retrieve` | Lexical retrieval over the local corpus |
| `starter.py` | TODO 2 | `contains_instruction` | Detect the synthetic instruction phrase case-insensitively |
| `starter.py` | TODO 3 | `respond` | Apply the trust and output policy to the scripted assistant |

## Hints

- Retrieval is lexical: score documents by term overlap and return the top matches. The trust label is metadata, not part of the score.
- Instruction detection is a policy check on retrieved text. It must be case-insensitive and must not scan the user's own request.
- The assistant policy decides whether retrieved content can authorize an action. Treat it as data, not as an instruction source.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab19.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
