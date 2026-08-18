# R(2,2): stagewise scalar-cocycle visibility

Status: **CANDIDATE-NEW / exact solver-structure observation, independent verification pending**

This note records a structural feature of the localized `R(2,2)` pentagon system that became visible only after separating scalar A/B/C associators from multiplicity-two D/E/F history layers.

## 1. Scalar components are not read globally

The scalar A/B/C quotient has 16 gauge-inequivalent components.  It is tempting to regard each component as one indivisible global cocycle label.  The localized pentagons do not see it that way.

A direct incidence audit of the exact pentagon compiler gives:

\[
\boxed{\text{D-layer pentagons read exactly the 54 B-layer scalar associators}},
\]

\[
\boxed{\text{E-layer pentagons read exactly the 72 C-layer scalar associators}},
\]

and the F-linear layer reads B+C but no pointed A-layer scalar data.

Thus the scalar cocycle enters the extension problem according to operation-history depth:

\[
\begin{array}{c|c}
\text{history layer} & \text{scalar data visible}\
\hline
D & B\\
E & C\\
F & B+C.
\end{array}
\]

This is a solver/localization statement about ordinary pentagon coherence; it is not proposed as a new categorical invariant.

## 2. D-visible quotient of epsilon-plus scalar components

The eight `epsilon=+1` scalar components are

\[
0,1,2,3,8,9,10,11.
\]

Restricting their exact sign representatives to the 54 D-visible B coordinates collapses them to only two fingerprints:

\[
\boxed{\{0,1,2,3\}},
\qquad
\boxed{\{8,9,10,11\}}.
\]

Components `0,1,2,3` agree entry-for-entry on all D-visible scalar coordinates. Components `8,9,10,11` likewise agree entry-for-entry with one another and differ from the first class by a fixed B-layer sign twist.

Consequently, all projective D geometry and all D-amplitude equations are identical inside each of these two D-visible classes.

## 3. Universal projective character-sheet CSP

Even across the two D-visible classes, scalar twisting does not change the projective *invertibility* compatibility relation on a D-history edge.

For every one of the three edge colors (visible stabilizer coordinate pairs `(L,M)`, `(L,R)`, `(M,R)`) and for every `36 x 36` pair of endpoint unordered character pairs, the set of endpoint assignments admitting an invertible projective D intertwiner is identical for all eight epsilon-plus scalar components.

The condition is exactly

\[
\{\chi_{u,1}|_S,\chi_{u,2}|_S\}
=
\{\chi_{v,1}|_S,\chi_{v,2}|_S\},
\]

where `S` is the two-coordinate stabilizer set visible on the edge.

Thus all epsilon-plus components share one finite character-sheet gluing skeleton. Scalar twisting enters only through the multiplicative D amplitudes and later layers.

## 4. D-amplitude phase fingerprints

For the important separated orientable pair `(0,7)|(0,7)`, all eight epsilon-plus components share the same rank-84 D-amplitude exponent lattice with Smith nonunit factors `(2,2,2,2)`.

The right-hand-side phase data collapse further to two classes:

- `0,1,2,3`: one common phase pattern; an exact solution may be chosen using only `±1`;
- `8,9,10,11`: a second common phase pattern; an exact solution requires `±1,±i` in a convenient gauge.

Again, the combinatorial history lattice is unchanged; only the discrete cocycle phase decorating it changes.

## 5. E-visible refinement

The C-layer fingerprints distinguish the epsilon-plus scalar components more finely.  In particular, components `1,2,3` are indistinguishable from component `0` throughout D, but first differ at E because E pentagons read the C-layer scalar coordinates.

This gives an exact reason to organize the remaining search stagewise rather than by rerunning the full associator problem separately for each scalar component:

\[
\boxed{
\text{one universal history skeleton}
\; + \;
\text{stage-visible discrete cocycle phases}.
}
\]

## 6. Research significance

The value of this observation is computational/structural rather than invariant-theoretic.  The original 16 scalar components do not induce 16 unrelated associator systems.  Localization factors the search through progressively finer quotients of the scalar cocycle, allowing entire families of components to reuse the same projective geometry, amplitude exponent lattice, and sparse compiler.

The immediate consequence is that components `1--3` can reuse every D-layer result proved for component `0`; only their C-layer E twist and B+C F twist need fresh verification.  Components `8--11` form a second D-visible family and likewise need only one D analysis before E/F refinement.
