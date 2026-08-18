# R(2,2) scalar component 0: exact exclusion

Status: **CANDIDATE-NEW / exact branch-local obstruction chain, independent verification pending**

This note closes scalar A/B/C component `0` of the `R(2,2)` associator problem.  Component `0` lies in the `epsilon=+1` commuting-stabilizer regime.

The argument is finite and stratified by the unordered character pair carried by each multiplicity-two history fiber.

## 1. Character-sheet partition

For `epsilon=+1`, the three stabilizer involutions on every 2D multiplicity space commute, so the fiber decomposes as an unordered pair

\[
\{\chi_1,\chi_2\}\subset \widehat{(\mathbb Z_2)^3}.
\]

Character pairs fall into three types:

1. repeated: `chi_1=chi_2`;
2. weight one: the characters differ in one stabilizer bit;
3. separated: they differ in at least two bits.

The eight multiplicity spaces split into two parity `K_4` history components.

## 2. Repeated pairs

For repeated nontrivial characters `a=1,...,7`, allow the cross D transports to be arbitrary `GL_2` matrices.  Since the three stabilizer seeds are scalar `±I`, vertex `GL_2` gauge may normalize the six directed star transports of each parity `K_4` to identity without changing the seeds.  The D pentagons then contain a constant contradiction `±2=0`.  Hence these branches are impossible.

For the repeated trivial character `a=0`, the same full-GL(2) calculation identifies the two fusion-label realizations of each directed edge and reduces the remaining connection, after star gauge fixing, to one matrix `S` on every non-star directed edge with

\[
S^2=I.
\]

Over `C`, this leaves only three conjugacy types per parity component:

\[
I,\quad -I,\quad H=\operatorname{diag}(1,-1).
\]

Thus there are only nine repeated-trivial D-holonomy types.  All nine admit invertible E-layer solutions (E nullity 8, 6, or 4 depending on the holonomy pair).  Keeping the *entire* E nullspace symbolic, however, the F-linear equations in every holonomy type have constant coefficients `±1` and force, in all eight required `10 x 10` F blocks,

\[
\mathrm{row}_0=\mathrm{row}_1,
\qquad
\mathrm{col}_0=\mathrm{col}_1.
\]

Every block is singular.  Hence every repeated branch is excluded.

## 3. Weight-one pairs

There are twelve unordered character pairs of Hamming distance one.  The projective D calculation was performed without a diagonal ansatz:

- edges whose visible stabilizer coordinates distinguish the two characters were restricted only to the correct diagonal intertwiner space;
- edges whose restrictions coincide were allowed a full `2 x 2` mixing matrix.

For all twelve pairs and for both parity `K_4`s, the projective D linear pentagons force required transport determinants identically to zero.  Depending on the pair, 4, 8, or all 12 directed transports in the parity component are structurally singular.

Therefore every weight-one branch fails D-invertibility.

## 4. Separated nonorientable pairs

For edge-separated sheets, projective D coherence allows both globally orientable sheet systems and nonorientable sheet-swap local systems.  Full D-amplitude pentagons eliminate all nonorientable systems.

The relevant multiplicative exponent matrices have only Smith factors 1 and 2 and RHS in `mu_2`; therefore any complex solution would admit a `mu_4` lift.  The `mu_4` systems are inconsistent for all nonorientable assignments.  This is a genuine `C*` obstruction, not a sign-only test.

## 5. Separated orientable pairs: exact E filter

An orientable separated sheet system is constant on each parity component.  There are `16 x 16` pair choices and sixteen D torsion classes, hence 4096 finite branches.

A Gaussian-integer scan of singleton rows in the complete 32-block E system immediately kills 4032 branches: some required `2 x 2` E block has at least three entries forced to zero by single-entry pentagons with nonzero coefficients (typically `±2`).

Only four pair-pair choices avoid that immediate certificate:

\[
(0,7)|(0,7),\quad
(0,7)|(2,5),\quad
(2,5)|(0,7),\quad
(2,5)|(2,5),
\]

each with sixteen D torsion classes.

The remaining cases are eliminated as follows.

### `(2,5)|(2,5)`

The E coefficient matrix has full rank 128 modulo a characteristic not dividing the coefficients.  A nonzero full-size minor modulo the prime is the reduction of a nonzero Gaussian-integer minor, so the characteristic-zero E system also has rank 128 and only the zero solution.  No invertible E associators exist.

### Mixed `(0,7)|(2,5)` and `(2,5)|(0,7)`

All 32 torsion cases were recomputed in characteristic zero.  Every case has

\[
\operatorname{rank}A_E=126,
\qquad \dim\ker A_E=2,
\]

and exactly sixteen required E blocks are identically the zero matrix.  Hence all mixed branches fail.

### `(0,7)|(0,7)`

All sixteen torsion cases reach an E nullspace of dimension four with potentially invertible E blocks.  They nevertheless die *before any E specialization is needed*.

Treat all 128 E entries as independent symbols.  For every D torsion class, the F-layer pentagons contain exactly

\[
2304
\]

support-one equations whose coefficients are constant `±2` and do not involve E.  They force 1088 F entries to zero.  The remaining support has structural rank

\[
\boxed{
8\times8\text{ blocks}:\ 2,
\qquad
10\times10\text{ blocks}:\ 6.
}
\]

Thus no required F associator can be invertible.

## 6. Conclusion

Every character-sheet branch of scalar component `0` is excluded:

\[
\boxed{\text{scalar component 0 cannot extend to invertible associator data.}}
\]

This is a branch-local statement inside the full `R(2,2)` problem.  Together with the separately established exclusion of all eight `epsilon=-1` scalar components, the unresolved scalar components are now the seven remaining `epsilon=+1` components

\[
1,2,3,8,9,10,11.
\]

The next step is to run the same cheapest-first D-character compatibility cascade on those seven scalar cocycle twists before constructing any new E/F systems.
