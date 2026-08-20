# R(2,2) — complete Phase-5 closure of scalar component 5 on the second D-amplitude sheet

**Status:** `CLOSED / EXACT / ALL FOUR CHIRALITY SURVIVORS / D-AMPLITUDE CLASS 1`

This note freezes the complete Phase-5 closure of scalar component `5` on the additional gauge-inequivalent D-amplitude sheet discovered during the theorem-level audit.

The theorem audit established that each deep epsilon-minus chirality branch has two physical cross-D amplitude classes after quotienting the full residual gauge action.  The historical Phase-5 analysis covered only class `0`.  This note records the independent closure of the missing class `1` for all four Phase-1 chirality survivors

\[
\boxed{0,105,150,255}.
\]

Therefore

\[
\boxed{
\forall m\in\{0,105,150,255\},\qquad
\mathcal C^{\mathrm{Phase5}}_{5,m,\mathrm{Dclass}=1}=\varnothing.
}
\]

Together with the accepted class-0 closure on `main`, scalar component `5` is now closed on **both** physical D-amplitude sheets.

No global Gröbner basis, floating-point search, numerical continuation, or timeout increase is used in any certificate below.

---

## 1. Common second-sheet Phase-5 kernel

All four class-1 masks were reconstructed from the torsion-twisted exact D data and passed through the same E/F/final-pentagon compiler used for class `0`.

For every mask the Phase-5 kernel has

- 21 active weighted F components;
- 23 effective nonlinear variables `p,q,z0,...,z20`;
- 50,880 raw nonzero final-pentagon entries;
- 219 unique exact cubic Laurent-polynomial relations;
- no generic constant contradiction.

Thus the additional physical `Z2` D sheet changes exact phases but does not change the macroscopic nonlinear-kernel geometry.

---

## 2. Source-derived finite scale systems

For every mask, five fixed local final-pentagon cells were re-derived directly from source provenance.  A separate raw-before-canonical zero-branch audit proved `z0 != 0` before any division by `z0`.

The resulting exact class-1 relation table is

| mask | `z2*z3/(p^2*z0)` | `z1*z8/(q^2*z0)` | `p^3` | `q^3` |
|---:|---:|---:|---|---|
| 0   | `-i` | `-i` | `(-1+i)/4` | `(-1-i)/4` |
| 105 | `+i` | `-i` | `(-1-i)/4` | `(-1-i)/4` |
| 150 | `-i` | `+i` | `(-1+i)/4` | `(-1+i)/4` |
| 255 | `+i` | `+i` | `(-1-i)/4` | `(-1+i)/4` |

In all four cases the fifth relation is

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

Hence each branch collapses to exactly

\[
3\times3\times2=18
\]

finite `(p,q,z0)` strata.

---

## 3. Universal finite-stratum geometry

Fresh exact census gives the same affine-rank split for all four class-1 masks:

\[
\boxed{18=10+8}.
\]

Ten strata have

\[
\operatorname{rank}=11,
\qquad
\dim_{\rm free}=9,
\]

force

\[
z_6=z_7=z_9=z_{10}=0,
\]

and are excluded by low-support final-pentagon target cells reducing to nonzero Laurent monomials in already-proved nonzero scale variables.

The remaining eight strata are exactly

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\}
\]

for both roots of the `z0` quadratic.  They have

\[
\operatorname{rank}=10,
\qquad
\dim_{\rm free}=10,
\]

with no affine forced zero.  In every mask the nonlinear residual core is two-dimensional in

\[
x=z_{19},\qquad y=z_{20}.
\]

This `50,880 -> 219 -> 18 -> 10+8 -> 2-variable core` compression therefore survives the newly discovered physical D-amplitude sheet.

---

## 4. Mask 0

Mask `0` was closed first on the second sheet.

The 18 finite branches split as `10+8`.  The eight rank-10 branches are excluded by source-validated local `g` cells:

- four branches by a three-cell resultant certificate with
  \[
  \operatorname{Res}_x(G_0,G_1)=-48y^4;
  \]
- four branches by a three-cell sign-split certificate using
  \[
  G_3-iG_2=4(1-i)(x-y)(x+y).
  \]

GitHub Actions run `32288052784` verifies the complete rank-10 closure.

See `notes/49-r22-second-d-sheet-component5-mask0-phase5-closure.md`.

---

## 5. Mask 105

Mask `105` exhibits a particularly uniform rank-drop obstruction.

For all eight rank-10 strata, fixed source cells

```text
G2 = (X,X,X,X;g)_(0,2)
G3 = (X,X,X,X;g)_(0,3)
H  = (X,X,X,X,X)_(2,23)
```

normalize to

\[
G_2=4xy-4y^2-1,
\qquad
G_3=4x^2-4xy+1.
\]

Thus

\[
G_2+G_3=4(x-y)(x+y).
\]

The slice `x=y` contradicts `G2`, so

\[
x=-y,
\qquad
y^2=-\frac18.
\]

Both exact signs

\[
y=\pm\frac{i\sqrt2}{4}
\]

were substituted directly into the source cell `H`; on all 16 sign subbranches `H` normalizes to the nonzero constant `1`.

GitHub Actions run `32311826537` reports

```text
rank10_closed = 8
rank10_total = 8
sign_subbranches_checked = 16
```

under this single fixed three-cell source family.

---

## 6. Mask 150

A fresh single-mask finite census independently reproduces

\[
18=10+8.
\]

The eight rank-10 strata have exactly the same normalized source models as mask `105`:

\[
G_2=4xy-4y^2-1,
\qquad
G_3=4x^2-4xy+1.
\]

The same fixed source cell

```text
H = (X,X,X,X,X)_(2,23)
```

again normalizes to `1` on both exact signs of every one of the eight strata.

Thus mask `150` is closed by the identical provenance-level three-cell family, not by an assumed chirality symmetry.

Fresh verification:

- finite census: Actions run `32361213085`;
- eight rank-10 certificates / 16 sign checks: Actions run `32361723088`.

---

## 7. Mask 255

Mask `255` again has the exact `10+8` finite split, but its two-variable phase geometry is a different local normal form.

Write

\[
C=(4-4i)xy+(4+4i)y^2+i,
\]

\[
D=(4-4i)x^2-(4+4i)xy+1.
\]

The source cells `G2,G3` are nonzero branch scalars times `C,D`.

### 7.1 Four off-diagonal/root branches

For `(a,b)=(2,1),(1,2)`, source cells `G0,G1` factor as

\[
G_0\sim(x+y)(x+(-1+2i)y),
\]

\[
G_1\sim(x-y)((2-i)x-iy).
\]

Their exact resultant is

\[
\boxed{\operatorname{Res}_x(G_0,G_1)=-48y^4}.
\]

A common zero therefore forces `y=0`, then `x=0`, while

\[
C(0,0)=i\ne0.
\]

These four strata are excluded by three cells.

### 7.2 Four diagonal/root branches

For `(a,b)=(1,1),(2,2)`,

\[
C-iD=-4(1+i)(x-y)(x+y).
\]

Thus `x=±y`.

On `x=y`, `C=0` gives

\[
y^2=-\frac{i}{8};
\]

on `x=-y`, it gives

\[
y^2=-\frac18.
\]

A fixed source cell `G0` is nonzero on both sign slices.  For `(1,1)` its exact values are

\[
\frac{\sqrt3-i}{4},
\qquad
-\frac34+\frac{\sqrt3}{4}i,
\]

and for `(2,2)` they are

\[
\frac{\sqrt3+i}{4},
\qquad
\frac34+\frac{\sqrt3}{4}i.
\]

Hence all four diagonal/root strata are excluded.

Fresh verification:

- finite census: Actions run `32361969716`;
- rank-10 source certificates: Actions run `32362530577`, reporting
  `closed=8,total=8` with four resultant and four sign-split certificates.

---

## 8. Component-5 second-sheet closure

Combining the four independent mask closures gives

\[
\boxed{
\mathcal C^{\mathrm{Phase5}}_{5,m,1}=\varnothing
\quad
\text{for every }m\in\{0,105,150,255\}.
}
\]

Therefore scalar component `5` has no invertible associator extension on the second physical D-amplitude sheet.

Since the accepted class-0 analysis already closes the first sheet,

\[
\boxed{\text{scalar component 5 is now D-amplitude complete at Phase 5}.}
\]

This is a theorem-audit closure statement for scalar component `5`; it is not yet the global `R(2,2)` non-categorifiability theorem.

---

## 9. Updated theorem frontier

The second physical D-amplitude sheet originally added

\[
4\text{ deep scalar components}\times4\text{ chirality masks}=16
\]

new Phase-5 branches.

Current class-1 closure ledger is now

\[
\boxed{
5:4/4,\qquad
7:4/4,\qquad
15:4/4,
}
\]

leaving only

\[
\boxed{
13/0,\quad13/105,\quad13/150,\quad13/255.
}
\]

Thus

\[
\boxed{12/16\text{ second-sheet branches are CLOSED / EXACT}.}
\]

The next research node is therefore the complete Phase-5 audit of scalar component `13` on D-amplitude class `1`.

No component-5 coordinate, local relation, or certificate should be imported into component `13` without a fresh source replay.
