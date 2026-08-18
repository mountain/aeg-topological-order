# R(2,2) epsilon=-1 Uniform-Clifford Branch — Exact D/E Extension and F-Layer Obstruction

**Date:** 2026-08-17  
**Status:** exact branch exclusion / not a global categorifiability result

## 0. Scope

This note continues the finite-branch attack described in `notes/10-r22-localization-audit.md`.

Fix one concrete scalar A/B/C representative from the `(Z/2)^4` component inventory with

\[
\epsilon_X=\epsilon_Y=-1.
\]

On each of the eight multiplicity-two fusion spaces choose the same Clifford chirality, with stabilizer seed matrices represented by the Pauli triple

\[
L=X,\qquad M=Z,\qquad R=Y.
\]

The purpose is to decide whether this *one finite branch* extends to invertible F-data. It does not.

---

## 1. D layer: exact amplitude closure

The 24 Pauli stabilizer seeds satisfy all local involution and pairwise anticommutation pentagons.

The remaining 48 D-layer blocks each have a one-dimensional local intertwiner space with an invertible projective representative. Write

\[
D_j=t_j\widehat D_j,\qquad j=1,\ldots,48.
\]

Substituting these projective shapes into **all** D-layer pentagons yields 576 nonzero scalar residual equations. Every residual is binomial:

- 384 equations involve two amplitude variables;
- 192 equations involve four amplitude variables;
- right-hand sides are 368 copies of `1`, 112 copies of `-1`, and 96 copies of `i` in the chosen normalization.

Instead of a generic Smith-decomposition solve, encode

\[
t_j=\zeta_8^{u_j}
\]

and solve the integer congruence system modulo 8 by exact lifting

\[
\bmod 2\ \longrightarrow\ \bmod 4\ \longrightarrow\ \bmod 8.
\]

All lifts exist. One exact solution uses only

\[
\boxed{32\times1,\qquad8\times i,\qquad8\times(-1).}
\]

Thus this branch extends exactly through the complete D layer.

**COMPUTATIONAL-CLAIM.** This replaces the earlier numerical phase reconnaissance. No floating-point solve is needed for the D amplitude closure.

---

## 2. E layer: again projective shape plus root-of-unity amplitude

There are 32 E-layer `2 x 2` associator blocks.

For each block, the two local singleton pentagons produce eight entry equations of rank three. Hence every block has a one-dimensional projective solution space.

All 32 projective representatives are invertible. In the chosen gauge only two matrix shapes occur:

\[
\begin{pmatrix}-i&1\\ i&1\end{pmatrix},
\qquad
\begin{pmatrix}-i&-1\\ -i&1\end{pmatrix},
\]

both with determinant `-2 i`.

Write

\[
E_j=e_j\widehat E_j,\qquad j=1,\ldots,32.
\]

A dedicated sparse monomial IR evaluates all E-layer pentagons without expanding a 32-variable SymPy expression graph. The complete amplitude system contains

\[
\boxed{1280\text{ binomial equations},}
\]

all with support two. Their exponent matrix has

\[
\boxed{\operatorname{rank}=30,\qquad\operatorname{nullity}=2.}
\]

The right-hand sides are powers of `i`. Exact lifting modulo four gives a solution with amplitude counts

\[
\boxed{16\times1,\qquad8\times i,\qquad8\times(-i).}
\]

Thus the fixed branch extends exactly through E as well.

---

## 3. F layer: weighted equality graph

The remaining noninvertible-output associators are the 16 F-layer blocks:

- eight `8 x 8` blocks;
- eight `10 x 10` blocks;
- 1312 scalar entries total.

After the exact A--E data above are fixed, the 192 F-layer pentagon blocks produce

\[
\boxed{15744\text{ nonzero scalar linear equations}.}
\]

Every equation has support exactly two. Coefficients lie in

\[
\{\pm1,\pm i\},
\]

so each equation is a weighted identification

\[
x_j=i^r x_k,\qquad r\in\mathbb Z/4.
\]

Therefore the F layer is a weighted graph problem rather than a general linear solve.

### 3.1 Exact component structure

Over the exact `mu_4` weights, the 1312 F entries form 21 connected components:

\[
20\times64,\qquad1\times32.
\]

Five components contain inconsistent weighted cycles. Since the equations are homogeneous, every entry in those components is forced to zero.

The remaining 16 components provide the unconstrained linear parameters. Equivalently,

\[
\boxed{\operatorname{rank}=1296,\qquad\operatorname{nullity}=16.}
\]

A modular calculation over a prime with a square root of `-1` gives the same rank, but the component description is characteristic-zero and is the preferred certificate.

### 3.2 Exact rank obstruction in every 10 x 10 block

In every one of the eight `10 x 10` F-blocks, the entries in rows 0 and 1 belong to forced-zero components. The same is true for columns 0 and 1.

Thus each such associator has the exact form

\[
F=\begin{pmatrix}
0&0&\cdots&0\\
0&0&\cdots&0\\
\vdots&\vdots&*&\vdots\\
0&0&\cdots&*
\end{pmatrix},
\]

so

\[
\boxed{\operatorname{rank}F\le8<10.}
\]

The two killed basis directions are the fusion paths through the two invertible intermediate channels `1` and `h` in the canonical path ordering.

For comparison, the eight `8 x 8` blocks admit full-rank samples under the same linear constraints; the obstruction is specifically the required 10-dimensional associators.

**BRANCH OBSTRUCTION.** The chosen epsilon=-1, uniform-Clifford-chirality branch cannot define a fusion category because pentagon coherence forces required associators to be noninvertible.

---

## 4. What this excludes and what it does not

This is stronger than a failed nonlinear solve: the branch is killed by a finite sequence of exact local extensions followed by a linear weighted-cycle obstruction.

It does **not** prove that `R(2,2)` is not categorifiable.

Remaining branch axes include:

1. the other scalar A/B/C components in the 16-component inventory;
2. Clifford chirality assignments on the eight multiplicity-two fusion spaces;
3. the commuting `epsilon=+1` D regime and its discrete character data.

A seed-only chirality audit shows that all `2^8=256` chirality assignments satisfy the purely local Clifford seed pentagons. A precompiled modular scan of the 48 cross-space D intertwiner systems likewise finds rank-three, invertible projective solutions for all 256 assignments. Thus chirality pruning must occur at amplitude closure or at E/F consistency, not at the seed/projective-D level.

The next experiment should batch the finite chirality assignments through sparse D-amplitude, E-amplitude, and F weighted-graph filters before considering any final four-noninvertible pentagon kernel.
