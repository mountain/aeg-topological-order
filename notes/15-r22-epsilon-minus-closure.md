# R(2,2) epsilon-minus closure

Status: **CANDIDATE-NEW / exact finite-branch exclusion, independent verification pending**

This note closes the `epsilon=-1` (Clifford/Pauli) half of the 16 scalar A/B/C components in the `R(2,2)` categorification attack.

## 1. Scalar components

The scalar A/B/C monomial system has 16 gauge-inequivalent components, with eight satisfying `epsilon=+1` and eight satisfying `epsilon=-1`.

For `epsilon=-1`, each multiplicity-two fusion space carries three pairwise anticommuting projective involutions.  Up to local conjugacy this is a two-dimensional Clifford/Pauli representation with a chirality sign.

The eight multiplicity spaces split into two size-four transport orbits, distinguished by `Y`-parity.

## 2. Chirality localization at D

A characteristic-zero scan of the 48 cross-space projective-D intertwiner systems over all `2^8=256` local chirality assignments shows that every small system is one-dimensional with an invertible representative whenever the scalar component is in the first Clifford family.

The full D-amplitude pentagons then reduce the eight local chirality bits to two orbit-level bits.  Exactly four patterns survive:

- both parity orbits positive;
- even negative / odd positive;
- even positive / odd negative;
- both negative.

Equivalently, chirality must be constant on each size-four `Y`-parity orbit.

For scalar components 4--7 the D-amplitude exponent lattice has rank 42 and nontrivial Smith factors `(2,2)`.  The four surviving chirality patterns have exact nonzero amplitude solutions.

For scalar components 12--15 the 256 chirality assignments split into 192 immediate structural/monomial obstructions and 64 amplitude-lattice candidates.  The latter share the same rank-42 exponent lattice with Smith factors `(2,2)`, but their `mu_8` systems are inconsistent.  Since the RHS phases are fourth roots of unity and the Smith factors are only 1 and 2, any complex nonzero solution would admit an eighth-root lift.  Therefore components 12--15 are genuinely obstructed already at D.

## 3. Components 4--7

### Component 4

The four orbit-constant chirality patterns extend through exact D and E amplitude closure.  At the F-linear layer every required `10 x 10` block is forced singular.  The branch is excluded before final four-noninvertible pentagons.

### Component 5

Both independent chirality classes (the other two are their complex conjugates) pass D, E, and the F-linear invertibility filter.  The final four-noninvertible pentagons collapse to a tiny contradiction certificate.  In one chirality convention four scalar entries give

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
1-2x_0^2+(4+4i)x_1x_3+(4-4i)x_2x_8=0.
\]

The first two equations imply `x_1 x_3=0` and `x_0=0`; the third implies `x_2 x_8=0`; the fourth becomes `1=0`.  The opposite chirality gives the complex-conjugate certificate.

Hence component 5 is excluded.

### Component 6

The surviving D/E branches encounter an F-linear structural-rank obstruction: every required `10 x 10` associator has maximum possible rank 8.  Hence component 6 is excluded.

### Component 7

The final kernel is even smaller.  A pentagon gives a nonzero scalar multiple of `x_0=0`, while another gives

\[
1-2x_0^2=0.
\]

Thus `1=0`, and component 7 is excluded.

## 4. Conclusion

All eight scalar components with `epsilon=-1` are excluded:

\[
\boxed{\epsilon=-1\Longrightarrow\text{no invertible associator extension}.}
\]

This is not yet a noncategorifiability theorem for `R(2,2)`, because seven `epsilon=+1` scalar components remain after the separate exclusion of component 0.

The important solver consequence is that the open problem is no longer a continuous Clifford-matrix search.  The entire anticommuting regime has been reduced to finite branches and eliminated by exact D/F/final-pentagon certificates.
