# R(2,2) scalar component 13 — complete Phase-5 closure

## Status

**CLOSED / EXACT.**

All four Phase-1 chirality survivors of scalar component `13`,

\[
\boxed{0,105,150,255},
\]

are independently obstructed at the final four-noninvertible pentagon layer.

Therefore

\[
\boxed{\text{scalar component 13 is completely non-categorifiable at Phase 5}.}
\]

The mask-level proof audits are:

- `notes/32-r22-component13-mask0-phase5-closure.md`;
- `notes/33-r22-component13-mask105-phase5-closure.md`;
- `notes/34-r22-component13-mask150-phase5-closure.md`;
- `notes/35-r22-component13-mask255-phase5-closure.md`.

The final mask-255 eight-branch rank-10 replay is GitHub Actions run `32222771962`, which reports `closed=8,total=8` under one fixed three-cell certificate family.

## 1. Common Phase-5 scale

Every chirality was replayed from a fresh Phase-5 kernel rather than inferred from another mask. In all four cases the exact sparse compiler has the same macroscopic size:

- 96 final pentagon blocks;
- 56,448 scalar positions;
- 50,880 raw nonzero final entries;
- 23 kernel variables;
- 219 unique cubic kernel polynomials;
- no generic constant contradiction.

Thus the obstruction is not visible at the raw generic-kernel level.

The named F-coordinate charts differ substantially between chiralities. The finite-scale coordinates are:

```text
mask 0    -> z5
mask 105  -> z0
mask 150  -> z6
mask 255  -> z3
```

This coordinate motion is one reason no chirality closure was imported by naive conjugation or variable identity.

## 2. Four independently derived finite scale systems

### Mask 0

The exact local relations give a quadratic finite scale in `z5`, cubic constraints on `p,q`, and proved-nonzero product coordinates. All 18 finite branches are excluded. See note 32.

### Mask 105

\[
\boxed{z_0^2=\frac12},
\qquad
\boxed{p^3=q^3=\frac{1-i}{4}},
\]

\[
\boxed{z_3z_{10}=-ip^2z_0},
\qquad
\boxed{z_6z_9=-q^2z_0}.
\]

All 18 branches are excluded. See note 33.

### Mask 150

\[
\boxed{z_6^2=\frac12},
\qquad
\boxed{p^3=q^3=\frac{-1+i}{4}},
\]

\[
\boxed{z_0z_9=-p^2z_6},
\qquad
\boxed{z_1z_7=q^2z_6}.
\]

All 18 branches are excluded. See note 34.

### Mask 255

\[
\boxed{z_3^2=\frac12},
\qquad
\boxed{p^3=\frac{1-i}{4}},
\qquad
\boxed{q^3=\frac{-1+i}{4}},
\]

\[
\boxed{z_0z_4=i q^2z_3},
\qquad
\boxed{z_{17}z_{18}=-i p^2z_3}.
\]

All 18 branches are excluded. See note 35.

## 3. Stable finite-stratum geometry

For masks `105`, `150`, and `255`, the independently computed affine census is exactly

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

Mask `0` was obtained before this uniform census vocabulary was established, but it exhibits the same qualitative compression: a finite 18-branch algebraic problem followed by a small exceptional rank-drop family.

This repeated geometry is the central structural output of component 13. The detailed F-coordinate labels change, but the relation-space stratification is much more stable than the coordinates.

## 4. Rank-11 obstructions are local

The rank-11 strata retain an invertible F locus; their forced-zero coordinates are not by themselves determinant obstructions.

Nevertheless, after exact affine substitution, very small final pentagon cells close them.

Examples:

- mask 105 p-side: `(XXXX;Y)_(1,0) -> c*z3=0`, with `c != 0`, `z3 != 0`;
- mask 105 q-side: `(XXXX;X)_(5,2) -> c*z6=0`, with `c != 0`, `z6 != 0`;
- mask 150 p-side: `(XXXX;Y)_(1,0)` is a pure nonzero constant;
- mask 150 q-side: `(XXXX;X)_(2,5)` is a pure nonzero constant;
- mask 255 p-side: `(XXXX;X)_(5,2)` is a pure nonzero constant;
- mask 255 q-side: `(XXXX;Y)_(0,1)` is a pure nonzero constant.

Thus the obstruction becomes simpler after quotienting by the exact lower coherence relations.

## 5. Rank-10 obstruction cores are two-dimensional

The eight rank-10 branches repeatedly collapse to a two-variable residual core.

For masks `150` and `255`, the core is

\[
(r,s)=(z_{19},z_{20}).
\]

### Mask 150

The fixed cells

```text
(XXXX;g)_(0,3)
(XXXX;g)_(0,2)
(XXXX;g)_(0,0)
```

normalize the first two equations to

\[
1+4rs-4s^2=0,
\qquad
1+4rs-4r^2=0.
\]

Hence `r^2=s^2`. The two sign slices are excluded by the same local certificate family on all eight branches.

### Mask 255

The fixed cells

```text
(XXXX;g)_(0,3)
(XXXX;g)_(0,2)
(XXXX;g)_(0,1)
```

have difference

\[
A(s^2-r^2)=0,
\qquad A\ne0.
\]

Thus again `r=±s`. The two slices give exact square values `s^2=i/8` and `s^2=1/8`; the fixed third cell is nonzero on both exact points for every one of the eight branches.

Masks `0` and `105` likewise end in low-dimensional local nonlinear cores, though their precise coordinates and certificate forms differ.

## 6. Methodological compression

The component-13 computation repeatedly follows the hierarchy

\[
\boxed{
50{,}880\ \text{raw final entries}
\to
219\ \text{unique cubics}
\to
18\ \text{finite algebraic strata}
\to
\text{affine rank strata}
\to
\text{one- or two-variable residual core}
\to
\text{few-cell exact obstruction}.
}
\]

This is stronger than a successful brute-force solve. The decisive information appears only after moving from the raw representation space to a much smaller exact relation space.

The recurrence of the same finite-stratum geometry across independently replayed chirality masks suggests that the Phase-5 obstruction has a coordinate-independent structural description that has not yet been extracted as a theorem.

That structural extraction is a later task; it is not used as a premise for the current closure.

## 7. Final theorem boundary

Scalar components `5` and `13` are now completely closed:

\[
\boxed{5\ \text{CLOSED},\qquad13\ \text{CLOSED}.}
\]

The remaining deep epsilon-minus scalar components are

\[
\boxed{7,15},
\]

with chirality masks

\[
\boxed{0,105,150,255}
\]

still requiring Phase-5 analysis.

The global categorifiability theorem for `R(2,2)` therefore remains open.

## 8. Next research gate

Proceed to scalar component `7`, chirality mask `0`, from a fresh Phase-5 kernel fingerprint.

Component `7` is the first `17 free + 4 forced-zero` Phase-4 type, unlike components `5` and `13`, which have 21 free F components. Therefore no component-13 finite-scale coordinate, 18-branch split, or local certificate is authorized as an assumption.

The first question is structural:

\[
\boxed{\text{does the component-13 relation-space compression survive the 17+4 Phase-4 geometry?}}
\]

Only fresh exact replay can answer it.
