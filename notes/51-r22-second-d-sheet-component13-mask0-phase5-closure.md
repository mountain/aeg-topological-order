# R(2,2) theorem audit — component 13 / mask 0 / D class 1 Phase-5 closure

**Status:** `CLOSED / EXACT / second physical D-amplitude sheet`

This note records the complete fresh Phase-5 closure of scalar component `13`,
chirality mask `0`, on the second gauge-inequivalent D-amplitude sheet found by
the theorem audit.

No historical component-13 coordinate identification is assumed.  The class-1
kernel, local scale relations, finite branch census, and terminal source cells
are all replayed from fresh state.  No Gröbner basis or global nonlinear solve is
used.

## 1. Fresh nonlinear kernel

Actions run `32363936787` fresh-compiles all 96 final pentagon blocks and gives:

- 21 active F-linear components;
- 23 kernel variables `p,q,z0,...,z20`;
- 56,448 final scalar positions;
- 50,880 raw nonzero final entries;
- 219 unique exact cubic kernel polynomials;
- F-degree profile `57 x degree-2 + 162 x degree-3`;
- no generic constant contradiction.

Thus the macroscopic kernel size agrees with the historical D sheet, but this is
not used as an identification.

## 2. Five source-validated local relations

The fixed source cells are

```text
P1 = (X,X,X,X,X)_(0,0)
P2 = (X,X,X,X,X)_(0,2)
P3 = (X,X,X,X,Y)_(0,18)
P4 = (X,X,X,X,Y)_(18,18)
P5 = (X,X,X,X,1)_(0,0)
```

The class-1 kernel gives exactly

\[
p^2z_5+i z_0z_6=0,
\]
\[
pz_0z_6+\frac{1-i}{4}z_5=0,
\]
\[
qz_{12}z_{16}+\frac{1-i}{4}z_5=0,
\]
\[
q^2z_5+z_{12}z_{16}=0.
\]

Before any localization, the literal polynomial combination

\[
P_5-P_2+P_3
=\frac{1-i}{8}(1-2z_5^2)
\]

gives

\[
\boxed{z_5^2=\frac12}.
\]

Hence `z5 != 0`.  Only after this nonzeroness is proved, the combinations

\[
pP_1-iP_2=z_5\left(p^3-\frac{1+i}{4}\right),
\]
\[
qP_4-P_3=z_5\left(q^3-\frac{1-i}{4}\right)
\]

give

\[
\boxed{p^3=\frac{1+i}{4}},\qquad
\boxed{q^3=\frac{1-i}{4}}.
\]

The product identities are

\[
\boxed{z_0z_6=i p^2z_5},
\qquad
\boxed{z_{12}z_{16}=-q^2z_5}.
\]

Thus

\[
p,q,z_0,z_5,z_6,z_{12},z_{16}\ne0.
\]

Actions run `32364289954` source-validates all five cells and the three polynomial
combinations.

## 3. Exact finite census

The local scale sector has exactly

\[
3\times3\times2=18
\]

branches.  The class-1 census eliminates only `z6` and `z16` via the proved
product identities and localizes only at proved-nonzero `z0,z12`.

Actions run `32364558701` gives the exact split

\[
\boxed{18=2+4+4+8}.
\]

More precisely:

- 2 branches `(a,b)=(0,0)`, both signs, are affine-inconsistent;
- 4 p-side branches `(1,0),(2,0)` have rank 11 and force `z13=z14=0`;
- 4 q-side branches `(0,1),(0,2)` have rank 11 and force `z7=z8=0`;
- 8 branches `(1,1),(2,1),(1,2),(2,2)`, both signs, have rank 10 and no forced zero.

The rank-10 free chart is

```text
z0,z10,z11,z12,z15,z18,z19,z20.
```

This reproduces the historical `2+4+4+8` relation-space stratification while
moving the named coordinate chart.

## 4. Rank-11 terminal cells

A fresh representative residual probe (`32364916408`) shows that the historical
provenance positions survive but attach to the class-1 nonzero scales.

### p-side

For all four p-rank11 branches,

```text
(X,X,X,X;Y)_(1,0)
```

reduces to

\[
c\,z_0=0,\qquad c\ne0.
\]

Since `z0 != 0`, all four branches are impossible.

### q-side

For all four q-rank11 branches,

```text
(X,X,X,X;X)_(5,2)
```

reduces to

\[
c\,z_{12}=0,\qquad c\ne0.
\]

Since `z12 != 0`, all four branches are impossible.

## 5. Rank-10 three-cell certificate

On every rank-10 branch set

\[
r=z_{18},\qquad s=z_{19}.
\]

The fixed source cells

```text
G0 = (X,X,X,X;g)_(0,0)
G2 = (X,X,X,X;g)_(0,2)
G3 = (X,X,X,X;g)_(0,3)
```

satisfy

\[
G_2-G_3=A(r^2-s^2),\qquad A\ne0.
\]

Thus any common zero has `r=+s` or `r=-s`.  On each sign slice the exact source
remainder of `G0` is

\[
H s^2,
\qquad H\ne0,
\]

so `s=0` and hence `r=0`.  But on both sign slices `G2` retains a nonzero exact
constant term, giving an immediate contradiction.

Actions run `32365233091` verifies this independently on all eight rank-10
branches and also rechecks all eight rank-11 branches.  Its final ledger is

```text
affine_inconsistent = 2
p_rank11_closed      = 4
q_rank11_closed      = 4
rank10_closed        = 8
finite_total         = 18
```

## 6. Closure

Therefore every finite Phase-5 branch is excluded:

\[
\boxed{\text{component 13 / mask 0 / D class 1 is CLOSED / EXACT}.}
\]

The second D sheet now has 13 of its 16 deep Phase-5 branches closed.  The only
remaining branches are scalar component `13`, masks `105,150,255`.
