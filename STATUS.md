# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CLOSED / COMPONENTS 5,13 PHASE 5 CLOSED / COMPONENT 7 MASKS 0,105 CLOSED / COMPONENT 15 OPEN`

Canonical checkpoints:

- Phase 1–4: `notes/23-r22-phases1-4-closure.md`;
- component 5 Phase 5: `notes/31-r22-component5-phase5-closure.md`;
- component 13 Phase 5: `notes/36-r22-component13-phase5-closure.md`;
- component 7 / mask 0: `notes/37-r22-component7-mask0-phase5-closure.md`;
- component 7 / mask 105: `notes/38-r22-component7-mask105-phase5-closure.md`.

## Theorem boundary

The target is the categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`. The epsilon-plus half is independently excluded. For epsilon-minus the deep scalar components are `5,7,13,15`; Phase 1 leaves masks `0,105,150,255` in each, and Phases 2–4 show no obstruction.

Scalar components `5` and `13` are completely CLOSED / EXACT at Phase 5.

## Phase 5 — scalar component 7

Component `7` is the first `17 active + 4 forced-zero` Phase-4 type. Its fresh mask-0 and mask-105 kernels both have:

- 19 kernel variables;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- degree profile `1` linear, `2` quadratic, `144` cubic.

### Mask 0 — CLOSED / EXACT

After coordinate stability across `PYTHONHASHSEED=1,2,17`, two fixed cells give

\[
(XXXXX)_{(0,0)}:\ z_0=0,
\qquad
(XXXX;1)_{(0,0)}:\ z_0^2-\frac12=0,
\]

hence `-1/2=0`. Source replay: Actions run `32230627427`. Audit: `notes/37-r22-component7-mask0-phase5-closure.md`.

### Mask 105 — CLOSED / EXACT

Mask `105` was independently fresh-compiled and its named coordinates independently audited across the same three hash seeds. The same two fixed provenances were then source-validated on the mask-105 kernel itself:

\[
z_0=0,
\qquad
z_0^2-\frac12=0,
\]

again giving `-1/2=0` without localization or finite branch analysis. Fresh kernel run `32231056735`; coordinate audit `32231265402`; source certificate `32231671110`. Audit: `notes/38-r22-component7-mask105-phase5-closure.md`.

Therefore

\[
\boxed{0,105\ \text{CLOSED};\qquad150,255\ \text{OPEN}.}
\]

Component `7` as a whole is not yet closed.

## Open frontier — Phase 5

Remaining work:

\[
\boxed{\text{component 7 masks }150,255;\quad\text{component 15 masks }0,105,150,255.}
\]

Immediate next gate:

\[
\boxed{\text{component 7 / mask 150: fresh Phase-5 kernel fingerprint}.}
\]

The two-cell certificate is not assumed for mask 150; it must be established by its own fresh kernel, coordinate audit, and source validation.

No Gröbner computation is authorized before small exact local structure is exhausted. The 10-minute per-job guardrail remains in force.

## SCM boundary

`main` records accepted, reproducible research state. Exploratory work remains on `agent/*` branches. New conclusions require fresh exact replay and archive notes before promotion.
