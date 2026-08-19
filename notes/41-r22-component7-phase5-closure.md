# R(2,2) scalar component 7 — complete Phase-5 closure

## Status

**CLOSED / EXACT.**

All four Phase-1 chirality survivors of scalar component `7`,

\[
\boxed{0,105,150,255},
\]

are independently obstructed at the final four-noninvertible pentagon layer.

Therefore

\[
\boxed{\text{scalar component 7 is completely non-categorifiable at Phase 5}.}
\]

Mask-level proof audits:

- `notes/37-r22-component7-mask0-phase5-closure.md`;
- `notes/38-r22-component7-mask105-phase5-closure.md`;
- `notes/39-r22-component7-mask150-phase5-closure.md`;
- `notes/40-r22-component7-mask255-phase5-closure.md`.

## 1. The `17+4` Phase-4 geometry changes Phase 5 qualitatively

Components `5` and `13` reach Phase 5 with 21 active weighted F components. Component `7` reaches it with only 17 active weighted components because four F components are already forced to zero by the lower coherence equations.

Freshly compiling every surviving chirality mask of component `7` gives the same macroscopic final-kernel size:

- 96 final pentagon blocks;
- 56,448 scalar positions;
- 17 active F components;
- 19 kernel variables `p,q,z0,...,z16`;
- 15,744 support-two F-linear equations before quotienting;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- total-degree profile: 1 linear, 2 quadratic, 144 cubic relations;
- no generic constant contradiction.

Thus the `17+4` lower quotient removes four F coordinates and roughly one quarter of the raw final nonzero entries relative to the 21-free-component geometry.

## 2. Named-coordinate reproducibility was checked mask by mask

For each of the four masks, the F-component partition and a fixed final-pentagon target were independently reconstructed under

```text
PYTHONHASHSEED = 1, 2, 17
```

before any named `z_j` certificate was accepted.

The audits gave a single partition and a single target polynomial for each mask. Consequently the `z0` coordinate used in the obstruction below is not a hash/union-find naming accident within these tests.

## 3. One universal local obstruction

After the fresh kernel and coordinate audit, every chirality mask independently verifies exactly the same two fixed final-pentagon provenances.

First,

```text
(XXXXX)_(0,0)
```

is exactly proportional to

\[
\boxed{z_0}.
\]

Therefore

\[
\boxed{z_0=0}.
\]

Second,

```text
(XXXX;1)_(0,0)
```

is exactly proportional to

\[
\boxed{z_0^2-\frac12}.
\]

Therefore

\[
\boxed{z_0^2=\frac12}.
\]

Combining the two gives

\[
\boxed{-\frac12=0}.
\]

This contradiction is characteristic-zero exact and uses no localization or division.

## 4. Independent mask-level evidence

The masks were not inferred from one another.

### Mask 0

Fresh kernel, coordinate audit, and source certificate all pass. The source run `32230627427` gives

```text
P1 = z0
P2 = z0**2 - 1/2
contradiction = -1/2
closed = True
```

### Mask 105

Fresh kernel run `32231056735`, coordinate audit `32231265402`, and source certificate `32231671110` independently give the same exact two-cell contradiction.

### Mask 150

Fresh kernel run `32231957064`, coordinate audit `32232184182`, and source certificate `32232746046` independently give the same exact two-cell contradiction.

### Mask 255

Fresh kernel run `32233038719`, coordinate audit `32233338572`, and source certificate `32233649046` independently give the same exact two-cell contradiction.

## 5. Unified component-level replay

Only after all four masks had been independently established, the executable

```text
experiments/r22_phase5_component7_all_masks_two_cell_certificate.py
```

was added as a component-level theorem replay.

It recompiles the masks serially in the order

```text
0 -> 105 -> 150 -> 255
```

and checks the same two fixed provenances in each kernel.

GitHub Actions run `32233916428` reports

```text
mask 0    P1=z0  P2=z0**2-1/2  contradiction=-1/2  closed=True
mask 105  P1=z0  P2=z0**2-1/2  contradiction=-1/2  closed=True
mask 150  P1=z0  P2=z0**2-1/2  contradiction=-1/2  closed=True
mask 255  P1=z0  P2=z0**2-1/2  contradiction=-1/2  closed=True
SUMMARY closed=4,total=4
```

Hence the local obstruction is uniform across all four surviving chiralities of scalar component `7`.

## 6. Contrast with scalar component 13

The component-13 Phase-5 closure required the hierarchy

\[
50{,}880
\to219\text{ cubic relations}
\to18\text{ finite algebraic strata}
\to\text{affine rank stratification}
\to\text{one/two-variable residual cores}
\to\text{few-cell certificates}.
\]

Component `7` collapses much earlier:

\[
\boxed{
38{,}080
\to147\text{ relations}
\to2\text{ fixed final cells}
\to-\frac12=0.
}
\]

This is a genuine qualitative change in obstruction geometry.

A plausible interpretation is that the four F components already forced to zero in the `17+4` Phase-4 quotient place the associator data on a singular relation-space stratum where final coherence becomes locally inconsistent. This interpretation is a hypothesis suggested by the calculation; it is not needed for the exact proof above.

## 7. Current theorem boundary

Scalar components

\[
\boxed{5,7,13}
\]

are now completely obstructed at Phase 5.

The only remaining deep epsilon-minus scalar component is

\[
\boxed{15},
\]

with chirality masks

\[
\boxed{0,105,150,255}
\]

still requiring fresh Phase-5 analysis.

The global `R(2,2)` categorifiability theorem therefore remains open until component `15` is resolved.

## 8. Next gate

Proceed to scalar component `15`, chirality mask `0`, from a fresh Phase-5 kernel fingerprint.

Component `15` is also a `17 active + 4 forced-zero` Phase-4 type, so the component-7 two-cell obstruction is now a strong structural hypothesis. It must nevertheless be independently established rather than assumed.