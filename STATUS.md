# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CANONICALLY CLOSED / SCALAR COMPONENT 5 PHASE 5 CLOSED / COMPONENTS 7,13,15 OPEN`

The canonical Phase 1–4 checkpoint is `notes/23-r22-phases1-4-closure.md`.  The complete scalar-component-5 Phase-5 closure is frozen in `notes/31-r22-component5-phase5-closure.md`, with branch details in notes 26, 27, 29, and 30.

## Theorem boundary

The target is the categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`.  A global theorem still requires either an explicit invertible associator satisfying every pentagon or rigorous obstruction of every remaining scalar branch.

The epsilon-plus half is independently excluded by the local-F determinant obstruction recorded in `notes/17-r22-epsilon-plus-local-f-obstruction.md`.

For epsilon-minus, the deep scalar frontier after the early exact reductions was

\[
\boxed{5,7,13,15}.
\]

### Phase 1 — chirality localization

For every deep scalar component, all `2^8=256` chirality assignments split exactly as

\[
\boxed{256=192\;\text{structural}+60\;\text{phase-conflict}+4\;\text{survivors}},
\]

with survivors

\[
\boxed{0,105,150,255}.
\]

### Phase 2 — D amplitude

All 16 deep branches admit explicit nonzero D-amplitude witnesses in

\[
\mu_4=\{1,i,-1,-i\},
\]

and every witness replays all 1728 D-layer matrix entries exactly.

### Phase 3 — E layer

All 16 branches have

\[
128\text{ E entries},\qquad1536\text{ support-two equations},
\]

with

\[
\operatorname{rank}A_E=126,\qquad\dim\ker A_E=2.
\]

The two-dimensional space is not the previously conjectured residual scalar gauge.  With exact weighted coordinates `p,q`, all 32 required E determinants are nonzero monomials, so the invertible locus is the genuine algebraic torus

\[
\boxed{pq\ne0}.
\]

### Phase 4 — parametric F-linear coherence

The complete F-linear quotient retains an invertible associator locus on every deep branch.

- components `5` and `13`: 21 free weighted F components;
- components `7` and `15`: 17 free components plus 4 coherence-forced-zero components.

The forced zeros for components 7 and 15 do not make any required 8x8/10x10 associator determinant identically zero.  Thus

\[
\boxed{\text{there is no obstruction in D/E/F-linear coherence}.}
\]

## Phase 5 — scalar component 5 CLOSED

All four component-5 chirality survivors are now rigorously excluded:

\[
\boxed{0,105,150,255\quad\text{all CLOSED}.}
\]

Detailed closure notes:

- mask `0`: `notes/26-r22-component5-mask0-phase5-closure.md`;
- mask `105`: `notes/27-r22-component5-mask105-phase5-closure.md`;
- mask `150`: `notes/29-r22-component5-mask150-phase5-closure.md`;
- mask `255`: `notes/30-r22-component5-mask255-phase5-closure.md`;
- component-level synthesis: `notes/31-r22-component5-phase5-closure.md`.

For masks 150 and 255, final verification was run as strict serial gates: F-coordinate reproducibility, direct provenance validation of the five local scale relations, raw-before-canonical exclusion of `z0=0`, exact 18-branch finite census, then branch-by-branch low-dimensional local certificates.  GitHub Actions runs `32173886648` and `32175782953` both completed successfully.

Every component-5 chirality exhibits the finite affine stratification

\[
\boxed{18=10+8},
\]

with ten rank-11 branches and eight rank-10 branches.  The final obstruction collapses to a small local relation core, ultimately requiring only a few neighboring final-pentagon entries per difficult branch.

Therefore

\[
\boxed{\text{scalar component 5 is completely obstructed at Phase 5}.}
\]

This is **not** yet a global non-categorifiability theorem for `R(2,2)`.

## Open frontier — Phase 5

The remaining epsilon-minus scalar components are

\[
\boxed{13,7,15}.
\]

The priority order is:

1. component `13` — same 21-free-F-component Phase-4 type as component 5;
2. component `7` — first 17-free-plus-4-forced-zero type;
3. component `15` — second 17+4 type;
4. after all scalar branches are resolved, perform a fresh global replay and write the theorem-level synthesis.

The immediate next gate is

\[
\boxed{\text{component 13 / chirality mask 0}.}
\]

No component-5 relation, coordinate identification, rank split, or local certificate may be imported into component 13 without fresh exact replay.

No Gröbner computation is authorized before each new final nonlinear kernel has been compiled, deduplicated, degree-profiled, and audited for small local contradiction certificates.  A timeout or symbolic blow-up is treated as a representation problem, not as evidence of mathematical obstruction.

## Auxiliary PAL/PCRG geometry

The edge-relation observable

\[
\eta_{uv}=c_uc_v
\]

on the two parity-K4 history graphs has projective-overlap strata

\[
0,\quad1/9,\quad1
\]

with multiplicities

\[
192,\quad60,\quad4.
\]

This matches the exact Phase-1 verifier partition mask-by-mask.  It remains an auxiliary geometric observation rather than a proof gate.  See `experiments/r22_pal_edge_geometry.py` and `notes/20-pal-edge-relation-geometry.md`.

## SCM boundary

`main` records accepted, reproducible research state.  Exploratory and potentially supersedable work remains on `agent/*` branches.  New Phase-5 scalar work must start from the latest accepted `main` state and must not rewrite frozen conclusions without a fresh exact replay and an explicit supersession note.

## Prior closed benchmark line

The earlier T0–T8 exact Fibonacci/category benchmark line remains closed.  Its negative benchmark and coherence-quotient conclusions are preserved in repository history; the current research frontier is the remaining `R(2,2)` scalar Phase-5 problem.
