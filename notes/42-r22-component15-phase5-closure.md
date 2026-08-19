# R(2,2) scalar component 15 — complete Phase-5 closure

## Status

**CLOSED / EXACT.**

All four Phase-1 chirality survivors of scalar component `15`,

\[
\boxed{0,105,150,255},
\]

are independently obstructed at the final four-noninvertible pentagon layer.

Therefore

\[
\boxed{\text{scalar component 15 is completely non-categorifiable at Phase 5}.}
\]

This closes the last deep epsilon-minus scalar component. A theorem-level claim for the full fusion ring is deliberately deferred until the accepted Phase-1–4 branch exhaustion, epsilon-plus obstruction, and all Phase-5 component closures have been replayed together from fresh state.

## 1. Fresh Phase-5 geometry

Component `15` is a `17 active + 4 coherence-forced-zero` Phase-4 type, like component `7`.

Fresh compilation of the surviving masks gives the same macroscopic kernel fingerprint in every case:

- 96 final pentagon blocks;
- 56,448 scalar positions;
- 17 active weighted F components;
- 19 kernel variables (`p,q` plus 17 active F coordinates);
- 15,744 support-two F-linear equations before quotienting;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- total-degree profile: 1 linear, 2 quadratic, 144 cubic relations;
- no generic constant contradiction.

No Gröbner basis, global nonlinear solve, floating-point root search, or numerical continuation is used.

## 2. Methodological correction: prove the relation, not the `z_j` name

During the mask-150 audit, a red-team check exposed a weakness in the earlier named-coordinate reproducibility probe.

`r22_phase5_coordinate_stability.py` reconstructed the F-component partition and the fixed target pentagon polynomial in two independent quotient builds inside the same subprocess. Since weighted-union-find root identifiers are implementation representatives rather than mathematical invariants, a second build can permute the active-coordinate names even when the underlying partition and relation are unchanged.

Consequently a statement such as

```text
this fixed cell is always z_j
```

is stronger than that probe actually certifies.

This does **not** create a mathematical branch or alter the pentagon equations. It means only that hard-coded `z_j` labels should not be part of the theorem interface.

The closure therefore introduces

```text
experiments/r22_phase5_two_cell_certificate.py
```

as the canonical source certificate. For each fresh kernel it:

1. locates two fixed pentagon cells by provenance;
2. discovers the active F coordinate `s` appearing in the first cell;
3. verifies that the first relation is exactly `s=0`;
4. verifies that the second relation is exactly `s^2-1/2=0`;
5. derives the characteristic-zero contradiction `-1/2=0`.

The proof depends on the two source cells and their algebraic relation, not on the incidental coordinate name assigned to `s`.

## 3. The two fixed source cells

For every surviving chirality, the same two final-pentagon provenances are used:

```text
(XXXXX)_(0,0)
(XXXX;1)_(0,0)
```

In each independently compiled kernel the first cell has the form

\[
\boxed{s=0},
\]

where `s` is one active F-component coordinate discovered from that kernel.

The second cell has the form

\[
\boxed{s^2-\frac12=0}.
\]

Hence

\[
\boxed{-\frac12=0}.
\]

This contradiction uses no division or localization.

## 4. Mask-level exact checks

### Mask 0

The final fresh component-level replay discovers

```text
scale = z6
P1 = z6
P2 = z6**2 - 1/2
contradiction = -1/2
closed = True
```

### Mask 105

The final fresh component-level replay discovers

```text
scale = z2
P1 = z2
P2 = z2**2 - 1/2
contradiction = -1/2
closed = True
```

The earlier direct source run `32236706412` also closed this mask; the final replay supersedes any theorem-level dependence on its hard-coded coordinate name.

### Mask 150

Fresh kernel run `32254426038` gives the common `17 / 19 / 38080 / 147` fingerprint.

Coordinate-free source run `32255085536` executes the certificate in four fresh processes: the default hash environment and `PYTHONHASHSEED=1,2,17`. Every process independently discovers

```text
scale = z5
P1 = z5
P2 = z5**2 - 1/2
contradiction = -1/2
closed = True
```

### Mask 255

Fresh kernel run `32255740415` again gives the common fingerprint.

Coordinate-free source run `32255927111` executes the certificate in four fresh processes. Every process independently discovers

```text
scale = z8
P1 = z8
P2 = z8**2 - 1/2
contradiction = -1/2
closed = True
```

The different scale names across masks are immaterial: the fixed provenance pair and the relation pattern are the invariant content.

## 5. Fresh four-mask component replay

After the four masks had been established, GitHub Actions run

```text
32256425671
```

serially recompiles

```text
0 -> 105 -> 150 -> 255
```

with the coordinate-free verifier. It reports:

```text
mask 0    scale=z6  P1=z6  P2=z6**2-1/2  contradiction=-1/2  closed=True
mask 105  scale=z2  P1=z2  P2=z2**2-1/2  contradiction=-1/2  closed=True
mask 150  scale=z5  P1=z5  P2=z5**2-1/2  contradiction=-1/2  closed=True
mask 255  scale=z8  P1=z8  P2=z8**2-1/2  contradiction=-1/2  closed=True
```

Each fresh kernel has 19 variables and 147 unique kernel polynomials.

Therefore

\[
\boxed{\text{scalar component 15 is completely obstructed at Phase 5}.}
\]

## 6. Structural observation

Components `7` and `15` are both `17+4` Phase-4 types, and both expose the same pair of fixed final-pentagon provenances as a two-cell obstruction.

This strongly suggests a more invariant statement: the `17+4` quotient geometry may force a provenance-local relation pair

\[
s=0,\qquad s^2=\frac12,
\]

independently of chirality and of the implementation coordinate chart.

That interpretation is a structural hypothesis, not an additional premise of the component-15 proof. Before using it at theorem level, component `7` should be replayed with the new coordinate-free verifier as part of the global closure pass.

## 7. Theorem boundary after component 15

The epsilon-minus deep scalar components are

\[
\boxed{5,7,13,15}.
\]

All four now have accepted Phase-5 obstruction certificates on the research branch. The epsilon-plus half was independently excluded earlier.

This is sufficient to open the **theorem-closure audit**, but not yet to promote the global statement to accepted `main` state.

The remaining obligations are procedural and proof-global rather than new local branch search:

1. replay component `7` with the coordinate-free two-cell verifier;
2. fresh-replay the accepted component `5` and `13` closure certificates;
3. fresh-replay the epsilon-plus obstruction and the canonical Phase-1–4 branch-exhaustion chain;
4. audit that the union of these cases is exhaustive;
5. only then write and promote the theorem-level `R(2,2)` synthesis.

## 8. SCM boundary

This note closes only scalar component `15`.

After its PR is merged, theorem-level work should begin from the resulting `main` commit on a fresh branch. No global non-categorifiability claim is promoted merely from this component-local closure.