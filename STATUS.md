# Status

## Stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — epsilon-plus independently closed; epsilon-minus canonical re-audit reopened`

## Success criterion

**RESEARCH DECISION.** The goal is not to show that AEG/history notation is merely faster than ordinary category theory.  The target is Meng--Yu's unresolved categorifiability problem for the rank-six self-dual fusion ring `R(2,2)`.

Success means either:

- construct invertible associator/F-data satisfying every pentagon; or
- derive a rigorous obstruction to categorification.

No final theorem is claimed until both scalar-sign regimes are independently closed.

## Target and raw scale

The based ring is

\[
\{1,g,h,gh,X,Y\},\qquad gX=Y,
\]

\[
X^2=Y^2=1+h+2X+2Y,
\qquad
XY=g+gh+2X+2Y.
\]

The exact scale audit gives

\[
\operatorname{FPdim}(X)=2+\sqrt6,
\qquad
\operatorname{FPdim}(R(2,2))=24+8\sqrt6.
\]

The strict-unit raw problem contains

\[
273\text{ nontrivial F-blocks},\quad1881\text{ scalar entries},
\]

and

\[
1833\text{ non-unit pentagon blocks},\quad76185\text{ scalar matrix equations}.
\]

A global symbolic solve is rejected.

## History-layer localization

Associators are organized into six dependency layers:

| layer | blocks | entries | role |
|---|---:|---:|---|
| A | 27 | 27 | pointed |
| B | 54 | 54 | one noninvertible |
| C | 72 | 72 | two noninvertibles, invertible output |
| D | 72 | 288 | two noninvertibles, noninvertible output |
| E | 32 | 128 | three noninvertibles, invertible output |
| F | 16 | 1312 | three noninvertibles, noninvertible output |

The corrected E count includes vacuum output `1`.

Stagewise incidence further shows:

\[
D\text{ reads exactly B-layer scalar data},
\]

\[
E\text{ reads exactly C-layer scalar data},
\]

while the F-linear layer reads B+C.  This is recorded in `notes/16-r22-stagewise-cocycle-visibility.md`.

## Scalar A/B/C quotient

The 153 scalar associators satisfy a 729-row monomial pentagon system of rank 129.  Effective complex trivalent-gauge rank is 24, so there are no continuous scalar moduli.

Smith normal form leaves

\[
\boxed{(\mathbb Z_2)^4},
\]

hence exactly 16 scalar components.

A full-`C*` gauge audit is essential: sign-only gauge has rank 23, while an additional `i`-phase gauge supplies the 24th finite sign direction.

The gauge-invariant stabilizer sign satisfies

\[
\epsilon_X=\epsilon_Y=: \epsilon,
\qquad
\epsilon^2=1.
\]

Thus there are eight `epsilon=+1` and eight `epsilon=-1` scalar components.

---

# Epsilon-plus: independently closed

**CANDIDATE-NEW / EXACT.** The entire `epsilon=+1` half has now been independently excluded by a unified local-F obstruction.  See `notes/17-r22-epsilon-plus-local-f-obstruction.md` and `experiments/r22_epsplus_local_f_obstruction.py`.

Because the three D stabilizer involutions commute, every multiplicity-two fiber decomposes into an unordered pair of characters of `(Z/2)^3`.  Exact projective D compatibility on the two parity `K_4` history graphs has exactly

\[
52\times52=2704
\]

admissible character-sheet gluing assignments per scalar component.

Only two local pentagons are needed:

\[
(X,h,X,X;X),
\qquad
(X,X,X,h;X).
\]

They involve scalar A/B/C data, diagonal stabilizer actions, and the target required matrix `F^{XXX}_X`; they do **not** use cross-D amplitudes or E associators.

After exact weighted contraction, each target entry is `0` or `±z_alpha`.  An integer subset-DP computes the determinant polynomial of the `10 x 10` matrix directly in characteristic zero.

For every one of the eight `epsilon=+1` canonical scalar components

\[
0,1,2,3,8,9,10,11
\]

and every one of its 2704 projective gluings,

\[
\boxed{\det F^{XXX}_{X}\equiv0.}
\]

The standalone replay therefore checks

\[
\boxed{8\times2704=21632}
\]

exact branch certificates.

Hence

\[
\boxed{\epsilon=+1\Longrightarrow\text{no invertible associator extension}.}
\]

This result supersedes the need to use the earlier repeated/weight-one/separated D/E branch taxonomy as the primary epsilon-plus proof.

---

# Epsilon-minus: old closure superseded; fresh audit in progress

**IMPORTANT CORRECTION.** The previous version of `notes/15-r22-epsilon-minus-closure.md` claimed that scalar components `12--15` failed at D amplitude.  A fresh canonical-representative implementation found exact counterexamples to that claim.

For example, canonical component `13` with uniform Clifford chirality admits 48 D amplitudes in

\[
\{1,i,-1,-i\}.
\]

Substitution into the original multiplicity-aware SymPy pentagon engine verifies

\[
\boxed{1728/1728}
\]

D-layer matrix entries exactly equal zero.  The new solver likewise finds D solutions for all four orbit-constant chirality patterns in each of components `12,13,14,15`.

Therefore the old D-family obstruction is invalid and `notes/15-r22-epsilon-minus-closure.md` is explicitly marked **SUPERSEDED**.

## Fresh epsilon-minus progress

The canonical `epsilon=-1` scalar components are

\[
\boxed{4,5,6,7,12,13,14,15}.
\]

A new local-F engine uses all four placements of a single stabilizer `h`.  It independently proves characteristic-zero determinant obstruction for

\[
\boxed{4,6,12,14}.
\]

For each of these four scalar components and all sixteen local Clifford chirality patterns relevant to `F^{XXX}_X`, exact Gaussian-integer subset-DP gives

\[
\boxed{\det F^{XXX}_{X}\equiv0.}
\]

The complementary scalar components

\[
\boxed{5,7,13,15}
\]

are not killed by this local cell on the four orbit-constant chirality patterns.  They require the deeper D/E/F/final-pentagon audit.

Historical compact certificates for components 5 and 7 remain promising, but are not yet accepted as canonical-component proofs until their lower A--F data are independently reconstructed.

## Current theorem boundary

The repository may safely state:

\[
\boxed{\epsilon=+1\text{ is independently impossible}.}
\]

It may **not yet** state that `R(2,2)` is noncategorifiable.

The remaining verification frontier is exactly

\[
\boxed{5,7,13,15\quad(\epsilon=-1).}
\]

---

## Immediate next task

1. Reconstruct the complete D chirality/amplitude system for the canonical `epsilon=-1` B-visible families using the new implementation.
2. Determine the true D survivor set over all `2^8=256` chirality assignments; do not inherit the old `256 -> 64 -> 4` numbers without replay.
3. For components `13,15`, locate the first valid obstruction after the newly verified D solutions.
4. For components `5,7`, independently reproduce the historical compact final-pentagon certificates from canonical lower data.
5. Only after `5,7,13,15` are independently excluded should the combined result be promoted to an `R(2,2)` noncategorifiability theorem candidate.

## Compute discipline

- Do not materialize the full 76185-equation SymPy problem.
- Python handles combinatorial/history incidence; SymPy handles exact small linear/Smith calculations; custom sparse/token IR handles large monomial/linear layers.
- Finite-field computations are reconnaissance/certificate discovery only.
- Heavy symbolic operations have hard time limits.  A timeout changes the representation rather than increasing the budget.
- A branch obstruction is accepted only after characteristic-zero substitution, determinant identity, valid lifting/Smith argument, or another exact certificate.

## Research labels

**CLASSICAL.** The fusion ring and categorification problem belong to existing fusion-category theory.

**REFORMULATION.** A--F layering, character-sheet graphs, and sparse monomial/weighted-component IRs are solver organizations of ordinary coherence.

**CANDIDATE-NEW.** The unified epsilon-plus local determinant obstruction and the emerging finite Clifford certificates may become new mathematical content if the full `R(2,2)` question is resolved and independently verified.
