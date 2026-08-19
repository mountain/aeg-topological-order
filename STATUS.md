# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CLOSED / COMPONENTS 5,13 PHASE 5 CLOSED / COMPONENT 7 MASK 0 CLOSED / COMPONENT 15 OPEN`

Canonical checkpoints:

- Phase 1–4: `notes/23-r22-phases1-4-closure.md`;
- component 5 Phase 5: `notes/31-r22-component5-phase5-closure.md`;
- component 13 Phase 5: `notes/36-r22-component13-phase5-closure.md`;
- component 7 / mask 0: `notes/37-r22-component7-mask0-phase5-closure.md`.

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

Phases 2–4 are canonically closed and show no obstruction. Components `5,13` have 21 active weighted F components; components `7,15` have 17 active F components plus 4 coherence-forced-zero components, while still retaining an invertible F locus.

## Phase 5 — scalar components 5 and 13 CLOSED

Scalar components `5` and `13` are completely obstructed at Phase 5. See `notes/31...` and `notes/36...`.

## Phase 5 — scalar component 7

### Mask 0 — CLOSED / EXACT

Fresh replay of the first `17+4` branch gives a substantially smaller final kernel:

- 17 active F components;
- 19 kernel variables;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- degree profile `1` linear, `2` quadratic, `144` cubic;
- no generic constant contradiction.

Coordinate reproducibility was verified across `PYTHONHASHSEED=1,2,17` before accepting the named `z0` certificate.

Two fixed final-pentagon provenances then give directly

\[
(XXXXX)_{(0,0)}:\quad z_0=0,
\]

and

\[
(XXXX;1)_{(0,0)}:\quad z_0^2-\frac12=0.
\]

Hence

\[
\boxed{-\frac12=0},
\]

an exact characteristic-zero contradiction. No finite-stratum analysis or nonlinear solve is required.

GitHub Actions run `32230627427` verifies both source relations and reports `closed=True`.

Full audit: `notes/37-r22-component7-mask0-phase5-closure.md`.

Therefore the current component-7 status is

\[
\boxed{0\ \text{CLOSED};\qquad105,150,255\ \text{OPEN}.}
\]

Component 7 as a whole is not yet closed.

## Open frontier — Phase 5

The remaining epsilon-minus work is

\[
\boxed{\text{component 7 masks }105,150,255;\quad\text{component 15 masks }0,105,150,255.}
\]

Priority order:

1. component `7`, mask `105`;
2. complete component `7` masks `150,255` one at a time;
3. component `15` one mask at a time;
4. after all scalar branches resolve, perform a fresh global replay and write the theorem-level synthesis.

The immediate next gate is

\[
\boxed{\text{component 7 / chirality mask 105: fresh Phase-5 kernel fingerprint}.}
\]

The mask-0 two-cell certificate is not assumed for mask 105. Each mask must begin from its own fresh kernel and coordinate/source audit.

No Gröbner computation is authorized before each new nonlinear kernel is compiled, deduplicated, degree-profiled, and audited for small exact local certificates. A timeout or symbolic blow-up is a representation problem, not evidence of mathematical obstruction.

## SCM boundary

`main` records accepted, reproducible research state. Exploratory work remains on `agent/*` branches. New Phase-5 conclusions must be backed by fresh exact replay and explicit archive notes before promotion.
