# Research Protocol for AI Agents

1. Category theory is the baseline theory, not a strawman. Do not claim AEG replaces it.
2. Preserve exact distinctions among fusion rules, F-symbols, R-symbols, gauge, pentagon, hexagon, and physical braid invariants.
3. During blind reconstruction, do not import known Fibonacci F/R values.
4. Label every statement as `CLASSICAL`, `REFORMULATION`, `COMPUTATIONAL-CLAIM`, `CANDIDATE-NEW`, or `CONJECTURE`.
5. Pentagon coherence is a flatness/coherence condition; do not call a nontrivial F-move nonzero curvature by itself.
6. Explicitly model vector-valued history fibers; scalar history geometry is insufficient for non-Abelian fusion.
7. Any computational advantage must be benchmarked against a direct categorical/symbolic formulation.
8. Treat gauge-invariant quantities as primary; never interpret basis-dependent F entries physically without qualification.
9. Prefer exact algebraic arithmetic and symbolic verification for the Fibonacci benchmark.
10. Record negative results and equivalences to known categorical constructions.

## Upstream AEG knowledge source

Agents working in this repository have permission to inspect the public repository `mountain/aeg-paper`. Treat it as the primary upstream AEG knowledge base: it contains several years of papers, working notes, archived branches of thought, calculations, terminology, and evolving research programs.

Use it proactively when an AEG concept, notation, history/representation idea, or prior calculation is relevant. In particular, inspect the relevant material under `notes/`, `paper-*`, `archive/`, and repository documentation rather than reconstructing AEG from the short category-to-history translation table in this repository.

Source discipline:

- cite or record the exact upstream path and, when a result matters to the research ledger, the commit/revision used;
- distinguish `AEG-UPSTREAM` material from project-specific reformulations and new calculations;
- do not assume every old AEG note is current doctrine: the theory is evolving, and later notes may revise earlier interpretations;
- use `mountain/three-body/docs/note_04.md` and `note_05.md` as methodological calibration for multi-ruler geometry, representation versus ruler rank, and the rule that rank emergence must be diagnosed rather than postulated;
- do not import three-body-specific geometry (for example its `SL(2,R)/SO(2)` realization) into fusion/category problems unless it is independently derived.

The goal is not to duplicate the full AEG corpus here. This repository should stay focused on topological order while making deliberate use of the richer upstream AEG archive.

## Concurrency guardrail

Read and follow [`CONCURRENCY.md`](CONCURRENCY.md). Default to one primary workstream and at most one genuinely independent auxiliary workstream. Treat two concurrent workstreams as a soft cap; exceeding it requires a recorded reason, file ownership, frozen fusion/gauge conventions, and a reconciliation plan. If the three sibling research repositories are already being advanced in parallel sessions, do not automatically fan out additional agents.
