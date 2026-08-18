# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CANONICALLY CLOSED / PHASE 5 OPEN`

The canonical Phase 1–4 checkpoint is `notes/23-r22-phases1-4-closure.md`. It supersedes earlier epsilon-minus branch-level conclusions that depended on mutable notebook state or on a single chosen E representative.

## Theorem boundary

The goal is the categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`. A final theorem requires either an invertible associator satisfying every pentagon or a rigorous obstruction.

The epsilon-plus half is independently excluded by the local-F determinant obstruction recorded in `notes/17-r22-epsilon-plus-local-f-obstruction.md`.

For epsilon-minus, the remaining deep scalar components are

\[
\boxed{5,7,13,15}.
\]

The fresh canonical replay closes the following stages.

### Phase 1 — chirality localization

For every deep component, all `2^8=256` chirality assignments split exactly as

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

The complete F-linear quotient retains an invertible associator locus on every deep branch. Components 5 and 13 have 21 free weighted F components. Components 7 and 15 have 17 free components plus 4 coherence-forced-zero components; those forced zeros do not make any required 8x8/10x10 associator determinant identically zero.

Therefore

\[
\boxed{\text{there is no obstruction in D/E/F-linear coherence}.}
\]

## Open frontier — Phase 5

The unresolved mathematical content is localized to pentagons with four noninvertible external inputs. After the Phase 1–4 quotient, the effective parameter scale is approximately

\[
2+21=23\quad\text{for components }5,13,
\]

and

\[
2+17=19\quad\text{for components }7,15.
\]

No Gröbner computation is authorized before the final nonlinear kernel has been compiled, deduplicated, degree-profiled, and audited for small local contradiction certificates.

A timeout or symbolic blow-up is treated as a representation problem, not as evidence of mathematical obstruction.

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

This matches the exact verifier partition mask-by-mask. It is an auxiliary geometric observation, not a proof gate. See `experiments/r22_pal_edge_geometry.py` and `notes/20-pal-edge-relation-geometry.md`.

## SCM boundary

`main` records accepted, reproducible research state. Exploratory and potentially supersedable work remains on `agent/*` branches. Phase 5 must develop from this canonical Phase 1–4 checkpoint and must not rewrite the frozen conclusions without a fresh exact replay and an explicit supersession note.

## Prior closed benchmark line

The earlier T0–T8 exact Fibonacci/category benchmark line remains closed. Its negative benchmark and coherence-quotient conclusions are preserved in repository history and the existing benchmark notes; the current research frontier is the `R(2,2)` categorification problem.
