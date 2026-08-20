# R(2,2) theorem audit — second D sheet, component 13 / mask 255 Phase-5 closure

## Status

**CLOSED / EXACT.**

This is the final previously unresolved branch on the second physical D-amplitude sheet.

## Fresh class-1 local model

The fresh Phase-5 kernel has

- 21 F-linear components;
- 23 nonlinear variables;
- 50,880 raw nonzero final entries;
- 219 exact cubic kernel relations;
- no generic constant contradiction.

Five fixed final-pentagon source cells give, before any localization,

\[
\boxed{z_3^2=\frac12},
\qquad
\boxed{p^3=q^3=\frac{1-i}{4}},
\]

\[
\boxed{z_0z_4=-i q^2 z_3},
\qquad
\boxed{z_{17}z_{18}=-i p^2 z_3}.
\]

The scale equation is obtained from the literal pre-localization identity

\[
P_5-P_3+P_2=\frac{1+i}{4}\left(z_3^2-\frac12\right),
\]

so the subsequent divisions use only proved-nonzero variables.

## Finite census

The exact 18 finite branches split as

\[
\boxed{18=2_{\rm affine}+4_{\rm p-rank11}+4_{\rm q-rank11}+8_{\rm rank10}}.
\]

The p-side rank-11 branches force `z7=z8=0`; the q-side rank-11 branches force `z13=z14=0`.  The rank-10 branches have free set

```text
z0,z5,z6,z9,z10,z17,z19,z20
```

with residual two-variable core `(r,s)=(z19,z20)`.

## Terminal certificates

The four p-side rank-11 branches are excluded by the fixed cell

```text
(XXXXX)_(5,2)
```

which reduces to an exact nonzero constant on every branch.

The four q-side rank-11 branches are excluded by the fixed cell

```text
(XXXX;Y)_(0,1)
```

which likewise reduces to an exact nonzero constant on every branch.

For all eight rank-10 branches use the fixed cells

```text
(XXXX;g)_(0,3)
(XXXX;g)_(0,2)
(XXXX;g)_(0,1)
```

in the `(r,s)=(z19,z20)` core.  The first two have the symmetric form

\[
C+A s^2+B rs=0,
\qquad
C+A r^2+B rs=0,
\qquad A\ne0,
\]

hence

\[
r^2=s^2.
\]

On every branch the two exact slices are

\[
r=s:\quad s^2=\frac{i}{8},
\qquad
r=-s:\quad s^2=\frac18,
\]

and the fixed third cell is nonzero on both slices.

Thus

\[
\boxed{18/18\text{ finite branches are excluded}.}
\]

The terminal verifier is

```text
experiments/r22_phase5_component13_torsion_mask255_terminal_certificate.py
```

and GitHub Actions run `32393826437` is `SUCCESS` with

```text
affine_inconsistent = 2
p_rank11_closed      = 4
q_rank11_closed      = 4
rank10_closed        = 8
finite_total         = 18
```

## Consequence

Component `13` is now closed on all four masks `0,105,150,255` on the second D-amplitude sheet.  Since components `5,7,15` were already closed on all four masks, the entire second physical D-amplitude sheet is Phase-5 closed.

This does **not** yet promote the global non-categorifiability theorem.  The next theorem-completeness gate is the exact completeness of the Pauli/Clifford seed normal form used before the chirality census.
