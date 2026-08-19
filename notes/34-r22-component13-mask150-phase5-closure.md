# R(2,2) component 13 / mask 150 — Phase-5 exact closure

## Status

**CLOSED / EXACT.**

For scalar component `13` and chirality mask `150`, there is no invertible associator extension satisfying the final four-noninvertible pentagons.

This closure was obtained by a fresh mask-150 replay.  No mask-0 or mask-105 coordinate identification, finite-stratum split, or final local certificate was assumed.  No Gröbner basis, floating-point root search, numerical continuation, or global nonlinear solver was used.

## 1. Fresh Phase-5 kernel

The fresh exact sparse compiler gives:

- 96 final pentagon blocks;
- block dimensions `32 x 10`, `32 x 8`, `32 x 40`;
- 56,448 scalar positions;
- 50,880 raw nonzero final entries;
- 2 E parameters and 21 F-linear components;
- 23 kernel variables `p,q,z0,...,z20`;
- 15,744 support-two F-linear equations before the kernel quotient;
- 219 unique kernel polynomials;
- all 219 polynomials have total degree 3;
- F-degree profile `57` of degree 2 and `162` of degree 3;
- no generic constant contradiction.

The current named `z_j` coordinates were independently checked under

```text
PYTHONHASHSEED = 1, 2, 17
```

and gave one F-component partition and one fixed-target polynomial in all three processes:

```text
partition_variants = 1
target_variants    = 1
```

Thus all named-coordinate certificates below are reproducible with respect to the tested union-find/hash ordering.

## 2. Exact local scale relations

Five fixed pentagon provenances were recompiled and validated directly:

```text
P1 = (XXXXX)_(0,0)
P2 = (XXXXX)_(0,2)
P3 = (XXXXY)_(0,18)
P4 = (XXXXY)_(18,18)
P5 = (XXXX;1)_(0,0)
```

With

\[
D=\frac{1-i}{4},
\]

they are proportional to

\[
P_1:\quad p^2z_6+z_0z_9=0,
\]

\[
P_2:\quad pz_0z_9-Dz_6=0,
\]

\[
P_3:\quad qz_1z_7+Dz_6=0,
\]

\[
P_4:\quad q^2z_6-z_1z_7=0.
\]

The fifth relation satisfies the exact polynomial identity

\[
P_5-(P_2+P_3)=D\left(z_6^2-\frac12\right),
\]

before any localization.  Hence

\[
\boxed{z_6^2=\frac12},
\]

so `z6 != 0`.

The combinations

\[
pP_1-P_2=z_6(p^3+D),
\]

and

\[
qP_4+P_3=z_6(q^3+D)
\]

then give

\[
\boxed{p^3=q^3=\frac{-1+i}{4}}.
\]

The product relations are

\[
\boxed{z_0z_9=-p^2z_6},
\qquad
\boxed{z_1z_7=q^2z_6}.
\]

Therefore

\[
\boxed{p,q,z_0,z_1,z_6,z_7,z_9\ne0}.
\]

The source validator is

```text
experiments/r22_phase5_component13_mask150_local_relations.py
```

## 3. Finite algebraic stratification

Because `p` and `q` each have three cube-root choices and `z6` has two square-root choices, the continuous scale sector collapses to

\[
3\times3\times2=18
\]

exact finite branches.

After eliminating `z9` and `z7` using only the proved-nonzero product relations and stripping only Laurent factors in the proved-nonzero scales `z0,z1`, the exact affine census separates the 18 branches into

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

The two `(a,b)=(0,0)` branches are affine-inconsistent and are closed immediately.

The two rank-11 families are:

- p-side: `(a,b)=(1,0),(2,0)`, both `z6` signs, with `z2=z8=0`;
- q-side: `(a,b)=(0,1),(0,2)`, both `z6` signs, with `z12=z16=0`.

The remaining eight branches are

```text
(a,b) = (1,1), (2,1), (1,2), (2,2)
```

with both `z6` signs, and have affine rank 10.

The census is implemented in

```text
experiments/r22_phase5_component13_mask150_finite_census.py
```

## 4. Forced zeros are not themselves an invertibility obstruction

Both rank-11 forced-zero patterns were tested against all required Phase-4 `8x8/10x10` F determinant polynomials.

Neither pattern kills every monomial of any required determinant.  Thus the rank-11 strata cannot be discarded merely because of the affine forced zeros; final pentagon equations are still required.

The independent gate is

```text
experiments/r22_phase5_component13_mask150_forced_zero_invertibility.py
```

## 5. Four p-side rank-11 branches — one constant cell

A representative p-side branch was first fully substituted into the 219-polynomial kernel.  Its affine residual quotient contains an exact nonzero constant at the fixed provenance

```text
(XXXX;Y)_(1,0).
```

The same cell was then replayed independently on all four p-side branches:

```text
(1,0,+), (1,0,-), (2,0,+), (2,0,-).
```

For every branch it reduces to a nonzero element of

\[
K=\mathbf Q(i,\sqrt2,\sqrt3),
\]

so the pentagon equation is literally

\[
\boxed{c=0,\qquad c\ne0}.
\]

Hence all four p-side rank-11 strata are closed by one fixed local cell.

Certificate:

```text
experiments/r22_phase5_component13_mask150_p_rank11_certificate.py
```

GitHub Actions run `32218886383` reports `closed=4,total=4`.

## 6. Four q-side rank-11 branches — a second constant cell

The q-side representative likewise has an exact constant obstruction, now at the fixed provenance

```text
(XXXX;X)_(2,5).
```

That same cell was replayed independently on

```text
(0,1,+), (0,1,-), (0,2,+), (0,2,-),
```

and is a nonzero exact constant on all four branches.

Therefore all four q-side rank-11 strata are closed.

Certificate:

```text
experiments/r22_phase5_component13_mask150_q_rank11_certificate.py
```

GitHub Actions run `32219237168` reports `closed=4,total=4`.

## 7. Eight rank-10 branches — universal three-cell certificate

For the representative `(a,b,z6-sign)=(1,1,+)`, the affine residual quotient leaves a 17-equation subsystem supported only on

\[
(r,s)=(z_{19},z_{20}).
\]

Three fixed `g`-cells are sufficient:

```text
P1 = (XXXX;g)_(0,3)
P2 = (XXXX;g)_(0,2)
P3 = (XXXX;g)_(0,0)
```

After division only by each equation's own proved-nonzero scalar coefficient, the first two take the scale-independent normal forms

\[
\boxed{1+4rs-4s^2=0},
\]

\[
\boxed{1+4rs-4r^2=0}.
\]

Subtracting them yields

\[
\boxed{r^2=s^2},
\]

hence, in characteristic zero,

\[
r=s\quad\text{or}\quad r=-s.
\]

### Slice `r=s`

The first normalized equation immediately becomes

\[
1=0.
\]

So this slice is impossible.

### Slice `r=-s`

The first normalized equation gives

\[
1-8s^2=0,
\qquad
\boxed{s^2=\frac18}.
\]

The fixed third cell `P3` is a homogeneous quadratic in `r,s`.  Substitution of `r=-s` and `s^2=1/8` gives a nonzero exact element of `K` on every rank-10 branch.

The same three cells were then replayed independently on all eight branches

```text
(1,1,+), (1,1,-),
(2,1,+), (2,1,-),
(1,2,+), (1,2,-),
(2,2,+), (2,2,-).
```

All eight pass the same certificate shape and are excluded.

Representative probe:

```text
experiments/r22_phase5_component13_mask150_rank10_probe.py
```

Eight-branch certificate:

```text
experiments/r22_phase5_component13_mask150_rank10_certificate.py
```

GitHub Actions run `32219850511` reports

```text
closed = 8
total  = 8
```

with the same three fixed cells on every branch.

## 8. Final accounting

All 18 finite branches are now excluded:

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
\text{component 13 / chirality mask 150 has no invertible Phase-5 associator extension.}
}
\]

Equivalently,

\[
\boxed{\text{component 13 / mask 150 is non-categorifiable}.}
\]

## 9. Structural comparison inside component 13

The first three closed chirality masks now show a useful pattern.

- mask `0`: finite scale coordinate `z5`;
- mask `105`: finite scale coordinate `z0`;
- mask `150`: finite scale coordinate `z6`.

The coordinate charts differ, but the global kernel size remains 219 unique cubics, the continuous scale sector collapses to 18 exact algebraic strata, and the final obstruction localizes to very few pentagon cells.

Mask 150 is in fact locally stronger at rank 11 than masks 0/105: each rank-11 family is killed by a pure nonzero-constant pentagon entry, without an additional nonzero-coordinate argument.

The next unresolved chirality of scalar component 13 is mask `255`.  It must begin from a fresh kernel and independent coordinate audit; no mask-150 chart or certificate is assumed a priori.
