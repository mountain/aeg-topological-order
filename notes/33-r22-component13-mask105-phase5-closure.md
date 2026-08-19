# R(2,2) Phase-5 closure: scalar component 13, chirality mask 105

## Status

**CLOSED / EXACT.**

For scalar component `13` and chirality mask `105`, every Phase-5 finite branch is rigorously excluded by serial exact replay. No Gröbner basis, floating-point root search, numerical continuation, or global nonlinear solve is used.

The final branch accounting is

\[
\boxed{18=2+4+4+8=18\ \text{closed}.}
\]

The four classes are:

1. two affine-inconsistent finite branches;
2. four p-side rank-11 branches, each excluded by one local pentagon cell;
3. four q-side rank-11 branches, each excluded by one local pentagon cell;
4. eight rank-10 branches, each excluded by the same three fixed residual cells after exact two-variable elimination.

This closes **component 13 / mask 105 only**. Together with `notes/32-r22-component13-mask0-phase5-closure.md`, masks `0` and `105` are now closed; masks `150` and `255` remain open at this checkpoint.

---

## 1. Fresh Phase-5 kernel

Mask `105` was started from a fresh final-kernel compilation rather than importing mask-0 coordinates or relations.

The exact sparse kernel has:

- 96 final pentagon blocks;
- block dimensions `32 x 10`, `32 x 8`, `32 x 40`;
- 56,448 scalar positions;
- 50,880 raw nonzero final entries;
- two E-torus parameters `p,q`;
- 21 F-linear components;
- 23 kernel variables;
- 219 unique exact kernel polynomials;
- all 219 of total degree 3;
- F-degree profile `57 x degree-2 + 162 x degree-3`;
- no direct constant contradiction.

Although the aggregate kernel dimensions match other component-13/component-5 branches, the shortest equations use a different coordinate core, so no cross-mask coordinate identification was assumed.

GitHub Actions run: `32202206303`.

---

## 2. Coordinate reproducibility

The Phase-4 F quotient was rebuilt in independent Python processes with

```text
PYTHONHASHSEED = 1, 2, 17.
```

For component 13 / mask 105:

```text
partition_variants = 1
target_variants    = 1
```

Thus the named coordinates used below are reproducible across the tested hash seeds.

GitHub Actions run: `32202406688`.

---

## 3. Five exact local relations

Five short final-pentagon entries were independently validated by provenance:

\[
(XXXX;X)_{(0,0)},\quad
(XXXX;X)_{(0,2)},\quad
(XXXX;Y)_{(0,18)},\quad
(XXXX;Y)_{(18,18)},\quad
(XXXX;1)_{(0,0)}.
\]

They give

\[
p^2z_0-i z_3z_{10}=0,
\]

\[
pz_3z_{10}+\frac{1+i}{4}z_0=0,
\]

\[
qz_6z_9+\frac{1-i}{4}z_0=0,
\]

\[
q^2z_0+z_6z_9=0.
\]

The fifth cell, combined with the second and third by polynomial addition only, yields

\[
\boxed{2z_0^2-1=0}.
\]

Therefore

\[
\boxed{z_0^2=\frac12},
\qquad z_0\ne0.
\]

Exact polynomial combinations then give

\[
\boxed{p^3=q^3=\frac{1-i}{4}},
\]

and the product identities

\[
\boxed{z_3z_{10}=-ip^2z_0},
\qquad
\boxed{z_6z_9=-q^2z_0}.
\]

Hence

\[
\boxed{p,q,z_0,z_3,z_6,z_9,z_{10}\ne0}.
\]

Unlike component-13/mask-0, where the finite scale variable is `z5`, mask 105 has `z0` as the finite scale variable.

GitHub Actions run: `32202828165`.

---

## 4. Exact finite-stratum census

Since

\[
p^3=q^3=\frac{1-i}{4},\qquad z_0=\pm\frac{\sqrt2}{2},
\]

the finite scale space again contains

\[
3\times3\times2=18
\]

branches.

The proved-nonzero product relations safely eliminate `z10` and `z9`, localizing only at the already-proved nonzero coordinates `z3` and `z6`. The exact affine census over

\[
K=\mathbf Q(i,\sqrt2,\sqrt3)
\]

gives

\[
\boxed{18=2+4+4+8}.
\]

### A. Two affine-inconsistent branches

\[
(a,b)=(0,0),\qquad z_0=\pm\frac{\sqrt2}{2}.
\]

Both are closed immediately.

### B. Four p-side rank-11 branches

\[
(a,b)\in\{(1,0),(2,0)\},\qquad z_0=\pm\frac{\sqrt2}{2}.
\]

They have affine rank 11 and force

\[
z_7=z_8=0.
\]

### C. Four q-side rank-11 branches

\[
(a,b)\in\{(0,1),(0,2)\},\qquad z_0=\pm\frac{\sqrt2}{2}.
\]

They have affine rank 11 and force

\[
z_{17}=z_{18}=0.
\]

### D. Eight rank-10 branches

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\},\qquad z_0=\pm\frac{\sqrt2}{2}.
\]

They have affine rank 10 and no forced-zero F coordinate at this stage.

GitHub Actions run: `32203012964`.

---

## 5. Forced zeros do not themselves kill required F invertibility

The two rank-11 zero patterns

\[
(z_7,z_8)=(0,0),
\qquad
(z_{17},z_{18})=(0,0)
\]

were tested against the exact determinant polynomials of all 16 required F blocks.

Neither pattern kills any required determinant identically. The minimum number of surviving determinant monomials is 123, and the `XXXX` determinant retains 174 monomials in both cases.

Therefore these eight branches require final-pentagon residual certificates rather than a determinant obstruction.

GitHub Actions run: `32203250230`.

---

## 6. p-side rank-11 closure: one fixed cell

A representative p-side branch first exposed a singleton residual in the already-proved nonzero scale coordinate `z3`.

The fixed provenance is

\[
\boxed{(XXXX;Y)_{(1,0)}}.
\]

Fresh replay of all four p-side branches gives

\[
\left(1+\frac{\sqrt2}{2}\right)z_3=0
\]

for the positive `z0` branches and

\[
\left(1-\frac{\sqrt2}{2}\right)z_3=0
\]

for the negative `z0` branches.

Both coefficients are nonzero, while `z3 != 0` was already established by the local-scale relations. Hence all four p-side branches are excluded.

- representative residual scan: `32203444501`;
- four-branch fixed-cell replay: `32203630712`.

---

## 7. q-side rank-11 closure: one fixed cell

The q-side representative independently exposes a singleton in the proved-nonzero scale coordinate `z6`.

The fixed provenance is

\[
\boxed{(XXXX;X)_{(5,2)}}.
\]

Across all four q-side branches the residual is

\[
\left(-1+\frac{\sqrt2}{2}\right)z_6=0
\]

for positive `z0`, and

\[
\left(-1-\frac{\sqrt2}{2}\right)z_6=0
\]

for negative `z0`.

Both coefficients are nonzero and `z6 != 0`; hence all four q-side branches are excluded.

- representative residual scan: `32203800676`;
- four-branch fixed-cell replay: `32203963052`.

---

## 8. Rank-10 residual geometry

For the representative rank-10 branch

\[
(a,b,z_0)=(1,1,+\sqrt2/2),
\]

the exact affine quotient leaves

```text
z3, z4, z5, z6, z16, z18, z19, z20
```

free.

There are 175 unique residual polynomials, with no constant contradiction and no univariate equation. However, 17 residual equations lie entirely in the two-variable core

\[
r=z_{16},\qquad s=z_{18}.
\]

The representative residual scan is Actions run `32204163082`.

---

## 9. Rank-10 exact bivariate certificate

Fix the same three residual provenance cells on every rank-10 branch:

\[
P_1=(XXXX;g)_{(0,3)},
\]

\[
P_2=(XXXX;g)_{(0,2)},
\]

\[
P_3=(XXXX;g)_{(0,0)}.
\]

For the representative branch, exact elimination gives

\[
P_1+P_2=s(a+bs),
\qquad a\ne0,\ b\ne0.
\]

Thus there are exactly two `s` candidates:

\[
s=0,
\qquad
s=-a/b.
\]

For each value, `P1` is affine in `r` with nonzero coefficient and gives one exact `r`. In the representative branch the candidates are

\[
(r,s)=\left(-\frac{i\sqrt2}{4},0\right)
\]

and

\[
(r,s)=\left(\frac{i\sqrt2}{4},
-\frac{\sqrt2}{4}+\frac{i\sqrt2}{4}
+\frac{\sqrt6}{4}+\frac{i\sqrt6}{4}\right).
\]

The fixed third residual `P3` evaluates to the same nonzero exact value at both candidates:

\[
\frac{3-i+\sqrt3-i\sqrt3}{16}\ne0.
\]

Thus the representative branch is closed by three residual cells, with no multivariate Gröbner computation.

Representative bivariate probe: `32204438523`.

---

## 10. All eight rank-10 branches: same three fixed cells

The same algorithm was then replayed independently on each of the eight rank-10 branches:

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\},
\qquad z_0=\pm\frac{\sqrt2}{2}.
\]

For every branch:

1. `P1+P2` has exactly the form `s*(a+b*s)` with both coefficients nonzero;
2. the two exact candidate points solve `P1=P2=0`;
3. the fixed third residual `P3=(XXXX;g)_(0,0)` is nonzero at both candidates.

No branch is allowed to substitute a different third equation.

The exact third values vary by cube-root sector, for example:

\[
\frac{3-i+\sqrt3-i\sqrt3}{16},
\qquad
\frac{i-\sqrt3}{8},
\qquad
\frac{i+\sqrt3}{8},
\qquad
\frac{3-i-\sqrt3+i\sqrt3}{16},
\]

and are nonzero in every case.

The final replay reports

```text
SUMMARY {'closed': 8, 'total': 8,
         'cells': ((XXXX;g)_(0,3), (XXXX;g)_(0,2), (XXXX;g)_(0,0))}
RESULT: all eight component-13/mask-105 rank-10 strata are excluded
        by the same three residual cells
```

GitHub Actions run: `32204615272`.

---

## 11. Final branch accounting

The 18 finite branches are exhausted:

\[
\boxed{
18
=
2_{\rm affine}
+4_{\rm p\text{-}rank11}
+4_{\rm q\text{-}rank11}
+8_{\rm rank10}
=18_{\rm closed}.
}
\]

Therefore

\[
\boxed{\text{component 13 / chirality mask 105 is obstructed at Phase 5}.}
\]

Equivalently, this Phase-1 survivor admits no invertible associator extension satisfying all final pentagons.

Together with mask 0, component 13 is now closed on two of its four Phase-1 chirality survivors:

\[
\boxed{0,105\ \text{CLOSED};\qquad150,255\ \text{OPEN}.}
\]

This is **not** yet a scalar-component-13 closure and **not** a global non-categorifiability theorem for `R(2,2)`.

---

## 12. Reproducible implementation

Principal exact probes introduced or used for mask 105:

- `experiments/r22_epsminus_final_kernel.py`;
- `experiments/r22_phase5_coordinate_stability.py`;
- `experiments/r22_phase5_component13_mask105_local_relations.py`;
- `experiments/r22_phase5_component13_mask105_finite_census.py`;
- `experiments/r22_phase5_component13_mask105_forced_zero_invertibility.py`;
- `experiments/r22_phase5_component13_mask105_residual_scan.py`;
- `experiments/r22_phase5_component13_mask105_p_rank11_certificate.py`;
- `experiments/r22_phase5_component13_mask105_q_rank11_certificate.py`;
- `experiments/r22_phase5_component13_mask105_rank10_bivariate_probe.py`;
- `experiments/r22_phase5_component13_mask105_rank10_certificate.py`.

The workflow stayed under the 10-minute per-job guardrail and followed serial branch validation throughout.

---

## 13. Next frontier

The next branch is

\[
\boxed{\text{component 13 / chirality mask 150}.}
\]

It must begin with a fresh Phase-5 kernel fingerprint. Mask-105 coordinate identities, finite-stratum split, one-cell rank-11 certificates, and the rank-10 bivariate certificate must not be imported until independently verified for mask 150.
