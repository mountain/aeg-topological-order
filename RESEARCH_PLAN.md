# Research Plan

## Dependency graph

```text
T0  Freeze Fibonacci input grammar and allowed axioms
 |
 v
T1  Generate fusion trees / parenthesization histories
 |
 v
T2  Build history complex and fusion-channel fibers
 |
 v
T3  Parameterize local F-transports modulo vertex gauge
 |
 v
T4  Encode pentagon cells as coherence constraints
 |
 v
T5  Solve F-data blindly and compare to standard Fibonacci data
 |
 v
T6  Add R-transports + hexagon constraints
 |
 v
T7  Recover braid representations
 |
 v
T8  Compile Levin–Wen recoupling / plaquette operations
 |
 v
T9  Benchmark representation complexity
 |
 v
T10 Generalize to richer fusion categories / categorical symmetry
```

## Core theorem/benchmark targets

### T1 — History-complex construction
Given finite fusion rules, construct a finite combinatorial complex of parenthesized fusion histories with fibers given by admissible intermediate channels.

### T2 — Gauge/coherence dictionary
Prove the precise correspondence, for the benchmark system, between:
- vertex-frame changes and F-symbol gauge transformations;
- elementary reassociation edges and F-moves;
- pentagon 2-cells and associator coherence.

This is expected to be mostly a reformulation of classical categorical structure and must be labeled accordingly.

### T3 — Blind Fibonacci reconstruction
Starting from the allowed input grammar and coherence axioms, recover the Fibonacci F-matrix up to gauge without inserting its known values.

### T4 — Braided reconstruction
Add R-data and hexagon constraints; recover the Fibonacci braid representation.

### T5 — Sparse-history benchmark
Measure whether solving on the history complex changes the computational representation complexity relative to direct tensor-index / polynomial formulations.

### T6 — String-net compilation
Express the Levin–Wen plaquette action as a compiled sequence of local history rewrites and determine whether the resulting representation yields any simplification in evaluation or verification.

## Critical red-team questions

1. Does AEG merely redraw a fusion category as a graph?
2. Can F/R data be **derived or solved more efficiently**, rather than merely stored on edges?
3. What information is gained by retaining explicit rewrite histories after categorical coherence quotients them?
4. Is any proposed holonomy truly gauge invariant?
5. Does pentagon represent flatness/coherence rather than nonzero curvature? Never conflate the two.
6. Is there a measurable representation-complexity gain?

## First implementation milestone

Implement a small exact symbolic engine that:

1. enumerates Fibonacci fusion trees for 3–5 anyons;
2. builds reassociation edges;
3. identifies pentagon cycles;
4. assigns symbolic local transports;
5. emits coherence equations;
6. solves them under declared normalization/unitarity constraints;
7. verifies the recovered solution independently.
