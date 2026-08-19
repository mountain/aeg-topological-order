# R(2,2) component 7 / mask 0 — Phase-5 exact closure

## Status

**CLOSED / EXACT.**

For scalar component `7` and chirality mask `0`, there is no invertible associator extension satisfying the final four-noninvertible pentagons.

Unlike scalar components `5` and `13`, no finite algebraic stratification is required. Two fixed final-pentagon cells already contradict one another after the exact Phase-4 quotient.

## 1. Fresh `17+4` Phase-5 kernel

Component `7` is the first deep scalar type whose Phase-4 F-linear quotient has `17` active weighted F components together with `4` coherence-forced-zero components.

Fresh mask-0 replay gives:

- 96 final pentagon blocks;
- 56,448 scalar positions;
- 17 active F-linear components;
- 19 kernel variables `p,q,z0,...,z16`;
- 15,744 support-two F-linear equations before the kernel quotient;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- degree profile: 1 linear, 2 quadratic, 144 cubic relations;
- no generic constant contradiction.

This is a genuine reduction from the 21-free-component geometry of scalar components `5` and `13`, whose final kernels had 23 variables, 50,880 raw nonzero entries, and 219 unique cubics.

Fresh kernel replay: GitHub Actions run `32229775991`.

## 2. Coordinate reproducibility

Before accepting named `z_j` certificates, the current F-component partition and a fixed final-pentagon target were reconstructed in independent Python processes under

```text
PYTHONHASHSEED = 1, 2, 17
```

The result was

```text
partition_variants = 1
target_variants    = 1
```

for mask `0`.

Hence the `z0` coordinate used below is reproducible with respect to the tested union-find/hash ordering.

Coordinate-stability replay: GitHub Actions run `32229975687`.

## 3. Two fixed final-pentagon cells

The exact source validator recompiles the fresh kernel and reads the following fixed provenances directly.

First:

```text
(XXXXX)_(0,0)
```

is exactly proportional to

\[
\boxed{z_0}.
\]

Thus the pentagon equation forces

\[
\boxed{z_0=0}.
\]

Second:

```text
(XXXX;1)_(0,0)
```

is exactly proportional to

\[
\boxed{z_0^2-\frac12}.
\]

Thus the same associator must satisfy

\[
\boxed{z_0^2=\frac12}.
\]

Substituting the first equation into the second gives the exact characteristic-zero contradiction

\[
\boxed{-\frac12=0}.
\]

No localization, determinant argument, finite branch enumeration, residual scan, Gröbner basis, or numerical solve is used.

Source certificate:

```text
experiments/r22_phase5_component7_mask0_local_relations.py
```

GitHub Actions run `32230627427` reports

```text
P1 = z0
P2 = z0**2 - 1/2
contradiction = -1/2
closed = True
```

and concludes:

```text
RESULT: component 7 / mask 0 is excluded by two fixed final-pentagon cells
```

## 4. Final conclusion

Therefore

\[
\boxed{\text{component 7 / chirality mask 0 has no invertible Phase-5 associator extension}.}
\]

Equivalently,

\[
\boxed{\text{component 7 / mask 0 is non-categorifiable}.}
\]

## 5. Structural significance

The first `17+4` Phase-4 type is qualitatively different from component `13`.

For component `13`, the final search compressed through

\[
50{,}880\to219\to18\text{ finite strata}\to\text{small residual cores}.
\]

For component `7 / mask 0`, the `17+4` lower quotient already exposes a much stronger local obstruction:

\[
\boxed{
38{,}080\text{ raw entries}
\to147\text{ unique relations}
\to2\text{ fixed cells}
\to1=0.
}
\]

This suggests that the four F components forced to zero at Phase 4 may place the final coherence system on a substantially more singular relation-space stratum. That interpretation is a research hypothesis, not a premise of this proof.

## 6. Next gate

Masks `105`, `150`, and `255` of scalar component `7` remain open.

Proceed next to **component 7 / mask 105** from a fresh Phase-5 kernel fingerprint. The mask-0 two-cell certificate must not be imported without independent exact source verification.