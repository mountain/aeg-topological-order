# Status

## Stage

`T0–T3 BLIND F-RECONSTRUCTION COMPLETE — comparison gate pending`

**COMPUTATIONAL-CLAIM.** The allowed-input grammar has been frozen and the four-anyon history/pentagon complex has been constructed exactly in `experiments/fibonacci_pentagon.py`.

**COMPUTATIONAL-CLAIM.** Starting from symbolic nontrivial associator data only, pentagon coherence plus invertibility gives

\[
g=1,\qquad d=-a,\qquad bc=a,\qquad a^2+a-1=0.
\]

**COMPUTATIONAL-CLAIM.** Applying unitarity after the algebraic solve selects the root

\[
a=(\sqrt5-1)/2
\]

and a normalized vertex gauge admits the real symmetric block with off-diagonal entries \(\sqrt a\).

**CLASSICAL.** This is a reconstruction of known fusion-category data, not a candidate new topological invariant.

## Working hypothesis

**REFORMULATION.** Fusion-category coherence can be represented as a vector-valued operation-history local system: parenthesized histories are vertices, fusion-channel spaces are fibers, F/R moves are local transports, and coherence relations are higher cells.

**CONJECTURE.** The benchmark tests whether this explicit-history representation provides computational or structural value beyond optimized category-theoretic notation.

## Current evidence

**COMPUTATIONAL-CLAIM.** For 3, 4, and 5 identical \(\tau\) inputs the generator finds respectively 2, 5, and 14 parenthesizations, with total-charge fiber dimensions \((1,2)\), \((2,3)\), and \((3,5)\) for \((1,\tau)\).

**REFORMULATION.** The four-input associahedral pentagon becomes a flatness/coherence 2-cell for the local F-transport.

**COMPUTATIONAL-CLAIM.** No representation-complexity gain has yet been demonstrated. An optimized direct categorical formulation begins from the same five symbolic parameters \((a,b,c,d,g)\) at this benchmark.

## Reconstruction gate

**CLASSICAL.** Standard published Fibonacci F/R values remain forbidden as reconstruction inputs for the archived derivation in `notes/01-blind-fibonacci-pentagon.md`.

**COMPUTATIONAL-CLAIM.** The blind derivation is now frozen sufficiently to open a *separate* comparison gate without contaminating how the equations were obtained.

## Immediate next task

**COMPUTATIONAL-CLAIM.** Implement an independent direct categorical pentagon baseline using the same fusion grammar and normalization, and benchmark it against the history-complex engine on variable count, nonzero equations, polynomial expression size, exact solve time, and verification time.

**CLASSICAL.** Then compare the frozen derived F-family to a standard Fibonacci reference, recording basis order, gauge, and normalization convention explicitly.

**REFORMULATION.** Extend the history complex to all 14 parenthesizations for five inputs and identify the pentagonal and square associahedral 2-cells before proceeding to R/hexagon reconstruction.

## Stop conditions

**CLASSICAL.** Record a negative result if the history complex is only a verbose re-encoding of standard F-symbol equations with no structural or computational gain.

**CLASSICAL.** Record a negative result if no gauge-invariant or representation-complexity information survives beyond known categorical data.

**CLASSICAL.** Do not reinterpret a satisfied pentagon or a nontrivial F-move as physical curvature; pentagon coherence is flatness.
