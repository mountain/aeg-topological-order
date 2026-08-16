# Round 3 — Levin–Wen Plaquette Factorization and the History-IR Boundary

**Stage:** T8 / string-net compilation benchmark  
**Date:** 2026-08-17  
**Code:** `experiments/levin_wen_plaquette.py`

---

## 0. Executive result

**COMPUTATIONAL-CLAIM.** The Fibonacci Levin–Wen plaquette operator has now been constructed exactly from the frozen F-stage data and exhaustively checked on all `2^6 = 64` external-label sectors of a hexagonal plaquette.

For every sector,

\[
\boxed{B_p^1=I}
\]

and

\[
\boxed{(B_p^\tau)^2=B_p^1+B_p^\tau.}
\]

Thus the loop-insertion operators furnish the Fibonacci fusion algebra directly at the plaquette-operator level.

**COMPUTATIONAL-CLAIM.** Writing

\[
\phi=1+\alpha=\alpha^{-1},
\qquad
\alpha^2+\alpha-1=0,
\]

the standard smooth-phase combination

\[
\boxed{
B_p=\frac{B_p^1+\phi B_p^\tau}{1+\phi^2}
}
\]

satisfies

\[
\boxed{B_p^2=B_p}
\]

in all 64 boundary sectors.

**NEGATIVE BENCHMARK.** The hoped-for AEG representation advantage is not visible at the level of a single plaquette. The standard Levin–Wen matrix-element formula is already a cyclic product of local F-symbols, hence already an O(n)-size local factor graph / tensor-network description of an n-gon plaquette. An AEG history DAG recovers this locality but does not improve its asymptotic representation size against a fair categorical baseline.

**REFORMULATION.** What remains potentially useful is a proof-carrying interpretation: the local factor graph can be retained together with the exact rewrite/coherence history that certifies its compilation, while numerical execution uses the optimized tensor-network or local-block representation.

---

# 1. Source convention and exact dictionary

**CLASSICAL.** Levin and Wen define the plaquette insertion operator \(B_p^s\) by adding a loop of type \(s\) around a plaquette and resolving it through local F-moves. For an n-gon, its matrix element is a product of n local six-index F-symbols.

For the self-dual Fibonacci category we use the six-index convention

\[
\boxed{
F^{a b e}_{c d f}
:=
[F^{a b c}_{d}]_{e f}.
}
\]

Let

- \(a_k\) be the fixed external leg at vertex \(k\);
- \(i_k\) be the old plaquette-edge label;
- \(i'_k\) be the new plaquette-edge label;
- \(s\) be the inserted loop label.

Then

\[
\boxed{
(B_p^s)_{\mathbf i',\mathbf i}(\mathbf a)
=
\prod_{k=1}^{n}
F^{a_k\,i_{k-1}\,i_k}_{s\,i'_k\,i'_{k-1}},
}
\tag{1}
\]

with cyclic indices.

**REFORMULATION.** Equation (1) can be read literally as an operation-history evaluation: each vertex contributes one local reassociation transport and the plaquette amplitude is the ordered product of those local factors.

**CLASSICAL.** This history reading does not alter the categorical content. In particular, no R-symbol is required for \(B_p^s\); the string-net plaquette construction uses fusion data, F-symbols, and quantum dimensions.

---

# 2. Frozen Fibonacci data used

**COMPUTATIONAL-CLAIM.** The code imports no new Fibonacci constants. It uses the F-data already reconstructed in the earlier blind F-stage:

\[
F^{\tau\tau\tau}_{\tau}
=
\begin{pmatrix}
\alpha&q\\
q&-\alpha
\end{pmatrix},
\]

subject to

\[
\boxed{
q^2=\alpha,
\qquad
\alpha^2+\alpha-1=0.
}
\tag{2}
\]

All unit-containing associators use the strict-unit normalization, and

\[
F^{\tau\tau\tau}_{1}=1.
\]

**CLASSICAL.** Because the plaquette benchmark is F-only, the source-contamination warning attached to the previous R-stage is irrelevant to the algebra computed here. The F-data themselves remain the already-audited frozen input.

---

# 3. Hexagonal state spaces

Fix six external labels

\[
\mathbf a=(a_1,\ldots,a_6)\in\{1,\tau\}^6.
\]

An inner plaquette labeling

\[
\mathbf i=(i_1,\ldots,i_6)
\]

is admissible exactly when every trivalent vertex satisfies

\[
\boxed{
i_k\in a_k\otimes i_{k-1}.}
\tag{3}
\]

**COMPUTATIONAL-CLAIM.** Exhausting all 64 external boundary sectors gives the following distribution of block dimensions:

| block dimension | number of external sectors |
|---:|---:|
| 1 | 6 |
| 2 | 1 |
| 3 | 15 |
| 4 | 20 |
| 7 | 15 |
| 11 | 6 |
| 18 | 1 |

The unique dimension-18 sector is the all-\(\tau\) boundary.

**COMPUTATIONAL-CLAIM.** For \(B_p^\tau\), the corresponding number of nonzero matrix elements is determined solely by the block dimension in the hexagonal case:

| dimension | nnz \(B_p^\tau\) |
|---:|---:|
| 1 | 1 |
| 2 | 3 |
| 3 | 7 |
| 4 | 13 |
| 7 | 35 |
| 11 | 81 |
| 18 | 199 |

---

# 4. Exact loop-insertion algebra

**COMPUTATIONAL-CLAIM.** The vacuum insertion is exactly identity in every boundary sector:

\[
B_p^1=I.
\]

This is a useful convention check: the six-index mapping in Section 1 is consistent with the frozen associator convention.

**COMPUTATIONAL-CLAIM.** More importantly, exact symbolic multiplication followed by reduction modulo (2) gives, in every one of the 64 sectors,

\[
\boxed{
(B_p^\tau)^2=I+B_p^\tau.
}
\tag{4}
\]

Equation (4) is precisely the operator image of

\[
\tau\otimes\tau=1\oplus\tau.
\]

**CLASSICAL.** This is the expected Levin–Wen loop-insertion fusion algebra; it is not a new topological invariant.

**REFORMULATION.** In AEG/history language, repeated plaquette-loop insertion gives a particularly clean example in which a large family of explicit operation histories collapses, after coherence quotienting, to a small process algebra:

\[
\boxed{
\text{loop-insertion histories}
\longrightarrow
\text{fusion algebra action}.
}
\]

**CONJECTURE.** If an AEG-specific residual is to survive here, it cannot be the quotient algebra itself. It must live in information intentionally retained before quotienting: provenance, alternative recoupling paths, dependency structure, or proof certificates.

---

# 5. Projector recovered algebraically

Let

\[
\phi=1+\alpha.
\]

Modulo \(\alpha^2+\alpha-1=0\),

\[
\phi=\alpha^{-1},
\qquad
\phi^2=\phi+1.
\]

Define

\[
B_p
=
\frac{I+\phi B_p^\tau}{1+\phi^2}.
\]

Using (4),

\[
(I+\phi B)^2
=
I+2\phi B+\phi^2(I+B).
\]

Since \(\phi^2=\phi+1\), the coefficient comparison gives

\[
(I+\phi B)^2
=(1+\phi^2)(I+\phi B),
\]

hence

\[
\boxed{B_p^2=B_p.}
\]

**COMPUTATIONAL-CLAIM.** The code verifies the projector identity entrywise and exactly in all 64 boundary sectors rather than relying only on the abstract derivation.

---

# 6. All-τ boundary: exact representation-complexity law

The all-\(\tau\) boundary is the largest block and gives a clean scaling laboratory for an n-gon.

## 6.1 Basis dimension

**COMPUTATIONAL-CLAIM.** At each vertex the old inner label obeys

\[
i_k\in\tau\otimes i_{k-1}.
\]

In the ordered state set \((1,\tau)\), the transition matrix is

\[
\boxed{
C=
\begin{pmatrix}
0&1\\
1&1
\end{pmatrix}.
}
\tag{5}
\]

A cyclic admissible labeling is a closed length-n walk in \(C\). Therefore

\[
\boxed{
d_n=\operatorname{tr}(C^n).}
\tag{6}
\]

Because

\[
\chi_C(\lambda)=\lambda^2-\lambda-1,
\]

we obtain

\[
\boxed{d_n=L_n,}
\tag{7}
\]

where \(L_n\) is the Lucas sequence.

Thus

\[
d_n\sim\phi^n.
\]

## 6.2 Number of nonzero plaquette matrix elements

A matrix entry is specified by a pair of cyclic histories

\[
(i_k,i'_k).
\]

There are four pair states

\[
(1,1),(1,\tau),(\tau,1),(\tau,\tau).
\]

**COMPUTATIONAL-CLAIM.** A local transition contributes a nonzero F-symbol exactly according to

\[
\boxed{
A=
\begin{pmatrix}
0&0&0&0\\
0&0&1&1\\
0&1&0&1\\
0&1&1&1
\end{pmatrix}.
}
\tag{8}
\]

Therefore the number of nonzero matrix elements is

\[
\boxed{
N_n=\operatorname{tr}(A^n).
}
\tag{9}
\]

The characteristic polynomial is

\[
\chi_A(\lambda)
=
\lambda(\lambda+1)(\lambda^2-2\lambda-1).
\]

Hence

\[
\boxed{
N_n
=(-1)^n+(1+\sqrt2)^n+(1-\sqrt2)^n.
}
\tag{10}
\]

**COMPUTATIONAL-CLAIM.** Values through n=14 are:

| n | \(d_n\) | nnz \(N_n\) | dense \(d_n^2\) |
|---:|---:|---:|---:|
| 3 | 4 | 13 | 16 |
| 4 | 7 | 35 | 49 |
| 5 | 11 | 81 | 121 |
| 6 | 18 | 199 | 324 |
| 7 | 29 | 477 | 841 |
| 8 | 47 | 1155 | 2209 |
| 9 | 76 | 2785 | 5776 |
| 10 | 123 | 6727 | 15129 |
| 11 | 199 | 16237 | 39601 |
| 12 | 322 | 39203 | 103684 |
| 13 | 521 | 94641 | 271441 |
| 14 | 843 | 228487 | 710649 |

The density obeys asymptotically

\[
\frac{N_n}{d_n^2}
\asymp
\left(\frac{1+\sqrt2}{\phi^2}\right)^n,
\]

where

\[
\frac{1+\sqrt2}{\phi^2}<1.
\]

So the matrix becomes relatively sparser, but the number of nonzero entries remains exponential.

---

# 7. The apparent exponential compression — and why it is not yet AEG

The explicit sparse matrix requires

\[
\Theta(N_n)
\sim
(1+\sqrt2)^n
\]

stored scalar entries in the all-\(\tau\) sector.

But Equation (1) represents the same operator by n local factors with constant local label dimension:

\[
\boxed{
\text{plaquette operator}
=
\text{cyclic network of }n\text{ local F tensors}.
}
\]

Thus the symbolic structural representation has size

\[
\boxed{O(n)}
\]

rather than exponential matrix size.

**NEGATIVE BENCHMARK.** This is a genuine compression relative to materializing the operator matrix, but it is not an AEG-specific result. It is already present in the original local Levin–Wen formula, and tensor-network representations of string-net states are classical prior art.

In particular, the fair comparison is

\[
\boxed{
\text{AEG history DAG}
\quad\text{vs}\quad
\text{categorical local-factor / tensor-network IR},
}
\]

not

\[
\text{AEG history DAG}
\quad\text{vs}\quad
\text{dense matrix}.
\]

At the single-plaquette level, both optimized representations contain one local factor node per plaquette vertex and constant-size F-data templates.

---

# 8. Incremental compilation does not yet separate the two approaches

Suppose one external leg \(a_k\) is changed.

**REFORMULATION.** In an explicit history DAG, only the local F-move node at vertex \(k\) changes at the structural level; the cyclic wiring remains fixed.

**CLASSICAL.** The same is true in the categorical factor graph/tensor network: only the corresponding local tensor changes.

Therefore a naive claim such as

> “AEG allows local recompilation while the categorical formulation requires rebuilding the whole plaquette matrix”

would compare against an artificially weak baseline.

**NEGATIVE BENCHMARK.** No asymptotic incremental-compilation advantage has been demonstrated by the single-plaquette experiment.

---

# 9. What the history representation still contributes conceptually

Although the local factor graph is classical, the AEG framing still suggests a useful separation of layers.

**REFORMULATION.** We can distinguish:

\[
\boxed{
\begin{array}{c}
\text{graphical/string-net operation history}\\
\downarrow\\
\text{local F-move certificate DAG}\\
\downarrow\\
\text{cyclic tensor/factor IR}\\
\downarrow\\
\text{sparse/dense numerical operator as needed}.
\end{array}}
\]

The lower two levels are standard computational representations.

The possible AEG contribution is the explicit retention of the upper proof/provenance layer and its relation to the compiled lower layers.

**CONJECTURE.** This only becomes substantively different if the retained history can support one of the following more cheaply than a conventional implementation:

1. verification that two independently compiled operator circuits are coherent;
2. incremental re-verification after a local graph/category change;
3. extraction of a minimal dependency certificate for a large string-net operator;
4. automatic compilation from a generic graph rewrite rather than a hand-written plaquette formula;
5. diagnostics of failed coherence in approximate, learned, or perturbed categorical data.

None of these has yet been established.

---

# 10. Originality audit

**CLASSICAL.** Local tensor-network representations are already native to string-net theory. Gu–Levin–Swingle–Wen construct tensor-product representations for general string-net condensed states, and Buerschaper–Aguado–Vidal give explicit tensor-network representations built from the underlying tensor-category data.

**CLASSICAL.** Bonesteel–DiVincenzo also construct quantum circuits for Fibonacci Levin–Wen vertex and plaquette measurements using local categorical transformations, reinforcing that “compile the plaquette into local F operations” is not new by itself.

**COMPUTATIONAL-CLAIM.** A targeted primary-source search did not locate the exact closed form (10) for the number of nonzero all-\(\tau\) plaquette matrix elements. We therefore record (8)–(10) as a project calculation, not as a novelty claim. A broader literature audit would be required before calling it new.

---

# 11. Research verdict after the single-plaquette benchmark

The current evidence is now unusually consistent across three stages:

\[
\begin{array}{c|c|c}
\text{stage}&\text{AEG/history observation}&\text{fair baseline verdict}\\
\hline
F/pentagon&\text{sparse history complex}&\text{same polynomial ideal}\\
R/hexagon&\text{local exchange history}&\text{same optimized local blocks}\\
B_p&\text{cyclic F-history DAG}&\text{same local tensor network}
\end{array}
\]

**NEGATIVE BENCHMARK.** Through the single-plaquette stage, there is still no demonstrated algebraic, asymptotic storage, or execution-time advantage over an optimized categorical implementation.

**REFORMULATION.** The strongest surviving interpretation is now sharply delimited:

\[
\boxed{
\text{AEG here is a candidate proof/provenance IR above a categorical execution IR.}
}
\]

That claim is narrower than the original hope but also much more testable.

---

# 12. Next discriminating experiment: overlapping plaquettes

The single plaquette is too local to distinguish proof-history value from ordinary tensor-network locality.

The next benchmark should use two adjacent plaquettes \(p,q\), where Levin–Wen exact solvability requires

\[
\boxed{[B_p,B_q]=0.}
\]

This introduces overlapping local rewrites and genuinely different evaluation orders.

The experiment should compare two certificate strategies:

### A. Direct categorical/tensor baseline

Construct the two operators on the shared finite patch and verify their commutator by optimized tensor contraction / symbolic reduction.

### B. Explicit history certificate

Compile

\[
B_pB_q
\]

and

\[
B_qB_p
\]

as two rewrite histories and reduce the equality using only recorded local coherence cells, primarily pentagon/orthogonality identities.

Measure:

- number of local F nodes;
- number of distinct intermediate histories;
- amount of shared DAG structure;
- certificate size;
- exact verification operations;
- invalidation footprint under one local boundary edit;
- comparison with the optimized tensor-network proof, not with a dense matrix.

**CONJECTURE.** If explicit operation history has a genuine computational role in this project, overlapping-plaquette commutation is the first benchmark where it has a realistic chance to appear. If the two proof representations again canonicalize to the same local tensor-network contraction, the evidence will strongly favor treating the AEG contribution here as interpretive rather than computational.
