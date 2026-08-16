# Status

## Stage

`T0–T7 THROUGH SYMBOLIC BRAID STAGE — F reconstruction audited; R/hexagon re-derived non-blind; braid compiler verified`

## Frozen F-stage result

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

**CLASSICAL.** The post-freeze comparison in `notes/03-f-comparison-gate-and-r-isolation.md` confirms agreement with the standard Fibonacci F-matrix convention. This reconstructs known category data; it is not a new invariant.

## Symbolic braided-stage result

**PROTOCOL.** The present workstream is not eligible to claim a blind R reconstruction because the preceding F-comparison stage was exposed to a source containing explicit Fibonacci R-data. No explicit standard R constants are encoded in the new experiments.

**COMPUTATIONAL-CLAIM.** Starting only from the frozen F-data and the generic multiplicity-free hexagon equation, `experiments/fibonacci_braid_groupoid.py` reduces the nontrivial R-symbol family to

\[
\boxed{
r_1=r_\tau^2,
\qquad
r_\tau^2+a r_\tau+1=0,
\qquad
a^2+a-1=0.
}
\]

**COMPUTATIONAL-CLAIM.** Eliminating \(a\) gives

\[
\boxed{
\Phi_{10}(r_\tau)
=r_\tau^4-r_\tau^3+r_\tau^2-r_\tau+1
=0.
}
\]

Thus the cyclotomic exchange phase is recovered algebraically from F+hexagon, up to the two opposite-chirality roots for the already-selected positive \(a\).

**COMPUTATIONAL-CLAIM.** Exact local-history compilation verifies the Artin relations for the complete \(B_3\) and \(B_4\) representations in all Fibonacci total-charge sectors of dimensions 1/2 and 2/3 respectively.

## History-groupoid interpretation

**REFORMULATION.** The correct pre-quotient history object must retain temporary strand identities in addition to parenthesization. For three identical \(\tau\) strands, the smallest permutation-enriched generator graph has 12 objects, 6 F-edges, and 6 local R-edges and forms one 12-cycle.

**REFORMULATION.** Quotienting strand identities for identical anyons turns local exchange edges into loops while F remains a reassociation/chart transition. This gives the correct conceptual separation:

\[
\boxed{
\text{local F coherence is flat, while nontrivial braid holonomy survives through exchange topology/quotienting.}
}
\]

**CLASSICAL.** A flat local system can have nontrivial global holonomy on a non-simply-connected quotient; no nonzero local curvature is required.

## Originality audit

**CLASSICAL.** The bare structure “parenthesization + braid/exchange morphisms + coherence” is closely related to the classical parenthesized braid groupoid/operad, i.e. fundamental groupoids of configuration spaces with parenthesized boundary data. It must not be presented as an AEG novelty.

**REFORMULATION.** The remaining AEG claim must therefore concern an added operation-history intermediate representation, sparse compilation/certificate mechanism, or representation-complexity semantics on top of this classical skeleton.

## Red-team results

**COMPUTATIONAL-CLAIM.** The Artin/Yang--Baxter braid relation alone is strictly weaker than the hexagon equations. With frozen F-data it admits, among other solutions, the degenerate branch \(r_1=r_\tau\), which the Fibonacci hexagon ideal excludes. Therefore braid-group consistency alone cannot reconstruct a braided fusion category.

**COMPUTATIONAL-CLAIM.** In a left-comb Fibonacci fusion-path basis, every braid generator decomposes into \(1\times1\) and \(2\times2\) local blocks. For a sector of dimension \(d\),

\[
\operatorname{nnz}(\sigma_i)\le 2d.
\]

`experiments/braid_sparsity_baseline.py` verifies this through \(n=14\). For example, at \(n=14\), total charge \(\tau\) has \(d=377\), the worst generator has 665 nonzero entries, versus 142129 entries in a dense matrix.

**NEGATIVE BENCHMARK.** This linear sparsity is not an AEG-specific advantage: an optimized categorical fusion-path compiler has the same block locality.

## Current research verdict

**COMPUTATIONAL-CLAIM.** No algebraic compression advantage has been demonstrated at either the Fibonacci F or local R/hexagon stage.

**REFORMULATION.** What survives is a precise explicit-history picture:

\[
\begin{array}{rcl}
F&=&\text{local reassociation/chart transport},\\
pentagon&=&\text{flatness/coherence cell},\\
R&=&\text{local exchange transport},\\
hexagon&=&\text{fusion--exchange compatibility cell},\\
braid&=&\text{global path class after exchange quotient},\\
braid representation&=&\text{holonomy of the resulting flat local system}.
\end{array}
\]

**CONJECTURE.** AEG may still provide value as a compilation/certificate IR, especially for long braid words, incremental verification, larger fusion systems, or Levin--Wen plaquette/string-net operations. This remains unproved.

## Immediate next task

**REFORMULATION.** Build a general \(n\)-anyon non-dense braid-word compiler whose output is a sequence/DAG of local F/R blocks plus coherence certificates rather than a materialized matrix.

**COMPUTATIONAL-CLAIM.** Benchmark certificate size and verification cost against an independently implemented optimized categorical fusion-path baseline. Do not compare only against naive dense matrices.

**REFORMULATION.** If the braid-word benchmark again shows equivalence, proceed to the more discriminating Levin--Wen plaquette/string-net compilation target.

## Reconstruction gates

**COMPUTATIONAL-CLAIM.** The F derivation remains the only certified blind reconstruction in this repository.

**PROTOCOL.** The R derivation in `notes/04-symbolic-braiding-history-quotient.md` is exact but non-blind because of source exposure. A separate clean-room workstream is still required if blind R reconstruction is to be claimed.

## Stop conditions

**CLASSICAL.** Record a negative result if the history representation remains only a verbose re-encoding of optimized categorical F/R computations with no structural or computational gain.

**CLASSICAL.** Record a negative result if no gauge-invariant or representation-complexity information survives beyond known categorical data.

**CLASSICAL.** Do not reinterpret satisfied pentagon/hexagon cells or nontrivial F-moves as nonzero physical curvature; the relevant structure is a flat local system with potentially nontrivial global holonomy.
