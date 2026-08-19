# R(2,2) theorem audit — component 5 / mask 0 / D class 1 Phase-5 closure

**Status:** `CLOSED / EXACT / second physical D-amplitude sheet`

This note records the first complete Phase-5 closure among the `21 active
F-component` branches on the newly discovered gauge-inequivalent D-amplitude
sheet.

The proof is rebuilt from the class-1 lower data.  It does not identify the
class-1 kernel with the historical class-0 kernel, even though their combinatorial
sizes agree.  In fact the first p-side short relation changes phase.

No Gröbner basis, floating-point solve, numerical continuation, or global
nonlinear solver is used.

## 1. Fresh nonlinear kernel

For scalar component `5`, chirality mask `0`, D-amplitude class `1`, the complete
final-pentagon compiler gives

```text
F-linear components          = 21
kernel variables             = 23 = p,q,z0,...,z20
final scalar positions       = 56448
raw nonzero final entries    = 50880
unique kernel polynomials    = 219
constant contradictions      = 0
```

All 219 equations have total degree 3.  The shortest cells are four binomials
and two trinomials.

GitHub Actions run: `32286013095`.

## 2. Fresh five-cell local model

The fixed source provenances

\[
(XXXX;X)_{(0,0)},\quad (XXXX;X)_{(0,2)},
\]
\[
(XXXX;Y)_{(0,18)},\quad (XXXX;Y)_{(18,18)},
\]
\[
(XXXX;1)_{(0,0)}
\]

are read directly from the class-1 kernel.  They give

\[
p^2z_0-i z_2z_3=0,
\]

\[
pz_2z_3-\frac{1+i}{4}z_0=0,
\]

\[
qz_1z_8+\frac{1-i}{4}z_0=0,
\]

\[
q^2z_0-i z_1z_8=0.
\]

Thus

\[
z_2z_3=-ip^2z_0,
\qquad
z_1z_8=-iq^2z_0.
\]

Conditional on `z0 != 0`, the cube constants are

\[
\boxed{p^3=\frac{-1+i}{4}},
\qquad
\boxed{q^3=-\frac{1+i}{4}}.
\]

The fifth cell reduces using only those four short relations to

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

The p-side cube phase differs from the historical D sheet, so the class-0
finite branch constants were not imported.

GitHub Actions run: `32286439147`.

## 3. Independent `z0 != 0` certificate

Before dividing by `z0`, the raw final-pentagon rows are specialized at `z0=0`
**before** canonicalization.  The four product-zero branches are

```text
A, ZB, ZC, D
```

and all four close exactly:

- `A` and `D`: required F-block invertibility fails;
- `ZB` and `ZC`: `(XXXX;1)_(0,0)` becomes a torus-only nonzero monomial.

Hence

\[
\boxed{z_0\ne0}.
\]

The proof does not use the cube constants or the z0 quadratic.

GitHub Actions run: `32286782725`.

## 4. Eighteen finite scale strata

Now localization at `z0` is legitimate.  Choose

\[
P_0=\frac{1+i}{2},\qquad Q_0=\frac{1-i}{2},
\qquad \omega^3=1.
\]

Then

\[
p=P_0\omega^a,\qquad q=Q_0\omega^b,
\qquad a,b\in\{0,1,2\},
\]

and `z0` has the two roots of

\[
2z_0^2+4z_0-1=0.
\]

Therefore there are exactly

\[
\boxed{18}
\]

finite scale branches.

The fresh affine/local-cell census gives

\[
\boxed{18=10+8}.
\]

### 4.1 Ten rank-11 branches

Ten branches have

```text
rank = 11
free dimension = 9
forced zero = z6,z7,z9,z10
```

and are all excluded by the first three diagnostic cells.  In particular the
cell

\[
(XXXXX)_{(5,2)}
\]

reduces to a nonzero Laurent monomial in the already-proved nonzero scale
coordinates on every one of those branches.

### 4.2 Eight rank-10 branches

The only survivors of that first gate are

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\}
\]

for both z0 roots.  They have

```text
rank = 10
free dimension = 10
forced zero = none
```

with residual coordinates including

\[
x=z_{19},\qquad y=z_{20}.
\]

GitHub Actions run: `32287188335`.

## 5. Exact rank-10 local certificates

Two fixed cells reduce on every rank-10 branch, up to nonzero branch scalars, to

\[
G_2=4(1-i)xy-4(1+i)y^2-1,
\]

\[
G_3=4(1-i)x^2+4(1+i)xy-i.
\]

### 5.1 Off-diagonal cube pairs

For

\[
(a,b)=(2,1),(1,2),
\]

the additional cells are proportional to

\[
G_0=(x-y)(x+(1-2i)y),
\]

\[
G_1=(x+y)((2-i)x+iy).
\]

Their exact resultant is

\[
\boxed{\operatorname{Res}_x(G_0,G_1)=-48y^4}.
\]

Thus a common zero forces `y=0`; then `G0=x^2` forces `x=0`, while

\[
G_2(0,0)=-1.
\]

All four off-diagonal/root branches are impossible.

### 5.2 Diagonal cube pairs

For

\[
(a,b)=(1,1),(2,2),
\]

we have the exact relation

\[
\boxed{G_3-iG_2=4(1-i)(x-y)(x+y)}.
\]

Hence `x=+/-y`.  The origin is impossible because `G2(0,0)=-1`, so `y` is
nonzero.  The branch-specific `G0` is a nonzero scalar times `y^2` on both sign
slices.  The exact coefficients are

```text
(1,1): x= y ->  6-2*sqrt(3)*i
       x=-y ->  2+2*sqrt(3)*i

(2,2): x= y -> -6-2*sqrt(3)*i
       x=-y -> -2+2*sqrt(3)*i
```

and none vanishes.  Therefore all four diagonal/root branches are impossible.

GitHub Actions run: `32288052784`.

## 6. Closure

The full finite branch account is

\[
\boxed{18=10_{\rm rank11}+8_{\rm rank10}=18_{\rm closed}}.
\]

Together with the independent raw `z0=0` closure, no Phase-5 branch remains.
Hence

\[
\boxed{\text{component 5 / mask 0 / D class 1 is obstructed}.}
\]

## 7. Next gate

Do not propagate this certificate to the other chirality masks by assumption.
The next step is to fresh-derive the same five source-cell relations for

```text
component 5 / D class 1 / masks 105,150,255
```

and use their actual phase constants to determine whether the `18=10+8`
stratification and rank-10 local models persist.
