# R(2,2) epsilon-minus closure — SUPERSEDED

**Status:** `SUPERSEDED / contains an invalid D-amplitude family claim / retained as research history`

> **Do not use this note as a proof that the `epsilon=-1` half is closed.**  A fresh canonical-representative audit on 2026-08-17 found exact D-layer solutions for scalar components in the `12--15` family, contradicting Section 2 below.  The historical branch calculations are retained because several local certificates remain useful, but the global closure conclusion is withdrawn until independently reconstructed.

## 0. What was invalidated

The previous version claimed that scalar components `12--15` had no nonzero D-amplitude solution after the projective Clifford stage.  A new implementation using the **full complex scalar-gauge quotient canonical representatives** found, for example, a component-13 uniform-chirality solution with 48 amplitudes in

\[
\{1,i,-1,-i\}.
\]

That solution was substituted back into the original multiplicity-aware SymPy pentagon engine.  All

\[
\boxed{1728/1728}
\]

D-layer matrix entries vanished exactly in characteristic zero.  The same new solver finds D solutions for all four orbit-constant chirality patterns in each of components `12,13,14,15`.

Therefore the old statement

\[
\text{components }12\text{--}15\text{ fail at D amplitude}
\]

is false.

The likely source of the old error is not yet assigned to one line of code; the new audit deliberately uses canonical full-`C*` gauge representatives rather than sign-only/gauge-dependent branch labels.

## 1. What remains useful from the old analysis

The scalar A/B/C audit itself is unaffected:

- sixteen full-gauge scalar components;
- eight with `epsilon=+1` and eight with `epsilon=-1`;
- the `epsilon=-1` D seeds are two-dimensional Clifford/Pauli triples;
- the eight multiplicity spaces split into two size-four `Y`-parity transport orbits.

Several **branch-local** calculations below also remain candidate certificates, but they must be reattached to canonical scalar representatives before being used globally.

### Historical component-4 branch

A detailed uniform-Clifford branch is recorded in `notes/12-r22-epsminus-uniform-branch.md`.  Its exact D/E extension and F-layer rank obstruction remain internally consistent for that branch.

A fresh independent local-F audit has since strengthened this: for canonical scalar components

\[
4,6,12,14
\]

and all sixteen local Clifford chirality patterns relevant to the target block, the characteristic-zero determinant polynomial of the required `10 x 10` associator `F^{XXX}_X` is identically zero under the four single-`h` local pentagons.  Thus these four scalar components have a new, much shorter obstruction route independent of the invalid old D-amplitude claim.

### Historical component-5 certificate

The old computation reached final four-noninvertible pentagons and extracted

\[
x_0+x_1x_3=0,
\]
\[
x_0+(2+2i)x_1x_3=0,
\]
\[
x_0+(2-2i)x_2x_8=0,
\]
\[
1-2x_0^2+(4+4i)x_1x_3+(4-4i)x_2x_8=0,
\]

which gives `1=0`.  This is a promising compact certificate, but in the fresh audit it is **not yet accepted as a canonical-component proof** until its A--F lower data are independently reconstructed.

### Historical component-6 and component-7 certificates

The old branch tree reported:

- component 6: F-linear structural rank at most 8 in every required `10 x 10` block;
- component 7: a final contradiction `x_0=0` together with `1-2x_0^2=0`.

These are also retained as candidate branch certificates pending canonical-representative replay.

## 2. Fresh independent audit status

The new audit uses the canonical scalar representatives produced after including the extra `i`-gauge sign direction in the full complex trivalent gauge quotient.

The `epsilon=-1` components are

\[
\boxed{4,5,6,7,12,13,14,15}.
\]

A fresh local-F engine that uses all four positions of a single stabilizer `h` has independently proved exact characteristic-zero determinant obstruction for

\[
\boxed{4,6,12,14}.
\]

For each of those four scalar components, all sixteen local Clifford chirality patterns satisfy

\[
\boxed{\det F^{XXX}_{X}\equiv0}.
\]

The complementary components

\[
\boxed{5,7,13,15}
\]

are **not** killed by that local cell on the orbit-constant chirality patterns that survive the expected D-localization.  They are the current verification frontier.

A new D-amplitude engine has also shown that components `12--15` admit exact solutions for the four orbit-constant chirality patterns, so their exclusion must occur later than D if it occurs at all.

## 3. Current conclusion

The old boxed conclusion

\[
\epsilon=-1\Longrightarrow\text{no invertible associator extension}
\]

is withdrawn.

The correct present statement is:

\[
\boxed{
\text{four of eight epsilon-minus scalar components are independently obstructed};
\quad
5,7,13,15\text{ remain under fresh audit}.
}
\]

No `R(2,2)` noncategorifiability theorem should be claimed until those four remaining Clifford components are independently closed.
