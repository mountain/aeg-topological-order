# Round 3 — Adjacent Plaquette Commutation as a Proof-History Benchmark

**Stage:** T8 / overlapping string-net compilation  
**Date:** 2026-08-17  
**Code:** `experiments/adjacent_plaquette_commutator.py`

---

## 0. Executive result

**COMPUTATIONAL-CLAIM.** The single-plaquette benchmark in `note_06` has now been extended to the first genuinely overlapping rewrite problem: two hexagonal Levin–Wen plaquettes sharing one edge.

The finite patch contains

\[
\boxed{
11\text{ internal edges},\qquad
8\text{ fixed dangling legs},\qquad
10\text{ trivalent vertices}.
}
\]

For every one of the

\[
2^8=256
\]

assignments of Fibonacci labels to the dangling legs, the code constructs the complete admissible internal Hilbert-space block and the two exact sparse operators

\[
B_L^\tau,\qquad B_R^\tau.
\]

It then verifies

\[
\boxed{
B_L^\tau B_R^\tau
=
B_R^\tau B_L^\tau
}
\tag{1}
\]

exactly, with zero failed sectors.

**CLASSICAL.** Equation (1) is required by Levin–Wen exact solvability and is not a new theorem.

**REFORMULATION.** What is new to the project is its role as a benchmark: the two sides of (1) are two different overlapping local rewrite histories leading to the same physical operator. This is the first test in which an explicit history/proof IR could conceivably show value beyond merely storing local tensors.

---

# 1. The two-plaquette patch

Use two hexagons sharing the edge \(AB\):

\[
\begin{aligned}
L &: A-B-C-D-E-F-A,\\
R &: B-A-G-H-I-J-B.
\end{aligned}
\]

The unique internal edges are

\[
AB,BC,CD,DE,EF,FA,AG,GH,HI,IJ,JB.
\]

Vertices \(C,D,E,F,G,H,I,J\) each carry one fixed dangling external leg.

The shared vertices are

\[
A:\{AB,FA,AG\},
\qquad
B:\{AB,BC,JB\}.
\]

**CLASSICAL.** The patch is trivalent and all vertex states are constrained by the Fibonacci branching rule.

**REFORMULATION.** Relative to the left plaquette, \(AG\) and \(JB\) are external legs; relative to the right plaquette, \(FA\) and \(BC\) are external legs. Consequently the two plaquette operators overlap nontrivially: an edge changed by one operator can be control/boundary data for the other.

This is why commutation is not a trivial disjoint-support statement.

---

# 2. Exact coefficient ring

The frozen F-stage uses

\[
q^2=\alpha,
\qquad
\alpha^2+\alpha-1=0.
\]

Eliminating \(\alpha\) gives

\[
\boxed{q^4+q^2-1=0.}
\tag{2}
\]

**COMPUTATIONAL-CLAIM.** To make the exhaustive two-plaquette check fast and exactly auditable, the experiment implements coefficients directly in

\[
K=\mathbb Q[q]/(q^4+q^2-1)
\]

using the basis

\[
1,q,q^2,q^3.
\]

No floating-point comparison is used.

The nontrivial F entries are represented as

\[
\alpha=q^2,\qquad q,\qquad -\alpha=-q^2.
\]

---

# 3. Global admissible state spaces

Let \(k\) be the number of dangling external legs labeled \(\tau\), with

\[
0\le k\le8.
\]

**COMPUTATIONAL-CLAIM.** Exhaustive enumeration shows that the Hilbert-space block dimension depends only on \(k\), not on the positions of the \(\tau\) legs:

\[
\boxed{
D_k=5F_{k+1},
}
\tag{3}
\]

where \(F_n\) is the Fibonacci sequence with \(F_1=F_2=1\).

Thus:

| \(k\) | block dimension \(D_k\) | number of external sectors |
|---:|---:|---:|
| 0 | 5 | 1 |
| 1 | 5 | 8 |
| 2 | 10 | 28 |
| 3 | 15 | 56 |
| 4 | 25 | 70 |
| 5 | 40 | 56 |
| 6 | 65 | 28 |
| 7 | 105 | 8 |
| 8 | 170 | 1 |

Equivalently, the dimension histogram is

\[
5^9,
10^{28},
15^{56},
25^{70},
40^{56},
65^{28},
105^8,
170^1,
\]

where exponents denote numbers of external sectors.

**COMPUTATIONAL-CLAIM.** Equation (3) is recorded as a project calculation, not as an originality claim. A separate literature audit would be required before assigning novelty.

---

# 4. Maximal all-τ sector

The largest sector has all eight dangling legs equal to \(\tau\).

Its dimension is

\[
\boxed{D_8=170.}
\]

**COMPUTATIONAL-CLAIM.** In this block,

\[
\operatorname{nnz}(B_L^\tau)
=
\operatorname{nnz}(B_R^\tau)
=1551.
\]

After exact coefficient reduction,

\[
\operatorname{nnz}(B_L^\tau B_R^\tau)
=
\operatorname{nnz}(B_R^\tau B_L^\tau)
=11922.
\]

The sparse composition performs

\[
14854
\]

nonzero scalar multiplications in each order before accumulation.

So this is already large enough that the identity (1) is not visually or syntactically trivial.

---

# 5. Why this is a better history benchmark

For one plaquette, the standard Levin–Wen formula is already a single cyclic product

\[
\prod_{k=1}^{6}F_k.
\]

An AEG history DAG and an ordinary tensor-factor representation are therefore almost the same object.

For two adjacent plaquettes, however, we now have two orderings:

\[
\boxed{
\mathcal H_{LR}:
B_R^\tau\to B_L^\tau
}
\]

and

\[
\boxed{
\mathcal H_{RL}:
B_L^\tau\to B_R^\tau.
}
\]

The operators share the edge \(AB\), and the side edges

\[
FA,AG,BC,JB
\]

play the role of dynamic plaquette labels for one operator and control/external labels for the other.

**REFORMULATION.** Thus \(\mathcal H_{LR}\) and \(\mathcal H_{RL}\) are genuinely distinct operation histories, not merely scalar factors written in another order.

Equation (1) states that categorical coherence identifies their compiled actions.

This is much closer to the motivating AEG question:

> what useful information is carried by explicitly retaining two different coherent process histories that conventional semantics identify?

---

# 6. Direct verification is large; the mathematical proof is local

**COMPUTATIONAL-CLAIM.** A direct sparse-matrix verifier on the maximal block handles operators with 1551 nonzero entries and products with 11922 nonzero entries.

**CLASSICAL.** Yet the theorem that neighboring Levin–Wen plaquette operators commute is local and follows from the tensor-category consistency conditions. The mathematical reason does not scale with the Hilbert-space block dimension.

This creates the first meaningful certificate gap:

\[
\boxed{
\begin{array}{c}
\text{large instantiated operator equality}\\
\updownarrow\\
\text{small local coherence proof}.
\end{array}}
}
\]

**REFORMULATION.** An operation-history compiler could be valuable if it automatically emits the lower object—the small proof certificate—while still compiling the upper operator when numerical execution is required.

But this advantage must be compared against a conventional categorical/diagrammatic proof system, not against sparse matrix multiplication alone.

---

# 7. What has and has not been demonstrated

## Demonstrated

**COMPUTATIONAL-CLAIM.** The direct instantiated baseline is now complete for this finite patch:

- all 256 external sectors are enumerated;
- both plaquette operators are generated from the same frozen F-data;
- both composition orders are evaluated exactly;
- every sector satisfies commutation.

**REFORMULATION.** The benchmark therefore has a precise target for a future history certificate generator.

## Not yet demonstrated

**NEGATIVE BENCHMARK.** We have not yet shown that an AEG history certificate is smaller than, easier to verify than, or more reusable than a standard categorical graphical proof.

**NEGATIVE BENCHMARK.** The current exact program is still an instantiated operator verifier. It does not yet extract the pentagon/orthogonality proof steps responsible for the cancellation.

**CLASSICAL.** Since Levin–Wen theory already supplies a local coherence proof of commutation, merely rediscovering that proof in history notation would be a reformulation.

---

# 8. A sharper compiler architecture

The evidence now supports a three-layer architecture:

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

The first layer records what transformations were requested.

The second records why alternative rewrite orders are equivalent.

The third is what should actually execute numerically.

**REFORMULATION.** This is more specific than the previous two-level braid architecture because overlapping plaquettes introduce a genuine proof obligation between two independently valid local compilation orders.

---

# 9. The next decisive subproblem: certificate extraction

The immediate next task is no longer another larger matrix calculation.

It is to turn the verified identity

\[
B_L^\tau B_R^\tau=B_R^\tau B_L^\tau
\]

into an explicit local coherence certificate.

The compiler should:

1. retain the two twelve-F-factor histories before contraction;
2. identify factors outside the shared-edge neighborhood that are identical in both histories;
3. isolate the minimal nontrivial overlap kernel around \(A,B\);
4. reduce that kernel by named pentagon/orthogonality identities rather than by substituting Fibonacci numbers;
5. emit a machine-checkable proof DAG;
6. compare that DAG with a direct categorical tensor proof after common-subexpression elimination.

Measure:

- primitive F nodes before and after shared-factor elimination;
- number of summed intermediate channels;
- number of coherence-cell applications;
- proof DAG node/edge count;
- verification arithmetic after treating pentagon/orthogonality as trusted lemmas;
- invalidation footprint if one local F datum or boundary edge changes.

**CONJECTURE.** If AEG has a computationally meaningful contribution to this string-net problem, it should appear here as automatic proof-object construction or dependency localization.

**STOP CONDITION.** If the extracted history certificate canonicalizes one-for-one to the standard graphical/tensor categorical proof with no additional compression, reuse, or diagnostics, then the topological-order program should record that AEG is primarily an interpretive layer for this class of problems and redirect effort elsewhere.
