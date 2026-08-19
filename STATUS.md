# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CLOSED / COMPONENT 5 PHASE 5 CLOSED / COMPONENT 13 MASKS 0,105,150 CLOSED / MASK 255 OPEN`

Canonical checkpoints:

- Phase 1–4: `notes/23-r22-phases1-4-closure.md`;
- component 5 Phase 5: `notes/31-r22-component5-phase5-closure.md`;
- component 13 / mask 0: `notes/32-r22-component13-mask0-phase5-closure.md`;
- component 13 / mask 105: `notes/33-r22-component13-mask105-phase5-closure.md`;
- component 13 / mask 150: `notes/34-r22-component13-mask150-phase5-closure.md`.

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

Therefore

\[
\boxed{\text{scalar component 5 is completely obstructed at Phase 5}.}
\]

## Phase 5 — scalar component 13

### Mask 0 — CLOSED / EXACT

Fresh replay gives a 219-cubic kernel, proves `z5^2=1/2` and its own cubic/product relations, collapses to 18 finite branches, and excludes all 18 by exact local certificates.  See `notes/32-r22-component13-mask0-phase5-closure.md`.

### Mask 105 — CLOSED / EXACT

Independent replay gives

\[
z_0^2=\frac12,
\qquad
p^3=q^3=\frac{1-i}{4},
\]

\[
z_3z_{10}=-ip^2z_0,
\qquad
z_6z_9=-q^2z_0.
\]

Its exact branch split is

\[
18=2_{\rm affine}+4_{\rm p\text{-}rank11}+4_{\rm q\text{-}rank11}+8_{\rm rank10},
\]

and all 18 are excluded.  See `notes/33-r22-component13-mask105-phase5-closure.md`.

### Mask 150 — CLOSED / EXACT

A third fully fresh replay has now closed mask 150.  Coordinate reproducibility was checked under `PYTHONHASHSEED=1,2,17` before named-coordinate certificates were accepted.

The exact local relations are

\[
\boxed{z_6^2=\frac12},
\qquad
\boxed{p^3=q^3=\frac{-1+i}{4}},
\]

\[
\boxed{z_0z_9=-p^2z_6},
\qquad
\boxed{z_1z_7=q^2z_6},
\]

hence

\[
p,q,z_0,z_1,z_6,z_7,z_9\ne0.
\]

The 18 exact finite branches split as

\[
\boxed{18=2_{\rm affine}+4_{\rm p\text{-}rank11}+4_{\rm q\text{-}rank11}+8_{\rm rank10}}.
\]

Their closures are:

- 2 branches by affine inconsistency;
- 4 p-side rank-11 branches by the fixed pure-constant cell `(XXXX;Y)_(1,0)`;
- 4 q-side rank-11 branches by the fixed pure-constant cell `(XXXX;X)_(2,5)`;
- 8 rank-10 branches by the same three fixed `g` cells `(XXXX;g)_(0,3)`, `(0,2)`, `(0,0)`.  With `r=z19,s=z20`, the first two normalize to

\[
1+4rs-4s^2=0,
\qquad
1+4rs-4r^2=0.
\]

Thus `r^2=s^2`.  The `r=s` slice gives `1=0`; the `r=-s` slice gives `s^2=1/8`, after which the fixed third cell is nonzero on every one of the eight branches.

GitHub Actions run `32219850511` reports `closed=8,total=8` for the rank-10 certificate.

Full proof audit: `notes/34-r22-component13-mask150-phase5-closure.md`.

Therefore the current component-13 status is

\[
\boxed{0,105,150\ \text{CLOSED};\qquad255\ \text{OPEN}.}
\]

Component 13 as a whole is **not yet closed**.

## Open frontier — Phase 5

The remaining epsilon-minus work is

\[
\boxed{\text{component 13 mask }255;\quad\text{components }7,15\text{ all four masks}.}
\]

Priority order:

1. component `13`, mask `255`;
2. component `7`;
3. component `15`;
4. after all scalar branches resolve, perform a fresh global replay and write the theorem-level synthesis.

The immediate next gate is

\[
\boxed{\text{component 13 / chirality mask 255: fresh Phase-5 kernel fingerprint}.}
\]

No mask-0/105/150 coordinate relation, finite-stratum split, or local certificate may be imported into mask 255 without fresh exact replay.

No Gröbner computation is authorized before each new nonlinear kernel is compiled, deduplicated, degree-profiled, and audited for small exact local certificates.  A timeout or symbolic blow-up is a representation problem, not evidence of mathematical obstruction.

## SCM boundary

`main` records accepted, reproducible research state.  Exploratory work remains on `agent/*` branches.  New Phase-5 conclusions must be backed by fresh exact replay and explicit archive notes before promotion.
