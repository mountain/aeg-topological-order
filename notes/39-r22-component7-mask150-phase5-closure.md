# R(2,2) component 7 / mask 150 — Phase-5 exact closure

## Status

**CLOSED / EXACT.**

Scalar component `7`, chirality mask `150`, has no invertible associator extension satisfying the final four-noninvertible pentagons.

This conclusion is based on a fresh mask-150 kernel, an independent coordinate-stability audit, and an independent source certificate.

## Fresh kernel

The exact Phase-5 compiler gives:

- 17 active weighted F components;
- 19 kernel variables;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- degree profile: 1 linear, 2 quadratic, 144 cubic;
- no generic constant contradiction.

Fresh kernel replay: GitHub Actions run `32231957064`.

## Coordinate audit

Named F coordinates were independently reconstructed under

```text
PYTHONHASHSEED = 1, 2, 17
```

and were stable before the named certificate below was accepted.

Coordinate-stability replay: GitHub Actions run `32232184182`.

## Two-cell certificate

The fresh mask-150 source validator independently verifies

```text
(XXXXX)_(0,0)   -> z0
(XXXX;1)_(0,0)  -> z0^2 - 1/2
```

so the final pentagons require

\[
z_0=0,
\qquad
z_0^2=\frac12,
\]

hence the exact contradiction

\[
\boxed{-\frac12=0}.
\]

Certificate:

```text
experiments/r22_phase5_component7_mask150_local_relations.py
```

GitHub Actions run `32232746046` reports `closed=True`.

No localization, determinant obstruction, finite branch enumeration, residual solve, Gröbner basis, or floating-point computation is used.

## Conclusion

\[
\boxed{\text{component 7 / mask 150 is non-categorifiable}.}
\]

The current component-7 boundary is

\[
\boxed{0,105,150\ \text{CLOSED};\qquad255\ \text{OPEN}.}
\]

Proceed next to mask `255` from a fresh kernel fingerprint.