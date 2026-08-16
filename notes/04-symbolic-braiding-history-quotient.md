# Note 04 — Symbolic Braiding, Parenthesized-History Quotients, and the First Nontrivial Holonomy

**Status:** research note / exact symbolic derivation / originality audit  
**Date:** 2026-08-17

---

## 0. Scope and protocol status

This note continues the frozen Fibonacci F-stage.

The present workstream is **not eligible to claim a blind R reconstruction**: during the post-freeze F comparison, it was exposed to a source that also contains explicit Fibonacci R-data. No explicit standard Fibonacci R-values are copied into this repository or used as inputs below.

Accordingly the result is labeled as a symbolic re-derivation from:

1. the frozen Fibonacci fusion grammar;
2. the frozen F-data derived in `notes/01-blind-fibonacci-pentagon.md`;
3. the generic multiplicity-free hexagon equation.

A genuinely blind R benchmark still requires an independent clean-room reproduction.

---

## 1. Frozen F input

Use

\[
\tau\otimes\tau=1\oplus\tau
\]

and the real symmetric unitary F gauge already frozen at the end of the blind stage:

\[
F^{\tau\tau\tau}_{\tau}
=
\begin{pmatrix}
a&s\\
s&-a
\end{pmatrix},
\qquad
s^2=a,
\qquad
a^2+a-1=0,
\]

with the unitary-selected root \(a>0\), and

\[
F^{\tau\tau\tau}_{1}=1.
\]

All associators involving the tensor unit are normalized to the identity.

**CLASSICAL / frozen from the preceding stage.**

---

## 2. Unknown local exchange data

With vacuum braiding normalized to the identity, only two nontrivial local exchange symbols remain:

\[
\boxed{
 r_1:=R^{\tau\tau}_{1},
 \qquad
 r_\tau:=R^{\tau\tau}_{\tau}.
}
\]

Both are required to be nonzero.

For identical incoming simple objects, these quantities are already particularly well behaved under ordinary multiplicity-free vertex-frame rescaling: the source and target one-dimensional fusion spaces are the same \(V^{\tau\tau}_c\), so conjugating the exchange map by a scalar frame change cancels. Thus their eigenvalues, and in particular their ratio, are the natural gauge-invariant quantities to monitor.

**CLASSICAL.**

---

## 3. Generic hexagon equation

The implementation follows the multiplicity-free convention in Aboumrad 2022, Eq. (2.3):

\[
(R^{ac}_{e})^{\pm1}
[F^{acb}_{d}]_{eg}
(R^{bc}_{g})^{\pm1}
=
\sum_f
[F^{cab}_{d}]_{ef}
(R^{fc}_{d})^{\pm1}
[F^{abc}_{d}]_{fg}.
\]

The exact symbolic enumerator is

`experiments/fibonacci_braid_groupoid.py`.

Over all \(2^6\) label sextuples, after admissibility pruning there are only five nonzero equation instances for the positive hexagon and five for the negative hexagon.

**COMPUTATIONAL-CLAIM.**

---

## 4. Exact symbolic reduction

A Groebner reduction of the positive-hexagon equations together with

\[
s^2-a=0,
\qquad
a^2+a-1=0
\]

gives the canonical ideal

\[
\boxed{
\begin{aligned}
a r_\tau+r_1+1&=0,\\
a r_\tau+r_\tau^2+1&=0,\\
s^2-a&=0,\\
a^2+a-1&=0.
\end{aligned}}
\]

Equivalently,

\[
\boxed{
 r_1=r_\tau^2,
 \qquad
 r_\tau^2+a r_\tau+1=0.
}
\tag{4.1}
\]

The negative hexagon equations reduce identically to zero modulo this positive-hexagon ideal, so they add no extra constraint in this benchmark.

**COMPUTATIONAL-CLAIM.**

This is a reconstruction of classical Fibonacci braided data, not a candidate-new invariant.

---

## 5. Cyclotomic structure emerges without inserting a phase

Eliminate \(a\) between

\[
a^2+a-1=0
\]

and

\[
r_\tau^2+a r_\tau+1=0.
\]

The resultant is

\[
\boxed{
 r_\tau^4-r_\tau^3+r_\tau^2-r_\tau+1=0.
}
\]

But

\[
\boxed{
 r_\tau^4-r_\tau^3+r_\tau^2-r_\tau+1
 =\Phi_{10}(r_\tau).
}
\]

Hence

\[
\boxed{r_\tau\text{ is a primitive tenth root of unity}}
\]

on the algebraic solution set, and since

\[
r_1=r_\tau^2,
\]

\(r_1\) lies on the corresponding fifth-root orbit.

For the already-selected positive real \(a\), the quadratic

\[
z^2+a z+1=0
\]

has two complex-conjugate unit-modulus roots. They give the two opposite chiralities/orientations of the braided structure.

**COMPUTATIONAL-CLAIM / CLASSICAL interpretation.**

The important point for this project is methodological:

> the cyclotomic exchange phase is selected by fusion coherence plus the already-derived F geometry; it need not be postulated as an extra numerical constant.

Because this workstream is source-contaminated with respect to explicit R-data, this statement still requires a future clean-room reproduction before it can be entered in the blind-reconstruction ledger.

---

## 6. The first gauge-invariant history holonomy

From (4.1),

\[
\frac{r_1}{r_\tau}=r_\tau.
\]

Therefore the projective spectral ratio of the elementary exchange operator is itself constrained by

\[
\boxed{\Phi_{10}\!\left(\frac{r_1}{r_\tau}\right)=0.}
\]

This is the first point in the project at which a nontrivial gauge-invariant transport survives after the pure reassociation coherence has been quotiented.

Contrast the F-only stage:

\[
\text{associahedral F transport}
\quad\Longrightarrow\quad
\text{all contractible 2-cell holonomies}=I.
\]

After exchange is admitted:

\[
\text{local R transport}
\quad\Longrightarrow\quad
\text{nontrivial projective exchange spectrum}.
\]

**REFORMULATION.** This is not a new invariant; it is the classical braided data seen through the operation-history local-system language.

---

## 7. Three-anyon braid representation from local history moves

On the three-\(\tau\), total-\(\tau\) fusion space with basis indexed by the first-pair channel \(\{1,\tau\}\), define

\[
D=\operatorname{diag}(r_1,r_\tau),
\qquad
F=
\begin{pmatrix}
a&s\\s&-a\end{pmatrix}.
\]

Then

\[
\boxed{\sigma_1=D}
\]

is already local in the left-associated chart, while

\[
\boxed{\sigma_2=F^{-1}DF=FDF}
\]

is compiled as the history path

\[
((\tau\tau)\tau)
\xrightarrow{F}
(\tau(\tau\tau))
\xrightarrow{R}
(\tau(\tau\tau))
\xrightarrow{F^{-1}}
((\tau\tau)\tau).
\]

The exact symbolic verifier proves

\[
\boxed{
\sigma_1\sigma_2\sigma_1
=
\sigma_2\sigma_1\sigma_2
}
\]

modulo the frozen F relations and the hexagon-derived R ideal.

The one-dimensional total-1 sector also satisfies the relation trivially.

**COMPUTATIONAL-CLAIM.**

---

## 8. Four-anyon braid representation

For four \(\tau\) anyons in a left-comb fusion-path basis, the dimensions are

\[
\dim V^{\tau^4}_{1}=2,
\qquad
\dim V^{\tau^4}_{\tau}=3.
\]

The experiment compiles

\[
\sigma_1,\sigma_2,\sigma_3
\]

using only diagonal R blocks and local \(F^{-1}RF\) blocks. Exact symbolic reduction verifies in both total-charge sectors:

\[
\boxed{
\begin{aligned}
\sigma_1\sigma_2\sigma_1&=\sigma_2\sigma_1\sigma_2,\\
\sigma_2\sigma_3\sigma_2&=\sigma_3\sigma_2\sigma_3,\\
\sigma_1\sigma_3&=\sigma_3\sigma_1.
\end{aligned}}
\]

Thus the history compiler has reached an exact \(B_4\) representation without importing an explicit phase table.

**COMPUTATIONAL-CLAIM.**

---

## 9. A crucial red-team result: braid relations alone are too weak

Suppose instead that we forget the hexagon equations and ask only that

\[
\sigma_1=D,
\qquad
\sigma_2=FDF
\]

satisfy the Artin relation.

Reducing the matrix equation modulo only the frozen F relations gives a common factor

\[
\boxed{
(r_1-r_\tau)\,Q(a,r_1,r_\tau)=0,
}
\]

where

\[
Q
=(2a-1)(r_1^2+r_\tau^2)
 +(2-3a)r_1r_\tau.
\]

In particular, the entire degenerate branch

\[
r_1=r_\tau
\]

satisfies the braid relation but does **not** satisfy the Fibonacci hexagon ideal.

Therefore:

\[
\boxed{
\text{braid-group consistency}
\;<\;
\text{braided-fusion coherence}.
}
\]

This is strategically important. AEG cannot reconstruct a braided fusion theory by observing global braid relations alone. The local higher-cell compatibility tying F and R together is indispensable.

**COMPUTATIONAL-CLAIM.**

---

## 10. Why strand identities must be retained before quotienting

If all incoming simple-object labels are merely written as \(\tau\), an exchange appears to start and end at the same labelled fusion tree. That representation hides the topology too early.

Instead retain temporary strand identities \(1,2,3\), even though each strand carries the same simple-object label \(\tau\).

Define a history object by

\[
\boxed{
(\text{parenthesization},\text{strand permutation}).
}
\]

For three strands:

- there are \(2\) parenthesizations;
- there are \(3!=6\) strand orders;
- hence \(12\) labelled history objects;
- F-edges preserve strand order;
- local R-edges swap the sibling pair.

The resulting undirected generator graph has

\[
\boxed{
12\text{ vertices},\quad
6\text{ F-edges},\quad
6\text{ R-edges},
}
\]

and is a single 12-cycle.

After quotienting the temporary strand identities by the permutation symmetry appropriate to identical anyons, only two parenthesization objects remain. The F edge remains a chart transition, while the two local exchange edges become loops.

This gives the correct geometric intuition:

\[
\boxed{
\text{exchange is not local curvature of the F complex;}
\quad
\text{it becomes nontrivial holonomy after the identical-particle quotient.}
}
\]

**REFORMULATION / small-model computation.**

We are not claiming that this 12-vertex graph by itself is a new model of configuration space. It is a finite combinatorial skeleton for the local history compiler.

---

## 11. Originality audit: this is close to the classical parenthesized braid groupoid

The previous section immediately triggers a literature red flag.

The classical **parenthesized braid groupoid/operad** already combines:

- parenthesized words;
- braid/exchange morphisms;
- configuration-space fundamental groupoids;
- associator and braiding coherence.

A particularly direct modern reference is:

Yuto Moriwaki, *Vertex operator algebra and parenthesized braid operad*, arXiv:2209.10443.

That work explicitly describes the parenthesized braid operad as the operad of fundamental groupoids of configuration spaces and studies its monodromy action.

Therefore:

\[
\boxed{
\text{the bare fusion--braid history groupoid is not an AEG novelty.}
}
\]

The remaining AEG question must be narrower and testable:

> Does an operation-history representation attached to this classical parenthesized-braid skeleton provide a superior intermediate representation, sparse certificate system, compilation method, or complexity semantics for concrete fusion-category/string-net computations?

**CLASSICAL literature audit / REFORMULATION.**

This is a useful narrowing of the research claim.

---

## 12. Sparsity benchmark

Let

\[
d=\dim V^{\tau^n}_c
\]

in the standard left-comb fusion-path basis.

The Fibonacci dimensions satisfy

\[
\dim V^{\tau^n}_{1}=F_{n-1},
\qquad
\dim V^{\tau^n}_{\tau}=F_n.
\]

For every Artin generator \(\sigma_i\):

- \(\sigma_1\) is diagonal;
- for \(i\ge2\), only the single intermediate charge \(q_i\) is changed;
- therefore the basis decomposes into local blocks of size at most \(2\times2\).

If there are \(B\) nontrivial 2-blocks, then

\[
\operatorname{nnz}(\sigma_i)
=d+2B
\le 2d.
\]

Thus

\[
\boxed{
\operatorname{nnz}(\sigma_i)=O(d)
}
\]

whereas a materialized dense operator has \(d^2\) entries.

`experiments/braid_sparsity_baseline.py` verifies this combinatorially through at least \(n=14\). For the total-\(\tau\) sector, the worst generator profiles include:

| \(n\) | \(d\) | max nnz | dense entries |
|---:|---:|---:|---:|
| 4 | 3 | 5 | 9 |
| 6 | 8 | 14 | 64 |
| 8 | 21 | 37 | 441 |
| 10 | 55 | 97 | 3025 |
| 12 | 144 | 254 | 20736 |
| 14 | 377 | 665 | 142129 |

This is a genuine representation-complexity distinction between a local compiled form and a naive dense matrix.

However, it is **not yet an AEG advantage**: an optimized categorical fusion-path implementation uses exactly the same local block structure.

So the current verdict remains:

\[
\boxed{
\text{history IR: linear sparse certificate}\;
\equiv\;
\text{optimized categorical local compiler at this benchmark}.
}
\]

**COMPUTATIONAL-CLAIM / negative benchmark.**

---

## 13. Revised conceptual picture

The project now has three clearly separated layers.

### Layer A — reassociation geometry

\[
\text{parenthesized fusion histories}
\xrightarrow{F}
\text{flat coherent local system}.
\]

Pentagon cells kill path dependence on the associahedron.

### Layer B — exchange geometry

\[
\text{strand-labelled histories}
\xrightarrow{R}
\text{permutation-changing transports}.
\]

Hexagon cells tie exchange to fusion.

### Layer C — identical-particle quotient

\[
\text{strand-labelled groupoid}
\longrightarrow
\text{quotient by permutation identity}
\longrightarrow
\text{nontrivial braid holonomy}.
\]

This is the first version of the AEG/topological-order dictionary that survives the red-team checks:

\[
\boxed{
\begin{array}{rcl}
F&=&\text{local chart/reassociation transport},\\
pentagon&=&\text{flatness/coherence cell},\\
R&=&\text{local exchange transport},\\
hexagon&=&\text{fusion--exchange compatibility cell},\\
braid&=&\text{global path class after exchange quotient},\\
braid representation&=&\text{holonomy of the resulting flat local system}.
\end{array}}
\]

The word **flat** is important: nontrivial topological holonomy does not require nonzero local curvature. A flat connection on a non-simply-connected quotient can have nontrivial global holonomy.

**REFORMULATION.**

---

## 14. What has and has not been achieved

### Achieved

1. **COMPUTATIONAL-CLAIM:** symbolic R-family recovered from generic hexagon equations without inserting explicit standard Fibonacci phases.
2. **COMPUTATIONAL-CLAIM:** cyclotomic polynomial \(\Phi_{10}\) emerges by exact elimination.
3. **COMPUTATIONAL-CLAIM:** exact \(B_3\) and \(B_4\) braid relations verified in all small total-charge sectors.
4. **REFORMULATION:** a permutation-enriched history skeleton cleanly separates F-flatness from exchange holonomy.
5. **CLASSICAL originality audit:** this skeleton is closely related to the classical parenthesized braid groupoid/operad, so the bare construction is not new.
6. **COMPUTATIONAL-CLAIM / negative benchmark:** generator sparsity is \(O(d)\), but optimized categorical fusion-path methods obtain the same locality.

### Not achieved

1. No clean-room blind R reconstruction has been certified.
2. No new topological invariant has been found.
3. No asymptotic advantage over an optimized categorical compiler has been demonstrated.
4. No Levin--Wen/string-net operator has yet been compiled.
5. No general theorem identifying an AEG history complex with a parenthesized-braid operad/local system has been proved.

---

## 15. Next decisive experiment

The next useful question is no longer “can AEG recover Fibonacci F/R data?” It can represent and symbolically recover them, but this is classical structure.

The more discriminating benchmark is:

\[
\boxed{
\textbf{Can the explicit history IR compile and verify a nontrivial string-net/plaquette operator}
\textbf{ with a smaller or more auditable certificate than a direct categorical implementation?}
}
\]

Before the full Levin--Wen step, a smaller intermediate benchmark is advisable:

1. implement the general \(n\)-anyon local braid compiler without dense matrices;
2. represent a braid word as a sequence of local history blocks;
3. verify equality/reduction of braid words using local F/R/hexagon certificates;
4. compare certificate size and verification cost against a direct optimized fusion-path implementation;
5. only then move to string-net plaquette compilation.

The research burden has shifted from **recovering known constants** to **demonstrating a representation/verification advantage**.
