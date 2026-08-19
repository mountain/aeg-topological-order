# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CLOSED / COMPONENTS 5,13 PHASE 5 CLOSED / COMPONENTS 7,15 OPEN`

Canonical checkpoints:

- Phase 1–4: `notes/23-r22-phases1-4-closure.md`;
- component 5 Phase 5: `notes/31-r22-component5-phase5-closure.md`;
- component 13 / mask 0: `notes/32-r22-component13-mask0-phase5-closure.md`;
- component 13 / mask 105: `notes/33-r22-component13-mask105-phase5-closure.md`;
- component 13 / mask 150: `notes/34-r22-component13-mask150-phase5-closure.md`;
- component 13 / mask 255: `notes/35-r22-component13-mask255-phase5-closure.md`;
- component 13 Phase 5 synthesis: `notes/36-r22-component13-phase5-closure.md`.

## Theorem boundary

The target is the categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`. A global theorem still requires either an explicit invertible associator satisfying every pentagon or rigorous obstruction of every remaining scalar branch.

The epsilon-plus half is independently excluded by `notes/17-r22-epsilon-plus-local-f-obstruction.md`.

For epsilon-minus, the deep scalar components after the early exact reductions are

\[
\boxed{5,7,13,15}.
\]

For every deep scalar component, Phase 1 leaves exactly the four chirality masks

\[
\boxed{0,105,150,255}.
\]

Phases 2–4 are canonically closed and show no obstruction: all 16 deep branches admit D witnesses, the E layer has a genuine two-parameter invertible torus `p*q != 0`, and the F-linear quotient retains an invertible locus.

## Phase 5 — scalar component 5 CLOSED

All four component-5 chirality survivors are rigorously excluded:

\[
\boxed{0,105,150,255\quad\text{all CLOSED}.}
\]

See `notes/31-r22-component5-phase5-closure.md` and its mask-level notes.

## Phase 5 — scalar component 13 CLOSED

All four component-13 chirality survivors are independently replayed and exactly excluded:

\[
\boxed{0,105,150,255\quad\text{all CLOSED}.}
\]

Mask-level audits are `notes/32...` through `notes/35...`; the component synthesis is `notes/36-r22-component13-phase5-closure.md`.

The final mask-255 replay establishes

\[
z_3^2=\frac12,
\qquad
p^3=\frac{1-i}{4},
\qquad
q^3=\frac{-1+i}{4},
\]

\[
z_0z_4=i q^2z_3,
\qquad
z_{17}z_{18}=-i p^2z_3,
\]

followed by the exact finite census

\[
18=2_{\rm affine}+4_{\rm p\text{-}rank11}+4_{\rm q\text{-}rank11}+8_{\rm rank10}.
\]

The p-side rank-11 family is closed by `(XXXX;X)_(5,2)`, the q-side family by `(XXXX;Y)_(0,1)`, and all eight rank-10 branches by fixed `g` cells `(0,3)`, `(0,2)`, `(0,1)` in the `r=z19,s=z20` core. GitHub Actions run `32222771962` reports `closed=8,total=8`.

Therefore

\[
\boxed{\text{scalar components 5 and 13 are completely obstructed at Phase 5}.}
\]

## Open frontier — Phase 5

The remaining epsilon-minus work is exactly

\[
\boxed{\text{components }7,15\text{, each with masks }0,105,150,255.}
\]

Priority order:

1. component `7`, mask `0`;
2. complete component `7` one mask at a time;
3. component `15` one mask at a time;
4. after all scalar branches resolve, perform a fresh global replay and write the theorem-level synthesis.

The immediate next gate is

\[
\boxed{\text{component 7 / chirality mask 0: fresh Phase-5 kernel fingerprint}.}
\]

Component `7` is the first deep scalar type whose Phase-4 F quotient has `17` free components plus `4` coherence-forced-zero components. No component-5/13 coordinate relation, finite-stratum split, or local certificate may be imported without fresh exact replay.

No Gröbner computation is authorized before each new nonlinear kernel is compiled, deduplicated, degree-profiled, and audited for small exact local certificates. A timeout or symbolic blow-up is a representation problem, not evidence of mathematical obstruction.

## SCM boundary

`main` records accepted, reproducible research state. Exploratory work remains on `agent/*` branches. New Phase-5 conclusions must be backed by fresh exact replay and explicit archive notes before promotion.
