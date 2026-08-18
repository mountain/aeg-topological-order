# R(2,2) Phase 5 closure — component 5 / chirality mask 150

**Status:** `CLOSED / EXACT / SERIAL REPLAY VERIFIED`

This note records the complete fresh Phase-5 closure of

```text
component 5 / chirality mask 150
```

from the canonical Phase-1–4 quotient on `main`.

The final verification was deliberately serialized.  Each gate had to pass before the next one was scheduled:

1. F-coordinate reproducibility;
2. direct derivation of the five local relations from exact pentagon entries;
3. complete exclusion of `z0=0` from raw final-pentagon equations;
4. exact census of all 18 finite `(p,q,z0)` strata;
5. exact local certificates for all eight rank-drop strata.

The successful serial replay is GitHub Actions run `32173886648` (`R22 research replay`, run number 99).  No Gröbner basis, global nonlinear solver, floating-point root search, or numerical continuation is used.

---

## 1. Stable Phase-5 coordinates

The Phase-4 quotient for component 5 has 21 active F-linear components.  The final-kernel compiler names them

\[
z_0,\ldots,z_{20}
\]

by the sorted weighted-union-find component representatives.

Because the local certificates refer to specific coordinates such as `z19,z20`, the naming itself was audited across independent Python processes with

```text
PYTHONHASHSEED = 1, 2, 17.
```

For mask 150 all three runs produced exactly one F-component partition and one fixed target-pentagon polynomial:

```text
partition_variants = 1
target_variants    = 1
stable             = True
```

The common 1312-entry F-component partition digest was

```text
fe4c78f047d5e62b319fc16449436f21aaf2e9150cdb59f6ca4e07337fe082a7
```

and the fixed target digest was

```text
1fbc1f972db851152a8956911308c2156ee318152249dcff78f849c3ebfb10b1.
```

Thus the `z_j` coordinates used below are reproducible under the tested Python hash seeds rather than artifacts of one union-find execution order.

---

## 2. Fresh final kernel

A fresh exact sparse compilation gives the same global Phase-5 size as the other component-5 chiralities:

- 96 final pentagon blocks with four noninvertible external inputs;
- block profile `32 x 8`, `32 x 10`, `32 x 40`;
- 56,448 scalar positions;
- 50,880 nonzero scalar entries;
- 23 variables `p,q,z0,...,z20`;
- 219 unique exact cubic Laurent polynomials.

No nonlinear solve is performed at this stage.

---

## 3. Five local relations, derived directly from pentagon entries

The finite-stratum relations were not accepted as hard-coded assumptions.  A separate source-validation gate recompiles the exact kernel, locates five entries by pentagon provenance, and derives the relations from those entries.

The first four entries are

```text
P1 = (X,X,X,X;X)_(0,0)
P2 = (X,X,X,X;X)_(0,2)
P3 = (X,X,X,X;Y)_(0,18)
P4 = (X,X,X,X;Y)_(18,18)
```

and are respectively proportional to

\[
\begin{aligned}
z_2z_3-i p^2z_0 &=0,\\
pz_2z_3-i\frac{1-i}{4}z_0&=0,\\
qz_1z_8-i\frac{-1+i}{4}z_0&=0,\\
z_1z_8-iq^2z_0&=0.
\end{aligned}
\]

Once `z0 != 0` is established, these imply

\[
\boxed{p^3=\frac{1-i}{4}},
\qquad
\boxed{q^3=\frac{-1+i}{4}},
\]

and

\[
\boxed{z_2z_3=i p^2z_0},
\qquad
\boxed{z_1z_8=i q^2z_0}.
\]

The fifth provenance is

```text
P5 = (X,X,X,X;1)_(0,0).
```

A dedicated derivation reduces `P5` using only the four product/cube relations above — crucially **without assuming any polynomial relation for `z0`**.  It yields exactly

\[
\frac{1+i}{8}\left(2z_0^2+4z_0-1\right)=0.
\]

Hence

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

This gate closes a provenance gap in the earlier exploratory finite audit: all five relations now have a direct exact source in the final pentagons.

---

## 4. Exact exclusion of `z0=0`

The four shortest binomials imply, under `z0=0`,

\[
z_2z_3=0,
\qquad
z_1z_8=0.
\]

Thus there are four zero patterns:

```text
A  : z0=z2=z1=0
ZB : z0=z2=z8=0
ZC : z0=z3=z1=0
D  : z0=z3=z8=0.
```

The final serial gate does **not** specialize an already-deduplicated 219-polynomial kernel.  Instead it replays all 50,880 raw nonzero final entries, applies the zero pattern to each raw polynomial first, and only then canonicalizes the surviving equations.  This avoids spurious implications caused by specializing after common-factor normalization.

For mask 150 the raw-before-canonical replay closes all four zero patterns immediately.  In every case the entry

```text
(X,X,X,X;1)_(0,0)
```

specializes to a nonzero torus-only constant equation.  The exact summary is

```text
closed    = 4
total     = 4
survivors = []
```

Therefore

\[
\boxed{z_0\ne0}.
\]

This fresh replay supersedes the earlier exploratory `ZC -> singleton-zero -> ...` chain for mask 150; that longer chain is unnecessary once raw specialization is performed in the correct order.

---

## 5. Continuous torus collapses to 18 finite strata

Since

\[
z_0\ne0,
\]

the first four local equations may now be localized safely.  Together with the fifth relation they give

\[
p^3=\frac{1-i}{4},
\qquad
q^3=\frac{-1+i}{4},
\qquad
2z_0^2+4z_0-1=0.
\]

Choose

\[
P_0=-\frac{1+i}{2},
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

Hence exactly

\[
\boxed{3\times3\times2=18}
\]

finite strata remain.

---

## 6. Exact finite census: `10 + 8`

The serial finite audit independently rebuilds the safely localized affine closure on all 18 strata and requires the exact expected census as a hard assertion.

It obtains precisely

\[
\boxed{18=10+8}.
\]

### 6.1 Rank-11 stratum

Ten branches have

\[
\operatorname{rank}=11,
\qquad
\dim_{\rm free}=9,
\]

with forced zeros

\[
\boxed{z_6=z_7=z_9=z_{10}=0}.
\]

All ten are excluded by the existing low-support diagnostic final-pentagon cells; their projected remainders are nonzero Laurent monomials in the already-proved nonzero scale variables.

### 6.2 Rank-10 stratum

Exactly eight branches survive the first diagnostic gate:

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\}
\]

for both roots of `z0`.

Each has

\[
\operatorname{rank}=10,
\qquad
\dim_{\rm free}=10,
\]

with no affine-level forced-zero component.

The serial workflow asserts both the rank profile and the exact survivor set, so a merely similar-looking `10+8` split is not sufficient to pass.

---

## 7. Rank-drop core

Set

\[
x=z_{19},
\qquad
y=z_{20}.
\]

After the affine closure, the decisive short equations again occur in the local cells

```text
G0 = (X,X,X,X;g)_(0,0)
G2 = (X,X,X,X;g)_(0,2)
G3 = (X,X,X,X;g)_(0,3).
```

The eight branches divide into four off-diagonal and four diagonal/root cases.

### 7.1 Off-diagonal cube pairs: two-cell certificates

For

\[
(a,b)=(2,1),(1,2),
\]

for either root of `z0`, `G0` is a nonzero algebraic scalar times

\[
(x-y)^2.
\]

Thus `G0=0` implies

\[
x=y.
\]

`G2` is a nonzero scalar multiple of

\[
4xy-4y^2-1.
\]

Substituting `x=y` gives

\[
\boxed{-1=0}.
\]

Hence these four finite branches are excluded by only two local cells each.

### 7.2 Diagonal cube pairs: three-cell certificates

For

\[
(a,b)=(1,1),(2,2),
\]

for either root, `G2` and `G3` are nonzero scalar multiples of

\[
4xy-4y^2-1=0
\]

and

\[
4x^2-4xy+1=0.
\]

Adding them gives

\[
4(x-y)(x+y)=0.
\]

The branch `x=y` contradicts the first equation immediately, so

\[
x=-y.
\]

Then

\[
y^2=-\frac18.
\]

For `(a,b)=(1,1)`, substituting this derived branch into `G0` leaves

\[
\boxed{-\frac{\sqrt3}{4}+\frac{i}{4}\ne0}.
\]

For `(a,b)=(2,2)`, it leaves

\[
\boxed{-\frac{\sqrt3}{4}-\frac{i}{4}\ne0}.
\]

Thus these four branches are excluded by three local cells each.

The exact serial replay reports

```text
closed            = 8
total             = 8
certificate_types = {'two-cell': 4, 'three-cell': 4}
```

with every branch printed and checked individually.

---

## 8. Closure statement

All possible Phase-5 strata for component 5 / mask 150 have been excluded:

1. `z0=0` is impossible;
2. `z0!=0` collapses the E/scale sector to 18 exact finite strata;
3. ten rank-11 strata are killed by short diagnostic entries;
4. the eight rank-drop strata are killed by exact two- and three-cell certificates.

Therefore

\[
\boxed{\text{component 5 / chirality mask 150 is non-categorifiable}.}
\]

Equivalently, the canonical Phase-4 branch has no invertible associator extension satisfying all final pentagons with four noninvertible external inputs.

---

## 9. Reproducibility boundary

This closure is stronger than the exploratory result in three ways:

- the `z_j` coordinate partition has been replayed across independent Python hash seeds;
- the five finite/local relations are re-derived directly from their pentagon provenance rather than accepted as a rewrite table;
- `z0=0` is excluded by specializing the raw 50,880-entry final system before canonicalization.

The complete serial verification chain is run `32173886648`, and every gate completed successfully before the next was scheduled.

---

## 10. Next branch

This note closes mask 150 only.  The remaining component-5 chirality is

\[
\boxed{255}.
\]

It must be replayed through the same serial gates independently.  In particular, the naive identity-coordinate complex-conjugation audit has already failed, so this note does not transfer the mask-150 result to mask 255 by symmetry.
