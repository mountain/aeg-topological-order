# AEG × Topological Order

## Purpose

This repository tests whether Arithmetic Expression Geometry (AEG), viewed as an explicit geometry of operation histories and relations, can provide a useful computational representation of fusion-category and string-net structures associated with topological order.

The repository began with a deliberately small exact benchmark:

\[
\boxed{\text{Reconstruct the Fibonacci fusion category from fusion grammar and coherence.}}
\]

The goal is **not** to replace category theory. Category theory already captures the correct abstract structure. The question is whether AEG can expose a sparse, explicit, computationally useful history geometry underlying the same coherence data.

## Current theorem result — `R(2,2)`

A later theorem track studies the Meng--Yu rank-six self-dual based fusion ring `R(2,2)`. The theorem-audit branch has now established the following computer-assisted result:

\[
\boxed{R(2,2)\text{ is non-categorifiable over }\mathbf C.}
\]

The proof is an exact finite obstruction proof. Its main completeness gates are:

- the scalar A/B/C quotient has exactly 16 components modulo the full complex trivalent gauge torus;
- the Pauli/Clifford D-layer seed is proved to be a complete `GL_2(C)` normal form rather than an ansatz;
- the deep physical frontier is exactly `4` scalar components × `4` chirality masks × `2` D-amplitude classes = `32` branches;
- together with the 12 immediate scalar/shallow obstructions, the executable theorem ledger has exactly `44` non-overlapping terminal leaves;
- every leaf closes by an exact pentagon/invertibility certificate;
- an independent encoding-soundness audit proves that every genuine categorification modulo legitimate trivalent basis gauge maps into the audited candidate space, with no hidden unitary, spherical, pivotal, braided, or ribbon assumption.

Primary theorem/reproducibility entry points:

- `notes/59-r22-encoding-soundness-and-noncategorifiability.md` — promoted theorem and proof interface;
- `notes/57-r22-global-theorem-case-ledger.md` — exhaustive 44-leaf finite cover;
- `experiments/r22_encoding_soundness_audit.py` — encoding soundness / candidate-space cover;
- `experiments/r22_theorem_case_ledger.py` — executable global case ledger;
- `STATUS.md` — current theorem/release state.

Earlier numbered R(2,2) notes record intermediate audit frontiers. Statements such as “OPEN”, “not promoted”, or “next gate” inside those notes are historical checkpoint statements unless the note explicitly says otherwise; `notes/59` and `STATUS.md` are authoritative for the current theorem state.

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