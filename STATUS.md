# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CANONICALLY CLOSED / SCALAR COMPONENT 5 PHASE 5 CLOSED / COMPONENT 13 MASK 0 CLOSED / COMPONENTS 7,13,15 OPEN`

The canonical Phase 1–4 checkpoint is `notes/23-r22-phases1-4-closure.md`. The complete scalar-component-5 Phase-5 closure is frozen in `notes/31-r22-component5-phase5-closure.md`. Component `13`, chirality mask `0`, is independently closed in `notes/32-r22-component13-mask0-phase5-closure.md`.

## Theorem boundary

The target is the categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`. A global theorem still requires either an explicit invertible associator satisfying every pentagon or rigorous obstruction of every remaining scalar branch.

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

The two-dimensional space is not the previously conjectured residual scalar gauge. With exact weighted coordinates `p,q`, all 32 required E determinants are nonzero monomials, so the invertible locus is the genuine algebraic torus

\[
\boxed{pq\ne0}.
\]

### Phase 4 — parametric F-linear coherence

The complete F-linear quotient retains an invertible associator locus on every deep branch.

- components `5` and `13`: 21 free weighted F components;
- components `7` and `15`: 17 free components plus 4 coherence-forced-zero components.

The forced zeros for components 7 and 15 do not make any required 8x8/10x10 associator determinant identically zero. Thus

\[
\boxed{\text{there is no obstruction in D/E/F-linear coherence}.}
\]

## Phase 5 — scalar component 5 CLOSED

All four component-5 chirality survivors are rigorously excluded:

\[
\boxed{0,105,150,255\quad\text{all CLOSED}.}
\]

Detailed closure notes:

- mask `0`: `notes/26-r22-component5-mask0-phase5-closure.md`;
- mask `105`: `notes/27-r22-component5-mask105-phase5-closure.md`;
- mask `150`: `notes/29-r22-component5-mask150-phase5-closure.md`;
- mask `255`: `notes/30-r22-component5-mask255-phase5-closure.md`;
- component-level synthesis: `notes/31-r22-component5-phase5-closure.md`.

Therefore

\[
\boxed{\text{scalar component 5 is completely obstructed at Phase 5}.}
\]

## Phase 5 — component 13 / chirality mask 0 CLOSED

The first component-13 chirality survivor has now been independently excluded from a fresh Phase-5 replay:

\[
\boxed{\text{component 13 / mask 0: CLOSED / EXACT}.}
\]

The fresh kernel has 96 final pentagon blocks, 50,880 raw nonzero final entries, 23 variables, and 219 unique cubic relations. Coordinate reproducibility was verified across `PYTHONHASHSEED=1,2,17` before named `z_j` certificates were accepted.

The five local relations give

\[
\boxed{z_5^2=\frac12},
\qquad
\boxed{p^3=-\frac{1+i}{4}},
\qquad
\boxed{q^3=\frac{1-i}{4}},
\]

and

\[
\boxed{z_0z_6=-ip^2z_5},
\qquad
\boxed{z_{11}z_{14}=-q^2z_5},
\]

so

\[
\boxed{p,q,z_0,z_5,z_6,z_{11},z_{14}\ne0}.
\]

The 18 finite branches split exactly as

\[
\boxed{18=2_{\rm affine}+4_{\rm p\text{-}rank11}+4_{\rm q\text{-}rank11}+8_{\rm rank10}}.
\]

Their closures are:

- 2 branches: affine inconsistency;
- 4 p-side rank-11 branches: one-cell contradiction `(XXXX;Y)_(1,0) -> c z0 = 0` with `c != 0` and `z0 != 0`;
- 4 q-side rank-11 branches: one-cell contradiction `(XXXX;X)_(5,2) -> c z11 = 0` with `c != 0` and `z11 != 0`;
- 8 rank-10 branches: the same three `g`-cells `(XXXX;g)_(0,0)`, `(0,2)`, `(0,3)` reduce to a two-variable core `r=z17`, `s=z18`, force `r=+-s`, then give incompatible `G0` and `G2` equations.

The final 8/8 rank-10 replay completed successfully in GitHub Actions run `32181956600`.

Full proof audit and CI provenance are frozen in `notes/32-r22-component13-mask0-phase5-closure.md`.

This closes only one of the four component-13 chirality survivors. It is **not** yet a component-13 closure and **not** a global non-categorifiability theorem for `R(2,2)`.

## Open frontier — Phase 5

The remaining epsilon-minus work is

\[
\boxed{
\text{component 13 masks }105,150,255;\quad
\text{components }7,15\text{ all four masks}.
}
\]

The priority order is:

1. component `13`, mask `105`;
2. component `13`, masks `150`, then `255`, one at a time;
3. component `7`;
4. component `15`;
5. after all scalar branches are resolved, perform a fresh global replay and write the theorem-level synthesis.

The immediate next gate is

\[
\boxed{\text{component 13 / chirality mask 105: fresh Phase-5 kernel fingerprint}.}
\]

No mask-0 relation, coordinate identification, finite-stratum split, or local certificate may be imported into mask 105 without fresh exact replay.

No Gröbner computation is authorized before each new final nonlinear kernel has been compiled, deduplicated, degree-profiled, and audited for small local contradiction certificates. A timeout or symbolic blow-up is treated as a representation problem, not as evidence of mathematical obstruction.

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

This matches the exact Phase-1 verifier partition mask-by-mask. It remains an auxiliary geometric observation rather than a proof gate. See `experiments/r22_pal_edge_geometry.py` and `notes/20-pal-edge-relation-geometry.md`.

## SCM boundary

`main` records accepted, reproducible research state. Exploratory and potentially supersedable work remains on `agent/*` branches. New Phase-5 scalar work must start from the latest accepted state and must not rewrite frozen conclusions without a fresh exact replay and an explicit supersession note.

## Prior closed benchmark line

The earlier T0–T8 exact Fibonacci/category benchmark line remains closed. Its negative benchmark and coherence-quotient conclusions are preserved in repository history; the current research frontier is the remaining `R(2,2)` scalar Phase-5 problem.
