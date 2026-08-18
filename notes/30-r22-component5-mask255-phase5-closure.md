# R(2,2) Phase 5 closure — component 5 / chirality mask 255

**Status:** `CLOSED / EXACT / SERIAL REPLAY VERIFIED`

This note records the complete fresh Phase-5 closure of

```text
component 5 / chirality mask 255
```

from the canonical Phase-1–4 quotient on `main`.

As for mask 150, the final verification was deliberately serialized.  Each gate had to pass before the next was scheduled:

1. F-coordinate reproducibility;
2. direct derivation of the five local relations from exact pentagon entries;
3. complete exclusion of `z0=0` from raw final-pentagon equations;
4. exact census of all 18 finite `(p,q,z0)` strata;
5. exact local certificates for all eight rank-drop strata.

The successful serial replay is GitHub Actions run `32175782953` (`R22 research replay`, run number 100).  No Gröbner basis, global nonlinear solver, floating-point root search, or numerical continuation is used.

---

## 1. Stable Phase-5 coordinates

The Phase-4 quotient has 21 active F-linear components, named

\[
z_0,\ldots,z_{20}.
\]

The component partition and a fixed final-pentagon target were rebuilt in independent Python processes with

```text
PYTHONHASHSEED = 1, 2, 17.
```

The serial gate required one partition digest and one target digest across all three processes.  It passed exactly, so the `z_j` coordinates used below are reproducible under the tested execution-order perturbations.

---

## 2. Fresh final kernel

A fresh exact sparse compilation gives

- 96 final pentagon blocks with four noninvertible external inputs;
- 56,448 scalar positions;
- 50,880 nonzero scalar entries;
- 23 variables `p,q,z0,...,z20`;
- 219 unique exact cubic Laurent polynomials.

No nonlinear solving is performed at this stage.

---

## 3. Five local relations derived from exact pentagon provenance

The source-validation gate recompiles the exact kernel and locates

```text
P1 = (X,X,X,X;X)_(0,0)
P2 = (X,X,X,X;X)_(0,2)
P3 = (X,X,X,X;Y)_(0,18)
P4 = (X,X,X,X;Y)_(18,18)
P5 = (X,X,X,X;1)_(0,0).
```

For mask 255 the first four entries give, up to nonzero Gaussian-rational scalars,

\[
\boxed{z_2z_3=-i p^2z_0},
\qquad
\boxed{z_1z_8=i q^2z_0}.
\]

Once `z0 != 0` is proved, the paired equations imply

\[
\boxed{p^3=\frac{1+i}{4}},
\qquad
\boxed{q^3=\frac{-1+i}{4}}.
\]

The fifth entry is then reduced using only these four product/cube relations — without assuming any equation for `z0` — and becomes exactly

\[
\frac{1-i}{8}\left(2z_0^2+4z_0-1\right)=0.
\]

Hence

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

Thus the finite-stratum relations are derived from the original exact pentagons rather than accepted as an external rewrite table.

---

## 4. Exact exclusion of `z0=0`

Under `z0=0`, the four shortest binomials give

\[
z_2z_3=0,
\qquad
z_1z_8=0,
\]

and therefore four zero patterns:

```text
A  : z0=z2=z1=0
ZB : z0=z2=z8=0
ZC : z0=z3=z1=0
D  : z0=z3=z8=0.
```

The final verification specializes the 50,880 raw nonzero final-pentagon entries **before** canonicalization and deduplication.  This ordering is essential: specialization of an already-normalized quotient can create spurious singleton implications.

For mask 255 all four patterns close immediately.  In every case

```text
(X,X,X,X;1)_(0,0)
```

specializes to a nonzero torus-only constant equation.  The exact replay reports

```text
closed    = 4
total     = 4
survivors = []
```

so

\[
\boxed{z_0\ne0}.
\]

---

## 5. Finite algebraic strata

After the legal localization at `z0 != 0`,

\[
p^3=\frac{1+i}{4},
\qquad
q^3=\frac{-1+i}{4},
\qquad
2z_0^2+4z_0-1=0.
\]

Choose

\[
P_0=-\frac{1-i}{2},
\qquad
Q_0=\frac{1+i}{2},
\qquad
\omega=\frac{-1+i\sqrt3}{2}.
\]

Then

\[
p=P_0\omega^a,
\qquad
q=Q_0\omega^b,
\qquad
a,b\in\{0,1,2\},
\]

and

\[
z_0=-1\pm\frac{\sqrt6}{2}.
\]

Therefore the continuous scale sector collapses to exactly

\[
\boxed{18}
\]

finite algebraic strata.

---

## 6. Exact finite census: `10 + 8`

The serial finite audit requires the complete branch census as a hard assertion.  Mask 255 gives exactly

\[
\boxed{18=10+8}.
\]

Ten branches have

\[
\operatorname{rank}=11,
\qquad
\dim_{\rm free}=9,
\]

with

\[
z_6=z_7=z_9=z_{10}=0,
\]

and are excluded by the existing low-support diagnostic entries.

The only survivors are

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\}
\]

for both roots of `z0`.  All eight have

\[
\operatorname{rank}=10,
\qquad
\dim_{\rm free}=10,
\]

with no affine-level forced-zero variable.

---

## 7. Rank-drop core

Let

\[
x=z_{19},
\qquad
y=z_{20}.
\]

The decisive equations are local entries

```text
G0 = (X,X,X,X;g)_(0,0)
G1 = (X,X,X,X;g)_(0,1)
G2 = (X,X,X,X;g)_(0,2)
G3 = (X,X,X,X;g)_(0,3).
```

Unlike mask 150, mask 255 has two distinct three-cell certificate types.

### 7.1 Off-diagonal cube pairs

For

\[
(a,b)=(2,1),(1,2),
\]

for either root, after removing nonzero algebraic scalar factors the first two equations have the models

\[
G_0=(x-y)(x+(1+2i)y),
\]

and

\[
G_1=(x+y)((1-2i)x-y).
\]

Their exact resultant in `x` is

\[
\boxed{\operatorname{Res}_x(G_0,G_1)=48y^4}.
\]

A common zero therefore requires

\[
y=0,
\]

and then either factorization forces

\[
x=0.
\]

But the third local equation satisfies

\[
\boxed{G_2(0,0)=i\ne0}.
\]

Hence all four off-diagonal/root branches are impossible.  Each uses three local cells.

### 7.2 Diagonal cube pairs

For

\[
(a,b)=(1,1),(2,2),
\]

for either root, the exact local equations satisfy

\[
\boxed{iG_3-G_2=4(1+i)(x-y)(x+y)}.
\]

Thus any common zero must obey

\[
x=y
\quad\text{or}\quad
x=-y.
\]

For `(a,b)=(1,1)`, the `G0` coefficient on the two signs is respectively

\[
-6+2\sqrt3\,i,
\qquad
-2-2\sqrt3\,i,
\]

both nonzero.

For `(a,b)=(2,2)`, the corresponding coefficients are

\[
6+2\sqrt3\,i,
\qquad
2-2\sqrt3\,i,
\]

again both nonzero.

Thus `G0=0` on either sign forces `y=0`, hence `x=0`; but `G2(0,0)=i` is again impossible.

Therefore all four diagonal/root branches are excluded by three local cells each.

The exact serial replay reports

```text
closed            = 8
total             = 8
certificate_types = {'three-cell': 8}
```

with every branch checked separately.

---

## 8. Closure statement

Every Phase-5 possibility for component 5 / mask 255 is excluded:

1. `z0=0` has no branch;
2. `z0!=0` reduces the scale sector to 18 finite algebraic strata;
3. ten rank-11 strata are killed by short diagnostic cells;
4. all eight rank-drop strata are killed by exact three-cell certificates.

Therefore

\[
\boxed{\text{component 5 / chirality mask 255 is non-categorifiable}.}
\]

Equivalently, the canonical Phase-4 branch has no invertible associator extension satisfying all final pentagons with four noninvertible external inputs.

---

## 9. Component-5 consequence

Together with the independently verified closures for masks

\[
0,\ 105,\ 150,
\]

this closes the last surviving chirality for scalar component 5.  Hence

\[
\boxed{\text{scalar component 5 is completely obstructed at Phase 5}.}
\]

The next scalar frontier is component 13; no statement about components 7, 13, or 15 follows from the component-5 calculation alone.
