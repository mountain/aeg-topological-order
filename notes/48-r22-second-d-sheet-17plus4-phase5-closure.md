# R(2,2) theorem audit — second D sheet, 17+4 Phase-5 closure

**Status:** `EXACT / COMPONENTS 7 AND 15, D-CLASS 1, ALL MASKS CLOSED`

The theorem audit found a second gauge-inequivalent D-amplitude class on every
deep epsilon-minus scalar/chirality branch.  Notes 46 and 47 showed that this
second sheet passes the complete E and parametric F-linear layers and reproduces
the same two Phase-4 structural types as the historical sheet.

This note records the first Phase-5 closure on the new sheet: all eight branches
belonging to the `17 active + 4 coherence-forced-zero` type are excluded by the
same fixed two final-pentagon provenances used on the first D sheet.

## 1. Shared exact compiler

No second nonlinear compiler was created.  The class-1 facade

```text
experiments/r22_phase5_torsion_sheet.py
```

injects second-sheet lower data into the accepted
`r22_epsminus_final_kernel.py` compiler and restores the historical provider
after each process-local run.  The monomial lift and coordinate-free two-cell
verifier are therefore shared verbatim by both D sheets.

## 2. Fresh component-7 nonlinear fingerprint

Before any certificate propagation, component `7`, mask `0`, D class `1` was
fresh-compiled through all 96 final pentagon blocks.

The kernel is exactly of the historical `17+4` size:

```text
F linear components          = 17
kernel variables             = 19 = p,q,z0,...,z16
final scalar positions       = 56448
raw nonzero final entries    = 38080
unique kernel polynomials    = 147
constant contradictions      = 0
```

The term profile is

```text
1 term  : 2
2 terms : 1
7 terms : 12
8 terms : 16
9 terms : 20
10 terms: 96
```

and the degree profile is

\[
1\times1 + 2\times2 + 144\times3.
\]

GitHub Actions run: `32283952644`.

## 3. Coordinate-free certificate

For every audited branch, the verifier locates two cells by provenance:

\[
P_1=(X,X,X,X,X)_{(0,0)},
\]

\[
P_2=(X,X,X,X,1)_{(0,0)}.
\]

It does not assume a `z_j` name.  It first requires `P1` to be one monic active
F coordinate `s`, then independently requires `P2` to be

\[
s^2-\frac12.
\]

Thus the two pentagons imply

\[
s=0,
\qquad
s^2=\frac12,
\]

and therefore the exact contradiction

\[
\boxed{-\frac12=0}.
\]

## 4. Component 7, D class 1

All four chirality masks replay fresh and close:

```text
mask 0   : s = z0
mask 105 : s = z0
mask 150 : s = z0
mask 255 : s = z0
```

Every branch has 19 kernel variables and 147 unique polynomials.

GitHub Actions run: `32284518200`.

Hence

\[
\boxed{\text{component 7 / D class 1 is Phase-5 obstructed}.}
\]

## 5. Component 15, D class 1

All four chirality masks replay independently and close:

```text
mask 0   : s = z7
mask 105 : s = z2
mask 150 : s = z5
mask 255 : s = z8
```

Again every branch has 19 kernel variables and 147 unique polynomials.  The
coordinate variation confirms why provenance, rather than a hard-coded `z_j`,
is the correct theorem-level certificate.

GitHub Actions run: `32285195233`.

Hence

\[
\boxed{\text{component 15 / D class 1 is Phase-5 obstructed}.}
\]

## 6. Updated second-sheet frontier

The new D sheet began with sixteen deep scalar/chirality branches.  Phase 5 has
now removed all eight `17+4` branches:

\[
\boxed{7,15\ \text{closed on all four masks}.}
\]

The only remaining new-sheet frontier is

\[
\boxed{\text{components }5,13\times\text{masks }0,105,150,255},
\]

eight branches of the 21-active-F-component type.

Do not import the historical component-5/13 finite-stratum certificates by
assumption.  The next gate is a fresh nonlinear kernel for

\[
\boxed{\text{component 5 / mask 0 / D class 1}.}
\]

Its short local relations and finite scale stratification must be reconstructed
from source provenance before any old-sheet branch geometry is reused.
