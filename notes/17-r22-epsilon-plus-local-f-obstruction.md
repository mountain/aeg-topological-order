# R(2,2): unified epsilon-plus local-F obstruction

**Status:** `CANDIDATE-NEW / exact characteristic-zero obstruction / independent replay completed`

This note supersedes the need for the long branch-by-branch `epsilon=+1` exclusion chain as the primary proof mechanism.  The earlier character-sheet/D/E analyses remain useful for interpretation and solver development, but the final obstruction is much smaller and more local.

## 1. Setup

The scalar A/B/C monomial system has sixteen gauge-inequivalent components.  Eight have

\[
\epsilon_X=\epsilon_Y=+1.
\]

On every multiplicity-two fusion space the three stabilizer actions therefore commute and can be simultaneously diagonalized.  The fiber is an unordered pair of characters

\[
\{\chi_1,\chi_2\}\subset\widehat{(\mathbb Z_2)^3}.
\]

The eight multiplicity-two spaces split into two `Y`-parity `K_4` history graphs.

Projective D coherence on an edge seeing two stabilizer coordinates `S` admits an invertible intertwiner exactly when

\[
\{\chi_{u,1}|_S,\chi_{u,2}|_S\}
=
\{\chi_{v,1}|_S,\chi_{v,2}|_S\}.
\]

An exhaustive exact CSP enumeration gives exactly

\[
\boxed{52}
\]

projectively admissible character-pair gluings on each parity `K_4`.  Hence every `epsilon=+1` projective D possibility is represented in the finite set

\[
\boxed{52^2=2704}
\]

of two-parity gluing assignments.

## 2. Only two local pentagons are needed

Consider the required ten-dimensional associator

\[
F^{XXX}_{X}.
\]

Instead of solving cross-D amplitudes, E associators, or the final four-noninvertible pentagons, retain only the two local pentagon families

\[
(X,h,X,X;X),
\qquad
(X,X,X,h;X).
\]

For fixed scalar component and character-sheet assignment, these pentagons contain only:

- frozen scalar A/B/C associators;
- diagonal stabilizer actions of `h` on the relevant multiplicity fibers;
- entries of the target `10 x 10` matrix `F^{XXX}_{X}`;
- strict-unit maps.

They contain **no cross-space D amplitudes and no E-layer associator**.

A precompiled exact linear IR reduces their matrix entries to weighted identifications among the 100 entries of `F^{XXX}_{X}`.  After contracting these relations, every matrix entry has the form

\[
0
\quad\text{or}\quad
\pm z_\alpha,
\]

where the `z_alpha` are independent weighted-component parameters.

## 3. Exact determinant certificate

For each branch, form the symbolic `10 x 10` matrix over

\[
\mathbb Z[z_1,z_2,\ldots].
\]

The determinant is computed directly by exact subset dynamic programming, using only integer coefficient addition.  No floating-point, finite-field, random-rank, or numerical determinant test is used in the final certificate.

For each of the eight canonical `epsilon=+1` scalar components

\[
0,1,2,3,8,9,10,11,
\]

and for each of its `52 x 52 = 2704` projective character-sheet gluings, the determinant polynomial is identically zero:

\[
\boxed{
\det F^{XXX}_{X}\equiv0.
}
\]

The complete exact count is therefore

\[
\boxed{
8\times2704=21632
}
\]

branch certificates, all with zero determinant polynomial in characteristic zero.

Consequently no projectively admissible `epsilon=+1` D branch can extend to an invertible associator system:

\[
\boxed{
\epsilon=+1
\Longrightarrow
\text{no invertible }F^{XXX}_{X}.
}
\]

## 4. Independence from the earlier D/E scanners

This proof deliberately avoids the parts of the exploratory notebook that underwent several gauge/index corrections.  In particular it does not use:

- the repeated/weight-one/separated partition as a completeness argument;
- D-amplitude root-of-unity solutions;
- E-layer nullspaces;
- F-layer solutions obtained after choosing E representatives;
- the final nonlinear four-noninvertible pentagons.

The only finite completeness input is the 52-state projective character-sheet CSP on each parity `K_4`, whose edge condition is the direct invertible-intertwiner condition for commuting stabilizer characters.

The standalone replay script `experiments/r22_epsplus_local_f_obstruction.py` reconstructs this proof path and verifies all 21632 determinant identities exactly.

## 5. Relation to the earlier component-0 analysis

The older component-0 branch analysis exposed useful geometry:

- repeated characters and full `GL_2` D transport;
- weight-one degeneracies;
- orientable/nonorientable sheet local systems;
- D-amplitude Smith obstructions;
- E-layer singularity patterns.

Those results remain useful as diagnostics, but they are no longer needed to prove the epsilon-plus exclusion.  The local-F determinant lemma absorbs all those cases uniformly, including nonconstant and nonorientable projective gluings.

## 6. Current global implication

The repository separately contains an exact finite-branch exclusion of the `epsilon=-1` Clifford half in `notes/15-r22-epsilon-minus-closure.md`, but that half is still undergoing a fresh canonical-representative audit.

Therefore the correct current status is:

\[
\boxed{
\epsilon=+1\text{ is independently closed exactly};
\qquad
\epsilon=-1\text{ closure remains the final verification frontier}.
}
\]

Only after the Clifford half is independently reproduced should the repository promote the combined result to an `R(2,2)` noncategorifiability theorem candidate.