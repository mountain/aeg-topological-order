# R(2,2) theorem audit — full-C* scalar component inventory

## Status

**CLOSED / EXACT.**

The sixteen hard-coded canonical scalar representatives used by the later R(2,2) branch machinery are now independently certified to be a complete set of connected-component representatives modulo the **full complex trivalent gauge torus**, not merely modulo sign gauge.

The executable certificate is

```text
experiments/r22_scalar_component_inventory.py
```

and the fresh theorem-audit run is

```text
32259357537
```

## 1. Scalar solution group

The scalar A/B/C layer has

- 153 scalar associator variables;
- 729 nontrivial monomial pentagon equations;
- exponent-matrix rank 129;
- connected solution dimension `153-129=24`.

The strict-unit trivalent gauge action has

- 29 gauge variables;
- effective rank 24;
- image contained in the scalar-pentagon kernel.

Thus the gauge image and the identity component of the scalar solution group have the same dimension.  Since the image of a complex torus is connected, it is the full identity component.

The Smith torsion of the scalar exponent matrix is

\[
\boxed{2,2,2,2},
\]

so the scalar solution group modulo connected gauge has exactly

\[
\boxed{2^4=16}
\]

connected components.

## 2. Why sign-only gauge is insufficient

A historical failure in the epsilon-minus branch analysis came from treating sign-valued gauge transformations as though they exhausted the complex gauge action.  They do not: an `i`-valued gauge parameter can induce a sign change after passing through an even exponent.

The theorem-audit verifier therefore computes an integer Smith decomposition of the gauge exponent matrix

\[
D=SGT.
\]

The nonzero Smith factors of the gauge map are

```text
1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,2
```

or

\[
\boxed{1^{23},2}.
\]

The final factor `2` is exactly the structural warning that the naive mod-2 column span of `G` is not the full set of sign points reachable by the complex gauge torus.

## 3. Full-C* membership test

For a sign vector `b`, view the corresponding scalar phase point as `b/2` in additive torus coordinates.

From

\[
D=SGT,
\]

a sign point lies in the full complex gauge image iff every coordinate of `S b` beyond `rank(G)` is even.  The first 24 Smith coordinates impose no restriction because multiplication by any nonzero integer is surjective on `C*`.

This gives an exact integer test for gauge equivalence that includes all root-of-unity gauge parameters, including the previously missed `i` direction.

## 4. Canonical representative audit

The verifier checks all sixteen `COMPONENT_REPS` and proves:

1. each representative is an exact sign-valued solution of all 729 scalar monomial pentagons;
2. no pair differs by a point of the full complex gauge torus;
3. there are sixteen pairwise distinct representatives;
4. the scalar quotient has exactly sixteen components.

Therefore the list is exhaustive:

\[
\boxed{\text{the 16 COMPONENT_REPS are a complete full-C* component inventory}.}
\]

## 5. Epsilon partition

The gauge-invariant stabilizer sign

\[
\epsilon=F^{hXh}_X=F^{hYh}_Y
\]

splits the sixteen components exactly as

\[
\epsilon=+1:\quad
\boxed{0,1,2,3,8,9,10,11},
\]

\[
\epsilon=-1:\quad
\boxed{4,5,6,7,12,13,14,15}.
\]

The independently replayed epsilon-plus local-F certificate closes the first eight.  The fresh shallow epsilon-minus certificate closes `4,6,12,14`; the remaining deep components are exactly `5,7,13,15`.

## 6. Theorem consequence

The global theorem audit no longer needs to assume either

- that the hard-coded scalar representatives are complete, or
- that sign gauge captures the full complex gauge quotient.

Both are now executable exact statements.
