# R(2,2) component 7 / mask 105 — Phase-5 exact closure

## Status

**CLOSED / EXACT.**

Scalar component `7`, chirality mask `105`, has no invertible associator extension satisfying the final four-noninvertible pentagons.

This is an independent fresh replay; the mask-0 result is not used as a premise.

## 1. Fresh kernel

The exact Phase-5 compiler gives the same macroscopic `17+4` geometry as mask 0:

- 17 active weighted F components;
- 19 kernel variables;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- degree profile: 1 linear, 2 quadratic, 144 cubic;
- no generic constant contradiction.

Fresh kernel replay: GitHub Actions run `32231056735`.

## 2. Coordinate stability

Named F coordinates were independently reconstructed under

```text
PYTHONHASHSEED = 1, 2, 17
```

with

```text
partition_variants = 1
target_variants    = 1
```

Coordinate-stability replay: run `32231265402`.

## 3. Two-cell exact contradiction

The fresh mask-105 source validator reads two fixed provenances directly:

```text
(XXXXX)_(0,0)   -> z0
(XXXX;1)_(0,0)  -> z0^2 - 1/2
```

Hence the pentagons require simultaneously

\[
z_0=0,
\qquad
z_0^2=\frac12,
\]

and therefore

\[
\boxed{-\frac12=0}.
\]

Source certificate:

```text
experiments/r22_phase5_component7_mask105_local_relations.py
```

GitHub Actions run `32231671110` reports

```text
P1 = z0
P2 = z0**2 - 1/2
contradiction = -1/2
closed = True
```

No localization, determinant argument, finite-stratum enumeration, residual solve, Gröbner basis, or floating-point computation is used.

## 4. Conclusion

\[
\boxed{\text{component 7 / mask 105 is non-categorifiable}.}
\]

The current component-7 boundary is

\[
\boxed{0,105\ \text{CLOSED};\qquad150,255\ \text{OPEN}.}
\]

Proceed next to mask `150` from a fresh kernel fingerprint.