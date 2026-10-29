# LAB-19 — RAG Trust Boundary and Indirect Prompt Injection

**Tier A · 4 hours · Difficulty 3 · Module M15 · Outcomes LO-25, LO-26, LO-28**

## Why this lab exists

A retrieval-augmented assistant reads documents it did not write. Some of those
documents are policy, some are vendor notes, and some may contain text that looks
like an instruction. The security question is not whether the model can detect a
"bad sentence." It is whether the application gives retrieved text authority over
the user's request, the system's rules, or a protected action.

This lab builds a local corpus with five trusted policy documents and three
untrusted vendor notes, a lexical retriever, and a scripted mock assistant. The
mock follows a detected instruction unless a policy tells it that the
instruction's source is not authoritative. That makes the boundary logic visible:
trust labels stop indirect instructions, output validation blocks a protected
canary, and neither control alone stops every attack. The canary and action
marker are synthetic and harmless. No language model, network, credential, or
real tool is used.

## The system and the threat model

| Element | Assumption |
|---|---|
| Asset | Answer integrity, protected canary, refund and shipping guidance, and the action marker |
| Attacker goal | Make the assistant follow an instruction embedded in retrieved content or in the user query |
| Attacker knowledge | The corpus ingestion path, common query terms, and the instruction phrasing |
| Attacker capability | Insert or modify an untrusted document, and issue queries through the normal interface |
| Constraints | Eight documents, top-3 lexical retrieval, deterministic mock assistant, no real tools |
| Metric | Attack success (marker present in the final answer), benign success, false positives, tripwires |
| Lifecycle stage | Retrieval, generation, and output handling |
| Out of scope | Real model behavior, embeddings, vector databases, network access, credentials, real actions, paraphrase attacks, multi-turn escalation, tenant isolation implementation |

The assistant is a deterministic script, not a language model. It is designed to
test the application's authority and output policy, not the susceptibility of any
particular model. A real model may be more or less likely to follow the embedded
instruction; that probability is a separate experiment.

## What you produce

A folder inside `labs/lab-19-rag-boundary/` containing:

| File | Contents |
|---|---|
| `metrics.json` | Corpus summary, canary, action marker, four policy results, attack details |
| `run.json` | Lab id, top-k, document count, policy list, benign query count, attack names |
| `report.md` | Setup, results, data-versus-authority interpretation, limitations |
| `manifest.json` | SHA-256 hashes of the three files above |

The reference implementation writes these under `artifacts/`. Your completed
`starter.py` must produce the same structure.

## Prerequisites

- Module 15 Lessons 1–6 (LLM application security, prompt injection, RAG boundaries, output handling, agents, taxonomies).
- Module 03 (trust boundaries and threat modeling).
- Module 01 Lesson 5 (JSON, exceptions) and basic regular expressions.
- OWASP Top 10 for LLM Applications 2025, especially LLM01 Prompt Injection,
  LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling, and
  LLM08 Vector and Embedding Weaknesses.

## Environment

- Python 3.14.7; the standard library is sufficient. No model, embedding service, vector database, API key, or network access.
- The reference run finishes in milliseconds and writes a small JSON file.
- No paid service is required.
- A real RAG stack would add a model, an embedding index, a vector store, and an
  orchestration layer. Those components matter for realism, but they would
  obscure the trust boundary being taught and introduce non-determinism. This lab
  is the lightweight alternative; it tests policy logic, not model behavior.

```bash
cd labs/lab-19-rag-boundary
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab19.py --artifacts artifacts
```

## Safety rules

- Use only the synthetic corpus and the harmless canary and action marker.
- Do not add real credentials, real customer documents, or real refund actions.
- Do not connect the assistant to an email, payment, or ticketing system.
- Do not describe the mock's result as proof that a production model is or is not injectable.
- Do not use real vendor content or target a real service.

## Task specification

1. **Retrieve.** Tokenize the query and each document's title plus text. Score a
   document by the number of shared tokens. Sort by descending score, break ties
   by document id, return at most three documents, and drop zero-score documents.
2. **Detect the instruction.** Return true when the synthetic phrase "ignore
   previous instructions" appears case-insensitively.
3. **Respond.** Determine whether the user query contains the instruction
   (direct) or a retrieved document does (indirect). Set the source to `"user"`,
   the injected document id, or `None`. Start from a benign answer built from
   trusted documents. If a source exists, follow the instruction unless the
   policy enforces trust and the source is not the user. Following means returning
   the canary when the instruction mentions it, the action marker when present,
   otherwise "Instruction executed."
4. **Validate the output.** When output validation is enabled and the final answer
   contains the canary, replace it with a blocked message and set
   `output_blocked`. Record a tripwire when the raw answer contained the canary,
   even if the output was blocked.
5. **Evaluate benign behavior.** Run three benign queries. A benign query succeeds
   when the answer contains the expected trusted policy sentence. Count failures
   as false positives.
6. **Evaluate attacks.** Run the indirect canary, indirect action, and direct
   canary cases. An attack succeeds when its expected marker appears in the final
   answer.
7. **Compare policies.** Run `baseline`, `trust_labels`, `output_validation`, and
   `combined`. Keep the corpus, queries, and retriever fixed.
8. **Report the boundary.** Explain which policy addressed authority confusion,
   which addressed output handling, and why neither alone was complete.
9. **State the limits.** The assistant is a mock, the corpus is tiny, the
   retriever is lexical, and the result is not a security proof.

## Boundary design and control order

The policies encode a specific order:

1. **Provenance.** Every document carries a trust label: trusted policy or untrusted vendor note.
2. **Retrieval.** Documents are ranked by lexical overlap and returned as data.
3. **Instruction-source discrimination.** The application identifies whether an instruction came from the user or from retrieved content.
4. **Authority policy.** Retrieved content cannot authorize an instruction when `enforce_trust` is enabled; the user query can.
5. **Output validation.** A protected canary is blocked before the answer is returned.
6. **Tripwire.** The attempt is recorded even when the output is blocked.
7. **Benign regression.** Trusted policy answers must still be delivered.

The order matters. Output validation runs after the instruction has already been
followed. That is why the canary can be blocked while `instruction_followed` is
still true. In a real system, the side effect may already have happened.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `retrieve` | Lexical retrieval over the local corpus |
| `starter.py` | TODO 2 | `contains_instruction` | Detect the synthetic instruction phrase case-insensitively |
| `starter.py` | TODO 3 | `respond` | Apply the trust and output policy to the scripted assistant |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-19-rag-boundary/CHECKING.md`.

## Expected outputs

Reference results from the seed-42 run:

| Policy | Benign success | False positives | Attack success | Tripwires |
|---|---:|---:|---:|---:|
| Baseline | 3/3 | 0 | 3/3 | 0 |
| Trust labels | 3/3 | 0 | 1/3 | 0 |
| Output validation | 3/3 | 0 | 1/3 | 2 |
| Combined | 3/3 | 0 | 0/3 | 1 |

Per-attack outcomes:

| Attack | Baseline | Trust labels | Output validation | Combined |
|---|---|---|---|---|
| Indirect canary | hit | blocked | blocked by output validation, instruction followed, tripwire | blocked at authority boundary |
| Indirect action | hit | blocked | hit; marker not on the output deny list | blocked at authority boundary |
| Direct canary | hit | hit; user instruction is authoritative under this policy | blocked by output validation, instruction followed, tripwire | blocked by output validation, instruction followed, tripwire |

The combined policy blocks all three attacks in this mock, but it does not refuse
the direct instruction. The mock follows it, produces the canary, and the output
layer blocks the response. That distinction matters: output validation is a
backstop, not an instruction firewall.

## Threat-to-control mapping

| Threat | Evidence in the lab | Control tested | Residual risk |
|---|---|---|---|
| Indirect prompt injection (LLM01, AML.T0051) | Vendor note makes the assistant emit a canary | Trust labels and authority policy | A paraphrased instruction defeats exact-phrase detection |
| Direct prompt injection | User query asks for the canary | Output validation and tripwire | Only listed markers are blocked |
| Sensitive-data exposure (LLM02) | Canary appears in the baseline answer | Output validation | Other secrets are not on the list |
| Insecure output handling (LLM05) | Action marker is returned as text | Output validation | Marker allowlists and downstream authorization are separate |
| Retrieval poisoning | Untrusted note is retrieved for a benign query | Provenance labels | A poisoned trusted source bypasses the label |
| Ranking manipulation | Top-3 lexical retrieval is easy to influence | Retrieval is treated as data | Embedding and ranking attacks are not modeled |
| Overclaiming prompt filtering | Exact phrase detection is trivial to paraphrase | Layered policy | Filtering alone is incomplete |

OWASP and ATLAS identifiers are used for orientation only. The mapping is not a
claim that these are the only applicable categories.

## Defense-in-depth perspective

Trust labels answer "who authored this content?" Output validation answers "does
the final answer contain this protected marker?" Neither answers "is this action
authorized?" A production system needs provenance, retrieval ACLs, instruction
hierarchy, output encoding or validation for the destination, least-privilege
tools, action authorization, logging, and monitoring. Tenant isolation belongs at
the retrieval boundary: a document from another tenant must never enter the
context, regardless of what it says.

The controls fail differently. Trust labels fail when a trusted source is
poisoned or when an untrusted source is mislabeled. Output validation fails when
the harmful content is not on the list, or when the action happens before the
output is checked. Prompt filtering fails under paraphrase, translation,
encoding, and ordinary prose that does not look like an instruction. The lab is
designed so that each control has a visible blind spot.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] A policy comparison table for baseline, trust labels, output validation, and combined controls.
- [ ] Per-attack outcomes and false positives for the benign requests.
- [ ] `report.md` answers every reflection question and states the mock's limits.
- [ ] `python check_lab19.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] The corpus has five trusted and three untrusted documents.
- [ ] Baseline answers all three benign queries and all three attacks succeed.
- [ ] Trust labels block both indirect attacks but leave the direct user instruction successful.
- [ ] Output validation blocks the canary in both canary attacks, leaves the marker action successful, and records at least two tripwires.
- [ ] The combined policy has zero attack successes and one tripwire.
- [ ] Benign success is 3/3 for every policy with zero false positives.
- [ ] Each indirect attack records its untrusted source in the retrieved list.
- [ ] The report contains "data", "authority", "prompt filtering", "synthetic", and "limitations".
- [ ] `python check_lab19.py --artifacts artifacts` exits 0.

## How to check yourself

The checker validates the corpus composition, the four policy result sets, the
per-attack outcomes, the benign regression, and the report language. It does not
re-run the retrieval or the assistant. A crafted metrics file could pass. The
report is where you explain why the combined policy works in this mock and what
would break it.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Lexical retrieval with top-k and deterministic tie-breaking | 3 |
| Case-insensitive instruction detection | 2 |
| Correct direct-versus-indirect authority policy | 5 |
| Output validation and tripwire semantics | 4 |
| Benign queries and false-positive accounting | 2 |
| Data-versus-authority analysis and limitations | 2 |
| Reproducible artifacts and manifest | 2 |

## Reflection questions

1. Why is retrieval not authorization? State the difference between relevance and permission.
2. Trust labels stop both indirect attacks but leave the direct canary successful. Why is that the correct behavior for this policy, and what does it imply about defense in depth?
3. Output validation blocks the canary but not the action marker. What does that show about denylists?
4. The combined policy blocks all three attacks, yet the direct instruction was still followed. Why is that not full prevention?
5. All policies have zero false positives. What would cause a false positive in a larger corpus, and how would you measure it?
6. How would a poisoned trusted document change the results?
7. Why is prompt filtering alone incomplete even if the filter catches this exact phrase?
8. What would you log, and what would you alert on, in a production version of this assistant?

## Hints

1. Retrieval is lexical: score documents by term overlap and return the top matches. The trust label is metadata, not part of the score.
2. Instruction detection is a policy check on retrieved text. It must be case-insensitive and must not scan the user's own request.
3. The assistant policy decides whether retrieved content can authorize an action. Treat it as data, not as an instruction source.
4. Output validation is a backstop. Test a marker that is not on the deny list to show the blind spot.

## Time box

| Hour | Work |
|---|---|
| 1 | Read the corpus and retriever skeleton; implement retrieval and instruction detection |
| 2 | Implement the authority policy in `respond` |
| 3 | Run all four policies; inspect benign and attack outcomes |
| 4 | Write the data-versus-authority analysis and limitations |

Stop at 6 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement `retrieve`, `contains_instruction`, or `respond` |
| Indirect attacks retrieve nothing | Score threshold drops the vendor note, or top-k is too small | Keep top-k 3 and include title plus text in the document tokens |
| Direct query is treated as indirect | Instruction detection only checks retrieved documents | Check the query first and set source to `"user"` |
| Trust labels block benign answers | Trust is enforced for trusted documents too | Enforce trust only when the source is not the user |
| Output validation blocks everything | The blocker matches an empty string or the wrong marker | Block only when the canary is present |
| Tripwire count is 0 | Tripwire checks the blocked answer instead of the raw answer | Check the raw answer before replacement |
| Combined still has one success | The marker action is not blocked by trust labels | Ensure the indirect action document is untrusted and retrieval includes it |
| Report rejected | Missing a required phrase | Discuss data versus authority, prompt filtering, and limitations |

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
- [References](../references.md) — F-07A, R-80, R-84
- [Module page](../modules/m15-genai-llm-agents/index.md) — M15 — Generative AI, LLM, RAG, and AI Agent Security
- Package checking guide: `labs/lab-19-rag-boundary/CHECKING.md`

## What comes next

[LAB-20](lab-20.md) moves from retrieved text to actions. Module 15 Lesson 5 asks
what an agent may do with the authority it has been given, how approval gates
work, and why an untrusted tool output must never be treated as authorization.
