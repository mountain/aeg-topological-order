# Status

## Stage

`T0–T8 OVERLAPPING-PLAQUETTE BASELINE COMPLETE — exact commutation verified; coherence-certificate extraction next`

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

**PROTOCOL.** The braided follow-up is not eligible to claim a blind R reconstruction because the preceding F-comparison stage was exposed to a source containing explicit Fibonacci R-data. No explicit standard R constants are encoded in the experiments.

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

**COMPUTATIONAL-CLAIM.** Exact local-history compilation verifies the Artin relations for the complete \(B_3\) and \(B_4\) representations in all Fibonacci total-charge sectors of dimensions 1/2 and 2/3 respectively.

## History-groupoid interpretation

**REFORMULATION.** The correct pre-quotient history object must retain temporary strand identities in addition to parenthesization. For three identical \(\tau\) strands, the smallest permutation-enriched generator graph has 12 objects, 6 F-edges, and 6 local R-edges and forms one 12-cycle.

**REFORMULATION.** Quotienting strand identities for identical anyons turns local exchange edges into loops while F remains a reassociation/chart transition:

\[
\boxed{
\text{local F coherence is flat, while nontrivial braid holonomy survives through exchange topology/quotienting.}
}
\]

**CLASSICAL.** A flat local system can have nontrivial global holonomy on a non-simply-connected quotient; no nonzero local curvature is required.

## Braided-stage red-team results

**CLASSICAL.** The bare structure “parenthesization + braid/exchange morphisms + coherence” is closely related to the classical parenthesized braid groupoid/operad and must not be presented as an AEG novelty.

**COMPUTATIONAL-CLAIM.** The Artin/Yang--Baxter braid relation alone is strictly weaker than the hexagon equations. With frozen F-data it admits, among other solutions, the degenerate branch \(r_1=r_\tau\), which the Fibonacci hexagon ideal excludes.

**COMPUTATIONAL-CLAIM.** In a left-comb Fibonacci fusion-path basis, every braid generator decomposes into \(1\times1\) and \(2\times2\) local blocks. For a sector of dimension \(d\),

\[
\operatorname{nnz}(\sigma_i)\le 2d.
\]

`experiments/braid_sparsity_baseline.py` verifies this through \(n=14\).

**NEGATIVE BENCHMARK.** This linear sparsity is not AEG-specific: an optimized categorical fusion-path compiler has the same block locality.

**NEGATIVE BENCHMARK.** `experiments/braid_ir_cost_model.py` shows that replaying an explicit history block \(F\to R\to F^{-1}\) is more expensive at execution time than applying its already-verified precompiled \(2\times2\) block. The defensible compiler architecture is therefore

\[
\boxed{
\text{history/proof IR}
\longrightarrow
\text{verified compilation}
\longrightarrow
\text{optimized fusion-path execution IR}.
}
\]

## Levin–Wen single-plaquette result

**CLASSICAL.** The physical baseline is the Levin–Wen string-net plaquette operator. For an n-gon, \(B_p^s\) is a cyclic product of n local F-symbols; no R-data are required.

**COMPUTATIONAL-CLAIM.** `experiments/levin_wen_plaquette.py` constructs the Fibonacci hexagonal plaquette operator from the frozen F-stage data and exhausts all \(2^6=64\) external boundary sectors.

**COMPUTATIONAL-CLAIM.** In every boundary sector,

\[
\boxed{B_p^1=I,\qquad (B_p^\tau)^2=B_p^1+B_p^\tau.}
\]

Thus loop insertion realizes the Fibonacci fusion algebra exactly at operator level.

**COMPUTATIONAL-CLAIM.** With \(\phi=1+a=a^{-1}\),

\[
\boxed{
B_p=\frac{B_p^1+\phi B_p^\tau}{1+\phi^2}
}
\]

satisfies \(B_p^2=B_p\) entrywise in all 64 sectors.

**COMPUTATIONAL-CLAIM.** The hexagonal block dimensions have distribution

\[
1^6,\;2^1,\;3^{15},\;4^{20},\;7^{15},\;11^6,\;18^1,
\]

where the exponent denotes the number of external sectors with that dimension. The all-\(\tau\) boundary is the unique dimension-18 sector and \(B_p^\tau\) has 199 nonzero entries there.

## Exact all-τ n-gon scaling

**COMPUTATIONAL-CLAIM.** For an all-\(\tau\) n-gon, admissible inner histories are closed walks of

\[
C=\begin{pmatrix}0&1\\1&1\end{pmatrix},
\]

so the block dimension is

\[
\boxed{d_n=\operatorname{tr}(C^n)=L_n.}
\]

**COMPUTATIONAL-CLAIM.** Nonzero matrix elements are closed walks of the pair-state transition matrix

\[
A=
\begin{pmatrix}
0&0&0&0\\
0&0&1&1\\
0&1&0&1\\
0&1&1&1
\end{pmatrix},
\]

hence

\[
\boxed{
N_n=\operatorname{tr}(A^n)
=(-1)^n+(1+\sqrt2)^n+(1-\sqrt2)^n.
}
\]

At \(n=14\), \(d_{14}=843\), \(N_{14}=228487\), while the dense matrix has 710649 entries.

**COMPUTATIONAL-CLAIM.** A cyclic local-factor representation still has only \(O(n)\) factor nodes, giving exponential structural compression relative to materializing the sparse matrix.

**NEGATIVE BENCHMARK.** This compression is not AEG-specific. The standard Levin–Wen formula is already precisely such a cyclic local F-factor network, and tensor-network representations of string-net states are classical prior art.

## Adjacent-plaquette commutation baseline

**CLASSICAL.** Neighboring Levin–Wen plaquette operators commute. The project now uses this theorem as a proof-history benchmark rather than as a novelty target.

**COMPUTATIONAL-CLAIM.** `experiments/adjacent_plaquette_commutator.py` constructs two hexagons sharing one edge, with 11 internal lattice edges, 8 fixed dangling legs, and 10 trivalent vertices. It exhausts all \(2^8=256\) dangling-label sectors in the exact coefficient ring

\[
\mathbb Q[q]/(q^4+q^2-1).
\]

**COMPUTATIONAL-CLAIM.** Every sector satisfies

\[
\boxed{B_L^\tau B_R^\tau=B_R^\tau B_L^\tau}
\]

with zero failures.

**COMPUTATIONAL-CLAIM.** If \(k\) of the eight dangling legs carry \(\tau\), the global admissible block dimension is

\[
\boxed{D_k=5F_{k+1}},\qquad 0\le k\le8.
\]

The maximal all-\(\tau\) sector has

\[
D_8=170,
\]

and

\[
\operatorname{nnz}(B_L^\tau)
=
\operatorname{nnz}(B_R^\tau)
=1551.
\]

After exact reduction, each ordered product has 11922 nonzero entries, and the sparse composition performs 14854 nonzero scalar multiplications before accumulation in each order.

**REFORMULATION.** This is the first benchmark in which the two sides are genuinely different overlapping operation histories rather than disjoint-support operations or two spellings of a single local tensor product. The shared edge and neighboring control labels are modified/read in different orders, yet coherence identifies the compiled operators.

**COMPUTATIONAL-CLAIM.** The direct instantiated baseline is therefore complete: there is now a finite, exact, nontrivial operator equality against which an extracted local proof certificate can be measured.

**NEGATIVE BENCHMARK.** No AEG advantage follows from the equality itself. Levin–Wen theory already proves plaquette commutation locally from categorical consistency. The current program still verifies the instantiated operators; it has not yet shown that an explicit history certificate is smaller, more reusable, or easier to verify than a conventional graphical/tensor categorical proof.

## Current research verdict

**COMPUTATIONAL-CLAIM.** No algebraic compression, asymptotic storage advantage, or execution-time advantage over an optimized categorical implementation has been demonstrated through the single-plaquette and direct adjacent-plaquette stages.

**REFORMULATION.** The surviving AEG hypothesis has narrowed to

\[
\boxed{
\text{explicit operation history as a proof/provenance IR above a categorical tensor/execution IR}.
}
\]

**REFORMULATION.** The adjacent-plaquette benchmark sharpens this into a three-layer architecture:

\[
\boxed{
\begin{array}{c}
\text{graph rewrite / operation history}\\
\downarrow\\
\text{coherence proof certificate}\\
\downarrow\\
\text{optimized categorical tensor/operator IR}.
\end{array}}
}
\]

The second layer is now the only untested layer with a plausible computational role.

## Immediate next task

**REFORMULATION.** Extract a local machine-checkable coherence certificate for

\[
\boxed{B_L^\tau B_R^\tau=B_R^\tau B_L^\tau}
\]

without substituting Fibonacci numerical/algebraic constants entry by entry.

The certificate generator should:

1. retain the two twelve-F-factor histories before contraction;
2. factor/cancel identical history outside the shared-edge neighborhood;
3. isolate the minimal nontrivial overlap kernel around the two shared vertices;
4. reduce that kernel by named pentagon and orthogonality/invertibility identities;
5. emit a proof DAG whose nodes are local transports/coherence cells;
6. compare it against an independently constructed optimized categorical/graphical proof after common-subexpression elimination.

Measure primitive F-node count, summed intermediate channels, coherence-cell applications, proof-DAG nodes/edges, trusted-lemma verification work, and invalidation footprint under a local F-data or boundary edit.

**CONJECTURE.** If explicit operation history has a computationally meaningful contribution to the topological-order program, automatic proof-object construction or dependency localization should become visible here.

**STOP CONDITION.** If the extracted history certificate canonicalizes one-for-one to the standard graphical/tensor proof with no additional compression, reuse, or diagnostics, record that AEG is primarily an interpretive layer for this class of fusion/string-net computations and redirect research effort.

## Reconstruction gates

**COMPUTATIONAL-CLAIM.** The F derivation remains the only certified blind reconstruction in this repository.

**PROTOCOL.** The R derivation in `notes/04-symbolic-braiding-history-quotient.md` is exact but non-blind because of source exposure. A separate clean-room workstream is still required if blind R reconstruction is to be claimed.

## Stop conditions

**CLASSICAL.** Record a negative result if the history representation remains only a verbose re-encoding of optimized categorical F/R/string-net computations with no structural or computational gain.

**CLASSICAL.** Record a negative result if no gauge-invariant or representation-complexity information survives beyond known categorical data.

**CLASSICAL.** Do not reinterpret satisfied pentagon/hexagon cells or nontrivial F-moves as nonzero physical curvature; the relevant structure is a flat local system with potentially nontrivial global holonomy.
