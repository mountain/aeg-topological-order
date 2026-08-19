# R(2,2) component 7 / mask 255 — Phase-5 exact closure

## Status

**CLOSED / EXACT.**

Scalar component `7`, chirality mask `255`, has no invertible associator extension satisfying the final four-noninvertible pentagons.

This is a fully fresh mask-255 replay. No conclusion from masks `0`, `105`, or `150` is used as a premise.

## 1. Fresh kernel

The exact Phase-5 compiler gives the same `17+4` macroscopic geometry found in the earlier component-7 masks:

- 17 active weighted F components;
- 19 kernel variables `p,q,z0,...,z16`;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- degree profile: 1 linear, 2 quadratic, 144 cubic;
- no generic constant contradiction.

Fresh kernel replay: GitHub Actions run `32233038719`.

## 2. Coordinate stability

Named F coordinates were independently reconstructed under

```text
PYTHONHASHSEED = 1, 2, 17
```

before accepting the named `z0` certificate.

Coordinate-stability replay: GitHub Actions run `32233338572`.

## 3. Two-cell exact obstruction

The fresh mask-255 source validator directly verifies the fixed provenances

```text
(XXXXX)_(0,0)   -> z0
(XXXX;1)_(0,0)  -> z0^2 - 1/2
```

so the final pentagons require simultaneously

\[
\boxed{z_0=0}
\]

and

\[
\boxed{z_0^2=\frac12}.
\]

Substitution gives

\[
\boxed{-\frac12=0},
\]

an exact characteristic-zero contradiction.

Source certificate:

```text
experiments/r22_phase5_component7_mask255_local_relations.py
```

GitHub Actions run `32233649046` reports

```text
P1 = z0
P2 = z0**2 - 1/2
contradiction = -1/2
closed = True
```

No localization, determinant obstruction, finite-stratum enumeration, residual solve, Gröbner basis, or floating-point computation is used.

## 4. Component-level replay

After all four chirality masks had been independently fresh-compiled, coordinate-audited, and source-validated, a final serial component-level replay recompiled the masks in the order

```text
0 -> 105 -> 150 -> 255
```

and checked the same two fixed provenances in each fresh kernel.

GitHub Actions run `32233916428` reports:

```text
mask 0    P1=z0  P2=z0**2-1/2  closed=True
mask 105  P1=z0  P2=z0**2-1/2  closed=True
mask 150  P1=z0  P2=z0**2-1/2  closed=True
mask 255  P1=z0  P2=z0**2-1/2  closed=True
SUMMARY closed=4,total=4
```

The executable component-level certificate is

```text
experiments/r22_phase5_component7_all_masks_two_cell_certificate.py
```

## 5. Conclusion

Therefore

\[
\boxed{\text{component 7 / mask 255 is non-categorifiable}.}
\]

Together with masks `0`, `105`, and `150`, this closes scalar component `7` completely. See `notes/41-r22-component7-phase5-closure.md` for the component-level synthesis.