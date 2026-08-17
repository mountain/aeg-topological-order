# R(2,2) epsilon-plus character-sheet localization

Status: **CANDIDATE-NEW / exact branch-local calculations, independent verification pending**

This note records the current `epsilon = +1` frontier for the open categorification attack on the Meng--Yu fusion ring `R(2,2)`.  It supersedes earlier reconnaissance that treated all multiplicity-two transports as diagonal matrices.

## 1. Commuting stabilizer regime

After the scalar A/B/C audit, `epsilon_X = epsilon_Y = epsilon`.  The `epsilon=-1` Clifford regime is handled separately.  For `epsilon=+1`, the three stabilizer actions on every multiplicity-two fusion space commute and may be simultaneously diagonalized.

Thus a multiplicity-two history fiber is represented by an unordered pair of characters

\[
\{\chi_1,\chi_2\}\subset \widehat{(\mathbb Z_2)^3}.
\]

The eight spaces `V_{MN}^P` form two parity components, each a `K_4` history graph.  Every edge sees two of the three stabilizer coordinates.

For an edge seeing coordinates `S`, the projective D-intertwiner is invertible exactly when the two endpoint character pairs have the same unordered restricted multiset

\[
\{\chi_{u,1}|_S,\chi_{u,2}|_S\}
=
\{\chi_{v,1}|_S,\chi_{v,2}|_S\}.
\]

This converts the projective D problem from general `2 x 2` matrix search into a finite character-sheet gluing problem.

## 2. Separated sheets and sheet-swap holonomy

On one parity `K_4` there are 52 projectively admissible character-pair gluings.  In the edge-separated subfamily, 16 are globally orientable (the two sheets can be globally labelled) and 16 carry nontrivial sheet-swap `Z_2` holonomy.

For the separated subfamily the full D amplitude problem has 96 nonzero sheet amplitudes.  Exact Smith/root-of-unity auditing shows that every nonorientable sheet-swap assignment fails the complete D pentagons.  Representative exponent lattices have rank 83 with nontrivial Smith factors `(2,2)`; because the right-hand sides lie in `mu_2`, any complex solution would admit a `mu_4` lift, but the `mu_4` system is inconsistent.

Hence complete D coherence kills separated sheet-swap holonomy.

The orientable separated family is constant on each parity component.  Previous exhaustive E reconnaissance isolates `({0,7},{0,7})` as the only separated pair-pair candidate that can reach invertible E blocks; that survivor is killed at the F-linear layer by forced-zero support/rank deficiency.  The full characteristic-zero exactification of the *failed* E branches remains on the audit list before claiming complete component-0 exclusion from this fact alone.

## 3. Repeated characters: full GL(2) D normal form

The repeated case `\{a,a\}` cannot be treated by a diagonal sheet ansatz: when both sheets carry the same character the cross-space D intertwiners are genuinely `GL_2`-valued.

For the trivial repeated character `a=0`, we therefore allowed all 48 cross D blocks to be arbitrary `2 x 2` matrices.  The D pentagons first identify the two fusion-label realizations of each directed history edge, leaving 24 directed `K_4` edge transports.

On either parity `K_4`, choose one base vertex and use vertex `GL_2` gauge to make the six directed star transports identity.  The remaining D equations then give exactly

\[
T_{uv}=S
\]

for all six directed non-star edges and

\[
\boxed{S^2=I}.
\]

Thus, up to conjugacy over `C`, there are only three D holonomy normal forms per parity:

\[
S=I,\qquad S=-I,\qquad S\sim \operatorname{diag}(1,-1).
\]

The global repeated-trivial D problem therefore has only `3 x 3 = 9` holonomy branches.

All nine branches admit invertible E-layer solutions.  Their E nullities are 8 for `(±I,±I)`, 6 when exactly one parity holonomy is `H=diag(1,-1)`, and 4 for `(H,H)`.

Keeping the complete E nullspace symbolic, the F-layer equations for every one of the nine branches reduce to constant-coefficient `±1` entry identifications.  In every required `10 x 10` F block,

\[
\boxed{\mathrm{row}_0=\mathrm{row}_1,
\qquad
\mathrm{col}_0=\mathrm{col}_1.}
\]

Hence every such block is singular.  The repeated-trivial branch is excluded independently of the E parameters and independently of the D involutive holonomy.

For repeated nontrivial characters `a=1,...,7`, the same legal star-edge gauge fixing is even more restrictive: the D pentagons contain a constant contradiction `±2=0`.  Because the three stabilizer seeds are scalar `±I`, conjugating vertex bases does not change them, so this is not a gauge artifact.

Therefore **all repeated-character epsilon-plus branches are excluded**.

## 4. Weight-one character pairs

There are 12 unordered pairs whose characters differ in exactly one of the three stabilizer bits.

For such a pair, an edge whose visible coordinates distinguish the two characters was constrained only to the correct diagonal intertwiner subspace; an edge whose restrictions coincide was allowed a full `2 x 2` mixing matrix.  Thus this test does *not* assume diagonal D transport on the degenerate edge color.

For every one of the 12 pairs and for both parity `K_4`s, the projective D linear pentagons force at least one required transport to have determinant identically zero.  The exact counts of structurally singular directed transports are 4, 8, or 12 depending on the pair.

Consequently

\[
\boxed{\text{all Hamming-distance-1 character-pair branches fail already at projective D coherence}.}
\]

## 5. Current epsilon-plus taxonomy for scalar component 0

The character-pair possibilities are now divided as follows:

1. repeated pairs: excluded exactly (D or F, using the full GL(2) analysis above);
2. weight-one pairs: excluded exactly at projective D;
3. separated nonorientable pairs: excluded exactly by the D amplitude/Smith obstruction;
4. separated orientable pairs: finite constant-pair family; the known `0+7` survivor reaches E but is excluded at F, while the failed E branches still need a compact characteristic-zero certificate rather than only the existing exhaustive modular scan.

The remaining work for scalar component 0 is therefore sharply localized to exactifying the separated-orientable E filter.  No continuous `2 x 2` D-matrix search remains in the repeated or weight-one sectors.
