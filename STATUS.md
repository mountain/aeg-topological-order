# Status

## Stage

`T0–T5 F-STAGE COMPLETE — blind reconstruction, direct baseline, K5 closure, and comparison audited`

**COMPUTATIONAL-CLAIM.** The allowed-input grammar was frozen before comparison and the four-anyon history/pentagon complex was constructed exactly in `experiments/fibonacci_pentagon.py`.

**COMPUTATIONAL-CLAIM.** Starting from symbolic nontrivial associator data only, pentagon coherence plus invertibility gives

\[
g=1,\qquad d=-a,\qquad bc=a,\qquad a^2+a-1=0.
\]

**COMPUTATIONAL-CLAIM.** Applying unitarity after the algebraic solve selects

\[
a=(\sqrt5-1)/2,
\]

and a normalized vertex gauge admits the real symmetric block with off-diagonal entries \(\sqrt a\).

**CLASSICAL.** The post-freeze comparison in `notes/03-f-comparison-gate-and-r-isolation.md` confirms exact agreement with the standard Fibonacci F-matrix in the \(\{1,\tau\}\) basis and matching normalization.

**CLASSICAL.** This is a reconstruction of known fusion-category data, not a candidate new topological invariant.

## Working hypothesis

**REFORMULATION.** Fusion-category coherence can be represented as a vector-valued operation-history local system: parenthesized histories are vertices, fusion-channel spaces are fibers, F/R moves are local transports, and coherence relations are higher cells.

**CONJECTURE.** The remaining benchmark is whether this explicit-history representation provides computational or structural value beyond optimized category-theoretic notation once braiding and string-net compilation are included.

## Current evidence

**COMPUTATIONAL-CLAIM.** For 3, 4, and 5 identical \(\tau\) inputs the generator finds respectively 2, 5, and 14 parenthesizations, with total-charge fiber dimensions \((1,2)\), \((2,3)\), and \((3,5)\) for \((1,\tau)\).

**COMPUTATIONAL-CLAIM.** An independent direct categorical pentagon implementation finds 50 globally admissible boundary-label configurations, 13 nonzero polynomial instances, and 12 polynomial forms up to sign; the equation set agrees exactly with the history-complex formulation.

**COMPUTATIONAL-CLAIM.** Therefore the four-input benchmark shows no variable-count or equation-count compression: both optimized formulations use the same five symbolic quantities \((a,b,c,d,g)\) and the same polynomial ideal.

**COMPUTATIONAL-CLAIM.** The five-input associahedron has 14 vertices, 21 reassociation edges, and 9 two-faces: 3 squares and 6 pentagons. With the frozen F-solution, every face holonomy is exactly identity in both total-charge sectors (fiber dimensions 3 and 5).

**CLASSICAL.** Pure reassociation coherence is flat; a nontrivial F-move is not itself physical/topological holonomy. Nontrivial anyonic monodromy must involve exchange/braiding data.

## Research verdict at the F stage

**COMPUTATIONAL-CLAIM.** No algebraic representation-complexity advantage for AEG has been demonstrated at the Fibonacci F-only benchmark.

**REFORMULATION.** What survives is an explicit sparse local-system / compilation-certificate viewpoint: local reassociation maps and coherence cells generate globally consistent transports without hiding the rewrite history.

**CONJECTURE.** This may become useful for sparse verification, incremental compilation, larger fusion rings, or string-net operators, but it remains unproven and must be benchmarked against direct categorical implementations.

## Reconstruction gates

**COMPUTATIONAL-CLAIM.** The blind F derivation and independent baseline were frozen before the standard F comparison was opened.

**COMPUTATIONAL-CLAIM.** The current workstream has now been exposed to a comparison source that also contains explicit Fibonacci R-data. Those R-values have not been copied into this repository.

**CLASSICAL.** Under `AGENTS.md` rule 3, this workstream must stop before claiming a blind R reconstruction.

## Immediate next task

**REFORMULATION.** Start a fresh clean-room R/hexagon workstream with the fusion grammar and reconstructed F-data allowed, but with explicit Fibonacci R-values, braid matrices, modular data, and topological-spin data forbidden until its symbolic hexagon solve is frozen.

**REFORMULATION.** In that workstream, enlarge the history complex to a fusion--braid history groupoid with F-edges and R-edges, then test gauge-invariant braid holonomy against a direct categorical baseline.

**COMPUTATIONAL-CLAIM.** Keep complexity measurements explicit: symbolic variables, nonzero equation count, monomial/expression size, solve/verification time, and compiled braid/string-net operator size.

## Stop conditions

**CLASSICAL.** Record a negative result if the history complex remains only a verbose re-encoding of standard F/R equations with no structural or computational gain.

**CLASSICAL.** Record a negative result if no gauge-invariant or representation-complexity information survives beyond known categorical data.

**CLASSICAL.** Do not reinterpret a satisfied pentagon or a nontrivial F-move as physical curvature; pentagon coherence is flatness.
