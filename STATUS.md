# Status

## Stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — 9 of 16 scalar components excluded; 7 epsilon-plus components remain`

## Success criterion

**RESEARCH DECISION.** This line is no longer trying to show that explicit AEG/history notation is merely faster than ordinary category theory.  The target is Meng--Yu's currently unresolved categorifiability problem for the rank-six self-dual fusion ring `R(2,2)`.

Success means either:

- construct invertible associator/F-data satisfying every pentagon; or
- derive a rigorous obstruction to categorification.

Reproducing known criteria, rephrasing coherence, or reducing runtime alone is not sufficient.

## Open target

**CLASSICAL.** The based ring is

\[
\{1,g,h,gh,X,Y\},\qquad gX=Y,
\]

\[
X^2=Y^2=1+h+2X+2Y,
\qquad
XY=g+gh+2X+2Y.
\]

`experiments/r22_scale_audit.py` verifies associativity and

\[
\operatorname{FPdim}(X)=2+\sqrt6,
\qquad
\operatorname{FPdim}(R(2,2))=24+8\sqrt6.
\]

See `references/r22-open-problem.md`.

## Raw scale and localization

The strict-unit raw problem contains

\[
273\text{ nontrivial F-blocks},\quad1881\text{ scalar entries},
\]

and

\[
1833\text{ non-unit pentagon blocks},\quad76185\text{ scalar matrix equations}.
\]

A global symbolic solve is rejected.

The history/dependency audit splits associators into six layers:

| layer | blocks | scalar entries | role |
|---|---:|---:|---|
| A | 27 | 27 | pointed |
| B | 54 | 54 | one noninvertible |
| C | 72 | 72 | two noninvertibles, invertible output |
| D | 72 | 288 | two noninvertibles, noninvertible output |
| E | 32 | 128 | three noninvertibles, invertible output |
| F | 16 | 1312 | three noninvertibles, noninvertible output |

The 32 E-block count includes output `1`; an earlier reconnaissance omission of the vacuum-output blocks was identified and corrected before the current branch exclusions were accepted.

## Scalar A/B/C quotient

**COMPUTATIONAL-CLAIM.** `experiments/r22_scalar_audit.py` converts the scalar pentagons to

\[
A_{sc}\in M_{729\times153}(\mathbb Z),
\qquad \operatorname{rank}A_{sc}=129.
\]

The effective scalar trivalent-gauge rank is 24, so there are no continuous scalar moduli:

\[
153-129-24=0.
\]

Smith normal form leaves

\[
\boxed{(\mathbb Z_2)^4},
\]

hence exactly 16 discrete scalar components.

The two stabilizer signs satisfy

\[
\boxed{\epsilon_X=\epsilon_Y=: \epsilon,\qquad\epsilon^2=1.}
\]

The quotient splits into eight `epsilon=+1` and eight `epsilon=-1` components.

A subtle gauge point is recorded in the audit: sign-only trivalent gauge has rank 23, but full complex gauge supplies one additional sign direction through an `i`-phase gauge, restoring finite gauge rank 24 and the expected four quotient bits.

## Epsilon-minus closure

**CANDIDATE-NEW / COMPUTATIONAL-CLAIM.** All eight `epsilon=-1` scalar components have been excluded exactly.  See `notes/15-r22-epsilon-minus-closure.md`.

The D seed data become 2D Clifford/Pauli triples.  Complete D coherence reduces eight local chirality bits to two parity-orbit chirality bits.  Components 12--15 fail the D amplitude/Smith system; components 4 and 6 fail at F-linear invertibility; components 5 and 7 reach the final four-noninvertible pentagons but admit tiny exact contradiction certificates.

Therefore

\[
\boxed{\epsilon=-1\text{ cannot extend to an invertible associator system}.}
\]

This is a branch-family exclusion, not yet a full `R(2,2)` noncategorifiability theorem.

## Epsilon-plus character-sheet geometry

For `epsilon=+1`, the three stabilizer involutions commute.  Every multiplicity-two history fiber decomposes into an unordered pair of characters

\[
\{\chi_1,\chi_2\}\subset\widehat{(\mathbb Z_2)^3}.
\]

The eight multiplicity spaces form two parity `K_4` history graphs.  Projective D coherence on an edge is exactly equality of the unordered restricted character multisets on the two visible stabilizer coordinates.

This exposes a two-sheet local-system description instead of a general `2 x 2` matrix search.

## Scalar component 0 closure

**CANDIDATE-NEW / COMPUTATIONAL-CLAIM.** Scalar component `0` (an `epsilon=+1` component) is now fully excluded.  See `notes/13-r22-epsplus-character-sheets.md` and `notes/14-r22-component0-exclusion.md`.

The proof is a finite partition of character-sheet types.

### Repeated characters

For repeated nontrivial characters, full `GL_2` D transport plus legal star-edge gauge fixing produces a constant D-pentagon contradiction `±2=0`.

For the repeated trivial character, the full 48-block D system reduces on each parity `K_4` to one involutive holonomy

\[
S^2=I.
\]

Up to conjugacy there are only

\[
S=I,\quad -I,\quad H=\operatorname{diag}(1,-1),
\]

so nine global D-holonomy types.  All nine admit invertible E solutions, but keeping the complete E nullspaces symbolic, F coherence forces in every required `10 x 10` block

\[
\mathrm{row}_0=\mathrm{row}_1,
\qquad
\mathrm{col}_0=\mathrm{col}_1.
\]

Hence all repeated branches are singular.

### Weight-one pairs

All twelve Hamming-distance-one character pairs fail already at projective D coherence, even when restriction-degenerate edges are allowed full `2 x 2` mixing matrices.  Required transport determinants are identically zero.

### Separated nonorientable pairs

The projective history graph permits sheet-swap local systems, but complete D-amplitude pentagons kill every nonorientable assignment.  The exponent lattices have only Smith factors 1 and 2, so the root-of-unity failure is a genuine `C*` obstruction.

### Separated orientable pairs

There are 4096 finite pair/torsion branches.  Characteristic-zero Gaussian singleton equations immediately kill 4032: some required E block has at least three entries forced to zero.

The remaining branches reduce to four pair-pair choices.  `((2,5),(2,5))` has full-rank homogeneous E coefficient matrix and only the zero E solution.  The two mixed `(0,7)|(2,5)` orientations were recomputed for all 32 D torsion cases in characteristic zero; each has a 2D E nullspace but sixteen required E blocks are identically zero matrices.

The final `(0,7)|(0,7)` sixteen torsion cases need no E specialization: even when all 128 E entries are left algebraically independent, F coherence contains exactly 2304 support-one equations with constant coefficients `±2`.  They force 1088 F entries to zero and bound structural ranks by

\[
8\times8:\ 2,
\qquad
10\times10:\ 6.
\]

Thus component 0 is excluded.

## Current search space

Nine of sixteen scalar components are now excluded:

- all eight `epsilon=-1` components;
- `epsilon=+1` component 0.

The unresolved scalar components are

\[
\boxed{1,2,3,8,9,10,11},
\]

all with `epsilon=+1`.

The original approximately 1900-entry nonlinear problem has therefore become a finite sequence of seven scalar cocycle twists, each to be subjected to the same cheapest-first cascade:

\[
\boxed{
\text{scalar component}
\to
\text{D character compatibility}
\to
\text{D amplitude / holonomy}
\to
\text{E invertibility}
\to
\text{F linear rank}
\to
\text{final small kernel only if necessary}.
}
\]

## Immediate next task

1. Freeze exact sign representatives for scalar components `1,2,3,8,9,10,11`.
2. Recompute D seed normalizations for each scalar twist; do not assume component-0 character phases unchanged.
3. Compile the projective D edge compatibility as a finite character-pair CSP for each component.
4. Reject branches with singular D transports before amplitude solving.
5. Apply Smith/root-of-unity D amplitude filters to survivors.
6. Construct E/F systems only for finite branches that pass D.
7. Search for compact local contradiction certificates before any Gröbner calculation.

## Compute discipline

- Do not materialize the full 76185-equation SymPy problem.
- Python handles combinatorial/history incidence; SymPy handles exact small linear/Smith calculations; custom sparse IR handles large monomial/linear layers; NumPy finite-field work is reconnaissance/certificate discovery only.
- A heavy symbolic operation has a hard time limit.  A timeout changes the representation; it does not automatically increase the budget.
- A numerical or finite-field obstruction is not promoted to a theorem until an exact characteristic-zero certificate or valid lifting argument is frozen.

## Research labels

**CLASSICAL.** The fusion ring and general coherence/categorification problem belong to existing fusion-category theory.

**REFORMULATION.** A--F layering, character-sheet history graphs, and sparse amplitude/weighted-component IRs are solver organizations of ordinary coherence data.

**CANDIDATE-NEW.** The finite branch eliminations and compact obstruction certificates for the previously unresolved `R(2,2)` ring may constitute new mathematical content if independently verified and if the full categorifiability question is resolved.  No final theorem or originality claim is made yet.
