# R(2,2) component 13 / mask 255 — Phase-5 exact closure

## Status

**CLOSED / EXACT.**

For scalar component `13` and chirality mask `255`, there is no invertible associator extension satisfying the final four-noninvertible pentagons.

This closure is a fully fresh mask-255 replay. No coordinate identification, scale relation, finite-stratum split, or local certificate from masks `0`, `105`, or `150` is assumed. No Gröbner basis, floating-point root search, numerical continuation, or global nonlinear solver is used.

## 1. Fresh Phase-5 kernel

The exact sparse compiler gives:

- 96 final pentagon blocks;
- block dimensions `32 x 10`, `32 x 8`, `32 x 40`;
- 56,448 scalar positions;
- 50,880 raw nonzero final entries;
- 2 E parameters and 21 F-linear components;
- 23 kernel variables `p,q,z0,...,z20`;
- 15,744 support-two F-linear equations before the kernel quotient;
- 219 unique kernel polynomials;
- all 219 have total degree 3;
- F-degree profile `57` of degree 2 and `162` of degree 3;
- no generic constant contradiction.

Fresh kernel replay: GitHub Actions run `32220170567`.

The named F coordinates were independently reconstructed under

```text
PYTHONHASHSEED = 1, 2, 17
```

and gave a single partition and a single fixed-target polynomial across all three processes. Thus the named `z_j` coordinates used below are reproducible with respect to the tested union-find/hash ordering.

Coordinate-stability replay: GitHub Actions run `32220367043`.

## 2. Exact local scale relations

Five fixed pentagon provenances were recompiled directly:

```text
P1 = (XXXXX)_(0,0)
P2 = (XXXXX)_(0,2)
P3 = (XXXXY)_(0,18)
P4 = (XXXXY)_(18,18)
P5 = (XXXX;1)_(0,0)
```

Their exact polynomial combinations give, before unsafe division,

\[
\boxed{z_3^2=\frac12}.
\]

Hence `z3 != 0`. The same local system then gives

\[
\boxed{p^3=\frac{1-i}{4}},
\qquad
\boxed{q^3=\frac{-1+i}{4}},
\]

and the product relations

\[
\boxed{z_0z_4=i q^2z_3},
\qquad
\boxed{z_{17}z_{18}=-i p^2z_3}.
\]

Therefore

\[
\boxed{p,q,z_0,z_3,z_4,z_{17},z_{18}\ne0}.
\]

Source validator:

```text
experiments/r22_phase5_component13_mask255_local_relations.py
```

GitHub Actions run `32220734053` verifies the five provenance relations and these exact consequences.

## 3. Finite algebraic stratification

Since `p` and `q` each have three cube-root choices and `z3` has two square-root choices, the continuous scale sector collapses to

\[
3\times3\times2=18
\]

exact algebraic branches.

After eliminating the product variables only through the proved-nonzero identities above and stripping Laurent factors only in proved-nonzero scales, the exact affine census is

\[
\boxed{
18
=
2_{\rm affine}
+4_{\rm p\text{-}rank11}
+4_{\rm q\text{-}rank11}
+8_{\rm rank10}.
}
\]

The branches are:

- `(a,b)=(0,0)`, both `z3` signs: affine-inconsistent;
- p-side `(a,b)=(1,0),(2,0)`, both signs: affine rank 11 with `z7=z8=0`;
- q-side `(a,b)=(0,1),(0,2)`, both signs: affine rank 11 with `z13=z14=0`;
- mixed `(a,b)=(1,1),(2,1),(1,2),(2,2)`, both signs: affine rank 10 with no forced zero.

Finite census:

```text
experiments/r22_phase5_component13_mask255_finite_census.py
```

GitHub Actions run `32220954013` records the complete 18-branch census.

## 4. The rank-11 forced zeros are not F-singularity certificates

Both rank-11 zero patterns were checked against every required Phase-4 `8x8/10x10` F determinant polynomial:

```text
p-side: z7=z8=0
q-side: z13=z14=0
```

Neither pattern kills all determinant monomials in any required block. The minimum surviving determinant support is 123 monomials. Thus these strata cannot be discarded by invertibility alone; final pentagon equations are required.

Independent gate:

```text
experiments/r22_phase5_component13_mask255_forced_zero_invertibility.py
```

GitHub Actions run `32221178582` verifies this negative invertibility result.

## 5. Four p-side rank-11 branches — one pure constant cell

The representative branch `(a,b,z3-sign)=(1,0,+)` was fully substituted through the affine quotient. Its residual system contains one exact nonzero constant at

```text
(XXXX;X)_(5,2).
```

The same fixed cell was then replayed independently on

```text
(1,0,+), (1,0,-), (2,0,+), (2,0,-).
```

In every branch the residual is an explicit nonzero element of

\[
K=\mathbf Q(i,\sqrt2,\sqrt3),
\]

so the pentagon equation is literally

\[
\boxed{c=0,\qquad c\ne0}.
\]

Representative residual run: `32221373384`.

Four-branch certificate:

```text
experiments/r22_phase5_component13_mask255_p_rank11_certificate.py
```

GitHub Actions run `32221558933` reports

```text
closed = 4
total  = 4
```

for the fixed cell `(XXXX;X)_(5,2)`.

## 6. Four q-side rank-11 branches — a second pure constant cell

The q-side representative `(0,1,+)` has a pure nonzero constant at

```text
(XXXX;Y)_(0,1).
```

That same provenance was replayed on

```text
(0,1,+), (0,1,-), (0,2,+), (0,2,-),
```

and is nonzero in every case.

Representative residual run: `32221780288`.

Four-branch certificate:

```text
experiments/r22_phase5_component13_mask255_q_rank11_certificate.py
```

GitHub Actions run `32221977484` reports

```text
closed = 4
total  = 4
```

for the fixed cell `(XXXX;Y)_(0,1)`.

## 7. Eight rank-10 branches — universal three-cell certificate

For the representative `(a,b,z3-sign)=(1,1,+)`, the exact affine quotient leaves a low-dimensional residual core supported only on

\[
(r,s)=(z_{19},z_{20}).
\]

Use the fixed three `g`-cells

```text
P1 = (XXXX;g)_(0,3)
P2 = (XXXX;g)_(0,2)
P3 = (XXXX;g)_(0,1)
```

The first two have identical constant and `rs` coefficients. Their exact difference is

\[
\boxed{A(s^2-r^2)=0},
\qquad A\ne0.
\]

Hence

\[
\boxed{r=s\quad\text{or}\quad r=-s}.
\]

On the representative branch the two slices are

\[
r=s:\qquad s^2=\frac{i}{8},
\]

\[
r=-s:\qquad s^2=\frac18.
\]

The fixed third cell `P3` evaluates to a nonzero exact element of `K` on both slice points.

Representative probe:

```text
experiments/r22_phase5_component13_mask255_rank10_probe.py
```

GitHub Actions run `32222519484` verifies the representative three-cell certificate.

The identical three provenances were then replayed independently on all eight rank-10 branches:

```text
(1,1,+), (1,1,-),
(2,1,+), (2,1,-),
(1,2,+), (1,2,-),
(2,2,+), (2,2,-).
```

For every branch:

1. `P1-P2` is a nonzero scalar multiple of `s^2-r^2`;
2. the `r=s` slice gives `s^2=i/8`;
3. the `r=-s` slice gives `s^2=1/8`;
4. the fixed third cell `P3` is nonzero on both exact slice points.

Eight-branch certificate:

```text
experiments/r22_phase5_component13_mask255_rank10_certificate.py
```

GitHub Actions run `32222771962` reports

```text
closed = 8
total  = 8
```

with the same three fixed `g` cells on every branch.

## 8. Final accounting

All 18 finite branches are excluded:

\[
\boxed{
18
=
2_{\rm affine}
+4_{\rm p\text{-}rank11}
+4_{\rm q\text{-}rank11}
+8_{\rm rank10}
=
18_{\rm closed}.
}
\]

Therefore

\[
\boxed{
\text{component 13 / chirality mask 255 has no invertible Phase-5 associator extension.}
}
\]

Equivalently,

\[
\boxed{\text{component 13 / mask 255 is non-categorifiable}.}
\]

## 9. Consequence for scalar component 13

Masks

\[
\boxed{0,105,150,255}
\]

have now each been independently replayed and exactly excluded at Phase 5.

Hence scalar component `13` as a whole is closed. The separate component-level synthesis is archived in

```text
notes/36-r22-component13-phase5-closure.md
```

The next unresolved deep scalar components are `7` and `15`.