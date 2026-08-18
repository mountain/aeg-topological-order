# Status

## Stage

`T0–T8 EXACT FIBONACCI CATEGORY BENCHMARK CLOSED — coherence-quotient barrier identified; un-enriched history line stopped`

## Executive verdict

**COMPUTATIONAL-CLAIM.** The repository has now tested explicit operation-history representations through four increasingly demanding exact Fibonacci benchmarks:

1. fusion/F-symbol reconstruction and pentagon coherence;
2. braiding/R-symbol reconstruction and hexagon/braid transport;
3. Levin–Wen single-plaquette compilation;
4. adjacent-plaquette commutation and proof-certificate extraction.

**NEGATIVE BENCHMARK.** At every stage, once the baseline is an optimized categorical/graphical implementation rather than a naive dense encoding, no AEG-specific algebraic compression, asymptotic storage advantage, execution-time advantage, or proof-certificate compression has been demonstrated.

**REFORMULATION.** AEG remains a faithful language for making operation histories explicit, but explicitness alone is not a new invariant or computational advantage in this exact fusion/string-net setting.

**RESEARCH DECISION.** Stop scaling the un-enriched exact Fibonacci/category line. Any further topological-order work must add an explicit semantics that ordinary coherence deliberately forgets: resource cost, provenance/dependency, approximation defect, physical control path, or another justified enrichment.

---

## F-stage result

**COMPUTATIONAL-CLAIM.** The blind reconstruction in `experiments/fibonacci_pentagon.py` starts from the Fibonacci fusion grammar and symbolic nontrivial associator only. Pentagon coherence plus invertibility gives

\[
\boxed{
g=1,\qquad d=-a,\qquad bc=a,\qquad a^2+a-1=0.
}
\]

Unitarity selects

\[
\boxed{a=(\sqrt5-1)/2},
\]

and a real symmetric gauge has off-diagonal entries \(\sqrt a\).

**CLASSICAL.** The post-freeze comparison agrees with the standard Fibonacci F-matrix. This reconstructs known category data.

**NEGATIVE BENCHMARK.** The independent direct categorical pentagon baseline has the same five symbolic variables and the same polynomial ideal. The history complex therefore gives no algebraic compression at this benchmark.

**COMPUTATIONAL-CLAIM.** The five-input associahedron has 14 vertices, 21 reassociation edges, 3 square faces, and 6 pentagonal faces. Every face holonomy is identity under the frozen F solution in both total-charge sectors.

**CLASSICAL.** Pure reassociation coherence is flat. A nontrivial F-move is not physical/topological curvature.

---

## Braided-stage result

**PROTOCOL.** The braided follow-up is exact but not certified blind because its lineage was exposed to a comparison source containing explicit Fibonacci R-data. No standard R constants are encoded in the experiments.

**COMPUTATIONAL-CLAIM.** Frozen F-data plus the generic multiplicity-free hexagon equation gives

\[
\boxed{
r_1=r_\tau^2,
\qquad
r_\tau^2+a r_\tau+1=0,
\qquad
a^2+a-1=0.
}
\]

Eliminating \(a\) gives

\[
\boxed{
\Phi_{10}(r_\tau)
=r_\tau^4-r_\tau^3+r_\tau^2-r_\tau+1=0.
}
\]

**COMPUTATIONAL-CLAIM.** The compiled \(B_3\) and \(B_4\) representations satisfy the Artin relations exactly in all small Fibonacci total-charge sectors.

**COMPUTATIONAL-CLAIM.** The Artin relation alone is weaker than hexagon coherence and admits a degenerate \(r_1=r_\tau\) branch excluded by the braided fusion-category equations.

**CLASSICAL.** The permutation-enriched “parenthesization + exchange” skeleton is closely related to the classical parenthesized braid groupoid/operad. It is not an AEG novelty.

**NEGATIVE BENCHMARK.** Fusion-path braid generators already decompose into local 1x1/2x2 blocks in the optimized categorical baseline; replaying explicit F–R–F histories is slower than applying verified precompiled blocks.

---

## Single-plaquette string-net result

**CLASSICAL.** The physical baseline is the Levin–Wen string-net Hamiltonian. For an n-gon, \(B_p^s\) is already a cyclic product of n local F-symbols.

**COMPUTATIONAL-CLAIM.** `experiments/levin_wen_plaquette.py` exhausts all \(2^6=64\) external-label sectors of a Fibonacci hexagonal plaquette and verifies exactly

\[
\boxed{
B_p^1=I,
\qquad
(B_p^\tau)^2=B_p^1+B_p^\tau.
}
\]

With \(\phi=1+a=a^{-1}\),

\[
\boxed{
B_p=\frac{B_p^1+\phi B_p^\tau}{1+\phi^2}
}
\]

satisfies \(B_p^2=B_p\) in every sector.

**COMPUTATIONAL-CLAIM.** For an all-\(\tau\) n-gon,

\[
\boxed{d_n=L_n}
\]

and the number of nonzero matrix elements of \(B_p^\tau\) is

\[
\boxed{
N_n=(-1)^n+(1+\sqrt2)^n+(1-\sqrt2)^n.
}
\]

At \(n=14\), \(d_n=843\) and \(N_n=228487\).

**NEGATIVE BENCHMARK.** Although the local-factor representation is exponentially smaller than a materialized operator matrix, the standard Levin–Wen formula and classical string-net tensor-network representations already have this O(n) local structure. This is not an AEG-specific compression.

---

## Adjacent-plaquette exact baseline

**COMPUTATIONAL-CLAIM.** `experiments/adjacent_plaquette_commutator.py` constructs two adjacent hexagons sharing one edge, with 11 internal edges, 8 fixed dangling legs, and 10 trivalent vertices. All \(2^8=256\) dangling-label sectors are verified exactly in

\[
\mathbb Q[q]/(q^4+q^2-1).
\]

Every sector satisfies

\[
\boxed{B_L^\tau B_R^\tau=B_R^\tau B_L^\tau}.
\]

If \(k\) dangling legs carry \(\tau\), the global block dimension is

\[
\boxed{D_k=5F_{k+1}}.
\]

The maximal all-\(\tau\) sector has dimension 170; each plaquette operator has 1551 nonzero entries; each ordered product has 11922 nonzero entries after exact reduction; sparse composition performs 14854 nonzero scalar multiplications per order before accumulation.

**REFORMULATION.** This is a genuinely overlapping-history benchmark: the two operator schedules are different local rewrite orders, not disjoint-support operations.

---

## Graphical certificate result

**CLASSICAL.** Levin–Wen Appendix C already gives a constant-size graphical proof of adjacent-plaquette commutation. In the fattened-lattice representation,

\[
\boxed{B_p^s=\mathcal R\circ I_p^s},
\]

where \(I_p^s\) inserts an \(s\)-loop and \(\mathcal R\) coherently reduces the fattened diagram to physical lattice states.

For adjacent plaquettes \(L,R\),

\[
\boxed{
I_L^{s_L}I_R^{s_R}X
=
I_R^{s_R}I_L^{s_L}X
}
\]

as the same two-loop graphical state. Applying the same coherent reduction yields plaquette commutation.

**REFORMULATION.** `experiments/plaquette_commutation_certificate.py` machine-encodes this as a constant-size history diamond: 5 explicit nodes, 4 explicit edges, zero coefficient arithmetic, with graphical semantics and coherent reduction as the trusted categorical boundary.

**NEGATIVE BENCHMARK.** This certificate is a machine-readable restatement of the classical string-net graphical proof. It does not supply AEG-specific proof compression, proof reuse, or incremental-verification asymptotics.

This triggers the repository stop condition for the un-enriched exact-category line.

---

## Coherence-quotient barrier

**REFORMULATION.** `notes/08-graphical-certificate-and-coherence-barrier.md` records the structural reason the benchmarks repeatedly collapse to known categorical semantics.

Let \(\mathsf H(x,y)\) be explicit histories between presentations \(x,y\), and let \(\sim_{\mathrm{coh}}\) be generated by triangle/pentagon/hexagon/string-net coherence cells.

For a proposed history quantity

\[
J:\mathsf H(x,y)\to S,
\]

there is a basic dichotomy.

### A. Coherence-invariant history quantity

If

\[
h_1\sim_{\mathrm{coh}}h_2\Rightarrow J(h_1)=J(h_2),
\]

then \(J\) factors through the categorical coherence quotient. For pure reassociation it is constant on parallel coherent histories; in the braided case the surviving nontrivial path classes are already braid/categorical data.

### B. History-sensitive quantity

If \(J\) distinguishes coherence-equivalent histories, it does not descend to the exact categorical/topological object. It can still be meaningful only after adding extra semantics such as computational cost, memory, provenance, error, uncertainty, physical time, or implementation constraints.

Thus

\[
\boxed{
\begin{array}{c}
\text{coherence invariant}\Rightarrow\text{factors through category},\\
\text{history sensitive}\Rightarrow\text{requires enrichment}.
\end{array}}
}
\]

**CLASSICAL.** This is not claimed as a new category-theoretic theorem; it is a strategic consequence of classical coherence for the AEG program.

---

## Research decision and next admissible direction

**NEGATIVE BENCHMARK.** Do not continue the exact Fibonacci line merely by increasing anyon count, fusion-tree size, plaquette count, or operator dimension. The current evidence predicts that optimized categorical graphical/tensor methods will absorb the same exact coherence structure.

**REFORMULATION.** If this repository continues, the next experiment must first define an enrichment deliberately not killed by coherence. The cleanest candidate is a resource-enriched history groupoid:

\[
\boxed{
(\text{coherence class},\;\text{cost/provenance/dependency data}).
}
\]

Then the nontrivial problem is optimization over a coherence class,

\[
\boxed{
\min_{h\in[h_0]_{\mathrm{coh}}} W(h),
}
\]

or diagnosis of coherence defects for approximate/learned/noisy F/R data.

**CONJECTURE.** Such enrichment may give explicit history a real computational semantics. It would, however, be a compiler/proof/error-geometry problem layered on top of topological order, not a new exact invariant of the Fibonacci fusion category.

## Reconstruction gate

**COMPUTATIONAL-CLAIM.** The F derivation remains the only certified blind reconstruction in this repository.

**PROTOCOL.** The R derivation is exact but non-blind because of source exposure. A separate clean-room workstream is required before any blind-R claim.

## Stop condition now active

**CLASSICAL.** The un-enriched exact-category workstream is closed. Reopening it requires a recorded new question that is not already identified with standard category/string-net graphical coherence, or an explicit enrichment with measurable semantics.
