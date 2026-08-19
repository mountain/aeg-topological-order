# Status

## Current stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — PHASES 1–4 CLOSED / COMPONENTS 5,7,13 PHASE 5 CLOSED / COMPONENT 15 OPEN`

Canonical checkpoints:

- Phase 1–4: `notes/23-r22-phases1-4-closure.md`;
- component 5 Phase 5: `notes/31-r22-component5-phase5-closure.md`;
- component 13 Phase 5: `notes/36-r22-component13-phase5-closure.md`;
- component 7 masks 0/105/150/255: `notes/37...` through `notes/40...`;
- component 7 Phase 5 synthesis: `notes/41-r22-component7-phase5-closure.md`.

## Theorem boundary

The target is the categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`. The epsilon-plus half is independently excluded.

For epsilon-minus, the deep scalar components after early exact reductions are

\[
\boxed{5,7,13,15}.
\]

Phase 1 leaves exactly the chirality masks

\[
\boxed{0,105,150,255}
\]

for every deep scalar component. Phases 2–4 are canonically closed and show no obstruction.

Scalar components `5` and `13` are completely obstructed at Phase 5 by the previously archived exact certificates.

## Phase 5 — scalar component 7 CLOSED

Component `7` is a `17 active + 4 coherence-forced-zero` Phase-4 type. Every surviving chirality mask was independently fresh-compiled, coordinate-audited, and source-validated.

For masks

\[
\boxed{0,105,150,255},
\]

the fresh Phase-5 kernels all have:

- 17 active weighted F components;
- 19 kernel variables;
- 38,080 raw nonzero final entries;
- 147 unique kernel polynomials;
- total-degree profile `1` linear, `2` quadratic, `144` cubic relations;
- no generic constant contradiction.

For each mask, named F coordinates were independently audited under `PYTHONHASHSEED=1,2,17` before accepting the following source certificate.

The same two fixed final-pentagon provenances independently give

\[
(XXXXX)_{(0,0)}:\quad z_0=0,
\]

and

\[
(XXXX;1)_{(0,0)}:\quad z_0^2-\frac12=0.
\]

Therefore

\[
\boxed{-\frac12=0}.
\]

The mask-level source runs are:

- mask 0: `32230627427`;
- mask 105: `32231671110`;
- mask 150: `32232746046`;
- mask 255: `32233649046`.

A final component-level executable replays all four masks serially:

```text
experiments/r22_phase5_component7_all_masks_two_cell_certificate.py
```

GitHub Actions run `32233916428` reports

```text
mask 0    closed=True
mask 105  closed=True
mask 150  closed=True
mask 255  closed=True
SUMMARY closed=4,total=4
```

with the same two fixed cells and contradiction `-1/2` in every mask.

Therefore

\[
\boxed{\text{scalar component 7 is completely obstructed at Phase 5}.}
\]

Full synthesis: `notes/41-r22-component7-phase5-closure.md`.

## Open frontier — Phase 5

The only remaining deep epsilon-minus scalar component is

\[
\boxed{15},
\]

with masks

\[
\boxed{0,105,150,255}
\]

still open.

Priority order:

1. component `15`, mask `0` fresh Phase-5 kernel;
2. complete masks `105,150,255` one at a time;
3. perform a fresh global replay;
4. write the theorem-level synthesis for `R(2,2)`.

Component `15` is also a `17+4` Phase-4 type. The component-7 two-cell obstruction is therefore a strong hypothesis, but must not be imported without fresh exact replay.

No Gröbner computation is authorized before small exact local structure is exhausted. The 10-minute per-job guardrail remains in force.

## SCM boundary

`main` records accepted, reproducible research state. Exploratory work remains on `agent/*` branches. New conclusions require fresh exact replay and archive notes before promotion.
