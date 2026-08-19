# R(2,2) Phase-5 closure: scalar component 13, chirality mask 0

## Status

**CLOSED / EXACT.**

For scalar component `13` and chirality mask `0`, every Phase-5 finite branch is rigorously excluded. No Gröbner basis, floating-point root search, numerical continuation, or global nonlinear solve is used.

The final branch accounting is

\[
\boxed{18=2+4+4+8=18\ \text{closed}.}
\]

The four classes are:

1. two affine-inconsistent finite branches;
2. four p-side rank-11 branches, each excluded by one local pentagon cell;
3. four q-side rank-11 branches, each excluded by one local pentagon cell;
4. eight rank-10 branches, each excluded by the same three local `g`-cells.

This closes **component 13 / mask 0 only**. Component-13 masks `105`, `150`, and `255` remain open at this checkpoint.

---

## 1. Fresh Phase-5 kernel

The component-13/mask-0 kernel was compiled from the accepted Phase-1--4 quotient without importing component-5 local relations or branch geometry.

The fresh exact sparse kernel has:

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

The numerical fingerprint matches the size of component 5, but the shortest local relations involve different F coordinates. Therefore no component-5 coordinate identification was assumed.

GitHub Actions run: `32177845432`.

---

## 2. Coordinate reproducibility

Before accepting any certificate written in named coordinates `z_j`, the Phase-4 F quotient was rebuilt in independent Python processes with

```text
PYTHONHASHSEED = 1, 2, 17.
```

For component 13 / mask 0:

```text
partition_variants = 1
target_variants    = 1
```

Thus the current `z_j` naming is reproducible across the tested hash seeds, including the coordinates used below.

GitHub Actions run: `32178137814`.

---

## 3. Five exact local relations

Five short final-pentagon entries were located by provenance and validated directly against the fresh kernel:

\[
(XXXX;X)_{(0,0)},\quad
(XXXX;X)_{(0,2)},\quad
(XXXX;Y)_{(0,18)},\quad
(XXXX;Y)_{(18,18)},\quad
(XXXX;1)_{(0,0)}.
\]

They yield the exact local model

\[
p^2z_5-i z_0z_6=0,
\]

\[
pz_0z_6+\frac{1-i}{4}z_5=0,
\]

\[
qz_{11}z_{14}+\frac{1-i}{4}z_5=0,
\]

\[
q^2z_5+z_{11}z_{14}=0.
\]

The fifth cell, combined only by polynomial addition/subtraction with the preceding local cells, gives

\[
\boxed{2z_5^2-1=0}.
\]

Hence

\[
\boxed{z_5^2=\frac12},
\]

and the p/q scale equations reduce to

\[
\boxed{p^3=-\frac{1+i}{4}},
\qquad
\boxed{q^3=\frac{1-i}{4}}.
\]

The two product identities are

\[
\boxed{z_0z_6=-ip^2z_5},
\qquad
\boxed{z_{11}z_{14}=-q^2z_5}.
\]

Therefore

\[
\boxed{p,q,z_0,z_5,z_6,z_{11},z_{14}\ne0}.
\]

This is the key geometric difference from component 5: here `z5` is the finite scale variable, while `z0` and `z11` are proved nonzero scale coordinates.

### Verification incident

The first source-validation attempt intentionally failed because the fourth relation had been manually transcribed as

\[
q^2z_5+i z_{11}z_{14}=0,
\]

while the raw kernel actually gives

\[
q^2z_5+z_{11}z_{14}=0.
\]

The serial gate stopped before any finite-stratum analysis. The model was corrected and the same source-validation gate was rerun successfully. This failure is part of the audit history rather than evidence for the theorem.

- failed source gate: `32178662435`;
- corrected successful source gate: `32178876094`.

---

## 4. Exact finite-stratum census

Since

\[
p^3=-\frac{1+i}{4},\qquad q^3=\frac{1-i}{4},\qquad z_5=\pm\frac{\sqrt2}{2},
\]

the finite local scale space contains

\[
3\times3\times2=18
\]

branches.

After safely eliminating `z6` and `z14` using the proved-nonzero product identities, and localizing only at already-proved nonzero coordinates, the exact affine census over

\[
K=\mathbf Q(i,\sqrt2,\sqrt3)
\]

gives the new stratification

\[
\boxed{18=2+8+8}.
\]

More explicitly:

### A. Two affine-inconsistent branches

\[
(a,b)=(0,0),\qquad z_5=\pm\frac{\sqrt2}{2}.
\]

Both exact affine systems are inconsistent and therefore closed immediately.

### B. Four p-side rank-11 branches

\[
(a,b)\in\{(1,0),(2,0)\},\qquad z_5=\pm\frac{\sqrt2}{2}.
\]

They have affine rank 11 and force

\[
z_{12}=z_{13}=0.
\]

### C. Four q-side rank-11 branches

\[
(a,b)\in\{(0,1),(0,2)\},\qquad z_5=\pm\frac{\sqrt2}{2}.
\]

They have affine rank 11 and force

\[
z_7=z_8=0.
\]

### D. Eight rank-10 branches

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\},\qquad z_5=\pm\frac{\sqrt2}{2}.
\]

They have affine rank 10 and no forced-zero F coordinate at this stage.

GitHub Actions run: `32179104968`.

---

## 5. Forced zeros do not by themselves kill F invertibility

The two rank-11 forced-zero patterns were checked against the exact generic determinant polynomials of all 16 required F blocks.

For both

\[
(z_{12},z_{13})=(0,0)
\]

and

\[
(z_7,z_8)=(0,0),
\]

no required determinant is identically killed. The minimum number of surviving determinant monomials over the required blocks is 123.

Therefore these eight branches cannot be excluded merely from the affine forced-zero information.

GitHub Actions run: `32179512950`.

---

## 6. p-side rank-11 closure: one cell

A representative p-side branch was first reduced through its complete affine quotient. The residual kernel immediately exposed a singleton equation in the already-proved nonzero scale coordinate `z0`.

The provenance is

\[
\boxed{(XXXX;Y)_{(1,0)}}.
\]

For all four p-side branches, fresh branch-by-branch replay gives

\[
c_\pm z_0=0,
\]

with

\[
c_+=1+\frac{\sqrt2}{2},
\qquad
c_-=1-\frac{\sqrt2}{2},
\]

up to the exact branch normalization used by the sparse field implementation. Both coefficients are nonzero.

Since `z0 != 0` was already proved from the five local relations, all four p-side rank-11 branches are excluded.

- representative residual scan: `32179946874`;
- four-branch certificate replay: `32180234988`.

---

## 7. q-side rank-11 closure: one cell

A representative q-side branch was independently reduced through the affine quotient. Its shortest obstruction uses the different provenance

\[
\boxed{(XXXX;X)_{(5,2)}}.
\]

For all four q-side branches, exact replay gives

\[
d_\pm z_{11}=0,
\]

where the branch coefficients are nonzero exact elements of

\[
\mathbf Q(i,\sqrt2).
\]

For example, for `(a,b,z5-sign)=(0,1,+)`:

\[
d_+=-\frac{1+i}{2}+\frac{1+i}{4}\sqrt2\ne0.
\]

Since `z11 != 0` was already proved, all four q-side rank-11 branches are excluded.

- representative residual scan: `32180660985`;
- four-branch certificate replay: `32180891662`.

---

## 8. Rank-10 closure: a universal three-cell core

For the representative branch

\[
(a,b,z_5)=(1,1,+\sqrt2/2),
\]

the exact affine quotient leaves free variables

```text
z0, z9, z10, z11, z17, z18, z19, z20.
```

The shortest nonlinear core localizes to

\[
r=z_{17},\qquad s=z_{18}.
\]

Use the three fixed cells

\[
G_0=(XXXX;g)_{(0,0)},
\]

\[
G_2=(XXXX;g)_{(0,2)},
\]

\[
G_3=(XXXX;g)_{(0,3)}.
\]

For every one of the eight rank-10 finite branches, exact replay establishes

\[
G_2-G_3=A(r^2-s^2),\qquad A\ne0.
\]

Therefore

\[
r=\pm s.
\]

On each of these two sign slices, `G0` becomes

\[
G_0=H_\pm s^2,
\qquad H_\pm\ne0,
\]

so `G0=0` forces

\[
s=0.
\]

But on the same sign slice, `G2` retains a nonzero constant term. Hence `G2=0` is impossible at `s=0`.

Thus the three cells form a complete local obstruction certificate for every rank-10 branch.

The final all-branch replay reports

```text
SUMMARY {'closed': 8, 'total': 8,
         'cells': ((XXXX;g)_(0,0), (XXXX;g)_(0,2), (XXXX;g)_(0,3))}
RESULT: all eight component-13/mask-0 rank-10 strata are excluded
        by the same three local g-cells
```

- representative rank-10 residual scan: `32181248837`;
- representative three-cell certificate: `32181593397`;
- complete 8/8 three-cell replay: `32181956600`.

---

## 9. Final branch accounting

The 18 finite branches are now exhausted:

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
\boxed{\text{component 13 / chirality mask 0 is obstructed at Phase 5}.}
\]

Equivalently, this Phase-1 survivor admits no invertible associator extension satisfying all final pentagons.

This statement does **not** yet close scalar component 13 as a whole and does **not** imply the global non-categorifiability of `R(2,2)`.

---

## 10. Reproducible implementation

The principal exact probes are:

- `experiments/r22_epsminus_final_kernel.py`;
- `experiments/r22_phase5_coordinate_stability.py`;
- `experiments/r22_phase5_component13_mask0_local_relations.py`;
- `experiments/r22_phase5_component13_mask0_finite_census.py`;
- `experiments/r22_phase5_component13_mask0_forced_zero_invertibility.py`;
- `experiments/r22_phase5_component13_mask0_residual_scan.py`;
- `experiments/r22_phase5_component13_mask0_p_rank11_certificate.py`;
- `experiments/r22_phase5_component13_mask0_q_rank11_certificate.py`;
- `experiments/r22_phase5_component13_mask0_rank10_representative_certificate.py`;
- `experiments/r22_phase5_component13_mask0_rank10_certificate.py`.

The workflow remained under the 10-minute per-job guardrail and used serial research gates rather than concurrent branch closure.

---

## 11. Next frontier

The next branch is

\[
\boxed{\text{component 13 / chirality mask 105}.}
\]

It must begin with a fresh Phase-5 kernel fingerprint. In particular, the mask-0 identities involving `z5`, the `18=2+8+8` stratification, and the three-cell rank-10 certificate must not be imported until independently verified for mask 105.
