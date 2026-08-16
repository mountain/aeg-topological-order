# Blind Fibonacci reconstruction — T0 input freeze through the pentagon solve

**Date:** 2026-08-17  
**Status:** blind reconstruction result; standard-value comparison gate remains closed  
**Implementation:** `experiments/fibonacci_pentagon.py`

## 0. Result in one line

**COMPUTATIONAL-CLAIM.** Starting only from the multiplicity-free fusion grammar

\[
1\otimes x=x\otimes1=x,\qquad \tau\otimes\tau=1\oplus\tau,
\]

strict-unit normalization, invertibility of the associator, and pentagon coherence, the four-\(\tau\) history complex forces the nondegenerate local associator data to satisfy

\[
\boxed{g=1,\qquad d=-a,\qquad bc=a,\qquad a^2+a-1=0.}
\]

**COMPUTATIONAL-CLAIM.** Adding unitarity *after* this algebraic solve selects

\[
\boxed{a=\frac{\sqrt5-1}{2}}
\]

and a vertex-gauge choice can make the nontrivial \(2\times2\) block real symmetric,

\[
\boxed{
F^{\tau\tau\tau}_{\tau}
\sim
\begin{pmatrix}
a&\sqrt a\\
\sqrt a&-a
\end{pmatrix}.}
\]

**CLASSICAL.** This recovered datum is standard fusion-category structure, not a candidate new invariant. The research question is whether the *history-complex representation and its compilation/benchmark behavior* later provide structural or computational value beyond the categorical formulation.

---

## 1. T0 — frozen input grammar

### 1.1 Allowed during the blind monoidal solve

**CLASSICAL.** The simple labels are \(\{1,\tau\}\), with vacuum \(1\).

**CLASSICAL.** Fusion is multiplicity-free and is fixed only by

\[
1\otimes x=x\otimes1=x,
\qquad
\tau\otimes\tau=1\oplus\tau.
\]

**CLASSICAL.** Fusion-tree spaces are built from admissible trivalent channels. No multiplicity index is needed because every \(N_{ab}^{c}\in\{0,1\}\).

**CLASSICAL.** We use strict-unit / triangle normalization: an associator with a vacuum among its three simple inputs is the identity.

**CLASSICAL.** Nontrivial associators are required to be invertible and satisfy the pentagon identity.

### 1.2 Deferred until after the algebraic pentagon solve

**CLASSICAL.** Unitarity is *not* used to derive the polynomial pentagon solutions. It is applied only as a second-stage selection criterion.

**CLASSICAL.** Pivotal, spherical, twist, braiding, \(R\)-symbol, and hexagon data are not used in this note.

### 1.3 Forbidden reconstruction inputs

**CLASSICAL.** No known numerical Fibonacci \(F\)- or \(R\)-symbols are allowed as inputs.

**CLASSICAL.** No known Fibonacci quantum dimension, golden-ratio identity, braid phase, modular data, or preferred standard gauge is used as an input.

**COMPUTATIONAL-CLAIM.** The implementation contains only the fusion grammar above plus symbolic variables; the radical \(\sqrt5\) appears only after solving the generated polynomial relation.

---

## 2. AEG/history interpretation used here

**REFORMULATION.** A parenthesized fusion tree is treated as an explicit operation history rather than quotienting all parenthesizations immediately by coherence.

**REFORMULATION.** A history vertex carries a vector-valued fiber whose basis is the set of admissible intermediate-channel assignments for that parenthesization and fixed total charge.

**REFORMULATION.** A single reassociation

\[
((A B)C)\longrightarrow(A(BC))
\]

is an oriented edge carrying the corresponding local \(F\)-transport.

**REFORMULATION.** The associahedral pentagon is a 2-cell, and the pentagon axiom is exactly the statement that the two boundary paths from the same source history to the same target history define the same linear transport.

**CLASSICAL.** This is a flatness/coherence statement. A nontrivial \(F\)-move by itself is not nonzero curvature.

**AEG-UPSTREAM.** The useful upstream analogy is the explicit path/transport/holonomy viewpoint in `mountain/aeg-paper/notes/foundations-and-geometry/04-affine-torus-holonomy.tex`, blob `de501e888110f887815328ae4524c602698e6a38`. That note is used only as methodological calibration; its affine commutator geometry is not imported into the fusion problem.

**AEG-UPSTREAM.** `mountain/three-body/docs/note_04.md`, blob `6d7c5198df5fdb782a03dd7b342a4aa057bc039c`, and `docs/note_05.md`, blob `023dab383fec9375dd02fc2b7f1823144c685f41`, are used for the methodological rule that ruler/representation rank must be diagnosed from the problem rather than postulated. No three-body-specific \(SL(2,\mathbb R)/SO(2)\) geometry is imported here.

---

## 3. T1/T2 — generated histories and vector-valued fibers

**COMPUTATIONAL-CLAIM.** Exact enumeration for \(n=3,4,5\) identical \(\tau\) inputs gives:

| \(n\) | parenthesizations | \(\dim V^{\tau^n}_{1}\) | \(\dim V^{\tau^n}_{\tau}\) |
|---:|---:|---:|---:|
| 3 | 2 | 1 | 2 |
| 4 | 5 | 2 | 3 |
| 5 | 14 | 3 | 5 |

**CLASSICAL.** The parenthesization counts are Catalan numbers; the fiber dimensions follow the Fibonacci fusion recurrence.

**REFORMULATION.** The first genuinely vector-valued AEG history fibers already appear for three \(\tau\)'s with total charge \(\tau\), where the local fiber is two-dimensional.

**REFORMULATION.** For four \(\tau\)'s the five parenthesizations form the vertices of the associahedral pentagon. Each vertex has a 2-dimensional fiber in total channel \(1\) and a 3-dimensional fiber in total channel \(\tau\).

---

## 4. Blind symbolic local data

**CLASSICAL.** Under strict-unit normalization, only two all-\(\tau\) associators can be nontrivial.

**COMPUTATIONAL-CLAIM.** For total charge \(1\), write the unique scalar as

\[
F^{\tau\tau\tau}_{1}=g.
\]

**COMPUTATIONAL-CLAIM.** For total charge \(\tau\), with old and new intermediate channels ordered by \((1,\tau)\), write

\[
F^{\tau\tau\tau}_{\tau}
=
\begin{pmatrix}
a&b\\c&d\end{pmatrix}.
\]

**CLASSICAL.** A vertex-frame change rescales the two trivalent bases. In this multiplicity-free case the two off-diagonal entries \(b,c\) rescale reciprocally, while \(a,d,g\) and the product \(bc\) are invariant under normalized vertex gauge.

---

## 5. Four-anyon pentagon as sparse local transport

Use the five parenthesizations

\[
\begin{aligned}
P_0&=(((ab)c)d),\\
P_1&=((a(bc))d),\\
P_2&=(a((bc)d)),\\
P_3&=(a(b(cd))),\\
P_4&=((ab)(cd)).
\end{aligned}
\]

**CLASSICAL.** Pentagon coherence is

\[
M_{23}M_{12}M_{01}=M_{43}M_{04}.
\]

### 5.1 Total charge \(1\)

**COMPUTATIONAL-CLAIM.** In the basis generated by the script,

\[
M_{01}=M_{23}=
\begin{pmatrix}a&c\\b&d\end{pmatrix},
\qquad
M_{12}=M_{04}=M_{43}=
\begin{pmatrix}1&0\\0&g\end{pmatrix}.
\]

**COMPUTATIONAL-CLAIM.** The path difference is

\[
\Delta_1=
\begin{pmatrix}
a^2+bcg-1 & c(a+dg)\\
b(a+dg) & bc+d^2g-g^2
\end{pmatrix}.
\]

### 5.2 Total charge \(\tau\)

**COMPUTATIONAL-CLAIM.** The generated edge matrices are

\[
M_{01}=M_{23}=
\begin{pmatrix}
g&0&0\\0&a&c\\0&b&d\end{pmatrix},
\]

\[
M_{12}=M_{43}=
\begin{pmatrix}
a&0&c\\0&1&0\\b&0&d\end{pmatrix},
\qquad
M_{04}=
\begin{pmatrix}
0&1&0\\a&0&c\\b&0&d
\end{pmatrix}.
\]

**COMPUTATIONAL-CLAIM.** The path difference is

\[
\Delta_{\tau}=
\begin{pmatrix}
a g^2-bc & -a+bcg & cd(g-1)\\
-a+bcg & a^2+bcd & c(a+d^2-1)\\
bd(g-1) & b(a+d^2-1) & bc+d^3-d^2
\end{pmatrix}.
\]

**COMPUTATIONAL-CLAIM.** Setting \(\Delta_1=0\) and \(\Delta_{\tau}=0\) produces twelve nonzero polynomial entries before algebraic dependency reduction.

---

## 6. Exact nondegenerate solve

**COMPUTATIONAL-CLAIM.** From

\[
a=bcg
\]

and invertibility of the \(2\times2\) associator block, \(bc\neq0\); otherwise \(a=0\) and the determinant vanishes.

**COMPUTATIONAL-CLAIM.** Hence \(b\neq0\) and \(c\neq0\), so the equations

\[
b(a+dg)=c(a+dg)=0
\]

force

\[
a+dg=0.
\]

**COMPUTATIONAL-CLAIM.** The equations

\[
bd(g-1)=cd(g-1)=0
\]

together with nondegeneracy rule out \(d=0\), and therefore force

\[
g=1.
\]

**COMPUTATIONAL-CLAIM.** It follows that

\[
d=-a,\qquad bc=a.
\]

**COMPUTATIONAL-CLAIM.** The remaining equation

\[
a^2+bcg-1=0
\]

reduces to

\[
\boxed{a^2+a-1=0.}
\]

**COMPUTATIONAL-CLAIM.** Consequently

\[
\det F^{\tau\tau\tau}_{\tau}=ad-bc=-a^2-a=-1,
\]

so both algebraic roots are nondegenerate monoidal solutions at this stage.

**COMPUTATIONAL-CLAIM.** The script independently substitutes

\[
g=1,\quad d=-a,\quad c=a/b,\quad a^2+a-1=0
\]

back into both sector path differences and verifies exact vanishing.

---

## 7. Unitary selection, still without a known Fibonacci table

**CLASSICAL.** In a unitary fusion category, an \(F\)-move written in orthonormal trivalent bases is unitary.

**COMPUTATIONAL-CLAIM.** The two exact roots are

\[
a_{\pm}=\frac{-1\pm\sqrt5}{2}.
\]

**COMPUTATIONAL-CLAIM.** The entry \(a\) is vertex-gauge invariant in the normalized convention. Since every entry of a unitary matrix has modulus at most \(1\), the root with modulus greater than \(1\) cannot admit a unitary representative.

**COMPUTATIONAL-CLAIM.** The surviving root is therefore

\[
\boxed{a=\frac{\sqrt5-1}{2}}.
\]

**COMPUTATIONAL-CLAIM.** Unitarity then gives

\[
|b|^2=|c|^2=a,
\qquad c=\overline b,
\]

and the remaining phase is removable by normalized vertex gauge.

**COMPUTATIONAL-CLAIM.** Thus a real symmetric orthogonal gauge exists with

\[
b=c=\sqrt a,
\]

and the script verifies exactly that

\[
\begin{pmatrix}a&\sqrt a\\\sqrt a&-a\end{pmatrix}^{T}
\begin{pmatrix}a&\sqrt a\\\sqrt a&-a\end{pmatrix}=I.
\]

**CLASSICAL.** This completes the blind \(F\)-reconstruction up to gauge. It does not yet constitute a comparison against a published Fibonacci table; that comparison remains a separate gate.

---

## 8. What this says about the AEG hypothesis

**REFORMULATION.** The history-complex language is mathematically faithful at the first nontrivial benchmark: vector-valued fibers, local reassociation transports, vertex gauge, and pentagon 2-cell flatness all line up exactly with their categorical counterparts.

**CLASSICAL.** This faithfulness is not by itself a new theorem about topological order; it is a concrete realization of ordinary associator coherence.

**COMPUTATIONAL-CLAIM.** The sparse history engine recovers the full nontrivial Fibonacci associator from five symbolic variables and local edge composition without using a pre-tabulated \(F\)-matrix.

**REFORMULATION.** The useful object retained by AEG at this point is the *explicit rewrite complex plus its local system*, not a new scalar curvature.

**CONJECTURE.** The explicit-history representation may become computationally useful when larger fusion rings make global pentagon systems sparse and highly local, but the four-anyon Fibonacci example is too small to establish a complexity advantage.

**COMPUTATIONAL-CLAIM.** No compression claim is made yet. An optimized categorical formulation begins from the same five symbolic degrees of freedom \((a,b,c,d,g)\), so variable count alone does not favor the history representation in this benchmark.

---

## 9. Red-team conclusions

**CLASSICAL.** Question: “Does AEG merely redraw a fusion category as a graph?”  
**REFORMULATION.** Current answer: at T0–T3, largely yes—except that the graph is more precisely a vector-valued local system on an associahedral rewrite complex, not merely a picture of objects.

**CLASSICAL.** Question: “Is pentagon curvature?”  
**REFORMULATION.** Answer: no. Satisfied pentagon cells are flat/coherent cells. Calling the nontrivial \(F\)-matrix itself curvature would be incorrect.

**CLASSICAL.** Question: “Did the representation derive anything not already known categorically?”  
**COMPUTATIONAL-CLAIM.** Answer: it derived the known algebraic data from the allowed grammar, but no new gauge-invariant topological datum has appeared.

**CLASSICAL.** Question: “Is there already a computational gain?”  
**COMPUTATIONAL-CLAIM.** Answer: not demonstrated. The next experiment must compare against a direct symbolic categorical baseline rather than against a deliberately naive dense formulation.

---

## 10. Next tasks

**COMPUTATIONAL-CLAIM.** Freeze this note and script as the blind result before any standard-value comparison.

**CLASSICAL.** Next gate: compare the derived \(F\)-family to a standard Fibonacci reference and record convention/gauge matching explicitly.

**COMPUTATIONAL-CLAIM.** Implement an independent direct categorical pentagon baseline using the same fusion grammar and normalization, then compare:

- symbolic variables before gauge reduction;
- nonzero equations and algebraic dependencies;
- polynomial monomial count / expression size;
- exact solve time;
- verification time.

**REFORMULATION.** Extend the history generator from the \(K_4\) pentagon to the full \(K_5\) associahedron for five inputs, including its pentagonal and square 2-cells, and verify path independence from local cells.

**CLASSICAL.** Only after the \(F\)-comparison gate is closed should the project proceed to \(R\)-symbols and hexagon reconstruction.

---

## 11. Source discipline

**CLASSICAL.** Willie Aboumrad, *Quantum computing with anyons: an F-matrix and braid calculator*, arXiv:2212.00831. Used for multiplicity-free fusion-space conventions, the role of the pentagon equations, and the direct-solver baseline concept. Numerical Fibonacci \(F/R\) values from comparison literature are not used here.

**CLASSICAL.** Michael A. Levin and Xiao-Gang Wen, *String-net condensation: A physical mechanism for topological phases*, arXiv:cond-mat/0404617. Comparison/later-stage source for the string-net program only; not used in this blind \(F\)-solve.

**AEG-UPSTREAM.** `mountain/aeg-paper/notes/foundations-and-geometry/04-affine-torus-holonomy.tex`, blob `de501e888110f887815328ae4524c602698e6a38`.

**AEG-UPSTREAM.** `mountain/three-body/docs/note_04.md`, blob `6d7c5198df5fdb782a03dd7b342a4aa057bc039c`.

**AEG-UPSTREAM.** `mountain/three-body/docs/note_05.md`, blob `023dab383fec9375dd02fc2b7f1823144c685f41`.
