# Status

## Current stage

`T9 R(2,2) THEOREM-CLOSURE AUDIT — PHASES 1–4 CLOSED / COMPONENTS 5,7,13,15 PHASE 5 CLOSED / GLOBAL REPLAY PENDING`

Canonical checkpoints:

- Phase 1–4: `notes/23-r22-phases1-4-closure.md`;
- component 5 Phase 5: `notes/31-r22-component5-phase5-closure.md`;
- component 13 Phase 5: `notes/36-r22-component13-phase5-closure.md`;
- component 7 Phase 5: `notes/41-r22-component7-phase5-closure.md`;
- component 15 Phase 5: `notes/42-r22-component15-phase5-closure.md`.

## Theorem boundary

The target is the categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`. The epsilon-plus half is independently excluded.

For epsilon-minus, the deep scalar components after the accepted early exact reductions are

\[
\boxed{5,7,13,15}.
\]

Phase 1 leaves exactly the chirality masks

\[
\boxed{0,105,150,255}
\]

for every deep scalar component. Phases 2–4 are canonically closed and show no obstruction.

All four deep scalar components are now obstructed at Phase 5 on the research record:

\[
\boxed{5,7,13,15\;\text{CLOSED / EXACT}.}
\]

This opens the theorem-closure audit. The global `R(2,2)` non-categorifiability statement is **not yet promoted** until the accepted branch-exhaustion chain and all component closures are replayed together from fresh state and checked for exhaustiveness.

## Phase 5 — scalar component 15 CLOSED

Component `15` is a `17 active + 4 coherence-forced-zero` Phase-4 type. Every surviving chirality mask was independently fresh-compiled and source-validated.

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

The canonical verifier

```text
experiments/r22_phase5_two_cell_certificate.py
```

avoids hard-coded F-coordinate names. In each fresh kernel it locates the same two fixed final-pentagon provenances

```text
(XXXXX)_(0,0)
(XXXX;1)_(0,0)
```

and discovers the active scale coordinate `s` from the first relation. The two cells give

\[
\boxed{s=0},
\]

and

\[
\boxed{s^2-\frac12=0},
\]

hence

\[
\boxed{-\frac12=0}.
\]

Fresh four-mask serial replay `32256425671` reports:

```text
mask 0    scale=z6  contradiction=-1/2  closed=True
mask 105  scale=z2  contradiction=-1/2  closed=True
mask 150  scale=z5  contradiction=-1/2  closed=True
mask 255  scale=z8  contradiction=-1/2  closed=True
```

Therefore

\[
\boxed{\text{scalar component 15 is completely obstructed at Phase 5}.}
\]

Full synthesis: `notes/42-r22-component15-phase5-closure.md`.

## Verification-method correction

The component-15 mask-150 audit exposed a limitation in the historical named-coordinate stability probe: the F-component partition and target pentagon polynomial were reconstructed in separate quotient builds, so implementation-dependent weighted-union-find representatives could rename the same active coordinate between builds.

This is a coordinate-label issue, not a new mathematical branch. The theorem interface is therefore changed from “this source cell is a fixed `z_j`” to the provenance-based statement “the first fixed source cell defines `s`, and the second is `s^2-1/2`.”

The component-15 closure already uses this coordinate-free verifier. Component `7` should be replayed through the same verifier during the theorem-closure audit so that the final theorem does not depend on the older named-coordinate reproducibility argument.

## Open frontier — theorem closure

No deep epsilon-minus scalar component remains locally open.

Priority order:

1. fresh coordinate-free replay of component `7`, masks `0,105,150,255`;
2. fresh replay of the accepted component `5` and `13` Phase-5 closures;
3. fresh replay of the epsilon-plus obstruction and canonical Phase-1–4 branch-exhaustion chain;
4. audit case exhaustiveness from the original `R(2,2)` coherence problem to all terminal obstructions;
5. write the theorem-level synthesis and only then decide whether to promote

\[
\boxed{R(2,2)\text{ is non-categorifiable}.}
\]

No Gröbner computation is authorized before small exact local structure is exhausted. The 10-minute per-job guardrail remains in force.

## SCM boundary

`main` records accepted, reproducible research state. Exploratory and theorem-closure work remains on `agent/*` branches. New conclusions require fresh exact replay and archive notes before promotion.
