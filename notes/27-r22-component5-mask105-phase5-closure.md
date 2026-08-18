# R(2,2) Phase 5 — component 5 / chirality mask 105 closure

**Status:** `CLOSED / EXACT LOCAL CERTIFICATES / fresh replay`

This note records the complete Phase-5 closure of the fresh branch

```text
component 5 / chirality mask 105
```

It is independent of the earlier component-5/mask-0 closure except for shared Phase-1–4 infrastructure.  In particular, mask 105 has a different 219-polynomial term-count fingerprint and a different p-side finite relation, so no mask-0 certificate is imported by assumption.

No Gröbner basis or global nonlinear solve is used anywhere below.

## 1. Fresh final-kernel fingerprint

The sparse exact compiler gives:

- 96 final pentagon blocks with four noninvertible external inputs;
- block dimensions: 32 of size 8, 32 of size 10, 32 of size 40;
- 56,448 scalar positions;
- 50,880 nonzero final entries;
- 23 kernel variables: `p,q,z0,...,z20`;
- 219 unique exact cubic Laurent polynomials;
- maximum F-degree 3.

The mask-105 term-count profile is

```text
{2:4, 3:2, 4:45, 5:20, 6:8, 7:8, 8:12, 9:20, 10:96, 11:4}
```

which differs from mask 0.  Thus the two kernels are not identified merely by a variable permutation or scalar rephasing that preserves monomial support cardinalities.

## 2. The zero branch is impossible

Assume `z0=0`.  The four shortest final-pentagon equations imply product-zero alternatives exactly as in the generic local analysis.  Fresh branch replay gives four zero-pattern cases.

Two cases are excluded by required F-block invertibility.  The remaining zero-pattern cases produce final-pentagon equations that reduce to nonzero torus monomials.  Hence every `z0=0` branch is impossible and

\[
\boxed{z_0\neq0}.
\]

## 3. Five exact local relations

Because `z0 != 0`, the four shortest binomials may be divided legitimately.  For mask 105 they give

\[
\boxed{p^3=\frac{1+i}{4}},
\qquad
\boxed{q^3=-\frac{1+i}{4}},
\]

and

\[
\boxed{z_2z_3=-i p^2z_0},
\qquad
\boxed{z_1z_8=-i q^2z_0}.
\]

Therefore

\[
z_1z_2z_3z_8\neq0.
\]

The fifth short equation again reduces to

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

Thus the continuous `(p,q,z0)` torus collapses to

\[
3\times3\times2=18
\]

finite algebraic strata.

A dedicated mask-105 five-relation rewrite reduces the 219-polynomial kernel to 210 unique residual polynomials.  Five equations vanish identically, but there is no singleton contradiction and no direct full-rank contradiction on monomial support of size at most four.  The finite-stratum step is therefore genuinely necessary.

## 4. Exact finite-stratum split: 10 + 8

Write

\[
p=P_0\omega^a,
\qquad
q=Q_0\omega^b,
\qquad
a,b\in\{0,1,2\},
\]

with

\[
P_0=-\frac{1-i}{2},
\qquad
Q_0=\frac{1-i}{2},
\qquad
\omega^3=1,
\]

and take either root of

\[
2z_0^2+4z_0-1=0.
\]

Fresh exact affine closure on all 18 branches gives precisely two strata:

### Rank-11 stratum

Ten branches have

\[
\operatorname{rank}=11,
\qquad
\dim_{\mathrm{free}}=9,
\]

and force

\[
z_6=z_7=z_9=z_{10}=0.
\]

All ten are excluded immediately by the three diagnostic final-pentagon cells

```text
(X,X,X,X,X;X)_(5,2)
(X,X,X,X;1)_(1,3)
(X,X,X,X;1)_(3,1)
```

which reduce to nonzero Laurent monomials in the already-proved nonzero scale variables `z1,z2`.

### Rank-10 stratum

Exactly eight branches survive that first local-cell gate:

```text
(a,b) = (1,1), (2,1), (1,2), (2,2)
```

for both roots of `z0`.  Each has

\[
\operatorname{rank}=10,
\qquad
\dim_{\mathrm{free}}=10,
\]

with no forced-zero variable at the affine level.

These are the only remaining branches.

## 5. Two-cell certificates for the off-diagonal cube pairs

Set

\[
x=z_{19},\qquad y=z_{20}.
\]

For both roots and each of

```text
(a,b)=(2,1), (1,2),
```

the final-pentagon cell

```text
G0 = (X,X,X,X;g)_(0,0)
```

is a nonzero algebraic scalar times

\[
(x-y)^2.
\]

Thus `G0=0` forces

\[
x=y.
\]

The adjacent cell

```text
G2 = (X,X,X,X;g)_(0,2)
```

is a nonzero algebraic scalar times

\[
4xy-4y^2-1.
\]

Substituting `x=y` gives

\[
-1=0.
\]

Hence all four off-diagonal/root branches are impossible.  Each uses only two final-pentagon cells.

## 6. Three-cell certificates for the diagonal cube pairs

For

```text
(a,b)=(1,1), (2,2),
```

and either root, the two cells

```text
G2 = (X,X,X,X;g)_(0,2)
G3 = (X,X,X,X;g)_(0,3)
```

are nonzero scalar multiples of

\[
4xy-4y^2-1=0,
\]

and

\[
4x^2-4xy+1=0.
\]

Adding them gives

\[
4(x^2-y^2)=4(x-y)(x+y)=0.
\]

The branch `x=y` contradicts the first equation immediately.  Therefore

\[
x=-y.
\]

The first equation then gives

\[
-8y^2-1=0,
\qquad
\boxed{y^2=-\frac18}.
\]

Now use

```text
G0 = (X,X,X,X;g)_(0,0).
```

### Pair `(1,1)`

Up to a nonzero scalar,

\[
G_0=(\sqrt3+i)(x^2+y^2)+4ixy.
\]

On `x=-y`, `y^2=-1/8`, this reduces exactly to

\[
\boxed{\frac{-\sqrt3+i}{4}\neq0}.
\]

### Pair `(2,2)`

Up to a nonzero scalar,

\[
G_0=(\sqrt3-i)(x^2+y^2)-4ixy.
\]

On the same derived branch this reduces exactly to

\[
\boxed{\frac{-\sqrt3-i}{4}\neq0}.
\]

Thus all four diagonal/root branches are impossible.  Each uses only three final-pentagon cells.

## 7. Closure

The finite audit gives

\[
18=10+8.
\]

The ten rank-11 branches are excluded by the first diagnostic local cells.  The eight rank-10 branches are excluded by the two- and three-cell certificates above.  Therefore no finite branch remains.

Hence the fresh branch

\[
\boxed{\text{component 5 / chirality mask 105 is non-categorifiable}.}
\]

Equivalently, after the exact Phase-1–4 quotient, the final four-noninvertible pentagons have empty invertible coherence locus on this branch.

## 8. Scope and next step

This note closes **component 5 / mask 105 only**.  Together with the independently closed mask 0 branch, component 5 now has two of its four Phase-2 survivor chiralities closed at Phase 5.

The next preferred step is not to assume the remaining masks `150` and `255` are equivalent.  Instead, test whether the known chirality conjugations

```text
0 <-> 255
105 <-> 150
```

extend to an exact conjugation of the full Phase-5 quotient, including required F-block determinant loci.  If so, the remaining two component-5 masks close by a proved symmetry; otherwise they must be replayed fresh.
