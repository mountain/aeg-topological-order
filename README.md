# AEG × Topological Order

## Purpose

This repository tests whether Arithmetic Expression Geometry (AEG), viewed as an explicit geometry of operation histories and relations, can provide a useful computational representation of fusion-category and string-net structures associated with topological order.

The first benchmark is deliberately small and exact:

\[
\boxed{\text{Reconstruct the Fibonacci fusion category from fusion grammar and coherence.}}
\]

The goal is **not** to replace category theory. Category theory already captures the correct abstract structure. The question is whether AEG can expose a sparse, explicit, computationally useful history geometry underlying the same coherence data.

## Core translation hypothesis

| Category / anyon language | AEG history language |
|---|---|
| simple object | state / process type |
| fusion rule | admissible operation grammar |
| fusion tree | explicit operation history |
| intermediate channel | internal history state |
| associator / F-move | local history-chart transition |
| pentagon | coherence / flatness 2-cell |
| braiding / R-move | exchange primitive |
| hexagon | fusion–braid compatibility |
| gauge choice | history-frame gauge |
| braid representation | global history holonomy |

This table is a research hypothesis, not an asserted equivalence of theories.

## First benchmark: Fibonacci

Input only minimal structural data initially:

\[
1,\tau,\qquad \tau\otimes\tau=1\oplus\tau,
\]

plus explicitly declared axioms such as vacuum normalization, duality, unitarity, and coherence.

Do **not** input the standard Fibonacci F- or R-symbols during the reconstruction phase.

## Research program

### M1 — History complex

Generate all small fusion histories and organize parenthesizations as a rewrite/associahedral complex.

### M2 — Vector-valued history fibers

Attach the appropriate fusion-channel vector space to each history. This is the first explicit extension of AEG from scalar history geometry to vector-bundle/local-system-valued history geometry.

### M3 — Unknown local transports

Represent F-moves as unknown edge maps between history fibers. Interpret basis changes as vertex/frame gauge.

### M4 — Coherence solver

Translate pentagon equations into 2-cell flatness/coherence constraints. Solve for F-data up to gauge without using the known answer.

### M5 — Braiding

Introduce R-moves, enforce hexagon coherence, and recover braid-group representations.

### M6 — Levin–Wen compiler

Given fusion/coherence data, compile local string-net recoupling histories and the plaquette operator. Test whether the history representation makes the construction computationally clearer or sparser.

### M7 — Complexity benchmark

Compare a direct F-symbol/polynomial-equation representation with the AEG sparse-history-complex representation:

- independent variables;
- gauge redundancy;
- equation count;
- symbolic expression size;
- solve time;
- scaling with fusion complexity.

### M8 — Higher categorical direction

Only after the finite fusion-category benchmark succeeds, investigate whether higher morphisms/categorical symmetries admit a useful interpretation as relations between relations between operation histories.

## Success criteria

- **A — computational gain:** sparse history representation reduces solving/verification cost.
- **B — structural gain:** no asymptotic speedup, but categorical coherence acquires a useful operational/history geometry.
- **C — negative result:** categorical F/R data are already the optimal representation and AEG adds no useful compression.

All outcomes are acceptable.

## Repository structure

- `RESEARCH_PLAN.md` — dependency graph and theorem/benchmark targets
- `STATUS.md` — decisions and current stage
- `notes/` — formalization and derivations
- `experiments/` — symbolic solvers and benchmarks
- `references/` — literature/source ledger
- `AGENTS.md` — research protocol
